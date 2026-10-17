from contextlib import redirect_stdout
import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import growth
from engine import dashboard, ledger


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = ledger.connect(self.root / 'local/engine.sqlite3')
        self.state = {'sha': 'a' * 40, 'rules_ok': True, 'synced_at': '2026-10-17T08:00:00Z'}

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def test_missing_reports_stay_missing_and_prepared_recommendations_keep_their_close(self):
        recommendation = {'title': 'Review the change', 'why': 'One blocker', 'next_action': 'Review the PR',
                          'closes_when': 'The report can be read back', 'target_url': 'https://github.com/owner/repo/pull/1'}
        numbers, report = dashboard.build(self.db, self.state, '2026-10-01', '2026-10-17', 'Europe/London', '2026-10-17', 'b' * 40, [recommendation])
        self.assertEqual(numbers['venture'], 'heartside')
        self.assertTrue(all(row.get(m) is None for row in numbers['numbers'] for m in dashboard.MEASURES))
        self.assertTrue(all('Coverage 0 of 16 days' in row['note'] for row in numbers['numbers']))
        self.assertIn('Complete when: The report can be read back', report['items'][-1]['text'])
        self.assertFalse(growth.check_pack(numbers))
        self.assertFalse(growth.check_pack(report))

    def test_zero_sales_and_partial_coverage_are_preserved_with_source_and_time(self):
        ledger.import_report(self.db, {'platform': 'shopify', 'scope': 'store', 'currency': 'USD',
            'period': {'start': '2026-10-01', 'end': '2026-10-03', 'timezone': 'Europe/London'},
            'source': 'Connected ShopifyQL', 'observed_at': '2026-10-17T08:00:00Z', 'values': {'net_sales': 0, 'orders': 1}})
        numbers, _ = dashboard.build(self.db, self.state, '2026-10-01', '2026-10-17', 'Europe/London', '2026-10-17', 'b' * 40, [])
        sales = numbers['numbers'][0]
        self.assertEqual(sales['net_sales'], 0)
        self.assertIn('Coverage 2 of 16 days', sales['note'])
        self.assertIn('Connected ShopifyQL', sales['note'])
        self.assertIn('observed 2026-10-17T08:00:00+00:00', sales['note'])
        self.assertNotIn('conversion_rate', sales)

    def test_failed_delivery_retains_retry_copy_and_history(self):
        pack = {'pack_date': '2026-10-17', 'kind': 'report', 'heartside_sha': 'a' * 40, 'headline': 'Progress', 'items': []}
        with patch.object(growth, 'LOCAL', str(self.root / 'local')), patch.object(growth, 'token', return_value='test-only'), \
                patch.object(growth, 'control_center_takes_heartside', return_value=(True, 'ready')), \
                patch.object(growth.urllib.request, 'urlopen', side_effect=urllib.error.URLError('offline')), redirect_stdout(io.StringIO()):
            growth.store_pack(pack)
            growth.store_pack({**pack, 'headline': 'New progress'})
        saved = json.loads((self.root / 'local/packs/2026-10-17-report.json').read_text())
        self.assertEqual(saved['headline'], 'New progress')
        self.assertEqual(len(list((self.root / 'local/packs/history').glob('*.json'))), 1)

    def test_remote_read_is_scoped_and_merges_dashboard_status_without_losing_media(self):
        day = dt.date.today().isoformat()
        local = {'pack_date': day, 'kind': 'daily', 'venture': 'heartside', 'production': {'manifest': 'local/media/manifest.json'}, 'items': []}
        folder = self.root / 'local/packs'; folder.mkdir(parents=True)
        (folder / f'{day}-daily.json').write_text(json.dumps(local))
        remote = {**local, 'source_revision': 'a' * 40, 'items': [{'platform': 'instagram', 'text': 'Draft', 'status': 'posted'}]}
        del remote['production']
        response = io.BytesIO(json.dumps({'ok': True, 'packs': [remote, {**remote, 'venture': 'makeyourmindup'}]}).encode())
        with patch.object(growth, 'LOCAL', str(self.root / 'local')), patch.object(growth, 'token', return_value='test-only'), \
                patch.object(growth, 'control_center_takes_heartside', return_value=(True, 'ready')), \
                patch.object(growth.urllib.request, 'urlopen', return_value=response) as request:
            packs = growth.read_packs(7, 'daily')
        self.assertEqual(len(packs), 1)
        self.assertEqual(packs[0]['items'][0]['status'], 'posted')
        self.assertEqual(packs[0]['production'], local['production'])
        self.assertIn('venture=heartside', request.call_args.args[0].full_url)


if __name__ == '__main__':
    unittest.main()
