"""The sprint ledger and the still template must hold a 120-post batch to the same gates as one post."""
import copy, hashlib, json, os, sys, tempfile, unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'factory'))
import lock, sprint, still  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

MANIFEST = os.path.join(HERE, '..', 'factory', 'sprints', '2026-11-S120.json')


def manifest():
    return json.load(open(MANIFEST, encoding='utf-8'))


class SprintManifestTest(unittest.TestCase):
    def test_the_sprint_manifest_is_ready(self):
        self.assertEqual(sprint.errors(manifest()), [])

    def test_counts_match_the_ask(self):
        m = manifest(); lanes = [s['lane'] for s in m['slots']]
        self.assertEqual((lanes.count('signature'), lanes.count('viral')), (20, 100))
        self.assertEqual(m['targets']['views'], 500000)

    def test_a_franchise_graded_out_is_refused(self):
        # Nothing is excluded since Krish's 10 Nov ruling; the mechanism stays for a format he rules out later.
        m = manifest(); s = next(x for x in m['slots'] if x.get('concept'))
        saved = sprint.franchises
        def graded_out():
            fr = saved(); fr[s['franchise']] = dict(fr[s['franchise']], grade='C'); return fr
        sprint.franchises = graded_out
        try:
            self.assertTrue(any('excluded' in e for e in sprint.errors(m)))
        finally:
            sprint.franchises = saved

    def test_nothing_is_excluded_and_the_lip_sync_leads(self):
        fr = sprint.franchises()
        self.assertFalse([f for f in fr.values() if f['grade'] == 'C'])
        first = sorted((s for s in manifest()['slots'] if s.get('franchise') == 'The Human-Arms Lip-Sync'), key=lambda s: s['day'])
        self.assertEqual(first[0]['day'], manifest()['window']['start'])

    def test_a_platform_cap_is_enforced(self):
        m = manifest(); m['caps']['per_platform_per_day']['tiktok'] = 5
        self.assertTrue(any('the cap is' in e for e in sprint.errors(m)))

    def test_a_double_down_before_the_first_read_is_refused(self):
        m = manifest(); s = next(x for x in m['slots'] if x.get('double_down'))
        s['day'] = m['window']['start']
        self.assertTrue(any('72-hour read' in e for e in sprint.errors(m)))

    def test_a_repeated_concept_is_refused(self):
        m = manifest(); cs = [x for x in m['slots'] if x.get('concept')]
        cs[1]['franchise'], cs[1]['concept'] = cs[0]['franchise'], cs[0]['concept']
        self.assertTrue(any('repeats belong in double-down' in e for e in sprint.errors(m)))

    def test_a_signature_post_needs_a_real_render_and_a_payoff(self):
        m = manifest(); s = next(x for x in m['slots'] if x['lane'] == 'signature')
        s['breed'] = 'lab'; s['product'] = 'blanket'; s['payoff'] = ''
        errs = sprint.errors(m)
        self.assertTrue(any('no approved blanket render' in e for e in errs))
        self.assertTrue(any('dumb-stopping' in e for e in errs))

    def test_a_lip_sync_needs_its_song(self):
        m = manifest(); s = next(x for x in m['slots'] if x.get('franchise') == 'The Human-Arms Lip-Sync')
        s.pop('track')
        self.assertTrue(any('names its song' in e for e in sprint.errors(m)))

    def test_every_post_goes_to_every_platform(self):
        self.assertTrue(all(sorted(s['platforms']) == ['facebook', 'instagram', 'tiktok'] for s in manifest()['slots']))

    def test_advance_moves_one_gate_at_a_time(self):
        m = manifest(); sid = next(x['id'] for x in m['slots'] if x['stage'] == 'idea')
        with self.assertRaises(SystemExit):
            sprint.advance(m, sid, 'approved')
        sprint.advance(m, sid, 'script')
        self.assertEqual(next(x for x in m['slots'] if x['id'] == sid)['stage'], 'script')

    def test_specs_come_only_from_approved_still_slots(self):
        m = manifest(); slot = next(x for x in m['slots'] if x['template'] == 'still' and x.get('concept'))
        slot['slides'] = [{'frame': 'x.png', 'line': 'F10.c01', 'focus_y': 0.4}]
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(sprint.specs(m, d), [])
            slot['stage'] = 'approved'
            wrote = sprint.specs(m, d)
            self.assertEqual(len(wrote), 1)
            spec = json.load(open(wrote[0], encoding='utf-8'))
            self.assertEqual((spec['template'], spec['concept']), ('still', slot['concept']))

    def test_views_are_summed_per_post_from_the_latest_reading(self):
        m = manifest()
        with tempfile.TemporaryDirectory() as d:
            saved = sprint.VIEWS; sprint.VIEWS = os.path.join(d, 'v.jsonl')
            try:
                rows = [('V001', 'tiktok', 100, '2026-11-13T00:00:00Z'), ('V001', 'tiktok', 900, '2026-11-14T00:00:00Z'),
                        ('V001', 'instagram', 50, '2026-11-14T00:00:00Z')]
                with open(sprint.VIEWS, 'w') as f:
                    for slot, pl, v, at in rows:
                        f.write(json.dumps({'sprint': m['sprint'], 'slot': slot, 'platform': pl, 'views': v, 'at': at, 'source': 'test'}) + '\n')
                self.assertEqual(sprint.latest_views(m)['V001'], 950)
            finally:
                sprint.VIEWS = saved


class StillTemplateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); lib = self.tmp.name
        for sub in ('renders', 'frames'): os.makedirs(f'{lib}/{sub}')
        Image.new('RGB', (1200, 1600), (90, 120, 80)).save(f'{lib}/frames/dog.png')
        self._saved = (lock.LIB, copy.deepcopy(lock.RENDERS), lock.LEDGER)
        lock.LIB = lib; lock.LEDGER = f'{lib}/ledger.json'
        for f, r in lock.RENDERS.items():
            data = f'render {f}'.encode(); open(f'{lib}/renders/{f}', 'wb').write(data)
            r['sha256'] = hashlib.sha256(data).hexdigest()
        from engine.creative_ui import REVISION
        self.spec = {'id': 'V900', 'template': 'still', 'ui_profile': REVISION, 'breed': 'lab', 'aspect': '4:5',
                     'slides': [{'frame': 'dog.png', 'line': 'F10.c01', 'focus_y': 0.3}], 'end': {'renders': ['mug-real-lab.jpg']}}

    def tearDown(self):
        lock.LIB, renders, lock.LEDGER = self._saved
        lock.RENDERS.clear(); lock.RENDERS.update(renders); self.tmp.cleanup()

    def test_an_approved_still_passes_the_static_gate(self):
        self.assertEqual(lock.check(self.spec)[0], [])

    def test_photo_and_text_placement_are_slots_but_lines_are_not(self):
        other = copy.deepcopy(self.spec); other['id'] = 'V901'
        other['slides'][0].update(frame='other.png', focus_y=0.8)
        self.assertEqual(lock.fingerprint(self.spec), lock.fingerprint(other))
        other['slides'].append({'frame': 'dog.png'})
        self.assertNotEqual(lock.fingerprint(self.spec), lock.fingerprint(other))

    def test_a_missing_photo_and_a_bad_aspect_are_held(self):
        s = copy.deepcopy(self.spec); s['slides'][0]['frame'] = 'nope.png'; s['aspect'] = '1:1'
        probs = lock.check(s)[0]
        self.assertTrue(any('missing' in p for p in probs) and any('aspect' in p for p in probs))

    def test_existing_locks_keep_their_fingerprints(self):
        # F01's spec was edited after its lock (3d675d1, 4 Nov) and already drifts on main; that is a
        # finding for Krish, not something the still template may paper over by re-locking.
        already_drifting = {'F01.json'}
        for name in sorted(set(os.listdir(os.path.join(HERE, '..', 'factory', 'locks'))) - already_drifting):
            lk = json.load(open(os.path.join(HERE, '..', 'factory', 'locks', name), encoding='utf-8'))
            spec = json.load(open(os.path.join(HERE, '..', 'factory', lk['master']), encoding='utf-8'))
            self.assertEqual(lock.fingerprint(spec), lk['fingerprint'], name)

    def test_built_slides_are_checked_for_count_and_size(self):
        with tempfile.TemporaryDirectory() as out:
            Image.new('RGB', (1080, 1350)).save(f'{out}/slide-01.png')
            self.assertTrue(any('expected' in p for p in lock.still_media(self.spec, out)))
            Image.new('RGB', (1080, 1350)).save(f'{out}/slide-02.png')
            self.assertEqual(lock.still_media(self.spec, out), [])
            Image.new('RGB', (1080, 1920)).save(f'{out}/slide-02.png')
            self.assertTrue(any('not 4:5' in p for p in lock.still_media(self.spec, out)))


class StillLayoutTest(unittest.TestCase):
    font = ImageFont.load_default(size=54)

    def test_the_line_sits_above_the_photo_never_on_it(self):
        photo = Image.new('RGB', (1200, 1600), (200, 0, 0))
        im = still.slide(photo, 'Every sock in this house answers to me now', self.font, '4:5')
        self.assertEqual(im.size, (1080, 1350))
        self.assertEqual(im.getpixel((5, 5)), still.PAPER)      # the band is paper
        self.assertEqual(im.getpixel((540, 1340)), (200, 0, 0))  # the photo fills below it

    def test_a_long_line_is_refused_not_shrunk(self):
        with self.assertRaises(ValueError):
            still.slide(Image.new('RGB', (100, 100)), ' '.join(['word'] * 60), self.font, '9:16')

    def test_no_word_is_left_alone_on_the_last_line(self):
        d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
        lines = still.wrap(d, 'one two three four five six seven eight nine ten eleven twelve thirteen', self.font, 600)
        self.assertGreater(len(lines[-1].split()), 1)

    def test_the_product_slide_is_the_render_scaled_only(self):
        render = Image.new('RGB', (400, 300), (10, 200, 30))
        im = still.product_slide(render, '9:16')
        self.assertEqual(im.size, (1080, 1920))
        self.assertEqual(im.getpixel((540, 960)), (10, 200, 30))
        self.assertEqual(im.getpixel((5, 5)), still.GROUND)


if __name__ == '__main__':
    unittest.main()
