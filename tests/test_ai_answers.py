"""AI answers through AEO-Engine, the one specialist (protocol 1.22.0; Ruling, Krish, 2026-11-12)."""
import unittest
from pathlib import Path

from engine import ai_answers

ROOT = Path(__file__).resolve().parent.parent


class FakeClient:
    def __init__(self, fail=False):
        self.posted = []
        self.fail = fail

    def answers_request(self, body):
        if self.fail:
            raise RuntimeError('down')
        self.posted.append(body)
        return {'ok': True, 'request_id': '0b4f6a1e-7c2d-4e8a-9b1f-3d5c7e9a2b4c', 'questions': len(body['questions'])}


def directive(standing='absent', features=True):
    body = {'directive_id': 'heartside:2026-11-13', 'features': {'engine_state': True, 'krish_instruction': True, **({'ai_answers': True} if features else {})}}
    if standing != 'absent':
        body['ai_answers'] = {'standing': standing, 'rule': 'synthetic rule'}
    return {'ok': True, 'chosen_by': 'rule', 'directive': body}


class AiAnswersTest(unittest.TestCase):
    def test_the_bank_gives_its_buyer_questions_best_first_at_most_25(self):
        qs = ai_answers.questions(ROOT)
        self.assertTrue(0 < len(qs) <= 25)
        self.assertTrue(all(8 <= len(q) <= 300 for q in qs))
        self.assertEqual(len(qs), len(set(qs)))
        self.assertTrue(all('@' not in q and 'http' not in q for q in qs), 'a buyer question carries no address or link')

    def test_with_no_request_on_file_it_asks_aeo_once_naming_heartside_io(self):
        client = FakeClient()
        lines = ai_answers.sync(client, directive({'product_slug': 'heartside', 'tracked': False, 'latest': None, 'misses': [], 'moves': [], 'history': [], 'request': None}), ROOT)
        self.assertEqual(len(client.posted), 1)
        self.assertEqual(client.posted[0]['domains'], ['heartside.io'])
        self.assertEqual(lines[0], 'AI answers: not tracked yet.')
        self.assertIn('Asked AEO-Engine to track', lines[1])

    def test_with_a_request_on_file_it_only_says_where_heartside_stands(self):
        client = FakeClient()
        standing = {'product_slug': 'heartside', 'tracked': True, 'latest': {'as_of': '2026-11-22', 'asked': 20, 'cited_first': 2, 'share': 10},
                    'misses': [{'question': 'What can I get my wife from the dog?', 'first': 'rival.example'}],
                    'moves': [{'title': 'Answer the wife question plainly', 'target_query': 'What can I get my wife from the dog?'}, {'title': 'A new page', 'target_query': None}],
                    'history': [], 'request': {'id': 'x', 'state': 'served', 'questions': 20, 'requested_at': '2026-11-13T05:00:00Z', 'served_at': '2026-11-22T10:00:00Z'}}
        lines = ai_answers.sync(client, directive(standing), ROOT)
        self.assertEqual(client.posted, [])
        self.assertEqual(lines, ['AI answers: cited first on 2 of 20 questions, 22 Nov.'])
        self.assertEqual(ai_answers.misses_and_moves(standing), ['What can I get my wife from the dog?', 'A new page'])

    def test_a_directive_that_serves_no_ai_answers_changes_nothing_and_a_failure_is_one_line(self):
        self.assertEqual(ai_answers.sync(FakeClient(), directive(features=False), ROOT), [])
        self.assertEqual(ai_answers.sync(FakeClient(), None, ROOT), [])
        lines = ai_answers.sync(FakeClient(fail=True), directive(None), ROOT)
        self.assertIn('Could not ask AEO-Engine', lines[-1])


if __name__ == '__main__':
    unittest.main()
