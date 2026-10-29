import importlib.util
import json
from pathlib import Path
import random
import tempfile
import unittest
from unittest import mock

from engine import examples

JOBS = {'jobs': [
    {'id': 'golden-sentimental-portrait', 'stage': 1, 'dog': 'golden', 'breed': 'Golden Retriever', 'style': 'Painterly',
     'tone': 'Sentimental', 'format': 'portrait', 'size': '64x96'},
    {'id': 'golden-warm-mug', 'stage': 2, 'dog': 'golden', 'breed': 'Golden Retriever', 'style': 'Painterly',
     'tone': 'Warm with a wink', 'format': 'mug', 'size': '96x64'},
]}


@unittest.skipUnless(importlib.util.find_spec('PIL'), 'Pillow is required')
class ExampleBatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.base = self.root / examples.ROOT
        self.base.mkdir(parents=True)
        raw = json.dumps(JOBS).encode()
        (self.base / 'jobs.json').write_bytes(raw)
        import hashlib
        patcher = mock.patch.object(examples, 'JOBS_SHA256', hashlib.sha256(raw).hexdigest())
        patcher.start(); self.addCleanup(patcher.stop)
        self.ratios = mock.patch.dict(examples.RATIOS, {'1x1': (40, 40), '4x5': (40, 50), '9x16': (36, 64)}, clear=True)
        self.ratios.start(); self.addCleanup(self.ratios.stop)

    def busy(self, rel, size, alpha=False, fmt='PNG'):
        from PIL import Image
        rng = random.Random(rel)
        mode = 'RGBA' if alpha else 'RGB'
        image = Image.new(mode, size)
        pixels = []
        for y in range(size[1]):
            for x in range(size[0]):
                rgb = (rng.randrange(256), rng.randrange(256), rng.randrange(256))
                pixels.append(rgb + ((0 if x < size[0] // 3 else 255),) if alpha else rgb)
        image.putdata(pixels)
        path = self.base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path, fmt)

    def complete_stage_one(self):
        from PIL import Image
        photo = self.base / 'photos/golden.jpg'; photo.parent.mkdir(parents=True)
        Image.new('RGB', (900, 1200), '#c8a060').save(photo, 'JPEG')
        job = 'golden-sentimental-portrait'
        self.busy(f'paintings/{job}.png', (64, 96))
        self.busy(f'cutouts/{job}.png', (64, 96), alpha=True)
        manifest = [{'file': f'paintings/{job}.png', 'kind': 'painting'}, {'file': f'cutouts/{job}.png', 'kind': 'cutout'}]
        for ratio, dims in examples.RATIOS.items():
            self.busy(f'crops/{job}-{ratio}.png', dims)
            manifest.append({'file': f'crops/{job}-{ratio}.png', 'kind': 'crop', 'ratio': ratio})
            for scene in examples.SCENES:
                self.busy(f'mockups/{job}/{scene}-{ratio}.png', dims)
                manifest.append({'file': f'mockups/{job}/{scene}-{ratio}.png', 'kind': 'mockup', 'scene': scene, 'ratio': ratio})
        for entry in manifest:
            entry.update(job=job, breed='Golden Retriever', style='Painterly', tone='Sentimental', gift='portrait', uses=['social', 'ad'])
        (self.base / 'manifest.json').write_text(json.dumps(manifest))
        (self.base / 'credits.json').write_text(json.dumps({'golden': {
            'photographer': 'A Photographer', 'source_url': 'https://unsplash.com/photos/abc', 'licence': 'Unsplash License'}}))

    def test_a_complete_stage_passes(self):
        self.complete_stage_one()
        errors, status = examples.check(self.root, 1)
        self.assertEqual(errors, [])
        self.assertTrue(all(v == 'done' for v in status.values()))

    def test_stage_two_work_during_stage_one_is_refused(self):
        self.complete_stage_one()
        self.busy('paintings/golden-warm-mug.png', (96, 64))
        errors, _ = examples.check(self.root, 1)
        self.assertTrue(any('golden-warm-mug' in e and 'later stage' in e for e in errors))

    def test_a_retry_file_is_refused(self):
        self.complete_stage_one()
        self.busy('paintings/golden-sentimental-portrait-v2.png', (64, 96))
        self.assertTrue(any('-v2' in e for e in examples.check(self.root, 1)[0]))

    def test_wrong_size_flat_image_and_opaque_cutout_are_caught(self):
        from PIL import Image
        self.complete_stage_one()
        Image.new('RGB', (64, 96), '#ffffff').save(self.base / 'mockups/golden-sentimental-portrait/home-1x1.png')
        self.busy('crops/golden-sentimental-portrait-4x5.png', (40, 40))
        self.busy('cutouts/golden-sentimental-portrait.png', (64, 96))
        errors = examples.check(self.root, 1)[0]
        self.assertTrue(any('home-1x1' in e and 'must be 40x40' in e for e in errors))
        self.assertTrue(any('4x5' in e and 'must be 40x50' in e for e in errors))
        self.assertTrue(any('cutout' in e and 'transparent' in e for e in errors))

    def test_missing_files_must_be_reported_as_failures(self):
        self.complete_stage_one()
        (self.base / 'mockups/golden-sentimental-portrait/hand-9x16.png').unlink()
        errors = examples.check(self.root, 1)[0]
        self.assertTrue(any('hand-9x16' in e and 'not reported' in e for e in errors))
        (self.base / 'failures.json').write_text(json.dumps({'mockups/golden-sentimental-portrait/hand-9x16.png': 'composite tore the frame'}))
        errors, status = examples.check(self.root, 1)
        self.assertFalse(any('hand-9x16' in e and 'not reported' in e for e in errors))
        self.assertTrue(status['mockups/golden-sentimental-portrait/hand-9x16.png'].startswith('failed'))

    def test_credits_must_be_a_free_photo_site(self):
        self.complete_stage_one()
        (self.base / 'credits.json').write_text(json.dumps({'golden': {
            'photographer': 'X', 'source_url': 'https://example.com/dog.jpg', 'licence': 'unknown'}}))
        self.assertTrue(any('Unsplash or Pexels' in e for e in examples.check(self.root, 1)[0]))

    def test_manifest_must_list_every_file_with_its_job_facts(self):
        self.complete_stage_one()
        manifest = json.loads((self.base / 'manifest.json').read_text())
        manifest[0]['tone'] = 'Warm'
        del manifest[-1]
        (self.base / 'manifest.json').write_text(json.dumps(manifest))
        errors = examples.check(self.root, 1)[0]
        self.assertTrue(any("tone 'Warm'" in e for e in errors))
        self.assertTrue(any('is missing' in e and 'manifest' in e for e in errors))

    def test_a_changed_job_list_is_refused(self):
        (self.base / 'jobs.json').write_text(json.dumps({'jobs': []}))
        with self.assertRaises(ValueError):
            examples.check(self.root, 1)


if __name__ == '__main__':
    unittest.main()
