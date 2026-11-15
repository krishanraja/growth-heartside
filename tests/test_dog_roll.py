"""The dog roller must keep every generated dog a real, scruffy pet on a phone, and never the same dog twice.

Floor real-scruffy-dogs (Krish, 10 Nov: "way too perfect and not real"). Every attribute is rolled outside the
model; these tests hold the roller to the floor: never a chestnut or red dachshund, the avoid list on every
prompt, no repeats inside a batch, and the recent history respected across batches.
"""
import json, os, random, re, sys, tempfile, unittest
from pathlib import Path

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'factory'))
import dog_roll  # noqa: E402
from engine import stills  # noqa: E402

POOLS = dog_roll.load_pools()
FLOOR = stills.load_floor(ROOT)


def roll(count=1, **kw):
    kw.setdefault('history', None)
    kw.setdefault('out', None)
    return dog_roll.roll(count, pools=POOLS, floor_data=FLOOR, **kw)


def subject(rec):
    """The sentence that names the dog: where a coat colour sits beside its breed."""
    return next(s for s in rec['prompt'].split('. ') if s.startswith('The dog:') or ' The dog:' in s)


class RandomnessTest(unittest.TestCase):
    def test_the_roller_draws_from_os_entropy(self):
        self.assertIsInstance(dog_roll.RNG, random.SystemRandom)

    def test_count_is_one_to_twelve(self):
        for bad in (0, 13):
            with self.assertRaises(ValueError):
                roll(bad)

    def test_every_roll_passes_the_floor_prompt_checks(self):
        for frame in ('photo', 'video'):
            for _ in range(8):
                for rec in roll(12, frame=frame):
                    self.assertEqual(stills.content(rec, FLOOR, POOLS), [], rec['prompt'])
                    self.assertTrue(3 <= len(rec['attributes']['artifacts']) <= 5)
                    self.assertTrue(rec['attributes']['conditions'])
                    self.assertEqual(rec['prompt_sha256'], stills.sha256_text(rec['prompt']))

    def test_a_photo_and_a_video_frame_say_which_they_are(self):
        photo, video = roll(frame='photo')[0], roll(frame='video')[0]
        self.assertEqual((photo['aspect_ratio'], video['aspect_ratio']), ('3:4', '9:16'))
        self.assertIn('A vertical snapshot on', photo['prompt'])
        self.assertIn('frame taken from a clip the owner shot', video['prompt'])
        self.assertIn('motion blur smeared across the whole frame', video['avoid'])


class DachshundTest(unittest.TestCase):
    """factory/lock.py STANDING: no chestnut or red dachshund in a generated frame; it can read as Buddy."""

    def test_a_random_roll_never_draws_a_dachshund(self):
        breeds = {r['attributes']['breed'] for _ in range(30) for r in roll(12)}
        self.assertNotIn('dachshund', breeds)
        self.assertGreater(len(breeds), 20)

    def test_a_locked_dachshund_is_never_chestnut_or_red(self):
        for rec in (r for _ in range(10) for r in roll(6, breeds=['dachshund'])):
            self.assertEqual(rec['attributes']['breed'], 'dachshund')
            self.assertIsNone(stills.RED.search(rec['attributes']['color']), rec['attributes']['color'])
            self.assertIsNone(stills.RED.search(subject(rec)), subject(rec))
            self.assertIn('a chestnut, red or ginger coat', rec['avoid'])

    def test_a_chestnut_or_red_dachshund_lock_is_refused(self):
        for coat in ('chestnut', 'red', 'ginger', 'fox-red'):
            with self.assertRaisesRegex(ValueError, 'lock.py STANDING'):
                roll(breeds=['dachshund'], coat=coat)

    def test_the_pools_offer_no_red_dachshund_coat(self):
        dach = next(b for b in POOLS['breeds'] if b['key'] == 'dachshund')
        self.assertTrue(dach['lock_only'])
        self.assertFalse([c for c in dach['colors'] if stills.RED.search(c)])

    def test_a_sprint_slot_naming_a_dachshund_without_breed_ok_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'm.json')
            Path(path).write_text(json.dumps({'slots': [{'id': 'S99', 'breed': 'dachshund'}, {'id': 'S98', 'breed': 'golden'}]}))
            with self.assertRaisesRegex(ValueError, 'reads as Buddy'):
                dog_roll.slot_breed('S99', path)
            self.assertEqual(dog_roll.slot_breed('S98', path), 'golden')

    def test_every_sprint_slot_breed_is_in_the_pools(self):
        m = json.loads(Path(dog_roll.SPRINT).read_text(encoding='utf-8'))
        named = sorted({s['breed'] for s in m['slots'] if s.get('breed')})
        self.assertEqual(len(dog_roll.breed_keys(POOLS, named)), len(named))


