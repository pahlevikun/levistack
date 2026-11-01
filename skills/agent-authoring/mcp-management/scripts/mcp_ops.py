#!/usr/bin/env python3
"""Plan JSON config changes, probe MCP stdio, or scaffold an SDK server. Python 3.9+."""
import argparse
import base64
import binascii
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import sys
import threading
import time

MAX_FILE = 2_000_000
MAX_FRAME = 256_000
MAX_STREAM = 2_000_000
PLACEHOLDER = re.compile(r'^\$\{[A-Z_][A-Z0-9_]*\}$')
NAME = re.compile(r'^[A-Za-z0-9_.-]{1,128}$')


class Failure(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def load(path):
    path = Path(path)
    if path.stat().st_size > MAX_FILE:
        raise Failure('JSON input exceeds the supported size')
    raw = path.read_bytes()
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise Failure('JSON input contains a duplicate object key')
            result[key] = value
        return result
    try:
        value = json.loads(raw, object_pairs_hook=unique)
    except (ValueError, UnicodeError):
        raise Failure('Input must contain valid UTF-8 JSON')
    return value, raw


def write_new(path, value):
    path = Path(path)
    if path.is_symlink():
        raise Failure('Output cannot be a symbolic link')
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)


def validate_entry(entry):
    if not isinstance(entry, dict):
        raise Failure('Server entry must be a JSON object')
    local = 'command' in entry
    remote = 'url' in entry
    if local == remote:
        raise Failure('Specify exactly one transport: command or url')
    allowed = {'command', 'args', 'env', 'cwd'} if local else {'url', 'headers'}
    if set(entry) - allowed:
        raise Failure('Entry contains fields outside the explicit portable JSON profile')
    if local:
        if not isinstance(entry['command'], str) or not entry['command'].strip():
            raise Failure('command must be a nonempty executable string')
        if not isinstance(entry.get('args', []), list) or not all(isinstance(v, str) for v in entry.get('args', [])):
            raise Failure('args must be a list of strings; no shell syntax is interpreted')
        if 'cwd' in entry and (not isinstance(entry['cwd'], str) or not entry['cwd']):
            raise Failure('cwd must be a nonempty string')
        env = entry.get('env', {})
        if not isinstance(env, dict) or not all(isinstance(k, str) and PLACEHOLDER.fullmatch(v) if isinstance(v, str) else False for k, v in env.items()):
            raise Failure('env values must be runtime placeholders such as ${SERVICE_TOKEN}')
    else:
        from urllib.parse import urlsplit
        if not isinstance(entry['url'], str):
            raise Failure('url must be a string')
        url = urlsplit(entry['url'])
        if url.scheme != 'https' or not url.hostname or url.username or url.password or url.fragment or url.query:
            raise Failure('Remote endpoint must be HTTPS without credentials, query or fragment')
        headers = entry.get('headers', {})
        if not isinstance(headers, dict) or not all(isinstance(k, str) and isinstance(v, str) and PLACEHOLDER.fullmatch(v) for k, v in headers.items()):
            raise Failure('header values must be runtime placeholders')
    return entry


def merged(config, name, entry):
    if not NAME.fullmatch(name):
        raise Failure('Server name must be a short identifier')
    if not isinstance(config, dict) or not isinstance(config.get('mcpServers', {}), dict):
        raise Failure('This profile requires a top-level JSON object with an mcpServers object')
    # Unknown runtime schemas must be adapted explicitly rather than guessed.
    result = dict(config)
    result['mcpServers'] = dict(config.get('mcpServers', {}))
    result['mcpServers'][name] = validate_entry(entry)
    return result


def plan_from_snapshots(config, raw_config, entry, raw_entry, name):
    result = merged(config, name, entry)
    before = config.get('mcpServers', {}).get(name)
    return {
        'schema': 1, 'profile': 'json-mcpServers', 'name': name,
        'base_sha256': digest(raw_config), 'entry_sha256': digest(raw_entry),
        'result_sha256': digest(canonical(result)),
        'operation': 'add' if before is None else ('unchanged' if before == entry else 'replace'),
        'changed_path': ['mcpServers', name],
        'transport': 'stdio' if 'command' in entry else 'https',
        'sensitive_values': 'omitted; original input files are required to render',
    }


def plan_config(config_path, entry_path, name):
    config, raw_config = load(config_path)
    entry, raw_entry = load(entry_path)
    return plan_from_snapshots(config, raw_config, entry, raw_entry, name)


