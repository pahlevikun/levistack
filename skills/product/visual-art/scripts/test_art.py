import json
import subprocess
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('art.py')


class ArtTest(unittest.TestCase):
    def test_seed_rebuilds_source_and_new_seed_changes_it(self):
        with tempfile.TemporaryDirectory() as directory:
            outputs=[]
            for index,seed in enumerate([42,42,43]):
                output=Path(directory)/('scene%d.json'%index)
                subprocess.run([sys.executable,str(SCRIPT),'scene','--seed',str(seed),'--output',str(output)],check=True,capture_output=True)
                outputs.append(json.loads(output.read_text()))
            self.assertEqual(outputs[0],outputs[1]);self.assertNotEqual(outputs[0],outputs[2])
            self.assertEqual(len(outputs[0]['shapes']),80)

    def test_invalid_palette_and_existing_output_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'art.json';output.write_text('keep')
            result=subprocess.run([sys.executable,str(SCRIPT),'scene','--output',str(output)],capture_output=True)
            self.assertNotEqual(result.returncode,0);self.assertEqual(output.read_text(),'keep')
            result=subprocess.run([sys.executable,str(SCRIPT),'scene','--palette','red<script>','--output',str(Path(directory)/'bad.json')],capture_output=True)
            self.assertNotEqual(result.returncode,0)

    @unittest.skipUnless(shutil.which('magick'), 'ImageMagick backend unavailable')
    def test_explicit_fps_gif_command_uses_real_encoder(self):
        toolkit = Path(__file__).resolve().parents[3] / 'delivery/file-toolkit/scripts/files.py'
        with tempfile.TemporaryDirectory() as directory:
            paths = []
            for index, color in enumerate(['#123456', '#abcdef']):
                spec = Path(directory) / ('frame%d.json' % index)
                spec.write_text(json.dumps({'kind':'image','width':32,'height':32,'background':color,'shapes':[]}))
                frame = Path(directory) / ('frame%d.png' % index)
                subprocess.run([sys.executable,str(toolkit),'create',str(spec),'--output',str(frame)],check=True,capture_output=True)
                paths.append(str(frame))
            output = Path(directory) / 'animation.gif'
            result = subprocess.run([sys.executable,str(SCRIPT),'gif']+paths+['--fps','8','--toolkit',str(toolkit),'--output',str(output)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn(output.read_bytes()[:6],[b'GIF87a',b'GIF89a'])

    def test_interactive_art_is_self_contained(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'explore.html'
            subprocess.run([sys.executable,str(SCRIPT),'explore','--output',str(output)],check=True,capture_output=True)
            text=output.read_text();self.assertIn('canvas.toDataURL',text);self.assertIn('lcg-circles-v1',text);self.assertNotIn('<script src=',text)


if __name__=='__main__': unittest.main()
