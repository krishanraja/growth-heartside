"""AI answers through AEO-Engine, the one specialist (protocol 1.22.0; Ruling, Krish, 2026-11-12), and the detail
Control Center is asked to serve (1.26.0, features.ai_answers_detail; Ruling, Krish, 2026-11-13)."""
import datetime as dt
import hashlib
import http.client
import io
from contextlib import redirect_stdout
import json
import shutil
import socket
import tempfile
import unittest
import urllib.error
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from engine import ai_answers, runner, state_store
from engine.control_center import Client

ROOT = Path(__file__).resolve().parent.parent


class FakeClient:
    def __init__(self, fail=False, reports=(), reports_fail=False):
        self.posted = []
        self.fail = fail
        self.reports, self.reports_fail, self.reads = list(reports), reports_fail, 0

    def answers_request(self, body):
        if self.fail:
            raise RuntimeError('down')
        self.posted.append(body)
        return {'ok': True, 'request_id': '0b4f6a1e-7c2d-4e8a-9b1f-3d5c7e9a2b4c', 'questions': len(body['questions'])}

    def recent_reports(self, n=10):
        self.reads += 1
        if self.reports_fail:
            raise RuntimeError('down')
        return self.reports


def directive(standing='absent', features=True, detail=False):
    body = {'directive_id': 'heartside:2026-11-13', 'features': {'engine_state': True, 'krish_instruction': True, **({'ai_answers': True} if features else {}),
                                                                 **({'ai_answers_detail': True} if detail else {})}}
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



# ---------------------------------------------------------------------------
# 1.26.0: the request's digest, AEO's win kits and what has shipped.
# ---------------------------------------------------------------------------
# The fixed vector: computed in JavaScript as Control Center defines it (q.trim().replace(/\s+/g, ' '), sorted,
# JSON.stringify, SHA-256 hex), with a tab, double spaces, a no-break space, a byte order mark and non-ASCII.
VECTOR = ['  What can I get my partner\tfrom the dog? ', '\u00c7a va: a gift\u00a0from  the dog?',
          'How do you sign a gift from the dog?', 'Best dog mug for a dog\u2019s mom?\ufeff']
VECTOR_DIGEST = '5eba81926f9359eaa4b10ccbbeab1b42f2f6c6916684123946f867e1ea68c7d2'
PUBLISHED = [{'id': 'q90', 'priority': 1, 'tier': 1, 'question': 'What can I get my dog walker from the dog?', 'status': 'published',
              'url': 'https://heartside.io/blogs/answers/what-can-i-get-my-dog-walker-from-the-dog', 'published': '2026-10-21'},
             {'id': 'q91', 'priority': 2, 'tier': 1, 'question': 'What can I get my neighbor from the dog?', 'status': 'published',
              'url': 'https://heartside.io/blogs/answers/what-can-i-get-my-neighbor-from-the-dog', 'published': '2026-11-02'}]


def rows_root(rows):
    """A synthetic checkout whose question bank holds exactly these rows."""
    tmp = tempfile.TemporaryDirectory()
    path = Path(tmp.name) / ai_answers.BANK
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({'questions': rows}))
    return tmp


def synthetic_rows(n=22, published=()):
    return list(published) + [{'id': f'q{i + 10:02d}', 'priority': 5, 'tier': 1, 'question': q, 'status': 'todo'}
                              for i, q in enumerate(SYNTHETIC[:n])]


def filed(root, questions=None, count=None, state='served'):
    """A standing whose request on file carries the digest of `questions` (the bank's own list by default)."""
    s = on_file(len(questions or ai_answers.questions(root)) if count is None else count, state)
    s['request']['digest'] = ai_answers.digest(ai_answers.questions(root) if questions is None else questions)
    return s


def kit(question, priority, title=None, **extra):
    return {'kit_id': f'kit-{priority}', 'v': 1, 'query_id': f'qid-{priority}', 'question': question, 'gap_class': 'cited_not_first',
            'priority': priority, 'target': {'kind': 'new_page', 'url': None, 'host': 'heartside.io', 'suggested_path': None},
            'title': title or question, 'capsule': {'rules': ['Answer in the first sentence.'], 'must_cover': None},
            'h2s': ['What the dog would choose'], 'beat': [{'url': 'https://rival.example/gifts', 'host': 'rival.example', 'engine': 'perplexity', 'position': 1, 'features': []}],
            'site_fixes': [], 'off_site': [], 'verify': {}, 'evidence': [], **extra}


