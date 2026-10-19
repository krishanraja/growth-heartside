"""Report this engine's work to Control Center through the growth engine protocol 1.0.0.

One run: journal the attempt, read today's directive, read what the engine
already has (product truth and the ledger restored from the latest
checkpoint), report it, read the report back by digest, read Krish's
decisions, then close the attempt. It renders nothing, calls no paid
provider and never posts, sends, publishes or spends. A matching decision only
records that Krish said yes to exactly one payload; he still acts by hand.
"""
import datetime as dt
import json
import os
from pathlib import Path
import re
import sqlite3
from zoneinfo import ZoneInfo

from . import ledger, offers
from .control_center import CODE, Client, ProtocolError, report_digest, sha256

ENGINE_ID, PRODUCT_SLUG, SLUG, COMMAND = 'growth-heartside', 'heartside', 'heartside', 'directive'
DEFAULT_URL = 'https://controlcenter.krishraja.com'
LONDON, NEW_YORK = ZoneInfo('Europe/London'), ZoneInfo('America/New_York')
ATTEMPT_FILE = 'local/control-center/attempt.json'
PR13 = 'https://github.com/krishanraja/heartside/pull/13'
ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9:._-]{0,119}$')
HTTPS = re.compile(r'^https://\S+$')
MAX_PROPOSALS, MAX_EVENTS = 10, 40
CHANNELS = {'IG': 'instagram', 'FB': 'facebook', 'TT': 'tiktok', 'PIN': 'pinterest', 'YT': 'youtube'}
NAMES = {'instagram': 'Instagram', 'facebook': 'Facebook', 'tiktok': 'TikTok', 'pinterest': 'Pinterest', 'youtube': 'YouTube'}


def stamp(moment):
    return moment.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def midnight(day, zone=LONDON):
    return dt.datetime.combine(day, dt.time(), zone)


def money(value):
    value = round(float(value), 2)
    return int(value) if value.is_integer() else value


def fit(text, limit):
    """Shorten at a sentence or word boundary, never mid-word."""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    end = cut.rfind('. ')
    return cut[:end + 1] if end > limit // 2 else cut[:cut.rfind(' ')].rstrip(' ,;:')


# ---------------------------------------------------------------------------
# Objectives: unknown is null with a reason, a measured zero is 0.
# ---------------------------------------------------------------------------
def month_window(now):
    end = now.astimezone(LONDON).date()
    first = end.replace(day=1)
    if first == end:  # on the 1st, the month that just closed
        first = (end - dt.timedelta(days=1)).replace(day=1)
    return first, end


def net_sales(db, now):
    first, end = month_window(now)
    base = {'key': 'net_sales_usd', 'unit': 'USD', 'timezone': 'Europe/London'}
    empty = {'value': None, 'window_start': None, 'window_end': None, 'availability': 'missing'}
    if db is None:
        return {**base, **empty, 'reason': 'No engine ledger checkpoint was available to this run, so no Shopify aggregate could be read'}
    ends = sorted({dt.date.fromisoformat(r['end']) for r in db.execute(
        "SELECT end FROM metrics WHERE platform='shopify' AND timezone='Europe/London' AND start>=? AND end<=?",
        (first.isoformat(), end.isoformat()))}, reverse=True)
    for last in ends:
        if last <= first:
            continue
        # ledger.summary never adds overlapping windows; require every day covered.
        summary = ledger.summary(db, first.isoformat(), last.isoformat(), 'Europe/London')
        if summary['covered_days'].get('net_sales') != summary['days']:
            continue
        reading = {**base, 'value': money(summary['totals']['net_sales']),
                   'window_start': midnight(first).isoformat(), 'window_end': midnight(last).isoformat()}
        if last == end:
            return {**reading, 'availability': 'measured', 'reason': None}
        return {**reading, 'availability': 'stale',
                'reason': f'Imported Shopify net sales run only through {last - dt.timedelta(days=1)}; later days are not imported yet'}
    return {**base, **empty, 'reason': f'No imported Shopify aggregate covers every day from {first} to {end - dt.timedelta(days=1)} '
            '(Europe/London). Missing is not zero'}


