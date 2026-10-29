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
            for role in (*assets.PRODUCT_IMAGES, 'logo'):
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
                from tests.test_offers import state as ready_state
                sale = copy.deepcopy(spec); sale['intent'] = 'buy'; sale['variation'] = 3
                sale['offers'] = [{'id':'blanket','quantity':1,'unit_price':'129.00'}]
                sale['destination'] = 'https://heartside.io/products/your-dogs-personality-blanket'
                for platform in ('instagram','facebook','tiktok'):
                    sale['captions'][platform] = "Your Dog's Personality Blanket, $129.00. {link}"
                state_ready = ready_state()
                bought, bought_manifest = media.render(root, sale, state_ready, growth.check_pack, day='2026-10-17', link_builder=growth.tracked)
                self.assertEqual(media.verify(root, bought['production'], bought), [])
                self.assertTrue(all(item['intent']=='buy' and item['offers']==sale['offers'] for item in bought['items']))
                self.assertTrue(all('utm_content='+item['creative_id'] in item['text'] for item in bought['items']))
                changed_offer = copy.deepcopy(bought); changed_offer['items'][0]['offers'][0]['quantity'] = 2
                self.assertTrue(media.verify(root, changed_offer['production'], changed_offer))
                blocked = ready_state(); blocked['store'] = []
                with self.assertRaises(ValueError):
                    media.render(root, sale, blocked, growth.check_pack, day='2026-10-17', link_builder=growth.tracked)
                wrong_sale = copy.deepcopy(sale); wrong_sale['offers'][0]['unit_price']='89.00'
                with self.assertRaises(ValueError):
                    media.render(root, wrong_sale, state_ready, growth.check_pack, day='2026-10-17', link_builder=growth.tracked)
                # The mug is shown, never sold as the hero offer.
                mug_sale = copy.deepcopy(sale); mug_sale['offers'] = [{'id':'mug','quantity':1,'unit_price':'45.00'}]
                mug_sale['destination'] = 'https://heartside.io/products/your-dogs-illustrated-mug'
                with self.assertRaises(ValueError):
                    media.render(root, mug_sale, state_ready, growth.check_pack, day='2026-10-17', link_builder=growth.tracked)
                # A retired scene asset never renders.
                retired = copy.deepcopy(spec); retired['scenes'][0]['asset'] = 'biscuit'
                with self.assertRaises(ValueError):
                    media.render(root, retired, state, growth.check_pack, day='2026-10-17')
                wrong = {**pack, 'heartside_sha': 'b' * 40}
                self.assertTrue(media.verify(root, pack['production'], wrong))
                wrong = copy.deepcopy(pack); wrong['items'][0]['text'] = 'A different claim.'
                self.assertTrue(media.verify(root, pack['production'], wrong))
                wrong = copy.deepcopy(pack); wrong['items'][0]['alt_text'] = 'A different description.'
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

    def test_a_blank_template_is_not_a_painted_render(self):
        from PIL import Image
        import random
        with tempfile.TemporaryDirectory() as temporary:
            blank = Path(temporary) / 'blank.png'
            Image.new('RGB', (600, 800), '#F4F4F4').save(blank)
            self.assertFalse(assets.painted(blank))
            busy = Path(temporary) / 'busy.png'
            rng = random.Random(1)
            image = Image.new('RGB', (256, 256))
            image.putdata([(rng.randrange(256), rng.randrange(256), rng.randrange(256)) for _ in range(256 * 256)])
            image.save(busy)
            self.assertTrue(assets.painted(busy))

    def test_an_approved_role_missing_from_the_live_gallery_stops(self):
        store = [{'title': "Your Dog's Portrait", 'url': 'https://heartside.io/products/your-dogs-portrait',
                  'images': [{'src': 'https://heartside.io/cdn/shop/files/checkout-tile-portrait.png?v=1'}]}]
        with self.assertRaises(ValueError):
            assets.product_image(store, 'portrait_black')
        with self.assertRaises(ValueError):
            assets.product_image(None, 'blanket')

    def test_generated_paths_cannot_escape_local(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                assets.local_path(Path(temporary), '../outside.png')


if __name__ == '__main__':
    unittest.main()