class DigestTest(unittest.TestCase):
    def test_the_digest_is_control_centers_definition_on_a_fixed_vector(self):
        self.assertEqual(ai_answers.digest(VECTOR), VECTOR_DIGEST)
        self.assertEqual(ai_answers.digest(list(reversed(VECTOR))), VECTOR_DIGEST, 'sorted, so order never matters')
        self.assertEqual(ai_answers.digest([]), hashlib.sha256(b'[]').hexdigest())
        # Non-ASCII stays unescaped, compact, UTF-8: exactly JSON.stringify's bytes.
        self.assertEqual(ai_answers.digest(['\u00c7a va, my dog?']), hashlib.sha256('["\u00c7a va, my dog?"]'.encode('utf-8')).hexdigest())
        self.assertEqual(ai_answers.digest(['b  question', ' a\u2003question ']), ai_answers.digest(['a question', 'b question']))
        # Never raises, even on a lone surrogate (JSON.stringify writes it as an escape).
        self.assertEqual(ai_answers.digest(['a\ud800b?']), hashlib.sha256(b'["a\\ud800b?"]').hexdigest())

    def test_a_matching_digest_never_asks_again_even_when_the_count_is_short(self):
        with rows_root(synthetic_rows()) as root:
            for detail in (False, True):
                client = FakeClient()
                lines = ai_answers.sync(client, directive(filed(root, count=3), detail=detail), root)
                self.assertEqual(client.posted, [], 'the count rule would ask; the digest says the request is the bank')
                self.assertEqual(len(lines), 2 if detail else 1)

    def test_a_different_digest_asks_again_replacing_the_request(self):
        with rows_root(synthetic_rows()) as root:
            asked = ai_answers.questions(root)
            # Same count, other questions: the count rule would never see it.
            client = FakeClient()
            lines = ai_answers.sync(client, directive(filed(root, questions=asked[:21] + ['What is a good gift from the cat?'], count=22), detail=True), root)
            self.assertEqual(len(client.posted), 1)
            self.assertEqual(client.posted[0]['questions'], asked)
            self.assertEqual(client.posted[0]['mode'], 'replace')
            self.assertNotIn('shipped', client.posted[0], 'nothing has shipped in this bank')
            mark = ai_answers.questions_mark(asked)
            self.assertEqual(lines[-1], 'Asked AEO-Engine again to track 22 of Heartside\'s buyer questions, replacing the request on file, '
                                        f'whose questions no longer match the bank, from its next research run ({mark}).')
            self.assertRegex(mark, r'^questions [0-9a-f]{12}$')
            # Without the detail flag the digest still decides, and the body is exactly 1.22.0's.
            client = FakeClient()
            ai_answers.sync(client, directive(filed(root, questions=asked[:5], count=22)), root)
            self.assertEqual(sorted(client.posted[0]), ['domains', 'note', 'questions'])

    def test_a_digest_that_never_meets_the_bank_is_asked_for_once_not_every_day(self):
        with rows_root(synthetic_rows()) as root:
            other = filed(root, questions=['What is a good gift from the cat?'], count=22)  # Control Center reads it otherwise
            first = FakeClient()
            lines = ai_answers.sync(first, directive(other, detail=True), root)
            self.assertEqual(len(first.posted), 1)
            # The next run finds its own ask for exactly this list in its last report, and asks nothing.
            again = FakeClient(reports=[{'activity': [{'line': l, 'evidence_url': None} for l in lines]}])
            self.assertEqual(ai_answers.sync(again, directive(other, detail=True), root)[-1], ai_answers.SETTLED)
            self.assertEqual((again.posted, again.reads), ([], 1), 'its reports are read once a run')
            # A bank that changes is asked for again; an unknown history asks again too (bounded: once a run).
            with rows_root(synthetic_rows(21)) as grown:
                changed = FakeClient(reports=again.reports)
                ai_answers.sync(changed, directive(other, detail=True), grown)
                self.assertEqual(len(changed.posted), 1)
            unknown = FakeClient(reports_fail=True)
            ai_answers.sync(unknown, directive(other, detail=True), root)
            self.assertEqual(len(unknown.posted), 1)

    def test_a_bank_that_changes_back_is_asked_for_again(self):
        """A, then B, then A again inside the report window: Control Center tracks B, so A is asked for again."""
        with rows_root(synthetic_rows()) as root:
            a = ai_answers.questions(root)
            b = a[:21] + ['What is a good gift from the cat?']
            tracks_b = directive(filed(root, questions=b, count=22), detail=True)
            line = 'Asked AEO-Engine again to track 22 of Heartside\'s buyer questions ({}).'
            newest_b = [{'activity': [{'line': line.format(ai_answers.questions_mark(b))}]},
                        {'activity': [{'line': line.format(ai_answers.questions_mark(a))}]}]
            client = FakeClient(reports=newest_b)
            lines = ai_answers.sync(client, tracks_b, root)
            self.assertEqual(len(client.posted), 1, 'the older ask for A is not the last one: B is')
            self.assertEqual((client.posted[0]['questions'], client.posted[0]['mode']), (a, 'replace'))
            self.assertIn(f'({ai_answers.questions_mark(a)})', lines[-1])
            # Once the newest ask is for A and the request still reads otherwise, it holds.
            client = FakeClient(reports=list(reversed(newest_b)))
            self.assertEqual(ai_answers.sync(client, tracks_b, root)[-1], ai_answers.SETTLED)
            self.assertEqual(client.posted, [])

    def test_a_malformed_digest_falls_back_to_the_count_rule(self):
        with rows_root(synthetic_rows()) as root:
            for bad in ('ABC', ai_answers.digest(['x']).upper(), 7, None, ['a']):
                s = on_file(22)
                s['request']['digest'] = bad
                client = FakeClient()
                ai_answers.sync(client, directive(s), root)
                self.assertEqual(client.posted, [], repr(bad))
                s['request']['questions'] = 21
                ai_answers.sync(client, directive(s), root)
                self.assertEqual(len(client.posted), 1, repr(bad))


