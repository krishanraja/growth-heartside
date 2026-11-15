"""The boost audit: what each paid boost did against Krish's rules, with how much of it is actually known.

Ruling (Krish, 2026-11-15): "Evaluate Claude Ads for advertising account audits, campaign diagnostics, channel
performance analysis and evidence-based optimisation proposals. Integrate only functionality that adds measurable
value beyond the existing system." Read-only evaluation of claude-ads at fc3908e (github.com/AgriciDaniel/claude-ads,
MIT, (c) 2026 Daniel Agrici): its Meta audit is 72 checks a model marks by judgement, with no code that reads the
data, no boost or organic support, and skills that contemplate applying changes. What it adds here is its method,
re-implemented, not its code or its skills:

- every check ends pass, fail, unknown or not applicable, with severity, observation, rule and action;
- severity weights critical 5, high 3, medium 1, informational 0; an unknown lowers evidence coverage and never the
  health score; not applicable leaves both;
- evidence coverage of 80% or more is normal, 60% provisional, and below that no health score is shown at all.

Every check below is computed from recorded aggregates, so the same records always give the same report, and each
names the ruling it enforces. Inputs: the `boost` records Codex read in Krish's Ads Manager (engine/social.py) and an
optional aggregate traffic file (sessions by referrer, read in Shopify analytics). Nothing here reads or writes an ad
account, and every action it prints is a proposal for Krish's Yes (AGENTS.md rule 1; docs/PAID-BOOSTS.md).
"""
import datetime as dt
import json
import math
import statistics
from urllib.parse import parse_qs, urlparse

from . import attribution
from .social import boost_verdict, when

WEIGHTS = {'critical': 5, 'high': 3, 'medium': 1, 'informational': 0}
NORMAL_COVERAGE, PROVISIONAL_COVERAGE = 80.0, 60.0
# Ruling (Krish, 2026-11-10), on the review board: boosts of up to $20 a day, one post at a time, each proved by
# that post's organic reach results. Boosts before it ran under the 4 Nov $250 test (docs/PAID-BOOSTS.md).
CAP_FROM = dt.datetime(2026, 11, 10, tzinfo=dt.timezone.utc)
CAP_USD_PER_DAY = 20
# The engine's burst rule, a test assumption like insights.decisions' pilot thresholds, never a platform benchmark:
# a period is a burst when its sessions a day are at least 5 times the channel's rate outside the recorded periods
# and at least 10 a day.
BURST_MULTIPLE, BURST_MIN_PER_DAY = 5, 10
META_CHANNELS = {'facebook': 'meta', 'instagram': 'meta', 'tiktok': 'tiktok'}

CHECKS = {
    'HS-B01': ('critical', 'Approved before money moved',
               "A boost is never placed without Krish's Yes on that exact boost (AGENTS.md; docs/PAID-BOOSTS.md)."),
    'HS-B02': ('critical', 'Within $20 a day',
               'Ruling (Krish, 2026-11-10): boosts of up to $20 a day, one post at a time.'),
    'HS-B03': ('high', 'On Meta until Meta has a winner',
               'docs/PAID-BOOSTS.md: TikTok Spark Ads follow once a Meta boost has won.'),
    'HS-B04': ('high', 'Landing page views objective',
               'docs/PAID-BOOSTS.md: Ads Manager with a landing-page-views objective, never the Boost button.'),
    'HS-B05': ('high', 'Paid-tagged link to a product page',
               'docs/PAID-BOOSTS.md gate 3: heartside.io/products/<product> with utm_medium=paid_social and the '
               "post's creative_id as utm_content."),
    'HS-B06': ('high', 'Organic proof recorded before the boost',
               "Ruling (Krish, 2026-11-10): each boost proved by that post's organic reach results."),
    'HS-B07': ('critical', 'Paid visits kept out of the organic number',
               'docs/PAID-BOOSTS.md: META_UNVERIFIED is True for a Meta boost\'s window (engine/attribution.py).'),
    'HS-B08': ('medium', 'Read after the boost ended',
               'A reading taken while the boost still ran is partial: read it again after its window.'),
    'HS-B09': ('high', 'Bought buying intent, not reach',
               'engine/social.py boost_verdict: add to cart, checkout or purchase per paid visit, never reach.'),
    'HS-A01': ('critical', 'Every traffic burst has a boost record',
               '15 Nov audit: Facebook traffic with no boost in the record is "paid or not unknown" until Codex reads '
               'Ads Manager (docs/audits/2026-11-15-interest-vs-paid.md).'),
}


