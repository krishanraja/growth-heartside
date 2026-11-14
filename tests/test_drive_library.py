"""The Drive listing Control Center serves (protocol 1.35.0, fleet integration I-25), audited every run."""
import json
import tempfile
import unittest
from pathlib import Path

from engine import drive_library

ROOT = Path(__file__).resolve().parents[1]
MAP = json.loads((ROOT / 'config/drive-map.json').read_text())
HS = MAP['heartside']
POSTS = next(k for k, v in MAP['folders'].items() if v['rule'] == 'posts')
SCHEDULE = next(k for k, v in MAP['folders'].items() if v['rule'] == 'schedule')


def directive(part):
    return {'directive': {'library': part}}


def served(files):
    folders = [{'id': HS, 'name': 'Heartside', 'parent_id': 'activeventures', 'folder': 'Heartside', 'link_role': None, 'trashed': False},
               {'id': SCHEDULE, 'name': '03b_Social-Schedule', 'parent_id': HS, 'folder': 'Heartside/03b_Social-Schedule', 'link_role': None, 'trashed': False},
               {'id': POSTS, 'name': 'Posts', 'parent_id': SCHEDULE, 'folder': 'Heartside/03b_Social-Schedule/Posts', 'link_role': None, 'trashed': False}]
    return directive({'available': True, 'complete': True, 'as_of': '2026-11-14T06:02:00Z',
                      'roots': [{'root': 'Ventures/Active Ventures/Heartside', 'id': HS, 'folders': folders, 'files': files}]})


class DriveLibraryTest(unittest.TestCase):
    def test_the_map_declares_its_root_in_drive_map_1(self):
        self.assertEqual(MAP['drive_map']['schema'], 'drive-map/1')
        self.assertEqual(MAP['drive_map']['roots'][0]['id'], HS)

    def test_unknown_is_never_clean(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(drive_library.check(d, {}), {'state': 'unknown', 'reason': 'not_served'})
            off = directive({'available': False, 'complete': False, 'reason': 'latest_read_partial', 'as_of': None})
            self.assertEqual(drive_library.check(d, off, MAP), {'state': 'unknown', 'reason': 'latest_read_partial'})
            self.assertFalse((Path(d) / drive_library.OUT).exists())

    def test_a_stray_in_the_schedule_folder_is_an_error_and_counts_only_leave_the_run(self):
        files = [{'folder': 'Heartside/03b_Social-Schedule', 'title': 'Copy of 02 Schedule', 'mime': 'application/vnd.google-apps.spreadsheet', 'modified': None},
                 {'folder': 'Heartside/03b_Social-Schedule', 'title': '01 Posting strategy', 'mime': 'application/vnd.google-apps.document', 'modified': None}]
        with tempfile.TemporaryDirectory() as d:
            out = drive_library.check(d, served(files), MAP)
            self.assertEqual(out['state'], 'checked')
            self.assertEqual(out['errors'], 1)
            self.assertNotIn('Copy of', json.dumps(out))
            saved = json.loads((Path(d) / drive_library.OUT).read_text())
            self.assertTrue(any('Copy of 02 Schedule' in p for p in saved['problems']))


if __name__ == '__main__':
    unittest.main()