class KitsTest(unittest.TestCase):
    def test_kits_are_read_loosely_best_priority_first_at_most_five(self):
        # AEO-Engine's priority is a score, higher is better (52-diagnose.ts kitPriority; 62-kits.ts sorts it highest first).
        raw = [None, 'a kit', {}, {'title': 5}, kit('Question three for the dog?', 3), kit('Question one for the dog?', 1),
               kit('Question without a rank for the dog?', None), kit('Question two for the dog?', 2), kit('Question one and a half?', 1.5),
               kit('Question four for the dog?', 4), kit('QUESTION FOUR FOR THE DOG', 0.5, title='A weaker repeat of question four'),
               kit('QUESTION ONE FOR THE DOG', 1.2, title='A stronger repeat of question one'),
               kit('Question nan for the dog?', float('nan')), kit('Question true for the dog?', True)]
        found = ai_answers.kits({'kits': raw})
        self.assertEqual([k['question'] for k in found],
                         ['Question four for the dog?', 'Question three for the dog?', 'Question two for the dog?',
                          'Question one and a half?', 'QUESTION ONE FOR THE DOG'])
        self.assertEqual([k['priority'] for k in found], [4, 3, 2, 1.5, 1.2], 'a repeated question keeps its highest priority')
        # AEO's real shape: no_page 1.1, cited_not_first 4.8, retrieved_not_cited 3.2. The best kit is never dropped.
        real = ai_answers.kits({'kits': [kit('What can I get my vet from the dog?', 1.1, gap_class='no_page'),
                                         kit('What can I get my groomer from the dog?', 4.8),
                                         kit('What can I get my sitter from the dog?', 3.2, gap_class='retrieved_not_cited')]})
        self.assertEqual([k['priority'] for k in real], [4.8, 3.2, 1.1])
        # A kit with no priority goes last, below even the weakest ranked one.
        unranked = ai_answers.kits({'kits': [kit('Question without a rank for the dog?', None), kit('Question ranked low for the dog?', 0.1)]})
        self.assertEqual([k['priority'] for k in unranked], [0.1, None])
        for nothing in (None, {}, {'kits': None}, {'kits': 'many'}, {'kits': [None, 3]}, 'standing', []):
            self.assertEqual(ai_answers.kits(nothing), [], repr(nothing))
        self.assertEqual(ai_answers.kits({'kits': found}), found, 'reading a cleaned kit again gives it back')

    def test_a_kit_is_cleaned_to_what_the_brief_uses(self):
        raw = kit('What can I get my vet from the dog?', 1, gap_class='a new class',
                  target={'kind': 'update_page', 'url': 'https://heartside.io/blogs/answers/vet?name=someone', 'host': 'HEARTSIDE.IO', 'suggested_path': '/../etc'},
                  beat=[{'url': 'https://www.Rival.example/a', 'host': None}, {'host': 'rival.example'}, {'host': 'not a host'}, 'x',
                        {'url': 'http://[bad'}, {'host': 'gifts.example'}, {'host': 'three.example'}, {'host': 'four.example'}],
                  site_fixes=[{'gate': 'faq_schema', 'host': 'heartside.io', 'url': 'https://heartside.io/x', 'fix': 'Add FAQPage markup.', 'owner_repo': 'krishanraja/heartside'},
                              {'gate': 'llms', 'fix': None}, 'x'])
        [k] = ai_answers.kits({'kits': [raw]})
        self.assertIsNone(k['gap_class'])
        self.assertEqual(k['target'], {'kind': 'update_page', 'url': None, 'host': 'heartside.io', 'suggested_path': None})
        self.assertEqual([b['host'] for b in k['beat']], ['rival.example', 'gifts.example', 'three.example'])
        self.assertEqual(k['site_fixes'], [{'gate': 'faq_schema', 'host': 'heartside.io', 'fix': 'Add FAQPage markup.', 'owner_repo': 'krishanraja/heartside'}])
        self.assertEqual(k['capsule'], {'rules': ['Answer in the first sentence.'], 'must_cover': []})

    def test_misses_and_moves_puts_kits_first(self):
        s = {**on_file(3), 'kits': [kit('What can I get my vet from the dog?', 2), kit('What can I get my groomer from the dog?', 1)],
             'misses': [{'question': 'What can I get my wife from the dog?', 'first': 'rival.example'}],
             'moves': [{'title': 'x', 'target_query': 'What can I get my vet from the dog?'}]}
        self.assertEqual(ai_answers.misses_and_moves(s), ['What can I get my vet from the dog?', 'What can I get my groomer from the dog?',
                                                          'What can I get my wife from the dog?'])

    def test_the_daily_run_keeps_kits_under_local_and_its_lines_carry_counts_only(self):
        with rows_root(synthetic_rows()) as root:
            s = {**filed(root), 'kits': [kit('What can I get my vet from the dog?', 2, title='Gifts for your vet, from the dog'),
                                         kit('What can I get my groomer from the dog?', 1)]}
            lines = ai_answers.sync(FakeClient(), directive(s, detail=True), root)
            self.assertEqual(lines[1], 'AEO-Engine has 2 win kits for Heartside; the Wednesday Answers brief takes the best two.')
            for word in ('vet', 'groomer', 'rival', 'Answer in the first'):
                self.assertFalse(any(word in l for l in lines), word)
            self.assertTrue(ai_answers.CACHE.startswith('local/control-center/'))
            self.assertNotIn('control-center', state_store.DIRECTORIES, 'kits never ride the checkpoint artifact')
            self.assertEqual([k['question'] for k in ai_answers.saved_kits(root)], ['What can I get my vet from the dog?', 'What can I get my groomer from the dog?'])
            # The next reading replaces them, none included.
            ai_answers.sync(FakeClient(), directive({**s, 'kits': []}, detail=True), root)
            self.assertEqual(ai_answers.saved_kits(root), [])
            # Without the detail nothing is kept or said about kits.
            shutil.rmtree(Path(root) / 'local')
            self.assertEqual(len(ai_answers.sync(FakeClient(), directive(s), root)), 1)
            self.assertFalse((Path(root) / ai_answers.CACHE).exists())

    def test_saved_kits_expire_and_never_fail(self):
        with rows_root([]) as root:
            now = dt.datetime(2026, 11, 18, 12, tzinfo=dt.timezone.utc)
            self.assertEqual(ai_answers.saved_kits(root, now), [])
            self.assertTrue(ai_answers.save(root, ai_answers.kits({'kits': [kit('What can I get my vet from the dog?', 1)]}), now - dt.timedelta(days=8)))
            self.assertEqual(len(ai_answers.saved_kits(root, now)), 1)
            self.assertEqual(ai_answers.saved_kits(root, now + dt.timedelta(days=1)), [], 'over 8 days old')
            self.assertEqual(ai_answers.saved_kits(root, now - dt.timedelta(days=9)), [], 'saved in the future')
            # A clock with no offset (`growth.py run --job answers --now 2026-11-18T12:00`) is read as UTC, never a TypeError.
            self.assertEqual(len(ai_answers.saved_kits(root, now.replace(tzinfo=None))), 1)
            self.assertEqual(ai_answers.saved_kits(root, (now + dt.timedelta(days=1)).replace(tzinfo=None)), [])
            (Path(root) / ai_answers.CACHE).write_text('{not json')
            self.assertEqual(ai_answers.saved_kits(root, now), [])

    def test_fetch_reads_get_answers_keeps_kits_and_says_counts(self):
        with rows_root([]) as root:
            standing = {**on_file(3), 'kits': [kit('What can I get my vet from the dog?', 1)]}
            line = ai_answers.fetch(SimpleNamespace(answers_standing=lambda: standing), root)
            self.assertEqual(line, 'AEO-Engine has 1 win kit for Heartside; the Wednesday Answers brief takes the best two.')
            self.assertEqual(len(ai_answers.saved_kits(root)), 1)
            self.assertIn('could be read', ai_answers.fetch(SimpleNamespace(answers_standing=lambda: None), root))
            self.assertIn('does not serve', ai_answers.fetch(SimpleNamespace(answers_standing=lambda: on_file(3)), root))
            self.assertEqual(len(ai_answers.saved_kits(root)), 1, 'an unserved read keeps what was kept')