def finding(check, status, observation, action=None, subject=None):
    severity, name, rule = CHECKS[check]
    out = {'check': check, 'name': name, 'severity': severity, 'status': status, 'observation': observation, 'rule': rule}
    if subject:
        out['subject'] = subject
    if action and status in ('fail', 'unknown'):
        out['action'] = action
    return out


def days(start, end):
    return max(1, math.ceil((when(end) - when(start)).total_seconds() / 86400))


def ratio(a, b, places=2):
    return round(a / b, places) if a is not None and b else None


def check_boost(b, now, meta_unverified, earlier_winner):
    url = b['post_url']
    start, end = when(b['window_start']), when(b['window_end'])
    counted = b.get('status') == 'counted'
    after_ruling = start >= CAP_FROM
    out = []

    words = ((b.get('approval') or {}).get('words') or '').strip()
    out.append(finding('HS-B01', 'pass' if words else 'unknown',
                       f'approval recorded: "{words[:120]}"' if words else 'no approval named on the record',
                       "Record Krish's words that approved this boost (review board item, CHANGES.md line) in the record's approval field.", url))

    if not after_ruling:
        out.append(finding('HS-B02', 'n/a', 'placed before the $20 a day ruling of 10 Nov', subject=url))
    elif not counted:
        out.append(finding('HS-B02', 'unknown', 'spend not read', 'Codex reads the spend in Ads Manager.', url))
    else:
        per_day = b['spend_usd'] / days(b['window_start'], b['window_end'])
        out.append(finding('HS-B02', 'pass' if per_day <= CAP_USD_PER_DAY else 'fail',
                           f'${b["spend_usd"]:.2f} over {days(b["window_start"], b["window_end"])} day(s): ${per_day:.2f} a day',
                           f'Propose to Krish: hold further spend on this post; a boost above ${CAP_USD_PER_DAY} a day needs his Yes on that amount.', url))

    if b['platform'] == 'meta':
        out.append(finding('HS-B03', 'pass', 'Meta', subject=url))
    else:
        out.append(finding('HS-B03', 'pass' if earlier_winner else 'fail',
                           'TikTok, after a Meta boost bought buying intent' if earlier_winner else 'TikTok, with no Meta winner before it',
                           'Propose to Krish: no TikTok promotion until a Meta boost has shown buying intent, or his ruling that changes it.', url))

    objective = b.get('objective')
    if objective is None:
        out.append(finding('HS-B04', 'unknown', 'objective not recorded', 'Codex reads the campaign objective in Ads Manager.', url))
    else:
        out.append(finding('HS-B04', 'pass' if objective == 'landing_page_views' else 'fail', f'objective: {objective}',
                           'Propose to Krish: the next boost of this post runs on landing page views, from Ads Manager.', url))

    dest = b.get('destination_url')
    if not dest:
        out.append(finding('HS-B05', 'unknown', 'destination not recorded', "Codex reads the Shop now button's website URL.", url))
    else:
        parsed = urlparse(dest)
        query = {k: v[-1] for k, v in parse_qs(parsed.query).items()}
        problems = []
        if parsed.scheme != 'https' or (parsed.hostname or '').removeprefix('www.') != 'heartside.io':
            problems.append('not heartside.io')
        if not parsed.path.startswith('/products/'):
            problems.append('not a product page')
        if query.get('utm_medium') != 'paid_social':
            problems.append('no utm_medium=paid_social')
        if b.get('creative_id') and query.get('utm_content') != b['creative_id']:
            problems.append(f"utm_content is not {b['creative_id']}")
        elif not query.get('utm_content'):
            problems.append('no utm_content')
        out.append(finding('HS-B05', 'fail' if problems else 'pass',
                           ('; '.join(problems) if problems else 'paid-tagged product page') + f': {parsed.path}',
                           'Propose to Krish: correct the Shop now link before any further spend, so paid sales stay out of the organic number.', url))

    proof = b.get('organic_before')
    if not after_ruling:
        out.append(finding('HS-B06', 'n/a', 'placed before the 10 Nov proof ruling', subject=url))
    elif isinstance(proof, dict) and any(isinstance(proof.get(k), (int, float)) for k in ('views', 'reach')):
        seen = proof.get('views', proof.get('reach'))
        acts = sum(proof.get(k) or 0 for k in ('shares', 'saves', 'sends'))
        out.append(finding('HS-B06', 'pass', f'organic before: {seen} viewed, {acts} shares, saves or sends', subject=url))
    else:
        out.append(finding('HS-B06', 'unknown', 'no organic reading before the boost on the record',
                           "Record the post's organic views and shares or saves at the moment the boost was proposed.", url))

    if b['platform'] != 'meta' or not start <= now <= end:
        out.append(finding('HS-B07', 'n/a', 'no Meta boost running now', subject=url))
    else:
        out.append(finding('HS-B07', 'pass' if meta_unverified else 'fail',
                           f'Meta boost running until {end:%Y-%m-%d %H:%M} UTC; META_UNVERIFIED is {meta_unverified}',
                           'Set META_UNVERIFIED = True in engine/attribution.py for this window, in the change that records the Yes.', url))

    read_at = when(b['at'])
    if not counted:
        out.append(finding('HS-B08', 'n/a', 'no results read yet (HS-B09 carries it)', subject=url))
    else:
        out.append(finding('HS-B08', 'pass' if read_at >= end else 'unknown',
                           f'read {read_at:%Y-%m-%d %H:%M} UTC, window ended {end:%Y-%m-%d %H:%M} UTC',
                           f'Codex reads it again after {end:%Y-%m-%d %H:%M} UTC.', url))

    verdict = boost_verdict(b)
    status = {'worth_testing_again': 'pass', 'reach_without_interest': 'fail'}.get(verdict['verdict'], 'unknown')
    out.append(finding('HS-B09', status, f"{verdict['verdict']}: {verdict['why']}",
                       {'fail': 'Propose to Krish: no more spend on this post; the next boost goes to a post with organic sends or saves.',
                        'unknown': 'Wait for enough paid visits, or for the Ads Manager reading.'}.get(status), url))
    return out


