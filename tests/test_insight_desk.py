"""The insight desk adapter (config/insight-desk.json, factory/insight_sheet.py, factory/insight_bench.py and
jokelab.py brief --insight). Synthetic sheets only: no customer, post or verdict of Krish's is in this file.

The joke lab's brief without --insight is byte for byte what it was; with it, the sheet's insight and lead idea come
first and the plain brief follows unchanged.
"""
import contextlib
import copy
import inspect
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'factory'))
import insight_bench  # noqa: E402
import insight_sheet  # noqa: E402
import jokelab  # noqa: E402

METHODS = {'ritual-hijack', 'rename-the-problem', 'give-them-a-role', 'instrument-first'}


def test_result(result='pass', reason='synthetic reason'):
    return {'result': result, 'reason': reason}


def idea(idea_id, method='ritual-hijack', level='campaign', analogue='pass'):
    return {
        'id': idea_id,
        'claim': f'Synthetic claim for {idea_id}: the dog owns up on the painted mug note.',
        'mechanic': 'The dog confesses the habit in its own voice.',
        'idea_level': level,
        'method': method,
        'channel_role': 'short video with the evidence in the first second',
        'conversion_path': {'offer': 'the painted mug', 'link': 'tracked link from growth.py link',
                            'why_act': 'the viewer sees their own dog in the confession'},
        'kill_condition': 'Fewer saves than the plain post over two weeks.',
        'tests': {
            'specificity': test_result(),
            'share': test_result(),
            'analogue': {**test_result(analogue), 'url': 'https://example.com/analogue' if analogue == 'pass' else None,
                         'read_at': '2026-11-24' if analogue == 'pass' else None},
            'floor': test_result(),
            'kill_the_favourite': test_result(),
        },
    }


def sheet(**change):
    s = {
        'schema': 'insight-sheet/1',
        'venture': 'heartside',
        'repo': 'krishanraja/growth-heartside',
        'harness_skill_sha': 'a' * 40,
        'made_at': '2026-11-24T09:00:00Z',
        'north_star': {'metric': 'synthetic organic sales', 'urgency': 5, 'current': 0, 'as_of': '2026-11-24'},
        'stall_check': {'diagnosis': 'idea', 'evidence': 'synthetic: views with no clicks'},
        'insights': [{'audience': 'people whose dog steals the couch', 'wants': 'to laugh about it',
                      'but': 'nobody else finds it funny', 'because': 'only they see it every night',
                      'source': 'synthetic comment themes', 'read_at': '2026-11-24'}],
        'chosen_insight': 0,
        'discarded_obvious': ['A countdown post', 'A discount code', 'A gallery of gifts'],
        'ideas': [idea('confession'), idea('name-the-habit', method='rename-the-problem', analogue='unavailable')],
        'consults': [{'engine': 'divergent-thinker', 'op': 'score', 'result': 'unavailable', 'ref': 'synthetic'}],
        'lead': 'confession',
        'blind_passes': [{'reader': 'reader one', 'order': ['confession', 'name-the-habit'], 'lead': 'confession'},
                         {'reader': 'reader two', 'order': ['name-the-habit', 'confession'], 'lead': 'confession'}],
    }
    s.update(change)
    s['sheet_sha256'] = insight_sheet.sheet_sha(s)
    return s


