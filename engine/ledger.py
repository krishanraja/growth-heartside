"""Transactional local creative history and aggregate metrics. No customer records."""
import datetime as dt
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path
import sqlite3
from urllib.parse import urlparse
from zoneinfo import ZoneInfo


COUNTS = {'orders', 'sessions', 'online_store_visitors', 'sessions_with_cart_additions',
          'sessions_that_reached_checkout', 'sessions_that_completed_checkout'}
MONEY = {'net_sales', 'gross_sales', 'discounts', 'sales_reversals'}
RATES = {'conversion_rate', 'average_order_value'}
TRANSITIONS = {'rendered': {'reviewed', 'approved', 'skipped'},
               'reviewed': {'approved', 'skipped'}, 'approved': {'published', 'skipped'},
               'published': set(), 'skipped': {'reviewed', 'approved'}}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def connect(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=30)
    db.row_factory = sqlite3.Row
    db.executescript('''
      PRAGMA journal_mode=WAL;
      CREATE TABLE IF NOT EXISTS creatives (
        creative_id TEXT NOT NULL, revision TEXT NOT NULL, status TEXT NOT NULL,
        spec TEXT NOT NULL, manifest TEXT NOT NULL, created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL, published_url TEXT,
        PRIMARY KEY (creative_id, revision));
      CREATE TABLE IF NOT EXISTS creative_events (
        id INTEGER PRIMARY KEY, creative_id TEXT NOT NULL, revision TEXT NOT NULL,
        status TEXT NOT NULL, recorded_at TEXT NOT NULL, details TEXT NOT NULL DEFAULT '{}');
      CREATE TABLE IF NOT EXISTS metrics (
        platform TEXT NOT NULL, source TEXT NOT NULL, start TEXT NOT NULL,
        end TEXT NOT NULL, timezone TEXT NOT NULL, observed_at TEXT NOT NULL,
        values_json TEXT NOT NULL, PRIMARY KEY (platform, source, start, end, timezone));
    ''')
    if 'details' not in {row['name'] for row in db.execute('PRAGMA table_info(creative_events)')}:
        db.execute("ALTER TABLE creative_events ADD COLUMN details TEXT NOT NULL DEFAULT '{}'")
        db.commit()
    return db


def record_render(db, creative_id, revision, spec, manifest):
    row = db.execute('SELECT * FROM creatives WHERE creative_id=? AND revision=?',
                     (creative_id, revision)).fetchone()
    spec_json, manifest_json, stamp = canonical(spec), canonical(manifest), now()
    if row and row['manifest'] == manifest_json and row['spec'] == spec_json:
        return False
    with db:
        db.execute('''INSERT INTO creatives VALUES (?, ?, 'rendered', ?, ?, ?, ?, NULL)
          ON CONFLICT(creative_id,revision) DO UPDATE SET
          status='rendered', spec=excluded.spec, manifest=excluded.manifest,
          updated_at=excluded.updated_at, published_url=NULL''',
                   (creative_id, revision, spec_json, manifest_json, stamp, stamp))
        db.execute('INSERT INTO creative_events(creative_id,revision,status,recorded_at) VALUES(?,?,?,?)',
                   (creative_id, revision, 'rendered', stamp))
    return True


def mark(db, creative_id, revision, status, published_url=None):
    row = db.execute('SELECT * FROM creatives WHERE creative_id=? AND revision=?',
                     (creative_id, revision)).fetchone()
    if not row:
        raise ValueError('unknown creative revision')
    if status == row['status'] and published_url == row['published_url']:
        return
    if status not in TRANSITIONS.get(row['status'], set()):
        raise ValueError(f'cannot move {row["status"]} to {status}')
    if status == 'published':
        hosts = {'IG': ('instagram.com', 'www.instagram.com'),
                 'FB': ('facebook.com', 'www.facebook.com'),
                 'TT': ('tiktok.com', 'www.tiktok.com'),
                 'PIN': ('pinterest.com', 'www.pinterest.com'),
                 'YT': ('youtube.com', 'www.youtube.com', 'youtu.be')}
        url = urlparse(published_url or '')
        if url.scheme != 'https' or url.hostname not in hosts.get(creative_id.split('_')[0], ()):
            raise ValueError('record the real HTTPS publication URL on this creative\'s platform')
    elif published_url:
        raise ValueError('published_url belongs only to the published state')
    with db:
        db.execute('UPDATE creatives SET status=?, updated_at=?, published_url=? WHERE creative_id=? AND revision=?',
                   (status, now(), published_url, creative_id, revision))
        db.execute('INSERT INTO creative_events(creative_id,revision,status,recorded_at,details) VALUES(?,?,?,?,?)',
                   (creative_id, revision, status, now(), canonical({'published_url': published_url})))


def shop_domains():
    """Heartside's own store domains. The Shopify store handle is never published (heartside NOW.md
    never_publish), so it comes from the HEARTSIDE_SHOP_DOMAIN repository variable, never from this file."""
    handle = os.environ.get('HEARTSIDE_SHOP_DOMAIN', '').strip().lower()
    return {'heartside.io'} | ({handle} if handle.endswith('.myshopify.com') else set())


