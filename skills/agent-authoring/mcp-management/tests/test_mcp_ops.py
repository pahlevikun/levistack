import ast
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('mcp_ops', ROOT / 'scripts/mcp_ops.py')
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)
VERSION = '2025-06-18'


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.config = self.root / 'config.json'
        self.entry = self.root / 'entry.json'
        self.plan = self.root / 'plan.json'
        self.draft = self.root / 'draft.json'
        self.original = {'theme': 'dark', 'other': {'private': 'not-for-report'},
                         'mcpServers': {'untouched': {'url': 'https://example.test/mcp'}}}
        self.config.write_text(json.dumps(self.original))
        self.entry.write_text(json.dumps({'command': 'python3', 'args': ['server.py'],
                                         'env': {'TOKEN': '${SERVICE_TOKEN}'}}))

    def tearDown(self):
        self.temp.cleanup()

    def test_plan_omits_private_values_and_render_preserves_other_settings(self):
        plan = ops.plan_config(self.config, self.entry, 'sample')
        self.assertEqual(plan['operation'], 'add')
        self.assertNotIn('not-for-report', json.dumps(plan))
        self.assertNotIn('${SERVICE_TOKEN}', json.dumps(plan))
        ops.write_new(self.plan, plan)
        receipt = ops.render_config(self.config, self.entry, self.plan, self.draft)
        actual = json.loads(self.draft.read_text())
        self.assertEqual(actual['other'], self.original['other'])
        self.assertEqual(actual['mcpServers']['untouched'], self.original['mcpServers']['untouched'])
        self.assertEqual(json.loads(self.config.read_text()), self.original)
        self.assertFalse(receipt['source_changed'])
        self.assertEqual(stat.S_IMODE(self.draft.stat().st_mode), 0o600)

    def test_stale_config_or_entry_cannot_render(self):
        ops.write_new(self.plan, ops.plan_config(self.config, self.entry, 'sample'))
        self.config.write_text('{}')
        with self.assertRaisesRegex(ops.Failure, 'no longer matches'):
            ops.render_config(self.config, self.entry, self.plan, self.draft)
        self.assertFalse(self.draft.exists())

    def test_tampered_plan_cannot_render(self):
        plan = ops.plan_config(self.config, self.entry, 'sample')
        plan['changed_path'] = ['other']
        ops.write_new(self.plan, plan)
        with self.assertRaises(ops.Failure):
            ops.render_config(self.config, self.entry, self.plan, self.draft)

    def test_render_uses_the_same_snapshots_that_were_verified(self):
        for input_path in [self.config, self.entry]:
            with self.subTest(input_path=input_path.name):
                self.config.write_text(json.dumps(self.original))
                self.entry.write_text(json.dumps({'command': 'python3'}))
                reviewed = ops.plan_config(self.config, self.entry, 'sample')
                self.plan.write_text(json.dumps(reviewed))
                original_load = ops.load
                reads = []

                def read_then_change(path):
                    value, raw = original_load(path)
                    if Path(path) == input_path:
                        reads.append(path)
                        changed = dict(value)
                        changed['theme' if input_path == self.config else 'command'] = 'changed-after-snapshot'
                        input_path.write_text(json.dumps(changed))
                    return value, raw

                with patch.object(ops, 'load', side_effect=read_then_change):
                    ops.render_config(self.config, self.entry, self.plan, self.draft)
                self.assertEqual(len(reads), 1)
                actual = json.loads(self.draft.read_text())
                self.assertEqual(ops.digest(ops.canonical(actual)), reviewed['result_sha256'])
                self.draft.unlink()

    def test_existing_output_and_input_overwrite_are_refused(self):
        ops.write_new(self.plan, ops.plan_config(self.config, self.entry, 'sample'))
        with self.assertRaises(ops.Failure):
            ops.render_config(self.config, self.entry, self.plan, self.config)
        self.draft.write_text('keep')
        with self.assertRaises(FileExistsError):
            ops.render_config(self.config, self.entry, self.plan, self.draft)
        self.assertEqual(self.draft.read_text(), 'keep')

    def test_profile_validation(self):
        invalid = [{'command': 'x', 'url': 'https://example.test'}, {'command': ''},
                   {'command': 'x', 'args': 'shell text'}, {'command': 'x', 'env': {'TOKEN': 'actual-secret'}},
                   {'url': 'http://example.test'}, {'url': 'https://user:pass@example.test'},
                   {'url': 'https://example.test?token=secret'}, {'url': 'https://example.test', 'headers': {'Authorization': 'secret'}},
                   {'command': 'x', 'unknown': True}]
        for entry in invalid:
            with self.subTest(entry=entry), self.assertRaises(ops.Failure):
                ops.validate_entry(entry)
        for entry in [{'command': 'x'}, {'url': 'https://example.test/mcp', 'headers': {'Authorization': '${AUTH_HEADER}'}}]:
            self.assertEqual(ops.validate_entry(entry), entry)

    def test_duplicate_json_keys_rejected(self):
        self.entry.write_text('{"command":"one","command":"two"}')
        with self.assertRaisesRegex(ops.Failure, 'duplicate'):
            ops.load(self.entry)

    def test_scaffold_profiles_parse_and_never_overwrite(self):
        for profile in ['mcpserver', 'fastmcp']:
            target = self.root / profile
            receipt = ops.scaffold(target, 'sample-server', profile)
            ast.parse((target / 'server.py').read_text())
            self.assertFalse(receipt['dependencies_installed'])
            with self.assertRaises(ops.Failure):
                ops.scaffold(target, 'sample-server', profile)