def run_main(fn, argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = fn(argv)
    return code, out.getvalue()


class SheetTest(unittest.TestCase):
    def test_a_good_sheet_is_valid(self):
        self.assertEqual(insight_sheet.validate(sheet(), METHODS), [])
        self.assertEqual(insight_sheet.for_this_engine(sheet(), insight_sheet.load_adapter()), [])

    def test_the_rules_a_schema_cannot_hold(self):
        def errs(s):
            s = copy.deepcopy(s)
            s['sheet_sha256'] = insight_sheet.sheet_sha(s)
            return ' | '.join(insight_sheet.validate(s, METHODS))
        self.assertIn('not the idea', errs(sheet(stall_check={'diagnosis': 'distribution', 'evidence': 'x'})))
        self.assertIn('measurement idea', errs(sheet(north_star={'metric': 'm', 'urgency': 4, 'current': None, 'as_of': None})))
        s = sheet(); s['lead'] = 'name-the-habit'
        for p in s['blind_passes']:
            p['lead'] = 'name-the-habit'
        self.assertIn('analogue is unavailable', errs(s))
        s = sheet(); s['blind_passes'][1]['lead'] = 'name-the-habit'
        self.assertIn('both blind passes', errs(s))
        s = sheet(); s['blind_passes'][1]['order'] = list(s['blind_passes'][0]['order'])
        self.assertIn('shuffled', errs(s))
        s = sheet(); s['ideas'][0]['tests']['share']['score'] = 8
        self.assertIn('no scores', errs(s))
        s = sheet(); s['ideas'][0]['conversion_path']['link'] = ''
        self.assertIn('no full conversion path', errs(s))
        s = sheet(); s['ideas'][0]['method'] = 'made-up-method'
        self.assertIn('not in the skill', errs(s))
        self.assertNotIn('not in the skill', ' '.join(insight_sheet.validate(sheet(ideas=[idea('x', method='made-up-method')],
                                                                                    lead='x', blind_passes=[
            {'reader': 'r1', 'order': ['x'], 'lead': 'x'}, {'reader': 'r2', 'order': ['x'], 'lead': 'x'}]), None)))
        s = sheet(); s['insights'][0]['because'] = 'Love ' + chr(0x2014) + ' Kuku'
        self.assertIn('em dash', errs(s))

    def test_a_changed_sheet_fails_its_sha(self):
        s = sheet(); s['ideas'][0]['claim'] = 'changed after hashing'
        self.assertTrue(any('does not match' in e for e in insight_sheet.validate(s, METHODS)))

    def test_another_venture_is_refused_here(self):
        s = sheet(venture='mindmake', repo='krishanraja/growth-mindmake')
        self.assertEqual(len(insight_sheet.for_this_engine(s, insight_sheet.load_adapter())), 2)


class BriefTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        jokelab.VERDICTS = os.path.join(self.tmp.name, 'verdicts.jsonl')

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, s):
        path = os.path.join(self.tmp.name, 'sheet.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(s, f)
        return path

    def test_brief_without_the_flag_is_byte_identical(self):
        # brief() itself is untouched (no new parameter), and the command prints exactly what it returns.
        self.assertEqual(list(inspect.signature(jokelab.brief).parameters), ['topic', 'n', 'slot'])
        for argv, args in ((['brief', 'Thanksgiving leftovers'], ('Thanksgiving leftovers', 30, None)),
                           (['brief', 'bath day', '--n', '12', '--slot', 'S1'], ('bath day', 12, 'S1'))):
            code, out = run_main(jokelab.main, argv)
            self.assertEqual(code, 0)
            self.assertEqual(out.encode('utf-8'), (jokelab.brief(*args) + '\n').encode('utf-8'))
            self.assertNotIn('Insight desk sheet', out)

    def test_the_flag_only_prepends_the_insight_and_lead(self):
        s = sheet()
        code, out = run_main(jokelab.main, ['brief', 'bath day', '--n', '12', '--insight', self.write(s)])
        self.assertEqual(code, 0)
        plain = jokelab.brief('bath day', 12, None) + '\n'
        self.assertTrue(out.endswith(plain))
        head = out[:-len(plain)]
        self.assertEqual(head, insight_sheet.preamble(s) + '\n\n')
        self.assertIn('The insight, for people whose dog steals the couch: they want to laugh about it', head)
        self.assertNotIn('couch wants', head)
        self.assertIn('The lead idea (confession', head)
        self.assertNotIn('name-the-habit', head)

    def test_an_unchecked_method_list_is_said_on_the_brief_path(self):
        s = sheet()
        saved = insight_sheet.methods_file
        try:
            insight_sheet.methods_file = lambda explicit=None: None
            notes = []
            _, errors = insight_sheet.usable(self.write(s), notes=notes)
            self.assertEqual(errors, [])
            self.assertEqual(notes, [insight_sheet.METHODS_NOT_CHECKED])
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code, out = run_main(jokelab.main, ['brief', 'bath day', '--insight', self.write(s)])
            self.assertEqual(code, 0)
            self.assertIn('method names were not checked', err.getvalue())
            self.assertNotIn('method names were not checked', out)
        finally:
            insight_sheet.methods_file = saved

    def test_a_bad_sheet_never_feeds_a_brief(self):
        s = sheet(); s['ideas'][0]['claim'] = 'tampered'
        with self.assertRaises(SystemExit) as stop:
            run_main(jokelab.main, ['brief', 'bath day', '--insight', self.write(s)])
        self.assertIn('cannot feed a brief', str(stop.exception))
        no_lead = sheet(lead=None)
        with self.assertRaises(SystemExit) as stop:
            run_main(jokelab.main, ['brief', 'bath day', '--insight', self.write(no_lead)])
        self.assertIn('no lead', str(stop.exception))


class AdapterAndBenchTest(unittest.TestCase):
    def test_the_adapter_names_only_real_commands(self):
        self.assertEqual(insight_sheet.adapter_problems(ROOT), [])
        broken = insight_sheet.load_adapter()
        broken['commands'] = broken['commands'] + ['python3 factory/jokelab.py brief --no-such-flag',
                                                   'python3 growth.py no-such-command']
        problems = insight_sheet.adapter_problems(ROOT, broken)
        self.assertEqual(len(problems), 2)

    def test_the_two_offline_checks(self):
        adapter = insight_sheet.load_adapter()
        self.assertTrue(insight_sheet.insight_format('dog people want a laugh but nobody gets it because only they see it')[0])
        self.assertFalse(insight_sheet.insight_format('He has an alibi.')[0])
        self.assertFalse(insight_sheet.specificity('Heartside: he has an alibi.', adapter)[0])
        self.assertTrue(insight_sheet.specificity('the painted portrait owns up for him', adapter)[0])
        self.assertFalse(insight_sheet.specificity('he looked smug', adapter)[0])

    def test_the_bench_is_calibrated_on_the_real_floor_and_live_posts(self):
        report = insight_bench.run()
        self.assertGreater(report['floor_items'], 0)
        self.assertGreater(report['live_items'], 0)
        self.assertEqual(report['gaps'], [])
        self.assertEqual(report['floor_pass_specificity'], [])
        self.assertFalse(report['generic_control']['specificity'])
        self.assertFalse(report['product_control']['format'])
        self.assertTrue(report['calibrated'])


if __name__ == '__main__':
    unittest.main()
