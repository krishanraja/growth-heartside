import datetime as dt
import os
import sqlite3
import unittest
from unittest import mock

from engine import attribution, protocol

CID = 'IG_EMO_REEL_C90_H01_V1_20261029'


def visit(content=None, campaign='hs_growth_202610', medium='organic_video', referrer=None, landing='https://heartside.io/'):
    return {'landingPage': landing, 'referrerUrl': referrer, 'source': None,
            'utmParameters': {'source': 'instagram', 'medium': medium, 'campaign': campaign, 'content': content} if content or medium else None}


def order(last=None, first=None, amount='129.00', created='2026-10-20T15:00:00Z', ready=True, refunded='0.00', **kw):
    return {'createdAt': created, 'test': False, 'cancelledAt': None, 'tags': [], 'discountCodes': [],
            'subtotalPriceSet': {'shopMoney': {'amount': amount, 'currencyCode': 'USD'}},
            'totalRefundedSet': {'shopMoney': {'amount': refunded, 'currencyCode': 'USD'}},
            'customerJourneySummary': {'ready': ready, 'lastVisit': last, 'firstVisit': first}, **kw}


class AttributionTests(unittest.TestCase):
    def test_engine_tags_name_the_post_family(self):
        self.assertEqual(attribution.classify(order(visit(CID))), ('engine', 'IG_EMO_C90'))

    def test_first_visit_from_a_post_still_counts(self):
        self.assertEqual(attribution.classify(order(last=visit(medium=None), first=visit(CID)))[0], 'engine')

    def test_social_referrer_without_tags_is_organic_social(self):
        self.assertEqual(attribution.classify(order(visit(medium=None, referrer='https://www.tiktok.com/')))[0], 'organic_social')

    def test_a_meta_visit_with_no_engine_id_or_code_is_unverified_until_the_ads_questions_are_answered(self):
        # Could be an ad click whose link carries no paid tag: never organic, never a winner, until Krish answers.
        untagged = order(visit(medium=None, referrer='https://l.instagram.com/?u=x'))
        fbclid = order(visit(medium='organic', landing='https://heartside.io/?fbclid=abc'))
        facebook = order(visit(medium=None, referrer='https://m.facebook.com/'))
        for one in (untagged, fbclid, facebook):
            self.assertEqual(attribution.classify(one), ('unverified', None))
        self.assertEqual(attribution.classify(order(visit(CID, referrer='https://l.instagram.com/'))), ('engine', 'IG_EMO_C90'))
        with mock.patch.object(attribution, 'META_UNVERIFIED', False):
            self.assertEqual(attribution.classify(untagged)[0], 'organic_social')
        reading = attribution.aggregate([untagged, order(visit(CID))], dt.date(2026, 10, 1), dt.date(2026, 10, 29))
        self.assertEqual(reading['tiers']['unverified'], {'orders': 1, 'net_sales': 129.0})
        self.assertEqual(reading['organic'], {'orders': 1, 'net_sales': 129.0})
        self.assertEqual(reading['store'], {'orders': 2, 'net_sales': 258.0})

    def test_meta_by_utm_or_shopify_source_alone_is_unverified(self):
        # Instagram's in-app browser often drops the referrer; Meta's {{site_source_name}} fills ig or fb.
        by_utm = visit(medium='paid_maybe', campaign='x', referrer=None); by_utm['utmParameters']['source'] = 'ig'
        by_source = visit(medium=None, referrer=None); by_source['source'] = 'facebook'
        for one in (by_utm, by_source):
            self.assertEqual(attribution.classify(order(one))[0], 'unverified')
        tiktok = visit(medium=None, referrer=None); tiktok['source'] = 'tiktok'
        self.assertNotEqual(attribution.classify(order(tiktok))[0], 'unverified')

    def test_a_fresh_month_read_beats_an_old_partial_import(self):
        from engine import ledger
        db = ledger.connect(':memory:')
        ledger.import_report(db, {'platform': 'shopify', 'scope': 'store', 'currency': 'USD', 'source': 'Synthetic ShopifyQL',
                                  'observed_at': '2026-11-05T06:00:00Z',
                                  'period': {'start': '2026-11-01', 'end': '2026-11-05', 'timezone': 'Europe/London'},
                                  'values': {'net_sales': 1, 'orders': 0}})
        now = dt.datetime(2026, 11, 13, 6, 0, tzinfo=dt.timezone.utc)
        self.assertEqual(protocol.net_sales(db, now)['availability'], 'stale')  # the import alone ends on the 5th
        start, end = attribution.windows(dt.date(2026, 11, 13))['month']
        attribution.store(db, 'month', attribution.aggregate([order(visit(CID), amount='129.00', created='2026-11-02T15:00:00Z')],
                                                             start, end), observed_at='2026-11-13T05:00:00+00:00')
        sales = protocol.net_sales(db, dt.datetime(2026, 11, 13, 6, 0, tzinfo=dt.timezone.utc))
        self.assertEqual((sales['value'], sales['availability']), (129, 'measured'))

    def test_the_month_window_feeds_net_sales(self):
        from engine import ledger
        spans = attribution.windows(dt.date(2026, 11, 13))
        self.assertEqual(spans['month'], (dt.date(2026, 11, 1), dt.date(2026, 11, 13)))
        self.assertEqual(attribution.windows(dt.date(2026, 12, 1))['month'], (dt.date(2026, 11, 1), dt.date(2026, 12, 1)))
        db = ledger.connect(':memory:')  # the engine's own ledger, with its empty metrics table
        now = dt.datetime(2026, 11, 13, 6, 0, tzinfo=dt.timezone.utc)
        self.assertEqual(protocol.net_sales(db, now)['availability'], 'missing')
        orders = [order(visit(CID), amount='129.00', created='2026-11-02T15:00:00Z'),
                  order(visit(medium='cpc'), amount='59.00', created='2026-11-03T15:00:00Z'),
                  order(visit(CID), amount='45.00', created='2026-10-30T15:00:00Z')]  # last month: not in it
        start, end = spans['month']
        attribution.store(db, 'month', attribution.aggregate(orders, start, end), observed_at='2026-11-13T05:00:00+00:00')
        sales = protocol.net_sales(db, now)
        self.assertEqual((sales['value'], sales['availability'], sales['reason']), (188, 'measured', None))
        self.assertEqual(sales['window_start'][:10], '2026-11-01')
        self.assertEqual(protocol.net_sales(db, now + dt.timedelta(days=2))['availability'], 'stale')

    def test_buffer_s_own_tags_count_as_organic_social(self):
        tagged = visit(medium='social', campaign='buffer')
        tagged['utmParameters']['source'] = 'buffer'
        self.assertEqual(attribution.classify(order(tagged))[0], 'organic_social')
        paid = visit(medium='cpc', campaign='buffer'); paid['utmParameters']['source'] = 'facebook'
        self.assertEqual(attribution.classify(order(paid))[0], 'paid')

    def test_paid_signals_never_count_even_when_tagged(self):
        self.assertEqual(attribution.classify(order(visit(CID, medium='paid_social')))[0], 'paid')
        self.assertEqual(attribution.classify(order(visit(CID, landing='https://heartside.io/?gclid=abc')))[0], 'paid')

    def test_search_pending_and_direct(self):
        self.assertEqual(attribution.classify(order(visit(medium=None, referrer='https://www.google.com/')))[0], 'organic_search')
        self.assertEqual(attribution.classify(order(ready=False))[0], 'pending')
        self.assertEqual(attribution.classify(order(visit(medium=None)))[0], 'direct')

    def test_a_lookalike_host_is_not_social(self):
        self.assertEqual(attribution.classify(order(visit(medium=None, referrer='https://notinstagram.com/')))[0], 'direct')

    def test_aggregate_excludes_test_cancelled_internal_and_out_of_window(self):
        orders = [order(visit(CID)), order(visit(CID), test=True), order(visit(CID), cancelledAt='2026-10-21T00:00:00Z'),
                  order(visit(CID), tags=['hs-internal']), order(visit(CID), created='2026-09-01T12:00:00Z'),
                  order(visit(medium=None), amount='45.00')]
        reading = attribution.aggregate(orders, dt.date(2026, 10, 1), dt.date(2026, 10, 29))
        self.assertEqual(reading['store'], {'orders': 2, 'net_sales': 174.0})
        self.assertEqual(reading['organic'], {'orders': 1, 'net_sales': 129.0})
        self.assertEqual(reading['families'], {'IG_EMO_C90': {'orders': 1, 'net_sales': 129.0}})

    def test_refunds_come_off_and_a_fully_refunded_order_is_not_a_sale(self):
        orders = [order(visit(CID), amount='24.00', refunded='24.00'), order(visit(CID), amount='129.00', refunded='29.00'),
                  order(visit(CID), amount='45.00', refunded='52.50')]
        reading = attribution.aggregate(orders, dt.date(2026, 10, 1), dt.date(2026, 10, 29))
        self.assertEqual(reading['organic'], {'orders': 1, 'net_sales': 100.0})
        self.assertEqual(reading['fully_refunded_orders'], 2)

    def test_london_day_decides_the_window(self):
        late = order(visit(CID), created='2026-10-28T23:30:00Z')  # 29 Oct in London? No: GMT from 25 Oct, so 28 Oct
        early = order(visit(CID), created='2026-10-24T23:30:00Z')  # BST: already 25 Oct in London
        reading = attribution.aggregate([late, early], dt.date(2026, 10, 25), dt.date(2026, 10, 29))
        self.assertEqual(reading['organic']['orders'], 2)

    def test_nothing_per_order_or_any_query_string_is_stored(self):
        private = order(visit(CID, landing='https://heartside.io/?dog=Kuku&person=Sam'), first=visit(medium=None, referrer='https://instagram.com/p/xyz'))
        reading = attribution.aggregate([private], dt.date(2026, 10, 1), dt.date(2026, 10, 29))
        text = str(reading)
        for leak in ('Kuku', 'Sam', 'dog=', 'instagram.com/p', 'createdAt'):
            self.assertNotIn(leak, text)

    def test_the_query_asks_for_no_customer_fields(self):
        import re
        body = attribution.QUERY.split('{', 1)[1]
        words = set(re.findall(r'(?<![$\w])([A-Za-z_]\w*)', re.sub(r'\([^)]*\)', '', body)))
        self.assertEqual(words, {'orders', 'pageInfo', 'hasNextPage', 'endCursor', 'nodes', 'createdAt', 'test', 'cancelledAt',
                                 'tags', 'discountCodes', 'subtotalPriceSet', 'totalRefundedSet', 'shopMoney', 'amount', 'currencyCode',
                                 'customerJourneySummary', 'ready', 'firstVisit', 'lastVisit', 'landingPage', 'referrerUrl',
                                 'source', 'utmParameters', 'medium', 'campaign', 'content'})

    def test_windows_are_trailing_28_days_and_the_last_full_week(self):
        spans = attribution.windows(dt.date(2026, 10, 29))  # a Thursday
        self.assertEqual(spans['trailing_28d'], (dt.date(2026, 10, 1), dt.date(2026, 10, 29)))
        self.assertEqual(spans['last_week'], (dt.date(2026, 10, 19), dt.date(2026, 10, 26)))

    def test_missing_setup_is_a_hold_naming_what_is_missing(self):
        with mock.patch.dict(os.environ, {name: '' for name in attribution.ENV}):
            result = attribution.run(None)
        self.assertEqual(result['status'], 'hold')
        self.assertIn('SHOPIFY_CLIENT_ID', result['reason'])

    def test_a_token_with_extra_scopes_is_refused(self):
        env = {'SHOPIFY_CLIENT_ID': 'id', 'SHOPIFY_CLIENT_SECRET': 'secret'}
        with mock.patch.dict(os.environ, env), mock.patch.object(attribution, 'post', return_value={'access_token': 't', 'scope': 'read_orders,write_orders'}):
            with self.assertRaises(ValueError):
                attribution.access_token('example-store.myshopify.com')
        with mock.patch.dict(os.environ, env), mock.patch.object(attribution, 'post', return_value={'access_token': 't', 'scope': 'read_orders'}):
            self.assertEqual(attribution.access_token('example-store.myshopify.com'), 't')

    def test_a_refusal_shows_shopify_s_error_code_and_never_the_secret(self):
        import io, urllib.error
        body = io.BytesIO(b'{"error": "invalid_client", "error_description": "Client authentication failed"}')
        error = urllib.error.HTTPError('https://example-store.myshopify.com/admin/oauth/access_token', 400, 'Bad Request', {}, body)
        env = {'SHOPIFY_CLIENT_ID': 'id', 'SHOPIFY_CLIENT_SECRET': 'very-secret-value'}
        with mock.patch.dict(os.environ, env), mock.patch('urllib.request.urlopen', side_effect=error) as opened:
            with self.assertRaises(ValueError) as caught:
                attribution.access_token('example-store.myshopify.com')
        self.assertIn('invalid_client', str(caught.exception))
        self.assertNotIn('very-secret-value', str(caught.exception))
        sent = opened.call_args[0][0]
        self.assertEqual(sent.get_header('Content-type'), 'application/x-www-form-urlencoded')

    def test_the_objective_reads_the_stored_window_without_writing(self):
        db = sqlite3.connect(':memory:'); db.row_factory = sqlite3.Row
        self.assertEqual(protocol.organic_orders(db)['availability'], 'missing')
        self.assertIsNone(db.execute("SELECT 1 FROM sqlite_master WHERE name='attribution'").fetchone())
        reading = attribution.aggregate([order(visit(CID))], dt.date(2026, 10, 1), dt.date(2026, 10, 29))
        attribution.store(db, 'trailing_28d', reading, observed_at='2026-10-29T06:00:00+00:00')
        now = dt.datetime(2026, 10, 29, 9, tzinfo=dt.timezone.utc)
        objective = protocol.organic_orders(db, now)
        self.assertEqual((objective['value'], objective['availability']), (1, 'measured'))
        self.assertEqual(protocol.organic_orders(db, now + dt.timedelta(days=3))['availability'], 'stale')

    def test_the_north_star_objective_is_organic_net_sales_over_the_trailing_28_days(self):
        # Control Center reads organic_net_sales_usd from the latest live report (api/_northStarRefresh.ts,
        # HEARTSIDE_ORGANIC_OBJECTIVE): an amount, measured, over 27 to 29 days ending in the last two days.
        db = sqlite3.connect(':memory:'); db.row_factory = sqlite3.Row
        missing = protocol.organic_net_sales(db)
        self.assertEqual((missing['key'], missing['value'], missing['availability']), ('organic_net_sales_usd', None, 'missing'))
        self.assertTrue(missing['reason'])
        self.assertIsNone(protocol.organic_net_sales(None)['value'])
        # Engine-tagged $129, organic social $45, engine-tagged $45.50 less a $0.50 refund; the paid $59 never counts.
        orders = [order(visit(CID), amount='129.00'), order(visit(medium=None, referrer='https://www.tiktok.com/'), amount='45.00'),
                  order(visit(medium=None, referrer='https://l.instagram.com/?u=x'), amount='30.00'),  # unverified
                  order(visit(medium='cpc'), amount='59.00'), order(visit(CID), amount='45.50', refunded='0.50')]
        today = dt.date(2026, 11, 12)
        start, end = attribution.windows(today)['trailing_28d']
        attribution.store(db, 'trailing_28d', attribution.aggregate(orders, start, end), observed_at='2026-11-12T05:00:00+00:00')
        now = dt.datetime(2026, 11, 12, 5, 10, tzinfo=dt.timezone.utc)
        objective = protocol.organic_net_sales(db, now)
        self.assertEqual((objective['value'], objective['unit'], objective['availability'], objective['reason']),
                         (219, 'USD', 'measured', None))
        self.assertIs(type(objective['value']), int)
        span = dt.datetime.fromisoformat(objective['window_end']) - dt.datetime.fromisoformat(objective['window_start'])
        self.assertTrue(dt.timedelta(days=27) <= span <= dt.timedelta(days=29))
        self.assertLessEqual(now - dt.datetime.fromisoformat(objective['window_end']), dt.timedelta(days=2))
        self.assertEqual(protocol.organic_net_sales(db, now + dt.timedelta(days=2))['availability'], 'stale')
        self.assertEqual(db.execute('SELECT count(*) FROM attribution').fetchone()[0], 1)  # read, never written

