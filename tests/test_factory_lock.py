"""The lock system must refuse drift, unapproved or edited lines, wrong-breed lines and altered renders."""
import copy, hashlib, json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'factory'))
import lock  # noqa: E402

SPECS = os.path.join(os.path.dirname(__file__), '..', 'factory', 'specs')


def load(name):
    return json.load(open(os.path.join(SPECS, name + '.json'), encoding='utf-8'))


class LockTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); lib = self.tmp.name
        os.makedirs(f'{lib}/renders'); os.makedirs(f'{lib}/locks'); os.makedirs(f'{lib}/frames')
        for name in os.listdir(SPECS):  # stand-in photos for every frame a spec names
            for fr in json.load(open(os.path.join(SPECS, name), encoding='utf-8')).get('frames', []):
                open(f'{lib}/frames/{fr}', 'wb').write(b'frame')
        self._saved = (lock.LIB, copy.deepcopy(lock.RENDERS), lock.LEDGER, lock.HERE)
        lock.LIB = lib; lock.LEDGER = f'{lib}/ledger.json'
        for f, r in lock.RENDERS.items():  # stand-in render files, registered by their own checksum
            data = f'render {f}'.encode(); open(f'{lib}/renders/{f}', 'wb').write(data)
            r['sha256'] = hashlib.sha256(data).hexdigest()

    def tearDown(self):
        lock.LIB, renders, lock.LEDGER, lock.HERE = self._saved
        lock.RENDERS.clear(); lock.RENDERS.update(renders); self.tmp.cleanup()

    def problems(self, spec):
        return lock.check(spec)[0]

    def test_approved_roast_passes(self):
        self.assertEqual(self.problems(load('F06-frenchie')), [])

    def test_variants_share_the_fingerprint_and_drift_breaks_it(self):
        fr, la = load('F06-frenchie'), load('F06-lab')
        self.assertEqual(lock.fingerprint(fr), lock.fingerprint(la))
        drift = copy.deepcopy(la); drift['durs'][1] = 1.0
        self.assertNotEqual(lock.fingerprint(fr), lock.fingerprint(drift))
        drift = copy.deepcopy(la); drift['lines'] = drift['lines'][:2]
        self.assertNotEqual(lock.fingerprint(fr), lock.fingerprint(drift))

    def test_unapproved_lines_are_held(self):
        s = load('F10'); s['messages'][1]['line'] = 'F10.c26'   # a proposed line
        self.assertTrue(any('not approved' in p for p in self.problems(s)))

    def test_wrong_breed_line_is_held(self):
        s = load('F10'); s['cast']['D'] = 'lab'
        s['end']['renders'] = ['mug-real-lab.jpg']
        self.assertTrue(any('tagged only for dachshund' in p for p in self.problems(s)))

    def test_edited_approved_line_is_held(self):
        line = lock.LINES['F10.c02']; saved = line['text']
        try:
            line['text'] = 'A really good stick, honestly.'
            self.assertTrue(any('edited after Krish approved' in p for p in self.problems(load('F10'))))
        finally:
            line['text'] = saved

    def test_altered_or_wrong_breed_render_is_held(self):
        s = load('F06-frenchie')
        open(f'{lock.LIB}/renders/{s["render"]}', 'wb').write(b'retouched')
        self.assertTrue(any('differs from the approved render' in p for p in self.problems(s)))
        s = load('F06-frenchie'); s['render'] = 'mug-real-lab.jpg'
        self.assertTrue(any('shows a lab' in p for p in self.problems(s)))

    def test_chat_photo_message_needs_its_frame_and_the_social_ui(self):
        spec = load('F34')
        photo = next(m['photo'] for m in spec['messages'] if 'photo' in m)
        self.assertIn(f'frame {photo} missing', self.problems(spec))
        open(f'{lock.LIB}/frames/{photo}', 'wb').write(b'frame')
        self.assertNotIn(f'frame {photo} missing', self.problems(spec))
        legacy = copy.deepcopy(spec); legacy.pop('ui_profile')
        self.assertTrue(any('only the social-ui profile' in p for p in self.problems(legacy)))
        swapped = copy.deepcopy(spec)
        next(m for m in swapped['messages'] if 'photo' in m)['photo'] = 'another.jpg'
        self.assertEqual(lock.fingerprint(spec), lock.fingerprint(swapped))   # the picture is a slot

    def test_social_ui_chat_refuses_novelty_sfx_and_long_typing(self):
        spec = load('F34')
        bark = copy.deepcopy(spec); bark['messages'][1]['sfx'] = 's_barks.mp3'
        self.assertTrue(any('no-novelty-sfx' in p for p in self.problems(bark)))
        slow = copy.deepcopy(spec); slow['messages'][1]['typing'] = 2.5
        self.assertTrue(any('typing bubble' in p for p in self.problems(slow)))
        self.assertFalse(any('no-novelty-sfx' in p or 'typing bubble' in p for p in self.problems(spec)))

    def test_balanced_wrap_never_leaves_a_lone_word(self):
        os.environ.setdefault('HEARTSIDE_ASSETS', self.tmp.name)
        from PIL import ImageDraw, Image, ImageFont
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'factory'))
        import importlib
        font = ImageFont.load_default()
        d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
        common = importlib.import_module('textfit')
        for text in ['Your dog loves you too.', 'What your dachshund really thinks of you.', 'Come on, you can throw better than that.']:
            for maxw in (60, 90, 140, 200):
                lines = common.balanced_wrap(d, text, font, maxw, 10)
                self.assertFalse(common.lone_word(lines), (text, maxw, lines))

    def test_placement_is_geometry_not_content(self):
        # Moving a post onto the current corpus profile keeps its lock: F34 was locked under the 6 Nov profile.
        from engine.creative_ui import REVISION
        spec = load('F34'); lk, _ = lock.lock_for(spec)
        self.assertEqual(spec['ui_profile'], REVISION)
        self.assertTrue(lock.matches(spec, lk['fingerprint']))
        old = copy.deepcopy(spec); old['ui_profile'] = 'social-ui-2026-11-06-v1'
        self.assertEqual(lock.fingerprint(old), lock.fingerprint(spec))
        self.assertTrue(any('retired profile' in p for p in self.problems(old)))
        legacy = load('F06-frenchie'); legacy.pop('ui_profile')
        self.assertTrue(any('legacy geometry' in p for p in self.problems(legacy)))
        changed = copy.deepcopy(spec); changed['end']['hold'] = 9.0   # content still drifts
        self.assertFalse(lock.matches(changed, lk['fingerprint']))

    def test_media_gate_holds_a_build_without_its_own_corpus_layout(self):
        import shutil, subprocess
        if not shutil.which('ffmpeg'):
            self.skipTest('needs ffmpeg')
        from engine.creative_ui import FFMPEG_VIDEO, FFMPEG_AUDIO
        sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
        from ui_fixtures import layout
        mp4 = f'{self.tmp.name}/F99.mp4'; lay = f'{self.tmp.name}/layout.json'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=s=1080x1920:d=10:r=30', '-f', 'lavfi',
                        '-i', 'sine=f=440:d=10', '-af', 'volume=0.3', *FFMPEG_VIDEO, *FFMPEG_AUDIO, mp4], check=True)
        spec = {'id': 'F99', '_layout': lay, '_end_png': f'{self.tmp.name}/none.png'}
        self.assertTrue(any('no layout manifest' in p for p in lock.media(spec, mp4)))
        data = layout(media_sha256=hashlib.sha256(open(mp4, 'rb').read()).hexdigest())
        json.dump(data, open(lay, 'w'))
        self.assertFalse([p for p in lock.media(spec, mp4) if 'layout' in p or 'export' in p or 'critical' in p])
        data['elements'][2]['box'] = [130, 1300, 820, 1440]; json.dump(data, open(lay, 'w'))
        self.assertTrue(any('leaves the critical region' in p for p in lock.media(spec, mp4)))
        json.dump(layout(media_sha256='0' * 64), open(lay, 'w'))
        self.assertTrue(any('another build' in p for p in lock.media(spec, mp4)))

    def test_free_text_is_refused(self):
        s = load('F06-frenchie'); s['lines'][0] = 'Some brand new joke.'
        self.assertTrue(any('not in the joke bank' in p for p in self.problems(s)))

    def test_ramp_needs_krish_for_the_first_variants_and_declines_pause(self):
        lock.HERE = self.tmp.name
        master = load('F06-frenchie')
        json.dump({'id': 'F06-frenchie', 'status': 'locked', 'fingerprint': lock.fingerprint(master)}, open(f'{self.tmp.name}/locks/F06-frenchie.json', 'w'))
        v = load('F06-lab'); v['id'] = 'F06-lab-1'
        self.assertEqual(lock.ramp(v)[0], 'krish')
        lock.record(v, 'krish-decline', 'not funny'); lock.record(v, 'krish-decline', 'still not')
        self.assertEqual(json.load(open(f'{self.tmp.name}/locks/F06-frenchie.json'))['status'], 'paused')
        self.assertTrue(any(r['line'] == 'F06.kla1' for r in lock.ledger()['retired']))


if __name__ == '__main__':
    unittest.main()
