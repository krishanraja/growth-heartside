import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from engine import ledger


def report(start='2026-10-01', end='2026-11-01', values=None, stamp='2026-11-02T12:00:00+00:00'):
    return {'platform': 'shopify', 'scope': 'store', 'currency': 'USD', 'source': 'ShopifyQL sales',
            'period': {'start': start, 'end': end, 'timezone': 'Europe/London'},
            'observed_at': stamp, 'values': values if values is not None else {'orders': 10, 'net_sales': 480}}


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = ledger.connect(Path(self.temp.name) / 'ledger.sqlite3')

    def tearDown(self):
        self.db.close(); self.temp.cleanup()

    def test_idempotent_import_and_later_correction(self):
        r = report()
        self.assertTrue(ledger.import_report(self.db, r))
        self.assertFalse(ledger.import_report(self.db, r))
        r['observed_at'] = '2026-11-03T12:00:00+00:00'; r['values']['net_sales'] = 400
        ledger.import_report(self.db, r)
        result = ledger.summary(self.db, '2026-10-01', '2026-11-01', 'Europe/London')
        self.assertEqual(result['totals']['net_sales'], 400)
        self.assertEqual(result['totals']['orders'], 10)
        self.assertEqual(self.db.execute('SELECT count(*) FROM metrics').fetchone()[0], 1)
        utc = report(stamp='2026-11-04T12:00:00Z')
        self.assertEqual(ledger.normalize_report(utc)['observed_at'], '2026-11-04T12:00:00+00:00')

    def test_overlapping_aggregate_and_daily_windows_are_not_added(self):
        ledger.import_report(self.db, report())
        ledger.import_report(self.db, report('2026-10-02', '2026-10-03', {'orders': 3, 'net_sales': 144}))
        result = ledger.summary(self.db, '2026-10-01', '2026-11-01', 'Europe/London')
        self.assertEqual(result['totals']['orders'], 10)
        self.assertEqual(result['covered_days']['orders'], 31)

    def test_distinct_daily_windows_sum_but_other_zones_do_not(self):
        ledger.import_report(self.db, report('2026-10-01', '2026-10-02', {'orders': 1}))
        ledger.import_report(self.db, report('2026-10-02', '2026-10-03', {'orders': 2}))
        r = report('2026-10-03', '2026-10-04', {'orders': 100}); r['period']['timezone'] = 'America/New_York'
        ledger.import_report(self.db, r)
        result = ledger.summary(self.db, '2026-10-01', '2026-11-01', 'Europe/London')
        self.assertEqual(result['totals']['orders'], 3)
        self.assertEqual(result['covered_days']['orders'], 2)

    def test_missing_values_remain_missing_and_refunds_can_be_negative(self):
        r = report(values={'orders': None, 'net_sales': -24})
        ledger.import_report(self.db, r)
        result = ledger.summary(self.db, '2026-10-01', '2026-11-01', 'Europe/London')
        self.assertNotIn('orders', result['totals'])
        self.assertEqual(result['totals']['net_sales'], -24)

    def test_raw_customer_fields_and_invalid_numbers_are_rejected(self):
        for values in ({'email': 'private'}, {'orders': True}, {'orders': -1}, {'orders': 1.5}, {'net_sales': float('nan')}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                ledger.import_report(self.db, report(values=values))

    def test_tool_result_has_one_row_and_the_right_store(self):
        r = report(); del r['values']
        r['result'] = {'shopDomain': 'example-store.myshopify.com', 'columns': [{'name': 'orders'}], 'rows': [['3']]}
        with mock.patch.dict(os.environ, {'HEARTSIDE_SHOP_DOMAIN': 'example-store.myshopify.com'}):
            ledger.import_report(self.db, r)
            self.assertEqual(ledger.normalize_report(r)['values'], {'orders': 3})
            r['result']['shopDomain'] = 'another.myshopify.com'
            with self.assertRaises(ValueError):
                ledger.normalize_report(r)
        r['result']['shopDomain'] = 'example-store.myshopify.com'
        with mock.patch.dict(os.environ, {'HEARTSIDE_SHOP_DOMAIN': ''}), self.assertRaises(ValueError):
            ledger.normalize_report(r)
        r['result']['shopDomain'] = 'heartside.io'
        self.assertEqual(ledger.normalize_report(r)['values'], {'orders': 3})

    def test_the_store_handle_is_not_in_the_public_repository(self):
        import subprocess
        tracked = subprocess.run(['git', '-C', str(Path(__file__).resolve().parent.parent), 'grep', '-l', '-i', '-E',
                                  '[a-z0-9]{6}-[a-z0-9]{2}' + r'\.myshopify\.com'], capture_output=True, text=True)
        self.assertEqual(tracked.stdout.strip(), '', 'a Shopify store handle is in a tracked file')

    def test_older_or_conflicting_observations_cannot_replace_current(self):
        ledger.import_report(self.db, report())
        with self.assertRaises(ValueError):
            ledger.import_report(self.db, report(values={'orders': 99}))
        with self.assertRaises(ValueError):
            ledger.import_report(self.db, report(stamp='2026-11-01T00:00:00+00:00'))

    def test_render_history_is_idempotent_and_publication_requires_approval(self):
        cid, revision = 'IG_EMO_REEL_C90_H01_V1_20261017', 'a' * 64
        self.assertTrue(ledger.record_render(self.db, cid, revision, {'hook': 'a'}, {'files': []}))
        self.assertFalse(ledger.record_render(self.db, cid, revision, {'hook': 'a'}, {'files': []}))
        with self.assertRaises(ValueError):
            ledger.mark(self.db, cid, revision, 'published', 'https://www.instagram.com/reel/example/')
        ledger.mark(self.db, cid, revision, 'approved')
        with self.assertRaises(ValueError):
            ledger.mark(self.db, cid, revision, 'published', 'https://other.test/post')
        ledger.mark(self.db, cid, revision, 'published', 'https://www.instagram.com/reel/example/')
        ledger.record_render(self.db, cid, revision, {'hook': 'a'}, {'files': ['changed']})
        row = self.db.execute('SELECT status,published_url FROM creatives').fetchone()
        self.assertEqual(tuple(row), ('rendered', None))

    def test_backup_includes_committed_records(self):
        ledger.import_report(self.db, report())
        destination = Path(self.temp.name) / 'backup.sqlite3'
        ledger.backup(self.db, destination)
        restored = ledger.connect(destination)
        self.assertEqual(restored.execute('SELECT count(*) FROM metrics').fetchone()[0], 1)
        restored.close()


if __name__ == '__main__':
    unittest.main()
