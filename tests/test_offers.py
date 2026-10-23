import copy
import datetime as dt
import unittest

import growth
from engine import offers


def state():
    return {'sha': 'a' * 40, 'synced_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'rules_ok': True,
            'offers': [{'id': 'the-morning-mug', 'name': 'The Morning Mug', 'price_cents': 2900, 'bundle_price_cents': None},
                       {'id': 'the-tree-ornament', 'name': 'The Tree Ornament', 'price_cents': 2400, 'bundle_price_cents': 1900}],
            'store': [{'title': 'The Morning Mug', 'available': True, 'prices': [29], 'url': 'https://heartside.io/products/mug'},
                      {'title': 'The Tree Ornament', 'available': True, 'prices': [24], 'url': 'https://heartside.io/products/ornament'}]}


class OfferTests(unittest.TestCase):
    def test_conversion_drafts_require_current_live_mug_and_homepage(self):
        from pathlib import Path
        import json
        spec=json.loads((Path(growth.HERE)/'campaigns/waits-at-the-door.json').read_text())
        ready=state()
        self.assertIsNone(offers.purchase_campaign(spec,ready))
        ready['homepage_v3']=True
        draft=offers.purchase_campaign(spec,ready)
        self.assertEqual(draft['offers'],[{'id':'the-morning-mug','quantity':1,'unit_price':'29.00'}])
        self.assertEqual(draft['destination'],'https://heartside.io/products/mug')
        self.assertIn('{link}',draft['captions']['pinterest'][0])
        self.assertEqual(spec['intent'],'audience')
        ready['store']=[]
        self.assertIsNone(offers.purchase_campaign(spec,ready))

    def test_price_is_read_from_canonical_gift_table(self):
        text = '## 3. The gift range (launch)\n| **The Morning Mug** | #403 | $29 | costs |\n## 4. Next\n'
        self.assertEqual(offers.canonical_offers({'v3': text})[0]['price_cents'], 2900)
        ornament = '## 3. The gift range (launch)\n| **The Tree Ornament** | #900 | $24, or $19 with another gift | costs |\n'
        row = offers.canonical_offers({'v3': ornament})[0]
        self.assertEqual((row['price_cents'], row['bundle_price_cents']), (2400, 1900))

    def test_original_wrong_price_probe_is_rejected_even_with_sentence_period(self):
        self.assertTrue(offers.validate_item({}, 'The Morning Mug is $89.', state()))

    def test_correct_active_gift_and_destination_pass(self):
        item = {'intent': 'buy', 'offers': [{'id': 'the-morning-mug', 'unit_price': '29.00'}]}
        self.assertEqual(offers.validate_item(item, 'The Morning Mug, $29. https://heartside.io/products/mug', state()), [])
        item['offers'][0]['unit_price'] = '89'
        self.assertTrue(offers.validate_item(item, 'The Morning Mug, $89. https://heartside.io/products/mug', state()))

    def test_draft_gift_and_unavailable_cheap_variant_do_not_pass(self):
        s = state(); s['store'] = []
        self.assertFalse(offers.catalog(s)[0]['ready'])
        s = state(); s['store'][0]['variants'] = [{'price': '29', 'available': False}, {'price': '39', 'available': True}]
        self.assertFalse(offers.catalog(s)[0]['ready'])

    def test_bundle_price_requires_current_evidence_and_another_gift(self):
        item = {'offers': [{'id': 'the-morning-mug', 'unit_price': '29'}, {'id': 'the-tree-ornament', 'unit_price': '19'}]}
        s = state()
        self.assertTrue(offers.validate_item(item, 'Two gifts, $48. https://heartside.io/?view=gifts', s))
        s['bundle_verified_at'] = s['synced_at']
        self.assertEqual(offers.validate_item(item, 'Two gifts, $48. https://heartside.io/?view=gifts', s), [])

    def test_price_for_another_gift_and_wrong_link_are_rejected(self):
        item = {'offers': [{'id': 'the-tree-ornament', 'unit_price': '24'}]}
        self.assertTrue(offers.validate_item(item, 'The Morning Mug, $24. https://heartside.io/products/ornament', state()))
        self.assertTrue(offers.validate_item(item, 'Buy for $24. https://heartside.io/products/mug', state()))

    def test_old_and_future_catalogs_are_not_fresh(self):
        s = state(); s['synced_at'] = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=2)).isoformat()
        self.assertFalse(offers.fresh_store(s))
        s['synced_at'] = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=2)).isoformat()
        self.assertFalse(offers.fresh_store(s))

    def test_unreachable_catalog_is_not_a_fresh_empty_catalog(self):
        s = state()
        s['store'] = None
        self.assertFalse(offers.fresh_store(s))
        self.assertEqual(offers.catalog(s)[0]['reason'], 'public catalog could not be checked')
        s['store'] = []
        self.assertTrue(offers.fresh_store(s))
        self.assertEqual(offers.catalog(s)[0]['reason'], 'not in the public catalog')

    def test_empty_and_duplicate_daily_items_fail(self):
        pack = {'kind': 'daily', 'pack_date': '2026-10-17', 'heartside_sha': 'a' * 40, 'headline': 'Pack', 'items': []}
        self.assertTrue(growth.check_pack(pack))
        item = {'platform': 'instagram', 'creative_id': 'IG_EMO_REEL_C90_H01_V1_20261017', 'text': 'Your dog loves you too.'}
        pack['items'] = [item, copy.deepcopy(item)]
        self.assertTrue(any('duplicate' in e for e in growth.check_pack(pack)))


if __name__ == '__main__':
    unittest.main()
