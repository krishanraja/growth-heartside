"""Repeatable draft-only jobs. No Control Centre requests or social writes.

Scheduled jobs run from the same canonical automations.json as authoring sessions.
Independent jobs continue after a failure; failed jobs remain retryable. Local
runs have a lease; GitHub Actions also serializes the cross-machine writer.
"""
from contextlib import contextmanager, closing
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

from . import assets, dashboard, insights, ledger, media, offers, review, retention


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def due_jobs(config, now):
    if not now.tzinfo:
        raise ValueError('scheduler clock needs an offset')
    local = now.astimezone(ZoneInfo(config['timezone']))
    result = []
    for entry in config['automations']:
        rule = dict(part.split('=', 1) for part in entry['schedule'].removeprefix('RRULE:').split(';'))
        due = local.replace(hour=int(rule['BYHOUR']), minute=int(rule['BYMINUTE']), second=0, microsecond=0)
        weekdays = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
        if rule['FREQ'] == 'WEEKLY' and local.weekday() not in [weekdays[x] for x in rule['BYDAY'].split(',')]:
            continue
        if rule['FREQ'] not in {'WEEKLY', 'DAILY'}:
            raise ValueError('unsupported scheduler frequency')
        if now >= due:
            result.append((Path(entry['job']).stem, local.date().isoformat()))
    return result


@contextmanager
def lease(root, now):
    path = assets.local_path(root, 'local/automation/runner.lock')
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        # Crash recovery is deliberately slower than the 60-minute job timeout.
        age = now.timestamp() - path.stat().st_mtime
        if age <= 7200:
            raise ValueError('another engine run holds the two-hour writer lease')
        path.unlink()
        handle = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(handle, 'w') as stream:
        stream.write(json.dumps({'pid': os.getpid(), 'started_at': now.isoformat()}))
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


def campaign(root, db, day):
    bank = sorted((Path(root) / 'campaigns').glob('*.json'))
    if not bank:
        raise ValueError('campaign bank is empty')
    candidates = insights.decisions(db)['decisions']
    winner = next((r for r in candidates if r['decision'] == 'replicate_candidate'), None)
    if winner:
        row = db.execute('SELECT spec FROM creatives WHERE creative_id=? AND revision=?', (winner['creative_id'], winner['revision'])).fetchone()
        spec = json.loads(row['spec']); spec['variation'] += 1
        first = spec['scenes'][0]
        first['headline'], first['text'] = first['text'], first['headline']
        spec['hook'] = 'H' + str(int(spec['hook'][1:]) + 1).zfill(2)
        spec['native_hooks'] = {platform: first['headline'] for platform in ('facebook', 'tiktok')}
        # Keep a declared experiment rather than inventing a causal winner.
        spec['mechanism'] += ' Exploratory replication after observed native evidence; hold the mechanism constant.'
        return spec
    # A stable seven-concept rotation is a fallback, not invented trend research.
    offset = dt.date.fromisoformat(day).toordinal() % len(bank)
    spec = json.loads(bank[offset].read_text())
    spec['mechanism'] += ' Scheduled campaign-bank hypothesis; no trend or performance claim.'
    return spec


def evidence_pack(state, day, kind, headline, items):
    return {'venture': 'heartside', 'pack_date': day, 'kind': kind,
            'heartside_sha': state['sha'], 'headline': headline, 'items': items}


def demand():
    query = 'personalized dog gifts'
    url = 'https://suggestqueries.google.com/complete/search?' + urllib.parse.urlencode({'client': 'firefox', 'q': query})
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'HeartsideGrowth/1.0'})
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read(100000))
        suggestions = [s for s in data[1] if isinstance(s, str) and len(s) < 150][:5]
        if not suggestions:
            raise ValueError('no suggestions returned')
        return 'Observed public Google suggestions (not search volumes or trends), retrieved ' + ledger.now() + ': ' + '; '.join(suggestions) + '\nSource: ' + url
    except (OSError, ValueError, TypeError, IndexError):
        return 'Public search suggestions unavailable. No current search demand, comment or trend claim is inferred. Native social dashboards are unavailable to this runner.'


