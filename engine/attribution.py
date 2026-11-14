"""Which store orders came from organic posts, as aggregates only.

Reads Heartside's Shopify orders through a read-only app (scope exactly
read_orders) and keeps nothing per order: no id, name, email, address, line
item, typed answer or full landing URL. Heartside's chat can write the buyer's
dog and person names into URL query strings, so a landing page is kept as its
path alone and a referrer as its host alone, and both only long enough to
classify the order.

Tiers, best evidence first:
  engine          the order used a discount code from a family Krish registered
                  in config/codes.json, or the visit carried this engine's own
                  tags (utm_campaign hs_growth_YYYYMM and a creative id in
                  utm_content), so the post family is known
  organic_social  a social referrer or organic social tags, with no paid signal
  organic_search  a search engine referrer, no paid signal (not counted as posts)
  paid            any paid signal: paid utm_medium or an ad click id
  pending         Shopify has not finished the journey (up to 72 hours)
  direct          nothing to go on
Organic posts = engine + organic_social. Paid never counts, even if tagged or
coded: the paid checks run first.
"""
import datetime as dt
from decimal import Decimal
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

from . import ledger

CODES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'codes.json')
FAMILY = re.compile(r'^(IG|FB|TT|YT|PIN|GG|EM|WEB|CR)_(EMO|ENT|UTIL|PROOF|OFFER)_C\d{2,3}$')

TIMEZONE = 'Europe/London'  # the shop's verified IANA zone (docs/ENGINE.md)
API_VERSION = '2026-10'
SCOPE = 'read_orders'
ENV = ('HEARTSIDE_SHOP_DOMAIN', 'SHOPIFY_CLIENT_ID', 'SHOPIFY_CLIENT_SECRET')
CREATIVE_ID = re.compile(r'^(IG|FB|TT|YT|PIN|GG|EM|WEB|CR)_(EMO|ENT|UTIL|PROOF|OFFER)_([A-Z]+)_C(\d{2,3})_H(\d{2,3})_V(\d{1,2})_(\d{8})$')
# A paid order Printful has not shipped within this many days: the order path may be broken (the order workflows
# keep no successful runs since 10 Nov, so this is the outcome check that still sees them). Counted, never itemised.
UNFULFILLED_DAYS = 7
TIERS = ('engine', 'organic_social', 'organic_search', 'paid', 'unverified', 'pending', 'direct')
# A Meta visit (a Facebook or Instagram referrer, or an fbclid) with no engine creative id and no code could be an
# ad click whose link carries no paid tag, so it never counts as organic and never crowns a winner until Krish
# answers the two ads questions on his board (are Meta ads running; does every ad link carry
# utm_medium=paid_social). A boosted Facebook post reuses its caption link, organic engine tags and all, so while
# the hold is on a Facebook-family engine link that came through Meta waits as unverified too. Set this to False
# only on his answer, which must also say that no boosted Facebook post carries an engine link in its caption,
# recorded as a Ruling in the commit.
# Answered 13 Nov 2026 from this repository's own record, as Krish asked ("ask growth repo"): the only Meta ad was
# the F10 pilot, $25 lifetime, 6 Nov 12:45 to 7 Nov 12:45 GMT, which used the Instagram post (no caption link) and a
# Shop now button tagged utm_medium=paid_social (docs/boost/2026-11-05-sandbox.md); the four $50 boosts stayed held
# and the 10 Nov ruling allows only $20-a-day boosts proposed one at a time (CHANGES.md). So no Meta ad runs now and
# the one that ran was tagged: Meta visits count as organic again. Read from the record, not from Ads Manager. Before
# any approved boost goes live, this goes back to True for its window (docs/PAID-BOOSTS.md, "Gates before money
# moves").
META_UNVERIFIED = False
# Threads is Meta's too (threads.net, and threads.com, its current domain).
META = ('instagram.com', 'facebook.com', 'fb.com', 'fb.me', 'messenger.com', 'threads.net', 'threads.com')
# Meta's own source names, as utm_source (its {{site_source_name}} fills ig, fb, msg or an) or as Shopify's visit
# source. This engine's own non-engine Meta links (hs_release_, thanksgiving_, page_button campaigns) carry these
# too, so they also wait as unverified until the ads questions are answered; engine-tagged links do not, except a
# Facebook-family one that came through Meta (META_UNVERIFIED above).
META_SOURCES = {'ig', 'instagram', 'fb', 'facebook', 'meta', 'msg', 'messenger', 'an', 'audience_network', 'threads'}
ORGANIC = ('engine', 'organic_social')
SOCIAL = ('instagram.com', 'facebook.com', 'fb.com', 'fb.me', 'tiktok.com', 'pinterest.com', 'pin.it',
          'youtube.com', 'youtu.be', 'threads.net', 'threads.com', 'reddit.com', 'linktr.ee')
