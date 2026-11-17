"""The joke lab: write wide, reject retreads and dressed-up dogs before a frame is made, read the joke's structure,
catch the polish-the-pictures loop, and learn from Krish's verdicts. Built from the 17 Nov failure (factory/jokelab.py)."""
import json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'factory'))
import jokelab  # noqa: E402


SCENES = [
    ('The couch cushion', 'The left cushion is now three cushions.', 'He was asleep at the time, allegedly.'),
    ('The Thanksgiving roll', 'One dinner roll is unaccounted for.', 'He has asked for a lawyer and a second roll.'),
    ('The doorbell', 'Nobody rang the doorbell today.', 'He has warned the street eleven times anyway.'),
    ('The new bed', 'We bought him a ninety dollar bed.', 'He would like to be clear that the box is the bed.'),
    ('The vet visit', 'The car turned left instead of right.', 'He considers the marriage over.'),
    ('The bath', 'Bath time was announced at noon.', 'He has relocated under the deck for the foreseeable future.'),
]


def cand(i, family='alibi', title=None, words=None, dog_does='a real terrier sits beside a shredded toilet roll, tail low',
         closest='none', **kw):
    t, w1, w2 = SCENES[(i - 1) % len(SCENES)]
    c = {'id': f'c{i:02d}', 'family': family, 'title': title or t,
         'observation': 'dogs destroy things the moment nobody is watching',
         'stupid_premise': f'the dog treats {t.lower()} like a legal defence with paperwork',
         'cruel_payoff': 'the evidence is still hanging out of his mouth in the last shot',
         'dog_does': dog_does, 'words': words or [w1, w2],
         'last_line': w2, 'closest_live_post': closest, 'why_new': 'a new object'}
    c.update(kw)
    return c


def engine_result(reading='supported', mech=('incongruity', 'reversal'), last_seg='w2', target='behaviour', deps=0, main=True):
    return {
        'comic_reading': reading, 'status': 'complete', 'analysis_mode': 'live', 'analysis_id': 'an_x',
        'interpretations': [{'id': 'i1', 'is_main': main, 'supported_reading': 'comic' if reading == 'supported' else None,
                             'expectations': ['a statement implies innocence'], 'connecting_logic': 'the statement is contradicted on screen',
                             'labels_by_axis': {'mechanism': list(mech)}, 'target_and_subject': {'target': target},
                             'evidence_refs': ['ev1']}],
        'evidence': [{'evidence_id': 'ev1', 'segment_id': last_seg, 'start': 0, 'end': 3, 'exact_text': 'He '}],
        'context_dependencies': [{'source_kind': 'cultural', 'required': True}] * deps,
        'missing_context': [],
    }


class JokeLabTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.verdicts = os.path.join(self.tmp.name, 'verdicts.jsonl')
        jokelab.VERDICTS = self.verdicts
        jokelab.RUNS = os.path.join(self.tmp.name, 'runs')

    def tearDown(self):
        self.tmp.cleanup()

    def test_brief_carries_his_formula_families_live_posts_and_floor(self):
        b = jokelab.brief('Thanksgiving leftovers', n=30)
        self.assertIn('the parody is in the words, and the dog does real dog behavior on screen', b)
        self.assertIn('Write 30 different candidates', b)
        for fam in jokelab.FAMILIES:
            self.assertIn(f'- {fam} (weight', b)
        self.assertIn('Up at 4. Aligned with stakeholders by 5:32', b)   # the live post the 17 Nov retread copied
        self.assertIn('F34', b)
        self.assertIn('closest_live_post', b)

    def test_the_17_nov_retread_of_f38_is_rejected(self):
        retread = cand(1, family='format_parody', title='Rise and grind',
                       words=['4:00 a.m. Up before the sun.', '4:01. Circled back on the bin.', '4:05. Cold plunge. The pond was closed.'],
                       dog_does='a golden retriever stands in its water bowl at dawn')
        rec = jokelab.screen([retread] + [cand(i) for i in range(2, 4)])
        r = [x for x in rec['rejected'] if x['id'] == 'c01']
        self.assertTrue(r and any('format of live post F38' in why for why in r[0]['reasons']), rec['rejected'])

    def test_a_premise_retread_is_caught_even_with_new_words(self):
        # 17 Nov: completely different wording, same premise as F38 (timestamped routine labels).
        d1 = cand(1, family='format_parody', title='Rise and grind',
                  words=['4:00 a.m. Up before the sun.', '4:01. Circled back on the bin.', '4:06. Recovery. Your side. Still warm.'])
        named = cand(2, closest='F34')
        argued = cand(3, closest='F34', beats_live='the gift reveal lands as a crime confession, which F34 never had')
        rec = jokelab.screen([d1, named, argued])
        reasons = {x['id']: ' '.join(x['reasons']) for x in rec['rejected']}
        self.assertIn('format of live post F38', reasons.get('c01', ''))
        self.assertIn('writer named live post F34', reasons.get('c02', ''))
        self.assertNotIn('c03', reasons)

    def test_a_dressed_up_dog_is_rejected_outside_literal_staging(self):
        dressed = cand(1, dog_does='a golden retriever in a fleece vest types on a laptop')
        staged = cand(2, family='literal_staging', dog_does='a pug wearing a tiny party hat acts out each word of the birthday song')
        rec = jokelab.screen([dressed, staged])
        ids = {x['id'] for x in rec['rejected']}
        self.assertIn('c01', ids)
        self.assertNotIn('c02', ids)

    def test_copy_rules_and_missing_core_parts_are_rejected(self):
        loud = cand(1, words=['He did it!', 'He has filed a statement.'])
        no_core = cand(2, stupid_premise='')
        rec = jokelab.screen([loud, no_core, cand(3)])
        reasons = {x['id']: ' '.join(x['reasons']) for x in rec['rejected']}
        self.assertIn('exclamation', reasons['c01'])
        self.assertIn('missing stupid_premise', reasons['c02'])

    def test_near_duplicates_are_dropped_and_a_narrow_slate_is_called_out(self):
        a = cand(1); b = dict(cand(1), id='c02')
        rec = jokelab.screen([a, b])
        self.assertTrue(any('near duplicate' in ' '.join(x['reasons']) for x in rec['rejected']))
        self.assertTrue(any('families' in p for p in rec['slate_problems']))
        self.assertTrue(any('candidates' in p for p in rec['slate_problems']))

    def test_engine_reading_maps_to_the_three_part_core(self):
        ok, notes, labels = jokelab.triad(engine_result(), ['line', 'He has filed a statement.'])
        self.assertTrue(ok, notes)
        self.assertEqual(labels['mechanism'], ['incongruity', 'reversal'])
        flat, notes, _ = jokelab.triad(engine_result(reading='not_supported'), ['a', 'b'])
        self.assertFalse(flat)
        no_premise, notes, _ = jokelab.triad(engine_result(mech=('callback',), target='none'), ['a', 'b'])
        self.assertFalse(no_premise)
        self.assertTrue(any('stupid premise' in n for n in notes))
        early, notes, _ = jokelab.triad(engine_result(last_seg='w1'), ['a', 'b'])
        self.assertTrue(any('not in the last line' in n for n in notes))
        jumps, notes, _ = jokelab.triad(engine_result(deps=2), ['a', 'b'])
        self.assertFalse(jumps)

    def test_engine_rejections_leave_the_shortlist_and_the_reader_never_breaks_a_run(self):
        cands = [cand(i) for i in range(1, 5)]
        def reader(c):
            if c['id'] == 'c01':
                return engine_result(reading='ambiguous')
            if c['id'] == 'c02':
                raise TimeoutError('provider timeout')
            return engine_result()
        rec = jokelab.screen(cands, reader)
        short = {c['id'] for c in rec['shortlist']}
        self.assertNotIn('c01', short)
        self.assertIn('c03', short)
        self.assertTrue(any(r['id'] == 'c01' and 'engine' in ' '.join(r['reasons']) for r in rec['rejected']))

    def test_engine_request_carries_the_words_and_the_real_dog_on_screen(self):
        req = jokelab.engine_request(cand(1))
        self.assertEqual([s['segment_id'] for s in req['segments']], ['w1', 'w2'])
        self.assertIn('a real terrier', req['context']['provided_facts'][0])
        self.assertEqual(req['provider_policy']['allowed_provider_ids'], ['controlcenter'])
        try:
            from humour_engine.contracts.analysis import AnalysisRequest
        except ImportError:
            self.skipTest('humour-engine not installed')
        AnalysisRequest.model_validate(req)

    def test_live_path_runs_the_real_humour_engine_through_control_center(self):
        try:
            import humour_engine  # noqa: F401
        except ImportError:
            self.skipTest('humour-engine not installed (pip install -r requirements-humour.txt)')
        seen = {}

        def transport(url, body):
            seen['url'] = url
            seen['tool'] = body['tool']['name']
            payload = {
                'comic_reading': 'supported',
                'humour_attempt': {'status': 'supported_inference', 'evidence': [{'segment_id': 'w2', 'quote': 'asked for a lawyer'}]},
                'interpretations': [{
                    'id': 'i1', 'is_main': True, 'literal_reading': 'a roll is missing and the dog wants a lawyer',
                    'supported_reading': 'the dog behaves like a suspect who knows he is guilty',
                    'expectations': ['a missing roll implies someone ate it'],
                    'connecting_logic': 'his legal request confirms the crime he denies',
                    'labels_by_axis': {'mechanism': ['incongruity', 'reversal'], 'rhetorical_mode': ['parody']},
                    'target': {'target': 'behaviour'},
                    'evidence': [{'segment_id': 'w2', 'quote': 'asked for a lawyer'}],
                }],
                'missing_context': [],
            }
            return 200, {'ok': True, 'payload': payload, 'model': 'claude-sonnet-5', 'prompt': 'comprehension-v1:engine',
                         'usage': {'input_tokens': 900, 'output_tokens': 300}, 'cost_usd': 0.0048, 'cap': 200, 'used': 1}

        os.environ['CONTROL_CENTER_ENGINE_TOKEN'] = 'test-token-not-real'
        os.environ.pop('HUMOUR_ENGINE_CC_BEARER', None)
        try:
            reader = jokelab.engine_reader(transport=transport)
            self.assertIsNotNone(reader)
            res = reader(cand(2))
        finally:
            os.environ.pop('CONTROL_CENTER_ENGINE_TOKEN', None)
            os.environ.pop('HUMOUR_ENGINE_CC_BEARER', None)
        self.assertTrue(seen['url'].endswith('/api/growth/engines/heartside/humour'))
        self.assertEqual(seen['tool'], 'submit_analysis')
        self.assertEqual(res['status'], 'complete')
        self.assertEqual(res['analysis_mode'], 'live')
        self.assertEqual(res['evidence'][0]['exact_text'], 'asked for a lawyer')
        ok, notes, labels = jokelab.triad(res, cand(2)['words'])
        self.assertTrue(ok, notes)
        self.assertIn('reversal', labels['mechanism'])

    # On call: any line, any time, the same reader and the same core (AGENTS.md, "Ask the humour engine").
    def test_check_passes_flags_and_never_passes_silently(self):
        lines = ['One dinner roll is unaccounted for.', 'He has asked for a lawyer and a second roll.']
        seen = {}
        def reader(c):
            seen.update(c)
            return engine_result()
        o = jokelab.consult(lines, 'caption', 'a real beagle licks butter off his nose', ['posted the day before Thanksgiving'], reader)
        self.assertEqual(o['status'], 'pass', o)
        req = jokelab.engine_request(seen)
        facts = req['context']['provided_facts']
        self.assertIn('a real beagle', facts[0])
        self.assertIn('caption', facts[1])
        self.assertIn('Thanksgiving', facts[2])
        flat = jokelab.consult(lines, reader=lambda c: engine_result(reading='not_supported'))
        self.assertEqual(flat['status'], 'flagged')
        boom = jokelab.consult(lines, reader=lambda c: (_ for _ in ()).throw(TimeoutError('slow')))
        self.assertEqual(boom['status'], 'unavailable')
        abstain = jokelab.consult(lines, reader=lambda c: {'comic_reading': None, 'errors': [{'code': 'budget_exhausted'}]})
        self.assertEqual(abstain['status'], 'unavailable')
        self.assertIn('budget_exhausted', abstain['reason'])
        banned = jokelab.consult(['He is obsessed!'], reader=lambda c: engine_result(last_seg='w1'))
        self.assertEqual(banned['status'], 'flagged', banned)
        self.assertTrue(banned['copy'])

    def test_check_without_the_engine_says_unavailable_and_exits_2(self):
        for k in ('CONTROL_CENTER_ENGINE_TOKEN', 'HUMOUR_ENGINE_CC_BEARER'):
            os.environ.pop(k, None)
        self.assertEqual(jokelab.consult(['a line'])['status'], 'unavailable')
        self.assertEqual(jokelab.main(['check', 'One dinner roll is unaccounted for.']), 2)

    def test_compare_names_the_differences_and_leaves_taste_to_krish(self):
        a = jokelab.consult(['x', 'y'], reader=lambda c: engine_result())
        b = jokelab.consult(['x', 'z'], reader=lambda c: engine_result(mech=('incongruity', 'understatement')))
        d = jokelab.compare_consults(a, b)
        self.assertTrue(any('mechanism' in x and 'reversal' in x and 'understatement' in x for x in d), d)
        self.assertEqual(jokelab.compare_consults(a, a), [])

    def test_doctor_checks_the_route_without_a_model_call_or_the_token_on_screen(self):
        class Resp:
            def __init__(self, body): self.status, self._b = 200, json.dumps(body).encode()
            def read(self, n=-1): return self._b
            def __enter__(self): return self
            def __exit__(self, *a): return False
        calls = []
        def opener(features):
            def open_(req, timeout=None):
                calls.append((req.get_method(), req.full_url))
                return Resp({'ok': True, 'features': features})
            return open_
        for k in ('CONTROL_CENTER_ENGINE_TOKEN', 'HUMOUR_ENGINE_CC_BEARER', 'CONTROL_CENTER_URL'):
            os.environ.pop(k, None)
        ok, lines = jokelab.doctor(opener=opener({'humour': True}))
        self.assertFalse(ok)
        self.assertIn('NOT SET', lines[0])
        os.environ['CONTROL_CENTER_ENGINE_TOKEN'] = 'secret-token-value'
        try:
            ok, lines = jokelab.doctor(opener=opener({'humour': True}))
            off, off_lines = jokelab.doctor(opener=opener({}))
        finally:
            os.environ.pop('CONTROL_CENTER_ENGINE_TOKEN', None)
            os.environ.pop('HUMOUR_ENGINE_CC_BEARER', None)
        try:
            import humour_engine  # noqa: F401
            self.assertTrue(ok, lines)
        except ImportError:
            pass
        self.assertFalse(off)
        self.assertTrue(any('NOT SERVED' in x for x in off_lines))
        self.assertTrue(all(m == 'GET' and u.endswith('/api/growth/engines/heartside/capabilities') for m, u in calls), calls)
        self.assertNotIn('secret-token-value', '\n'.join(lines + off_lines))

    def test_polishing_pictures_is_caught(self):
        same = jokelab.words_hash(['4:00 a.m. Up before the sun.'])
        seven = [{'cut': n, 'score': s, 'words_sha': same} for n, s in enumerate([8, 7, 8, 9, 9], 1)]
        self.assertIn('same words', jokelab.cut_warning(seven))
        two = [{'cut': 1, 'score': 7, 'words_sha': same}, {'cut': 2, 'score': 9, 'words_sha': same}]
        self.assertIn('picture moved a model', jokelab.cut_warning(two))
        changed = [{'cut': 1, 'score': 7, 'words_sha': same}, {'cut': 2, 'score': 9, 'words_sha': 'other'}]
        self.assertIsNone(jokelab.cut_warning(changed))

    def test_verdicts_move_the_weights_and_one_no_is_never_a_rule(self):
        base = jokelab.family_weights([])
        one_no = [{'family': 'format_parody', 'verdict': 'no'}]
        self.assertLess(jokelab.family_weights(one_no)['format_parody'], base['format_parody'])
        self.assertEqual(jokelab.taste_fit(one_no), {})
        three_yes = [{'family': 'alibi', 'verdict': 'yes', 'labels': {'mechanism': ['reversal']}}] * 3
        fit = jokelab.taste_fit(three_yes)
        self.assertGreater(fit['alibi'], 0)
        self.assertGreater(fit['mechanism:reversal'], 0)

    def test_cli_round_trip_screen_cut_verdict(self):
        cands = [cand(i, family=f) for i, f in enumerate(['alibi', 'rule_lawyer', 'status_puncture', 'escalation_list'], 1)]
        path = os.path.join(self.tmp.name, 'c.json')
        json.dump(cands, open(path, 'w'))
        self.assertEqual(jokelab.main(['screen', path, '--run', 'r1']), 0)
        words = os.path.join(self.tmp.name, 'w.txt'); open(words, 'w').write('\n'.join(cands[0]['words']))
        first = jokelab.load_run('r1')['shortlist'][0]['id']
        for score in (7, 8, 9):
            code = jokelab.main(['cut', 'r1', first, '--score', str(score), '--words', words])
        self.assertEqual(code, 1)  # three cuts, same words: warned
        self.assertEqual(jokelab.main(['verdict', 'r1', first, 'no', 'not funny']), 0)
        self.assertEqual(jokelab.read_verdicts()[0]['words_said'], 'not funny')


if __name__ == '__main__':
    unittest.main()
