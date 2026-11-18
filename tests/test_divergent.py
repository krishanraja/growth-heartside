"""divergent-thinker through Control Center (engine/divergent.py), proved against stubs and the local stand-in only.

Dormant until Control Center serves features.divergent: no call, no error, one quiet line. Held means no diverge. A
spark becomes one plan behind strategy with its provenance evidence, after this engine's own copy and claims checks;
a 429 or 503 is a quiet line; the joke lab's screen rejects a rejected_archive candidate.
"""
import argparse
import copy
import datetime as dt
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

import growth
from engine import divergent, protocol
from engine.control_center import ProtocolError
from tests import test_protocol as tp
from tests.test_protocol import DIRECTIVE, SCHEMA, STATE, validate

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'factory'))
import jokelab  # noqa: E402

NOW = dt.datetime(2026, 11, 18, 6, 0, tzinfo=dt.timezone.utc)
SPARKS = [
    {'rank': 1, 'title': 'The shelter sleepover portrait', 'mechanism': 'Krish films one foster dog\'s first night in a '
     'home and the store paints that dog for the foster family as the thank-you.', 'whyNonObvious': 'It sells the '
     'feeling of the gift without selling, and fosters share their own dogs.', 'firstStep': 'Ask one local rescue that '
     'already fosters on Instagram whether a foster family would like a portrait.', 'lens': 'inversion',
     'kind': 'partnership', 'conventionalTwin': 'Gift products to influencers', 'survivedAttack': True, 'score': 0.81},
    {'rank': 2, 'title': 'The dog park photo wall', 'mechanism': 'Collect strangers\' dog photos at the park and post '
     'them as painted portraits.', 'whyNonObvious': 'Nobody paints the dogs of people they just met.', 'firstStep':
     'Go to the park on Saturday.', 'lens': 'analogy', 'kind': 'event', 'survivedAttack': True, 'score': 0.77},
    {'rank': 3, 'title': 'The receipt reel', 'mechanism': 'A reel that reads the gift note out loud as the box opens.',
     'whyNonObvious': 'The note is the part people remember.', 'firstStep': 'Film one unboxing of the store\'s own '
     'sample.', 'lens': 'zoom', 'kind': 'content', 'survivedAttack': False, 'score': 0.7},
]
ANSWER = {'ok': True, 'runId': 'dvg_test123', 'consensus': {'obvious': ['post more'], 'orthodoxies': []}, 'sparks': SPARKS}


def body(urgency=5, held=False):
    out = copy.deepcopy(DIRECTIVE['directive'])
    out['north_star'] = {'own': {'urgency': urgency, 'week_target': 4862, 'current': 0}}
    if held:
        out['next_action'] = {'proposal_id': None, 'instruction': 'Krish has held this engine. Nothing runs.'}
    return out


class Stub:
    """A Control Center client that only records: never a network call."""

    def __init__(self, answer=ANSWER, error=None, features=None, reports=()):
        self.answer, self.error, self.features, self.reports, self.calls = answer, error, features, list(reports), []

    def capabilities(self):
        return self.features or {}

    def divergent(self, body, timeout=None):
        self.calls.append((body, timeout))
        if self.error:
            raise self.error
        return self.answer

    def recent_reports(self, n=10):
        return self.reports


class Recovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def recover(self, client, features=None, urgency=5, held=False, mode='live'):
        return divergent.recovery(
            root=self.root, growth=growth, client=client, body=body(urgency, held),
            features={'divergent': True} if features is None else features, state=copy.deepcopy(STATE),
            organic={'value': 0}, north_star='Heartside net sales attributed to organic posts: $50,000 by 2026-12-28.',
            held=held, mode=mode, now=NOW, recent_reports=client.recent_reports)

    def test_flag_off_or_absent_makes_no_call_and_says_so_quietly(self):
        for features in ({}, {'divergent': False}, {'humour': True}):
            stub = Stub()
            out = self.recover(stub, features=features)
            self.assertEqual(stub.calls, [])
            self.assertEqual(out, {'proposals': [], 'activity': [divergent.NOT_SERVED]})

    def test_held_below_u4_or_synthetic_never_diverges(self):
        for kwargs in ({'held': True}, {'urgency': 3}, {'mode': 'synthetic'}):
            stub = Stub()
            self.assertEqual(self.recover(stub, **kwargs), {'proposals': [], 'activity': []})
            self.assertEqual(stub.calls, [])

    def test_sparks_become_one_plan_with_provenance_after_the_checks(self):
        stub = Stub()
        out = self.recover(stub)
        request, timeout = stub.calls[0]
        self.assertEqual(timeout, 300)
        self.assertEqual((request['op'], request['target'], request['count'], request['namespace']),
                         ('diverge', 'strategy', 3, 'growth-heartside'))
        self.assertIn('Offer a discount code', request['cliches'])
        self.assertIn('elevate', request['bannedWords'])
        self.assertIn('delve', request['bannedWords'])
        self.assertNotIn('@', request['problem'])
        self.assertEqual(len(out['proposals']), 1)  # one ask per engine at a time
        plan = out['proposals'][0]
        self.assertEqual((plan['stage'], plan['wall'], plan['kind']), ('plan', 'strategy', 'prepared'))
        self.assertEqual(plan['evidence'], [{'label': 'divergent-thinker spark 1, run dvg_test123', 'url': None}])
        self.assertIn('The shelter sleepover portrait', plan['exact_payload'])
        self.assertTrue(protocol.ID.match(plan['proposal_id']))
        lines = '\n'.join(out['activity'])
        self.assertIn('Held divergent-thinker spark 2', lines)  # strangers' photos: rule 6 and the 18 Nov run
        self.assertIn('permission', lines)
        self.assertIn('Kept divergent-thinker spark 3', lines)  # in reserve, never a second ask
        report = protocol.build_report(root=self.root, state=copy.deepcopy(STATE), db=None, now=NOW,
                                       run_id='heartside:2026-11-18:directive-1', mode='live', directive=DIRECTIVE,
                                       recommendations=[], divergent=out)
        self.assertEqual(validate(SCHEMA, report), [])
        self.assertEqual([p['proposal_id'] for p in report['proposals']], [plan['proposal_id']])

    def test_the_18_nov_plays_are_held_by_the_walls(self):
        consent = {'title': 'Paint the park', 'mechanism': 'Use photos from strangers at the dog park in a reel.',
                   'whyNonObvious': 'Real dogs.', 'firstStep': 'Screenshot the photos from the park group.'}
        ai_art = {'title': 'Portrait drop', 'mechanism': 'Share AI portraits in breed subreddits each week.',
                  'whyNonObvious': 'They love their breed.', 'firstStep': 'Post in r/dachshund.'}
        self.assertTrue(any('permission' in p for p in divergent.spark_problems(consent, growth)))
        self.assertTrue(any('AI art' in p for p in divergent.spark_problems(ai_art, growth)))
        loud = dict(SPARKS[0], title='Elevate the gift game!')
        refused = divergent.spark_problems(loud, growth)
        self.assertTrue(any('elevate' in p for p in refused) and any('exclamation' in p for p in refused))
        self.assertEqual(divergent.spark_problems(SPARKS[2], growth), [])

    def test_a_429_or_503_is_a_quiet_line(self):
        for code, status in (('daily_diverge_cap_reached', 429), ('embedder_uncalibrated', 503)):
            stub = Stub(error=ProtocolError(code, status))
            with tempfile.TemporaryDirectory() as root:
                self.root = Path(root)
                out = self.recover(stub)
            self.assertEqual(out['proposals'], [])
            self.assertIn(code, out['activity'][0])

    def test_once_a_day_and_never_over_a_play_still_waiting(self):
        stub = Stub()
        self.recover(stub)
        again = self.recover(stub)
        self.assertEqual(len(stub.calls), 1)
        self.assertIn('once a day', again['activity'][0])
        waiting = [{'run_id': 'heartside:2026-11-17:directive-9', 'activity': [
            {'line': 'Proposed divergent-thinker recovery play heartside:divergent:dvg_x:1 ("A") behind strategy.'}]}]
        with tempfile.TemporaryDirectory() as root:
            self.root = Path(root)
            stub = Stub(reports=waiting)
            out = self.recover(stub)
            self.assertEqual(stub.calls, [])
            self.assertIn('still waits on Krish', out['activity'][0])

    def test_urgency_falls_back_to_now_md(self):
        (self.root / 'NOW.md').write_text('<!-- north-star-state {"urgency": 4, "current": 0} --> x\n')
        self.assertEqual(divergent.own_urgency({}, self.root), 4)
        self.assertEqual(divergent.own_urgency(body(5), self.root), 5)
        self.assertIsNone(divergent.own_urgency({}, self.root / 'nowhere'))

    def test_cliches_come_from_the_order_loop_plan(self):
        cliches = divergent.plan_cliches(Path(__file__).resolve().parent.parent)
        self.assertTrue(any(c.startswith("Krish's warm post") for c in cliches))
        self.assertEqual(cliches[-4:], list(divergent.GENERIC_CLICHES))


