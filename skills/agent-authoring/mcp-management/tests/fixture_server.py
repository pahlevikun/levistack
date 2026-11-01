"""Synthetic MCP peer for lifecycle tests; not a server implementation template."""
import json
import sys
import time

mode = sys.argv[1] if len(sys.argv) > 1 else 'valid'
initialized = False
for line in sys.stdin:
    request = json.loads(line)
    method = request['method']
    identifier = request.get('id')
    if mode == 'hang':
        time.sleep(10)
    if mode == 'exit':
        raise SystemExit(0)
    if mode == 'malformed':
        print('private log must not be reflected', flush=True)
        raise SystemExit(0)
    if mode == 'oversized':
        print('x' * 300000, flush=True)
        raise SystemExit(0)
    if method == 'initialize':
        result = {'protocolVersion': '1900-01-01' if mode == 'wrong-version' else request['params']['protocolVersion'],
                  'serverInfo': {'name': 'fixture', 'version': '1'},
                  'capabilities': {} if mode == 'no-tools' else {'tools': {}}}
        if mode == 'missing-server-version':
            result['serverInfo'].pop('version')
    elif method == 'notifications/initialized':
        initialized = True
        continue
    elif method == 'tools/list':
        if not initialized:
            raise SystemExit(7)
        tool = {'name': 'echo_message', 'inputSchema': {'type': 'object'}}
        if mode == 'paginated' and not request['params'].get('cursor'):
            result = {'tools': [tool], 'nextCursor': 'next'}
        elif mode == 'paginated':
            result = {'tools': [{'name': 'other_tool', 'inputSchema': {'type': 'object'}}]}
        elif mode == 'repeat-cursor':
            result = {'tools': [], 'nextCursor': 'same'}
        elif mode == 'bad-tool':
            result = {'tools': [{'name': 'echo_message'}]}
        elif mode == 'nonobject-input':
            result = {'tools': [{'name': 'echo_message', 'inputSchema': {'type': 'string'}}]}
        elif mode == 'empty':
            result = {'tools': []}
        else:
            result = {'tools': [tool]}
    elif method == 'tools/call':
        result = {'content': [{'type': 'text', 'text': request['params']['arguments'].get('message', '')}],
                  'isError': mode == 'tool-error'}
        if mode == 'missing-text':
            result['content'] = [{'type': 'text'}]
        if mode == 'bad-binary':
            result['content'] = [{'type': 'image', 'data': 'not base64!', 'mimeType': 'image/png'}]
        if mode == 'bad-iserror':
            result['isError'] = 'false'
    else:
        continue
    if mode == 'rpc-error':
        response = {'jsonrpc': '2.0', 'id': identifier, 'error': {'code': -32603, 'message': 'private failure detail'}}
    else:
        response = {'jsonrpc': '2.0', 'id': 99 if mode == 'wrong-id' else identifier, 'result': result}
    print(json.dumps(response), flush=True)
    if mode == 'blocked-call' and method == 'tools/list':
        time.sleep(10)