class ShippedTest(unittest.TestCase):
    def test_shipped_reads_published_rows_with_their_url_and_date_only(self):
        rows = PUBLISHED + [
            {'id': 'q92', 'question': 'What can I get my mail carrier from the dog?', 'status': 'published', 'published': '2026-10-21'},
            {'id': 'q93', 'question': 'What can I get my sitter from the dog?', 'status': 'published', 'url': 'https://heartside.io/blogs/answers/sitter'},
            {'id': 'q94', 'question': 'What can I get my trainer from the dog?', 'status': 'published', 'url': 'https://rival.example/trainer', 'published': '2026-10-21'},
            {'id': 'q95', 'question': 'What can I get my nanny from the dog?', 'status': 'todo', 'url': 'https://heartside.io/blogs/answers/nanny', 'published': '2026-10-21'},
            {'id': 'q96', 'question': 'What can I get my aunt from the dog?', 'status': 'published', 'url': 'https://heartside.io/blogs/answers/aunt', 'published': '2026-13-40'},
            {'id': 'q97', 'question': 'What can I get my uncle from the dog?', 'status': 'published', 'url': 'https://heartside.io/blogs/answers/uncle', 'published': 'soon'}]
        with rows_root(rows) as root:
            self.assertEqual(ai_answers.shipped(root), [{'question': r['question'], 'url': r['url'], 'shipped_at': r['published']} for r in PUBLISHED])
        real = ai_answers.shipped(ROOT)
        self.assertTrue(real and all(e['url'].startswith('https://heartside.io/') and e['shipped_at'] for e in real))

    def test_the_first_request_carries_shipped_only_where_the_detail_is_served(self):
        with rows_root(synthetic_rows(published=PUBLISHED)) as root:
            client = FakeClient()
            lines = ai_answers.sync(client, directive(None, detail=True), root)
            self.assertEqual(client.posted[0]['mode'], 'replace')
            self.assertEqual(client.posted[0]['shipped'], ai_answers.shipped(root))
            mark = ai_answers.shipped_mark(ai_answers.shipped(root))
            self.assertEqual(lines[-1], f'Asked AEO-Engine to track 24 of Heartside\'s buyer questions from its next research run '
                                        f'({ai_answers.questions_mark(ai_answers.questions(root))}), with 2 shipped answers ({mark}).')
            client = FakeClient()
            ai_answers.sync(client, directive(None), root)
            self.assertEqual(sorted(client.posted[0]), ['domains', 'note', 'questions'])

    def test_shipped_answers_are_told_once_per_change(self):
        with rows_root(synthetic_rows(published=PUBLISHED)) as root:
            done = ai_answers.shipped(root)
            mark = ai_answers.shipped_mark(done)
            client = FakeClient()
            lines = ai_answers.sync(client, directive(filed(root), detail=True), root)
            self.assertEqual(client.posted, [{'questions': [e['question'] for e in done], 'domains': ['heartside.io'], 'note': ai_answers.NOTE,
                                              'mode': 'append', 'shipped': done}])
            self.assertEqual(lines[-1], f'Told AEO-Engine that 2 of Heartside\'s answers have shipped ({mark}).')
            # The next run reads its own report back and tells nothing twice.
            told = FakeClient(reports=[{'run_id': 'r', 'status': 'ok', 'activity': [{'line': lines[-1], 'evidence_url': None}]}])
            self.assertEqual(len(ai_answers.sync(told, directive(filed(root), detail=True), root)), 2)
            self.assertEqual(told.posted, [])
            # Unknown is not told; a changed list is told again; without the detail nothing is told.
            for client in (FakeClient(reports_fail=True), FakeClient(reports=['x', {'activity': 'y'}])):
                ai_answers.sync(client, directive(filed(root), detail=True), root)
                self.assertEqual(len(client.posted), 1)
            stale = FakeClient(reports=[{'activity': [f'Told AEO-Engine that 1 of Heartside\'s answers has shipped ({ai_answers.shipped_mark(done[:1])}).']}])
            ai_answers.sync(stale, directive(filed(root), detail=True), root)
            self.assertEqual(len(stale.posted), 1)
            plain = FakeClient()
            ai_answers.sync(plain, directive(filed(root)), root)
            self.assertEqual((plain.posted, plain.reads), ([], 0))
            failed = ai_answers.sync(FakeClient(fail=True), directive(filed(root), detail=True), root)
            self.assertIn('Could not tell AEO-Engine which of Heartside\'s answers have shipped', failed[-1])
            for line in lines + failed:
                self.assertNotIn('walker', line)