def read_traffic(doc):
    """An aggregate sessions file: no visitor, order or customer, only counts by channel and period."""
    if not isinstance(doc, dict) or set(doc) - {'source', 'read_at', 'window', 'channels', 'periods'}:
        raise ValueError('traffic uses source, read_at, window, channels and periods only')
    for key in ('source', 'read_at', 'window', 'channels', 'periods'):
        if key not in doc:
            raise ValueError(f'traffic needs {key}')
    when(doc['read_at'])
    span = doc['window']
    start, end = dt.date.fromisoformat(span['start']), dt.date.fromisoformat(span['end'])
    for name, row in doc['channels'].items():
        if name not in META_CHANNELS or set(row) - {'sessions', 'cart_adds'} or not all(isinstance(v, int) and v >= 0 for v in row.values()):
            raise ValueError(f'channel {name}: whole sessions and cart_adds on facebook, instagram or tiktok only')
    for p in doc['periods']:
        if set(p) - {'channel', 'start', 'end', 'sessions', 'cart_adds', 'landing'} or p.get('channel') not in doc['channels']:
            raise ValueError('a period names a channel in channels, its start, end, sessions and optional cart_adds and landing')
        s, e = dt.date.fromisoformat(p['start']), dt.date.fromisoformat(p['end'])
        if not start <= s <= e <= end or not isinstance(p['sessions'], int) or p['sessions'] < 0:
            raise ValueError('a period sits inside the window and carries whole sessions')
    return doc


