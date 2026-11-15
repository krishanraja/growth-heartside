"""The still check must hold a generated dog still to the floor, and name the entry and Krish's words when it does.

Two stages (engine/stills.py): the prompt, before any credit is reserved, and the review, before the still
reaches his review board. The reservation goes through the provider ledger (engine/providers.py) and binds the
credits to the rolled prompt; nothing here generates or spends anything.
"""
import copy, datetime as dt, hashlib, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'factory'))
import dog_roll  # noqa: E402
from engine import ledger, providers, stills  # noqa: E402

POOLS = stills.load_pools(ROOT)
FLOOR = stills.load_floor(ROOT)
SHA = 'a' * 40


def rolled(**kw):
    rec = dog_roll.roll(1, history=None, out=None, pools=POOLS, floor_data=FLOOR, **kw)[0]
    return dict(rec, script_score=9, made_by='maker session')


def ids(failures):
    return {f['id'] for f in failures}


def quote():
    return {'provider': 'higgsfield', 'credits': '0.25', 'quote_source': 'Higgsfield quote for one still',
            'quote_observed_at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
            'allocation': 'credits:higgsfield:test'}


def every_verdict(verdict='pass'):
    return {e['id']: {'verdict': verdict, 'note': 'checked on the contact sheet'} for e in stills.owed(FLOOR)}


class PromptStageTest(unittest.TestCase):
    def test_a_fresh_roll_with_a_nine_on_paper_passes(self):
        self.assertEqual(stills.check(rolled(), 'prompt', FLOOR, POOLS), [])

    def test_no_script_score_is_held_by_spend_means_nine_in_his_words(self):
        rec = rolled(); rec.pop('script_score')
        failures = stills.check(rec, 'prompt', FLOOR, POOLS)
        self.assertEqual(ids(failures), {'spend-means-nine'})
        self.assertIn('"if you spend credits, nothing must be less than a 9"', stills.lines(failures)[0])
        self.assertEqual(ids(stills.check(dict(rec, script_score=8.5), 'prompt', FLOOR, POOLS)), {'spend-means-nine'})

    def test_an_edited_prompt_is_held_with_the_way_too_perfect_words(self):
        rec = rolled()
        rec['prompt'] = rec['prompt'].replace('What it is doing:', 'What it is doing, beautifully:')
        failures = stills.check(rec, 'prompt', FLOOR, POOLS)
        self.assertIn('real-scruffy-dogs', ids(failures))
        self.assertTrue(any('way too perfect and not real' in line and 'SHA-256' in line for line in stills.lines(failures)))

    def test_a_hand_written_prompt_is_held(self):
        prompt = 'A gorgeous golden retriever on a sofa.\n\nAvoid: blur.'
        rec = {'prompt': prompt, 'prompt_sha256': stills.sha256_text(prompt), 'avoid': ['blur'], 'script_score': 9}
        reasons = ' '.join(f['reason'] for f in stills.check(rec, 'prompt', FLOOR, POOLS))
        self.assertIn('did not come from factory/dog_roll.py', reasons)
        self.assertIn('realism block', reasons)
        self.assertIn('the avoid list is missing', reasons)

    def test_each_banned_ask_names_its_floor_entry(self):
        cases = {
            'real-product': 'the dog asleep on a fleece blanket',
            'no-badges': 'a sign above it that says GOOD BOY',
            'troll-not-mild': 'grinning at the lens',
            'dog-does-dog-things': 'holding the remote in its hands',
            'one-trend-one-scene': 'dancing on its hind legs',
            'real-scruffy-dogs': 'freshly groomed with glossy fur, studio light',
        }
        for fid, ask in cases.items():
            rec = rolled()
            positive, avoid = stills.split(rec['prompt'])
            rec['prompt'] = positive.replace('What it is doing:', f'What it is doing: {ask};') + '\n\nAvoid: ' + '; '.join(avoid) + '.'
            rec['prompt_sha256'] = stills.sha256_text(rec['prompt'])
            self.assertIn(fid, ids(stills.check(rec, 'prompt', FLOOR, POOLS)), fid)

    def test_a_prohibition_never_trips_its_own_ban(self):
        said = stills.affirmative('shampoo bottles with no readable labels, a real pet, not a show dog; never a studio catchlight.')
        for word in ('labels', 'show dog', 'studio'):
            self.assertNotIn(word, said)
        for _ in range(20):
            self.assertEqual(stills.check(rolled(settings=['bathroom', 'laundry']), 'prompt', FLOOR, POOLS), [])

    def test_a_chestnut_dachshund_is_held_by_the_standing_check(self):
        rec = rolled(breeds=['dachshund'])
        rec['prompt'] = rec['prompt'].replace(rec['attributes']['color'] + ' dachshund', 'chestnut dachshund')
        rec['prompt_sha256'] = stills.sha256_text(rec['prompt'])
        self.assertIn(stills.STANDING, ids(stills.check(rec, 'prompt', FLOOR, POOLS)))

    def test_asking_for_the_platforms_ai_label_is_held(self):
        rec = dict(rolled(), notes='Turn on the AI label when the post goes out.')
        failures = stills.check(rec, 'prompt', FLOOR, POOLS)
        self.assertEqual(ids(failures), {'no-ai-label'})
        self.assertIn('"no, do not turn on the AI label"', stills.lines(failures)[0])
        self.assertEqual(stills.check(dict(rolled(), notes='Keep the AI label off.'), 'prompt', FLOOR, POOLS), [])

    def test_a_missing_avoid_item_names_the_entry_it_guards(self):
        rec = rolled()
        rec['avoid'] = [a for a in rec['avoid'] if a != 'misshapen paws or toes']
        positive, _ = stills.split(rec['prompt'])
        rec['prompt'] = positive + '\n\nAvoid: ' + '; '.join(rec['avoid']) + '.'
        rec['prompt_sha256'] = stills.sha256_text(rec['prompt'])
        failures = stills.check(rec, 'prompt', FLOOR, POOLS)
        self.assertEqual(ids(failures), {'real-dogs'})
        self.assertIn('These dogs look fake and sometimes malformed.', stills.lines(failures)[0])


