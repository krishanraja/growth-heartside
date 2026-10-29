"""Prepaid credits, protocol 1.16.0: read the share, refuse past it, report a spend once."""
import copy
import datetime as dt
import tempfile
import unittest
from pathlib import Path

from engine import credits, ledger, protocol
from engine.control_center import Client, report_digest
from tests.test_protocol import DIRECTIVE, NOW, SCHEMA, STATE, TOKEN, StandIn, recommendations, validate

POOLS = {'rule': 'Spend your share before it is wiped.', 'pools': [
    {'pool': 'runway', 'tool': 'Runway', 'unit': 'credits', 'share': 'main', 'share_amount': 1800, 'spent_this_cycle': 0,
     'remaining_for_you': 1800, 'pool_balance': None, 'balance_as_of': None, 'use_by': '2026-11-06', 'resets_on': '2026-11-07',
     'days_left': 9, 'unit_costs': []},
    {'pool': 'higgsfield', 'tool': 'Higgsfield', 'unit': 'credits', 'share': 'main', 'share_amount': 2400, 'spent_this_cycle': 2390,
     'remaining_for_you': 10, 'pool_balance': 2722.5, 'balance_as_of': '2026-10-29T10:00:00Z', 'use_by': '2026-11-23',
     'resets_on': '2026-11-24', 'days_left': 26, 'unit_costs': [{'output': 'GPT Image still', 'credits': 2.75}]}]}


def with_credits():
    d = copy.deepcopy(DIRECTIVE)
    d['directive']['credits'] = copy.deepcopy(POOLS)
    return d


def request(credits_needed):
    return {'provider': 'higgsfield', 'capability': 'image', 'brief': 'Three stills for an approved concept.',
            'source_sha': 'a' * 40, 'maximum_usd': '0', 'quote_source': 'Higgsfield quote',
            'quote_observed_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'prepaid_credits': str(credits_needed)}


class CreditsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.db = ledger.connect(self.root / 'local/engine.sqlite3')

    def tearDown(self):
        self.db.close()
        self.temporary.cleanup()

    def build(self, directive, spent=()):
        return protocol.build_report(root=self.root, state=copy.deepcopy(STATE), db=self.db, now=NOW,
                                     run_id='heartside:2026-10-19:synthetic-directive', mode='synthetic',
                                     directive=directive, recommendations=recommendations(), credits_spent=spent)

    def test_no_credits_block_is_unknown_spends_nothing_and_keeps_the_version(self):
        self.assertIsNone(credits.read(DIRECTIVE))
        report = self.build(DIRECTIVE)
        self.assertEqual(report['schema_version'], '1.0.0')
        self.assertNotIn('credits_spent', report)
        self.assertTrue(any('share is unknown' in a['line'] for a in report['activity']))
        with self.assertRaisesRegex(ValueError, 'unknown'):
            credits.reserve(self.db, request(1), credits.read(DIRECTIVE), 'higgsfield', 'run')

    def test_each_pool_gets_a_line_with_what_is_left_and_the_last_day(self):
        report = self.build(with_credits())
        lines = [a['line'] for a in report['activity']]
        self.assertTrue(any(l.startswith('Runway: 1800 credits left for Heartside, use by 2026-11-06') for l in lines))
        self.assertEqual(report['schema_version'], '1.0.0', 'reading the block raises nothing: only a spend does')
        self.assertEqual(validate(SCHEMA, report), [])

    def test_a_reservation_past_the_share_is_refused_before_anything_runs(self):
        pools = credits.read(with_credits())
        row = credits.reserve(self.db, request(2.75), pools, 'higgsfield', 'heartside:2026-10-29:directive')
        self.assertEqual(row['status'], 'reserved')
        with self.assertRaisesRegex(ValueError, 'exceeded'):
            credits.reserve(self.db, dict(request(8), brief='Three more stills.'), pools, 'higgsfield', 'heartside:2026-10-29:directive')
        with self.assertRaisesRegex(ValueError, 'no prepaid pool'):
            credits.reserve(self.db, request(1), pools, 'elevenlabs', 'heartside:2026-10-29:directive')

    def test_a_spend_is_reported_at_1_16_0_and_the_stand_in_takes_it(self):
        spent = [{'pool': 'higgsfield', 'amount': 2.75, 'asset': 'One still for concept golden-hour mug', 'objective_key': 'net_sales'}]
        report = self.build(with_credits(), spent)
        self.assertEqual(report['schema_version'], '1.16.0')
        self.assertEqual(report['credits_spent'], spent)
        self.assertEqual(validate(SCHEMA, report), [])
        self.assertEqual(report['payload_sha256'], report_digest(report))
        stand = StandIn()
        try:
            protocol.deliver(Client(stand.base, TOKEN), report)
            self.assertIn(report['run_id'], stand.reports)
        finally:
            stand.close()

    def test_a_bad_spend_never_reaches_a_report(self):
        for bad in ({'pool': 'Higgsfield', 'amount': 1, 'asset': 'x'}, {'pool': 'higgsfield', 'amount': 0, 'asset': 'x'},
                    {'pool': 'higgsfield', 'amount': 1, 'asset': 'sent to a@b.co'}, {'pool': 'higgsfield', 'amount': 1, 'asset': 'x', 'objective_key': 'Net Sales'}):
            with self.assertRaises(ValueError):
                credits.spent([bad])
        with self.assertRaises(ValueError):
            credits.spent([{'pool': 'higgsfield', 'amount': 1, 'asset': 'x'}] * 41)


if __name__ == '__main__':
    unittest.main()
