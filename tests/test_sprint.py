"""The sprint ledger and the still template must hold a 120-post batch to the same gates as one post."""
import collections, copy, hashlib, json, os, sys, tempfile, unittest

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
        m = manifest(); slot = next(x for x in m['slots'] if x['template'] == 'still' and x.get('concept') and x['stage'] == 'idea')
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
        # Every other master moved onto the 12 Nov corpus profile and still matches its lock: placement
        # is not content (lock.fingerprints).
        already_drifting = {'F01.json'}
        for name in sorted(set(os.listdir(os.path.join(HERE, '..', 'factory', 'locks'))) - already_drifting):
            lk = json.load(open(os.path.join(HERE, '..', 'factory', 'locks', name), encoding='utf-8'))
            spec = json.load(open(os.path.join(HERE, '..', 'factory', lk['master']), encoding='utf-8'))
            self.assertTrue(lock.matches(spec, lk['fingerprint']), name)

    def test_built_slides_are_checked_for_count_and_size(self):
        from engine.creative_ui import REVISION
        layout = {'profile': REVISION, 'canvas': [1080, 1350], 'duration': 0, 'elements': [
            {'role': 'hook', 'box': [90, 90, 990, 220], 'start': 0, 'end': 0, 'text': 'A line'},
            {'role': 'picture', 'box': [0, 256, 1080, 1350], 'start': 0, 'end': 0}]}
        with tempfile.TemporaryDirectory() as out:
            Image.new('RGB', (1080, 1350)).save(f'{out}/slide-01.png')
            self.assertTrue(any('expected' in p for p in lock.still_media(self.spec, out)))
            Image.new('RGB', (1080, 1350)).save(f'{out}/slide-02.png')
            self.assertTrue(any('no layout manifest' in p for p in lock.still_media(self.spec, out)))
            import hashlib
            def bind(n, data):
                data = {**data, 'media_sha256': hashlib.sha256(open(f'{out}/slide-0{n}.png', 'rb').read()).hexdigest()}
                json.dump(data, open(f'{out}/slide-0{n}.layout.json', 'w'))
            json.dump(layout, open(f'{out}/slide-01.layout.json', 'w'))   # unbound: belongs to no particular slide
            self.assertTrue(any('another build' in p for p in lock.still_media(self.spec, out)))
            for n in (1, 2):
                bind(n, layout)
            self.assertEqual(lock.still_media(self.spec, out), [])
            bind(2, {**layout, 'elements': [{**layout['elements'][0], 'box': [30, 30, 1050, 220]}, layout['elements'][1]]})
            self.assertTrue(any('feed margin' in p for p in lock.still_media(self.spec, out)))
            bind(2, layout)
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

