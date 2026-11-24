"""The revenue desk adapter (config/revenue-desk.json, engine/revenue_desk.py). Synthetic edits of the real adapter
only: no figure or customer record is in this file."""
import copy
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import revenue_desk  # noqa: E402


def adapter():
    with open(os.path.join(ROOT, 'config', 'revenue-desk.json'), encoding='utf-8') as f:
        return json.load(f)


class RevenueDeskAdapter(unittest.TestCase):
    def test_real_adapter_passes(self):
        self.assertEqual(revenue_desk.adapter_problems(ROOT), [])

    def check(self, change):
        doc = copy.deepcopy(adapter())
        change(doc)
        return revenue_desk.adapter_problems(ROOT, doc)

    def test_missing_function_is_named(self):
        def change(doc):
            doc['steps'][4]['read'][0]['function'] = 'no_such_reader'
        self.assertTrue(any('no function no_such_reader' in p for p in self.check(change)))

    def test_steps_in_order(self):
        self.assertTrue(self.check(lambda d: d['steps'].reverse()))

    def test_band_figure_or_binding_refused(self):
        self.assertTrue(self.check(lambda d: d['bands'].update(warning=0.5)))
        self.assertTrue(self.check(lambda d: d['bands'].update(binding=True)))

    def test_each_alarm_has_one_action(self):
        self.assertTrue(self.check(lambda d: d['alarms']['breach'].pop('action')))

    def test_spend_and_store_job_walls(self):
        self.assertTrue(self.check(lambda d: d.update(spend_authority='boosts')))
        self.assertTrue(self.check(lambda d: d['store_job'].update(schedule='on')))
        self.assertTrue(self.check(lambda d: d['paid_boosts'].update(change='raise cap')))

    def test_offer_terms_bound_to_real_functions(self):
        self.assertTrue(self.check(lambda d: d['offer_terms']['functions'].append('invented_rule')))

    def test_unknown_command_refused(self):
        self.assertTrue(self.check(lambda d: d['steps'][0]['commands'].append('python3 growth.py nonsense')))

    def test_no_money_figure(self):
        self.assertTrue(self.check(lambda d: d.update(note='target $50 a day')))


if __name__ == '__main__':
    unittest.main()