def organic_orders():
    return {'key': 'organic_orders', 'value': None, 'unit': 'orders', 'window_start': None, 'window_end': None,
            'timezone': 'Europe/London', 'availability': 'missing',
            'reason': 'Organic order attribution is not measured on the runner. Store order totals do not show which post '
                      'caused a sale, and creative UTM observations are lifetime snapshots, not weekly windows'}


# ---------------------------------------------------------------------------
# Proposals, events and holds from what the engine already keeps.
# ---------------------------------------------------------------------------
def recommendation_proposals(recommendations):
    out = []
    for rec in recommendations:
        if (not isinstance(rec, dict) or not ID.match(str(rec.get('id', ''))) or not CODE.match(str(rec.get('close_event', '')))
                or not CODE.match(str(rec.get('objective_key') or 'none'))):
            raise ValueError('each recommendation needs a stable id, a lower_snake close_event and objective_key')
        payload = {k: rec[k] for k in ('title', 'why', 'next_action', 'closes_when')}
        why = rec['why'] + ' Next: ' + rec['next_action']
        if len(rec['title']) > 160 or len(why) > 1000 or len(rec['closes_when']) > 500:
            raise ValueError(f'recommendation {rec["id"]} is longer than the protocol allows')
        out.append({'proposal_id': rec['id'], 'title': rec['title'], 'why': why, 'kind': 'advice', 'wall': 'none',
                    'amount_usd': None, 'channel': None, 'objective_key': rec.get('objective_key'), 'exact_payload': None,
                    'payload_sha256': sha256(payload),
                    'evidence': [{'label': rec['title'], 'url': rec['target_url']}] if HTTPS.match(rec.get('target_url', '')) else [],
                    'close_condition': {'event': rec['close_event'], 'reference': rec['closes_when']}, 'expires_at': None})
    return out


def caption_index(root):
    """Stored pack items by creative id: the hot run workspace and local packs."""
    index = {}
    for pattern in ('local/automation/runs/*/daily-pack/pack.json', 'local/automation/runs/*/daily-pack/history/*.json',
                    'local/packs/*.json', 'local/packs/history/*.json'):
        for path in sorted(Path(root).glob(pattern)):
            try:
                pack = json.loads(path.read_text())
            except (OSError, ValueError):
                continue
            for item in (pack.get('items') or []) if isinstance(pack, dict) else []:
                if isinstance(item, dict) and isinstance(item.get('creative_id'), str) and isinstance(item.get('text'), str):
                    index.setdefault(item['creative_id'], []).append(item)
    return index


def expiry(creative_id):
    """Hot media is pruned seven New York days after its creative date (engine/retention.py)."""
    match = re.search(r'_(\d{8})$', creative_id)
    if not match:
        return None
    return midnight(dt.datetime.strptime(match[1], '%Y%m%d').date() + dt.timedelta(days=7), NEW_YORK)


def post_payload_sha256(creative_id, revision, channel, caption):
    return sha256({'caption': caption, 'channel': channel, 'creative_id': creative_id, 'revision': revision})


def post_proposals(root, db, now):
    """Approved creatives whose media and caption still match their render manifest."""
    from . import media, operations
    rows = db.execute('''SELECT * FROM (SELECT *, row_number() OVER (PARTITION BY creative_id
      ORDER BY updated_at DESC, rowid DESC) AS rank FROM creatives) WHERE rank=1 AND status='approved'
      ORDER BY updated_at DESC, creative_id''').fetchall()
    index = caption_index(root) if rows else {}
    proposals, holds = [], []
    for row in rows:
        cid, revision = row['creative_id'], row['revision']
        channel, expires = CHANNELS.get(cid.split('_')[0]), expiry(cid)
        try:
            if not channel or not ID.match('heartside:post:' + cid) or not re.fullmatch(r'[a-f0-9]{64}', revision):
                raise ValueError('unsupported creative')
            if expires is None or expires <= now:
                raise ValueError('expired')
            operations.validate_creative(root, db, cid, revision)
            expected = json.loads(row['manifest'])['copy_sha256'][cid]
            item = next(i for i in index.get(cid, []) if media.copy_digest(i) == expected)
            if len(item['text']) > 8000:
                raise ValueError('caption too long')
        except (ValueError, KeyError, TypeError, StopIteration, OSError):
            holds.append({'reason': 'An approved creative was not proposed: its media or caption could not be verified',
                          'detail': f'{cid} at revision {revision[:12]}. Render it again or restore its checkpoint, then record a fresh approval.'})
            continue
        try:
            mechanism = json.loads(row['spec']).get('mechanism') or ''
        except ValueError:
            mechanism = ''
        why = f'Reviewed and approved at revision {revision[:12]}. The caption and media match the render manifest. ' + mechanism
        proposals.append({'proposal_id': 'heartside:post:' + cid, 'title': f'Post {cid} on {NAMES[channel]}',
                          'why': fit(why.strip(), 1000), 'kind': 'prepared', 'wall': 'post', 'amount_usd': None,
                          'channel': channel, 'objective_key': 'organic_orders', 'exact_payload': item['text'],
                          'payload_sha256': post_payload_sha256(cid, revision, channel, item['text']), 'evidence': [],
                          'close_condition': {'event': 'creative_published', 'reference': cid}, 'expires_at': stamp(expires)})
    return proposals, holds


