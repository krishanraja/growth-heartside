"""Social operating history: engagement tests and the first-follower monitor.

Krish, 2026-11-09, on the engagement desk's handover: "We need to upgrade the Growth-Heartside engine to ensure
it learns from the attached Markdown file". The handover asked for continuity inside the existing engine, not a
parallel system. So these records arrive through the existing operator-event import (`growth.py events import`,
type `social`), get the same receipts and replay protection (operations.py), live in local/engine.sqlite3 beside
the creative ledger, and travel in the existing checkpoint (state_store.py). The radar and report jobs read them
back, and `growth.py social status` prints what is outstanding, who owns it and what not to do.

Records are append-only. A correction is a new record naming the one it corrects in `supersedes`; nothing is
rewritten. A failed observation is kept as `unavailable` and never replaces the last successful count.

Only public brand facts belong here: brand-authored text, public brand post URLs and aggregate counts. No
commenter, follower or customer identity, ever (AGENTS.md rule 6).
"""
import datetime as dt
import hashlib
import json
import re

CHANNELS = ('instagram', 'facebook', 'tiktok', 'pinterest')
HOSTS = {'instagram': ('instagram.com',), 'facebook': ('facebook.com',), 'tiktok': ('tiktok.com',),
         'pinterest': ('pinterest.com', 'pinterest.co.uk')}
# The handover's lifecycle (Krish's engagement desk, 7 to 9 Nov 2026): proposed, approved, handed off,
# live verified, measuring, evaluated. held and cancelled stop a test without deleting it.
STAGES = ('proposed', 'approved', 'handed_off', 'live_verified', 'evaluated', 'held', 'cancelled')
OWNERS = ('krish', 'engagement', 'publishing', 'production', 'audience', 'engine')
MONITOR = ('watching', 'delivered', 'retired')
WINDOW_HOURS = 48
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
FIELDS = {
    'engagement': {'kind', 'test_id', 'stage', 'channel', 'at', 'at_precision', 'source', 'target_url', 'text', 'approval',
                   'interaction', 'viewer_route', 'decision_rule', 'evidence', 'next_action', 'owner',
                   'outcome', 'supersedes'},
    'follower_check': {'kind', 'channel', 'at', 'at_precision', 'status', 'count', 'source', 'evidence', 'supersedes'},
    'monitor': {'kind', 'channel', 'state', 'at', 'at_precision', 'source', 'evidence', 'supersedes'},
}
REQUIRED = {'engagement': {'kind', 'test_id', 'stage', 'channel', 'at', 'source'},
            'follower_check': {'kind', 'channel', 'at', 'status', 'source'},
            'monitor': {'kind', 'channel', 'state', 'at', 'source'}}


def setup(db):
    db.execute('CREATE TABLE IF NOT EXISTS social_events(event_id TEXT PRIMARY KEY, kind TEXT NOT NULL, '
               'subject TEXT NOT NULL, at TEXT NOT NULL, recorded_at TEXT NOT NULL, body TEXT NOT NULL)')


def when(value):
    try:
        stamp = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except ValueError:
        raise ValueError(f'not an ISO time: {value}')
    if stamp.tzinfo is None:
        raise ValueError(f'a time needs its zone, in UTC: {value}')
    return stamp.astimezone(dt.timezone.utc)


