#!/usr/bin/env python3
"""The Heartside growth engine's one tool: stay current with the heartside
repository and the live store, check every draft against Heartside's house
rules, and leave a pack of drafts where Krish can work it.

Core commands use the standard library. Media also needs Pillow and FFmpeg.
Runs anywhere Python 3.9+ and git run (a Codex
session, a Cowork session, a Mac, a GitHub Action). Nothing here posts,
sends, comments, follows, DMs, orders or spends. The only writes are this
engine's own files under local/ (and state/ when a GitHub Action publishes
it), plus a pack to Control Center once Control Center can keep Heartside's
packs apart from makeyourmindup's (see `post` below).

    python3 growth.py sync [--publish]
        Read krishanraja/heartside as it is right now: the commit on main,
        what changed since the last sync, open pull requests, the canon
        documents its README tells every session to read, and what is on
        sale in the live store. Writes local/state/heartside.json and
        local/state/HEARTSIDE-NOW.md (--publish writes state/ instead, for
        the GitHub Action that keeps the repository's copy current). Every
        job starts here.

    python3 growth.py canon [--full]
        The canon documents at the synced commit, in the order heartside's
        README gives them. --full prints them: the only source of brand and
        product facts besides the live store.

    python3 growth.py store
        What is on sale at heartside.io right now: title, price, link.

    python3 growth.py link URL CREATIVE_ID
        The heartside.io url with the tracking every draft must carry, built
        from the creative id (PLAYBOOK.md, "Every tracked link").

    python3 growth.py check PACK.json
        Heartside's house rules on every draft, the creative ids and links,
        and that the pack was written against today's heartside (no canon
        change since the sync it names). Exit 1 names everything wrong.

    python3 growth.py post PACK.json
        Checks, then stores the pack. Until Control Center keeps a venture
        on each pack, it goes to local/packs/ and is printed in full, never
        to Control Center (where it would replace makeyourmindup's pack for
        the same day and kind).

    python3 growth.py read [--days 7] [--kind daily]
        The packs already stored, newest first (for the Sunday report).

    python3 growth.py doctor
        Is this machine ready? Exit 1 names what is not, with the fix.

    python3 growth.py --self-test

    python3 growth.py readiness
    python3 growth.py render campaigns/waits-at-the-door.json
    python3 growth.py metrics import local/metrics/report.json
    python3 growth.py creatives list
    python3 growth.py cc run [--mode live]
        See docs/ENGINE.md for production, the local ledger and report windows.

A pack file:
    {"pack_date": "2026-10-19", "kind": "daily", "venture": "heartside",
     "heartside_sha": "<the sha sync printed>",
     "headline": "Monday: 1 Reel brief, 3 native editions, 2 Pins",
     "items": [{"platform": "instagram", "creative_id": "IG_EMO_REEL_C01_H03_V1_20261019",
                "target_url": "", "target_name": "", "why": "...", "text": "..."}],
     "numbers": null, "link": null}

Kinds: daily, radar, numbers, partners, conversion, report.
Environment: GITHUB_TOKEN (optional, raises GitHub's read limit),
GROWTH_ENGINE_TOKEN (only once Control Center takes Heartside packs),
CONTROL_CENTER_ENGINE_TOKEN (the growth engine protocol bearer, used only by
`growth.py cc`; see docs/ENGINE.md), CONTROL_CENTER_URL (default
https://controlcenter.krishraja.com).
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

from engine import offers

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = 'krishanraja/heartside'
BRANCH = 'main'
STORE = 'https://heartside.io'
RAW = 'https://raw.githubusercontent.com/' + REPO
API = 'https://api.github.com/repos/' + REPO
BASE = os.environ.get('CONTROL_CENTER_URL', 'https://controlcenter.krishraja.com').rstrip('/')
UA = {'User-Agent': 'growth-heartside (+https://github.com/krishanraja/growth-heartside)'}
LOCAL = os.path.join(HERE, 'local')

KINDS = ('daily', 'radar', 'numbers', 'partners', 'conversion', 'report')
PLATFORMS = ('instagram', 'facebook', 'tiktok', 'pinterest', 'youtube', 'google', 'email', 'store',
             'reddit', 'creator', 'other')

# ---------------------------------------------------------------------------
# What heartside says every session must read. The README's "Picking this up?"
# line names the canon in order of authority. The newest dated handover in
# docs/ (e.g. docs/COWORK-HANDOVER-2026-10-15.md) is added after it, because
# sessions write those before the README catches up. These are always added.
# ---------------------------------------------------------------------------
ALWAYS_CANON = ('README.md', 'design/BRAND-SYSTEM.md', 'shopify/README.md')
FALLBACK_CANON = ('docs/V3-GIFTS-FROM-YOUR-DOG.md', 'docs/POSITIONING.md', 'docs/HANDOFF.md', 'docs/SYNC.md')
HANDOVER = re.compile(r'^(?:[A-Z0-9]+-)*HANDOVER-(\d{4}-\d{2}-\d{2})[\w-]*\.md$')

# The sections of heartside's canon that the RULES below were written from,
# with their fingerprint at heartside commit 1028556 (14 Oct 2026). If any
# section changes, or stops being canon, no pack passes until a person reads
# the new words and updates RULES and RULES_BASIS in an interactive session.
RULES_SOURCES = (
    ('docs/V3-GIFTS-FROM-YOUR-DOG.md', '## 2. '),    # what Krish rejected, and the rules that follow
    ('docs/V3-GIFTS-FROM-YOUR-DOG.md', '### 4.6 '),  # Biscuit's voice
    ('docs/HANDOFF.md', '## 2. '),                   # hard rules
    ('docs/POSITIONING.md', '## 3. '),               # retire from headlines
)
RULES_BASIS = {
    'docs/V3-GIFTS-FROM-YOUR-DOG.md ## 2. ': '125afc11c43dbc1b',
    'docs/V3-GIFTS-FROM-YOUR-DOG.md ### 4.6 ': 'f4a6bd4ab5ce2c91',
    'docs/HANDOFF.md ## 2. ': '7aa03e172d93daa7',
    'docs/POSITIONING.md ## 3. ': 'c102e12c77cb178f',
}

# ---------------------------------------------------------------------------
# Heartside's house rules, from the sections above. Each line says where.
# ---------------------------------------------------------------------------
EM_DASH = re.compile('\u2014')                                    # HANDOFF 2.6, V3 2
BANNED = ['elevate', 'unleash', 'must-have', 'must have', 'game-changer', 'game changer',
          'fur baby', 'furbaby', 'fur-baby', 'fur babies']        # V3 2
SLOP = ['delve', "in today's", 'in a world where', "it's worth noting", 'seamless', 'unlock',
        'harness', 'leverage', 'robust', 'tapestry', 'realm', 'cutting-edge', 'revolutionize',
        'transformative', 'synergy', 'buckle up', 'look no further', 'a testament to']  # Krish's kill list
NOT_BUT = re.compile(r"\b(?:it'?s|this is|that'?s)\s+not\s+(?:just\s+|only\s+|about\s+)?[^.;:!?]{1,60}[,;]\s*(?:it'?s|but)\b"
                     r"|\bisn'?t\s+(?:just|only)\b", re.I)           # V3 2
RETIRED = [  # POSITIONING 3 and V3 2, 3
    (re.compile(r'written by (?:your|the|a) dog', re.I), '"written by your dog" is retired (dogs can\'t write; gifts are FROM the dog)'),
    (re.compile(r"now it'?s in writing", re.I), '"Now it\'s in writing" is retired'),
    (re.compile(r'your dog has notes(?!\w)', re.I), '"Your dog has notes" is retired as a headline and undecided as a sign-off: ask Krish (the handle @yourdoghasnotes is fine)'),
    (re.compile(r'annual review|performance review|body double|areas? for improvement', re.I), 'names a product or the HR joke retired at the v3 launch'),
]
FAKE_PROOF = [  # HANDOFF 2.3, V3 2
    (re.compile(r'sold out|only \d+ left|selling fast|hurry|last chance|limited time|ends (?:tonight|soon|today)|while (?:supplies|stocks?) last|countdown', re.I),
     'invented scarcity or urgency (only a real, confirmed order-by date is allowed)'),
    (re.compile(r'best[- ]?sell(?:er|ing)|#1\b|number one|\u2605|5[- ]star|five[- ]star|\d+ reviews|happy customers|customers love|thousands of|loved by', re.I),
     'claims proof Heartside does not have (no invented reviews, ratings, rankings or customer counts)'),
    (re.compile(r'~~|\bwas \$\d|\bregularly \$\d', re.I), 'a strike-through or "was" price'),
]
SAD = re.compile(r'rainbow bridge|passed away|crossed the bridge|in (?:loving )?memory|memorial|put to sleep|\bRIP\b|cancer', re.I)  # HANDOFF 2.6, V3 4.6, 9
# Briefs, reports, radar notes and store fixes mix instructions for Krish with
# words the public will see. In those, only lines marked as public get the
# copy rules; every line still gets the em dash and link rules.
INTERNAL = ('other', 'store')
PUBLIC_LINE = re.compile(r'^\s*(?:on[- ]screen|voiceover|vo|biscuit|caption|cover|copy|headline|title|hook|cta)\s*:', re.I)
UK = [(re.compile(r'personalis', re.I), 'personaliz'), (re.compile(r'\bcolour', re.I), 'color'),
      (re.compile(r'\bfavourite', re.I), 'favorite'), (re.compile(r'\bcentre\b', re.I), 'center'),
      (re.compile(r'\bcatalogue', re.I), 'catalog'), (re.compile(r'\borganis', re.I), 'organiz'),
      (re.compile(r'\bcosy\b', re.I), 'cozy'), (re.compile(r'\bmum\b', re.I), 'mom'),
      (re.compile(r'\bjewellery', re.I), 'jewelry')]               # HANDOFF 2.6: US spelling
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
CONTACT = 'krish@heartside.io'                                     # HANDOFF 2.5
EMOJI = re.compile('[\U0001F300-\U0001FAFF\u2600-\u27bf]')
HASHTAG = re.compile(r'(?<![\w&])#\w+')
LIMITS = {'instagram': 2200, 'tiktok': 4000, 'pinterest': 500, 'youtube': 5000, 'reddit': 1500}
PRICE = re.compile(r'\$(\d{1,4}(?:\.\d{2})?)(?![\d,])')

# Every link to the store carries tracking built from the creative id.
OWN_LINK = re.compile(r'https?://(?:www\.)?heartside\.io[^\s)>\]"\']*', re.I)
CREATIVE_ID = re.compile(r'^(IG|FB|TT|YT|PIN|GG|EM|WEB|CR)_(EMO|ENT|UTIL|PROOF|OFFER)_'
                         r'(REEL|STORY|POST|CAROUSEL|PIN|SHORT|VIDEO|LIVE|REPLY|BIO|LISTING|ARTICLE|EMAIL|NOTE)_'
                         r'C(\d{2,3})_H(\d{2,3})_V(\d{1,2})_(\d{8})$')
SOURCE = {'IG': 'instagram', 'FB': 'facebook', 'TT': 'tiktok', 'YT': 'youtube', 'PIN': 'pinterest',
          'GG': 'google', 'EM': 'email', 'WEB': 'web', 'CR': 'creator'}


def medium(fmt):
    if fmt in ('REEL', 'SHORT', 'VIDEO', 'LIVE'):
        return 'organic_video'
    return {'LISTING': 'product_listing', 'ARTICLE': 'organic_search', 'EMAIL': 'email'}.get(fmt, 'organic_social')


def tracked(url, creative_id):
    """The url with this engine's UTM tags (replacing any already there)."""
    m = CREATIVE_ID.match(creative_id or '')
    if not m:
        raise ValueError(f'"{creative_id}" is not a creative id (PLAYBOOK.md, "Creative ids")')
    plat, _pillar, fmt, _c, _h, _v, day = m.groups()
    base, _, frag = url.partition('#')
    base = re.sub(r'([?&])utm_[a-z]+=[^&]*', r'\1', base).rstrip('?&').replace('?&', '?')
    while '&&' in base:
        base = base.replace('&&', '&')
    tags = (f'utm_source={SOURCE[plat]}&utm_medium={medium(fmt)}'
            f'&utm_campaign=hs_growth_{day[:6]}&utm_content={creative_id}')
    return base + ('&' if '?' in base else '?') + tags + (('#' + frag) if frag else '')


