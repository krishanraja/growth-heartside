"""Privacy-safe creative observations and conservative, reproducible decisions."""
import datetime as dt
import json
import statistics
from urllib.parse import urlparse

from . import ledger

FIELDS = {'reach', 'views', 'sends', 'saves', 'link_clicks', 'sessions', 'orders', 'net_sales'}
PLATFORMS = {'IG': 'instagram', 'FB': 'facebook', 'TT': 'tiktok', 'PIN': 'pinterest'}


def setup(db):
    db.executescript('''CREATE TABLE IF NOT EXISTS insights(
      creative_id TEXT NOT NULL, revision TEXT NOT NULL, source TEXT NOT NULL,
      observed_at TEXT NOT NULL, published_at TEXT NOT NULL, values_json TEXT NOT NULL,
      PRIMARY KEY(creative_id,revision,source));''')


def import_observation(db, document):
    setup(db)
    expected = {'creative_id', 'revision', 'platform', 'source', 'source_url', 'observed_at', 'published_at', 'attribution', 'values'}
    if set(document) != expected or document['source'] not in {'native', 'shopify_utm'}:
        raise ValueError('use the exact aggregate creative observation schema')
    cid, revision = document['creative_id'], document['revision']
    row = db.execute('SELECT * FROM creatives WHERE creative_id=? AND revision=?', (cid, revision)).fetchone()
    if not row or row['status'] != 'published':
        raise ValueError('insights need a recorded real publication for this exact creative revision')
    if document['platform'] != PLATFORMS.get(cid.split('_')[0]):
        raise ValueError('creative platform mismatch')
    url = urlparse(document['source_url'])
    if url.scheme != 'https' or not url.hostname or url.username or url.password or url.query or url.fragment:
        raise ValueError('use an HTTPS reporting surface URL without credentials or tracking queries')
    hosts = {'native': {'instagram.com', 'www.instagram.com', 'facebook.com', 'www.facebook.com',
                        'business.facebook.com', 'www.tiktok.com', 'tiktok.com', 'www.pinterest.com', 'pinterest.com', 'analytics.pinterest.com'},
             'shopify_utm': {'admin.shopify.com', 'bnf1em-ge.myshopify.com'}}
    if url.hostname not in hosts[document['source']]:
        raise ValueError('source URL is not a known reporting surface')
    observed, published = [dt.datetime.fromisoformat(document[k].replace('Z', '+00:00')) for k in ('observed_at', 'published_at')]
    if not observed.tzinfo or not published.tzinfo or published > observed or observed > dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5):
        raise ValueError('timestamps need offsets and must describe an observed publication')
    values = document['values']
    if not isinstance(values, dict) or not values or set(values) - FIELDS:
        raise ValueError('only allowlisted aggregate creative metrics may be imported')
    clean = {}
    for key, value in values.items():
        if value is None:
            continue
        try:
            number = ledger.Decimal(str(value))
        except Exception:
            raise ValueError('metric must be numeric') from None
        if isinstance(value, bool) or not number.is_finite() or (key != 'net_sales' and (number < 0 or int(number) != number)):
            raise ValueError('counts must be nonnegative integers; money must be finite')
        clean[key] = float(number) if key == 'net_sales' else int(number)
    if not clean:
        raise ValueError('observation has no measured fields')
    if document['source'] == 'native':
        if document['attribution'] != 'none' or {'orders', 'net_sales', 'sessions'} & clean.keys():
            raise ValueError('native attention cannot be credited with Shopify revenue or sessions')
    elif document['attribution'] != cid or not {'orders', 'net_sales', 'sessions'} >= clean.keys():
        raise ValueError('Shopify attribution must be explicitly filtered to the exact utm_content creative ID')
    stamp = observed.astimezone(dt.timezone.utc).isoformat()
    old = db.execute('SELECT * FROM insights WHERE creative_id=? AND revision=? AND source=?', (cid, revision, document['source'])).fetchone()
    payload = ledger.canonical({'source_url': document['source_url'], 'metrics': clean, 'attribution': document['attribution']})
    if old:
        if old['observed_at'] > stamp:
            raise ValueError('older insights cannot overwrite a newer observation')
        if old['observed_at'] == stamp:
            if old['values_json'] != payload:
                raise ValueError('conflicting observations need a later retrieval timestamp')
            return False
        if old['published_at'] != published.astimezone(dt.timezone.utc).isoformat():
            raise ValueError('a publication timestamp cannot change between snapshots')
    with db:
        db.execute('INSERT INTO insights VALUES(?,?,?,?,?,?) ON CONFLICT(creative_id,revision,source) DO UPDATE SET observed_at=excluded.observed_at,values_json=excluded.values_json',
                   (cid, revision, document['source'], stamp, published.astimezone(dt.timezone.utc).isoformat(), payload))
    return True