def render_config(config_path, entry_path, plan_path, output):
    plan, _ = load(plan_path)
    if not isinstance(plan, dict) or not isinstance(plan.get('name'), str):
        raise Failure('Invalid configuration plan')
    config, raw_config = load(config_path)
    entry, raw_entry = load(entry_path)
    current = plan_from_snapshots(config, raw_config, entry, raw_entry, plan['name'])
    if current != plan:
        raise Failure('Plan no longer matches the reviewed configuration and entry')
    output_path = Path(output).absolute()
    for source in (config_path, entry_path, plan_path):
        if output_path.resolve() == Path(source).resolve():
            raise Failure('Draft output must differ from every input path')
    # Render the verified in-memory snapshots, never a second read of mutable inputs.
    result = merged(config, plan['name'], entry)
    if digest(canonical(result)) != plan['result_sha256']:
        raise Failure('Draft does not match the reviewed result')
    write_new(output_path, result)
    return {'draft_created': True, 'profile': 'json-mcpServers', 'source_changed': False,
            'notice': 'Draft may contain existing private settings; review locally before installing'}


class StdioProbe:
    def __init__(self, command, timeout, max_frame=MAX_FRAME):
        if not command or not command[0]:
            raise Failure('A server executable is required after --')
        if not 0 < timeout <= 120:
            raise Failure('timeout must be greater than zero and at most 120 seconds')
        self.deadline = time.monotonic() + timeout
        self.messages = queue.Queue(maxsize=64)
        self.failure = None
        self.max_frame = max_frame
        self.total = 0
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=False)
        self.stdout = threading.Thread(target=self._read_stdout, daemon=True)
        self.stderr = threading.Thread(target=self._drain_stderr, daemon=True)
        self.stdout.start()
        self.stderr.start()
        self.counter = 0

    def _read_stdout(self):
        pending = b''
        try:
            while True:
                chunk = os.read(self.process.stdout.fileno(), 4096)
                if not chunk:
                    self.failure = self.failure or 'Server closed stdout before the required response'
                    return
                self.total += len(chunk)
                if self.total > MAX_STREAM:
                    self.failure = 'Server stdout exceeded the probe budget'
                    return
                pending += chunk
                while b'\n' in pending:
                    frame, pending = pending.split(b'\n', 1)
                    if len(frame) > self.max_frame:
                        self.failure = 'Server message exceeded the frame limit'
                        return
                    try:
                        message = json.loads(frame)
                    except (ValueError, UnicodeError):
                        self.failure = 'Server stdout was not newline-delimited JSON-RPC'
                        return
                    if not isinstance(message, dict) or message.get('jsonrpc') != '2.0':
                        self.failure = 'Server sent an invalid JSON-RPC envelope'
                        return
                    try:
                        self.messages.put_nowait(message)
                    except queue.Full:
                        self.failure = 'Server sent too many unsolicited messages'
                        return
                if len(pending) > self.max_frame:
                    self.failure = 'Server message exceeded the frame limit'
                    return
        except (OSError, ValueError):
            self.failure = self.failure or 'Server output stream failed'

    def _drain_stderr(self):
        # Drain to avoid deadlock; never retain or echo potentially private logs.
        try:
            while os.read(self.process.stderr.fileno(), 4096):
                pass
        except (OSError, ValueError):
            pass

    def send(self, message):
        frame = canonical(message) + b'\n'
        if len(frame) > self.max_frame:
            raise Failure('Outgoing protocol message exceeded the frame limit')
        # A peer can stop reading stdin; bound writes as well as response reads.
        try:
            fd = self.process.stdin.fileno()
            os.set_blocking(fd, False)
            remaining = memoryview(frame)
            while remaining:
                if time.monotonic() >= self.deadline:
                    raise Failure('MCP protocol probe timed out during write')
                try:
                    count = os.write(fd, remaining[:4096])
                    remaining = remaining[count:]
                except BlockingIOError:
                    time.sleep(0.005)
        except (OSError, ValueError):
            raise Failure('Server stdin failed or this platform lacks nonblocking pipe support')

    def request(self, method, params=None):
        self.counter += 1
        identifier = self.counter
        self.send({'jsonrpc': '2.0', 'id': identifier, 'method': method, 'params': params or {}})
        skipped = 0
        while True:
            remaining = self.deadline - time.monotonic()
            if remaining <= 0:
                raise Failure('MCP protocol probe timed out')
            try:
                message = self.messages.get(timeout=min(remaining, 0.05))
            except queue.Empty:
                if self.failure:
                    raise Failure(self.failure)
                continue
            if 'method' in message:
                if 'id' in message:
                    if message['method'] == 'ping':
                        self.send({'jsonrpc': '2.0', 'id': message['id'], 'result': {}})
                    else:
                        self.send({'jsonrpc': '2.0', 'id': message['id'], 'error': {'code': -32601, 'message': 'Probe callback unavailable'}})
                skipped += 1
                if skipped > 64:
                    raise Failure('Too many unsolicited protocol messages')
                continue
            if type(message.get('id')) is not int or message['id'] != identifier:
                raise Failure('Server response id did not match the pending request')
            if 'error' in message:
                raise Failure('Server returned a JSON-RPC error during ' + method)
            if not isinstance(message.get('result'), dict):
                raise Failure('Server response result must be an object')
            return message['result']

    def close(self):
        try:
            # Raw nonblocking writes leave no buffered payload to flush.
            self.process.stdin.close()
            self.process.wait(timeout=0.3)
        except (OSError, subprocess.TimeoutExpired):
            self.process.terminate()
            try:
                self.process.wait(timeout=0.3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=1)
        finally:
            self.stdout.join(timeout=0.3)
            self.stderr.join(timeout=0.3)
            self.process.stdout.close()
            self.process.stderr.close()