class RealWords(tp.FakeGrowth):
    """The stand-in's growth, with this engine's real copy checks and word lists."""
    BANNED, SLOP, problems = growth.BANNED, growth.SLOP, staticmethod(growth.problems)


class Loop(unittest.TestCase):
    """Through protocol.main against the local stand-in, in live mode at U5 with nothing else proposed."""
    tearDown = tp.LoopTests.tearDown

    def main(self, mode='live'):
        return tp.LoopTests.main(self, mode=mode, growth=RealWords())

    def setUp(self):
        tp.LoopTests.setUp(self)
        self.stand.directive['directive']['north_star'] = {'own': {'urgency': 5}}

    def test_unserved_route_is_never_called(self):
        code, _ = self.main(mode='live')
        self.assertEqual(code, 0)
        self.assertEqual(self.stand.routes('POST', 'divergent'), [])
        report = self.stand.routes('POST', 'reports')[0][2]
        self.assertIn(divergent.NOT_SERVED, [a['line'] for a in report['activity']])

    def test_served_route_puts_one_plan_on_the_report(self):
        self.stand.features = {'divergent': True, 'recent_reports': True}
        self.stand.divergent = lambda body: (200, ANSWER)
        code, out = self.main(mode='live')
        self.assertEqual(code, 0)
        self.assertEqual(len(self.stand.routes('POST', 'divergent')), 1)
        report = self.stand.routes('POST', 'reports')[0][2]
        self.assertEqual(len(report['proposals']), 1)
        self.assertEqual(report['proposals'][0]['evidence'][0]['label'], 'divergent-thinker spark 1, run dvg_test123')
        self.assertIn('heartside:divergent:', json.loads(out)['divergent'][0])

    def test_a_capped_route_never_fails_the_run(self):
        self.stand.features = {'divergent': True}
        self.stand.divergent = lambda body: (429, {'ok': False, 'error': 'daily_diverge_cap_reached'})
        code, _ = self.main(mode='live')
        self.assertEqual(code, 0)
        report = self.stand.routes('POST', 'reports')[0][2]
        self.assertEqual(report['proposals'], [])
        self.assertTrue(any('daily_diverge_cap_reached' in a['line'] for a in report['activity']))


