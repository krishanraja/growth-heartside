"""Post-family code drafts (R-3) and the do-not-quote statistics check (AGENTS.md rule 8)."""
import json
import os
import subprocess
import sys
import unittest

import growth
from engine import attribution, codes

HERE = os.path.dirname(__file__)
MANIFEST = os.path.join(HERE, '..', 'factory', 'sprints', '2026-11-S120.json')


def manifest():
    return json.load(open(MANIFEST, encoding='utf-8'))


class CodeDraftTests(unittest.TestCase):
    def test_only_buy_and_signature_slots_get_a_code(self):
        m = manifest(); drafts = codes.draft(m)
        selling = {s['id'] for s in m['slots'] if s.get('intent') == 'buy' or s['lane'] == 'signature'}
        self.assertEqual({d['slot'] for d in drafts}, selling)
        self.assertFalse(any(s['lane'] == 'viral' and s.get('intent') != 'buy' for s in m['slots'] if s['id'] in {d['slot'] for d in drafts}))

    def test_codes_are_tracking_words_with_no_discount(self):
        for d in codes.draft(manifest()):
            self.assertIsNone(d['discount'])
            self.assertRegex(d['code'], r'^[A-Z]{3,8}\d{2,3}[TIF]$')
            self.assertTrue(attribution.FAMILY.match(d['family']))
            self.assertTrue(d['creative_id'].startswith(d['family'].rsplit('_', 1)[0]))

    def test_the_drafts_register_cleanly_and_classify_as_their_family(self):
        drafts = codes.draft(manifest()); registry = codes.registry(drafts)
        self.assertEqual(len(registry), len(drafts))
        d = drafts[0]
        order = {'discountCodes': [d['code'].lower()], 'customerJourneySummary': {'ready': True, 'lastVisit': None, 'firstVisit': None}}
        self.assertEqual(attribution.classify(order, {k.upper(): v for k, v in registry.items()}), ('engine', d['family']))

    def test_a_clash_is_refused(self):
        m = manifest(); s = next(x for x in m['slots'] if x['lane'] == 'signature')
        twin = dict(s); m['slots'].append(twin)
        with self.assertRaises(ValueError):
            codes.draft(m)

    def test_the_command_prints_and_writes_nothing(self):
        before = open(os.path.join(HERE, '..', 'config', 'codes.json'), encoding='utf-8').read()
        out = subprocess.run([sys.executable, os.path.join(HERE, '..', 'growth.py'), 'codes'], capture_output=True, text=True, check=True).stdout
        self.assertIn('no discount', out)
        self.assertIn('PRESS301I', out)
        self.assertEqual(open(os.path.join(HERE, '..', 'config', 'codes.json'), encoding='utf-8').read(), before)


class DoNotQuoteTests(unittest.TestCase):
    def refused(self, text, platform='instagram'):
        return [p for p in growth.problems({'platform': platform, 'text': text}) if 'rule 8' in p]

    def test_unsourced_statistics_are_refused_on_every_line(self):
        for text in ('People have an 8-second attention span now.',
                     'Average human attention span on new info: 8 seconds.',
                     'Infographics are shared 30x more than text.',
                     'Referred customers have 16-25% higher LTV.',
                     'Visuals are processed 60,000 times faster than text.',
                     'Email subscribers are 70x more likely to buy.'):
            self.assertTrue(self.refused(text), text)
        self.assertTrue(self.refused('Note for Krish: remember the 8-second attention span.', platform='other'))

    def test_dog_jokes_and_real_counts_pass(self):
        for text in ('He has the attention span of a goldfish and the patience of a saint.',
                     'Shared 3 times more than last week on our own account.',
                     'Caption: my attention span is 8 seconds and you are the whole 8.',
                     'Caption: an 8-second attention span, all of it on you.',
                     'Referral customers have higher LTV.'):
            self.assertEqual(self.refused(text), [], text)

    def test_the_human_claims_are_still_refused(self):
        for text in ('Consumers now have an attention span of 8 seconds.',
                     'Our attention span is shorter than a goldfish.',
                     'LTV is 25% higher for referred customers.'):
            self.assertTrue(self.refused(text), text)


class CodeLineTests(unittest.TestCase):
    def code_problems(self, text, intent):
        return [p for p in growth.problems({'platform': 'instagram', 'intent': intent, 'text': text}) if 'discount-code' in p]

    def test_a_code_line_is_refused_off_a_buy_item(self):
        for text in ('Caption: the dog wrote you a note. Use code PRESS301I.',
                     'Caption: the dog wrote you a note. PRESS301I',
                     'Caption: enter the promo code at checkout.'):
            self.assertTrue(self.code_problems(text, 'audience'), text)
            self.assertTrue(self.code_problems(text, None), text)

    def test_a_registered_code_is_refused_off_a_buy_item(self):
        from unittest import mock
        with mock.patch.object(attribution, 'load_codes', return_value={'HEARTS': 'IG_EMO_C301'}):
            self.assertTrue(self.code_problems('Caption: hearts99 at checkout.', 'audience'))
            self.assertEqual(self.code_problems('Caption: all the hearts are yours.', 'audience'), [])

    def test_a_buy_item_may_carry_its_code(self):
        self.assertEqual(self.code_problems('Caption: the mug, from the dog. Use code PRESS301I.', 'buy'), [])

    def test_words_are_whole_and_never_weak(self):
        for title, want in (('Christmas list from the dog', 'LIST'), ('Who is the one dog draft', 'HEART'),
                            ('Interview with the dog', 'HEART'), ('Press release', 'PRESS')):
            self.assertEqual(codes.word({'title': title}, banned=set()), want, title)
        self.assertEqual(codes.word({'title': 'Press release'}, banned={'press'}), 'RELEASE')


if __name__ == '__main__':
    unittest.main()