def run_job(root, growth, job, day):
    # Every job refreshes product truth before doing any work.
    state = growth.sync(quiet=True)
    if not state.get('rules_ok'):
        raise ValueError('STOP: product rules changed; no content produced')
    out = assets.local_path(root, f'local/automation/runs/{day}/{job}')
    out.mkdir(parents=True, exist_ok=True)
    with closing(ledger.connect(Path(root) / 'local/engine.sqlite3')) as db:
        if job == 'sync':
            result = {'heartside_sha': state['sha'], 'synced_at': state['synced_at'], 'gifts': offers.catalog(state)}
            write_json(out / 'sync.json', result)
            return result
        if job == 'daily-pack':
            spec = campaign(root, db, day)
            write_json(out / 'spec.json', spec)
            pack, manifest = media.render(root, spec, state, growth.check_pack, day=day)
            for item in pack['items']:
                ledger.record_render(db, item['creative_id'], manifest['revision'], spec, manifest)
            result = review.bundle(root, pack, str((out / 'review.zip').relative_to(root)))
        elif job in {'numbers', 'report'}:
            # Data stays in the verified store timezone, never the job timezone.
            end = dt.datetime.now(ZoneInfo('Europe/London')).date()
            first = end.replace(day=1)
            if first == end:
                first = (end - dt.timedelta(days=1)).replace(day=1)
            numbers, progress = dashboard.build(db, state, first.isoformat(), end.isoformat(), 'Europe/London', day,
                growth_source(root), json.loads((Path(root) / 'recommendations.json').read_text()))
            pack = numbers if job == 'numbers' else progress
            if job == 'report':
                write_json(out / 'decisions.json', insights.decisions(db))
            result = {'data_access': 'Imported aggregate ledger only. Native dashboards and the Shopify connector are session capabilities, not credentials in this runner.'}
        elif job == 'radar':
            pack = evidence_pack(state, day, 'radar', 'Demand evidence and research access', [
                {'platform': 'other', 'target_name': 'Public search suggestions', 'why': 'A research input, not evidence of sales or volume.', 'text': demand()}])
            result = {'native_comments': 'not_available'}
        elif job == 'store':
            ready = offers.catalog(state)
            pack = evidence_pack(state, day, 'conversion', 'Public store readiness and acquisition handoff', [
                {'platform': 'other', 'target_name': 'Product readiness', 'target_url': 'https://github.com/krishanraja/heartside/pull/13',
                 'text': json.dumps(ready, indent=2) + '\nProduct fixes belong in heartside. No store setting was changed.'}])
            result = {'ready_gifts': sum(bool(o['ready']) for o in ready), 'canonical_gifts': len(ready)}
        elif job == 'creators':
            pack = evidence_pack(state, day, 'partners', 'Creator research handoff, no automated outreach', [
                {'platform': 'other', 'target_name': 'Creator evidence boundary',
                 'text': 'Use the creator acquisition operating brief in docs/CREATORS.md. Check each profile and latest relevant post again before a personalized draft. Gift only within the 20-creator US allowance, disclose the gift and request usage permission. No message was sent and no gift was ordered.'}])
            result = {'outreach_sent': 0, 'verified_creator_profiles': 0, 'research_access': 'not_available_to_hosted_runner'}
        else:
            raise ValueError('unknown scheduled job')
        errors = growth.check_pack(pack, state.get('price_points', []), state=state)
        if pack.get('production'):
            errors += media.verify(root, pack['production'], pack)
        errors += growth.freshness(pack, state, growth.head_sha, growth.raw, growth.docs_listing)
        if errors:
            raise ValueError('; '.join(errors))
        previous_pack = out / 'pack.json'
        if previous_pack.exists():
            previous = json.loads(previous_pack.read_text())
            if previous != pack:
                write_json(out / 'history' / (ledger.digest(previous) + '.json'), previous)
        write_json(out / 'pack.json', pack)
        (out / 'pack.md').write_text(growth.render_md(pack))
        # Internal local storage only. The user explicitly excluded Control Centre.
        packs = Path(root) / 'local/packs'; packs.mkdir(parents=True, exist_ok=True)
        write_json(packs / f'{day}-{pack["kind"]}.json', pack)
        (packs / f'{day}-{pack["kind"]}.md').write_text(growth.render_md(pack))
        return {**result, 'pack': str((out / 'pack.json').relative_to(root)), 'heartside_sha': state['sha']}


