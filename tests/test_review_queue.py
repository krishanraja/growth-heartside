"""I-24: Heartside's asks reach Krish's one list and his answers are read back by id (Ruling, Krish, 2026-11-14)."""
import copy
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest

from engine import review_queue, protocol
from tests.test_protocol import DIRECTIVE, NOW, SCHEMA, STATE, LoopTests, validate

ROOT = Path(__file__).resolve().parent.parent


def queue(*items, per_report=3):
    return {'schema': 'heartside-review-queue/1', 'about': 'test', 'per_report': per_report, 'items': list(items)}


def ask(n, answer=None, kind='decision', amount=None):
    return {'id': f'heartside:ask:t{n}', 'priority': n, 'kind': kind, 'title': f'Ask {n}', 'question': f'Question {n}?',
            'on_yes': f'Yes does {n}.', 'on_no': f'No does {n}.', 'amount_usd': amount, 'asked_on': '2026-11-14',
            'source': 'docs/plans/A1.md', 'answer': answer}


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / 'review').mkdir()
        (self.root / 'config').mkdir()
        (self.root / 'config/channels.json').write_text((ROOT / 'config/channels.json').read_text())

    def tearDown(self):
        self.temporary.cleanup()

    def write(self, doc):
        (self.root / 'review/queue.json').write_text(json.dumps(doc))

    def build(self, decisions=None, directive=None):
        return protocol.build_report(root=self.root, state=copy.deepcopy(STATE), db=None, now=NOW,
                                     run_id='heartside:2026-10-19:synthetic-queue', mode='synthetic',
                                     directive=directive, recommendations=[], queue_decisions=decisions)

    def test_the_committed_queue_is_valid_and_carries_the_open_asks(self):
        items = review_queue.load(ROOT)
        self.assertGreaterEqual(len(items), 15)
        self.assertEqual(sorted(i['priority'] for i in items), list(range(1, len(items) + 1)))
        self.assertEqual(len({i['id'] for i in items}), len(items))
        for item in items:
            self.assertNotIn(chr(0x2014), json.dumps(item, ensure_ascii=False))
            self.assertNotIn('!', item['question'] + item['on_yes'] + item['on_no'])

    def test_open_asks_are_walled_plans_in_priority_order_bound_to_their_words(self):
        self.write(queue(ask(2), ask(1), ask(3, kind='spend', amount=20), ask(4)))
        report = self.build(decisions=[])
        self.assertEqual(validate(SCHEMA, report), [])
        asks = [p for p in report['proposals'] if p['proposal_id'].startswith('heartside:ask:')]
        self.assertEqual([p['proposal_id'] for p in asks], ['heartside:ask:t1', 'heartside:ask:t2', 'heartside:ask:t3'])
        first, _, spend = asks
        self.assertEqual((first['wall'], first['kind'], first['stage'], first['amount_usd']), ('strategy', 'prepared', 'plan', None))
        self.assertEqual((spend['wall'], spend['amount_usd']), ('spend', 20))
        self.assertIn('Question 1?', first['exact_payload'])
        self.assertIn('On yes: Yes does 1.', first['exact_payload'])
        self.assertIn('On no: No does 1.', first['exact_payload'])
        self.assertEqual(first['payload_sha256'], review_queue.payload_sha256(ask(1)))
        self.assertNotEqual(review_queue.payload_sha256(ask(1)), review_queue.payload_sha256(dict(ask(1), question='Changed?')))

    def test_an_answer_on_the_current_words_stops_the_ask_and_is_reported_to_apply(self):
        self.write(queue(ask(1), ask(2), ask(3)))
        sha = review_queue.payload_sha256(ask(1))
        decisions = [{'proposal_id': 'heartside:ask:t1', 'decision': 'approved', 'decided_at': '2026-11-15T07:00:00Z',
                      'payload_sha256': sha, 'stage': 'plan', 'amended': False},
                     {'proposal_id': 'heartside:ask:t2', 'decision': 'declined', 'decided_at': '2026-11-15T07:00:00Z',
                      'payload_sha256': 'f' * 64, 'stage': 'plan', 'amended': False}]
        report = self.build(decisions=decisions)
        ids = [p['proposal_id'] for p in report['proposals']]
        self.assertNotIn('heartside:ask:t1', ids)
        self.assertIn('heartside:ask:t2', ids)  # answered on other words: it goes back to him
        lines = [a['line'] for a in report['activity']]
        self.assertIn('Answers to apply: 1 (heartside:ask:t1 approved).', lines)
        self.assertEqual(review_queue.to_apply(review_queue.load(self.root), decisions),
                         [{'id': 'heartside:ask:t1', 'decision': 'approved', 'decided_at': '2026-11-15T07:00:00Z', 'amended': False}])

    def test_an_applied_answer_is_neither_asked_nor_counted(self):
        applied = {'decision': 'declined', 'decided_at': '2026-11-15T07:00:00Z', 'applied_on': '2026-11-15', 'where': 'CHANGES.md'}
        self.write(queue(ask(1, answer=applied), ask(2)))
        report = self.build(decisions=[{'proposal_id': 'heartside:ask:t1', 'decision': 'declined',
                                        'decided_at': '2026-11-15T07:00:00Z', 'payload_sha256': review_queue.payload_sha256(ask(1)),
                                        'stage': 'plan', 'amended': False}])
        self.assertEqual([p['proposal_id'] for p in report['proposals']], ['heartside:ask:t2'])
        self.assertIn('Answers to apply: 0.', [a['line'] for a in report['activity']])

    def test_decisions_unread_holds_and_applies_nothing(self):
        self.write(queue(ask(1)))
        report = self.build(decisions=None)
        self.assertEqual(validate(SCHEMA, report), [])
        self.assertIn('decisions_unread', [h['reason'] for h in report['holds']])
        self.assertIn('heartside:ask:t1', [p['proposal_id'] for p in report['proposals']])
        self.assertFalse(any(a['line'].startswith('Answers to apply') for a in report['activity']))

    def test_the_directive_s_decisions_count_when_the_read_fails(self):
        self.write(queue(ask(1)))
        directive = copy.deepcopy(DIRECTIVE)
        directive['directive']['decisions_since'] = [{'proposal_id': 'heartside:ask:t1', 'decision': 'done',
                                                     'decided_at': '2026-11-15T07:00:00Z', 'payload_sha256': review_queue.payload_sha256(ask(1)),
                                                     'stage': 'plan', 'amended': False}]
        report = self.build(decisions=None, directive=directive)
        self.assertNotIn('heartside:ask:t1', [p['proposal_id'] for p in report['proposals']])

    def test_no_queue_file_is_no_asks_and_no_hold(self):
        report = self.build(decisions=None)
        self.assertEqual([h['reason'] for h in report['holds'] if h['reason'] == 'decisions_unread'], [])

    def test_a_malformed_item_is_refused(self):
        for bad in (dict(ask(1), id='bad id'), dict(ask(1), kind='post'), dict(ask(1), kind='spend', amount_usd=None),
                    dict(ask(1), question='')):
            self.write(queue(bad))
            with self.assertRaises(ValueError):
                review_queue.load(self.root)

    def test_since_reaches_back_to_the_oldest_open_ask(self):
        items = [ask(1), dict(ask(2), asked_on='2026-11-01')]
        self.assertEqual(review_queue.since(items, dt.datetime(2026, 11, 20, tzinfo=dt.timezone.utc)), '2026-11-01T00:00:00Z')
        self.assertIsNone(review_queue.since([ask(1, answer={'decision': 'done', 'decided_at': 'x', 'applied_on': 'y', 'where': 'z'})], NOW))