# ---------------------------------------------------------------------------
# Reading heartside and the store.
# ---------------------------------------------------------------------------
def http(url, accept_json=True, timeout=60):
    headers = dict(UA)
    if url.startswith('https://api.github.com/'):
        headers['Accept'] = 'application/vnd.github+json'
        if os.environ.get('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
        body = r.read()
    return json.loads(body) if accept_json else body.decode('utf-8', errors='replace')


def head_sha():
    """The commit on heartside's main right now: git first (no rate limit), then the API."""
    try:
        out = subprocess.run(['git', 'ls-remote', f'https://github.com/{REPO}', f'refs/heads/{BRANCH}'],
                             capture_output=True, text=True, timeout=60)
        sha = (out.stdout.split() or [''])[0]
        if re.fullmatch(r'[0-9a-f]{40}', sha):
            return sha
    except (OSError, subprocess.SubprocessError):
        pass
    return http(f'{API}/commits/{BRANCH}')['sha']


def raw(path, sha):
    try:
        return http(f'{RAW}/{sha}/{path}', accept_json=False)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def docs_listing(sha):
    """The file names directly in heartside's docs/ at a commit, or None if GitHub did not answer."""
    try:
        return [x['name'] for x in http(f'{API}/contents/docs?ref={sha}') if x.get('type') == 'file']
    except (urllib.error.URLError, ValueError, KeyError, TypeError):
        return None


def newest_handover(names):
    """The newest dated handover among docs/ file names, as a path, or None."""
    dated = [(m.group(1), n) for n in (names or []) for m in [HANDOVER.match(n)] if m]
    return f'docs/{max(dated)[1]}' if dated else None


def canon_paths(readme, handover=None):
    """The canon heartside's README names, in its order, then the newest handover, then the always-read files."""
    paths = []
    para = next((p for p in (readme or '').split('\n\n') if 'Picking this up' in p), '')
    for p in re.findall(r'\]\(((?:docs|design|shopify)/[^)#\s]+\.md)\)', para):
        if p not in paths:
            paths.append(p)
    found = bool(paths)
    if not found:
        paths = list(FALLBACK_CANON)
    if handover and handover not in paths:
        paths.append(handover)
    for p in ALWAYS_CANON:
        if p not in paths:
            paths.append(p)
    return paths, found


def section(text, prefix):
    """The section that starts with a heading line beginning `prefix`, up to the next heading of the same or higher level."""
    if text is None:
        return None
    level = len(prefix) - len(prefix.lstrip('#'))
    lines, out, on = text.split('\n'), [], False
    for line in lines:
        if line.startswith(prefix):
            on = True
            out.append(line)
            continue
        if on:
            m = re.match(r'^(#+) ', line)
            if m and len(m.group(1)) <= level:
                break
            out.append(line)
    return '\n'.join(out).strip() if out else None


def digest(s):
    return hashlib.sha256((s if s is not None else '\0MISSING').encode()).hexdigest()


def fingerprints(texts):
    out = {}
    for path, prefix in RULES_SOURCES:
        out[f'{path} {prefix}'] = digest(section(texts.get(path), prefix))[:16]
    return out


def store_products():
    data = http(f'{STORE}/products.json?limit=250')
    out = []
    for p in data.get('products', []):
        prices = sorted({float(v['price']) for v in p.get('variants', [])})
        out.append({'id': p.get('id'), 'title': p['title'], 'handle': p['handle'], 'type': p.get('product_type') or '',
                    'prices': prices, 'available': any(v.get('available') for v in p.get('variants', [])),
                    'variants': [{'id': v['id'], 'price': v['price'], 'available': v.get('available', False)} for v in p.get('variants', [])],
                    'url': f'{STORE}/products/{p["handle"]}'})
    return out


def canon_prices(texts):
    """Dollar amounts in the gift table of heartside's top canon document (V3 section 3)."""
    out = set()
    for path, text in texts.items():
        sec = section(text, '## 3. ') if text else None
        if sec and 'gift range' in sec.splitlines()[0].lower():
            for row in sec.splitlines():
                if row.startswith('|') and '**' in row:
                    cells = row.split('|')
                    if len(cells) > 3:
                        out.update(float(x) for x in re.findall(r'\$(\d+(?:\.\d{2})?)', cells[3]))
    return sorted(out)


def state_dir(publish):
    return os.path.join(HERE, 'state') if publish else os.path.join(LOCAL, 'state')


def load_state(published_only=False):
    """The latest reading: this machine's own first, then the repository's copy.
    A publish compares only with the repository's copy."""
    dirs = [os.path.join(HERE, 'state')] if published_only else [os.path.join(LOCAL, 'state'), os.path.join(HERE, 'state')]
    for d in dirs:
        f = os.path.join(d, 'heartside.json')
        if os.path.exists(f):
            return json.load(open(f))
    return None


MEANINGFUL = ('sha', 'canon', 'rules', 'rules_ok', 'store', 'open_pulls', 'offers', 'homepage_v3')


def sync(publish=False, quiet=False):
    prev = load_state(published_only=publish) or {}
    sha = head_sha()
    readme = raw('README.md', sha)
    notes = []
    listing = docs_listing(sha)
    if listing is None:
        handover = prev.get('handover')
        notes.append('heartside\'s docs/ listing not read, so the newest handover is the one last seen; set GITHUB_TOKEN if GitHub is rate limiting')
    else:
        handover = newest_handover(listing)
    paths, found = canon_paths(readme, handover)
    texts = {'README.md': readme}
    for p in paths:
        if p not in texts:
            texts[p] = raw(p, sha)
    for p, _ in RULES_SOURCES:
        if p not in texts:
            texts[p] = raw(p, sha)
    canon = {p: digest(texts.get(p))[:16] for p in paths}
    prints = fingerprints(texts)
    rules_ok = prints == RULES_BASIS and all(p in paths for p, _ in RULES_SOURCES)
    commits, pulls = [], []
    try:
        since = prev.get('synced_at') or (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3)).isoformat()
        for c in http(f'{API}/commits?sha={BRANCH}&per_page=30&since={since}'):
            commits.append({'sha': c['sha'][:10], 'date': c['commit']['committer']['date'],
                            'subject': c['commit']['message'].splitlines()[0][:140]})
        for p in http(f'{API}/pulls?state=open&per_page=20'):
            pulls.append({'number': p['number'], 'title': p['title'][:140], 'branch': p['head']['ref'],
                          'updated': p['updated_at']})
    except (urllib.error.URLError, KeyError, ValueError) as e:
        notes.append(f'commit list and pull requests not read ({getattr(e, "code", e)}); set GITHUB_TOKEN if GitHub is rate limiting')
    try:
        products = store_products()
    except (urllib.error.URLError, ValueError, KeyError) as e:
        products = None
        notes.append(f'the live store did not answer ({getattr(e, "code", e)})')
    try:
        homepage_v3 = 'data-hs3-config' in http(STORE + '/', accept_json=False)
    except (urllib.error.URLError, ValueError):
        homepage_v3 = None
        notes.append('the public homepage could not be checked; its purchase links are not verified')
    old = prev.get('canon') or {}
    changed = sorted(p for p in canon if p in old and old[p] != canon[p])
    added = sorted(set(paths) - set(prev.get('canon', {}))) if prev.get('canon') else []
    removed = sorted(set(prev.get('canon', {})) - set(paths)) if prev.get('canon') else []
    state = {
        'repo': REPO, 'sha': sha, 'synced_at': dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        'previous_sha': prev.get('sha'), 'canon_from_readme': found, 'handover': handover, 'canon': canon,
        'rules': prints, 'rules_ok': rules_ok, 'changed_since_last_sync': changed,
        'canon_added': added, 'canon_removed': removed, 'commits': commits, 'open_pulls': pulls,
        'store': products, 'price_points': sorted(set(canon_prices(texts)) | {x for p in (products or []) for x in p['prices']}),
        'offers': offers.canonical_offers({p: texts.get(p) for p in paths}), 'homepage_v3': homepage_v3,
        'notes': notes,
    }
    d = state_dir(publish)
    if publish and prev and all(prev.get(k) == state[k] for k in MEANINGFUL):
        # The repository's copy changes only when heartside or the store did,
        # so the hourly Action makes no commit for nothing.
        if not quiet:
            print(f'no change since {prev.get("synced_at")} (heartside {sha[:10]})')
        return prev
    os.makedirs(d, exist_ok=True)
    json.dump(state, open(os.path.join(d, 'heartside.json'), 'w'), indent=1)
    open(os.path.join(d, 'HEARTSIDE-NOW.md'), 'w').write(now_md(state, texts))
    if not quiet:
        print(now_md(state, texts))
    return state


