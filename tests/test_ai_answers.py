"""AI answers through AEO-Engine, the one specialist (protocol 1.22.0; Ruling, Krish, 2026-11-12)."""
import json
import tempfile
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


def on_file(questions, state='open'):
    """A synthetic standing whose request on file carries `questions` (a count, as Control Center serves it)."""
    return {'product_slug': 'heartside', 'tracked': True, 'latest': None, 'misses': [], 'moves': [], 'history': [],
            'request': {'id': 'r1', 'state': state, 'questions': questions, 'requested_at': '2026-11-13T05:00:00Z', 'served_at': None}}


def bank_root(questions):
    """A synthetic checkout whose question bank holds exactly these questions, best first."""
    tmp = tempfile.TemporaryDirectory()
    path = Path(tmp.name) / ai_answers.BANK
    path.parent.mkdir(parents=True)
    rows = [{'id': f'q{i:02d}', 'priority': 1, 'tier': 1, 'question': q} for i, q in enumerate(questions)]
    path.write_text(json.dumps({'questions': rows}))
    return tmp


SYNTHETIC = [f'What can I get my dog walker number {word} from the dog?' for word in
             ('one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen '
              'sixteen seventeen eighteen nineteen twenty twentyone twentytwo twentythree twentyfour '
              'twentyfive twentysix twentyseven').split()]
REFUSED = ['Short?',  # under 8 characters
           'Why ' + 'so ' * 110 + 'long?',  # over 300 characters
           'Can I email gifts@example.com about a dog mug?',  # an address
           'Is https://example.com a good dog gift shop?',  # a link
           'Is www.example.com a good dog gift shop?',  # a link without a scheme
           'Should I call 555 010 0199 to order a dog portrait?']  # a number


