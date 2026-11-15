"""The HyperFrames note template's static side: what lock.py sees in a note spec, and the pins that keep renders
reproducible. The render itself needs Node and Chrome and is proved by `python3 factory/hf.py`
(docs/audits/2026-11-15-hyperframes-and-claude-ads.md)."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'factory'))
import lock  # noqa: E402

SPEC = json.loads((ROOT / 'factory/hyperframes/example-note.json').read_text())


class NoteTemplate(unittest.TestCase):
    def test_lock_sees_the_line_and_the_render(self):
        lines, renders = lock.uses(SPEC)
        self.assertEqual(lines, [('F06.fr6', 'golden')])
        self.assertEqual(renders, [('golden-sentimental-portrait.jpg', 'golden')])

    def test_the_line_is_a_slot_and_the_template_is_not(self):
        skeleton = lock.skeleton(SPEC)
        self.assertEqual(skeleton['line'], 'role:roast.soft')
        self.assertEqual(skeleton['end']['renders'], ['product:portrait'])
        variant = dict(SPEC, line='F06.kda3', breed='frenchie', end={'renders': ['frenchie-hilarious-portrait.jpg']})
        self.assertEqual(lock.fingerprint(variant), lock.fingerprint(SPEC))

    def test_an_unapproved_line_is_held(self):
        retired = next(l['id'] for l in lock.BANK['lines'] if l['status'] == 'retired')
        problems, _ = lock.check(dict(SPEC, line=retired))
        self.assertTrue(any('not approved by Krish' in p for p in problems))

    def test_the_template_carries_no_copy_and_fetches_nothing(self):
        html = (ROOT / 'factory/hyperframes/note/index.html').read_text()
        self.assertNotIn('https://', html.split('-->', 1)[1])   # GSAP and fonts are local files
        self.assertIn('[line from the bank]', html)

    def test_versions_are_pinned_exactly(self):
        pkg = json.loads((ROOT / 'factory/hyperframes/package.json').read_text())
        lock_file = json.loads((ROOT / 'factory/hyperframes/package-lock.json').read_text())['packages']
        for name, version in pkg['dependencies'].items():
            self.assertRegex(version, r'^\d+\.\d+\.\d+$')
            self.assertEqual(lock_file[f'node_modules/{name}']['version'], version)

    def test_the_driver_switches_telemetry_off(self):
        source = (ROOT / 'factory/hf.py').read_text()
        for switch in ('HYPERFRAMES_NO_TELEMETRY', 'DO_NOT_TRACK', 'HYPERFRAMES_NO_UPDATE_CHECK', 'HYPERFRAMES_NO_AUTO_INSTALL',
                       'HYPERFRAMES_SKIP_SKILLS', "'telemetry', 'disable'", "'png-sequence'"):
            self.assertIn(switch, source)


if __name__ == '__main__':
    unittest.main()