def decisions(db, now=None):
    """Exploratory replication candidates, never fabricated statistical winners.

Fixed pilot thresholds are hypotheses. Account-wide sales are never allocated to
creatives. Snapshots are not summed. Comparisons use the same platform and age band.
"""
    setup(db)
    now = now or dt.datetime.now(dt.timezone.utc)
    result, eligible = [], []
    rows = db.execute("SELECT * FROM (SELECT *,row_number() OVER (PARTITION BY creative_id ORDER BY updated_at DESC,rowid DESC) AS rank FROM creatives WHERE status='published') WHERE rank=1").fetchall()
    for creative in rows:
        evidence = {row['source']: dict(row) for row in db.execute('SELECT * FROM insights WHERE creative_id=? AND revision=?', (creative['creative_id'], creative['revision']))}
        item = {'creative_id': creative['creative_id'], 'revision': creative['revision'], 'decision': 'hold_missing',
                'reason': 'No current native observation. Missing metrics are not zero.', 'attributed_net_sales': None}
        sales = evidence.get('shopify_utm')
        if sales:
            item['attributed_net_sales'] = json.loads(sales['values_json'])['metrics'].get('net_sales')
            item['attribution_source'] = json.loads(sales['values_json'])['source_url']
            item['attribution_observed_at'] = sales['observed_at']
        native = evidence.get('native')
        if native:
            stamp = dt.datetime.fromisoformat(native['observed_at'])
            age = (stamp - dt.datetime.fromisoformat(native['published_at'])).total_seconds() / 3600
            values = json.loads(native['values_json'])['metrics']
            item.update(observed_at=native['observed_at'], age_hours=round(age, 1), reach=values.get('reach'), sends=values.get('sends'))
            if now - stamp > dt.timedelta(days=7):
                item['reason'] = 'Native observation is over seven days old.'
            elif values.get('reach', 0) < 2000 or age < 48 or values.get('sends') is None:
                item.update(decision='observe', reason='Pilot needs at least 2,000 reached accounts, 48 hours and observed sends.')
            else:
                rate = 1000 * values['sends'] / values['reach']
                item.update(decision='hold', sends_per_1000=round(rate, 2), reason='Eligible observation. Keep testing the creative family.')
                eligible.append((creative['creative_id'].split('_')[0], int(age // 48), rate, item))
        result.append(item)
    for platform, age_band, rate, item in eligible:
        peers = [r for p, a, r, it in eligible if p == platform and a == age_band and it is not item]
        if len(peers) >= 2 and rate >= 10 and rate >= 2 * statistics.median(peers):
            item.update(decision='replicate_candidate', reason='Exploratory pilot candidate: at least 10 sends/1,000 reach and twice the median of two comparable peers. Test a new hook; this does not establish sales causation or statistical significance.')
        elif len(peers) < 2:
            item['reason'] = 'Need two comparable creatives on the same platform in the same 48-hour age band before replication.'
    return {'policy': {'min_reach': 2000, 'min_age_hours': 48, 'freshness_days': 7,
                       'candidate_sends_per_1000': 10, 'peer_multiple': 2, 'automatic_publishing': False},
            'decisions': result, 'note': 'Pilot thresholds are test assumptions. No published creative means no performance verdict.'}