class SprintCreativeIdTest(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(HERE, '..'))
        import growth
        from engine import attribution
        self.growth, self.attribution = growth, attribution

    def test_every_slot_gets_a_valid_unique_creative_id_per_platform(self):
        m = manifest(); ids = []
        for s in m['slots']:
            for p in s['platforms']:
                cid = sprint.creative_id(m, s, p)
                self.assertTrue(self.growth.CREATIVE_ID.match(cid), cid)
                self.assertTrue(self.attribution.CREATIVE_ID.match(cid), cid)
                ids.append(cid)
        self.assertEqual(len(ids), len(set(ids)))
        families = {(sprint.creative_id(m, s, 'tiktok').split('_')[3]) for s in m['slots']}
        self.assertEqual(len(families), len(m['slots']))

    def test_the_mapping_is_deterministic_and_documented(self):
        m = manifest(); s = sprint.find_slot(m, 'S01')
        self.assertEqual(sprint.creative_id(m, s, 'instagram'), 'IG_EMO_REEL_C301_H01_V1_20261117')
        self.assertEqual(sprint.creative_id(m, s, 'instagram'), sprint.creative_id(manifest(), sprint.find_slot(manifest(), 'S01'), 'instagram'))
        v = sprint.find_slot(m, 'V100')
        self.assertEqual(sprint.creative_id(m, v, 'tiktok'), 'TT_ENT_POST_C300_H01_V1_20261120')

    def test_the_schedule_row_carries_the_creative_id_and_leaves_approval_to_krish(self):
        m = manifest(); row = sprint.schedule_row(m, sprint.find_slot(m, 'S01'), 'facebook')
        self.assertEqual((row['creative_id'], row['approved']), ('FB_EMO_REEL_C301_H01_V1_20261117', ''))

    def test_a_slot_id_resolves_to_a_link_that_check_accepts(self):
        g = self.growth
        cid = g.slot_creative_id('S01', 'instagram')
        link = g.tracked('https://heartside.io/products/your-dogs-illustrated-mug', cid)
        item = {'platform': 'instagram', 'creative_id': cid, 'intent': 'audience', 'text': f'Caption: the mug, from the dog. {link}'}
        self.assertEqual(g.problems(item), [])
        pack = {'pack_date': '2026-11-17', 'kind': 'daily', 'venture': 'heartside', 'heartside_sha': 'abcdef1',
                'headline': 'Sprint post S01', 'items': [item]}
        self.assertEqual([e for e in g.check_pack(pack) if 'creative_id' in e or 'link' in e], [])

    def test_link_refuses_a_platform_that_disagrees_with_a_full_id(self):
        import subprocess
        g = os.path.join(HERE, '..', 'growth.py')
        bad = subprocess.run([sys.executable, g, 'link', 'https://heartside.io', 'IG_EMO_REEL_C301_H01_V1_20261117',
                              '--platform', 'tiktok'], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn('does not match', bad.stderr)
        ok = subprocess.run([sys.executable, g, 'link', 'https://heartside.io', 'IG_EMO_REEL_C301_H01_V1_20261117',
                             '--platform', 'instagram'], capture_output=True, text=True, check=True)
        self.assertIn('utm_content=IG_EMO_REEL_C301_H01_V1_20261117', ok.stdout)

    def test_a_slot_on_another_platform_is_refused(self):
        with self.assertRaises(ValueError):
            self.growth.slot_creative_id('S01', 'pinterest')
        with self.assertRaises(ValueError):
            self.growth.slot_creative_id('S99')


class SprintConceptNumberTest(unittest.TestCase):
    """Concept numbers run on through the whole engine, so two sprints (or two lanes) never share a family."""

    def second(self, m, sprint_id='2026-12-S121'):
        o = copy.deepcopy(m); o['sprint'] = sprint_id
        return o

    def test_two_manifests_on_the_default_blocks_are_refused(self):
        m = manifest(); o = self.second(m)
        errs = sprint.errors(o, others=[m])
        self.assertTrue(any('already used by 2026-11-S120' in e for e in errs), errs)

    def test_a_second_manifest_with_its_own_base_is_accepted(self):
        m = manifest(); o = self.second(m); o['concept_base'] = {'viral': 400, 'signature': 500}
        self.assertEqual(sprint.concept_errors(o, others=[m]), [])

    def test_the_shipped_manifests_do_not_collide(self):
        m = manifest()
        self.assertEqual(sprint.concept_errors(m), [])
        self.assertEqual(sprint.concept_errors(m, others=sprint.other_manifests(m)), [])

    def test_a_viral_slot_past_100_crossing_into_the_signature_block_is_refused(self):
        m = manifest(); v = copy.deepcopy(sprint.find_slot(m, 'V100')); v['id'] = 'V101'; m['slots'].append(v)
        errs = sprint.concept_errors(m, others=[])
        self.assertTrue(any('C301' in e and 'overlap' in e for e in errs), errs)

    def test_a_base_reaching_the_engine_range_is_refused(self):
        m = manifest(); m['concept_base'] = {'viral': 0, 'signature': 300}
        errs = sprint.concept_errors(m, others=[])
        self.assertTrue(any("engine's used range" in e for e in errs), errs)


class SprintDiagnosisTest(unittest.TestCase):
    def reading(self, slot, views, **funnel):
        return (slot, 'tiktok'), sprint.view_record(manifest(), slot, 'tiktok', views, '2026-11-15T12:00:00Z', 'tiktok analytics', **funnel)

    def test_absent_funnel_fields_are_not_written(self):
        rec = sprint.view_record(manifest(), 'V001', 'tiktok', 900, '2026-11-15T12:00:00Z', 'tiktok analytics', three_s_rate=0.4)
        self.assertEqual(rec['three_s_rate'], 0.4)
        for k in ('avg_watch_s', 'profile_visits', 'link_clicks'):
            self.assertNotIn(k, rec)
        with self.assertRaises(ValueError):
            sprint.view_record(manifest(), 'V001', 'tiktok', 900, 'x', 'y', three_s_rate=40)

    def test_below_five_posts_it_builds_the_baseline(self):
        r = dict([self.reading('V001', 1000, three_s_rate=0.1)])
        out = sprint.diagnose(manifest(), r)
        self.assertEqual({row['stage'] for row in out.values()}, {'baseline'})

    def test_each_franchise_gets_its_first_failing_stage_and_next_test(self):
        m = manifest(); by = collections.defaultdict(list)
        for s in m['slots']:
            if s.get('franchise') and not s.get('double_down'):
                by[s['franchise']].append(s['id'])
        names = sorted(by)[:3]
        a, b, c = (by[n][0] for n in names)
        r = dict([self.reading(a, 1000, three_s_rate=0.2, avg_watch_s=6, profile_visits=10),
                  self.reading(b, 1000, three_s_rate=0.6, avg_watch_s=3, profile_visits=10),
                  self.reading(c, 1000, three_s_rate=0.6, avg_watch_s=6, profile_visits=1),
                  self.reading(by[names[0]][1], 1000, three_s_rate=0.2, avg_watch_s=6, profile_visits=10),
                  self.reading(by[names[2]][1], 1000, three_s_rate=0.6, avg_watch_s=6, profile_visits=1)])
        out = sprint.diagnose(m, r)
        self.assertEqual(out[names[0]]['stage'], 'stop')
        self.assertIn('first shot', out[names[0]]['next_test'])
        self.assertEqual(out[names[1]]['stage'], 'stay')
        self.assertEqual(out[names[2]]['stage'], 'click')
        self.assertIn('gift-led', out[names[2]]['next_test'])

    def test_convert_needs_attributed_orders_and_missing_is_never_zero(self):
        m = manifest(); fr = sorted({s['franchise'] for s in m['slots'] if s.get('franchise')})[:2]
        a = [s['id'] for s in m['slots'] if s.get('franchise') == fr[0]][:3]
        b = [s['id'] for s in m['slots'] if s.get('franchise') == fr[1]][:2]
        r = dict([self.reading(x, 1000, three_s_rate=0.5, avg_watch_s=5, link_clicks=20) for x in a + b])
        self.assertEqual({row['stage'] for row in sprint.diagnose(m, r).values()}, {'holding'})
        out = sprint.diagnose(m, r, orders={fr[0]: 0, fr[1]: 2})
        self.assertEqual(out[fr[0]]['stage'], 'convert')
        self.assertIn('destination', out[fr[0]]['next_test'])
        blank = dict([self.reading(x, 1000) for x in a + b])
        self.assertEqual({row['stage'] for row in sprint.diagnose(m, blank).values()}, {'not shown'})

    def test_click_rate_divides_each_field_by_its_own_views(self):
        m = manifest()
        by = collections.defaultdict(list)
        for s in m['slots']:
            if s['lane'] == 'viral' and s.get('franchise'):
                by[s['franchise']].append(s['id'])
        name, slots = next((k, v) for k, v in by.items() if len(v) >= 2)
        r = dict([self.reading(slots[0], 1000, profile_visits=10, link_clicks=10),
                  self.reading(slots[1], 9000, profile_visits=90)])
        # Visits: 100 over 10,000 views is 10 per 1,000. Clicks: 10 over the 1,000 views that showed them is 10 per
        # 1,000. Together 20, not the 2 a shared denominator gave.
        self.assertAlmostEqual(sprint.diagnose(m, r)[name]['measures']['click'], 20.0)


if __name__ == '__main__':
    unittest.main()
