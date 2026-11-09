"""Social continuity: a fresh session restores the engagement and follower history from the repository alone.

The cases follow the verification list in the engagement desk's handover (Krish, 2026-11-09).
"""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

from engine import drive_audit, floor, ledger, operations, social

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / 'docs/social/2026-11-09-engagement-history.json'
NOW = dt.datetime(2026, 11, 9, 12, 0, tzinfo=dt.timezone.utc)


class SocialRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.db = ledger.connect(self.root / 'local/engine.sqlite3')
        self.events = json.loads(HISTORY.read_text())
        self.results = operations.apply(self.root, self.db, self.events)
        self.report = social.status(self.db, NOW)
        self.tests = {t['test_id']: t for t in self.report['tests']}

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_both_tests_restored_approved_and_handed_off_not_live(self):
        self.assertEqual(set(self.tests), {'fb-first-follower-rival', 'tt-first-follower-security'})
        for t in self.tests.values():
            stages = [h['stage'] for h in t['history']]
            self.assertEqual(stages, ['proposed', 'approved', 'handed_off'])
            self.assertEqual(t['stage'], 'handed_off')
            self.assertNotIn('live_at', t)
            self.assertNotIn('window_ends', t)

    def test_exact_text_and_target_survive_byte_for_byte(self):
        fb = self.tests['fb-first-follower-rival']
        self.assertEqual(fb['target_url'], 'https://www.facebook.com/reel/1436549414677089')
        self.assertTrue(fb['text'].endswith('Tell us their name and their sworn enemy. \U0001F602'))
        self.assertIn('’', fb['text'])
        self.assertEqual(fb['text_sha256'], social.text_sha(fb['text']))
        self.assertIn('Approve both the Facebook and TikTok engagement tests', fb['approval']['words'])

    def test_next_action_is_check_before_sending_and_owned_by_publishing(self):
        for t in self.tests.values():
            self.assertEqual(t['owner'], 'publishing')
            self.assertIn('check the native post', t['next_action'])
            self.assertIn('Never send it twice', t['next_action'])
            self.assertIn('treat approval or handoff as publication', t['do_not'])

    def test_window_starts_only_at_verified_publication(self):
        operations.apply(self.root, self.db, [{'event_id': 'social:fb-live', 'type': 'social', 'record': {
            'kind': 'engagement', 'test_id': 'fb-first-follower-rival', 'stage': 'live_verified', 'channel': 'facebook',
            'at': '2026-11-09T10:00:00Z', 'source': 'publishing desk receipt', 'evidence': 'native permalink read back'}}])
        fb = {t['test_id']: t for t in social.status(self.db, NOW)['tests']}['fb-first-follower-rival']
        self.assertEqual(fb['window_ends'], '2026-11-11T10:00:00+00:00')
        self.assertEqual(fb['owner'], 'engagement')
        later = {t['test_id']: t for t in social.status(self.db, NOW + dt.timedelta(days=3))['tests']}['fb-first-follower-rival']
        self.assertIn('Window closed', later['next_action'])

    def test_only_instagram_and_pinterest_remain_and_failed_checks_are_unknown(self):
        self.assertEqual(self.report['monitor_remaining'], ['instagram', 'pinterest'])
        for c in ('instagram', 'pinterest'):
            ch = self.report['channels'][c]
            self.assertEqual(ch['last_successful'], {'at': '2026-11-08T17:37:00Z', 'count': 0, 'source': ch['last_successful']['source']})
            self.assertEqual(ch['last_attempt']['status'], 'unavailable')
            self.assertTrue(ch['current'].startswith('unknown'))
            self.assertEqual(ch['consecutive_failures'], 2)
        self.assertEqual(self.report['channels']['facebook']['monitor'], 'delivered')
        self.assertEqual(self.report['channels']['tiktok']['last_successful']['count'], 1)

    def test_rules_keep_aggregates_apart_from_followers(self):
        self.assertIn('Aggregate views, likes or comments never establish what a follower did.', self.report['rules'])

    def test_replay_does_not_duplicate_and_changed_evidence_is_refused(self):
        again = operations.apply(self.root, self.db, self.events)
        self.assertTrue(all(r['status'] == 'already_applied' for r in again))
        count = self.db.execute('SELECT COUNT(*) FROM social_events').fetchone()[0]
        self.assertEqual(count, len(self.events))
        tampered = json.loads(json.dumps(self.events[0]))
        tampered['record']['text'] = 'something else'
        with self.assertRaises(ValueError):
            operations.apply(self.root, self.db, [tampered])

    def test_partial_batch_keeps_its_prefix(self):
        db = ledger.connect(self.root / 'local/second.sqlite3')
        bad = {'event_id': 'social:bad', 'type': 'social', 'record': {'kind': 'follower_check', 'channel': 'instagram',
               'at': '2026-11-09T11:00:00Z', 'status': 'unavailable', 'count': 0, 'source': 'x'}}
        with self.assertRaises(ValueError):
            operations.apply(self.root, db, self.events[:3] + [bad])
        self.assertEqual(db.execute('SELECT COUNT(*) FROM social_events').fetchone()[0], 3)
        retry = operations.apply(self.root, db, self.events)
        self.assertEqual(sum(r['status'] == 'already_applied' for r in retry), 3)
        db.close()

    def test_approved_text_cannot_be_reworded_under_the_same_test(self):
        with self.assertRaises(ValueError):
            operations.apply(self.root, self.db, [{'event_id': 'social:reword', 'type': 'social', 'record': {
                'kind': 'engagement', 'test_id': 'tt-first-follower-security', 'stage': 'handed_off', 'channel': 'tiktok',
                'at': '2026-11-09T11:00:00Z', 'source': 'x', 'text': 'A new wording'}}])

    def test_correction_supersedes_without_rewriting(self):
        operations.apply(self.root, self.db, [{'event_id': 'social:fix', 'type': 'social', 'record': {
            'kind': 'follower_check', 'channel': 'pinterest', 'at': '2026-11-09T09:37:00Z', 'status': 'counted', 'count': 0,
            'source': 'reread', 'supersedes': 'social:followers:pinterest:2026-11-09T0937'}}])
        ch = social.status(self.db, NOW)['channels']['pinterest']
        self.assertEqual(ch['last_attempt']['status'], 'counted')
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM social_events WHERE event_id='social:followers:pinterest:2026-11-09T0937'").fetchone()[0], 1)

    def test_no_customer_data_and_no_off_channel_urls(self):
        for record in ({'kind': 'follower_check', 'channel': 'tiktok', 'at': '2026-11-09T00:00:00Z', 'status': 'counted', 'count': 1, 'source': 'a fan, someone@example.com'},
                       {'kind': 'engagement', 'test_id': 'x-test', 'stage': 'proposed', 'channel': 'tiktok', 'at': '2026-11-09T00:00:00Z', 'source': 's', 'target_url': 'https://example.com/post'},
                       {'kind': 'follower_check', 'channel': 'threads', 'at': '2026-11-09T00:00:00Z', 'status': 'unavailable', 'source': 's'}):
            with self.assertRaises(ValueError):
                social.validate(record)

    def test_checkpoint_carries_the_history(self):
        from engine import state_store
        archive = self.root / 'local/checkpoint/state.tgz'
        state_store.export(self.root, archive)
        other = Path(tempfile.mkdtemp())
        (other / 'local').mkdir()
        moved = other / 'local/incoming.tgz'
        moved.write_bytes(archive.read_bytes())
        state_store.restore(other, moved, True)
        db = ledger.connect(other / 'local/engine.sqlite3')
        self.assertEqual(len(social.status(db, NOW)['tests']), 2)
        db.close()


