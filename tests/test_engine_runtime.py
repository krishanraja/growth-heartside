import copy
from contextlib import closing
import datetime as dt
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from engine import insights, ledger, providers, runner, state_store

ROOT = Path(__file__).resolve().parents[1]


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.db = ledger.connect(self.root / 'local/engine.sqlite3')

    def tearDown(self):
        self.db.close(); self.temporary.cleanup()

    def request(self, brief='Fictional room only'):
        return {'provider': 'imagegen', 'capability': 'image', 'brief': brief, 'source_sha': 'a'*40,
                'maximum_usd': '0.40', 'quote_source': 'Connected provider quote', 'quote_observed_at': ledger.now()}

    def published(self, cid='IG_EMO_REEL_C90_H01_V1_20261010'):
        ledger.record_render(self.db, cid, 'a'*64, {}, {'files': {}})
        ledger.mark(self.db, cid, 'a'*64, 'approved')
        ledger.mark(self.db, cid, 'a'*64, 'published', 'https://www.instagram.com/reel/example/')
        return cid

    def observation(self, cid=None, sends=100, reach=4000):
        return {'creative_id': cid or self.published(), 'revision': 'a'*64, 'platform': 'instagram',
                'source': 'native', 'source_url': 'https://www.instagram.com/insights/',
                'observed_at': '2026-10-14T12:00:00Z', 'published_at': '2026-10-12T12:00:00Z',
                'attribution': 'none', 'values': {'reach': reach, 'sends': sends}}

    def test_budget_default_blocks_paid_and_idempotency_survives_a_new_quote(self):
        request = self.request()
        with self.assertRaises(ValueError):
            providers.reserve(self.db, request)
        first = providers.reserve(self.db, request, '0.50')
        request['quote_observed_at'] = dt.datetime.now(dt.timezone.utc).isoformat()
        again = providers.reserve(self.db, request, '0.50')
        self.assertEqual(first['request_id'], again['request_id'])
        with self.assertRaises(ValueError):
            providers.reserve(self.db, self.request('Another room'), '0.50')

    def test_uncertain_generation_cannot_auto_retry_and_honest_overrun_blocks_budget(self):
        row = providers.reserve(self.db, self.request(), '1')
        providers.transition(self.db, row['request_id'], 'submitted')
        providers.transition(self.db, row['request_id'], 'unknown')
        with self.assertRaises(ValueError):
            providers.transition(self.db, row['request_id'], 'submitted')
        providers.transition(self.db, row['request_id'], 'completed', {'job_id': 'confirmed-provider-id', 'actual_usd': '1.20', 'observed_at': ledger.now()})
        with self.assertRaises(ValueError):
            providers.reserve(self.db, self.request('new asset'), '1')

    def test_generated_media_cannot_replace_a_product_photo(self):
        row = providers.reserve(self.db, self.request(), '1')
        providers.transition(self.db, row['request_id'], 'submitted')
        providers.transition(self.db, row['request_id'], 'completed', {'job_id':'a', 'actual_usd':'0.2', 'observed_at':ledger.now()})
        file = self.root / 'image.png'; file.write_bytes(b'fictional test asset')
        provenance = {'description':'Fictional room', 'rights':'Generated for the brand', 'disclosure':'AI scene', 'transcript':''}
        with self.assertRaises(ValueError):
            providers.import_asset(self.root, self.db, row['request_id'], file, 'mug_dog', provenance)
        result = providers.import_asset(self.root, self.db, row['request_id'], file, 'fictional_scene', provenance)
        self.assertEqual(json.loads(result.read_text())['source_sha'], 'a'*40)

    def test_checkpoint_restores_wal_and_omits_lists_and_tokens(self):
        self.published()
        for path in ('local/lists/creators.md', 'local/secrets/token', 'local/automation/runs/test/pack.json', 'local/automation/runner.lock', 'local/automation/runs/test/review.zip'):
            file = self.root / path; file.parent.mkdir(parents=True, exist_ok=True); file.write_text('sample')
        result = state_store.export(self.root, 'local/backups/state.tgz')
        destination = self.root / 'another-machine'; destination.mkdir()
        state_store.restore(destination, self.root / result['path'])
        self.assertFalse((destination / 'local/lists').exists())
        self.assertFalse((destination / 'local/secrets').exists())
        self.assertFalse((destination / 'local/automation/runner.lock').exists())
        self.assertFalse((destination / 'local/automation/runs/test/review.zip').exists())
        with closing(ledger.connect(destination / 'local/engine.sqlite3')) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM creatives').fetchone()[0], 1)
        with self.assertRaises(ValueError):
            state_store.restore(destination, self.root / result['path'])

    def test_unsafe_checkpoint_does_not_touch_existing_state(self):
        path = self.root / 'unsafe.tgz'
        with tarfile.open(path, 'w:gz') as out:
            payload = b'{}'; member = tarfile.TarInfo('../escape'); member.size = len(payload); out.addfile(member, io.BytesIO(payload))
        marker = self.root / 'local/assets/keep'; marker.parent.mkdir(); marker.write_text('keep')
        with self.assertRaises(ValueError):
            state_store.restore(self.root, path, replace=True)
        self.assertEqual(marker.read_text(), 'keep')
        self.assertFalse((self.root.parent / 'escape').exists())

    def test_observations_replace_snapshots_and_never_allocate_native_revenue(self):
        document = self.observation()
        self.assertTrue(insights.import_observation(self.db, document))
        self.assertFalse(insights.import_observation(self.db, document))
        bad = copy.deepcopy(document); bad['values']['net_sales'] = 89
        with self.assertRaises(ValueError):
            insights.import_observation(self.db, bad)
        bad = copy.deepcopy(document); bad['values']['email'] = 'not allowed'
        with self.assertRaises(ValueError):
            insights.import_observation(self.db, bad)
        old = copy.deepcopy(document); old['observed_at'] = '2026-10-14T11:00:00Z'
        with self.assertRaises(ValueError):
            insights.import_observation(self.db, old)

    def test_no_decision_without_publication_and_no_winner_from_one_post(self):
        self.assertEqual(insights.decisions(self.db)['decisions'], [])
        document = self.observation()
        insights.import_observation(self.db, document)
        decisions = insights.decisions(self.db, dt.datetime(2026,10,15,tzinfo=dt.timezone.utc))
        self.assertEqual(decisions['decisions'][0]['decision'], 'hold')
        self.assertIsNone(decisions['decisions'][0]['attributed_net_sales'])

    def test_replication_requires_two_comparable_peers_and_stale_evidence_is_held(self):
        for index, sends in enumerate((100, 10, 12)):
            cid = self.published(f'IG_EMO_REEL_C9{index}_H01_V1_20261010')
            insights.import_observation(self.db, self.observation(cid, sends))
        result = insights.decisions(self.db, dt.datetime(2026,10,15,tzinfo=dt.timezone.utc))
        self.assertEqual(sum(d['decision'] == 'replicate_candidate' for d in result['decisions']), 1)
        stale = insights.decisions(self.db, dt.datetime(2026,10,25,tzinfo=dt.timezone.utc))
        self.assertTrue(all(d['decision'] == 'hold_missing' for d in stale['decisions']))

    def test_changed_product_input_refreshes_completed_work(self):
        from types import SimpleNamespace
        (self.root / 'automations.json').write_text((ROOT/'automations.json').read_text())
        state = {'sha': 'a'*40, 'rules_ok': True, 'store': []}
        growth = SimpleNamespace(sync=lambda quiet: state)
        time = dt.datetime(2026,10,17,13,0,tzinfo=dt.timezone.utc)
        with patch('engine.runner.run_job', return_value={'pack':'checked'}) as work:
            runner.tick(self.root, growth, time, 'daily-pack')
            runner.tick(self.root, growth, time + dt.timedelta(minutes=1), 'daily-pack')
            self.assertEqual(work.call_count, 1)
            state['sha'] = 'b'*40
            runner.tick(self.root, growth, time + dt.timedelta(minutes=2), 'daily-pack')
            self.assertEqual(work.call_count, 2)

    def test_hot_media_retention_preserves_ledger_metadata(self):
        from engine import retention
        path = self.root/'local/media/IG_EMO_REEL_C90_H01_V1_20260901/revision/reel.mp4'
        path.parent.mkdir(parents=True); path.write_bytes(b'old render')
        self.published()
        retention.prune(self.root, '2026-10-17')
        self.assertFalse(path.exists())
        self.assertEqual(self.db.execute('SELECT count(*) FROM creatives').fetchone()[0], 1)

    def test_scheduling_uses_new_york_dst_and_seven_declared_jobs(self):
        config = json.loads((ROOT/'automations.json').read_text())
        before = runner.due_jobs(config, dt.datetime(2026,10,17,12,59,tzinfo=dt.timezone.utc))
        after = runner.due_jobs(config, dt.datetime(2026,10,17,13,0,tzinfo=dt.timezone.utc))
        self.assertNotIn(('daily-pack','2026-10-17'), before)
        self.assertIn(('daily-pack','2026-10-17'), after)
        winter = runner.due_jobs(config, dt.datetime(2026,11,3,14,0,tzinfo=dt.timezone.utc))
        self.assertIn(('daily-pack','2026-11-03'), winter)
        self.assertIn(('creators','2026-11-03'), winter)
        self.assertEqual(len(config['automations']), 7)

    def test_run_failure_is_retryable_and_completed_jobs_do_not_repeat(self):
        (self.root / 'automations.json').write_text((ROOT/'automations.json').read_text())
        time = dt.datetime(2026,10,17,13,0,tzinfo=dt.timezone.utc)
        with patch('engine.runner.run_job', side_effect=RuntimeError('temporary outage')) as work:
            result = runner.tick(self.root, None, time, 'daily-pack')
            self.assertEqual(result['results'][0]['status'], 'failed')
            runner.tick(self.root, None, time + dt.timedelta(minutes=1), 'daily-pack')
            self.assertEqual(work.call_count, 1)
        with patch('engine.runner.run_job', return_value={'pack':'checked'}) as work:
            result = runner.tick(self.root, None, time + dt.timedelta(minutes=16), 'daily-pack')
            self.assertEqual(result['results'][0]['status'], 'completed')
            runner.tick(self.root, None, time + dt.timedelta(minutes=32), 'daily-pack')
            self.assertEqual(work.call_count, 1)


if __name__ == '__main__':
    unittest.main()
