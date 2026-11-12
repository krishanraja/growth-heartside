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
        self.assertTrue(ui.contained(image.getbbox(), ui.SUBTITLES))
        self.assertLessEqual(image.getbbox()[2], 820)  # left of the action rail (corpus 3.5)
        with self.assertRaises(ValueError):
            ui_layout.caption(Image.new('RGBA', (1080, 1920)), 'A long caption ' * 12, font)
        with self.assertRaises(ValueError):
            ui_layout.caption(image, 'A caption.', font, y=1440)

    def test_chat_latest_payoff_visible_and_oversize_never_silently_disappears(self):
        from PIL import Image
        blocks = [Image.new('RGBA', (700, 180)) for _ in range(8)]
        visible = ui_layout.recent_blocks(blocks)
        self.assertLessEqual(len(visible), 3)
        self.assertIs(visible[-1][0], blocks[-1])
        self.assertTrue(all(ui_layout.CHAT_TOP <= y and y + block.height <= ui.CRITICAL[3] for block, y in visible))
        built = ui_layout.chat_blocks(blocks)
        self.assertIs(built[-1][0], blocks[-1])
        self.assertEqual(built[-1][1] + blocks[-1].height, ui.CRITICAL[3])   # the newest message ends above the bottom UI
        with self.assertRaises(ValueError):
            ui_layout.recent_blocks([Image.new('RGBA', (756, 700))])

    def test_locked_geometry_stays_locked_but_new_revision_uses_profile(self):
        locked = {'id': 'F01', 'status': 'locked', 'fingerprint': 'same'}
        self.assertFalse(ui_layout.enabled({'id': 'F01'}, locked, 'same'))
        self.assertTrue(ui_layout.enabled({'id': 'F01', 'ui_profile': ui.REVISION}, locked, 'new'))
        self.assertFalse(ui_layout.enabled({'id': 'F01-new'}, locked, 'same'))
        self.assertFalse(ui_layout.enabled({'id': 'F01'}, locked, 'pre-existing-drift'))
        self.assertTrue(ui_layout.enabled({'id': 'F99'}, None, 'new'))
        self.assertTrue(ui_layout.enabled({'id': 'F34', 'ui_profile': 'social-ui-2026-11-06-v1'}, locked, 'same'))
        with self.assertRaises(ValueError):
            ui_layout.enabled({'id': 'new', 'ui_profile': 'typo'})


