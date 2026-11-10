"""The judging panel: code checks, judge briefs drawn from the floor and anchors, and agreement with Krish."""
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'factory'))
import panel  # noqa: E402
from PIL import Image  # noqa: E402

MANIFEST = os.path.join(os.path.dirname(__file__), '..', 'factory', 'sprints', '2026-11-S120.json')


class PanelTest(unittest.TestCase):
    def test_tier0_passes_a_good_slot_and_holds_missing_media(self):
        self.assertEqual(panel.tier0(MANIFEST, 'V001'), [])
        self.assertTrue(panel.tier0(MANIFEST, 'V001', '/nope.mp4'))
        self.assertTrue(panel.tier0(MANIFEST, 'V999'))

    def test_briefs_carry_the_floor_and_the_anchors(self):
        t1 = panel.brief('tier1', ['a.png'])
        self.assertIn('real-dogs', t1); self.assertIn('text-clear-of-faces', t1)
        t2 = panel.brief('tier2', ['a.png'])
        self.assertIn('yt:u7s47cIeh6M', t2)
        self.assertIn('These dogs look fake and sometimes malformed.', t2)

    def test_an_image_sheet_is_the_picture_scaled(self):
        with tempfile.TemporaryDirectory() as d:
            Image.new('RGB', (2000, 3000)).save(f'{d}/a.png')
            panel.sheet(f'{d}/a.png', f'{d}/s.png')
            self.assertLessEqual(max(Image.open(f'{d}/s.png').size), 1024)

    def test_a_batch_tiles_up_to_four_sheets_into_one_image(self):
        with tempfile.TemporaryDirectory() as d:
            for i in range(4):
                Image.new('RGB', (1024, 900)).save(f'{d}/{i}.png')
            panel.batch([f'{d}/{i}.png' for i in range(4)], f'{d}/b.png')
            self.assertEqual(Image.open(f'{d}/b.png').width, 1536)
            with self.assertRaises(SystemExit):
                panel.batch([f'{d}/0.png'] * 5, f'{d}/x.png')

    def test_agreement_counts_only_slots_both_judged(self):
        rows = [{'slot': 'A', 'tier': 'tier2', 'verdict': 'tier2-9', 'score': 9},
                {'slot': 'A', 'tier': 'krish', 'verdict': 'krish-yes', 'score': None},
                {'slot': 'B', 'tier': 'tier2', 'verdict': 'tier2-9', 'score': 9},
                {'slot': 'B', 'tier': 'krish', 'verdict': 'krish-no', 'score': None},
                {'slot': 'C', 'tier': 'tier2', 'verdict': 'tier2-7', 'score': 7}]
        self.assertEqual(panel.agreement(rows), (0.5, 2))


if __name__ == '__main__':
    unittest.main()


class HumourAnchorTest(unittest.TestCase):
    def test_tier2_brief_carries_krish_humour_profile(self):
        text = panel.brief('tier2', ['x.jpg'])
        self.assertIn('an intelligent observation, an utterly stupid premise, and a slightly cruel payoff', text)
        self.assertIn('docs/HUMOUR.md', text)
        self.assertIn('"humour"', text)

    def test_humour_profile_doc_exists_with_krish_words(self):
        import os
        doc = open(os.path.join(os.path.dirname(__file__), '..', 'docs', 'HUMOUR.md'), encoding='utf-8').read()
        self.assertIn('Make sure every build in all the sessions anchors towards this', doc)
