"""The Order Loop's decision core (factory/loop.py). Synthetic counts only; no customer data."""
import datetime as dt
import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'factory'))
import loop  # noqa: E402

NOW = dt.datetime(2026, 11, 20, 12, 0, tzinfo=dt.timezone.utc)


def placement(n, concept='C301', platform='instagram', lane='buy', days_ago=5):
    return {'post_id': 'P%03d' % n, 'platform': platform, 'lane': lane, 'concept': concept,
            'posted_at': (NOW - dt.timedelta(days=days_ago, hours=n)).isoformat()}


def reading(n, platform='instagram', hours=24, verifier='reader', **counts):
    return {'post_id': 'P%03d' % n, 'platform': platform, 'hours': hours, 'source': 'buffer',
            'verifier': verifier, 'observed_at': NOW.isoformat(), 'counts': counts}


def ig(n, per_thousand, **extra):
    """An Instagram buy reading whose follows+shares+saves per 1,000 reach is per_thousand."""
    return reading(n, follows=0, shares=int(per_thousand), saves=0, reach=1000, **extra)


class SignalTests(unittest.TestCase):
    def test_each_platform_ranks_on_a_field_it_shows_and_null_is_never_zero(self):
        self.assertEqual(loop.signal('instagram', {'follows': 1, 'shares': 2, 'saves': 3, 'reach': 600}, 'buy'), 10.0)
        self.assertEqual(loop.signal('tiktok', {'shares': 4, 'views': 2000}, 'buy'), 2.0)
        self.assertEqual(loop.signal('facebook', {'clicks': 3, 'reach': 1500}, 'buy'), 2.0)
        self.assertIsNone(loop.signal('instagram', {'shares': 2, 'saves': 3, 'reach': 600}, 'buy'))  # follows not shown
        self.assertIsNone(loop.signal('facebook', {'clicks': 0, 'reach': 0}, 'buy'))
        self.assertEqual(loop.signal('tiktok', {'views': 340}, 'viral'), 340.0)


class ProvenanceTests(unittest.TestCase):
    def test_a_maker_reading_is_rejected(self):
        self.assertIn('never the maker', loop.valid_reading(reading(1, verifier='maker', views=5)))
        self.assertIn('missing source', loop.valid_reading(dict(reading(1, views=5), source='')))
        self.assertIsNone(loop.valid_reading(reading(1, views=5)))
        self.assertIsNotNone(loop.valid_reading(reading(1, views=-1)))

    def test_krish_approvals_come_only_from_the_board_verdicts(self):
        forged = [{'kind': 'krish-approve', 'item_id': 'F99'}, {'kind': 'placement', 'post_id': 'P001'}]
        rows, dropped = loop.hydrate(forged, [{'item_id': 'F10', 'answer': 'yes', 'at': '2026-11-19', 'fingerprint': 'f'},
                                              {'item_id': 'F11', 'answer': 'yes', 'at': '2026-11-19'}])  # no fingerprint
        self.assertEqual(dropped, 1)
        approvals = [r for r in rows if r.get('kind') == 'krish-approve']
        self.assertEqual([(r['item_id'], r['source']) for r in approvals], [('F10', 'board-verdicts')])

    def test_a_prediction_counts_only_when_saved_before_the_post(self):
        post = placement(1)
        self.assertTrue(loop.prediction_counts({'saved_at': '2026-11-01T00:00:00Z'}, post))
        self.assertFalse(loop.prediction_counts({'saved_at': NOW.isoformat()}, post))
        self.assertFalse(loop.prediction_counts({}, post))