def publication_events(db, now, days=14):
    rows = db.execute('''SELECT c.creative_id, c.published_url, max(e.recorded_at) AS at FROM creatives c
      JOIN creative_events e ON e.creative_id=c.creative_id AND e.revision=c.revision AND e.status='published'
      WHERE c.status='published' GROUP BY c.creative_id, c.revision ORDER BY at DESC, c.creative_id''').fetchall()
    events = []
    for row in rows:
        at = dt.datetime.fromisoformat(row['at'])
        if at.tzinfo is None or at < now - dt.timedelta(days=days):
            continue
        events.append({'event': 'creative_published', 'proposal_id': 'heartside:post:' + row['creative_id'], 'at': stamp(at),
                       'evidence_url': row['published_url'] if HTTPS.match(row['published_url'] or '') else None})
    return events[:MAX_EVENTS]


def product_holds(state):
    """The product constraint handed to heartside PR 13, read from current product truth."""
    gifts = offers.catalog(state)
    ready = sum(1 for gift in gifts if gift['ready'])
    if not gifts or ready < len(gifts):
        detail = (f'heartside PR 13 ({PR13}): {ready} of {len(gifts)} canonical gifts are live at the approved price. Audience material continues.'
                  if gifts else f'heartside PR 13 ({PR13}): the canonical gift range was not read from Heartside\'s canon at this commit.')
        return [{'reason': 'Purchase claims held until the public catalog matches the canonical gifts', 'detail': detail}]
    if not state.get('homepage_v3'):
        seen = 'could not be checked' if state.get('homepage_v3') is None else 'is not public yet'
        return [{'reason': 'Conversion editions held until the V3 homepage is public',
                 'detail': f'heartside PR 13 ({PR13}): all {len(gifts)} canonical gifts are live, but the V3 homepage {seen}. Audience material continues.'}]
    return []


def latest_decisions(decisions):
    latest = {}
    for d in decisions or []:
        if isinstance(d, dict) and isinstance(d.get('proposal_id'), str):
            if d['proposal_id'] not in latest or str(d.get('decided_at')) > str(latest[d['proposal_id']].get('decided_at')):
                latest[d['proposal_id']] = d
    return latest