SEARCH = ('google.', 'bing.com', 'duckduckgo.com', 'yahoo.com', 'ecosia.org', 'perplexity.ai', 'chatgpt.com')
# Sources our own organic posting can stamp on a link: Buffer's campaign tagging and the platforms themselves.
ORGANIC_SOURCES = {'buffer', 'instagram', 'ig', 'facebook', 'fb', 'tiktok', 'pinterest', 'youtube', 'threads', 'linktree', 'linkin.bio'}
PAID_MEDIUM = {'cpc', 'ppc', 'paid', 'paid_social', 'paidsocial', 'paid-social', 'ads', 'ad', 'display', 'cpm', 'affiliate'}
# GA4's own paid rule, ^(.*cp.*|ppc|retargeting|paid.*)$, plus sponsored: 'paid social', 'paid_search', 'cpv'.
PAID_PATTERN = re.compile(r'^(?:.*cp.*|ppc|retargeting|paid.*|sponsored)$')
AD_CLICK = {'gclid', 'gbraid', 'wbraid', 'msclkid', 'ttclid', 'dclid', 'twclid', 'li_fat_id', 'rdt_cid'}
INTERNAL_TAG = 'hs-internal'
DEFINITION = ('Net sales are each order\'s subtotal after discounts, less everything refunded, never below zero, '
              'by the London day the order was created. Fully refunded orders are not counted. '
              'Organic posts = engine-tagged plus organic social. A Meta visit with no engine id or code is '
              'unverified until the ads questions are answered, and never organic.')

# Exactly the fields this module reads. A test holds the query to this list.
QUERY = '''query Orders($first: Int!, $after: String, $query: String) {
  orders(first: $first, after: $after, query: $query, sortKey: CREATED_AT) {
    pageInfo { hasNextPage endCursor }
    nodes {
      createdAt test cancelledAt tags discountCodes displayFulfillmentStatus
      subtotalPriceSet { shopMoney { amount currencyCode } }
      totalRefundedSet { shopMoney { amount currencyCode } }
      customerJourneySummary {
        ready
        firstVisit { landingPage referrerUrl source utmParameters { source medium campaign content } }
        lastVisit { landingPage referrerUrl source utmParameters { source medium campaign content } }
      }
    }
  }
}'''


def host(url):
    try:
        name = (urllib.parse.urlparse(url or '').hostname or '').lower()
    except ValueError:
        return ''
    return name[4:] if name.startswith('www.') else name


def ad_click(url):
    """True when the landing URL carries an ad click id. Only the parameter names are read."""
    try:
        return bool(AD_CLICK & set(urllib.parse.parse_qs(urllib.parse.urlparse(url or '').query)))
    except ValueError:
        return False


def load_codes(path=None):
    """The registered code families, {PREFIX: family}, upper-cased. Missing file or no families: an empty registry."""
    try:
        with open(path or CODES, encoding='utf-8') as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return {}
    families = data.get('families') or {}
    if not isinstance(families, dict):
        raise ValueError('config/codes.json: "families" must map a code prefix to a post family')
    registry = {}
    for prefix, family in families.items():
        if not isinstance(prefix, str) or not prefix.strip() or not isinstance(family, str) or not FAMILY.match(family):
            raise ValueError(f'config/codes.json: {prefix!r} must map to a family like TT_EMO_C301, not {family!r}')
        registry[prefix.strip().upper()] = family
    return registry