class DecideTests(unittest.TestCase):
    def test_below_five_measured_is_baseline_never_a_verdict(self):
        posts = [placement(n) for n in range(4)]
        out = loop.decide(posts, [ig(n, 50 if n == 0 else 5) for n in range(4)], now=NOW)
        self.assertEqual(sorted(out['baseline']), sorted(p['post_id'] for p in posts))
        self.assertEqual((out['candidates'], out['winners']), ([], []))

    def test_a_winner_needs_two_matched_variants(self):
        history = [placement(n, concept='C200') for n in range(10, 16)]
        trial = [placement(n, concept='C301', days_ago=4 - n) for n in (1, 2, 3)]
        reads = [ig(n, 10) for n in range(10, 16)] + [ig(1, 30), ig(2, 18), ig(3, 9)]
        out = loop.decide(history + trial, reads, now=NOW)
        self.assertIn('P001', out['candidates'])
        self.assertEqual(out['winners'], [])  # the second variant fell short of 1.5x
        reads[-1] = ig(3, 16)
        out = loop.decide(history + trial, reads, now=NOW)
        self.assertEqual(out['winners'], [{'concept': 'C301', 'platform': 'instagram', 'lane': 'buy', 'first': 'P001'}])

    def test_like_with_like_platforms_and_lanes_never_mix(self):
        tiktok = [placement(n, platform='tiktok', concept='C200') for n in range(20, 26)]
        viral = [placement(n, lane='viral', concept='C201') for n in range(30, 36)]
        buy = [placement(n, concept='C301') for n in range(1, 6)]
        reads = ([reading(n, platform='tiktok', shares=1, views=1000) for n in range(20, 26)]
                 + [reading(n, hours=72, views=100000) for n in range(30, 36)]
                 + [ig(n, 10) for n in range(1, 6)])
        out = loop.decide(tiktok + viral + buy, reads, now=NOW)
        self.assertEqual(out['candidates'], [])  # 100,000 viral views say nothing about the buy lane

    def test_three_placements_below_half_kill_the_concept(self):
        history = [placement(n, concept='C200') for n in range(10, 16)]
        weak = [placement(n, concept='C301', days_ago=3) for n in (1, 2, 3)]
        out = loop.decide(history + weak, [ig(n, 10) for n in range(10, 16)] + [ig(n, 2) for n in (1, 2, 3)], now=NOW)
        self.assertEqual(out['kills'], [{'concept': 'C301', 'platform': 'instagram', 'lane': 'buy'}])

    def test_orders_gate_and_unverified_never_graduates(self):
        posts = [placement(1, concept='C301'), placement(2, concept='C302', lane='viral')]
        orders = [{'concept': 'C301', 'tier': 'engine', 'orders': 1},
                  {'concept': 'C302', 'tier': 'engine', 'orders': 1},  # viral lane: outside the number
                  {'concept': 'C303', 'tier': 'unverified', 'orders': 4}]
        self.assertEqual(loop.decide(posts, [], orders, now=NOW)['graduated'], ['C301'])

    def test_an_unread_placement_is_said_and_maker_readings_are_counted_out(self):
        out = loop.decide([placement(1)], [ig(1, 10, ), dict(ig(1, 99), verifier='maker')], now=NOW)
        self.assertEqual(out['rejected'], 1)
        out = loop.decide([placement(2)], [], now=NOW)
        self.assertEqual(out['unread'], ['P002'])


