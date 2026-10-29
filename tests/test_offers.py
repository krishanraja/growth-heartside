import copy
import datetime as dt
import unittest

import growth
from engine import offers


IMAGES = {'blanket': 'heartside-word-free-blanket-example.png', 'portrait': '6adf25082493a.webp', 'mug': '6ae2d892c1504.webp'}


def state():
    def product(title, handle, prices, gift):
        return {'title': title, 'available': True, 'prices': prices, 'url': f'https://heartside.io/products/{handle}',
                'images': [{'src': f'https://heartside.io/cdn/shop/files/{IMAGES[gift]}?v=1'}] if gift in IMAGES else []}
    return {'sha': 'a' * 40, 'synced_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'rules_ok': True,
            'offers': offers.canonical_offers({'docs/ECONOMICS.md': ECONOMICS}),
            'store': [product("Your Dog's Personality Blanket", 'your-dogs-personality-blanket', [129], 'blanket'),
                      product("Your Dog's Portrait", 'your-dogs-portrait', [59, 119], 'portrait'),
                      product("Your Dog's Illustrated Mug", 'your-dogs-illustrated-mug', [45], 'mug'),
                      product("Artist's touch", 'artists-touch', [29], None)]}


ECONOMICS = ('The configured baseline is USD45 mug, USD59 unframed portrait, USD119 framed portrait and USD129 blanket; '
             'NOW owns the readback. Two offers have been live since 27 October: the automatic bundle (15% off two gifts, '
             "20% off three or more, gifts only) and the USD29 Artist's touch add-on. In its two operating sets, two mugs "
             'at 15% sit USD0.79 to USD5.13 below the floor.')
BLANKET = 'https://heartside.io/products/your-dogs-personality-blanket'
PORTRAIT = 'https://heartside.io/products/your-dogs-portrait'


class OfferTests(unittest.TestCase):
    def test_conversion_drafts_sell_the_lead_gift_the_film_ends_on(self):
        from pathlib import Path
        import json
        spec=json.loads((Path(growth.HERE)/'campaigns/waits-at-the-door.json').read_text())
        ready=state()
        self.assertIsNone(offers.purchase_campaign(spec,ready))
        ready['homepage_v3']=True
        draft=offers.purchase_campaign(spec,ready)
        self.assertEqual(draft['offers'],[{'id':'blanket','quantity':1,'unit_price':'129.00'}])
        self.assertEqual(draft['destination'],BLANKET)
        self.assertIn('{link}',draft['captions']['pinterest'][0])
        self.assertEqual(spec['intent'],'audience')
        ready['store']=[]
        self.assertIsNone(offers.purchase_campaign(spec,ready))

    def test_the_mug_sells_like_any_other_gift(self):
        from pathlib import Path
        import json
        spec=json.loads((Path(growth.HERE)/'campaigns/morning-proof.json').read_text())
        ready=state(); ready['homepage_v3']=True
        draft=offers.purchase_campaign(spec,ready)
        self.assertEqual(draft['offers'],[{'id':'mug','quantity':1,'unit_price':'45.00'}])
        self.assertEqual(offers.validate_item({'intent':'buy','offers':draft['offers']},
                         "Your Dog's Illustrated Mug, $45. https://heartside.io/products/your-dogs-illustrated-mug", ready), [])

    def test_prices_are_read_from_the_canon_baseline(self):
        rows = {o['id']: o for o in offers.canonical_offers({'docs/ECONOMICS.md': ECONOMICS})}
        self.assertEqual(set(rows), {'blanket', 'portrait', 'mug', 'artists-touch'})
        self.assertEqual(rows['portrait']['prices_cents'], [5900, 11900])
        self.assertEqual(rows['artists-touch']['kind'], 'add_on')
        self.assertEqual(rows['blanket']['bundle_pct'], {'2': 15, '3': 20})
        self.assertNotIn(79, [c for o in rows.values() for c in o['prices_cents']])

    def test_canon_sources_that_disagree_hold_the_gift(self):
        s = state()
        s['offers'] = offers.canonical_offers({'docs/ECONOMICS.md': ECONOMICS, 'README.md': 'The configured retail baseline is $139 blanket.'})
        blanket = next(g for g in offers.catalog(s) if g['id'] == 'blanket')
        self.assertFalse(blanket['ready'])
        self.assertEqual(blanket['reason'], 'canon sources disagree on its price')

    def test_original_wrong_price_probe_is_rejected_even_with_sentence_period(self):
        self.assertTrue(offers.validate_item({}, "Your Dog's Personality Blanket is $89.", state()))

    def test_correct_active_gift_and_destination_pass(self):
        item = {'intent': 'buy', 'offers': [{'id': 'blanket', 'unit_price': '129.00'}]}
        self.assertEqual(offers.validate_item(item, f"Your Dog's Personality Blanket, $129. {BLANKET}", state()), [])
        item['offers'][0]['unit_price'] = '89'
        self.assertTrue(offers.validate_item(item, f"Your Dog's Personality Blanket, $89. {BLANKET}", state()))

    def test_either_portrait_price_passes(self):
        for price in ('59', '119'):
            item = {'intent': 'buy', 'offers': [{'id': 'portrait', 'unit_price': price}]}
            self.assertEqual(offers.validate_item(item, f"Your Dog's Portrait, ${price}. {PORTRAIT}", state()), [])

    def test_draft_gift_and_unavailable_cheap_variant_do_not_pass(self):
        s = state(); s['store'] = []
        self.assertFalse(offers.catalog(s)[0]['ready'])
        s = state(); s['store'][0]['variants'] = [{'price': '129', 'available': False}, {'price': '139', 'available': True}]
        self.assertFalse(offers.catalog(s)[0]['ready'])

    def test_bundle_price_requires_current_evidence_and_another_gift(self):
        item = {'offers': [{'id': 'blanket', 'unit_price': '109.65'}, {'id': 'portrait', 'unit_price': '50.15'}]}
        text = 'Two gifts, $159.80. https://heartside.io/?view=gifts'
        s = state()
        self.assertTrue(offers.validate_item(item, text, s))
        s['bundle_verified_at'] = s['synced_at']
        self.assertEqual(offers.validate_item(item, text, s), [])
        alone = {'offers': [{'id': 'blanket', 'unit_price': '109.65'}]}
        self.assertTrue(offers.validate_item(alone, 'One gift, $109.65. ' + BLANKET, s))

    def test_copy_naming_an_undeclared_gift_is_rejected(self):
        item = {'intent': 'buy', 'offers': [{'id': 'blanket', 'unit_price': '129'}]}
        self.assertTrue(any('portrait' in e for e in offers.validate_item(
            item, f'The blanket, $129, or the portrait. {BLANKET}', state())))

    def test_price_for_another_gift_and_wrong_link_are_rejected(self):
        item = {'offers': [{'id': 'mug', 'unit_price': '45'}]}
        self.assertTrue(offers.validate_item(item, f"Your Dog's Personality Blanket, $45. {BLANKET}", state()))
        self.assertTrue(offers.validate_item(item, f'Buy for $45. {BLANKET}', state()))

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
