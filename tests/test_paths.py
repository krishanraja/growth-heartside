"""Counted paths from a scheduled post to an order (engine/paths.py)."""
import unittest

import growth
from engine import attribution, paths

FB_CID = 'FB_ENT_REEL_C171_H01_V1_20261118'
TT_CID = 'TT_ENT_REEL_C171_H01_V1_20261118'
IG_CID = 'IG_ENT_REEL_C171_H01_V1_20261118'


def row(platform, cid, caption, link=''):
    return {'slot': f'2026-11-18_08:00_{platform}', 'platform': platform, 'post_id': 'F52', 'creative_id': cid,
            'caption': caption, 'link': link}


class PathTests(unittest.TestCase):
    def test_a_tracked_link_is_counted_under_its_family(self):
        link = growth.tracked('https://heartside.io', FB_CID)
        self.assertEqual(paths.counted_path(row('facebook', FB_CID, 'x\n' + link, link), {}, {}), ('tracked_link', 'FB_ENT_C171'))

    def test_another_posts_tags_do_not_count_for_this_row(self):
        link = growth.tracked('https://heartside.io', 'FB_ENT_REEL_C172_H01_V1_20261118')
        self.assertEqual(paths.counted_path(row('facebook', FB_CID, link, link), {}, {})[0], 'none')

    def test_tiktok_link_in_bio_is_uncounted_until_the_profile_link_is_set(self):
        r = row('tiktok', TT_CID, 'joke\n\nGifts from your dog. Link in bio.', 'link in bio')
        path, why = paths.counted_path(r, {}, {})
        self.assertEqual(path, 'none'); self.assertIn('TikTok', why)
        self.assertEqual(paths.counted_path(r, {}, {'tiktok': '2026-11-15'}), ('profile_link', 'TT_OFFER_C900'))

    def test_a_registered_code_in_the_caption_counts(self):
        r = row('instagram', IG_CID, 'joke. Code HEART171I at checkout.')
        self.assertEqual(paths.counted_path(r, {'HEART171I': 'IG_ENT_C171'}, {}), ('code', 'IG_ENT_C171'))
        self.assertEqual(paths.counted_path(r, {}, {})[0], 'none')

    def test_the_profile_url_classifies_in_the_engine_tier(self):
        for p in ('instagram', 'tiktok', 'facebook', 'pinterest'):
            url = paths.profile_url(p)
            cid = paths.profile_creative_id(p)
            self.assertTrue(attribution.CREATIVE_ID.match(cid))
            q = dict(kv.split('=') for kv in url.split('?', 1)[1].split('&'))
            visit = {'landingPage': '/', 'referrerUrl': '', 'source': '', 'utmParameters': {
                'source': q['utm_source'], 'medium': q['utm_medium'], 'campaign': q['utm_campaign'], 'content': q['utm_content']}}
            order = {'discountCodes': [], 'customerJourneySummary': {'ready': True, 'lastVisit': visit, 'firstVisit': None}}
            tier, family = attribution.classify(order, {})
            self.assertEqual(tier, 'engine', p); self.assertTrue(family.endswith('_OFFER_C900'))

    def test_code_drafts_cover_only_uncounted_rows_and_fit_the_code_shape(self):
        rows = paths.audit([row('tiktok', TT_CID, 'Link in bio.'), row('facebook', FB_CID, growth.tracked('https://heartside.io', FB_CID))], {}, {})
        drafts = paths.code_drafts(rows)
        self.assertEqual([d['code'] for d in drafts], ['HEART171T'])
        self.assertRegex(drafts[0]['code'], growth.CODE_SHAPE.pattern.strip('\\b'))
        self.assertTrue(attribution.FAMILY.match(drafts[0]['family']))

    def test_the_shipped_profile_config_sets_nothing(self):
        self.assertEqual(paths.set_profiles(), {})


if __name__ == '__main__':
    unittest.main()