class ReportTest(unittest.TestCase):
    def test_the_detail_lines_go_into_a_schema_valid_report_that_the_next_run_reads_back(self):
        from engine import ledger, protocol
        from tests.test_protocol import NOW, SCHEMA, STATE, recommendations, validate
        with rows_root(synthetic_rows(published=PUBLISHED)) as root:
            s = {**filed(root), 'kits': [kit('What can I get my vet from the dog?', 1)]}
            served = directive(s, detail=True)
            lines = ai_answers.sync(FakeClient(), served, root)
            db = ledger.connect(Path(root) / 'local/engine.sqlite3')
            try:
                report = protocol.build_report(root=Path(root), state=dict(STATE), db=db, now=NOW, run_id='heartside:2026-11-18:synthetic-directive',
                                               mode='synthetic', directive=served, recommendations=recommendations(), answers=lines)
            finally:
                db.close()
            self.assertEqual(validate(SCHEMA, report), [])
            self.assertTrue(set(lines) <= {a['line'] for a in report['activity']})
            again = FakeClient(reports=[{'run_id': report['run_id'], 'status': report['status'], 'activity': report['activity']}])
            ai_answers.sync(again, served, root)
            self.assertEqual(again.posted, [], 'told once; the next run reads its own report back')


class Reply:
    def __init__(self, status, body):
        self.status, self.body = status, body

    def read(self, n=-1):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def opener(outcome, seen):
    def call(request, timeout):
        seen.append((request.get_method(), request.full_url, request.get_header('Authorization'), timeout))
        if isinstance(outcome, BaseException):
            raise outcome
        status, body = outcome
        raw = body if isinstance(body, bytes) else json.dumps(body).encode()
        if status >= 300:
            raise urllib.error.HTTPError(request.full_url, status, 'no', {}, io.BytesIO(raw))
        return Reply(status, raw)
    return call