class JokeLabScreen(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        jokelab.VERDICTS = os.path.join(self.tmp.name, 'verdicts.jsonl')
        jokelab.RUNS = os.path.join(self.tmp.name, 'runs')

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_rejected_archive_candidate_is_rejected_and_labelled(self):
        from tests.test_jokelab import cand
        seen = []

        def scorer(problem, ideas, obvious, banned=()):
            seen.append((ideas, obvious, banned))
            return [{'status': 'rejected_archive'}, {'status': 'accepted'}, {'status': 'rejected_gravity'}]
        rec = jokelab.screen([cand(1), cand(2), cand(4)], divergent=scorer)
        reasons = {r['id']: r['reasons'] for r in rec['rejected']}
        self.assertIn('rejected_archive', reasons['c01'][0])
        self.assertIn('rejected_gravity', reasons['c04'][0])
        self.assertEqual([c['id'] for c in rec['shortlist']], ['c02'])
        ideas, obvious, banned = seen[0]
        self.assertEqual(len(ideas), 3)
        self.assertTrue(any('He has an alibi' in o for o in obvious))
        self.assertIn('elevate', banned)

    def test_a_failed_or_absent_scorer_leaves_the_screen_as_it_was(self):
        from tests.test_jokelab import cand

        def broken(*args, **kwargs):
            raise ProtocolError('embedder_uncalibrated', 503)
        plain = jokelab.screen([cand(1), cand(2)])
        failed = jokelab.screen([cand(1), cand(2)], divergent=broken)
        self.assertEqual([c['id'] for c in plain['shortlist']], [c['id'] for c in failed['shortlist']])
        self.assertIn('embedder_uncalibrated', failed['divergent'])
        self.assertEqual(plain['divergent'], 'not consulted')


class Record(unittest.TestCase):
    def test_only_newly_live_public_words_are_recorded_and_only_when_served(self):
        events = [{'event_id': 'a', 'type': 'social', 'record': {'kind': 'engagement', 'stage': 'live_verified', 'text': 'He has an alibi.'}},
                  {'event_id': 'b', 'type': 'social', 'record': {'kind': 'engagement', 'stage': 'approved', 'text': 'Not live yet.'}},
                  {'event_id': 'c', 'type': 'social', 'record': {'kind': 'engagement', 'stage': 'live_verified', 'text': 'Imported before.'}}]
        results = [{'event_id': 'a', 'status': 'applied'}, {'event_id': 'b', 'status': 'applied'}, {'event_id': 'c', 'status': 'already_applied'}]
        self.assertEqual(divergent.live_captions('.', events, results), ['He has an alibi.'])
        self.assertIn('no Control Center engine token', divergent.record_live('.', events, results, env={}))
        stub = Stub(answer={'ok': True}, features={'divergent': True})
        self.assertEqual(divergent.record(stub, ['He has an alibi.'], 'live 2026-11-18'), 1)
        sent = stub.calls[0][0]
        self.assertEqual((sent['op'], sent['namespace'], sent['items']), ('record', 'growth-heartside:jokes', ['He has an alibi.']))


if __name__ == '__main__':
    unittest.main()


class AtWillStub(Stub):
    """Served by default; directive() answers a held or unheld engine, or raises."""

    def __init__(self, answer=None, error=None, served=True, held=False, directive_error=None):
        super().__init__(answer or {'ok': True, 'runId': 'dvg_at_will'}, error, {'divergent': served})
        self.held, self.directive_error, self.directive_reads = held, directive_error, 0

    def directive(self, date=None):
        self.directive_reads += 1
        if self.directive_error:
            raise self.directive_error
        return {'ok': True, 'directive': body(5, self.held)}


class AtWill(unittest.TestCase):
    """growth.py divergent <op>: the body each op builds, the namespace, the exit codes and the hold."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def file(self, name, text):
        path = self.root / name
        path.write_text(text, encoding='utf-8')
        return str(path)

    def args(self, **kw):
        base = dict(problem=None, context=None, idea=None, ideas_file=None, obvious_file=None, items_file=None,
                    cliche=None, count=None, target=None, temperament=None, lane=None, judge=False)
        base.update(kw)
        return argparse.Namespace(**base)

    def consult(self, op, client, **kw):
        out, err = io.StringIO(), io.StringIO()
        code = divergent.consult(op, self.args(**kw), growth, client=client, out=out, err=err, root=self.root,
                                 today=dt.date(2026, 11, 18))
        return code, out.getvalue(), err.getvalue()

    def test_each_op_builds_the_contract_body(self):
        banned = divergent.banned_words(growth)
        ideas = self.file('ideas.json', json.dumps(['A dog that files taxes', 'A dog that reviews mugs']))
        obvious = self.file('obvious.txt', 'Dog in a sweater\n\nDog with a mug\n')
        items = self.file('items.txt', 'The caption that went live\n')
        cases = {
            'map': (dict(problem='P', context='C'), {'op': 'map', 'problem': 'P', 'context': 'C', 'namespace': 'growth-heartside'}),
            'provoke': (dict(problem='P', count=4, cliche=['Post more', 'Run ads'], target='content', temperament='wild'),
                        {'op': 'provoke', 'problem': 'P', 'count': 4, 'cliches': ['Post more', 'Run ads'], 'target': 'content',
                         'temperament': 'wild', 'bannedWords': banned, 'namespace': 'growth-heartside'}),
            'challenge': (dict(problem='P', idea='I'), {'op': 'challenge', 'problem': 'P', 'idea': 'I', 'namespace': 'growth-heartside'}),
            'diverge': (dict(problem='P', context='C'), {'op': 'diverge', 'problem': 'P', 'context': 'C', 'bannedWords': banned,
                                                         'namespace': 'growth-heartside'}),
            'score': (dict(problem='P', ideas_file=ideas, obvious_file=obvious, judge=True),
                      {'op': 'score', 'problem': 'P', 'ideas': ['A dog that files taxes', 'A dog that reviews mugs'],
                       'obvious': ['Dog in a sweater', 'Dog with a mug'], 'bannedWords': banned, 'judge': True,
                       'namespace': 'growth-heartside'}),
            'record': (dict(items_file=items), {'op': 'record', 'items': ['The caption that went live'],
                                                'label': 'at will 2026-11-18', 'namespace': 'growth-heartside'}),
        }
        for op, (kw, expected) in cases.items():
            with self.subTest(op=op):
                stub = AtWillStub(answer={'ok': True, 'results': [{'status': 'accepted'}] * 2} if op == 'score' else None)
                code, out, _ = self.consult(op, stub, **kw)
                self.assertEqual(code, 0)
                self.assertEqual(stub.calls[0][0], expected)
                self.assertEqual(len(stub.calls), 1)  # never retried
                self.assertTrue(json.loads(out)['ok'])
        self.assertEqual(divergent._marker(self.root).get('last_diverge_day'), '2026-11-18')  # the daily report skips

    def test_banned_words_are_this_engines_own_lists(self):
        self.assertEqual(set(divergent.banned_words(growth)), set(growth.BANNED) | set(growth.SLOP))

    def test_lane_sets_the_namespace_and_a_bad_lane_is_refused(self):
        stub = AtWillStub()
        self.assertEqual(self.consult('map', stub, problem='P', lane='jokes')[0], 0)
        self.assertEqual(stub.calls[0][0]['namespace'], 'growth-heartside:jokes')
        stub = AtWillStub()
        code, _, err = self.consult('map', stub, problem='P', lane='Bad Lane!')
        self.assertEqual((code, stub.calls), (2, []))
        self.assertIn('--lane', err)

    def test_score_exits_1_when_anything_is_flagged(self):
        ideas = self.file('ideas.txt', 'one\ntwo\n')
        stub = AtWillStub(answer={'ok': True, 'results': [{'status': 'accepted'}, {'status': 'rejected_archive'}]})
        code, out, _ = self.consult('score', stub, problem='P', ideas_file=ideas)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)['results'][1]['status'], 'rejected_archive')

    def test_refusals_caps_and_uncalibrated_exit_2_with_the_reason_on_stderr(self):
        for error in (ProtocolError('daily_diverge_cap_reached', 429), ProtocolError('embedder_uncalibrated', 503),
                      ProtocolError('connection_failed')):
            with self.subTest(code=error.code):
                stub = AtWillStub(error=error)
                code, out, err = self.consult('provoke', stub, problem='P')
                self.assertEqual((code, out), (2, ''))
                self.assertIn(error.code, err)
                self.assertEqual(len(stub.calls), 1)

    def test_held_refuses_generating_ops_but_score_and_record_run(self):
        for op in divergent.GENERATING:
            with self.subTest(op=op):
                stub = AtWillStub(held=True)
                code, _, err = self.consult(op, stub, problem='P', idea='I')
                self.assertEqual((code, stub.calls), (2, []))
                self.assertIn('holds this engine', err)
        self.assertEqual(divergent._marker(self.root), {})
        stub = AtWillStub(held=True, answer={'ok': True, 'results': [{'status': 'accepted'}]})
        self.assertEqual(self.consult('score', stub, problem='P', ideas_file=self.file('i.txt', 'one'))[0], 0)
        stub = AtWillStub(held=True)
        self.assertEqual(self.consult('record', stub, items_file=self.file('r.txt', 'live words'))[0], 0)
        self.assertEqual(stub.directive_reads, 0)

    def test_an_unread_directive_never_generates(self):
        stub = AtWillStub(directive_error=ProtocolError('connection_failed'))
        code, _, err = self.consult('diverge', stub, problem='P')
        self.assertEqual((code, stub.calls), (2, []))
        self.assertIn('hold could not be ruled out', err)

    def test_not_served_is_exit_2_with_no_call(self):
        stub = AtWillStub(served=False)
        code, out, err = self.consult('score', stub, problem='P', ideas_file=self.file('i.txt', 'one'))
        self.assertEqual((code, out, stub.calls), (2, '', []))
        self.assertIn('not served', err)
        out, err = io.StringIO(), io.StringIO()  # no token in the environment: no client, no call
        code = divergent.consult('map', self.args(problem='P'), growth, env={}, out=out, err=err)
        self.assertEqual((code, out.getvalue()), (2, ''))
        self.assertIn('no Control Center engine token', err.getvalue())

    def test_the_command_line_reaches_consult(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, CONTROL_CENTER_ENGINE_TOKEN='')
            import subprocess
            run = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), '..', 'growth.py'), 'divergent',
                                  'map', '--problem', 'P'], capture_output=True, text=True, env=env, cwd=tmp)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, '')
        self.assertIn('not consulted', run.stderr)