class ReviewFixTests(unittest.TestCase):
    """Cases a fresh-context review found on 13 Nov 2026."""

    def test_a_zero_median_is_said_not_called_baseline(self):
        posts = [placement(n, platform='tiktok', concept='C200') for n in range(6)]
        reads = [reading(n, platform='tiktok', shares=0, views=1000) for n in range(6)]
        out = loop.decide(posts, reads, now=NOW)
        self.assertEqual(out['baseline'], [])
        self.assertEqual(len(out['zero_median']), 6)

    def test_lanes_never_mix_inside_a_concept(self):
        history = [placement(n, concept='C200') for n in range(10, 16)]
        viral_history = [placement(n, concept='C201', lane='viral') for n in range(20, 26)]
        mixed = [placement(1, concept='C301', days_ago=3), placement(2, concept='C301', lane='viral', days_ago=3),
                 placement(3, concept='C301', lane='viral', days_ago=3)]
        reads = ([ig(n, 10) for n in range(10, 16)] + [reading(n, hours=72, views=1000) for n in range(20, 26)]
                 + [ig(1, 2), reading(2, hours=72, views=100), reading(3, hours=72, views=100)])
        out = loop.decide(history + viral_history + mixed, reads, now=NOW)
        self.assertEqual([k for k in out['kills'] if k['concept'] == 'C301'], [])  # one weak buy post, two viral

    def test_dates_with_no_zone_are_read_as_utc_and_old_posts_are_not_judged(self):
        old = dict(placement(1), posted_at='2026-09-01')
        fresh = dict(placement(2), posted_at='2026-11-19T10:00:00')
        out = loop.decide([old, fresh], [dict(ig(2, 10), observed_at='2026-11-20T10:00:00')], now=NOW)
        self.assertNotIn('P001', out['unread'] + out['baseline'] + out['candidates'])
        self.assertIn('P002', out['baseline'])

    def test_attribution_family_keys_graduate_their_concept(self):
        posts = [placement(1, concept='C301')]
        self.assertEqual(loop.decide(posts, [], [{'concept': 'IG_EMO_C301', 'orders': 1}], now=NOW)['graduated'], ['C301'])