def build_report(*, root, state, db, now, run_id, mode, directive, recommendations, degraded=()):
    """The report envelope, exactly engine-report.schema.json, sealed with its digest."""
    activity, holds = [], []
    body = (directive or {}).get('directive') or {}
    action = body.get('next_action') or {}
    if body:
        activity.append(f'Read directive {fit(str(body.get("directive_id")), 80)}, chosen by {fit(str(directive.get("chosen_by")), 20)}: '
                        f'next action {fit(str(action.get("proposal_id") or "none"), 130)}.')
        if str(action.get('proposal_id') or '').startswith('heartside:post:'):
            activity.append('Today\'s push is a post. The engine never posts; it waits for Krish to post by hand and record the permalink.')
    else:
        activity.append('No directive was available for today; the run reported what the engine already has.')
    activity.append(f'Read Heartside product truth at {state["sha"][:10]}, synced {state.get("synced_at", "at an unknown time")}.')
    activity += list(degraded)

    proposals, events = [], []
    if not state.get('rules_ok'):
        holds.append({'reason': 'Heartside rules changed since growth.py was last updated',
                      'detail': 'No copy is proposed until a person updates growth.py in an interactive session (AGENTS.md, rule 2).'})
    holds += product_holds(state)
    if db is not None:
        latest = db.execute('''SELECT status, count(*) AS n FROM (SELECT status, row_number() OVER (PARTITION BY creative_id
          ORDER BY updated_at DESC, rowid DESC) AS rank FROM creatives) WHERE rank=1 GROUP BY status ORDER BY status''').fetchall()
        activity.append('Read the engine ledger: ' + (', '.join(f'{r["n"]} {r["status"]}' for r in latest) or 'no creative revisions recorded') + '.')
        if state.get('rules_ok'):
            posts, post_holds = post_proposals(root, db, now)
            proposals += posts
            holds += post_holds
        events = publication_events(db, now)
        if events:
            activity.append(f'Reported {len(events)} publication(s) Krish recorded in the last 14 days.')
    proposals += recommendation_proposals(recommendations)
    for pid, decision in latest_decisions(body.get('decisions_since')).items():
        current = next((p for p in proposals if p['proposal_id'] == pid), None)
        if current is None:
            continue
        if decision.get('payload_sha256') != current['payload_sha256']:
            activity.append(f'The payload for {pid} changed since Krish decided on it, so it goes back to him.')
        elif decision.get('decision') in ('declined', 'done'):
            proposals.remove(current)
            activity.append(f'Krish {"declined" if decision["decision"] == "declined" else "marked done"} {pid} on this exact payload; it is not proposed again.')
        elif decision.get('decision') == 'approved':
            activity.append(f'Krish approved {pid} on this exact payload. Only he acts on it, by hand.')
    posts = [p for p in proposals if p['wall'] == 'post']
    room = MAX_PROPOSALS - (len(proposals) - len(posts))
    if len(posts) > room:  # newest first; the rest wait for the next report
        holds.append({'reason': 'More approved creatives than one report can carry',
                      'detail': f'{len(posts) - room} older approved creative(s) wait for the next report.'})
        proposals = [p for p in proposals if p['wall'] != 'post' or p in posts[:room]]
    if posts_count := sum(1 for p in proposals if p['wall'] == 'post'):
        activity.append(f'Proposed {posts_count} approved creative(s) for posting, each bound to its creative, revision and caption.')
    activity.append('Proposed no paid boost: the budget is $0 and the engine recommends no spend.')
    activity.append('Nothing was rendered, posted, sent, published or spent by this run.')

    status = 'degraded' if degraded or db is None else 'held' if holds else 'ready'
    report = {'schema_version': '1.0.0', 'engine_id': ENGINE_ID, 'product_slug': PRODUCT_SLUG, 'run_id': run_id, 'mode': mode,
              'observed_at': stamp(now), 'source': {'revision': state['sha'], 'captured_at': stamp(dt.datetime.fromisoformat(state['synced_at'].replace('Z', '+00:00')))},
              'status': status, 'objectives': [net_sales(db, now), organic_orders()],
              'activity': [{'line': fit(line, 500), 'evidence_url': None} for line in activity][:40],
              'proposals': proposals, 'events': events, 'holds': holds[:40]}
    report['payload_sha256'] = report_digest(report)
    return report


# ---------------------------------------------------------------------------
# The loop.
# ---------------------------------------------------------------------------
def directive_day(env):
    match = re.fullmatch(r'heartside:(\d{4}-\d{2}-\d{2})', env.get('CC_DIRECTIVE_ID', '').strip())
    return match[1] if match else None


def run_identity(day, mode, env, now):
    """Stable per engine per day and kind; a rerun or manual run never reuses the dispatch id."""
    if env.get('GITHUB_EVENT_NAME') == 'repository_dispatch':
        kind = 'directive'
    else:
        run = env.get('GITHUB_RUN_ID', '')
        kind = 'manual-' + (run if run.isdigit() else now.strftime('%H%M%S'))
    attempt = env.get('GITHUB_RUN_ATTEMPT', '1')
    if attempt.isdigit() and int(attempt) > 1:
        kind += f'-a{int(attempt)}'
    return f'{SLUG}:{day}:' + ('synthetic-' if mode == 'synthetic' else '') + kind