def now_md(s, texts):
    top = next(iter(s['canon']), '')
    log = section(texts.get(top), '## 13. ') or ''
    log_lines = [l for l in log.splitlines() if l.startswith('- ')][-8:]
    lines = [
        '# Heartside now', '',
        f'Read from `{s["repo"]}` at commit `{s["sha"][:10]}` on {s["synced_at"]} UTC by `python3 growth.py sync`.',
        'Rewritten when a sync finds heartside, its open pull requests or the store changed. Heartside\'s repository is the source of truth; this is a reading of it.', '',
    ]
    if not s['rules_ok']:
        lines += ['## STOP: Heartside\'s rules changed', '',
                  'A rules section this engine checks against has changed or is no longer canon. No pack passes until',
                  'a person reads the new words and updates RULES and RULES_BASIS in growth.py (AGENTS.md, rule 2).', '',
                  '| Section | Now | Engine was written for |', '|---|---|---|']
        lines += [f'| `{k}` | {v} | {RULES_BASIS.get(k)} |' for k, v in s['rules'].items() if v != RULES_BASIS.get(k)]
        lines += ['']
    if s['changed_since_last_sync'] or s['canon_added'] or s['canon_removed']:
        lines += ['## Canon changed since the last sync', '', 'Read these again before drafting anything:', '']
        lines += [f'- changed: `{p}`' for p in s['changed_since_last_sync']]
        lines += [f'- newly canon: `{p}`' for p in s['canon_added']]
        lines += [f'- no longer canon: `{p}`' for p in s['canon_removed']]
        lines += ['']
    lines += ['## The canon, in heartside\'s order', '']
    lines += [f'{i}. `{p}`' for i, p in enumerate(s['canon'], 1)]
    if not s['canon_from_readme']:
        lines += ['', 'The README\'s "Picking this up?" line was not found, so this is the fallback list. Check heartside\'s README.']
    lines += ['', '## On sale at heartside.io now', '']
    if s['store'] is None:
        lines += ['The store did not answer.']
    else:
        lines += ['| Product | Price | Available |', '|---|---|---|']
        lines += [f'| [{p["title"]}]({p["url"]}) | {", ".join(f"${x:g}" for x in p["prices"])} | {"yes" if p["available"] else "no"} |' for p in s['store']]
    lines += ['', '## Recent commits on main', '']
    lines += [f'- `{c["sha"]}` {c["date"][:10]} {c["subject"]}' for c in s['commits']] or ['- none since the last sync']
    lines += ['', '## Work in flight (open pull requests)', '']
    lines += [f'- #{p["number"]} {p["title"]} (`{p["branch"]}`, updated {p["updated"][:10]})' for p in s['open_pulls']] or ['- none']
    if log_lines:
        lines += ['', f'## Latest decisions (`{top}`, decision log)', ''] + log_lines
    if s['notes']:
        lines += ['', '## Not read this time', ''] + [f'- {n}' for n in s['notes']]
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Checking a pack.
# ---------------------------------------------------------------------------
def problems(item, price_points=()):
    """Every house rule this one draft breaks, in plain words."""
    out = []
    text = item.get('text') or ''
    if not isinstance(text, str):
        return ['text must be a string']
    platform = item.get('platform') or ''
    if not isinstance(platform, str):
        return ['platform must be a string']
    platform = platform.lower()
    if not text.strip():
        return ['it has no text']
    if platform not in PLATFORMS:
        out.append(f'platform "{platform}" is not one of {", ".join(PLATFORMS)}')
    cid = item.get('creative_id')
    if cid and (not isinstance(cid, str) or not CREATIVE_ID.match(cid)):
        out.append(f'creative_id "{cid}" does not follow PLAYBOOK.md, "Creative ids"')
    if EM_DASH.search(text):
        out.append('it has an em dash (use a comma, a full stop or "and")')
    full = text
    if platform in INTERNAL:
        text = '\n'.join(line for line in full.splitlines() if PUBLIC_LINE.match(line))
    low = text.lower()
    for w in BANNED:
        if re.search(r'(?<!\w)' + re.escape(w) + r'(?!\w)', low):
            out.append(f'it says "{w}", which Heartside bans (V3 section 2)')
    for w in SLOP:
        if w in low:
            out.append(f'it says "{w}", a stock phrase that reads as machine-written')
    if NOT_BUT.search(text):
        out.append('it uses the "it\'s not X, it\'s Y" turn')
    for rx, why in RETIRED + FAKE_PROOF:
        if rx.search(text):
            out.append(why)
    if SAD.search(text):
        out.append('it touches death, illness, memorials or abandonment (not in version one; never a joke)')
    for rx, us in UK:
        m = rx.search(text)
        if m:
            out.append(f'UK spelling "{m.group(0)}" (Heartside uses US spelling: {us}...)')
    for addr in EMAIL.findall(text):
        if addr.lower() != CONTACT:
            out.append(f'the address {addr} (the only customer-facing address is {CONTACT})')
    for line in text.splitlines():
        if line.strip().lower().startswith('biscuit:'):
            if line.count('!') > 1:
                out.append('a Biscuit line with more than one exclamation mark')
            if EMOJI.search(line):
                out.append('a Biscuit line with an emoji (Biscuit uses none)')
        elif '!' in line:
            out.append('an exclamation mark outside a "Biscuit:" line (none in body copy)')
    tags = HASHTAG.findall(text)
    if len(tags) > 5:
        out.append(f'{len(tags)} hashtags (2 to 5 specific ones at most)')
    if platform in LIMITS and len(text) > LIMITS[platform]:
        out.append(f'it is {len(text)} characters ({LIMITS[platform]} at most on {platform})')
    if len(full) > 6000:
        out.append('it is over 6,000 characters')
    for url in OWN_LINK.findall(full):
        if '/admin' in url:
            continue
        q = dict(re.findall(r'[?&](utm_[a-z]+)=([^&#]*)', url))
        if not all(k in q for k in ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content')):
            out.append(f'the link {url} is not tracked (python3 growth.py link <url> <creative_id>)')
        elif not CREATIVE_ID.match(q['utm_content']):
            out.append(f'the link {url} carries "{q["utm_content"]}", not a creative id')
        elif cid and q['utm_content'] != cid:
            out.append(f'the link {url} is tracked as {q["utm_content"]} but the draft is {cid}')
    if price_points:
        allowed = set(price_points)
        pts = list(price_points)
        allowed |= {round(a + b, 2) for i, a in enumerate(pts) for b in pts[i:]}
        for p in PRICE.findall(text):
            if float(p) not in allowed:
                out.append(f'the price ${p} is not a price in the live store or heartside\'s gift table (or a sum of two)')
    return out


def check_pack(pack, price_points=(), state=None):
    errs = []
    if not isinstance(pack, dict):
        return ['pack must be a JSON object']
    if pack.get('kind') not in KINDS:
        errs.append(f'kind must be one of {", ".join(KINDS)}')
    if pack.get('venture', 'heartside') != 'heartside':
        errs.append('venture must be "heartside"')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(pack.get('pack_date') or '')):
        errs.append('pack_date must be YYYY-MM-DD')
    else:
        try:
            dt.date.fromisoformat(pack['pack_date'])
        except ValueError:
            errs.append('pack_date is not a real calendar date')
    if not re.fullmatch(r'[0-9a-f]{7,40}', str(pack.get('heartside_sha') or '')):
        errs.append('heartside_sha is missing: run python3 growth.py sync and copy the commit it read')
    head = pack.get('headline') or ''
    if not isinstance(head, str):
        return errs + ['headline must be a string']
    head = head.strip()
    if not head:
        errs.append('headline is empty')
    elif EM_DASH.search(head):
        errs.append('headline has an em dash')
    items = pack.get('items') or []
    if not isinstance(items, list):
        return ['items must be a list']
    if pack.get('kind') == 'daily' and not items:
        errs.append('a daily pack cannot be empty')
    if len(items) > 40:
        errs.append('more than 40 drafts in one pack')
    seen = set()
    for i, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errs.append(f'draft {i}: must be an object'); continue
        cid = item.get('creative_id')
        if item.get('platform') not in INTERNAL and not cid:
            errs.append(f'draft {i}: creative_id is required')
        if isinstance(cid, str):
            if cid in seen:
                errs.append(f'draft {i}: duplicate creative_id {cid}')
            seen.add(cid)
            match = CREATIVE_ID.match(cid)
            if match:
                if item.get('platform') not in INTERNAL and SOURCE[match.group(1)] != item.get('platform'):
                    errs.append(f'draft {i}: creative_id names a different platform')
                if match.groups()[-1] != str(pack.get('pack_date', '')).replace('-', ''):
                    errs.append(f'draft {i}: creative_id date differs from pack_date')
        for p in problems(item, price_points):
            errs.append(f'draft {i} ({item.get("platform", "?")}): {p}')
        if state is not None and isinstance(item.get('text'), str):
            public = item['text']
            if item.get('platform') in INTERNAL:
                public = '\n'.join(l for l in public.splitlines() if PUBLIC_LINE.match(l))
            errs += [f'draft {i}: {e}' for e in offers.validate_item(item, public, state)]
    if pack.get('kind') == 'numbers':
        rows = pack.get('numbers')
        if not isinstance(rows, list) or not rows:
            errs.append('a numbers pack needs "numbers": one row per place read')
        else:
            for r in rows:
                if not isinstance(r, dict):
                    errs.append('every numbers row must be an object'); continue
                if not r.get('platform') or not r.get('note'):
                    errs.append('every numbers row needs a platform and a note saying where it was read')
                for k, v in r.items():
                    if k not in ('platform', 'note') and v is not None and (isinstance(v, bool) or not isinstance(v, (int, float)) or isinstance(v, float) and not math.isfinite(v)):
                        errs.append(f'numbers row {r.get("platform")}: {k} must be a number read today, or null')
    elif pack.get('numbers'):
        errs.append('numbers belong on a pack of kind numbers only')
    return errs


