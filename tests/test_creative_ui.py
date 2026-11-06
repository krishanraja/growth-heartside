import copy
import datetime as dt
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from engine import creative_ui as ui
from tests.ui_fixtures import evidence, font_path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'factory'))
import ui_layout
import textfit

TODAY = dt.date(2026, 11, 6)


class PlacementReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.release, self.review = evidence(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def errors(self, release=None, review=None):
        return ui.errors(self.root, release or self.release, review or self.review, today=TODAY)

    def test_complete_evidence_passes_and_unreviewed_stub_holds(self):
        self.assertEqual(self.errors(), [])
        self.assertTrue(self.errors(review=ui.review_stub(self.release)))

    def test_final_copy_cover_account_label_and_paid_changes_invalidate_review(self):
        for field, value in [('description', 'Longer caption'), ('account', 'another'),
                             ('disclosures', ['AI']), ('mode', 'paid'), ('destination', 'https://example.org'),
                             ('caption_route', 'native'), ('crop_anchors', [50, 60])]:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.release); changed[field] = value
                self.assertTrue(any('changed since review' in e for e in self.errors(changed)))
        cover = self.root / self.release['exports'][1]['path']
        cover.write_bytes(b'changed cover')
        self.assertTrue(self.errors())

    def test_wrong_file_and_copy_cannot_borrow_receipt(self):
        folder = self.root / 'local/creative-ui' / self.release['revision']
        other = self.root / 'other.mp4'; other.write_bytes(b'other')
        result = ui.check_files(self.root, folder / 'F99.release.json', folder / 'F99.review.json',
                                expected_media=other, expected_copy='different', today=TODAY)
        self.assertTrue(any('file being released' in p for p in result))
        self.assertTrue(any('publishing copy' in p for p in result))

    def test_missing_normal_view_or_device_and_false_check_hold(self):
        for state in ('normal', 'busiest', 'non_owner', 'search_entry', 'playback'):
            review = copy.deepcopy(self.review)
            review['observations'] = [o for o in review['observations'] if o['state'] != state]
            self.assertTrue(self.errors(review=review))
        changed = copy.deepcopy(self.release); changed['devices'].append('ios')
        review = copy.deepcopy(self.review); review['binding'] = ui.digest(changed)
        self.assertTrue(any('ios missing' in e for e in self.errors(changed, review)))
        review = copy.deepcopy(self.review); review['checks']['sound_off'] = 'fail'
        self.assertTrue(self.errors(review=review))

    def test_expanded_occlusion_is_observed_not_required_to_be_unobscured(self):
        self.assertEqual(self.errors(), [])
        review = copy.deepcopy(self.review)
        next(o for o in review['observations'] if o['state'] == 'expanded')['verdict'] = 'unverified'
        self.assertTrue(self.errors(review=review))

    def test_stale_future_and_malformed_evidence_hold(self):
        for field, date in [('checked_on', '2026-11-07'), ('overlay_captured_on', '2026-10-01'), ('checked_on', '')]:
            review = copy.deepcopy(self.review); review[field] = date
            self.assertTrue(self.errors(review=review))
        for field, value in [('observations', [None]), ('checks', None), ('devices', [None])]:
            release, review = copy.deepcopy(self.release), copy.deepcopy(self.review)
            (release if field == 'devices' else review)[field] = value
            self.assertTrue(self.errors(release, review))

    def test_paid_requires_its_own_ad_preview(self):
        self.release['mode'] = 'paid'; self.review['binding'] = ui.digest(self.release)
        self.assertTrue(any('ad_preview' in e for e in self.errors()))
        self.review['observations'].append({**self.review['observations'][0], 'state': 'ad_preview', 'verdict': 'pass'})
        self.assertEqual(self.errors(), [])

    def test_factory_release_gate_requires_the_placement_review(self):
        import lock
        with patch.object(lock, 'check', return_value=([], [])), patch.object(lock, 'media', return_value=[]), \
             patch.object(lock, 'ledger', return_value={'records': []}), patch.object(lock, 'ramp', return_value=('ok', 'test')):
            errors, _ = lock.gate({'id': 'synthetic'}, 'nonexistent.mp4')
        self.assertTrue(any('placement UI review required' in e for e in errors))

    def test_review_and_evidence_survive_a_runner_checkpoint(self):
        from engine import state_store
        state_store.export(self.root, 'local/backups/ui.tgz')
        restored = self.root / 'another-runner'; restored.mkdir()
        state_store.restore(restored, self.root / 'local/backups/ui.tgz')
        base = restored / 'local/creative-ui' / self.release['revision']
        self.assertEqual(ui.check_files(restored, base / 'F99.release.json', base / 'F99.review.json', today=TODAY), [])


class LayoutTests(unittest.TestCase):
    def test_actual_caption_pixels_fit_and_long_caption_is_rejected(self):
        from PIL import Image, ImageFont
        font = ImageFont.truetype(font_path(), 54)
        image = Image.new('RGBA', (1080, 1920))
        ui_layout.caption(image, 'The mug got another kiss.', font)
        self.assertTrue(ui.contained(image.getbbox()))
        self.assertLessEqual(image.getbbox()[2], 865)  # Pillow rectangle endpoint is inclusive.
        with self.assertRaises(ValueError):
            ui_layout.caption(Image.new('RGBA', (1080, 1920)), 'A long caption ' * 12, font)
        with self.assertRaises(ValueError):
            ui_layout.caption(image, 'A caption.', font, y=1440)

    def test_chat_latest_payoff_visible_and_oversize_never_silently_disappears(self):
        from PIL import Image
        blocks = [Image.new('RGBA', (756, 180)) for _ in range(8)]
        visible = ui_layout.recent_blocks(blocks)
        self.assertLessEqual(len(visible), 3)
        self.assertIs(visible[-1][0], blocks[-1])
        self.assertTrue(all(510 <= y and y + block.height <= 1152 for block, y in visible))
        with self.assertRaises(ValueError):
            ui_layout.recent_blocks([Image.new('RGBA', (756, 700))])

    def test_locked_geometry_stays_locked_but_new_revision_uses_profile(self):
        locked = {'id': 'F01', 'status': 'locked', 'fingerprint': 'same'}
        self.assertFalse(ui_layout.enabled({'id': 'F01'}, locked, 'same'))
        self.assertTrue(ui_layout.enabled({'id': 'F01', 'ui_profile': ui.REVISION}, locked, 'new'))
        self.assertTrue(ui_layout.enabled({'id': 'F01-new'}, locked, 'same'))
        with self.assertRaises(ValueError):
            ui_layout.enabled({'id': 'new', 'ui_profile': 'typo'})


if __name__ == '__main__':
    unittest.main()