class CorpusProfileTests(unittest.TestCase):
    """The 12 Nov corpus (knowledge/social-media-creative-production-corpus-2026-11-12.md), as code."""

    def test_profile_matches_the_corpus_numbers_and_the_stored_corpus(self):
        import hashlib
        self.assertEqual(ui.CRITICAL, (120, 330, 820, 1180))
        self.assertEqual(ui.SUBTITLES, (130, 940, 820, 1160))
        self.assertEqual(ui.HOOK, (140, 360, 820, 720))
        self.assertEqual(ui.COVER_GRID, (0, 240, 1080, 1680))
        for region in (ui.SUBTITLES, ui.HOOK, ui.LOGO, ui.FINAL_LINE):
            self.assertTrue(ui.contained(region, (0, 0, 1080, 1920)))
        self.assertTrue(ui.contained(ui.CRITICAL, ui.COVER_GRID))   # a safe first frame also survives the grid crop
        stored = Path(__file__).resolve().parents[1] / ui.CORPUS
        self.assertEqual(hashlib.sha256(stored.read_bytes()).hexdigest(), ui.CORPUS_SHA256)

    def test_a_compliant_layout_passes_and_each_breach_holds(self):
        from tests.ui_fixtures import layout
        self.assertEqual(ui.layout_errors(layout()), ([], []))
        def held(element=None, **changes):
            data = layout(**changes)
            if element:
                data['elements'][element[0]].update(element[1])
            return ui.layout_errors(data)[0]
        self.assertTrue(held((2, {'box': [130, 960, 900, 1100]})))                      # under the action rail
        self.assertTrue(held((2, {'box': [130, 1300, 820, 1440]})))                     # under the bottom caption
        self.assertTrue(held((1, {'box': [160, 250, 800, 320]})))                       # under the top tabs
        self.assertTrue(held((2, {'lines': 3})))
        self.assertTrue(held((2, {'text': 'one two three four five six seven eight'})))
        self.assertTrue(held((2, {'px': 38})))
        self.assertTrue(held((1, {'text': ' '.join(['word'] * 13)})))
        self.assertTrue(held((1, {'box': [130, 960, 820, 1100], 'start': 2, 'end': 3})))   # two texts collide
        dead = layout(); dead['elements'][0]['end'] = 3.0; dead['elements'][2]['end'] = 3.0; dead['elements'][3]['start'] = 3.0
        self.assertTrue(ui.layout_errors(dead)[0])                                       # a 7 s silent product outro
        self.assertTrue(held((3, {'start': 8.0})))                                       # under the 3 s floor
        self.assertTrue(held(profile='social-ui-2026-11-06-v1'))
        logo_only = layout(elements=[{'role': 'logo', 'box': [140, 360, 400, 420], 'start': 0, 'end': 1},
                                     {'role': 'picture', 'box': [0, 0, 1080, 1920], 'start': 1, 'end': 10}])
        self.assertTrue(any('logo-only cold open' in p for p in ui.layout_errors(logo_only)[0]))
        moving = layout(elements=layout()['elements'] + [
            {'role': 'label', 'box': [140, 360, 820, 440], 'start': 0, 'end': 1, 'text': '6:00 AM'},
            {'role': 'label', 'box': [140, 400, 820, 480], 'start': 1, 'end': 2, 'text': '9:00 AM'}])
        self.assertTrue(any('labels move' in p for p in ui.layout_errors(moving)[0]))
        feed = {'profile': ui.REVISION, 'canvas': [1080, 1350], 'duration': 0, 'elements': [
            {'role': 'hook', 'box': [40, 40, 1040, 200], 'start': 0, 'end': 0, 'text': 'A line'}]}
        self.assertTrue(any('feed margin' in p for p in ui.layout_errors(feed)[0]))

    def test_export_preset_holds_wrong_codecs_rates_and_peaks(self):
        good = {'streams': [{'codec_type': 'video', 'codec_name': 'h264', 'pix_fmt': 'yuv420p', 'field_order': 'progressive',
                             'r_frame_rate': '30/1', 'avg_frame_rate': '30/1', 'color_space': 'bt709', 'color_primaries': 'bt709',
                             'color_transfer': 'bt709', 'bit_rate': '9000000'},
                            {'codec_type': 'audio', 'codec_name': 'aac', 'sample_rate': '48000', 'channels': 2}],
                'format': {'duration': '12.0'}}
        self.assertEqual(ui.export_errors(good, -1.5), ([], []))
        def held(stream, **changes):
            bad = copy.deepcopy(good); bad['streams'][stream].update(changes)
            return ui.export_errors(bad, -1.5)[0]
        self.assertTrue(held(0, codec_name='hevc'))
        self.assertTrue(held(0, pix_fmt='yuv444p'))
        self.assertTrue(held(0, r_frame_rate='30/1', avg_frame_rate='24/1'))
        self.assertTrue(held(0, color_space='bt2020nc'))
        self.assertTrue(held(0, bit_rate='20000000'))
        self.assertTrue(held(1, sample_rate='44100'))
        self.assertTrue(held(1, channels=1))
        self.assertTrue(ui.export_errors(good, -0.2)[0])                                # clipping risk
        self.assertEqual(ui.export_errors({**good, 'streams': [{**good['streams'][0], 'bit_rate': '900000'}, good['streams'][1]]}, -2)[0], [])

    def test_spoken_lines_become_timed_segments_of_at_most_seven_words(self):
        line = 'I have been sitting by this door since you left, which was eleven minutes ago.'
        segs = ui.segments(line, 2.0, 8.0)
        self.assertEqual(' '.join(s for s, _, _ in segs), line)
        self.assertTrue(all(len(s.split()) <= ui.CAPTION_WORDS for s, _, _ in segs))
        self.assertTrue(all(len(s.split()) > 1 for s, _, _ in segs))
        self.assertAlmostEqual(segs[0][1], 2.0); self.assertAlmostEqual(segs[-1][2], 8.0)
        self.assertTrue(all(a[2] == b[1] for a, b in zip(segs, segs[1:])))

    def test_release_needs_the_layout_manifest_and_a_corpus_critical_region(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release, review = evidence(root)
            self.assertEqual(ui.errors(root, release, review, today=TODAY), [])
            wide = copy.deepcopy(release); wide['critical_region'] = list(ui.LEGACY['social-ui-2026-11-06-v1']['critical'])
            self.assertTrue(any('wider than the corpus box' in e for e in ui.errors(root, wide, {**review, 'binding': ui.digest(wide)}, today=TODAY)))
            bare = copy.deepcopy(release); bare['exports'] = [e for e in bare['exports'] if e['role'] != 'layout']
            self.assertTrue(any('layout manifest' in e for e in ui.errors(root, bare, {**review, 'binding': ui.digest(bare)}, today=TODAY)))


if __name__ == '__main__':
    unittest.main()


class CodexPictureCheckTests(unittest.TestCase):
    """codex/check_picture.py holds a Codex reel whose labels, ending or export break the corpus."""

    def test_label_box_ending_and_export(self):
        import shutil, subprocess
        if not shutil.which('ffmpeg'):
            self.skipTest('needs ffmpeg')
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            reel = Path(tmp) / 'reel.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=s=1080x1920:d=8:r=30', '-f', 'lavfi',
                            '-i', 'sine=f=440:d=8', '-af', 'volume=0.3', *ui.FFMPEG_VIDEO, *ui.FFMPEG_AUDIO, str(reel)], check=True)
            def run(timeline):
                path = Path(tmp) / 'timeline.json'; path.write_text(json.dumps(timeline))
                done = subprocess.run([sys.executable, str(root / 'codex/check_picture.py'), str(reel), str(path)], capture_output=True, text=True)
                return done.returncode, done.stdout
            good = {'label_box': [140, 360, 820, 440], 'shots': [
                {'seconds': 2.5, 'label': '6:00 AM · Up before the market'},
                {'seconds': 2.0, 'label': '9:00 AM · Board meeting'},
                {'seconds': 3.5, 'product': True}]}
            self.assertEqual(run(good), (0, 'ok\n'))
            self.assertIn('leaves the critical box', run({**good, 'label_box': [140, 300, 820, 380]})[1])   # the old y 300 top band
            self.assertIn('no label_box', run({k: v for k, v in good.items() if k != 'label_box'})[1])
            moving = copy.deepcopy(good); moving['shots'][1]['label_box'] = [140, 1050, 820, 1130]
            self.assertIn('labels move', run(moving)[1])
            dead = copy.deepcopy(good); dead['shots'][1]['seconds'] = 0.5; dead['shots'][2]['seconds'] = 5.0
            self.assertIn('held 3 to 4 seconds', run(dead)[1])