class CommandLine(unittest.TestCase):
    """Through growth.py itself, in a fresh copy with no local/ state: the path a new session actually takes."""

    def test_fresh_checkout_recovers_through_the_cli(self):
        import shutil
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / 'repo'
            shutil.copytree(ROOT, fresh, ignore=shutil.ignore_patterns('local', '.git', '__pycache__'))

            def run(*args):
                return subprocess.run([sys.executable, 'growth.py', *args], cwd=fresh, capture_output=True, text=True)
            first = run('events', 'import', 'docs/social/2026-11-09-engagement-history.json')
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout.count('"applied"'), len(json.loads(HISTORY.read_text())))
            again = run('events', 'import', 'docs/social/2026-11-09-engagement-history.json')
            self.assertNotIn('"applied"', again.stdout)
            status = run('social', 'status')
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn('Owner: publishing', status.stdout)
            self.assertIn('First-follower monitor still watching: instagram, pinterest', status.stdout)
            floor_out = run('floor', '--format', 'meme')
            self.assertEqual(floor_out.returncode, 0, floor_out.stderr)
            self.assertIn('dumb-stopping', floor_out.stdout)


class FloorAndDrive(unittest.TestCase):
    def test_floor_is_well_formed_and_filters_by_format(self):
        data = json.loads((ROOT / 'factory/floor.json').read_text())
        self.assertEqual(floor.errors(data), [])
        ids = {e['id'] for e in floor.load(ROOT, 'still')['entries']}
        self.assertIn('real-dogs', ids)
        self.assertNotIn('voice-personality', ids)

    def test_drive_audit_catches_sprawl(self):
        drive_map = json.loads((ROOT / 'config/drive-map.json').read_text())
        F = drive_audit.FOLDER
        listing = [
            {'id': '1boYZjB7ma-1YIcKzSl51usdYuNk6faHO', 'title': 'Posts', 'mimeType': F, 'parentId': '1AHZLgwj1nHemNJeP56fQU6iTpgIEALzZ'},
            {'id': 'p28', 'title': 'F28', 'mimeType': F, 'parentId': '1boYZjB7ma-1YIcKzSl51usdYuNk6faHO'},
            {'id': 'a', 'title': 'heartside_F28_stick_reel.mp4', 'mimeType': 'video/mp4', 'parentId': 'p28'},
            {'id': 'b', 'title': 'heartside_F28_stick-v2_cover.jpg', 'mimeType': 'image/jpeg', 'parentId': 'p28'},
            {'id': 'c', 'title': 'notes.txt', 'mimeType': 'text/plain', 'parentId': 'p28'},
            {'id': 'd', 'title': 'Random sheet', 'mimeType': 'x', 'parentId': '1AHZLgwj1nHemNJeP56fQU6iTpgIEALzZ'},
            {'id': 'e', 'title': 'loose.png', 'mimeType': 'image/png', 'parentId': '1Z2FeYx2hoBX0z8vP5jTHaGV0kBbsI9Fg'},
            {'id': 's', 'title': '2026-11-10_Claude-Hero-Batch', 'mimeType': F, 'parentId': '1Z2FeYx2hoBX0z8vP5jTHaGV0kBbsI9Fg'},
            {'id': 's1', 'title': 'frame.png', 'mimeType': 'image/png', 'parentId': 's'},
            {'id': 'w', 'title': 'Heartside | 4–8 November 2026 | Weekly placement review', 'mimeType': 'x', 'parentId': 'inbox'},
            {'id': 'ok', 'title': '02e Schedule and captions (F28)', 'mimeType': 'x', 'parentId': '1AHZLgwj1nHemNJeP56fQU6iTpgIEALzZ'},
        ]
        out = '\n'.join(drive_audit.audit(drive_map, listing))
        self.assertIn('notes.txt', out)
        self.assertIn('WARN  Heartside/03b_Social-Schedule/Posts/F28/heartside_F28_stick-v2_cover.jpg', out)
        self.assertIn('Random sheet', out)
        self.assertIn('loose.png', out)
        self.assertIn('no START-HERE.md', out)
        self.assertIn('outside the Heartside folder', out)
        self.assertNotIn('02e Schedule', out)
        self.assertIn('2 slugs in one post', out)


if __name__ == '__main__':
    unittest.main()
