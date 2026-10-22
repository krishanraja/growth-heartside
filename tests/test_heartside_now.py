"""Heartside's status is read live from its own NOW.md and never copied here
(Ruling, Krish, 2026-10-22). No network: every GitHub and store call is faked."""
import contextlib
import io
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

import growth

ROOT = Path(__file__).resolve().parents[1]
HEAD = 'a' * 40
NOW_COMMIT = 'n' * 40


def commit(sha, message):
    return {'sha': sha, 'commit': {'message': message, 'committer': {'date': '2026-10-22T10:00:00Z'}}}


def fake_github(history, now_text='# NOW\n\nShipping the mug.\n', fail_now=False):
    """http() and raw() for a heartside whose main is `history` (newest first)."""
    def http(url, accept_json=True, timeout=60):
        if url.startswith(growth.STORE):
            if url.endswith('/'):
                return '<div data-hs3-config></div>'
            return {'products': []}
        if '/commits?' in url and 'path=NOW.md' in url:
            if fail_now:
                raise urllib.error.HTTPError(url, 403, 'rate limited', None, None)
            return [c for c in history if c['sha'] == NOW_COMMIT][:1]
        if '/commits?' in url and 'since=' in url:
            return history[:2]
        if '/commits?' in url:
            return history
        if '/pulls?' in url:
            return [{'number': 7, 'title': 'Share card', 'head': {'ref': 'share'}, 'updated_at': '2026-10-22T09:00:00Z'}]
        if '/contents/docs' in url:
            return []
        raise AssertionError(url)

    def raw(path, sha):
        if path == 'NOW.md':
            if fail_now:
                raise urllib.error.URLError('offline')
            return now_text
        return f'text of {path}'
    return http, raw


class VerdictTests(unittest.TestCase):
    def test_fresh_when_only_steward_commits_follow(self):
        history = [{'sha': 'x', 'message': 'docs(steward): refresh LOG'}, {'sha': NOW_COMMIT, 'message': 'docs(steward): NOW'}]
        self.assertEqual(growth.now_verdict(history, NOW_COMMIT), ('fresh', []))

    def test_stale_when_other_work_follows(self):
        history = [{'sha': 'y', 'message': 'Gift page fits one screen'}, {'sha': 'x', 'message': 'docs(steward): log'},
                   {'sha': NOW_COMMIT, 'message': 'docs(steward): NOW'}]
        status, later = growth.now_verdict(history, NOW_COMMIT)
        self.assertEqual(status, 'stale')
        self.assertEqual([c['sha'] for c in later], ['y'])

    def test_unknown_when_its_commit_is_out_of_reach(self):
        self.assertEqual(growth.now_verdict([{'sha': 'x', 'message': 'docs(steward): log'}], NOW_COMMIT)[0], 'unknown')
        self.assertEqual(growth.now_verdict([{'sha': 'x', 'message': 'Fix'}], NOW_COMMIT)[0], 'stale')


class LiveReadTests(unittest.TestCase):
    def read(self, history, **kw):
        http, raw = fake_github(history, **kw)
        with mock.patch.object(growth, 'http', http), mock.patch.object(growth, 'raw', raw):
            return growth.heartside_now(HEAD)

    def test_fresh_now_md_is_returned(self):
        live = self.read([commit(NOW_COMMIT, 'docs(steward): NOW')])
        self.assertEqual(live['status'], 'fresh')
        self.assertIn('Shipping the mug', live['text'])

    def test_stale_now_md_is_unknown_and_withheld(self):
        live = self.read([commit('b' * 40, 'Gift page fits one screen'), commit(NOW_COMMIT, 'docs(steward): NOW')])
        self.assertEqual(live['status'], 'stale')
        self.assertIsNone(live['text'])
        self.assertIn('status: unknown', '\n'.join(growth.now_section(live)))

    def test_unreadable_source_is_unknown(self):
        live = self.read([commit(NOW_COMMIT, 'docs(steward): NOW')], fail_now=True)
        self.assertEqual(live['status'], 'unknown')
        self.assertIsNone(live['text'])
        self.assertIn('not read', live['reason'])
        self.assertIn('status: unknown', '\n'.join(growth.now_section(live)))

    def test_missing_now_md_is_unknown(self):
        live = self.read([commit(NOW_COMMIT, 'x')], now_text=None)
        self.assertEqual(live['status'], 'unknown')
        self.assertIn('no NOW.md', live['reason'])

    def test_head_unreachable_is_unknown_not_an_error(self):
        with mock.patch.object(growth, 'head_sha', side_effect=OSError('offline')):
            self.assertEqual(growth.heartside_now()['status'], 'unknown')


class NoCopyTests(unittest.TestCase):
    def sync(self, history, **kw):
        http, raw = fake_github(history, **kw)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        state_dir = Path(tmp.name) / 'state'
        state_dir.mkdir()
        (state_dir / growth.RETIRED_COPY).write_text('an old copy')
        out = io.StringIO()
        with mock.patch.object(growth, 'http', http), mock.patch.object(growth, 'raw', raw), \
                mock.patch.object(growth, 'head_sha', lambda: HEAD), mock.patch.object(growth, 'STATE_DIR', str(state_dir)), \
                contextlib.redirect_stdout(out):
            state = growth.sync()
        return state, state_dir, out.getvalue()

    def test_sync_writes_no_copy_of_heartside_status(self):
        state, state_dir, printed = self.sync([commit(NOW_COMMIT, 'docs(steward): NOW')])
        self.assertEqual(sorted(p.name for p in state_dir.iterdir()), ['heartside.json'])
        stored = (state_dir / 'heartside.json').read_text()
        self.assertNotIn('Shipping the mug', stored)
        self.assertNotIn('Share card', stored)
        for key in ('commits', 'open_pulls'):
            self.assertNotIn(key, state)
        self.assertEqual(state['heartside_status'], 'fresh')
        self.assertIn('Shipping the mug', printed)
        self.assertIn('Share card', printed)

    def test_sync_reports_an_unreadable_now_md_as_unknown(self):
        state, _, printed = self.sync([commit(NOW_COMMIT, 'docs(steward): NOW')], fail_now=True)
        self.assertEqual(state['heartside_status'], 'unknown')
        self.assertIn("Heartside's own status: unknown", printed)
        self.assertNotIn('Shipping the mug', printed)

    def test_the_repository_holds_no_copy(self):
        self.assertFalse((ROOT / 'state').exists())
        archived = (ROOT / 'docs/history/2026-10-22-HEARTSIDE-NOW.md').read_text().splitlines()
        self.assertEqual(archived[:3], [
            '> **Historical.** Archived 2026-10-22. Not current guidance.',
            '> Replaced by: live read of krishanraja/heartside NOW.md',
            "> Reason: a copy of another repository's status goes stale.",
        ])
        workflow = (ROOT / '.github/workflows/sync.yml').read_text()
        self.assertIn('contents: read', workflow)
        self.assertNotIn('git commit', workflow)
        self.assertNotIn('--publish', workflow)


if __name__ == '__main__':
    unittest.main()
