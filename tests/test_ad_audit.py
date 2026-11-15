"""The boost audit (engine/ad_audit.py): every check computed from recorded aggregates, measured against what the
engine already caught before it existed. Synthetic fixtures only: the repository is public, so no real spend,
post, account or reading appears here."""
import datetime as dt
import unittest

from engine import ad_audit, social

NOW = dt.datetime(2026, 11, 20, 12, 0, tzinfo=dt.timezone.utc)
POST = 'https://www.instagram.com/p/SYNTHETIC1/'
GOOD_LINK = 'https://heartside.io/products/your-dogs-illustrated-mug?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_TEST_C1'


def boost(**extra):
    body = {'kind': 'boost', 'channel': 'instagram', 'at': '2026-11-19T12:00:00Z', 'source': 'synthetic fixture',
            'post_url': POST, 'creative_id': 'IG_TEST_C1', 'platform': 'meta',
            'window_start': '2026-11-16T12:00:00Z', 'window_end': '2026-11-17T12:00:00Z', 'status': 'counted',
            'spend_usd': 20, 'objective': 'landing_page_views', 'destination_url': GOOD_LINK,
            'approval': {'words': 'Yes', 'by': 'Krish', 'date': '2026-11-16', 'where': 'synthetic', 'scope': 'this boost'},
            'organic_before': {'views': 400, 'shares': 3, 'saves': 1},
            'results': {'impressions': 9000, 'reach': 6000, 'video_views_3s': 2700, 'link_clicks': 90,
                        'landing_page_views': 70, 'add_to_cart': 2},
            'evidence': 'synthetic'}
    body.update(extra)
    return social.validate({k: v for k, v in body.items() if v is not None})


def by_check(report, check):
    return [f for f in report['findings'] if f['check'] == check]