def freshness(pack, state, head_fn, fetch_fn, list_fn=lambda sha: None):
    """Was this pack written against today's heartside? A list of reasons it was not."""
    if not state:
        return ['no sync on this machine: run python3 growth.py sync first']
    sha = str(pack.get('heartside_sha') or '')
    if not sha or not state['sha'].startswith(sha):
        return [f'the pack names heartside {sha or "(none)"} but the last sync read {state["sha"][:10]}: sync, re-read, redraft']
    if not state.get('rules_ok', False):
        return ['Heartside\'s rules changed (local/state/HEARTSIDE-NOW.md, "STOP"): a person must update growth.py first']
    now = head_fn()
    if now == state['sha']:
        return []
    readme = fetch_fn('README.md', now)
    listing = list_fn(now)
    paths, _ = canon_paths(readme, newest_handover(listing) if listing is not None else state.get('handover'))
    texts = {'README.md': readme}
    moved = []
    for p in paths:
        if p not in texts:
            texts[p] = fetch_fn(p, now)
        if state['canon'].get(p) != digest(texts[p])[:16]:
            moved.append(p)
    moved += sorted(set(state['canon']) - set(paths))
    for p, _ in RULES_SOURCES:
        if p not in texts:
            texts[p] = fetch_fn(p, now)
    if fingerprints(texts) != RULES_BASIS:
        moved.append('a rules section')
    if moved:
        return [f'heartside moved to {now[:10]} and changed {", ".join(sorted(set(moved)))} since your sync: sync, re-read, redraft']
    return []