class AnswersStandingTest(unittest.TestCase):
    def test_get_answers_returns_the_standing_or_none_and_never_raises(self):
        standing = {**on_file(3), 'kits': [kit('What can I get my vet from the dog?', 1)]}
        cases = [((200, {'ok': True, 'schema_version': '1.23.0', 'read_at': 'x', 'ai_answers': standing, 'rule': 'r'}), standing),
                 ((200, {'ok': True, 'ai_answers': {'standing': standing, 'rule': 'r'}}), standing),
                 ((200, {'ok': True, 'ai_answers': None}), None), ((200, {'ok': False, 'ai_answers': standing}), None),
                 ((200, b'not json'), None), ((200, b'[1]'), None), ((404, {'error': 'not_found'}), None),
                 ((500, {'error': 'store_failed'}), None), ((302, {}), None), ((401, {}), None),
                 (socket.timeout(), None), (urllib.error.URLError('down'), None), (OSError('reset'), None),
                 (http.client.IncompleteRead(b''), None), (http.client.LineTooLong('header line'), None)]
        for outcome, expected in cases:
            seen = []
            client = Client('https://cc.example', 'synthetic-token', opener=opener(outcome, seen))
            self.assertEqual(client.answers_standing(), expected, repr(outcome))
            self.assertEqual(seen, [('GET', 'https://cc.example/api/growth/engines/heartside/answers', 'Bearer synthetic-token', 20)])
            self.assertNotIn('synthetic-token', repr(client))
        # A reply cut while its body is read: no kits, never a traceback (`growth.py cc kits` prints its one line).
        cut = Reply(200, b'')
        cut.read = lambda n=-1: (_ for _ in ()).throw(http.client.IncompleteRead(b'{"ok":'))
        client = Client('https://cc.example', 'synthetic-token', opener=lambda request, timeout: cut)
        self.assertIsNone(client.answers_standing())
        with rows_root([]) as root:
            self.assertIn('could be read', ai_answers.fetch(client, root))