class ReviewFindingTests(unittest.TestCase):
    """Regressions for the independent review of 12 Nov: each was a false pass or a wrong hold."""

    def test_end_beat_counts_the_whole_trailing_product_run_less_speech(self):
        from tests.ui_fixtures import layout
        base = layout(duration=13.0)
        base['elements'][3].update(start=6.5, end=9.0)                       # a voiced product shot...
        base['elements'][2].update(end=9.0, text='I saw you')                 # ...speech runs over it
        base['elements'].append({'role': 'product', 'box': [150, 400, 790, 1100], 'start': 9.0, 'end': 13.0})
        self.assertEqual(ui.layout_errors(base)[0], [])                       # 4 s of silent product
        silent = copy.deepcopy(base); silent['elements'][2]['end'] = 6.5      # no speech over the first shot
        self.assertTrue(any('product end beat 6.5 s' in p for p in ui.layout_errors(silent)[0]))
        cards = {'profile': ui.REVISION, 'canvas': [1080, 1920], 'duration': 10.0, 'ending': 'product', 'elements': [
            {'role': 'product', 'box': [160, 620, 790, 920], 'start': a, 'end': b} for a, b in ((0, 3), (3, 7), (7, 10))] + [
            {'role': 'hook' if a == 0 else 'title', 'box': [140, 440, 810, 600], 'start': a, 'end': b, 'text': 'Line'} for a, b in ((0, 3), (3, 7), (7, 10))]}
        self.assertEqual(ui.layout_errors(cards)[0], [])                     # three product cards whose words change: a 3 s end
        undeclared = layout(); undeclared.pop('ending')
        self.assertTrue(any('declare how the post ends' in p for p in ui.layout_errors(undeclared)[0]))

    def test_still_slide_words_collide_even_though_a_slide_is_one_instant(self):
        still = {'profile': ui.REVISION, 'canvas': [1080, 1350], 'duration': 0, 'elements': [
            {'role': 'hook', 'box': [90, 90, 990, 220], 'start': 0, 'end': 0, 'text': 'A line'},
            {'role': 'text', 'box': [90, 150, 990, 260], 'start': 0, 'end': 0, 'text': 'Another'}]}
        self.assertTrue(any('overlap' in p for p in ui.layout_errors(still)[0]))

    def test_export_preset_is_exactly_twelve_mbps_and_bt709(self):
        good = {'streams': [{'codec_type': 'video', 'codec_name': 'h264', 'pix_fmt': 'yuv420p', 'r_frame_rate': '30/1',
                             'avg_frame_rate': '30/1', 'color_space': 'bt709', 'color_primaries': 'bt709', 'color_transfer': 'bt709',
                             'bit_rate': '11900000'}, {'codec_type': 'audio', 'codec_name': 'aac', 'sample_rate': '48000', 'channels': 2}],
                'format': {'duration': '12'}}
        self.assertEqual(ui.export_errors(good, -2)[0], [])
        fast = copy.deepcopy(good); fast['streams'][0]['bit_rate'] = '12500000'
        self.assertTrue(ui.export_errors(fast, -2)[0])
        sd = copy.deepcopy(good); sd['streams'][0]['color_space'] = 'smpte170m'
        self.assertTrue(ui.export_errors(sd, -2)[0])
        bare = copy.deepcopy(good); bare['streams'][0].pop('color_space')
        problems, notes = ui.export_errors(bare, -2)
        self.assertEqual(problems, []); self.assertTrue(any('untagged' in n for n in notes))

    def test_release_layout_must_belong_to_the_media_export(self):
        from tests.ui_fixtures import layout
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release, review = evidence(root)
            entry = next(e for e in release['exports'] if e['role'] == 'layout')
            path = root / entry['path']
            for wrong in (layout(canvas=[1080, 1350]), layout(media_sha256='0' * 64)):
                path.write_text(json.dumps(wrong)); entry['sha256'] = ui.file_sha(path)
                self.assertTrue(any('another' in e for e in ui.errors(root, release, {**review, 'binding': ui.digest(release)}, today=TODAY)))

    def test_a_reviewer_pass_from_before_the_profile_does_not_count(self):
        import lock
        spec = {'id': 'F99', 'ui_profile': ui.REVISION}
        old = {'records': [{'lock': 'F99', 'spec': 'F99', 'verdict': 'reviewer-pass', 'fingerprint': lock.fingerprint(spec)}]}
        new = {'records': [{**old['records'][0], 'ui_profile': ui.REVISION}]}
        with patch.object(lock, 'check', side_effect=lambda s: ([], [])), patch.object(lock, 'media', return_value=[]), \
             patch.object(lock, 'ramp', return_value=('ok', 'test')), patch('engine.creative_ui.check_files', return_value=[]):
            with patch.object(lock, 'ledger', return_value=old):
                self.assertTrue(any('current profile' in e for e in lock.gate(spec, 'x.mp4', 'r', 'v')[0]))
            with patch.object(lock, 'ledger', return_value=new):
                self.assertEqual(lock.gate(spec, 'x.mp4', 'r', 'v')[0], [])