def check_traffic(doc, boosts):
    out = []
    window_days = (dt.date.fromisoformat(doc['window']['end']) - dt.date.fromisoformat(doc['window']['start'])).days + 1
    for channel, total in doc['channels'].items():
        periods = [p for p in doc['periods'] if p['channel'] == channel]
        inside = sum(p['sessions'] for p in periods)
        inside_days = sum((dt.date.fromisoformat(p['end']) - dt.date.fromisoformat(p['start'])).days + 1 for p in periods)
        rest_days = window_days - inside_days
        baseline = (total['sessions'] - inside) / rest_days if rest_days > 0 else None
        for p in periods:
            n = (dt.date.fromisoformat(p['end']) - dt.date.fromisoformat(p['start'])).days + 1
            rate = p['sessions'] / n
            subject = f"{channel} {p['start']} to {p['end']}"
            if baseline is None:
                out.append(finding('HS-A01', 'unknown', f'{subject}: {p["sessions"]} sessions, no days outside the periods to compare',
                                   'Read the channel for the whole window, not only the bursts.', subject))
                continue
            if rate < max(BURST_MULTIPLE * baseline, BURST_MIN_PER_DAY):
                out.append(finding('HS-A01', 'n/a', f'{subject}: {rate:.1f} sessions a day, not a burst (baseline {baseline:.2f} a day)', subject=subject))
                continue
            s, e = dt.date.fromisoformat(p['start']), dt.date.fromisoformat(p['end'])
            covering = [b for b in boosts if b['platform'] == META_CHANNELS[channel]
                        and when(b['window_start']).date() <= e and when(b['window_end']).date() >= s]
            carts = p.get('cart_adds')
            seen = (f'{subject}: {p["sessions"]} sessions ({rate:.1f} a day against {baseline:.2f} outside the periods)'
                    + (f', {carts} cart adds' if carts is not None else '') + (f', landing {p["landing"]}' if p.get('landing') else ''))
            out.append(finding('HS-A01', 'pass' if covering else 'fail',
                               seen + (f"; boost on record: {covering[0]['post_url']}" if covering else '; no boost on record'),
                               'Codex reads Ads Manager and every Boost history for these dates, read only; until then this '
                               'traffic is "paid or not unknown" and no channel is judged on it.', subject))
    return out


def diagnostics(boosts):
    """Each counted boost's own numbers, and each against the median of the others: own history, never a benchmark."""
    rows = []
    for b in boosts:
        if b.get('status') != 'counted':
            continue
        r, spend = b['results'], b['spend_usd']
        visits = r.get('landing_page_views') or r.get('link_clicks')
        intent = sum(r.get(k) or 0 for k in ('add_to_cart', 'checkouts', 'purchases'))
        rows.append({'post_url': b['post_url'], 'creative_id': b.get('creative_id'), 'spend_usd': spend,
                     'spend_per_day_usd': round(spend / days(b['window_start'], b['window_end']), 2),
                     'cost_per_visit_usd': ratio(spend, visits), 'landing_per_click': ratio(r.get('landing_page_views'), r.get('link_clicks')),
                     'frequency': ratio(r.get('impressions'), r.get('reach')),
                     'hook_rate': ratio(r.get('video_views_3s'), r.get('impressions'), 3),
                     'cost_per_1000_reached_usd': ratio(spend * 1000, r.get('reach')),
                     'intent_actions': intent, 'cost_per_intent_usd': ratio(spend, intent)})
    keys = ('cost_per_visit_usd', 'landing_per_click', 'frequency', 'hook_rate', 'cost_per_1000_reached_usd')
    for row in rows:
        others = [o for o in rows if o is not row]
        row['vs_median_of_others'] = {k: ratio(row[k], statistics.median([o[k] for o in others if o[k] is not None]))
                                      for k in keys if row[k] is not None and any(o[k] is not None for o in others)}
    return rows