def object_input_schema(schema):
    if not isinstance(schema, dict) or schema.get('type') != 'object':
        return False
    if 'properties' in schema and not isinstance(schema['properties'], dict):
        return False
    if 'required' in schema and (not isinstance(schema['required'], list)
                                 or not all(isinstance(v, str) for v in schema['required'])):
        return False
    return True


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def valid_uri(value):
    if not nonempty_string(value) or any(c.isspace() for c in value):
        return False
    from urllib.parse import urlsplit
    try:
        return bool(urlsplit(value).scheme)
    except ValueError:
        return False


def valid_base64(value):
    if not isinstance(value, str):
        return False
    try:
        base64.b64decode(value, validate=True)
        return True
    except (ValueError, binascii.Error):
        return False


def valid_content(block):
    if not isinstance(block, dict):
        return False
    kind = block.get('type')
    if kind == 'text':
        return isinstance(block.get('text'), str)
    if kind in ('image', 'audio'):
        return valid_base64(block.get('data')) and nonempty_string(block.get('mimeType'))
    if kind == 'resource_link':
        return valid_uri(block.get('uri')) and nonempty_string(block.get('name'))
    if kind == 'resource':
        resource = block.get('resource')
        if not isinstance(resource, dict) or not valid_uri(resource.get('uri')):
            return False
        if 'text' in resource:
            return isinstance(resource['text'], str) and 'blob' not in resource
        return valid_base64(resource.get('blob'))
    # Unsupported future content types need a verified SDK validator, not a green receipt.
    return False


def valid_call_result(result):
    if not isinstance(result.get('content'), list):
        return False
    if 'isError' in result and type(result['isError']) is not bool:
        return False
    if result.get('isError') is True:
        return False
    if 'structuredContent' in result and not isinstance(result['structuredContent'], dict):
        return False
    return all(valid_content(block) for block in result['content'])


def probe(command, version, timeout=5, required_tool=None, call_tool=None, arguments=None,
          allow_tool_call=False):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', version):
        raise Failure('Supply an explicit supported protocol date version')
    if call_tool and not allow_tool_call:
        raise Failure('Tool execution requires --allow-tool-call and an explicitly selected tool')
    for tool in (required_tool, call_tool):
        if tool is not None and not NAME.fullmatch(tool):
            raise Failure('Tool name must be a short identifier')
    client = StdioProbe(command, timeout)
    try:
        init = client.request('initialize', {'protocolVersion': version, 'capabilities': {},
                              'clientInfo': {'name': 'local-lifecycle-probe', 'version': '1.0'}})
        if init.get('protocolVersion') != version:
            raise Failure('Server negotiated a protocol version this probe was not asked to support')
        if not isinstance(init.get('serverInfo'), dict) or not all(
                nonempty_string(init['serverInfo'].get(key)) for key in ('name', 'version')):
            raise Failure('Initialize response is missing server implementation information')
        if not isinstance(init.get('capabilities'), dict) or not isinstance(init['capabilities'].get('tools'), dict):
            raise Failure('Server does not advertise the tools capability')
        client.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        names = []
        cursor = None
        cursors = set()
        for _ in range(8):
            result = client.request('tools/list', {'cursor': cursor} if cursor else {})
            tools = result.get('tools')
            if not isinstance(tools, list):
                raise Failure('tools/list response must contain a tools array')
            for tool in tools:
                if not isinstance(tool, dict) or not isinstance(tool.get('name'), str) or not NAME.fullmatch(tool['name']) or not object_input_schema(tool.get('inputSchema')):
                    raise Failure('tools/list contains an invalid tool definition')
                if tool['name'] in names:
                    raise Failure('tools/list contains duplicate tool names')
                names.append(tool['name'])
            if len(names) > 256:
                raise Failure('Tool inventory exceeded the probe limit')
            cursor = result.get('nextCursor')
            if cursor is None:
                break
            if not isinstance(cursor, str) or not cursor or len(cursor) > 4096 or cursor in cursors:
                raise Failure('Invalid or repeated tools/list pagination cursor')
            cursors.add(cursor)
        else:
            raise Failure('Tool pagination exceeded the probe limit')
        if required_tool and required_tool not in names:
            raise Failure('The required tool is not advertised')
        receipt = {'initialized': True, 'protocol_version': version, 'transport': 'stdio',
                   'tools_listed': len(names), 'tool_names': names, 'tool_called': False,
                   'host_registration_verified': False}
        if call_tool:
            if call_tool not in names:
                raise Failure('The selected tool is not advertised')
            result = client.request('tools/call', {'name': call_tool, 'arguments': arguments or {}})
            if not valid_call_result(result):
                raise Failure('Selected tool did not return a successful tool result')
            receipt.update(tool_called=True, result_blocks=len(result['content']))
        return receipt
    finally:
        client.close()