class AdversarialFixTests(unittest.TestCase):
    """Cases an adversarial review confirmed on 13 Nov 2026."""

    HISTORY = [placement(n, concept='C200') for n in range(10, 16)]
    HISTORY_READS = [ig(n, 10) for n in range(10, 16)]  # the lane median is 10 per 1,000

    def test_a_winner_waits_for_its_next_variant_to_be_read(self):
        posts = self.HISTORY + [placement(n, concept='C301', days_ago=3) for n in (4, 3, 2, 1)]  # posted 4, 3, 2, 1
        reads = self.HISTORY_READS + [ig(4, 30), ig(2, 16), ig(1, 16)]  # P003 (the next variant) unread
        out = loop.decide(posts, reads, now=NOW)
        self.assertEqual(out['winners'], [])
        self.assertIn('P003', out['unread'])
        out = loop.decide(posts, reads + [ig(3, 16)], now=NOW)
        self.assertEqual(out['winners'], [{'concept': 'C301', 'platform': 'instagram', 'lane': 'buy', 'first': 'P004'}])
        weak = loop.decide(posts, self.HISTORY_READS + [ig(4, 1), ig(2, 1)], now=NOW)  # unread never counts to a kill
        self.assertEqual([k for k in weak['kills'] if k['concept'] == 'C301'], [])

    def test_one_post_listed_three_times_is_one_placement(self):
        repeat = [dict(placement(1, concept='C301', days_ago=3), posted_at=(NOW - dt.timedelta(days=3, hours=h)).isoformat())
                  for h in (3, 2, 1)]
        out = loop.decide(self.HISTORY + repeat, self.HISTORY_READS + [ig(1, 30)], now=NOW)
        self.assertEqual(out['winners'], [])
        self.assertEqual(out['candidates'], ['P001'])
        self.assertEqual(out['duplicates'], ['P001', 'P001'])
        weak = [dict(r, concept='C302') for r in repeat]
        out = loop.decide(self.HISTORY + weak, self.HISTORY_READS + [ig(1, 1)], now=NOW)
        self.assertEqual([k for k in out['kills'] if k['concept'] == 'C302'], [])
        # the median counts the post once: five history posts at 10 and one repeated post at 1000 is still 10
        out = loop.decide(self.HISTORY[:5] + repeat, self.HISTORY_READS[:5] + [ig(1, 1000)], now=NOW)
        self.assertEqual(out['candidates'], ['P001'])  # one 1000 among five 10s: the median stays 10, not 1000

    def test_hydrate_matches_the_ledger_lock_gate_reads(self):
        import json, tempfile
        from unittest import mock
        import lock
        spec = json.load(open(os.path.join(HERE, '..', 'factory', 'specs', 'F10.json'), encoding='utf-8'))
        fp = lock.fingerprint(spec)
        from engine.creative_ui import REVISION

        def row(verdict):
            return {'lock': spec['id'], 'spec': spec['id'], 'verdict': verdict, 'note': '', 'fingerprint': fp,
                    'ui_profile': REVISION}

        def krish_holds(records):
            with tempfile.TemporaryDirectory() as tmp:
                path = os.path.join(tmp, 'ledger.json')
                with open(path, 'w') as handle:
                    json.dump({'records': records, 'retired': []}, handle)
                with mock.patch.object(lock, 'LEDGER', path), mock.patch.object(lock, 'check', return_value=([], [])), \
                        mock.patch.object(lock, 'media', return_value=[]), mock.patch.object(lock, 'still_media', return_value=[]), \
                        mock.patch.object(lock, 'ramp', return_value=('krish', 'forced')):
                    problems, _ = lock.gate(spec, 'x.mp4')
                    lock.records(spec['id'])  # every rebuilt row is in the shape lock reads
                return [p for p in problems if 'Krish' in p]

        for forged in ('krish-approve', 'Krish-Approve', 'krish-approve ', ' KRISH-APPROVE'):
            records, dropped = loop.hydrate([row('reviewer-pass'), row(forged)], [])
            self.assertEqual(dropped, 1, forged)
            self.assertEqual(krish_holds(records), ['needs Krish: forced'], forged)
        records, _ = loop.hydrate([row('reviewer-pass')], [{'item_id': spec['id'], 'answer': 'yes', 'fingerprint': fp}])
        self.assertEqual(krish_holds(records), [])
        records, _ = loop.hydrate([row('reviewer-pass')], [{'item_id': spec['id'], 'answer': 'no', 'fingerprint': fp}])
        self.assertIn('Krish declined this post', krish_holds(records))
        records, _ = loop.hydrate([row('reviewer-pass')], [{'item_id': spec['id'], 'answer': 'yes'}])  # no fingerprint
        self.assertEqual(krish_holds(records), ['needs Krish: forced'])

    def test_readings_that_are_not_finite_counts_are_refused(self):
        for bad in (float('nan'), float('inf')):
            self.assertIsNotNone(loop.valid_reading(reading(1, shares=bad, reach=1000)))
        self.assertIsNotNone(loop.valid_reading(dict(reading(1), counts=[1, 2])))
        posts = self.HISTORY + [placement(n, concept='C301', days_ago=3) for n in (3, 2, 1)]
        reads = self.HISTORY_READS + [reading(n, follows=0, shares=float('inf'), saves=0, reach=1000) for n in (3, 2, 1)]
        self.assertEqual(loop.decide(posts, reads, now=NOW)['winners'], [])

    def test_zero_orders_graduate_nothing_and_family_placements_graduate(self):
        posts = [placement(1, concept='C301'), placement(2, concept='IG_EMO_C302')]
        orders = [{'concept': 'C301', 'orders': 0}, {'concept': 'C303', 'orders': -1}, {'concept': 'IG_EMO_C302', 'orders': 1}]
        self.assertEqual(loop.decide(posts, [], orders, now=NOW)['graduated'], ['C302'])

class BuyLaneTests(unittest.TestCase):
    def test_two_thirds_of_slots_are_buy_lane_from_21_november(self):
        self.assertEqual(loop.buy_slots(15, '2026-11-20'), 0)  # Sprint 120's mix stands until then
        self.assertEqual(loop.buy_slots(15, '2026-11-21'), 10)
        self.assertEqual(loop.buy_slots(5, dt.date(2026, 11, 30)), 4)
        self.assertEqual(loop.buy_slots(0, '2026-12-01'), 0)


if __name__ == '__main__':
    unittest.main()