def code_family(order, registry):
    """The family of the first registered code on the order, by the longest matching prefix, or None."""
    for code in order.get('discountCodes') or []:
        name = str(code or '').strip().upper()
        hits = [p for p in registry if name.startswith(p)]
        if hits:
            return registry[max(hits, key=len)]
    return None


def classify(order, registry=None):
    """(tier, family) for one order's journey; family is set only for the engine tier.
    registry: {code prefix: family} from config/codes.json (read when not given)."""
    registry = load_codes() if registry is None else registry
    journey = order.get('customerJourneySummary') or {}
    visits = [v for v in (journey.get('lastVisit'), journey.get('firstVisit')) if v]
    if not journey.get('ready', True) and not visits:
        return 'pending', None  # a paid signal may still arrive, and paid is checked before any code
    for visit in visits:
        if paid_medium(visit) or ad_click(visit.get('landingPage')):
            return 'paid', None
    family = code_family(order, registry)
    if family:
        return 'engine', family
    for visit in visits:
        utm = visit.get('utmParameters') or {}
        match = CREATIVE_ID.match(utm.get('content') or '')
        if match and (utm.get('campaign') or '').startswith('hs_growth_'):
            if META_UNVERIFIED and match.group(1) == 'FB' and meta_visit(visit):
                return 'unverified', None  # a boosted Facebook post's caption link keeps its organic engine tags
            return 'engine', f'{match.group(1)}_{match.group(2)}_C{match.group(4)}'
    if META_UNVERIFIED and any(meta_visit(v) for v in visits):
        return 'unverified', None
    for visit in visits:
        utm = visit.get('utmParameters') or {}
        name = host(visit.get('referrerUrl'))
        if (utm.get('medium') or '').lower().startswith('organic') or (utm.get('source') or '').lower() in ORGANIC_SOURCES or any(
                name == s or name.endswith('.' + s) for s in SOCIAL):
            return 'organic_social', None
    for visit in visits:
        if any(s in host(visit.get('referrerUrl')) for s in SEARCH):
            return 'organic_search', None
    if not journey.get('ready', True):
        return 'pending', None
    return 'direct', None


def paid_medium(visit):
    """True when a visit's utm_medium is paid: the known set or GA4's paid pattern, case and spaces aside."""
    medium = ((visit.get('utmParameters') or {}).get('medium') or '').strip().lower()
    return medium in PAID_MEDIUM or bool(PAID_PATTERN.match(medium))


def meta_visit(visit):
    """True when a visit came from Facebook or Instagram: its referrer, Meta's source name in utm_source or in
    Shopify's own visit source (Instagram's in-app browser often drops the referrer), or an fbclid."""
    name = host(visit.get('referrerUrl'))
    if any(name == m or name.endswith('.' + m) for m in META):
        return True
    utm = visit.get('utmParameters') or {}
    if (utm.get('source') or '').strip().lower() in META_SOURCES or (visit.get('source') or '').strip().lower() in META_SOURCES:
        return True
    try:
        query = urllib.parse.urlsplit(visit.get('landingPage') or '').query
    except ValueError:
        return False  # a landing URL urlsplit refuses: read as no fbclid, like ad_click and host, never a crash
    return any(k.lower() == 'fbclid' for k, _ in urllib.parse.parse_qsl(query, keep_blank_values=True))


def counted(order):
    """Test, cancelled and internal orders never count."""
    tags = {t.strip().lower() for t in order.get('tags') or []}
    return not order.get('test') and not order.get('cancelledAt') and INTERNAL_TAG not in tags


def money(order, field):
    value = ((order.get(field) or {}).get('shopMoney') or {})
    if value.get('currencyCode', 'USD') != 'USD':
        raise ValueError('attribution expects USD orders')
    return Decimal(str(value.get('amount') or '0'))


def amount(order):
    """Net sales for one order: its subtotal after discounts, less everything refunded, never below zero.
    Refunds include any refunded shipping or tax, so this can only understate, never overstate."""
    return max(Decimal(0), money(order, 'subtotalPriceSet') - money(order, 'totalRefundedSet'))