class AvoidListTest(unittest.TestCase):
    def test_the_avoid_list_is_on_every_prompt_whatever_is_rolled_or_locked(self):
        base = [a['text'] for a in POOLS['avoid_base']]
        recs = [r for _ in range(10) for r in roll(12)]
        recs += [r for s in POOLS['settings'] for r in roll(2, settings=[s], frame='video')]
        recs += roll(3, breeds=['dachshund'], action='lying flat on the cool floor, a sock hanging from its mouth')
        for rec in recs:
            positive, avoid = stills.split(rec['prompt'])
            self.assertTrue(rec['prompt'].split('\n\n')[-1].startswith('Avoid: '))
            self.assertEqual(avoid, rec['avoid'])
            for text in base:
                self.assertIn(text, avoid)

    def test_every_floor_rule_the_avoid_list_guards_is_a_real_floor_entry(self):
        ids = {e['id'] for e in FLOOR['entries']}
        for item in POOLS['avoid_base']:
            self.assertTrue(item['floor'] is None or item['floor'] in ids, item)
        guarded = {a['floor'] for a in POOLS['avoid_base']}
        for fid in ('real-scruffy-dogs', 'real-dogs', 'no-badges', 'troll-not-mild', 'real-product',
                    'dog-does-dog-things', 'one-trend-one-scene'):
            self.assertIn(fid, guarded)


class RepeatTest(unittest.TestCase):
    def test_no_breed_or_setting_repeats_inside_a_batch(self):
        for _ in range(20):
            recs = roll(8)
            for key in ('breed', 'setting'):
                values = [r['attributes'][key] for r in recs]
                self.assertEqual(len(set(values)), len(values), values)
            self.assertEqual(len({r['prompt'] for r in recs}), 8)
            self.assertEqual(len({r['roll_id'] for r in recs}), 8)

    def test_recent_breeds_and_settings_are_kept_out_of_the_next_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            hist = os.path.join(tmp, 'local', 'factory', 'dog-roll-history.json')
            recent_b = dog_roll.breed_keys(POOLS)[:12]
            recent_s = list(POOLS['settings'])[:6]
            os.makedirs(os.path.dirname(hist))
            Path(hist).write_text(json.dumps({'breeds': recent_b, 'settings': recent_s, 'conditions': []}))
            for _ in range(10):
                recs = roll(3, history=hist)
                for r in recs:
                    self.assertNotIn(r['attributes']['breed'], recent_b)
                    self.assertNotIn(r['attributes']['setting'], recent_s)
                Path(hist).write_text(json.dumps({'breeds': recent_b, 'settings': recent_s, 'conditions': []}))
            recs = roll(3, history=hist)
            saved = json.loads(Path(hist).read_text())
            self.assertEqual(saved['breeds'][-3:], [r['attributes']['breed'] for r in recs])
            self.assertLessEqual(len(saved['breeds']), dog_roll.KEEP['breeds'])
            self.assertLessEqual(len(saved['settings']), dog_roll.KEEP['settings'])

    def test_back_to_back_batches_do_not_repeat_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            hist = os.path.join(tmp, 'h.json')
            first = {r['attributes']['setting'] for r in roll(4, history=hist)}
            second = {r['attributes']['setting'] for r in roll(4, history=hist)}
            self.assertFalse(first & second)

    def test_a_missing_or_broken_history_file_is_an_empty_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, 'h.json')
            Path(bad).write_text('not json')
            self.assertEqual(dog_roll.load_history(bad), {'breeds': [], 'settings': [], 'conditions': []})
            self.assertEqual(len(roll(2, history=bad)), 2)


class LockTest(unittest.TestCase):
    def test_the_scripted_action_goes_in_verbatim_and_the_face_is_left_to_it(self):
        beat = 'lying in the open suitcase on the folded clothes, a whole loaf in its bag in its mouth'
        rec = roll(breeds=['golden'], settings=['bedroom'], action=beat)[0]
        self.assertIn(f'What it is doing: {beat}.', rec['prompt'])
        self.assertNotIn('Its face:', rec['prompt'])
        self.assertTrue(rec['attributes']['action_from_script'])
        free = roll()[0]
        self.assertIn('Its face:', free['prompt'])

    def test_a_breed_lock_by_alias_and_a_coat_lock_to_match_a_render(self):
        recs = roll(3, breeds=['golden retriever'], coat='medium gold')
        self.assertEqual({r['attributes']['breed'] for r in recs}, {'golden'})
        self.assertTrue(all('a medium gold golden retriever' in r['prompt'] for r in recs))

    def test_an_unknown_breed_or_setting_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'no breed'):
            roll(breeds=['wolf'])
        with self.assertRaisesRegex(ValueError, 'no setting'):
            roll(settings=['spaceship'])

    def test_records_are_written_by_roll_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            recs = roll(2, out=tmp)
            for r in recs:
                saved = json.loads(Path(tmp, r['roll_id'] + '.json').read_text())
                self.assertEqual(saved, r)


class PoolsTest(unittest.TestCase):
    def test_the_pools_name_no_product_person_link_or_em_dash(self):
        text = Path(dog_roll.POOLS).read_text(encoding='utf-8')
        self.assertNotIn('\u2014', text)
        self.assertNotIn('http', text)
        drawn = {k: v for k, v in POOLS.items() if k not in ('about', 'avoid_base')}
        drawn['breeds'] = [{k: v for k, v in b.items() if k != 'why'} for b in POOLS['breeds']]
        positive = json.dumps(drawn)
        for word in ('mug', 'blanket', 'portrait', 'painting', 'framed', 'greeting card', 'Heartside', 'Buddy', 'Biscuit'):
            self.assertIsNone(re.search(rf'\b{word}\b', positive, re.I), word)


if __name__ == '__main__':
    unittest.main()