def score(findings):
    """claude-ads' scoring method: unknowns lower coverage, never health; not applicable leaves both."""
    applicable = [f for f in findings if f['status'] != 'n/a']
    known = [f for f in applicable if f['status'] in ('pass', 'fail')]
    weight = lambda fs: sum(WEIGHTS[f['severity']] for f in fs)
    coverage = round(100 * weight(known) / weight(applicable), 1) if weight(applicable) else 0.0
    status = 'normal' if coverage >= NORMAL_COVERAGE else 'provisional' if coverage >= PROVISIONAL_COVERAGE else 'insufficient_evidence'
    health = round(100 * weight([f for f in known if f['status'] == 'pass']) / weight(known), 1) if weight(known) else None
    return {'health_score': None if status == 'insufficient_evidence' else health, 'evidence_coverage': coverage, 'status': status,
            'counts': {s: sum(f['status'] == s for f in findings) for s in ('pass', 'fail', 'unknown', 'n/a')}}


def audit(boosts, traffic=None, now=None, meta_unverified=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    meta_unverified = attribution.META_UNVERIFIED if meta_unverified is None else meta_unverified
    ordered = sorted(boosts, key=lambda b: b['window_start'])
    findings = []
    for i, b in enumerate(ordered):
        winner = any(e['platform'] == 'meta' and boost_verdict(e)['verdict'] == 'worth_testing_again'
                     and when(e['window_end']) <= when(b['window_start']) for e in ordered[:i])
        findings += check_boost(b, now, meta_unverified, winner)
    if traffic is not None:
        findings += check_traffic(read_traffic(traffic), ordered)
    order = {'critical': 0, 'high': 1, 'medium': 2, 'informational': 3}
    proposals = [{'check': f['check'], 'subject': f.get('subject'), 'severity': f['severity'], 'action': f['action']}
                 for f in sorted(findings, key=lambda f: (f['status'] != 'fail', order[f['severity']])) if f.get('action')]
    return {'read_at': now.isoformat(), 'boosts': len(ordered), 'score': score(findings), 'findings': findings,
            'diagnostics': diagnostics(ordered), 'proposals': proposals,
            'policy': {'cap_usd_per_day': CAP_USD_PER_DAY, 'cap_from': CAP_FROM.date().isoformat(),
                       'burst_multiple': BURST_MULTIPLE, 'burst_min_per_day': BURST_MIN_PER_DAY,
                       'coverage_tiers': [NORMAL_COVERAGE, PROVISIONAL_COVERAGE], 'severity_weights': WEIGHTS,
                       'writes_to_ad_accounts': False,
                       'note': 'Burst thresholds are the engine\'s test assumptions; diagnostics compare a boost only with '
                               'Heartside\'s own other boosts. Every action is a proposal for Krish\'s Yes.'}}


def lines(report):
    s = report['score']
    head = (f"Boost audit: {report['boosts']} boost(s); evidence coverage {s['evidence_coverage']}% ({s['status']}); "
            + (f"health {s['health_score']}" if s['health_score'] is not None else 'no health score: too little is known')
            + f"; {s['counts']['fail']} fail, {s['counts']['unknown']} unknown, {s['counts']['pass']} pass")
    out = [head]
    for f in report['findings']:
        if f['status'] != 'n/a':
            out.append(f"  {f['status'].upper():7} {f['check']} {f['name']} ({f['severity']}): {f['observation']}")
    for d in report['diagnostics']:
        out.append(f"  numbers {d['post_url']}: ${d['spend_usd']:.2f}, ${d['spend_per_day_usd']:.2f} a day, "
                   f"cost per visit {d['cost_per_visit_usd']}, landing per click {d['landing_per_click']}, frequency {d['frequency']}, "
                   f"hook rate {d['hook_rate']}, intent actions {d['intent_actions']}"
                   + (f"; against the median of the other boosts {json.dumps(d['vs_median_of_others'])}" if d['vs_median_of_others'] else ''))
    if report['proposals']:
        out.append('Proposals for Krish (none is acted on before his Yes):')
        out += [f"  [{p['severity']}] {p['check']} {p['subject'] or ''}: {p['action']}" for p in report['proposals']]
    return out