def month_start(today):
    """The first day of the London month to date; on the 1st, the month that just closed (protocol.month_window)."""
    first = today.replace(day=1)
    return (today - dt.timedelta(days=1)).replace(day=1) if first == today else first


def windows(today):
    """The trailing 28 days, the last complete London week (Monday to Monday) and the London month to date, as
    dates. The month is what Control Center's net_sales_usd reads (engine/protocol.py net_sales)."""
    return {'trailing_28d': (today - dt.timedelta(days=28), today),
            'last_week': (today - dt.timedelta(days=today.weekday() + 7), today - dt.timedelta(days=today.weekday())),
            'month': (month_start(today), today)}


def aggregate(orders, start, end):
    """Counts and net sales per tier, and per engine family, for orders created in [start, end) London time."""
    zone = ZoneInfo(TIMEZONE)
    registry = load_codes()
    tiers = {t: {'orders': 0, 'net_sales': Decimal(0)} for t in TIERS}
    families, refunded, stuck = {}, 0, 0
    for order in orders:
        if not counted(order):
            continue
        day = dt.datetime.fromisoformat(order['createdAt'].replace('Z', '+00:00')).astimezone(zone).date()
        if not start <= day < end:
            continue
        value = amount(order)
        if value <= 0:  # a fully refunded order is not a sale
            refunded += 1
            continue
        if order.get('displayFulfillmentStatus') == 'UNFULFILLED' and (end - day).days > UNFULFILLED_DAYS:
            stuck += 1
        tier, family = classify(order, registry)
        tiers[tier]['orders'] += 1
        tiers[tier]['net_sales'] += value
        if family:
            row = families.setdefault(family, {'orders': 0, 'net_sales': Decimal(0)})
            row['orders'] += 1
            row['net_sales'] += value
    organic = {'orders': sum(tiers[t]['orders'] for t in ORGANIC),
               'net_sales': sum((tiers[t]['net_sales'] for t in ORGANIC), Decimal(0))}
    store = {'orders': sum(t['orders'] for t in tiers.values()),
             'net_sales': sum((t['net_sales'] for t in tiers.values()), Decimal(0))}
    if organic['net_sales'] > store['net_sales'] or organic['orders'] > store['orders']:
        raise ValueError('organic cannot exceed the store total')
    pair = lambda row: {'orders': row['orders'], 'net_sales': float(row['net_sales'])}
    return {'start': start.isoformat(), 'end': end.isoformat(), 'timezone': TIMEZONE,
            'store': pair(store), 'organic': pair(organic), 'fully_refunded_orders': refunded,
            'unfulfilled_over_7_days': stuck,
            'tiers': {t: pair(v) for t, v in tiers.items()},
            'families': {f: pair(v) for f, v in sorted(families.items())},
            'definition': DEFINITION}


def setup(db):
    db.execute('''CREATE TABLE IF NOT EXISTS attribution (
        window TEXT NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL, timezone TEXT NOT NULL,
        observed_at TEXT NOT NULL, values_json TEXT NOT NULL, PRIMARY KEY (window, start, end, timezone))''')
    db.commit()


def store(db, name, reading, observed_at=None):
    setup(db)
    with db:
        db.execute('INSERT OR REPLACE INTO attribution VALUES (?, ?, ?, ?, ?, ?)',
                   (name, reading['start'], reading['end'], reading['timezone'], observed_at or ledger.now(),
                    json.dumps(reading, sort_keys=True)))