class AiAnswersTest(unittest.TestCase):
    def test_the_bank_gives_its_buyer_questions_best_first_at_most_25(self):
        qs = ai_answers.questions(ROOT)
        self.assertTrue(0 < len(qs) <= 25)
        self.assertTrue(all(8 <= len(q) <= 300 for q in qs))
        self.assertEqual(len(qs), len(set(qs)))
        self.assertTrue(all('@' not in q and 'http' not in q for q in qs), 'a buyer question carries no address or link')
        self.assertTrue(all(ai_answers.valid(q) for q in qs), 'every question passes the protocol\'s own test')

    def test_with_no_request_on_file_it_asks_aeo_once_naming_heartside_io(self):
        client = FakeClient()
        lines = ai_answers.sync(client, directive({'product_slug': 'heartside', 'tracked': False, 'latest': None, 'misses': [], 'moves': [], 'history': [], 'request': None}), ROOT)
        self.assertEqual(len(client.posted), 1)
        self.assertEqual(client.posted[0]['domains'], ['heartside.io'])
        self.assertEqual(lines[0], 'AI answers: not tracked yet.')
        self.assertIn('Asked AEO-Engine to track', lines[1])

    def test_with_a_request_on_file_for_the_whole_bank_it_only_says_where_heartside_stands(self):
        client = FakeClient()
        whole = len(ai_answers.questions(ROOT))
        standing = {'product_slug': 'heartside', 'tracked': True, 'latest': {'as_of': '2026-11-22', 'asked': 20, 'cited_first': 2, 'share': 10},
                    'misses': [{'question': 'What can I get my wife from the dog?', 'first': 'rival.example'}],
                    'moves': [{'title': 'Answer the wife question plainly', 'target_query': 'What can I get my wife from the dog?'}, {'title': 'A new page', 'target_query': None}],
                    'history': [], 'request': {'id': 'x', 'state': 'served', 'questions': whole, 'requested_at': '2026-11-13T05:00:00Z', 'served_at': '2026-11-22T10:00:00Z'}}
        lines = ai_answers.sync(client, directive(standing), ROOT)
        self.assertEqual(client.posted, [])
        self.assertEqual(lines, ['AI answers: cited first on 2 of 20 questions, 22 Nov.'])
        self.assertEqual(ai_answers.misses_and_moves(standing), ['What can I get my wife from the dog?', 'A new page'])

    def test_a_bank_with_more_valid_questions_than_the_request_on_file_asks_again_once(self):
        whole = len(ai_answers.questions(ROOT))
        self.assertGreater(whole, 20)
        for state in ('open', 'served'):
            client = FakeClient()
            lines = ai_answers.sync(client, directive(on_file(20, state)), ROOT)
            self.assertEqual(len(client.posted), 1, state)
            self.assertEqual(client.posted[0]['questions'], ai_answers.questions(ROOT))
            self.assertEqual(client.posted[0]['domains'], ['heartside.io'])
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines[1], f'Asked AEO-Engine again to track {whole} of Heartside\'s buyer questions, '
                                       'replacing the request on file for 20, from its next research run.')

    def test_a_request_on_file_with_no_readable_count_is_never_asked_again(self):
        for count in (None, '20', True, 2.5):
            client = FakeClient()
            lines = ai_answers.sync(client, directive(on_file(count)), ROOT)
            self.assertEqual(client.posted, [], repr(count))
            self.assertEqual(len(lines), 1, repr(count))

    def test_the_count_mirrors_the_protocols_filter_so_a_kept_request_is_not_asked_again_every_day(self):
        with bank_root(REFUSED + SYNTHETIC[:22] + [SYNTHETIC[0].upper(), SYNTHETIC[1].rstrip('?') + '.']) as root:
            qs = ai_answers.questions(root)
            # Only the 22 distinct valid questions: every refused one and every near repeat is left out.
            self.assertEqual(qs, SYNTHETIC[:22])
            self.assertFalse(any(ai_answers.valid(q) for q in REFUSED))
            client = FakeClient()
            self.assertEqual(len(ai_answers.sync(client, directive(on_file(22)), root)), 1)
            self.assertEqual(client.posted, [], 'what Control Center kept equals what the bank holds')
            lines = ai_answers.sync(client, directive(on_file(21)), root)
            self.assertEqual([len(b['questions']) for b in client.posted], [22])
            self.assertIn('replacing the request on file for 21', lines[1])

    def test_the_count_is_taken_after_the_cap_of_25(self):
        with bank_root(SYNTHETIC) as root:
            self.assertEqual(len(SYNTHETIC), 27)
            self.assertEqual(ai_answers.questions(root), SYNTHETIC[:25])
            client = FakeClient()
            ai_answers.sync(client, directive(on_file(25)), root)
            self.assertEqual(client.posted, [])
            ai_answers.sync(client, directive(on_file(24)), root)
            self.assertEqual([len(b['questions']) for b in client.posted], [25])

    def test_a_directive_that_serves_no_ai_answers_says_so_in_one_line_and_asks_nothing(self):
        for served in (directive(features=False), None, {}, {'ok': True, 'directive': {}}):
            client = FakeClient()
            self.assertEqual(ai_answers.sync(client, served, ROOT), ["AI answers: not served by today's directive."])
            self.assertEqual(client.posted, [])

    def test_a_served_directive_whose_standing_could_not_be_read_says_so_and_asks_nothing(self):
        # 1.22.0: `ai_answers` is absent when Control Center could not read the standing, while the feature stays on.
        # That is never "no request on file": a first request here would replace the open one on a guess.
        unread = [directive(),  # features.ai_answers true, no block
                  {'ok': True, 'directive': {'features': {'ai_answers': True}, 'ai_answers': None}},
                  {'ok': True, 'directive': {'features': {'ai_answers': True}, 'ai_answers': {'rule': 'synthetic rule'}}},
                  directive('not a standing'), directive(['a', 'list'])]
        for served in unread:
            client = FakeClient()
            self.assertEqual(ai_answers.sync(client, served, ROOT), [ai_answers.UNREAD], repr(served))
            self.assertEqual(client.posted, [], repr(served))
        self.assertFalse(ai_answers.readable(directive()))
        self.assertTrue(ai_answers.readable(directive(None)), 'a null standing is read: no request on file')
        self.assertTrue(ai_answers.readable(directive(on_file(3))))

    def test_a_failure_is_one_line_and_never_raises(self):
        lines = ai_answers.sync(FakeClient(fail=True), directive(None), ROOT)
        self.assertIn('Could not ask AEO-Engine', lines[-1])
        lines = ai_answers.sync(FakeClient(fail=True), directive(on_file(1)), ROOT)
        self.assertEqual(len(lines), 2)
        self.assertIn('Could not ask AEO-Engine', lines[-1])
        with bank_root([]) as root:
            self.assertEqual(ai_answers.sync(FakeClient(), directive(None), root)[-1],
                             'No buyer question is in the bank to ask AEO about yet.')
            self.assertEqual(ai_answers.sync(FakeClient(), directive(on_file(3)), root), ['AI answers: AEO tracks 3 questions from its next research run.'])


if __name__ == '__main__':
    unittest.main()