def growth_source(root):
    import subprocess
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(['git', 'status', '--porcelain'], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
    return revision + (' (working tree has changes)' if dirty else '')


def tick(root, growth, now=None, job=None, force=False):
    now = now or dt.datetime.now(dt.timezone.utc)
    config = json.loads((Path(root) / 'automations.json').read_text())
    day = now.astimezone(ZoneInfo(config['timezone'])).date().isoformat()
    names = [Path(a['job']).stem for a in config['automations']]
    if job and job not in names + ['all']:
        raise ValueError('job must be one of the seven declared jobs or all')
    due = [(name, day) for name in names if job == 'all' or job == name] if job else due_jobs(config, now)
    index = assets.local_path(root, 'local/automation/index.json')
    with lease(root, now):
        current = growth.sync(quiet=True) if growth else {}
        if growth and not current.get('rules_ok'):
            raise ValueError('STOP: current product rules changed; previous packs must not be reused')
        base_fingerprint = ledger.digest({'runner': 2, 'renderer': media.VERSION, 'renderer_source': media.renderer_fingerprint(), 'sha': current.get('sha'),
                                          'store': current.get('store'), 'homepage_v3': current.get('homepage_v3')})
        history = json.loads(index.read_text()) if index.exists() else {}
        results = []
        for name, date in due:
            key = date + '/' + name
            prior = history.get(key, {})
            fingerprint = base_fingerprint
            if name in {'numbers', 'report'}:
                with closing(ledger.connect(Path(root) / 'local/engine.sqlite3')) as db:
                    rows = [dict(r) for r in db.execute('SELECT * FROM metrics ORDER BY platform,source,start,end,timezone')]
                fingerprint = ledger.digest({'source': fingerprint, 'metrics': rows})
            completed = prior.get('status') == 'completed' and prior.get('input_fingerprint') == fingerprint
            if completed and name == 'daily-pack' and prior.get('result', {}).get('creative_revision'):
                try:
                    previous = json.loads(assets.local_path(root, prior['result']['pack']).read_text())
                    completed = not media.verify(root, previous.get('production'), previous)
                except (OSError, ValueError, KeyError, TypeError):
                    completed = False
            if not force and completed:
                results.append({'job': name, **prior, 'status': 'already_completed'})
                continue
            # Persist the claim before work. A crash leaves it retryable after lease expiry.
            attempt = int(prior.get('attempts', 0)) + 1
            if not force and prior.get('status') in {'running', 'failed'} and prior.get('last_attempt') and now - dt.datetime.fromisoformat(prior['last_attempt']) < dt.timedelta(minutes=15):
                results.append({'job': name, 'status': 'retry_deferred'})
                continue
            history[key] = {'status': 'running', 'attempts': attempt, 'last_attempt': now.isoformat(), 'input_fingerprint': fingerprint}
            write_json(index, history)
            try:
                result = run_job(root, growth, name, date)
                history[key].update(status='completed', result=result, completed_at=ledger.now())
            except Exception as error:
                # Do not serialize arbitrary provider response bodies or tokens.
                history[key].update(status='failed', error_type=type(error).__name__)
            write_json(index, history)
            results.append({'job': name, **history[key]})
        retained = retention.prune(root, day)
        # Checkpoints omit duplicate review ZIP bytes. Rebuild the latest bundle
        # after restore from its checked immutable media and pack evidence.
        latest = sorted((Path(root) / 'local/automation/runs').glob('*/daily-pack/pack.json'))
        if latest and not latest[-1].with_name('review.zip').exists():
            pack_path = latest[-1]
            pack = json.loads(pack_path.read_text())
            if not media.verify(root, pack.get('production'), pack):
                rebuilt = review.bundle(root, pack, str(pack_path.with_name('review.zip').relative_to(root)))
                completed_key = pack['pack_date'] + '/daily-pack'
                if completed_key in history:
                    history[completed_key].setdefault('result', {}).update(rebuilt)
                    write_json(index, history)
        result = {'retention': retained, 'checked_at': now.isoformat(), 'timezone': config['timezone'], 'results': results,
                  'external_writes': False, 'control_centre_work': False}
        write_json(Path(root) / 'local/automation/latest.json', result)
        return result