class BoostAudit(unittest.TestCase):
    def test_a_clean_boost_passes_every_check_with_normal_coverage(self):
        report = ad_audit.audit([boost()], now=NOW, meta_unverified=False)
        statuses = {f['check']: f['status'] for f in report['findings']}
        self.assertEqual(statuses, {'HS-B01': 'pass', 'HS-B02': 'pass', 'HS-B03': 'pass', 'HS-B04': 'pass', 'HS-B05': 'pass',
                                    'HS-B06': 'pass', 'HS-B07': 'n/a', 'HS-B08': 'pass', 'HS-B09': 'pass'})
        self.assertEqual(report['score']['status'], 'normal')
        self.assertEqual(report['score']['health_score'], 100.0)
        self.assertEqual(report['proposals'], [])
        self.assertFalse(report['policy']['writes_to_ad_accounts'])

    def test_each_seeded_defect_is_caught_and_the_old_verdict_misses_all_of_them(self):
        """The measurable value: six defects the record can show, against what boost_verdict saw before."""
        seeded = {
            'HS-B02': boost(spend_usd=60),                                            # $60 in one day, over the $20 cap
            'HS-B03': boost(platform='tiktok', channel='tiktok', post_url='https://www.tiktok.com/@x/video/1'),
            'HS-B04': boost(objective='engagement'),                                  # bought likes, not visits
            'HS-B05': boost(destination_url='https://heartside.io/?utm_source=meta'),  # home page, no paid tag
            'HS-B07': boost(window_start='2026-11-20T00:00:00Z', window_end='2026-11-21T00:00:00Z', at='2026-11-21T06:00:00Z'),
            'HS-B09': boost(results={'link_clicks': 120, 'landing_page_views': 100}),  # 100 visits, no cart
        }
        caught = 0
        for check, record in seeded.items():
            report = ad_audit.audit([record], now=NOW, meta_unverified=False)
            failed = {f['check'] for f in report['findings'] if f['status'] == 'fail'}
            self.assertIn(check, failed, check)
            caught += check in failed
            self.assertTrue(any(p['check'] == check for p in report['proposals']), f'{check} gives Krish a proposal')
        self.assertEqual(caught, 6)
        # Before: boost_verdict judges only buying intent, so it names one of the six at most.
        old = sum(social.boost_verdict(r)['verdict'] == 'reach_without_interest' for r in seeded.values())
        self.assertEqual(old, 1)

    def test_traffic_burst_with_no_boost_on_record_fails(self):
        traffic = {'source': 'synthetic sessions by referrer', 'read_at': '2026-11-20T10:00:00Z',
                   'window': {'start': '2026-10-22', 'end': '2026-11-20'},
                   'channels': {'facebook': {'sessions': 330, 'cart_adds': 0}},
                   'periods': [{'channel': 'facebook', 'start': '2026-11-16', 'end': '2026-11-17', 'sessions': 100, 'cart_adds': 0},
                               {'channel': 'facebook', 'start': '2026-11-18', 'end': '2026-11-19', 'sessions': 200, 'cart_adds': 0}]}
        report = ad_audit.audit([boost(channel='facebook', post_url='https://www.facebook.com/reel/1')], traffic, now=NOW, meta_unverified=False)
        bursts = by_check(report, 'HS-A01')
        self.assertEqual([f['status'] for f in bursts], ['pass', 'fail'])   # the first sits under the boost's window
        self.assertIn('no boost on record', bursts[1]['observation'])

    def test_a_quiet_period_is_not_a_burst(self):
        traffic = {'source': 's', 'read_at': '2026-11-20T10:00:00Z', 'window': {'start': '2026-11-01', 'end': '2026-11-20'},
                   'channels': {'tiktok': {'sessions': 40}},
                   'periods': [{'channel': 'tiktok', 'start': '2026-11-10', 'end': '2026-11-11', 'sessions': 6}]}
        self.assertEqual(by_check(ad_audit.audit([], traffic, now=NOW), 'HS-A01')[0]['status'], 'n/a')

    def test_unknowns_lower_coverage_and_withhold_the_score(self):
        bare = boost(objective=None, destination_url=None, approval=None, organic_before=None)
        report = ad_audit.audit([bare], now=NOW, meta_unverified=False)
        self.assertEqual(report['score']['status'], 'insufficient_evidence')
        self.assertIsNone(report['score']['health_score'])
        self.assertEqual(report['score']['counts']['unknown'], 4)

    def test_paid_hold_is_checked_only_while_a_meta_boost_runs(self):
        running = boost(window_start='2026-11-20T00:00:00Z', window_end='2026-11-21T00:00:00Z', at='2026-11-20T11:00:00Z')
        held = by_check(ad_audit.audit([running], now=NOW, meta_unverified=True), 'HS-B07')[0]
        self.assertEqual(held['status'], 'pass')
        self.assertEqual(by_check(ad_audit.audit([running], now=NOW, meta_unverified=False), 'HS-B08')[0]['status'], 'unknown')

    def test_before_the_ruling_the_cap_and_proof_do_not_apply(self):
        early = boost(window_start='2026-11-06T12:00:00Z', window_end='2026-11-07T12:00:00Z', at='2026-11-08T00:00:00Z',
                      spend_usd=25, organic_before=None)
        statuses = {f['check']: f['status'] for f in ad_audit.audit([early], now=NOW, meta_unverified=False)['findings']}
        self.assertEqual((statuses['HS-B02'], statuses['HS-B06']), ('n/a', 'n/a'))

    def test_diagnostics_compare_only_with_heartsides_own_boosts(self):
        a = boost()
        b = boost(post_url='https://www.instagram.com/p/SYNTHETIC2/', creative_id='IG_TEST_C2', spend_usd=10,
                  destination_url=GOOD_LINK.replace('IG_TEST_C1', 'IG_TEST_C2'),
                  results={'impressions': 3000, 'reach': 2000, 'link_clicks': 25, 'landing_page_views': 20})
        rows = ad_audit.diagnostics([a, b])
        self.assertEqual(rows[0]['cost_per_visit_usd'], 0.29)
        self.assertEqual(rows[1]['cost_per_visit_usd'], 0.5)
        self.assertEqual(rows[0]['vs_median_of_others']['cost_per_visit_usd'], 0.58)
        self.assertEqual(rows[0]['hook_rate'], 0.3)
        self.assertNotIn('hook_rate', rows[1]['vs_median_of_others'])   # the other boost has no 3 s views

    def test_records_reject_bad_audit_fields(self):
        for bad in ({'objective': 'awareness'}, {'destination_url': 'http://heartside.io/'}, {'approval': 'Yes'}):
            with self.assertRaises(ValueError, msg=str(bad)):
                boost(**bad)

    def test_traffic_file_holds_aggregates_only(self):
        with self.assertRaises(ValueError):
            ad_audit.read_traffic({'source': 's', 'read_at': '2026-11-20T10:00:00Z', 'window': {'start': '2026-11-01', 'end': '2026-11-20'},
                                   'channels': {'facebook': {'sessions': 5, 'visitor_ids': 2}}, 'periods': []})


if __name__ == '__main__':
    unittest.main()