class AnswersBriefTest(unittest.TestCase):
    """The Wednesday Answers job with a synthetic standing that carries kits (engine/runner.py, answers_brief)."""
    DAY = '2026-11-18'

    def setUp(self):
        import growth
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / 'knowledge').mkdir()
        shutil.copyfile(ROOT / ai_answers.BANK, self.root / ai_answers.BANK)
        self.state = {'sha': 'a' * 40, 'rules_ok': True, 'price_points': [], 'synced_at': '2026-11-18T12:00:00+00:00'}
        self.growth = SimpleNamespace(sync=lambda quiet=False: dict(self.state), check_pack=growth.check_pack, tracked=growth.tracked,
                                      render_md=growth.render_md, freshness=lambda *a: [], head_sha=None, raw=None, docs_listing=None)
        self.check = growth.check_pack
        self.demand = patch('engine.runner.demand', return_value='Public search suggestions unavailable. No current search demand is inferred.')
        self.demand.start()

    def tearDown(self):
        self.demand.stop()
        self.temporary.cleanup()

    def keep(self, kits):
        ai_answers.save(self.root, ai_answers.kits({'kits': kits}))

    def test_without_kits_the_brief_is_the_banks_next_two_questions_as_before(self):
        pack, result = runner.answers_brief(self.root, self.growth, self.state, self.DAY)
        self.assertEqual([i['target_name'] for i in pack['items']], ['Answers library: q03', 'Answers library: q04'])
        self.assertEqual(result, {'questions': ['q03', 'q04'], 'kits': 0, 'kits_dropped': 0, 'kit_lines_dropped': 0, 'kits_off_site': 0, 'published': 0, 'kits_hold': None})
        self.assertEqual(pack['headline'], 'Answers library: the next two questions to draft')
        self.assertEqual(self.check(pack, [], state=self.state), [])

    def test_kits_come_first_by_priority_and_text_the_linter_refuses_is_dropped_with_a_count(self):
        mom = 'What is a good gift from the dog to mom?'  # q05 in the bank
        self.keep([
            kit(mom, 5, title='A gift from the dog to mom',
                h2s=['What mom keeps from the dog', 'Unleash the perfect gift'],
                capsule={'rules': ['Answer in the first sentence.', 'Name one gift \u2014 the mug.'], 'must_cover': ['the note in the dog\'s voice']},
                target={'kind': 'update_page', 'url': 'https://heartside.io/blogs/answers/gift-from-the-dog-to-mom', 'host': 'heartside.io', 'suggested_path': None},
                beat=[{'host': 'rival.example'}, {'url': 'https://www.gifts.example/mom'}],
                site_fixes=[{'gate': 'faq_schema', 'host': 'heartside.io', 'fix': 'Add FAQPage markup to the answer.', 'owner_repo': 'krishanraja/heartside'},
                            {'gate': 'robots', 'host': 'heartside.io', 'fix': 'Open the answers to GPTBot.', 'owner_repo': 'krishanraja/control-center'},
                            {'gate': 'links', 'host': 'heartside.io', 'fix': 'Link it from https://heartside.io/pages/gifts in the footer.', 'owner_repo': None}]),
            kit('What can I get my vet from the dog?', 7, title='Gifts for your vet, from the dog!',
                target={'kind': 'new_page', 'url': None, 'host': 'heartside.io', 'suggested_path': '/blogs/answers/gifts-for-your-vet'}),
            kit('Is a dog mug a must-have gift from the dog?', 8, title='The must-have gift from the dog'),
            kit('What can I get my mail carrier from the dog?', 9, target={'kind': 'off_site_only', 'url': None, 'host': 'reddit.com', 'suggested_path': None}),
            kit('What can I get my groomer from the dog?', 1)])
        pack, result = runner.answers_brief(self.root, self.growth, self.state, self.DAY)
        self.assertEqual(self.check(pack, [], state=self.state), [], 'the brief passes the pack\'s own check')
        self.assertEqual(pack['headline'], 'Answers library: the next two questions to draft, AEO-Engine\'s win kits first')
        vet, mom_item = pack['items']
        # The highest priority first (AEO-Engine's own order), after the off-site and dropped kits ranked above it. Its title fails the linter (an exclamation mark), so its question is the title; nothing is rewritten.
        self.assertEqual(vet['text'].splitlines()[0], 'Title: What can I get my vet from the dog?')
        self.assertEqual(vet['creative_id'], 'WEB_UTIL_ARTICLE_C29_H01_V1_20261118', 'a question the bank lacks takes the next number')
        self.assertEqual(vet['target_url'], 'https://heartside.io/blogs/answers/gifts-for-your-vet')
        self.assertEqual(mom_item['creative_id'], 'WEB_UTIL_ARTICLE_C05_H01_V1_20261118')
        self.assertEqual(mom_item['target_url'], 'https://heartside.io/blogs/answers/gift-from-the-dog-to-mom')
        self.assertEqual(mom_item['target_name'], 'Answers library: q05, from AEO-Engine\'s win kit')
        text = mom_item['text']
        self.assertIn('Title: A gift from the dog to mom', text)
        self.assertIn('Headline: What mom keeps from the dog', text)
        self.assertNotIn('Unleash', text)
        self.assertIn('Capsule rule: Answer in the first sentence.', text)
        self.assertNotIn('\u2014', text)
        self.assertIn('Capsule must cover: the note in the dog\'s voice', text)
        self.assertIn('Pages to beat (hosts only): rival.example, gifts.example.', text)
        self.assertIn('Site fix for a heartside build session: faq_schema on heartside.io: Add FAQPage markup to the answer.', text)
        self.assertNotIn('GPTBot', text, 'a fix another repository owns is not briefed here')
        self.assertNotIn('pages/gifts', text, 'an untracked store link is dropped, never rewritten')
        self.assertIn('utm_content=WEB_UTIL_ARTICLE_C05_H01_V1_20261118', text)
        # Two kits briefed; the must-have kit dropped (its title and question both fail); the off-site kit passed over;
        # three lines dropped from the mom kit (the H2, the em dash rule and the link fix), plus the dropped kit's title.
        self.assertEqual(result, {'questions': ['q05'], 'kits': 2, 'kits_dropped': 1, 'kit_lines_dropped': 4, 'kits_off_site': 1, 'published': 0, 'kits_hold': None})
        public = json.dumps(result)
        for word in ('vet', 'mom', 'groomer', 'rival', 'must'):
            self.assertNotIn(word, public)

    def test_a_new_page_is_always_in_the_answers_blog_whatever_path_aeo_suggests(self):
        # AEO-Engine's own shape: suggestedPath is always /answers/<slug> (62-kits.ts), which the Shopify store cannot serve.
        self.keep([kit('What can I get my neighbor from the dog?', 4.8,
                       target={'kind': 'new_page', 'url': None, 'host': 'heartside.io', 'suggested_path': '/answers/what-get-neighbor-dog'}),
                   kit('What can I get my vet from the dog?', 3.2,
                       target={'kind': 'new_page', 'url': None, 'host': 'heartside.io', 'suggested_path': '/blogs/answers/'})])
        pack, _ = runner.answers_brief(self.root, self.growth, self.state, self.DAY)
        self.assertEqual([i['target_url'] for i in pack['items']],
                         ['https://heartside.io/blogs/answers/what-can-i-get-my-neighbor-from-the-dog',
                          'https://heartside.io/blogs/answers/what-can-i-get-my-vet-from-the-dog'])
        self.assertEqual(self.check(pack, [], state=self.state), [])

    def test_one_kit_and_then_the_bank_and_a_kit_never_repeats_a_bank_question(self):
        self.keep([kit('What can I get my husband from the dog?', 1)])  # q03, the bank's own next question
        pack, result = runner.answers_brief(self.root, self.growth, self.state, self.DAY)
        self.assertEqual([i['target_name'] for i in pack['items']], ['Answers library: q03, from AEO-Engine\'s win kit', 'Answers library: q04'])
        self.assertEqual(result['questions'], ['q03', 'q04'])
        self.assertEqual(self.check(pack, [], state=self.state), [])

    def test_the_scheduled_job_writes_a_checked_brief_under_local(self):
        self.keep([kit('What can I get my vet from the dog?', 2), kit('What can I get my groomer from the dog?', 1)])
        result = runner.run_job(self.root, self.growth, 'answers', self.DAY)
        self.assertEqual((result['kits'], result['questions']), (2, []))
        written = json.loads((self.root / result['pack']).read_text())
        self.assertTrue(result['pack'].startswith('local/'))
        self.assertEqual(self.check(written, [], state=self.state), [])
        self.assertEqual([i['creative_id'] for i in written['items']], ['WEB_UTIL_ARTICLE_C29_H01_V1_20261118', 'WEB_UTIL_ARTICLE_C30_H01_V1_20261118'])
        self.assertTrue((self.root / 'local/packs/2026-11-18-answers.md').exists())

    def test_a_job_without_the_token_holds_visibly_and_a_read_clears_it(self):
        from engine import protocol
        with redirect_stdout(io.StringIO()):
            self.assertEqual(protocol.main(self.root, self.growth, 'kits', 'live', env={}), 1)
        pack, result = runner.answers_brief(self.root, self.growth, self.state, self.DAY)
        self.assertIn('held: the Control Center engine token is not given to this job', pack['headline'])
        self.assertIn('token', result['kits_hold'])
        self.assertEqual(self.check(pack, [], state=self.state), [])
        ai_answers.clear_kits_hold(self.root)
        pack, result = runner.answers_brief(self.root, self.growth, self.state, self.DAY)
        self.assertNotIn('held', pack['headline']); self.assertIsNone(result['kits_hold'])


if __name__ == '__main__':
    unittest.main()
