import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('review_packet.py')


class ReviewPacketTest(unittest.TestCase):
    def test_packet_keeps_sections_and_treats_document_as_text(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'proposal.md'
            output = Path(directory) / 'review.html'
            source.write_text('# Context\n<script>alert(1)</script>\n## Choice\nUse a queue.\n')
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text()
            self.assertNotIn('<script>alert(1)</script>', text)
            self.assertIn('source_sha256', text)
            self.assertIn('Download feedback', text)
            self.assertIn('Use a queue.', text)
            self.assertEqual(source.read_text(), '# Context\n<script>alert(1)</script>\n## Choice\nUse a queue.\n')

    def test_empty_sections_and_literal_template_markers_survive(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'proposal.md'
            output = Path(directory) / 'review.html'
            source.write_text('# Empty\n## Literal\n__CONTEXT__ __SECTIONS__\n## Final\n')
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text()
            self.assertIn('__CONTEXT__ __SECTIONS__', text)
            self.assertEqual(text.count('<article>'), 3)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'proposal.md'; source.write_text('Text')
            output = Path(directory) / 'review.html'; output.write_text('keep')
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(output)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(), 'keep')

    def test_hardlinked_output_cannot_replace_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'proposal.md'; source.write_text('keep proposal')
            output = Path(directory) / 'alias.html'; __import__('os').link(str(source), str(output))
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(output), '--overwrite'], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_text(), 'keep proposal')

    def test_mixed_code_fences_do_not_promote_code_headings(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'proposal.md'
            source.write_text('# Doc\n````python\n~~~\n# code heading\n````\n## Real\nactual\n')
            output = Path(directory) / 'review.html'
            subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(output)], check=True, capture_output=True)
            text = output.read_text()
            self.assertEqual(text.count('<article>'), 2)
            self.assertNotIn('<h2>code heading</h2>', text)
            self.assertIn('<h2>Real</h2>', text)

    def test_missing_input_is_a_clear_failure(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '/missing/proposal.md', '--output', '/missing/review.html'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('error:', result.stderr)


if __name__ == '__main__':
    unittest.main()