class QueueLoopTests(LoopTests):
    """The live loop against the local stand-in: his answers are read before the report, by id."""

    def test_the_run_reads_answers_first_stops_the_answered_ask_and_names_it_to_apply(self):
        (self.root / 'review').mkdir()
        (self.root / 'review/queue.json').write_text(json.dumps(queue(ask(1), ask(2))))
        self.stand.decisions = [{'proposal_id': 'heartside:ask:t1', 'decision': 'declined', 'decided_at': '2026-10-19T07:00:00Z',
                                 'payload_sha256': review_queue.payload_sha256(ask(1)), 'stage': 'plan', 'amended': False}]
        code, out = self.main()
        self.assertEqual(code, 0)
        order = [(c[0], c[1].split('?')[0]) for c in self.stand.calls]
        self.assertLess(order.index(('GET', 'decisions')), order.index(('POST', 'reports')))
        posted = self.stand.routes('POST', 'reports')[0][2]
        self.assertEqual(validate(SCHEMA, posted), [])
        self.assertEqual([p['proposal_id'] for p in posted['proposals']], ['heartside:ask:t2'])
        summary = json.loads(out)
        self.assertEqual(summary['answers_to_apply'], ['heartside:ask:t1'])
        self.assertEqual((summary['posted'], summary['sent'], summary['spent_usd']), (0, 0, 0))

    def test_the_session_start_read_lists_each_answer_to_apply(self):
        (self.root / 'review').mkdir()
        (self.root / 'review/queue.json').write_text(json.dumps(queue(ask(1), ask(2))))
        self.stand.decisions = [{'proposal_id': 'heartside:ask:t2', 'decision': 'approved', 'decided_at': '2026-11-15T07:00:00Z',
                                 'payload_sha256': review_queue.payload_sha256(ask(2)), 'stage': 'plan', 'amended': True}]
        code, out = self.main('queue')
        self.assertEqual(code, 0)
        self.assertIn('Answers to apply: 1 (heartside:ask:t2 approved amended).', out)
        self.assertIn('apply heartside:ask:t2: approved', out)
        self.env.pop('CONTROL_CENTER_ENGINE_TOKEN')
        code, out = self.main('queue')
        self.assertEqual(code, 1)
        self.assertIn('Decisions unread', out)


if __name__ == '__main__':
    unittest.main()