class DiscountCodeTests(unittest.TestCase):
    # An example registry lives in the tests only; config/codes.json starts empty until Krish switches codes on.
    REGISTRY = {'PRESS301I': 'IG_EMO_C301', 'PRESS': 'TT_EMO_C399'}

    def test_a_registered_code_lands_in_engine_with_its_family(self):
        coded = order(visit(medium=None), discountCodes=['press301i'])
        self.assertEqual(attribution.classify(coded, self.REGISTRY), ('engine', 'IG_EMO_C301'))

    def test_a_coded_order_with_no_journey_still_counts_once_shopify_is_done(self):
        coded = order(None, ready=True, discountCodes=['PRESS301I'])
        self.assertEqual(attribution.classify(coded, self.REGISTRY), ('engine', 'IG_EMO_C301'))

    def test_the_longest_prefix_wins(self):
        self.assertEqual(attribution.classify(order(None, discountCodes=['PRESSX']), self.REGISTRY), ('engine', 'TT_EMO_C399'))

    def test_paid_signals_beat_a_registered_code(self):
        paid = order(visit(CID, medium='paid_social'), discountCodes=['PRESS301I'])
        self.assertEqual(attribution.classify(paid, self.REGISTRY), ('paid', None))
        clicked = order(visit(medium=None, landing='https://heartside.io/?fbclid=1&gclid=abc'), discountCodes=['PRESS301I'])
        self.assertEqual(attribution.classify(clicked, self.REGISTRY), ('paid', None))

    def test_an_unknown_code_falls_through(self):
        social = order(visit(medium=None, referrer='https://www.tiktok.com/'), discountCodes=['WELCOME10'])
        self.assertEqual(attribution.classify(social, self.REGISTRY), ('organic_social', None))
        self.assertEqual(attribution.classify(order(None, discountCodes=['WELCOME10']), self.REGISTRY), ('direct', None))

    def test_the_shipped_registry_is_valid(self):
        # Krish registers real families here, so the shipped file is checked for shape, not for being empty.
        registry = attribution.load_codes()
        for prefix, family in registry.items():
            self.assertTrue(prefix and prefix == prefix.upper())
            self.assertTrue(attribution.FAMILY.match(family), family)

    def test_an_empty_registry_counts_no_code(self):
        import json, tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump({'families': {}}, f)
        try:
            registry = attribution.load_codes(f.name)
            self.assertEqual(registry, {})
            self.assertEqual(attribution.classify(order(None, discountCodes=['PRESS301I']), registry), ('direct', None))
        finally:
            os.unlink(f.name)

    def test_a_bad_family_is_refused(self):
        import json, tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump({'families': {'PRESS': 'not a family'}}, f)
        try:
            with self.assertRaises(ValueError):
                attribution.load_codes(f.name)
        finally:
            os.unlink(f.name)

    def test_aggregate_counts_a_coded_order_under_its_family(self):
        with mock.patch.object(attribution, 'load_codes', return_value=self.REGISTRY):
            reading = attribution.aggregate([order(None, discountCodes=['PRESS301I'])], dt.date(2026, 10, 1), dt.date(2026, 10, 29))
        self.assertEqual(reading['families'], {'IG_EMO_C301': {'orders': 1, 'net_sales': 129.0}})
        self.assertEqual(reading['organic']['orders'], 1)


if __name__ == '__main__':
    unittest.main()