def scaffold(output, name, profile):
    if not NAME.fullmatch(name):
        raise Failure('Scaffold name must be a short identifier')
    path = Path(output)
    if path.exists() or path.is_symlink():
        raise Failure('Scaffold destination must not already exist')
    profile_import = {'mcpserver': 'from mcp.server import MCPServer\nserver = MCPServer',
                      'fastmcp': 'from mcp.server.fastmcp import FastMCP\nserver = FastMCP'}[profile]
    path.mkdir(parents=True)
    (path / 'server.py').write_text(profile_import + '(' + repr(name) + ')\n\n'
        '@server.tool()\ndef echo_message(message: str) -> str:\n'
        '    """Return a supplied message; no remote calls or persistence."""\n'
        '    if len(message) > 4096:\n        raise ValueError("message exceeds 4096 characters")\n'
        '    return message\n')
    (path / 'README.md').write_text('# ' + name + '\n\n'
        'This generated starter uses the explicitly selected `' + profile + '` SDK profile.\n'
        'Use a project-local Python environment and a compatible, pinned official MCP SDK.\n'
        'No dependency was installed by the generator. Check the SDK documentation and\n'
        'installed import before running. The current official Python SDK requires Python 3.11+.\n\n'
        'Run with the SDK CLI after installing its CLI extra in that environment:\n\n'
        '```sh\nmcp run server.py --transport stdio\n```\n\n'
        'Probe initialize and tools/list using the lifecycle skill. Tool calls are opt-in.\n'
        'Add input/output contracts, upstream authentication and bounded errors before\n'
        'connecting a real API; this echo starter is not a production authorization layer.\n')
    return {'scaffold_created': True, 'sdk_profile': profile, 'dependencies_installed': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='job', required=True)
    plan = commands.add_parser('plan')
    for key in ('config', 'entry', 'name', 'out'):
        plan.add_argument('--' + key, required=True)
    render = commands.add_parser('render')
    for key in ('config', 'entry', 'plan', 'out'):
        render.add_argument('--' + key, required=True)
    check = commands.add_parser('probe-stdio')
    check.add_argument('--protocol-version', required=True)
    check.add_argument('--timeout', type=float, default=5)
    check.add_argument('--require-tool')
    check.add_argument('--call-tool')
    check.add_argument('--arguments')
    check.add_argument('--allow-tool-call', action='store_true')
    check.add_argument('command', nargs=argparse.REMAINDER)
    starter = commands.add_parser('scaffold-python')
    starter.add_argument('--out', required=True)
    starter.add_argument('--name', required=True)
    starter.add_argument('--sdk-profile', choices=['mcpserver', 'fastmcp'], required=True)
    args = parser.parse_args(argv)
    try:
        if args.job == 'plan':
            receipt = plan_config(args.config, args.entry, args.name)
            write_new(args.out, receipt)
        elif args.job == 'render':
            receipt = render_config(args.config, args.entry, args.plan, args.out)
        elif args.job == 'scaffold-python':
            receipt = scaffold(args.out, args.name, args.sdk_profile)
        else:
            command = args.command[1:] if args.command[:1] == ['--'] else args.command
            arguments = load(args.arguments)[0] if args.arguments else {}
            if not isinstance(arguments, dict):
                raise Failure('Tool arguments must be a JSON object')
            receipt = probe(command, args.protocol_version, args.timeout, args.require_tool,
                            args.call_tool, arguments, args.allow_tool_call)
        print(json.dumps(receipt, indent=2))
        return 0
    except (Failure, OSError, ValueError) as error:
        # Never echo server stderr, config contents, command arguments, tokens or results.
        message = str(error) if isinstance(error, Failure) else 'Local file or executable operation failed'
        print(json.dumps({'ok': False, 'error': message}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
