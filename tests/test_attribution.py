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


def order(last=None, first=None, amount='129.00', created='2026-10-20T15:00:00Z', ready=True, **kw):
    return {'createdAt': created, 'test': False, 'cancelledAt': None, 'tags': [], 'discountCodes': [],
            'currentSubtotalPriceSet': {'shopMoney': {'amount': amount, 'currencyCode': 'USD'}},
            'customerJourneySummary': {'ready': ready, 'lastVisit': last, 'firstVisit': first}, **kw}


class AttributionTests(unittest.TestCase):
    def test_engine_tags_name_the_post_family(self):
        self.assertEqual(attribution.classify(order(visit(CID))), ('engine', 'IG_EMO_C90'))

    def test_first_visit_from_a_post_still_counts(self):
        self.assertEqual(attribution.classify(order(last=visit(medium=None), first=visit(CID)))[0], 'engine')

    def test_social_referrer_without_tags_is_organic_social(self):
        self.assertEqual(attribution.classify(order(visit(medium=None, referrer='https://l.instagram.com/?u=x')))[0], 'organic_social')

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
                                 'tags', 'discountCodes', 'currentSubtotalPriceSet', 'shopMoney', 'amount', 'currencyCode',
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


if __name__ == '__main__':
    unittest.main()