# ---------------------------------------------------------------------------
# Storing a pack.
# ---------------------------------------------------------------------------
TOKEN_FILE = os.path.expanduser('~/.config/growth-makeyourmindup/token')


def token():
    t = os.environ.get('GROWTH_ENGINE_TOKEN', '').strip()
    if not t and os.path.exists(TOKEN_FILE):
        t = open(TOKEN_FILE).read().strip()
    return t


def control_center_takes_heartside():
    """True only when Control Center says it keeps packs per venture and knows heartside.
    Today it keeps one pack per (date, kind), so a Heartside pack would replace makeyourmindup's."""
    if os.environ.get('HEARTSIDE_ENABLE_CC_DELIVERY') != '1':
        return False, 'Control Centre delivery disabled by scope; handoff brief only'
    from engine.control_center import probe
    result = probe(BASE, token())
    if result['authenticated'] and result['venture_isolation']:
        return True, 'Control Center keeps Heartside packs apart'
    if result['outcome'] == 'missing_runner_secret':
        return False, 'no reporting token in this process; the GitHub Actions workflow can use the existing repository secret'
    if result['authenticated']:
        return False, 'Control Center authenticated the runner but does not keep packs per venture yet (Control Center PR 472)'
    return False, f'Control Center access check: {result["outcome"]} (HTTP {result["http_status"] or "not received"})'


def render_md(pack):
    out = [f'# {pack["headline"]}', '', f'{pack["kind"]}, {pack["pack_date"]}, heartside `{pack["heartside_sha"][:10]}`', '']
    for i, it in enumerate(pack.get('items') or [], 1):
        out += [f'## {i}. {it.get("platform")}' + (f' `{it["creative_id"]}`' if it.get('creative_id') else ''), '']
        for k in ('target_name', 'target_url', 'why'):
            if it.get(k):
                out.append(f'**{k.replace("_", " ")}:** {it[k]}  ')
        out += ['', '```text', it.get('text', ''), '```', '']
    if pack.get('numbers'):
        out += ['## Numbers', '', '```json', json.dumps(pack['numbers'], indent=1), '```', '']
    if pack.get('production'):
        out += ['## Media for review', '', pack['production']['manifest'], '',
                'Open the manifest for the Reel, cover, Stories, Pins and subtitles. Nothing is published.', '']
    return '\n'.join(out)