class ProbeTests(unittest.TestCase):
    def command(self, mode='valid'):
        return [sys.executable, str(ROOT / 'tests/fixture_server.py'), mode]

    def test_initialize_notification_and_inventory(self):
        result = ops.probe(self.command(), VERSION, required_tool='echo_message')
        self.assertTrue(result['initialized'])
        self.assertEqual(result['tools_listed'], 1)
        self.assertFalse(result['tool_called'])
        self.assertFalse(result['host_registration_verified'])

    def test_paginated_tools(self):
        result = ops.probe(self.command('paginated'), VERSION)
        self.assertEqual(result['tools_listed'], 2)

    def test_untrusted_protocol_failures(self):
        for mode in ['exit', 'malformed', 'oversized', 'wrong-version', 'no-tools', 'wrong-id', 'rpc-error', 'bad-tool', 'repeat-cursor']:
            with self.subTest(mode=mode), self.assertRaises(ops.Failure) as failure:
                ops.probe(self.command(mode), VERSION, timeout=1)
            self.assertNotIn('private', str(failure.exception))

    def test_malformed_required_protocol_structures_are_rejected(self):
        for mode in ['missing-server-version', 'nonobject-input']:
            with self.subTest(mode=mode), self.assertRaises(ops.Failure):
                ops.probe(self.command(mode), VERSION)
        for mode in ['missing-text', 'bad-binary', 'bad-iserror']:
            with self.subTest(mode=mode), self.assertRaisesRegex(ops.Failure, 'successful tool result'):
                ops.probe(self.command(mode), VERSION, call_tool='echo_message', allow_tool_call=True)

    def test_supported_content_block_validation(self):
        for block in [{'type': 'text', 'text': ''},
                      {'type': 'image', 'data': 'YQ==', 'mimeType': 'image/png'},
                      {'type': 'audio', 'data': 'YQ==', 'mimeType': 'audio/wav'},
                      {'type': 'resource_link', 'name': 'note', 'uri': 'note://one'},
                      {'type': 'resource', 'resource': {'uri': 'note://one', 'text': 'one'}},
                      {'type': 'resource', 'resource': {'uri': 'note://one', 'blob': 'YQ=='}}]:
            with self.subTest(block=block):
                self.assertTrue(ops.valid_content(block))
        for block in [{}, {'type': 'text'}, {'type': 'audio', 'data': 'bad!', 'mimeType': 'audio/wav'},
                      {'type': 'resource_link', 'name': 'note', 'uri': 'relative'},
                      {'type': 'resource', 'resource': {'uri': 'note://one'}},
                      {'type': 'unknown', 'text': 'one'}]:
            with self.subTest(block=block):
                self.assertFalse(ops.valid_content(block))

    def test_empty_inventory_can_be_healthy_but_missing_required_tool_fails(self):
        self.assertEqual(ops.probe(self.command('empty'), VERSION)['tools_listed'], 0)
        with self.assertRaisesRegex(ops.Failure, 'required tool'):
            ops.probe(self.command('empty'), VERSION, required_tool='needed')

    def test_timeout_is_a_protocol_failure(self):
        with self.assertRaisesRegex(ops.Failure, 'timed out'):
            ops.probe(self.command('hang'), VERSION, timeout=0.1)

    def test_tool_call_requires_explicit_permission_and_receipt_omits_payload(self):
        with self.assertRaisesRegex(ops.Failure, 'requires'):
            ops.probe(self.command(), VERSION, call_tool='echo_message')
        result = ops.probe(self.command(), VERSION, call_tool='echo_message',
                           arguments={'message': 'secret-argument'}, allow_tool_call=True)
        self.assertTrue(result['tool_called'])
        self.assertNotIn('secret-argument', json.dumps(result))
        with self.assertRaisesRegex(ops.Failure, 'successful tool result'):
            ops.probe(self.command('tool-error'), VERSION, call_tool='echo_message', allow_tool_call=True)

    def test_outgoing_budget_and_stalled_reader_are_bounded(self):
        with self.assertRaisesRegex(ops.Failure, 'Outgoing protocol message'):
            ops.probe(self.command(), VERSION, call_tool='echo_message',
                      arguments={'message': 'x' * 300000}, allow_tool_call=True)
        with self.assertRaisesRegex(ops.Failure, 'timed out'):
            ops.probe(self.command('blocked-call'), VERSION, timeout=0.2,
                      call_tool='echo_message', arguments={'message': 'x' * 200000},
                      allow_tool_call=True)

    def test_cli_suppresses_private_stderr_and_bad_file_details(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = ops.main(['plan', '--config', '/does/not/exist-secret', '--entry', 'none', '--name', 'x', '--out', 'none'])
        self.assertEqual(result, 2)
        self.assertNotIn('exist-secret', stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
