import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import growth
from engine import assets, media


@unittest.skipUnless(importlib.util.find_spec('PIL') and shutil.which('ffmpeg') and shutil.which('ffprobe'),
                     'Pillow and FFmpeg are required for the media integration test')
class MediaTests(unittest.TestCase):
    def test_render_cache_checksums_and_failed_build_preserve_previous_output(self):
        from PIL import Image, ImageFont
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = root / 'local/assets/test'; cache.mkdir(parents=True)
            records = {}
            for role in ('mug_dog', 'mug_note', 'biscuit', 'biscuit_entryway', 'logo'):
                path = cache / (role + '.png')
                Image.new('RGB', (700, 700), '#F0C0C0').save(path)
                records[role] = {'path': str(path.relative_to(root)), 'sha256': assets.sha256(path)}
            for role in ('display_font', 'body_font'):
                path = cache / (role + '.ttf')
                shutil.copyfile(ImageFont.truetype('DejaVuSans.ttf', 20).path, path)
                records[role] = {'path': str(path.relative_to(root)), 'sha256': assets.sha256(path)}
            source = {'heartside_sha': 'a' * 40, 'assets': records}
            spec = json.loads((Path(growth.HERE) / 'campaigns/waits-at-the-door.json').read_text())
            spec.pop('voiceover', None)
            for scene in spec['scenes']:
                scene['seconds'] = 1
            state = {'sha': 'a' * 40, 'rules_ok': True}
            with patch('engine.media.assets.prepare', return_value=source):
                pack, manifest = media.render(root, spec, state, growth.check_pack, day='2026-10-17')
                self.assertEqual(media.verify(root, pack['production'], pack), [])
                self.assertTrue(media.REQUIRED_ROLES <= manifest['files'].keys())
                self.assertEqual(manifest['duration_seconds'], 3)
                with patch('engine.media.subprocess.run', side_effect=AssertionError('cached render must not encode again')):
                    again, cached = media.render(root, spec, state, growth.check_pack, day='2026-10-17')
                self.assertEqual(pack, again)
                self.assertEqual(manifest, cached)
                wrong = {**pack, 'heartside_sha': 'b' * 40}
                self.assertTrue(media.verify(root, pack['production'], wrong))
                wrong = copy.deepcopy(pack); wrong['items'][0]['text'] = 'A different claim.'
                self.assertTrue(media.verify(root, pack['production'], wrong))
                output = assets.local_path(root, manifest['files']['cover']['path'])
                original = output.read_bytes()
                output.write_bytes(original + b'changed')
                self.assertTrue(media.verify(root, pack['production'], pack))
                output.write_bytes(original)
                with patch('engine.media.subprocess.run', side_effect=subprocess.CalledProcessError(1, 'ffmpeg')):
                    changed = copy.deepcopy(spec); changed['variation'] = 2
                    with self.assertRaises(subprocess.CalledProcessError):
                        media.render(root, changed, state, growth.check_pack, day='2026-10-17')
                self.assertEqual(output.read_bytes(), original)
                self.assertEqual(media.verify(root, pack['production'], pack), [])

    def test_generated_paths_cannot_escape_local(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                assets.local_path(Path(temporary), '../outside.png')


if __name__ == '__main__':
    unittest.main()