def deliver(client, report):
    """POST once, then read back. A 409 or an uncertain write is read back, never retried."""
    try:
        ack = client.post_report(report)
    except ProtocolError as error:
        uncertain = error.status is None or error.status >= 500
        if not uncertain and error.status != 409:
            raise
        try:
            stored = client.read_report(report['run_id'])
        except ProtocolError:
            if uncertain:
                raise ProtocolError('report_outcome_unknown') from None
            raise
        if stored and stored.get('payload_sha256') == report['payload_sha256']:
            return {'replayed': True, 'readback': 'match'}
        if uncertain:
            raise ProtocolError('report_outcome_unknown') from None
        raise ProtocolError('report_conflict' if stored or error.code == 'conflict' else error.code, 409) from None
    stored = client.read_report(report['run_id'])
    if not stored or stored.get('payload_sha256') != report['payload_sha256']:
        raise ProtocolError('readback_mismatch')
    return {'replayed': bool(ack.get('replayed')), 'readback': 'match'}


def bind_decisions(decisions, proposals):
    current = {p['proposal_id']: p['payload_sha256'] for p in proposals}
    out = []
    for d in decisions:
        pid = d.get('proposal_id') if isinstance(d, dict) else None
        if not isinstance(pid, str) or not ID.match(pid):
            continue
        binding = ('not_in_this_report' if pid not in current else
                   'matches_current_payload' if d.get('payload_sha256') == current[pid] else 'payload_changed')
        out.append({'proposal_id': pid, 'decision': d.get('decision') if d.get('decision') in ('approved', 'declined', 'done') else 'unknown',
                    'binding': binding})
    return out


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def start(root, client, mode, now, env):
    """Journal the attempt before any source is read. The local file holds no credential."""
    day = directive_day(env) or now.astimezone(LONDON).date().isoformat()
    run_id = run_identity(day, mode, env, now)
    record = {'attempt_id': run_id, 'command': COMMAND, 'run_id': run_id, 'status': 'started', 'phase': 'start',
              'error_code': None, 'started_at': stamp(now)}
    local = {**record, 'mode': mode, 'github_run': env.get('GITHUB_RUN_ID'), 'terminal': None, 'start_error': None}
    try:
        client.attempt(record)
    except ProtocolError as error:
        local['start_error'] = error.code
    _write(Path(root) / ATTEMPT_FILE, local)
    if local['start_error']:
        raise ProtocolError(local['start_error'])
    return local


def current_attempt(root, mode, env):
    path = Path(root) / ATTEMPT_FILE
    try:
        local = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    if local.get('mode') != mode or local.get('github_run') != env.get('GITHUB_RUN_ID') or local.get('terminal'):
        return None
    return local


def finish(root, client, local, status, code, phase, now):
    """Exactly one terminal record per attempt; a second call is a no-op."""
    if local.get('terminal'):
        return local['terminal']
    record = {'attempt_id': local['attempt_id'], 'command': COMMAND, 'run_id': local['run_id'], 'status': status,
              'phase': phase, 'error_code': code, 'started_at': local['started_at'], 'finished_at': stamp(now)}
    try:
        client.attempt(record)
        recorded = True
    except ProtocolError:
        recorded = False
    local['terminal'] = {'status': status, 'error_code': code, 'phase': phase, 'recorded': recorded}
    _write(Path(root) / ATTEMPT_FILE, local)
    return local['terminal']


def capture(growth):
    """Product truth first; a failed sync falls back to the last published snapshot and says so."""
    try:
        return growth.sync(quiet=True), []
    except Exception as error:  # network or GitHub limits; never echo a response body
        state = growth.load_state()
        if not state or not state.get('sha') or not state.get('synced_at'):
            raise ProtocolError('product_state_missing') from None
        return state, [f'Product sync failed ({type(error).__name__}); used the last published snapshot instead.']