def normalize_report(document):
    """Only an ungrouped aggregate tool result or explicit aggregate values."""
    allowed = {'platform', 'scope', 'currency', 'source', 'observed_at', 'period'}
    if not isinstance(document, dict) or set(document) not in (allowed | {'result'}, allowed | {'values'}):
        raise ValueError('import only the exact aggregate envelope; no extra fields or mixed raw payloads')
    period = document['period']
    start, end = dt.date.fromisoformat(period['start']), dt.date.fromisoformat(period['end'])
    if start >= end:
        raise ValueError('period end is exclusive and must follow start')
    ZoneInfo(period['timezone'])
    observed = dt.datetime.fromisoformat(document['observed_at'].replace('Z', '+00:00'))
    if not observed.tzinfo:
        raise ValueError('observed_at needs a UTC offset')
    if document.get('currency') != 'USD' or document.get('platform') != 'shopify':
        raise ValueError('this adapter imports Shopify aggregates in USD only')
    source = document.get('source')
    if not isinstance(source, str) or not source.strip() or len(source) > 500:
        raise ValueError('source must name the report or query')
    if document.get('scope') != 'store':
        raise ValueError('only complete store aggregates are supported; declare scope=store')
    values = document.get('values')
    if 'result' in document:
        result = document['result']
        result = result.get('structuredContent') or result
        if result.get('shopDomain') not in shop_domains():
            raise ValueError('aggregate result is not from Heartside')
        columns, rows = result['columns'], result['rows']
        if len(rows) != 1 or len(rows[0]) != len(columns):
            raise ValueError('import one ungrouped aggregate row at a time')
        values = dict(zip([c['name'] for c in columns], rows[0]))
        if len(values) != len(columns):
            raise ValueError('duplicate metric columns')
    if not isinstance(values, dict) or not values or set(values) - (COUNTS | MONEY | RATES):
        raise ValueError('unsupported fields: import aggregate metrics only, never customer records')
    clean = {}
    for key, value in values.items():
        if value is None:
            continue
        try:
            if isinstance(value, bool):
                raise ValueError('boolean is not a metric')
            number = Decimal(str(value))
            if not number.is_finite():
                raise ValueError('metrics must be finite')
            if key in COUNTS and (number < 0 or number != int(number)):
                raise ValueError('counts must be nonnegative integers')
            if key in RATES and number < 0:
                raise ValueError('rates must be nonnegative')
            clean[key] = int(number) if key in COUNTS else float(number)
        except (InvalidOperation, TypeError):
            raise ValueError(f'{key}: invalid number') from None
    if not clean:
        raise ValueError('no observed metrics to import')
    return {'platform': 'shopify', 'source': source, 'start': start.isoformat(), 'end': end.isoformat(),
            'timezone': period['timezone'], 'observed_at': observed.astimezone(dt.timezone.utc).isoformat(),
            'values': clean}


def import_report(db, document):
    report = normalize_report(document)
    key = tuple(report[k] for k in ('platform', 'source', 'start', 'end', 'timezone'))
    old = db.execute('SELECT observed_at,values_json FROM metrics WHERE platform=? AND source=? AND start=? AND end=? AND timezone=?', key).fetchone()
    values = canonical(report['values'])
    if old and old['observed_at'] > report['observed_at']:
        raise ValueError('an older observation cannot replace a newer report')
    if old and old['observed_at'] == report['observed_at']:
        if old['values_json'] != values:
            raise ValueError('conflicting observations have the same timestamp')
        return False
    with db:
        db.execute('''INSERT INTO metrics VALUES(?,?,?,?,?,?,?)
          ON CONFLICT(platform,source,start,end,timezone) DO UPDATE SET
          observed_at=excluded.observed_at, values_json=excluded.values_json''',
                   (*key, report['observed_at'], values))
    return True


def summary(db, start, end, timezone):
    """Never add overlapping windows, incompatible zones, or rates."""
    first, last = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    if first >= last:
        raise ValueError('end must follow start')
    ZoneInfo(timezone)
    rows = [dict(r) for r in db.execute('SELECT * FROM metrics WHERE start>=? AND end<=? AND timezone=?',
                                      (start, end, timezone))]
    rows.sort(key=lambda r: ((dt.date.fromisoformat(r['end']) - dt.date.fromisoformat(r['start'])).days,
                             r['observed_at']), reverse=True)
    totals, coverage, evidence = {}, {}, {}
    for metric in sorted(COUNTS | MONEY):
        occupied, total, used = set(), Decimal(0), []
        for row in rows:
            values = json.loads(row['values_json'])
            a, b = dt.date.fromisoformat(row['start']), dt.date.fromisoformat(row['end'])
            days = {a + dt.timedelta(days=i) for i in range((b - a).days)}
            if metric not in values or occupied & days:
                continue
            occupied |= days
            total += Decimal(str(values[metric]))
            used.append({k: row[k] for k in ('source', 'start', 'end', 'observed_at')})
        if used:
            totals[metric] = int(total) if metric in COUNTS else float(total)
            coverage[metric] = len(occupied)
            evidence[metric] = used
    return {'period': {'start': start, 'end': end, 'timezone': timezone},
            'days': (last - first).days, 'totals': totals, 'covered_days': coverage, 'evidence': evidence,
            'note': 'Totals use nonoverlapping complete windows. Partial coverage is not a full-period total.'}


def backup(db, path):
    destination = sqlite3.connect(path)
    try:
        with destination:
            db.backup(destination)
    finally:
        destination.close()
