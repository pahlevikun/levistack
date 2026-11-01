import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'files.py'
spec = importlib.util.spec_from_file_location('files', SCRIPT)
f = importlib.util.module_from_spec(spec); spec.loader.exec_module(f)


class NativeFormats(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def make(self, extension, value):
        p = self.root / ('output.' + extension)
        f.write_spec(value, p); return p
    def document(self):
        return {'kind':'document','title':'Report & notes','paragraphs':['A synthetic paragraph.','Unicode café 日本語','<not markup>']}
    def test_docx_text_round_trip_and_xml_escaping(self):
        parsed = f.extract(self.make('docx', self.document()))
        self.assertEqual(parsed['paragraphs'], [self.document()['title']] + self.document()['paragraphs'])
    def test_slide_structure_round_trip(self):
        value={'kind':'presentation','slides':[{'title':'First','paragraphs':['One','Two']},{'title':'Second','paragraphs':['Three']} ]}
        self.assertEqual(f.extract(self.make('pptx',value))['slides'],value['slides'])
    def test_xlsx_cells_preserve_formula_without_claiming_calculation(self):
        value={'kind':'spreadsheet','sheets':[{'name':'Inputs','rows':[['Name','Value'],['Example',3],['Total','=B2*2'],['Flag',True]]}]}
        parsed=f.extract(self.make('xlsx',value))
        cells={x['cell']:x['value'] for x in parsed['sheets'][0]['cells']}
        self.assertEqual(cells['B3'],'=B2*2');self.assertTrue(cells['B4']);self.assertFalse(parsed['formulas_evaluated'])
    def test_sparse_cells_convert_to_csv_in_coordinates(self):
        value={'kind':'spreadsheet','sheets':[{'name':'Data','cells':[{'cell':'B2','value':9}]}]}
        parsed=f.extract(self.make('csv',value))
        self.assertEqual(parsed['sheets'][0]['rows'],[['',''],['','9']])
    def test_sheet_names_and_cell_bounds_rejected(self):
        for sheet in [{'name':'Bad/name','rows':[]},{'name':'OK','cells':[{'cell':'XFE1','value':3}]}]:
            with self.assertRaises(f.FormatError):self.make('xlsx',{'kind':'spreadsheet','sheets':[sheet]})
    def test_odt_round_trip(self):
        self.assertEqual(f.extract(self.make('odt',self.document()))['paragraphs'],[self.document()['title']]+self.document()['paragraphs'])
    def test_ods_and_odp_round_trip(self):
        sheet={'kind':'spreadsheet','sheets':[{'name':'Data','rows':[['a',2],['sum','=A2+1']]}]}
        parsed=f.extract(self.make('ods',sheet));self.assertEqual(parsed['sheets'][0]['rows'],[['a',2.0],['sum','=A2+1']])
        slides={'kind':'presentation','slides':[{'title':'Title','paragraphs':['Body']}]}
        self.assertEqual(f.extract(self.make('odp',slides))['slides'],slides['slides'])
    def test_epub_spine_omits_navigation(self):
        parsed=f.extract(self.make('epub',self.document()))
        self.assertNotIn('Contents','\n'.join(parsed['paragraphs']));self.assertIn('日本語','\n'.join(parsed['paragraphs']))
    def test_html_ignores_script_and_escapes_source(self):
        parsed=f.extract(self.make('html',self.document()))
        self.assertIn('<not markup>',parsed['paragraphs'])
        p=self.root/'unsafe.html';p.write_text('<p>Shown</p><script>hidden()</script>')
        self.assertEqual(f.extract(p)['paragraphs'],['Shown'])
    def test_delimited_quotes_newline_and_utf8(self):
        rows=[['Comma,value','Line\nbreak','日本語'],['quote"value','2','3']]
        for extension in ['csv','tsv']:
            self.assertEqual(f.extract(self.make(extension,{'kind':'spreadsheet','sheets':[{'name':'Data','rows':rows}]}))['sheets'][0]['rows'],rows)
    def test_text_json_xml_and_rtf_creation(self):
        for extension in ['txt','md','json','xml','rtf']:
            p=self.make(extension,{'kind':'document','paragraphs':['Simple plain text']})
            self.assertIn('Simple plain text',json.dumps(f.extract(p)))
    def test_rtf_unicode_and_escaped_braces(self):
        text='Café 日本語 {braces} \\ slash and 😀'
        parsed=f.extract(self.make('rtf',{'kind':'document','paragraphs':[text]}))
        self.assertEqual(parsed['paragraphs'],[text])
    def test_wav_create_inspect_real_frames(self):
        parsed=f.extract(self.make('wav',{'kind':'audio','duration_seconds':0.1,'sample_rate':8000,'frequency_hz':440}))
        self.assertEqual(parsed['frames'],800);self.assertEqual(parsed['sample_width'],2);self.assertEqual(parsed['transcription'],'not performed')
    def test_wav_bad_bounds(self):
        for key,value in [('duration_seconds',500),('sample_rate',1),('amplitude',2),('frequency_hz',999999)]:
            with self.assertRaises(f.FormatError): self.make('wav',{'kind':'audio',key:value})
    def test_svg_scene_bounds_and_external_resources(self):
        p=self.make('svg',{'kind':'image','width':320,'height':200,'shapes':[{'type':'text','x':10,'y':20,'text':'A & B'}]})
        self.assertEqual(f.extract(p)['width'],'320')
        p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="https://invalid.test/x"/></svg>')
        with self.assertRaises(f.FormatError):f.extract(p)
        with self.assertRaises(f.FormatError):self.make('svg',{'kind':'image','width':9000})
    def test_xml_entities_rejected(self):
        with self.assertRaises(f.FormatError):f.xml(b'<!DOCTYPE d [<!ENTITY e SYSTEM "file:///etc/passwd">]><d>&e;</d>')
    def test_archive_traversal_and_expansion_rejected(self):
        p=self.root/'bad.docx'
        with zipfile.ZipFile(p,'w') as z:z.writestr('../outside','not extracted')
        with self.assertRaises(f.FormatError):f.extract(p)
        with zipfile.ZipFile(p,'w') as z:z.writestr('word/document.xml',b'x'*100)
        with mock.patch.object(f,'LIMIT',10):
            with self.assertRaises(f.FormatError):f.extract(p)
        self.assertFalse((self.root.parent/'outside').exists())
    def test_output_and_symlink_guards(self):
        p=self.root/'out.txt';p.write_text('existing')
        with self.assertRaises(f.FormatError):f.output(p,lambda q:q.write_text('new'))
        link=self.root/'linked.txt';link.symlink_to(p)
        with self.assertRaises(f.FormatError):f.output(link,lambda q:q.write_text('new'),True)
        self.assertEqual(p.read_text(),'existing')
    def test_failure_does_not_publish_partial_output(self):
        p=self.root/'out.txt'
        def fail(q):q.write_text('partial');raise f.FormatError('bad backend')
        with self.assertRaises(f.FormatError):f.output(p,fail)
        self.assertFalse(p.exists())
    def test_conversion_requires_loss_acknowledgement(self):
        src=self.make('docx',self.document());dest=self.root/'converted.txt'
        with self.assertRaises(f.FormatError):f.convert(src,dest)
        f.convert(src,dest,True);self.assertIn('日本語',dest.read_text())
    def test_missing_backend_and_timeout_are_explicit(self):
        with mock.patch.object(f.shutil,'which',return_value=None):
            with self.assertRaisesRegex(f.FormatError,'missing optional backend'):f.require('missing')
        with mock.patch.object(f.subprocess,'run',side_effect=subprocess.TimeoutExpired(['fake'],1)):
            with self.assertRaisesRegex(f.FormatError,'timed out'):f.run(['fake'])
    def test_cli_reports_bad_spec_without_traceback(self):
        p=self.root/'bad.json';p.write_text('{}')
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()) as errors:
            code=f.main(['create',str(p),'--output',str(self.root/'bad.docx')])
        self.assertEqual(code,2);self.assertIn('kind',json.loads(errors.getvalue())['error'])
    @unittest.skipUnless(shutil.which('pdftotext'),'pdftotext unavailable')
    def test_native_pdf_extracts_with_real_backend(self):
        p=self.make('pdf',{'kind':'document','title':'Synthetic PDF','paragraphs':['Numbers (42) and café.']})
        text='\n'.join(f.extract(p)['paragraphs']);self.assertIn('Synthetic PDF',text);self.assertIn('Numbers (42)',text)
    def test_native_pdf_rejects_unsupported_glyphs(self):
        with self.assertRaises(f.FormatError):self.make('pdf',self.document())
    @unittest.skipUnless(shutil.which('magick'),'ImageMagick unavailable')
    def test_real_image_conversion_and_animation(self):
        a=self.make('png',{'kind':'image','width':32,'height':24,'background':'#224466'})
        b=self.root/'frame2.png';f.write_spec({'kind':'image','width':32,'height':24,'background':'#446688'},b)
        jpg=self.root/'result.jpg';f.convert(a,jpg,True)
        self.assertIn('32 24',' '.join(f.extract(jpg)['frames']))
        gif=self.root/'animation.gif';receipt=f.animate([a,b],gif,10)
        self.assertEqual(len(f.extract(gif)['frames']),2)
        self.assertEqual(receipt['frames'],2);self.assertEqual((receipt['width'],receipt['height']),(32,24))
        self.assertEqual(receipt['delays_centiseconds'],[10,10]);self.assertEqual(receipt['duration_seconds'],0.2)
        self.assertEqual(receipt['fps_effective'],10)
    @unittest.skipUnless(shutil.which('magick'),'ImageMagick unavailable')
    def test_animation_rejects_mismatched_size_and_animated_inputs(self):
        a=self.make('png',{'kind':'image','width':32,'height':24,'background':'#224466'})
        b=self.root/'different.png';f.write_spec({'kind':'image','width':16,'height':24,'background':'#446688'},b)
        with self.assertRaisesRegex(f.FormatError,'equal frame dimensions'):f.animate([a,b],self.root/'bad.gif',10)
        self.assertFalse((self.root/'bad.gif').exists())
        f.write_spec({'kind':'image','width':32,'height':24,'background':'#446688'},b)
        animated=self.root/'source.gif';f.animate([a,b],animated,10)
        with self.assertRaisesRegex(f.FormatError,'single-frame'):f.animate([a,animated],self.root/'bad.gif',10)
        self.assertFalse((self.root/'bad.gif').exists())
    @unittest.skipUnless(shutil.which('magick'),'ImageMagick unavailable')
    def test_animation_cli_reports_quantized_actual_timing(self):
        a=self.make('png',{'kind':'image','width':20,'height':20,'background':'#224466'})
        b=self.root/'second.png';f.write_spec({'kind':'image','width':20,'height':20,'background':'#446688'},b)
        with contextlib.redirect_stdout(io.StringIO()) as result:
            code=f.main(['animate',str(a),str(b),'--output',str(self.root/'result.gif'),'--fps','8'])
        receipt=json.loads(result.getvalue())
        self.assertEqual(code,0);self.assertEqual(receipt['fps_requested'],8)
        self.assertEqual(receipt['delays_centiseconds'],[12,12]);self.assertEqual(receipt['duration_seconds'],0.24)
        self.assertAlmostEqual(receipt['fps_effective'],100/12);self.assertNotEqual(receipt['fps_effective'],8)
    def test_animation_rejects_wrong_output_inventory(self):
        a=self.make('svg',{'kind':'image','width':20,'height':20})
        one=[{'width':20,'height':20,'delay_centiseconds':10}]
        with mock.patch.object(f,'frame_inventory',side_effect=[one,one,one]),mock.patch.object(f,'run'):
            with self.assertRaisesRegex(f.FormatError,'output frame count'):f.animate([a,a],self.root/'bad.gif',10)
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'ffmpeg unavailable')
    def test_real_audio_transcoding(self):
        a=self.make('wav',{'kind':'audio','duration_seconds':0.1,'sample_rate':8000})
        b=self.root/'result.flac';f.convert(a,b,True)
        parsed=f.extract(b);self.assertEqual(parsed['probe']['streams'][0]['sample_rate'],'8000')
    def test_office_backend_needs_actual_executable(self):
        src=self.make('docx',self.document())
        with mock.patch.object(f.shutil,'which',return_value=None):
            with self.assertRaisesRegex(f.FormatError,'missing optional backend'):
                f.convert(src,self.root/'out.pdf',True,backend='office')
    def test_office_backend_refuses_media(self):
        src=self.make('wav',{'kind':'audio','duration_seconds':0.1})
        with self.assertRaisesRegex(f.FormatError,'office conversion needs'):
            f.convert(src,self.root/'out.pdf',True,backend='office')
    def test_unsupported_features_and_metadata_recreation_fail(self):
        for value in [
            {'kind':'document','tables':[['not represented']]},
            {'kind':'image','format':'PNG','frames':['metadata only']},
            {'kind':'audio','channels':1,'duration_seconds':2},
            {'kind':'spreadsheet','sheets':[{'name':'Bad','rows':[[float('nan')]]}]},
        ]:
            with self.assertRaises(f.FormatError):self.make('json',value)
    def test_xml_control_character_fails_before_publication(self):
        p=self.root/'bad.docx'
        with self.assertRaises(f.FormatError):f.output(p,lambda q:f.write_spec({'kind':'document','paragraphs':['bad\x00value']},q))
        self.assertFalse(p.exists())
    def test_malformed_audio_cli_is_json_error(self):
        p=self.root/'broken.wav';p.write_bytes(b'not a wave file')
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()) as errors:
            code=f.main(['inspect',str(p)])
        self.assertEqual(code,2);self.assertIsInstance(json.loads(errors.getvalue())['error'],str)
    def test_unsupported_extension_is_explicit(self):
        p=self.root/'unknown.xyz';p.write_text('x')
        with self.assertRaisesRegex(f.FormatError,'unsupported'):f.extract(p)


if __name__=='__main__':unittest.main()