def store_pack(pack):
    # Keep production manifests and a durable retry copy even when the API
    # stores only its presentation fields or goes away during delivery.
    d = os.path.join(LOCAL, 'packs')
    os.makedirs(d, exist_ok=True)
    name = f'{pack["pack_date"]}-{pack["kind"]}'
    existing = os.path.join(d, name + '.json')
    if os.path.exists(existing):
        with open(existing) as f:
            old = f.read()
        history = os.path.join(d, 'history')
        os.makedirs(history, exist_ok=True)
        with open(os.path.join(history, name + '-' + digest(old)[:16] + '.json'), 'w') as f:
            f.write(old)
    with open(os.path.join(d, name + '.json'), 'w') as f:
        json.dump(pack, f, indent=1)
    with open(os.path.join(d, name + '.md'), 'w') as f:
        f.write(render_md(pack))
    takes, why = control_center_takes_heartside()
    if takes:
        try:
            req = urllib.request.Request(BASE + '/api/growth/packs', data=json.dumps({**pack, 'venture': 'heartside', 'source_revision': pack['heartside_sha']}).encode(),
                                         method='POST', headers={**UA, 'Authorization': f'Bearer {token()}', 'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read() or b'{}')
            saved = out.get('pack') or {}
            if (out.get('ok') and saved.get('venture') == 'heartside'
                    and saved.get('source_revision') == pack['heartside_sha']
                    and saved.get('pack_date') == pack['pack_date'] and saved.get('kind') == pack['kind']):
                print(f'stored in Control Center: {pack["kind"]} {pack["pack_date"]} {BASE}/#/growth?section=packs&venture=heartside (local copy retained)')
                return
            why = 'Control Center did not acknowledge the expected venture, date, kind and product SHA'
        except (urllib.error.URLError, ValueError) as e:
            why = f'Control Center delivery failed ({getattr(e, "code", type(e).__name__)}); local retry copy retained'
    print(f'stored on this machine: local/packs/{name}.md ({why}). The pack in full:\n')
    print(render_md(pack))


def read_packs(days, kind):
    d = os.path.join(LOCAL, 'packs')
    days = min(60, max(1, days))
    since = (dt.date.today() - dt.timedelta(days=days - 1)).isoformat()
    out = []
    for f in sorted(os.listdir(d) if os.path.isdir(d) else [], reverse=True):
        if f.endswith('.json') and f[:10] >= since:
            with open(os.path.join(d, f)) as source:
                p = json.load(source)
            if not kind or p.get('kind') == kind:
                out.append(p)
    takes, why = control_center_takes_heartside()
    if takes:
        query = urllib.parse.urlencode({'days': days, 'venture': 'heartside', **({'kind': kind} if kind else {})})
        try:
            req = urllib.request.Request(BASE + '/api/growth/packs?' + query, headers={**UA, 'Authorization': f'Bearer {token()}'})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = json.loads(r.read() or b'{}')
            if not isinstance(body, dict) or not body.get('ok') or not isinstance(body.get('packs'), list):
                raise ValueError('report read refused')
            merged = {(p['pack_date'], p['kind']): p for p in out}
            for p in body.get('packs') or []:
                if not isinstance(p, dict):
                    continue
                if p.get('venture') != 'heartside' or p.get('pack_date', '') < since or (kind and p.get('kind') != kind):
                    continue
                key = (p['pack_date'], p['kind'])
                merged[key] = {**merged.get(key, {}), **p, 'heartside_sha': p.get('source_revision')}
            return sorted(merged.values(), key=lambda p: (p['pack_date'], p['kind']), reverse=True)
        except (urllib.error.URLError, ValueError, KeyError) as e:
            print(f'Control Center read unavailable ({getattr(e, "code", type(e).__name__)}); showing local evidence only', file=sys.stderr)
    else:
        print(f'Control Center read unavailable ({why}); showing local evidence only', file=sys.stderr)
    return out


# ---------------------------------------------------------------------------
# Doctor and self-test.
# ---------------------------------------------------------------------------
def doctor():
    ok = True

    def line(good, what, fix=''):
        nonlocal ok
        ok = ok and good
        print(('ready     ' if good else 'NOT READY ') + what + ('' if good else f'\n          fix: {fix}'))

    line(sys.version_info >= (3, 9), f'Python {sys.version.split()[0]}', 'install Python 3.9 or newer')
    try:
        sha = head_sha()
        line(True, f'heartside main is readable (commit {sha[:10]})')
    except Exception as e:  # noqa: BLE001 - doctor reports, never raises
        line(False, 'heartside main is readable', f'network access is off or GitHub is blocked: {e}')
    try:
        n = len(store_products())
        line(n > 0, f'the live store answers ({n} products on sale)', 'check https://heartside.io/products.json opens')
    except Exception as e:  # noqa: BLE001
        line(False, 'the live store answers', f'network access is off or the store is locked: {e}')
    s = load_state()
    if s:
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(s['synced_at'])
        line(age < dt.timedelta(hours=26), f'last sync {int(age.total_seconds() // 3600)} hours ago (heartside {s["sha"][:10]})', 'run python3 growth.py sync')
        line(s.get('rules_ok', False), 'Heartside\'s rules match what the checker was written for',
             'read the changed sections in local/state/HEARTSIDE-NOW.md, then update RULES and RULES_BASIS in growth.py')
        ready_offers = offers.catalog(s)
        print(f'note      purchase-ready gifts: {sum(o["ready"] for o in ready_offers)}/{len(ready_offers)}; run growth.py readiness for details')
    else:
        line(False, 'a sync on this machine', 'run python3 growth.py sync')
    autos = json.load(open(os.path.join(HERE, 'automations.json')))['automations']
    line(all(os.path.exists(os.path.join(HERE, a['job'])) for a in autos),
         f'automations.json ({len(autos)} automations, every job file present)', 'a job file named in automations.json is missing')
    try:
        os.makedirs(os.path.join(LOCAL, 'packs'), exist_ok=True)
        line(True, 'local/ is writable (packs and lists stay on this machine)')
    except OSError as e:
        line(False, 'local/ is writable', str(e))
    _, why = control_center_takes_heartside()
    print(f'note      packs: {why}; until then they are saved in local/packs/ and printed in full')
    print('\nready to run; purchase copy is gated separately per gift' if ok else '\nnot ready: fix the lines above, then run doctor again')
    return 0 if ok else 1


def self_test():
    n = 0

    def t(name, cond):
        nonlocal n
        if not cond:
            sys.exit(f'self-test FAILED: {name}')
        n += 1

    cid = 'IG_EMO_REEL_C01_H03_V1_20261019'
    link = tracked('https://heartside.io/?view=gifts', cid)
    t('a tracked link is built from the creative id', link ==
      'https://heartside.io/?view=gifts&utm_source=instagram&utm_medium=organic_video&utm_campaign=hs_growth_202610&utm_content=' + cid)
    t('tracking replaces old tags', tracked('https://heartside.io/?utm_source=old&a=1', 'PIN_UTIL_PIN_C02_H01_V1_20261101') ==
      'https://heartside.io/?a=1&utm_source=pinterest&utm_medium=organic_social&utm_campaign=hs_growth_202611&utm_content=PIN_UTIL_PIN_C02_H01_V1_20261101')
    good = {'pack_date': '2026-10-19', 'kind': 'daily', 'venture': 'heartside', 'heartside_sha': '1028556df9',
            'headline': 'Monday pack', 'items': [{'platform': 'instagram', 'creative_id': cid,
                                                  'text': f'Your dog loves you too. Make their gift {link}'}]}
    t('a clean pack passes', check_pack(good, [29.0, 89.0, 24.0, 19.0]) == [])

    def bad(text, word, platform='instagram', pp=(29.0, 89.0, 24.0, 19.0)):
        return any(word in e for e in check_pack({**good, 'items': [{'platform': platform, 'text': text}]}, pp))
    t('an em dash is refused', bad('Love \u2014 Kuku', 'em dash'))
    t('a banned word is refused', bad('For your fur baby', 'bans'))
    t('"must-have" is refused', bad('The must-have gift', 'bans'))
    t('the not-X-but-Y turn is refused', bad("It's not a mug, it's a love letter", "it's not X"))
    t('"written by your dog" is refused', bad('Gifts written by your dog', 'retired'))
    t('"Your dog has notes" asks Krish', bad('Your dog has notes.', 'ask Krish'))
    t('the handle is fine', not bad('Follow @yourdoghasnotes', 'ask Krish'))
    t('the retired poster is refused', bad('The Annual Review is back', 'retired'))
    t('invented urgency is refused', bad('Only 3 left, hurry', 'urgency'))
    t('invented proof is refused', bad('Our bestseller, loved by thousands of dogs', 'proof'))
    t('a was-price is refused', bad('Was $39, now $29', 'was'))
    t('grief is refused', bad('In loving memory of Kuku', 'death'))
    t('UK spelling is refused', bad('A personalised gift in her favourite colour', 'UK spelling'))
    t('"dog mum" becomes mom', bad('For every dog mum', 'mom'))
    t('another email address is refused', bad('Write to hello@krishraja.com', 'customer-facing'))
    t('the store address passes', not bad('Write to krish@heartside.io', 'customer-facing'))
    t('an exclamation in body copy is refused', bad('So cute!', 'exclamation'))
    t('Biscuit may have one', not bad('Biscuit: My tail is going!', 'exclamation'))
    t('Biscuit may not have two', bad('Biscuit: Wow! Wow!', 'more than one'))
    t('Biscuit uses no emoji', bad('Biscuit: Good dog \U0001F436', 'emoji'))
    t('a hashtag wall is refused', bad('#a #b #c #d #e #f', 'hashtags'))
    t('an untracked store link is refused', bad('Make yours at https://heartside.io/', 'not tracked'))
    t('a mismatched creative id is refused', any('tracked as' in e for e in check_pack(
        {**good, 'items': [{'platform': 'instagram', 'creative_id': 'IG_EMO_REEL_C01_H03_V2_20261019', 'text': link}]})))
    t('a bad creative id is refused', any('creative_id' in e for e in check_pack(
        {**good, 'items': [{'platform': 'instagram', 'creative_id': 'reel-1', 'text': 'Hello'}]})))
    t('an unknown price is refused', bad('Just $35', 'price'))
    t('a live price passes', not bad('Mugs are $29', 'price'))
    t('a sum of two prices passes', not bad('Mug and ornament, $48 together', 'price'))
    t('a report can state revenue', not bad('Net sales $604 this week, 11 orders', 'price', 'other'))
    t('a brief may say what must not appear', not bad('Must not appear: memorial content, a countdown, AI customers', 'memorial', 'other'))
    t('a brief\'s on-screen line gets the copy rules', bad('Shot 1: the box\nOn screen: Only 3 left', 'urgency', 'other'))
    t('a brief\'s Biscuit line gets the copy rules', bad('Biscuit: Our bestseller', 'proof', 'other'))
    t('a store fix may name the abandoned checkout email', not bad('Turn on the abandoned checkout email in Shopify Messaging', 'death', 'store'))
    t('a store fix\'s copy line gets the copy rules', bad('Copy: Personalised gifts from your dog', 'UK spelling', 'store'))
    t('a brief\'s link is still tracked', bad('Landing: https://heartside.io/', 'not tracked', 'other'))
    t('a brief\'s em dash is still refused', bad('Shot 1 \u2014 the box', 'em dash', 'other'))
    t('an unknown kind is refused', any('kind' in e for e in check_pack({**good, 'kind': 'pitches'})))
    t('a pack without heartside_sha is refused', any('heartside_sha' in e for e in check_pack({**good, 'heartside_sha': ''})))
    t('a numbers row needs a note', any('note' in e for e in check_pack({**good, 'kind': 'numbers', 'items': [], 'numbers': [{'platform': 'shopify', 'orders': 3}]})))
    t('a guessed number is refused', any('number read today' in e for e in check_pack({**good, 'kind': 'numbers', 'items': [], 'numbers': [{'platform': 'shopify', 'orders': 'about 3', 'note': 'x'}]})))
    readme = ('# H\n\n**Picking this up? Read [`docs/V3.md`](docs/V3.md) first. Then [`docs/P.md`](docs/P.md).** '
              'What lives where: [`docs/SYNC.md`](docs/SYNC.md).\n\n- other [`docs/X.md`](docs/X.md)')
    paths, found = canon_paths(readme)
    t('canon comes from the README, in its order', found and paths[:3] == ['docs/V3.md', 'docs/P.md', 'docs/SYNC.md'])
    t('canon always adds the brand system', 'design/BRAND-SYSTEM.md' in paths and 'docs/X.md' not in paths)
    t('no "Picking this up" line falls back', canon_paths('# nothing')[0][:1] == ['docs/V3-GIFTS-FROM-YOUR-DOG.md'])
    t('the newest dated handover wins', newest_handover(['COWORK-HANDOVER-2026-10-15.md', 'HANDOVER-2026-10-20.md', 'HANDOFF.md',
                                                         'COWORK-PROMPT-2026-10-14-V3.md']) == 'docs/HANDOVER-2026-10-20.md')
    t('no handover is None', newest_handover(['HANDOFF.md', 'SYNC.md']) is None and newest_handover(None) is None)
    hp, _ = canon_paths(readme, 'docs/COWORK-HANDOVER-2026-10-15.md')
    t('the handover comes after the README\'s list and before the always-read files',
      hp[:4] == ['docs/V3.md', 'docs/P.md', 'docs/SYNC.md', 'docs/COWORK-HANDOVER-2026-10-15.md'] and hp[4] == 'README.md')
    doc = '# T\n\n## 1. A\none\n\n## 2. Rules\nno em dashes\n### 2.1 sub\nmore\n\n## 3. Next\nthree'
    t('a section runs to the next heading of its level', section(doc, '## 2. ') == '## 2. Rules\nno em dashes\n### 2.1 sub\nmore')
    t('a missing section is None', section(doc, '## 9. ') is None)
    files = {'README.md': readme, 'docs/V3.md': 'v3', 'docs/P.md': 'p', 'docs/SYNC.md': 's',
             'design/BRAND-SYSTEM.md': 'b', 'shopify/README.md': 'r'}
    st = {'sha': 'a' * 40, 'rules_ok': True, 'canon': {p: digest(files[p])[:16] for p in paths}}
    same = {**files}
    for p, _ in RULES_SOURCES:
        same.setdefault(p, None)
    global RULES_BASIS
    saved = RULES_BASIS
    RULES_BASIS = fingerprints(same)
    try:
        t('fresh when heartside has not moved', freshness({'heartside_sha': 'aaaaaaa'}, st, lambda: 'a' * 40, lambda p, s: same.get(p)) == [])
        t('fresh when heartside moved but no canon changed', freshness({'heartside_sha': 'aaaaaaa'}, st, lambda: 'b' * 40, lambda p, s: same.get(p)) == [])
        moved = {**same, 'docs/P.md': 'p changed'}
        t('stale when a canon file changed', any('docs/P.md' in e for e in freshness({'heartside_sha': 'aaaaaaa'}, st, lambda: 'b' * 40, lambda p, s: moved.get(p))))
        t('stale when the pack names another sync', any('last sync' in e for e in freshness({'heartside_sha': 'bbbbbbb'}, st, lambda: 'a' * 40, lambda p, s: same.get(p))))
        t('stopped when rules changed', any('rules changed' in e for e in freshness({'heartside_sha': 'aaaaaaa'}, {**st, 'rules_ok': False}, lambda: 'a' * 40, lambda p, s: same.get(p))))
        t('stopped with no sync', any('no sync' in e for e in freshness({'heartside_sha': 'aaaaaaa'}, None, lambda: 'a' * 40, lambda p, s: None)))
        newer = {**same, 'docs/COWORK-HANDOVER-2026-10-20.md': 'new handover'}
        t('stale when a newer handover appears', any('HANDOVER-2026-10-20' in e for e in freshness(
            {'heartside_sha': 'aaaaaaa'}, st, lambda: 'b' * 40, lambda p, s: newer.get(p), lambda s: ['COWORK-HANDOVER-2026-10-20.md'])))
        t('fresh when the docs listing is unavailable and nothing else moved', freshness(
            {'heartside_sha': 'aaaaaaa'}, st, lambda: 'b' * 40, lambda p, s: same.get(p), lambda s: None) == [])
    finally:
        RULES_BASIS = saved
    t('RULES_BASIS is filled in', all(v != 'FILL' and len(v) == 16 for v in RULES_BASIS.values()))
    import inspect
    t('a publish compares only with the published copy', 'load_state(published_only=publish)' in inspect.getsource(sync))
    gift = '## 3. The gift range (launch)\n\n| Gift | P | Price | x |\n|---|---|---|---|\n| **The Morning Mug** | #403 | $29 | $8 |\n| **The Tree Ornament** | #900 | $24, or $19 with another gift | $7 |'
    t('gift prices come from the canon table', canon_prices({'docs/V3.md': gift}) == [19.0, 24.0, 29.0])
    agents = open(os.path.join(HERE, 'AGENTS.md')).read()
    autos = json.load(open(os.path.join(HERE, 'automations.json')))['automations']
    for f in sorted(os.listdir(os.path.join(HERE, 'jobs'))):
        body = open(os.path.join(HERE, 'jobs', f)).read()
        m = re.search(r'Kind `(\w+)`', body)
        t(f'jobs/{f} names a kind', bool(m) and m.group(1) in KINDS or f == 'sync.md')
        t(f'jobs/{f} is on the schedule in AGENTS.md', f'jobs/{f}' in agents)
        t(f'jobs/{f} starts with a sync', 'growth.py sync' in body)
    for au in autos:
        t(f'automation "{au["name"]}" runs a job that exists', os.path.exists(os.path.join(HERE, au['job'])))
        t(f'automation "{au["name"]}" has a schedule rule', au['schedule'].startswith('RRULE:FREQ='))
        t(f'automation "{au["name"]}" never asks to post', not re.search(r'\b(post|publish|send)\b', au['prompt'], re.I))
    t('every job file has an automation', {a['job'] for a in autos} == {f'jobs/{f}' for f in os.listdir(os.path.join(HERE, 'jobs'))})
    for f in ('PLAYBOOK.md', 'BROWSER.md', 'knowledge/README.md', 'knowledge/organic-pet-commerce-engine.md', 'knowledge/organic-pet-growth-corpus.md',
              'knowledge/COPY-DOCTRINE.md'):
        t(f'{f} exists', os.path.exists(os.path.join(HERE, f)))
    # Preserved originals keep their exact bytes; the manifest is the record.
    for entry in json.load(open(os.path.join(HERE, 'knowledge/corpus-manifest.json')))['files']:
        path = os.path.join(HERE, entry['repository_path'])
        data = open(path, 'rb').read() if os.path.isfile(path) else None
        t(f'{entry["repository_path"]} matches its manifest bytes and SHA-256',
          data is not None and len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'])
    t('knowledge/COPY-DOCTRINE.md has no em dash', '\u2014' not in open(os.path.join(HERE, 'knowledge/COPY-DOCTRINE.md'), encoding='utf-8').read())
    ignored = open(os.path.join(HERE, '.gitignore')).read()
    t('local/ is never committed (the repository is public)', re.search(r'^/?local/?$', ignored, re.M) is not None)
    from engine.control_center import report_digest
    example = json.load(open(os.path.join(HERE, 'docs/control-center/engine-report.example.json')))
    t('the Control Center report digest reproduces the protocol worked example',
      report_digest(example) == example['payload_sha256'] == 'f4351324e84aa1baf6afd1bc4d2ffadb3039ab6399b2309c2717b89a26a0a517')
    recs = json.load(open(os.path.join(HERE, 'recommendations.json')))
    t('every recommendation has a stable proposal id and close event',
      all(re.fullmatch(r'heartside:rec:[a-z0-9-]+', r.get('id', '')) and re.fullmatch(r'[a-z][a-z0-9_]*', r.get('close_event', '')) for r in recs)
      and len({r['id'] for r in recs}) == len(recs))
    print(f'growth-heartside self-test passed: {n} checks')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--self-test', action='store_true')
    sub = ap.add_subparsers(dest='cmd')
    sy = sub.add_parser('sync'); sy.add_argument('--publish', action='store_true'); sy.add_argument('--quiet', action='store_true')
    cn = sub.add_parser('canon'); cn.add_argument('--full', action='store_true')
    sub.add_parser('store')
    lk = sub.add_parser('link'); lk.add_argument('url'); lk.add_argument('creative_id')
    c = sub.add_parser('check'); c.add_argument('file')
    s = sub.add_parser('post'); s.add_argument('file')
    r = sub.add_parser('read'); r.add_argument('--days', type=int, default=7); r.add_argument('--kind')
    sub.add_parser('doctor')
    from engine import cli
    cli.add_commands(sub)
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.cmd in cli.COMMANDS:
        try:
            return cli.run(a, sys.modules[__name__])
        except (ValueError, KeyError, TypeError, ImportError, OSError, subprocess.CalledProcessError) as e:
            sys.exit(f'Not ready: {e}')
    if a.cmd == 'sync':
        st = sync(publish=a.publish, quiet=a.quiet)
        print(f'heartside_sha: {st["sha"]}')
        if not st['rules_ok']:
            print('STOP: Heartside\'s rules changed. No pack can pass until growth.py is updated (AGENTS.md, rule 2).')
            sys.exit(2)
        return
    if a.cmd == 'canon':
        st = load_state()
        if not st:
            sys.exit('No sync yet: run python3 growth.py sync first.')
        for i, p in enumerate(st['canon'], 1):
            print(f'{i}. {p}  (heartside {st["sha"][:10]})')
            if a.full:
                print('\n' + (raw(p, st['sha']) or '(missing at this commit)') + '\n' + '-' * 72)
        return
    if a.cmd == 'store':
        for p in store_products():
            print(f'{p["title"]:40} {", ".join(f"${x:g}" for x in p["prices"]):16} {"on sale" if p["available"] else "unavailable"}  {p["url"]}')
        return
    if a.cmd == 'link':
        try:
            print(tracked(a.url, a.creative_id))
        except ValueError as e:
            sys.exit(str(e))
        return
    if a.cmd in ('check', 'post'):
        try:
            pack = json.load(open(a.file))
        except (OSError, ValueError) as e:
            sys.exit(f'Not ready: could not read pack JSON ({e})')
        st = load_state()
        purchase = False
        if isinstance(pack, dict) and isinstance(pack.get('items'), list):
            for item in pack['items']:
                if not isinstance(item, dict) or not isinstance(item.get('text'), str):
                    continue
                public = item['text']
                if item.get('platform') in INTERNAL:
                    public = '\n'.join(line for line in public.splitlines() if PUBLIC_LINE.match(line))
                purchase = purchase or item.get('intent') == 'buy' or bool(PRICE.search(public)) or bool(offers.BUY.search(public))
        catalog_errors = []
        if purchase and st:
            try:
                st = {**st, 'store': store_products(),
                      'homepage_v3': 'data-hs3-config' in http(STORE + '/', accept_json=False),
                      'synced_at': dt.datetime.now(dt.timezone.utc).isoformat()}
            except (urllib.error.URLError, ValueError, KeyError) as e:
                catalog_errors.append(f'purchase copy blocked: current public offers could not be confirmed ({e})')
        errs = check_pack(pack, (st or {}).get('price_points') or (), state=st)
        errs += catalog_errors
        if isinstance(pack, dict) and (pack.get('kind') == 'daily' or pack.get('production')):
            from engine.media import verify
            errs += verify(Path(HERE), pack.get('production'), pack)
        try:
            if isinstance(pack, dict):
                errs += freshness(pack, st, head_sha, raw, docs_listing)
        except (urllib.error.URLError, OSError) as e:
            errs.append(f'could not confirm heartside is unchanged since the sync ({e}); with no answer, nothing passes')
        if errs:
            print('Not ready:\n  ' + '\n  '.join(errs))
            sys.exit(1)
        if a.cmd == 'check':
            print(f'ready: {len(pack.get("items") or [])} drafts, written against heartside {pack["heartside_sha"][:10]}')
            return
        return store_pack(pack)
    if a.cmd == 'read':
        print(json.dumps(read_packs(a.days, a.kind), indent=1))
        return
    if a.cmd == 'doctor':
        sys.exit(doctor())
    ap.print_help()


if __name__ == '__main__':
    main()