def latest(db, name='trailing_28d'):
    """The newest stored reading, or None. Reads only: Control Center reports never write engine state."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='attribution'").fetchone():
        return None
    row = db.execute('SELECT * FROM attribution WHERE window=? ORDER BY end DESC, observed_at DESC LIMIT 1', (name,)).fetchone()
    return ({**json.loads(row['values_json']), 'observed_at': row['observed_at']}) if row else None


# ---------------------------------------------------------------------------
# Reading Shopify. Network code; the logic above is what the tests hold.
# ---------------------------------------------------------------------------
def missing_env():
    return [name for name in ENV if not os.environ.get(name, '').strip()]


def post(url, body, headers=None, form=False):
    data = urllib.parse.urlencode(body).encode() if form else json.dumps(body).encode()
    kind = 'application/x-www-form-urlencoded' if form else 'application/json'
    request = urllib.request.Request(url, data=data, method='POST',
                                     headers={'Content-Type': kind, 'Accept': 'application/json', **(headers or {})})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as e:
        raise ValueError(f'Shopify answered HTTP {e.code}: {refusal(e)}') from None


def refusal(error):
    """Shopify's own error code and description, never the request, truncated."""
    try:
        body = json.loads(error.read(4000) or b'{}')
    except (ValueError, OSError):
        return 'no readable error body'
    if isinstance(body, dict):
        parts = [str(body.get(k)) for k in ('error', 'error_description', 'errors') if body.get(k)]
        return '; '.join(parts)[:300] or 'no error code given'
    return 'no error code given'


def access_token(shop):
    """A 24-hour token from the app's client credentials, refused unless its scope is exactly read_orders."""
    answer = post(f'https://{shop}/admin/oauth/access_token',
                  {'client_id': os.environ['SHOPIFY_CLIENT_ID'], 'client_secret': os.environ['SHOPIFY_CLIENT_SECRET'],
                   'grant_type': 'client_credentials'}, form=True)
    scopes = {s.strip() for s in (answer.get('scope') or '').split(',') if s.strip()}
    if scopes != {SCOPE}:
        raise ValueError(f'the Shopify app must have exactly the {SCOPE} scope; it has {len(scopes)} scope(s) of another shape')
    return answer['access_token']


def fetch(shop, token, since, limit=2000):
    """Orders created since a date, with the allowlisted fields only."""
    orders, after = [], None
    while True:
        answer = post(f'https://{shop}/admin/api/{API_VERSION}/graphql.json',
                      {'query': QUERY, 'variables': {'first': 100, 'after': after, 'query': f'created_at:>={since.isoformat()}'}},
                      {'X-Shopify-Access-Token': token})
        if answer.get('errors'):
            raise ValueError('Shopify refused the orders query: ' + '; '.join(str(e.get('message', ''))[:120] for e in answer['errors']))
        page = answer['data']['orders']
        orders += page['nodes']
        if not page['pageInfo']['hasNextPage'] or len(orders) >= limit:
            return orders
        after = page['pageInfo']['endCursor']


def run(db, today=None):
    """Read, classify and store the windows. Returns a printable summary; never raises on missing setup."""
    gaps = missing_env()
    if gaps:
        return {'status': 'hold', 'reason': 'organic attribution needs the read-only Shopify app: missing ' + ', '.join(gaps)}
    shop = os.environ['HEARTSIDE_SHOP_DOMAIN'].strip().lower()
    if not shop.endswith('.myshopify.com'):
        return {'status': 'hold', 'reason': 'HEARTSIDE_SHOP_DOMAIN must be the store\'s .myshopify.com address'}
    previous = latest(db)
    london_today = dt.datetime.now(ZoneInfo(TIMEZONE)).date()
    if previous and previous.get('definition') == DEFINITION and dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(
            previous['observed_at'].replace('Z', '+00:00')) < dt.timedelta(hours=5) and today is None \
            and previous.get('end') == london_today.isoformat():
        # Five hours, so a runner every six hours reads every run; and always again once the London day changes,
        # so the month window never ends yesterday.
        return {'status': 'current', 'reason': f'read at {previous["observed_at"]}; the next read is due five hours later'}
    today = today or london_today
    spans = windows(today)
    # One day early: the query's date is read in the shop's own zone, and aggregate() keeps London days only.
    orders = fetch(shop, access_token(shop), min(a for a, _ in spans.values()) - dt.timedelta(days=1))
    readings = {}
    for name, (start, end) in spans.items():
        readings[name] = aggregate(orders, start, end)
        store(db, name, readings[name])
    return {'status': 'measured', 'windows': readings}