class FloorTest(unittest.TestCase):
    def test_every_check_names_a_floor_entry_that_exists(self):
        self.assertTrue(stills.coverage(FLOOR, POOLS))
        gone = copy.deepcopy(FLOOR)
        gone['entries'] = [e for e in gone['entries'] if e['id'] != 'real-dogs']
        with self.assertRaisesRegex(ValueError, 'real-dogs'):
            stills.coverage(gone, POOLS)

    def test_the_review_owes_a_verdict_on_every_still_review_entry_and_no_process_one(self):
        owed = {e['id'] for e in stills.owed(FLOOR)}
        self.assertTrue({'real-dogs', 'real-scruffy-dogs', 'stage-the-joke', 'ten-out-of-ten', 'no-ai-label'} <= owed)
        self.assertFalse({'one-status-page', 'no-priest', 'retire-weak-premise'} & owed)
        self.assertNotIn('voice-personality', owed)

    def test_a_new_still_entry_is_owed_a_verdict_at_once(self):
        grown = copy.deepcopy(FLOOR)
        grown['entries'].append({'id': 'new-still-rule', 'applies_to': ['still'], 'check': 'review: look', 'words': ['x']})
        self.assertIn('new-still-rule', {e['id'] for e in stills.owed(grown)})


class ReviewStageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = self.tmp.name
        self.db = ledger.connect(os.path.join(self.root, 'local/engine.sqlite3'))
        self.rec, self.row = stills.reserve(self.db, rolled(), SHA, quote(), '10', FLOOR, POOLS)
        rid = self.rec['reservation']['request_id']
        providers.transition(self.db, rid, 'submitted')
        providers.transition(self.db, rid, 'completed', {'job_id': 'job-1', 'actual_usd': '0', 'actual_credits': '0.25',
                                                         'observed_at': dt.datetime.now(dt.timezone.utc).isoformat()})
        os.makedirs(os.path.join(self.root, 'local/incoming'))
        self.image = os.path.join(self.root, 'local/incoming/still.png')
        Path(self.image).write_bytes(b'a generated still')
        self.review = {'image': 'local/incoming/still.png', 'by': 'tier 2 judge', 'verdicts': every_verdict(),
                       'score': 9, 'reason': 'reads as a real pet on a phone; the payoff lands with the caption covered'}

    def tearDown(self):
        self.db.close(); self.tmp.cleanup()

    def row_now(self):
        return dict(self.db.execute('SELECT * FROM provider_requests WHERE request_id=?',
                                    (self.rec['reservation']['request_id'],)).fetchone())

    def checked(self, review=None, rec=None):
        rec = stills.attach(rec or self.rec, review or self.review, self.root)
        return rec, stills.check(rec, 'review', FLOOR, POOLS, self.row_now(), self.root)

    def test_the_reservation_carries_the_exact_rolled_prompt(self):
        self.assertEqual(self.row['fingerprint'], stills.fingerprint(self.rec))
        self.assertEqual(self.row['credits_maximum'], '0.25')
        self.assertIn(self.rec['prompt'], stills.request_brief(self.rec))

    def test_a_complete_independent_review_at_nine_passes(self):
        rec, failures = self.checked()
        self.assertEqual(failures, [])
        self.assertEqual(rec['image']['sha256'], hashlib.sha256(b'a generated still').hexdigest())
        self.assertEqual(rec['image']['path'], 'local/incoming/still.png')

    def test_a_held_verdict_holds_the_still_with_his_words(self):
        review = dict(self.review, verdicts=dict(every_verdict(), **{'real-dogs': {'verdict': 'hold', 'note': 'five legs'}}))
        failures = self.checked(review)[1]
        self.assertEqual(ids(failures), {'real-dogs'})
        self.assertIn('five legs', stills.lines(failures)[0])

    def test_a_missing_verdict_or_a_bare_n_a_is_held(self):
        verdicts = every_verdict(); verdicts.pop('real-scruffy-dogs')
        verdicts['chat-lads-banter'] = {'verdict': 'n/a', 'note': ''}
        failures = self.checked(dict(self.review, verdicts=verdicts))[1]
        self.assertEqual(ids(failures), {'real-scruffy-dogs', 'chat-lads-banter'})

    def test_the_maker_cannot_review_its_own_still(self):
        failures = self.checked(dict(self.review, by='Maker Session'))[1]
        self.assertEqual(ids(failures), {'record'})

    def test_below_nine_or_no_reason_is_held(self):
        self.assertEqual(ids(self.checked(dict(self.review, score=8))[1]), {'spend-means-nine'})
        self.assertEqual(ids(self.checked(dict(self.review, reason=''))[1]), {'ten-out-of-ten'})

    def test_an_image_changed_after_review_is_held(self):
        rec = stills.attach(self.rec, self.review, self.root)
        Path(self.image).write_bytes(b'something else')
        failures = stills.check(rec, 'review', FLOOR, POOLS, self.row_now(), self.root)
        self.assertTrue(any('changed since it was reviewed' in f['reason'] for f in failures))

    def test_credits_not_yet_settled_or_reserved_for_another_prompt_are_held(self):
        rec = stills.attach(self.rec, self.review, self.root)
        row = dict(self.row_now(), status='submitted')
        self.assertTrue(any('not completed' in f['reason'] for f in stills.check(rec, 'review', FLOOR, POOLS, row, self.root)))
        row = dict(self.row_now(), fingerprint='0' * 64)
        self.assertIn('real-scruffy-dogs', ids(stills.check(rec, 'review', FLOOR, POOLS, row, self.root)))
        self.assertIn('record', ids(stills.check(rec, 'review', FLOOR, POOLS, None, self.root)))

    def test_a_held_prompt_reserves_nothing(self):
        before = self.db.execute('SELECT COUNT(*) FROM provider_requests').fetchone()[0]
        with self.assertRaises(stills.Held) as held:
            stills.reserve(self.db, dict(rolled(), script_score=8), SHA, quote(), '10', FLOOR, POOLS)
        self.assertEqual(ids(held.exception.failures), {'spend-means-nine'})
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM provider_requests').fetchone()[0], before)

    def test_a_reservation_never_exceeds_the_allowance(self):
        with self.assertRaisesRegex(ValueError, 'would be exceeded'):
            stills.reserve(self.db, rolled(), SHA, dict(quote(), credits='20'), '10', FLOOR, POOLS)

    def test_a_review_file_with_other_fields_or_no_image_is_refused(self):
        with self.assertRaises(ValueError):
            stills.attach(self.rec, dict(self.review, approved_by_krish=True), self.root)
        with self.assertRaises(ValueError):
            stills.attach(self.rec, dict(self.review, image='local/incoming/none.png'), self.root)


class CommandTest(unittest.TestCase):
    """growth.py still: the commands a session runs, end to end on synthetic paths."""

    def run_growth(self, *argv, env):
        return subprocess.run([sys.executable, os.path.join(ROOT, 'growth.py'), 'still', *argv],
                              capture_output=True, text=True, env=env, cwd=ROOT)

    def test_roll_then_check_names_what_is_owed(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, HEARTSIDE_DOG_ROLLS=os.path.join(tmp, 'rolls'),
                       HEARTSIDE_DOG_HISTORY=os.path.join(tmp, 'history.json'))
            out = self.run_growth('roll', '--count', '2', '--json', env=env)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn('growth.py floor --format still', out.stderr)
            recs = json.loads(out.stdout)
            self.assertEqual(len(recs), 2)
            check = self.run_growth('check', recs[0]['roll_id'], '--stage', 'prompt', env=env)
            self.assertEqual(check.returncode, 1)
            self.assertIn('spend-means-nine ("if you spend credits', check.stdout)
            template = self.run_growth('review', recs[0]['roll_id'], '--template', env=env)
            self.assertEqual(set(json.loads(template.stdout)['verdicts']), {e['id'] for e in stills.owed(FLOOR)})


if __name__ == '__main__':
    unittest.main()