def text_sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def validate(record):
    if not isinstance(record, dict) or record.get('kind') not in FIELDS:
        raise ValueError('a social record is an engagement, follower_check or monitor record')
    kind = record['kind']
    if not REQUIRED[kind] <= set(record) or not set(record) <= FIELDS[kind]:
        raise ValueError(f'{kind} uses the exact allowlisted fields: {sorted(FIELDS[kind])}')
    if record['channel'] not in CHANNELS:
        raise ValueError(f'channel must be one of {CHANNELS}')
    when(record['at'])
    if record.get('at_precision') not in (None, 'minute', 'day'):
        raise ValueError('at_precision is minute or day; a day-precision time is the date at 00:00 UTC, never a guessed hour')
    flat = json.dumps(record, ensure_ascii=False)
    if EMAIL.search(flat) or len(flat) > 6000:
        raise ValueError('social records hold public brand facts only: no email address, no long transcript')
    if kind == 'engagement':
        if record['stage'] not in STAGES:
            raise ValueError(f'stage must be one of {STAGES}')
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,63}', record['test_id']):
            raise ValueError('test_id is lowercase words joined by hyphens')
        if record.get('owner') not in (None, *OWNERS):
            raise ValueError(f'owner must be one of {OWNERS}')
        url = record.get('target_url')
        if url is not None and not (url.startswith('https://') and any(h in url.split('/')[2] for h in HOSTS[record['channel']])):
            raise ValueError('target_url is the public brand post on the named channel')
        if record['stage'] in ('approved', 'handed_off') and not record.get('text'):
            raise ValueError('an approved or handed-off test carries its exact text')
        if record['stage'] == 'approved' and not record.get('approval'):
            raise ValueError("an approval carries Krish's exact words and their scope")
        if record['stage'] in ('live_verified', 'evaluated') and not record.get('evidence'):
            raise ValueError('live and evaluated stages carry the evidence that verified them')
    elif kind == 'follower_check':
        if record['status'] not in ('counted', 'unavailable'):
            raise ValueError('a follower check is counted or unavailable; unavailable is never zero')
        if record['status'] == 'counted' and not (isinstance(record.get('count'), int) and record['count'] >= 0):
            raise ValueError('a counted follower check carries a whole count')
        if record['status'] == 'unavailable' and 'count' in record:
            raise ValueError('an unavailable check carries no count')
    elif record['state'] not in MONITOR:
        raise ValueError(f'monitor state must be one of {MONITOR}')
    return record


def record(db, event_id, body, recorded_at):
    """Store one validated record. Exact approved text can never change under the same test."""
    setup(db)
    body = validate(body)
    subject = body.get('test_id') or body['channel']
    if body['kind'] == 'engagement' and body.get('text'):
        for row in db.execute("SELECT body FROM social_events WHERE kind='engagement' AND subject=?", (subject,)):
            earlier = json.loads(row['body'])
            if earlier.get('text') and earlier['stage'] in ('approved', 'handed_off', 'live_verified') and earlier['text'] != body['text']:
                raise ValueError(f'{subject}: the approved text cannot change; a new wording is a new test')
    with db:
        db.execute('INSERT INTO social_events VALUES(?,?,?,?,?,?)',
                   (event_id, body['kind'], subject, when(body['at']).isoformat(), recorded_at, json.dumps(body, ensure_ascii=False, sort_keys=True)))


def rows(db, kind):
    setup(db)
    found = [dict(json.loads(r['body']), event_id=r['event_id']) for r in
             db.execute('SELECT event_id, body FROM social_events WHERE kind=? ORDER BY at, rowid', (kind,))]
    gone = {r['supersedes'] for r in found if r.get('supersedes')}
    return [r for r in found if r['event_id'] not in gone]


