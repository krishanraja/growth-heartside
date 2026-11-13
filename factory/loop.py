"""The Order Loop's decision core: read, rank and call buy-lane formats from readings the maker never wrote.

Plan (13 Nov 2026, approved by Krish as the build): only the buy lane carries the North Star number, posts that
end on the real product with a counted path. The viral lane builds audience and is never ranked for money.
This module holds the rules as constants; only Krish's ruling changes them. It reads lists and returns
decisions: it writes no file, posts nothing, sends nothing and spends nothing, so a scheduled session may
call it and change no tracked file (AGENTS.md rule 9).

The rules:

1. Like with like. A placement is compared only within its platform and lane, against that platform and lane's
   median over the trailing 14 days. Below MIN_MEASURED placements the answer is "baseline", never a verdict.
2. The buy lane is ranked on a signal each platform actually shows (Buffer's per-post fields, 13 Nov readback):
   Instagram follows, shares and saves per 1,000 reach; TikTok shares per 1,000 views; Facebook clicks per
   1,000 reach. A field the platform did not show is None, never zero; a placement with no signal is unread.
3. Candidate at 24 hours: buy at 2x the lane median; viral at 3x on 72-hour views.
4. Winner: a candidate whose next two variants of the same concept on the same platform each reach 1.5x.
5. Orders gate, never rank. A counted order (engine tier or code) graduates its concept. An unverified order
   (engine/attribution.py) never does.
6. Kill: a concept with three placements each below 0.5x its lane median.
7. Provenance. A reading the maker wrote is rejected: the reader is never the maker. A Krish approval or
   decline is taken only from the board's verdicts, never from a ledger row, because lock.gate trusts the
   local ledger with no provenance check (factory/lock.py).
8. A prediction counts only if it was saved before the placement went live.
"""
import datetime as dt
import statistics

LANES = ('buy', 'viral')
PLATFORMS = ('instagram', 'tiktok', 'facebook')
MIN_MEASURED = 5          # factory/sprint.py MIN_MEASURED: below it, build the baseline
WINDOW_DAYS = 14
CANDIDATE = {'buy': 2.0, 'viral': 3.0}
REPLICATE = 1.5
KILL_BELOW = 0.5
KILL_COUNT = 3
# The buy-lane signal per platform: (numerator fields, denominator field). Only fields Buffer shows.
SIGNAL = {'instagram': (('follows', 'shares', 'saves'), 'reach'),
          'tiktok': (('shares',), 'views'),
          'facebook': (('clicks',), 'reach')}
COUNTED_TIERS = ('engine',)
KRISH_KINDS = ('krish-approve', 'krish-decline')
READER = 'reader'


def _when(value):
    """An aware datetime; a time with no zone, or a bare date, is read as UTC."""
    if not isinstance(value, dt.datetime):
        value = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    return value if value.tzinfo else value.replace(tzinfo=dt.timezone.utc)


def concept_of(key):
    """C301 from C301 or from an attribution family such as IG_EMO_C301."""
    key = str(key or '')
    return key.rsplit('_', 1)[-1] if '_' in key else key


def valid_reading(reading):
    """Why a reading cannot be used, or None. Every reading names its source, its verifier and when it was read."""
    if not isinstance(reading, dict):
        return 'not a reading'
    for key in ('post_id', 'platform', 'source', 'observed_at', 'verifier'):
        if not reading.get(key):
            return 'missing ' + key
    if reading['verifier'] != READER:
        return 'written by ' + str(reading['verifier']) + ', not the reader: the reader is never the maker'
    if reading['platform'] not in PLATFORMS:
        return 'unknown platform ' + str(reading['platform'])
    try:
        _when(reading['observed_at'])
    except (TypeError, ValueError):
        return 'unreadable observed_at'
    for key, value in (reading.get('counts') or {}).items():
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0):
            return 'count ' + key + ' is not a whole number or not shown (None)'
    return None


def signal(platform, counts, lane):
    """The ranking number for one reading: buy lane per 1,000 on the platform's own fields, viral lane its views.
    None when the platform did not show what it needs: null is never zero."""
    counts = counts or {}
    if lane == 'viral':
        views = counts.get('views')
        return float(views) if views is not None else None
    tops, bottom = SIGNAL[platform]
    if counts.get(bottom) in (None, 0) or any(counts.get(k) is None for k in tops):
        return None
    return 1000.0 * sum(counts[k] for k in tops) / counts[bottom]


def latest(readings, hours):
    """The newest valid reading per (post_id, platform) at its `hours` mark (24 or 72), with the rejected count."""
    best, rejected = {}, 0
    for reading in readings:
        if valid_reading(reading):
            rejected += 1
            continue
        if reading.get('hours') != hours:
            continue
        key = (reading['post_id'], reading['platform'])
        if key not in best or _when(reading['observed_at']) > _when(best[key]['observed_at']):
            best[key] = reading
    return best, rejected