def run(root, growth, client, mode, env, recommendations, now=None, clock=None):
    clock = clock or (lambda: dt.datetime.now(dt.timezone.utc))
    now = now or clock()
    summary = {'engine_id': ENGINE_ID, 'mode': mode, 'posted': 0, 'sent': 0, 'spent_usd': 0}
    local = current_attempt(root, mode, env)
    if local is None:
        try:
            local = start(root, client, mode, now, env)
        except ProtocolError as error:
            local = json.loads((Path(root) / ATTEMPT_FILE).read_text())
            summary.update(run_id=local['run_id'], attempt=finish(root, client, local, 'failed', error.code, 'start', clock()))
            return summary
    summary['run_id'] = local['run_id']
    phase, db = 'directive', None
    try:
        directive = client.directive(local['run_id'].split(':')[1])
        expected = env.get('CC_DIRECTIVE_ID', '').strip()
        if directive and expected and directive['directive'].get('directive_id') != expected:
            raise ProtocolError('directive_mismatch')
        phase = 'capture'
        state, degraded = capture(growth)
        database = Path(root) / 'local/engine.sqlite3'
        if database.exists():
            db = ledger.connect(database)
        else:
            degraded.append('No engine checkpoint was available, so the ledger could not be read.')
        phase = 'plan'
        report = build_report(root=root, state=state, db=db, now=now, run_id=local['run_id'], mode=mode,
                              directive=directive, recommendations=recommendations, degraded=degraded)
        phase = 'report'
        summary['delivery'] = deliver(client, report)
        summary.update(status=report['status'], payload_sha256=report['payload_sha256'],
                       objectives={o['key']: o['availability'] for o in report['objectives']},
                       proposals=[p['proposal_id'] for p in report['proposals']], holds=len(report['holds']))
        phase = 'decisions'
        summary['decisions'] = bind_decisions(client.decisions(stamp(now - dt.timedelta(days=7))), report['proposals'])
        summary['attempt'] = finish(root, client, local, 'succeeded', None, 'finish', clock())
    except ProtocolError as error:
        status = 'unknown' if error.code == 'report_outcome_unknown' else 'failed'
        summary['attempt'] = finish(root, client, local, status, error.code, phase, clock())
    except (ValueError, KeyError, TypeError, OSError, sqlite3.Error):
        summary['attempt'] = finish(root, client, local, 'failed', 'engine_error', phase, clock())
    finally:
        if db is not None:
            db.close()
    return summary


def main(root, growth, action, mode, code=None, env=None):
    env = os.environ if env is None else env
    token = env.get('CONTROL_CENTER_ENGINE_TOKEN', '').strip()
    base = env.get('CONTROL_CENTER_URL', '').strip() or DEFAULT_URL
    if not token:
        print('Not ready: CONTROL_CENTER_ENGINE_TOKEN is not set in this environment. No request was made.')
        return 1
    try:
        client = Client(base, token, SLUG)
    except ProtocolError as error:
        print(f'Not ready: {error.code}. No request was made.')
        return 1
    now = dt.datetime.now(dt.timezone.utc)
    if action == 'start':
        try:
            local = start(root, client, mode, now, env)
        except ProtocolError as error:
            local = current_attempt(root, mode, env)
            terminal = finish(root, client, local, 'failed', error.code, 'start', now) if local else None
            print(json.dumps({'attempt': 'start_failed', 'error_code': error.code, 'terminal': terminal}))
            return 1
        print(json.dumps({'run_id': local['run_id'], 'attempt': 'started'}))
        return 0
    if action == 'finish':
        local = current_attempt(root, mode, env)
        if local is None:
            print(json.dumps({'attempt': 'nothing_open'}))
            return 0
        result = finish(root, client, local, 'failed', code if CODE.match(code or '') else 'workflow_failed', 'capture', now)
        print(json.dumps({'run_id': local['run_id'], 'attempt': result}))
        return 1
    recommendations = json.loads((Path(growth.HERE) / 'recommendations.json').read_text())
    summary = run(root, growth, client, mode, env, recommendations, now)
    print(json.dumps(summary, indent=2))
    outcome = summary.get('attempt') or {}
    if env.get('GITHUB_STEP_SUMMARY'):
        with open(env['GITHUB_STEP_SUMMARY'], 'a') as out:
            out.write(f'# Control Center report\n\n- run: {summary.get("run_id")}\n- mode: {mode}\n'
                      f'- attempt: {outcome.get("status")} {outcome.get("error_code") or ""}\n'
                      f'- report status: {summary.get("status", "not reported")}\n'
                      f'- objectives: {summary.get("objectives", {})}\n- proposals: {len(summary.get("proposals", []))}\n'
                      '\nNothing was posted, sent, published or spent.\n')
    return 0 if outcome.get('status') == 'succeeded' and outcome.get('recorded') else 1