def status(db, now=None):
    """What is true, what is outstanding, who owns it, and what must not be done again."""
    now = now or dt.datetime.now(dt.timezone.utc)
    tests = {}
    for r in rows(db, 'engagement'):
        t = tests.setdefault(r['test_id'], {'test_id': r['test_id'], 'channel': r['channel'], 'history': []})
        t['history'].append({k: r[k] for k in ('stage', 'at', 'source') if k in r} | ({'evidence': r['evidence']} if r.get('evidence') else {}))
        for k in ('target_url', 'text', 'approval', 'interaction', 'viewer_route', 'decision_rule', 'outcome'):
            if r.get(k) is not None:
                t[k] = r[k]
        t['stage'] = r['stage']
        if r['stage'] == 'live_verified':
            t['live_at'] = r['at']
        if r.get('next_action'):
            t['next_action'], t['owner'] = r['next_action'], r.get('owner', 'engine')
    for t in tests.values():
        if t.get('text'):
            t['text_sha256'] = text_sha(t['text'])
        reached = {h['stage'] for h in t['history']}
        if t['stage'] in ('held', 'cancelled', 'evaluated'):
            t.setdefault('next_action', {'evaluated': 'Feed the result to the radar and the weekly report; repeat only as the decision rule says.'}.get(t['stage'], 'Stopped. Nothing to do unless Krish reopens it.'))
            t.setdefault('owner', 'engine')
        elif 'live_verified' in reached:
            ends = when(t['live_at']) + dt.timedelta(hours=WINDOW_HOURS)
            t['window_ends'] = ends.isoformat()
            if now < ends:
                t['next_action'], t['owner'] = f'Measuring until {ends:%Y-%m-%d %H:%M} UTC. Record replies and aggregate changes at the end of the window; post nothing new to gather data.', 'engagement'
            else:
                t['next_action'], t['owner'] = 'Window closed. Count unique substantive replies (brand activity excluded), record outcome and the keep/iterate/hold/retire decision as an evaluated record.', 'engagement'
        elif 'handed_off' in reached:
            t['next_action'], t['owner'] = ('Publishing desk: check the native post and the desk receipt first. If the exact comment is already live, record live_verified with its permalink and time. '
                                            'Post it once only if it is absent. Never send it twice.'), 'publishing'
        elif 'approved' in reached:
            t['next_action'], t['owner'] = 'Hand the exact approved text, unchanged, to the publishing desk and record handed_off.', 'engagement'
        else:
            t['next_action'], t['owner'] = 'Waiting for Krish to approve the exact text and target.', 'krish'
        t['do_not'] = ['send the comment again before checking the native post',
                       'treat approval or handoff as publication',
                       'reuse this approval for any other comment, post or emoji']
    channels = {}
    for c in CHANNELS:
        checks = [r for r in rows(db, 'follower_check') if r['channel'] == c]
        good = [r for r in checks if r['status'] == 'counted']
        states = [r for r in rows(db, 'monitor') if r['channel'] == c]
        channels[c] = {
            'monitor': states[-1]['state'] if states else 'not_monitored',
            'last_successful': {k: good[-1][k] for k in ('at', 'count', 'source')} if good else None,
            'last_attempt': {k: checks[-1][k] for k in ('at', 'status', 'source') if k in checks[-1]} if checks else None,
        }
        last = checks[-1] if checks else None
        channels[c]['current'] = ('unknown: the latest check failed; the last successful count still stands as history, not as now'
                                  if last and last['status'] == 'unavailable' else
                                  f"{last['count']} at {last['at']}" if last else 'never checked')
        failures = 0
        for r in reversed(checks):
            if r['status'] != 'unavailable':
                break
            failures += 1
        channels[c]['consecutive_failures'] = failures
    watching = [c for c, v in channels.items() if v['monitor'] == 'watching']
    return {'tests': list(tests.values()), 'channels': channels, 'monitor_remaining': watching,
            'rules': ['Aggregate views, likes or comments never establish what a follower did.',
                      'Follower counts are milestone triggers, not the North Star; sales are.',
                      'An unavailable count is unknown, never zero.',
                      'One follower is not a rate and not a winner.']}


def lines(report):
    """Plain lines for a pack item or the terminal; no public copy rules apply because none of it is posted."""
    out = []
    for t in report['tests']:
        out.append(f"Test {t['test_id']} ({t['channel']}): {t['stage']}. Owner: {t['owner']}. Next: {t['next_action']}")
        if t.get('target_url'):
            out.append(f"  target {t['target_url']}")
        if t.get('text'):
            out.append(f"  exact approved text (sha256 {t['text_sha256'][:16]}): {t['text']}")
        if t.get('window_ends'):
            out.append(f"  48h window from verified publication ends {t['window_ends']}")
    for c, v in report['channels'].items():
        if v['monitor'] == 'not_monitored' and not v['last_attempt']:
            continue
        last = v['last_successful']
        out.append(f"Followers {c}: monitor {v['monitor']}; current {v['current']}; last successful "
                   + (f"{last['count']} at {last['at']}" if last else 'none') + f"; failed checks in a row {v['consecutive_failures']}")
    if report['monitor_remaining']:
        out.append('First-follower monitor still watching: ' + ', '.join(report['monitor_remaining']) + '. At the first verified count of 1 or more, bring one engagement test for review.')
    return out