def medians(placements, readings, now):
    """{(platform, lane): median or None} over the trailing WINDOW_DAYS; None below MIN_MEASURED."""
    now = _when(now)
    since = now - dt.timedelta(days=WINDOW_DAYS)
    values = {}
    for placement in placements:
        hours = 24 if placement['lane'] == 'buy' else 72
        reading = readings.get(hours, {}).get((placement['post_id'], placement['platform']))
        if not reading or not since <= _when(placement['posted_at']) <= now:
            continue
        value = signal(placement['platform'], reading.get('counts'), placement['lane'])
        if value is not None:
            values.setdefault((placement['platform'], placement['lane']), []).append(value)
    return {key: (statistics.median(v) if len(v) >= MIN_MEASURED else None) for key, v in values.items()}


def concept_orders(orders):
    """{concept: counted orders}; an order counts only in a counted tier, never unverified. Attribution's
    families (IG_EMO_C301) exist only in the engine tier, so a family key with no tier is passed as engine."""
    out = {}
    for order in orders or []:
        tier = order.get('tier', 'engine' if '_' in str(order.get('concept') or '') else None)
        concept = concept_of(order.get('concept'))
        if tier in COUNTED_TIERS and concept:
            out[concept] = out.get(concept, 0) + int(order.get('orders', 1))
    return out


def decide(placements, readings_list, orders=(), now=None):
    """The day's calls: {'baseline', 'candidates', 'winners', 'kills', 'graduated', 'unread', 'rejected'}.

    placements: [{post_id, platform, lane, concept, posted_at}]; readings_list: reader rows with `hours` 24 or 72
    and `counts`; orders: [{concept, tier, orders}] from the runner's attribution families."""
    now = _when(now or dt.datetime.now(dt.timezone.utc))
    at24, rejected = latest(readings_list, 24)
    at72, _ = latest(readings_list, 72)  # the same readings, so their rejections are counted once
    readings = {24: at24, 72: at72}
    lane_median = medians(placements, readings, now)
    out = {'baseline': [], 'zero_median': [], 'candidates': [], 'winners': [], 'kills': [], 'graduated': [],
           'unread': [], 'rejected': rejected}
    ratios = {}
    since = now - dt.timedelta(days=WINDOW_DAYS)
    for placement in sorted(placements, key=lambda p: _when(p['posted_at'])):
        if placement.get('lane') not in LANES or placement.get('platform') not in PLATFORMS:
            out['unread'].append(placement['post_id'])
            continue
        if not since <= _when(placement['posted_at']) <= now:
            continue  # judged against today's median only while it is inside the 14-day window
        hours = 24 if placement['lane'] == 'buy' else 72
        reading = readings[hours].get((placement['post_id'], placement['platform']))
        value = signal(placement['platform'], (reading or {}).get('counts'), placement['lane']) if reading else None
        if value is None:
            out['unread'].append(placement['post_id'])
            continue
        key = (placement['platform'], placement['lane'])
        median = lane_median.get(key)
        if median is None:
            out['baseline'].append(placement['post_id'])
            continue
        if median == 0:
            out['zero_median'].append(placement['post_id'])  # enough posts, but the lane's median is 0: no ratio
            continue
        ratio = value / median
        ratios.setdefault((placement['concept'], placement['platform'], placement['lane']), []).append((placement, ratio))
        if ratio >= CANDIDATE[placement['lane']]:
            out['candidates'].append(placement['post_id'])
    for (concept, platform, lane), rows in ratios.items():
        won = False
        for i, (placement, ratio) in enumerate(rows):
            if ratio < CANDIDATE[lane]:
                continue
            following = rows[i + 1:i + 3]
            if len(following) == 2 and all(r >= REPLICATE for _, r in following):
                out['winners'].append({'concept': concept, 'platform': platform, 'lane': lane,
                                       'first': placement['post_id']})
                won = True
                break
        low = [r for _, r in rows if r < KILL_BELOW]
        if len(low) >= KILL_COUNT and not won:  # a replicated winner is never killed in the same call
            out['kills'].append({'concept': concept, 'platform': platform, 'lane': lane})
    counted = concept_orders(orders)
    buy_concepts = {p['concept'] for p in placements if p.get('lane') == 'buy'}
    out['graduated'] = sorted(c for c in counted if c in buy_concepts)
    return out


def hydrate(ledger_rows, board_verdicts):
    """Ledger rows safe to load into local/: every row except a Krish approval or decline, which is rebuilt only
    from the board's verdicts. Returns (rows, dropped)."""
    rows, dropped = [], 0
    for row in ledger_rows or []:
        if isinstance(row, dict) and row.get('kind') in KRISH_KINDS:
            dropped += 1
            continue
        rows.append(row)
    for verdict in board_verdicts or []:
        if verdict.get('answer') in ('yes', 'no') and verdict.get('item_id'):
            rows.append({'kind': 'krish-approve' if verdict['answer'] == 'yes' else 'krish-decline',
                         'item_id': verdict['item_id'], 'source': 'board-verdicts', 'at': verdict.get('at')})
    return rows, dropped


def prediction_counts(prediction, placement):
    """True only when the prediction was saved before the placement went live."""
    try:
        return _when(prediction['saved_at']) < _when(placement['posted_at'])
    except (KeyError, TypeError, ValueError):
        return False
