"""Repeatable draft-only jobs. No Control Centre requests or social writes.

Scheduled jobs run from the same canonical automations.json as authoring sessions.
Independent jobs continue after a failure; failed jobs remain retryable. Local
runs have a lease; GitHub Actions also serializes the cross-machine writer.
"""
from contextlib import contextmanager, closing
import datetime as dt
import html
import json
import re
import os
from pathlib import Path
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

from . import ai_answers, assets, dashboard, insights, ledger, media, offers, review, retention, social

# A failed job's reason is printed in the public Actions log, so it is cut down to the engine's own words.
REDACT = (
    (re.compile(r'(https?://[^\s?#]+)[?#]\S*'), r'\1'),  # a query string can carry a buyer's or dog's name
    (re.compile(r'[^\s@]+@[^\s@]+\.[a-z]{2,}', re.I), '[address]'),
    (re.compile(r'\b(?:gen1|shp[a-z]{2}|gh[opsu]|github_pat)_[A-Za-z0-9_]+'), '[token]'),
)


def failure_reason(error):
    """Why a job failed, in the engine's own words and safe for a public log, or None.

    Only a ValueError carries a reason: this engine raises one for each of its own checks (a product
    render that left the live gallery, a pack that fails the copy or freshness rules, a STOP), and
    those name a role, a gift, a rule or a file, never a customer. Any other error keeps its type
    alone, so a provider's response body or a token is never written down.
    """
    if not isinstance(error, ValueError):
        return None
    text = ' '.join(str(error).split())
    for pattern, replacement in REDACT:
        text = pattern.sub(replacement, text)
    return text[:500] or None


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


def campaign(root, db, day, state=None):
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
        if spec.get('intent') != 'buy' or offers.purchase_campaign(spec, state):
            return offers.purchase_campaign(spec, state) if spec.get('intent') == 'buy' else spec
    # A stable seven-concept rotation is a fallback, not invented trend research.
    offset = dt.date.fromisoformat(day).toordinal() % len(bank)
    spec = json.loads(bank[offset].read_text())
    hooks = json.loads((Path(root) / 'config/hooks.json').read_text())['concepts'][spec['concept']]
    variant = (dt.date.fromisoformat(day).toordinal() // len(bank)) % len(hooks)
    original = spec['scenes'][0]['headline']
    opening = hooks[variant]
    spec['scenes'][0]['headline'] = opening
    spec['hook'] = 'H' + str(variant + 1).zfill(2)
    # Native caption lengths/tone remain in the source bank; replace only the
    # specific opening. The whole output passes the same copy/render checks.
    for platform in ('instagram', 'facebook', 'tiktok'):
        spec['captions'][platform] = spec['captions'][platform].replace(original, opening)
    spec['native_hooks'] = {'facebook': opening, 'tiktok': hooks[(variant + 1) % len(hooks)]}
    spec['mechanism'] += ' Scheduled campaign-bank hypothesis; no trend or performance claim.'
    if dt.date.fromisoformat(day).toordinal() % 3 == 0:
        return offers.purchase_campaign(spec, state) or spec
    return spec


def evidence_pack(state, day, kind, headline, items):
    return {'venture': 'heartside', 'pack_date': day, 'kind': kind,
            'heartside_sha': state['sha'], 'headline': headline, 'items': items}


def demand(query='personalized dog gifts'):
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


ANSWERS_URL = 'https://heartside.io/blogs/answers/'
BLOG_PATH = re.compile(r'/blogs/answers/[a-z0-9][a-z0-9_-]*')
GAP_WORDS = {'no_page': 'Heartside has no page that answers it',
             'not_retrieved': 'the assistants do not find Heartside\'s page for it',
             'retrieved_not_cited': 'the assistants read Heartside\'s page but cite another',
             'cited_not_first': 'Heartside is cited, but not first'}


def handle(question):
    return re.sub(r'[^a-z0-9]+', '-', question.lower()).strip('-')


def _passes(growth, state, day, text, creative_id=None):
    """Whether one draft passes the same check the finished pack must pass (growth.check_pack, the copy linter)."""
    item = {'platform': 'store', 'text': text, **({'creative_id': creative_id} if creative_id else {})}
    pack = evidence_pack(state, day, 'answers', 'Answers library: one line checked', [item])
    return not growth.check_pack(pack, state.get('price_points', []), state=state)


def kit_item(kit, match, number, growth, state, day):
    """One brief from one of AEO's win kits (`match` is its bank row, or None), or None, and how many lines were dropped.

    Every line of the kit's own words is checked alone by the copy linter and dropped, with a count, when it fails:
    never rewritten, so no word is invented. The kit's title (else its question) is the `Title:` line; without one
    that passes, the kit is not briefed. The whole brief is checked again, and dropped whole if it still fails, so
    the pack's own check (and the public log it would write to) never sees a kit's words.
    """
    question = kit['question'] or kit['title']
    creative_id = f'WEB_UTIL_ARTICLE_C{number:02d}_H01_V1_{day.replace("-", "")}'
    title = next((f'Title: {t}' for t in (kit['title'], kit['question']) if t and _passes(growth, state, day, f'Title: {t}')), None)
    candidates = [f'Headline: {h}' for h in kit['h2s']]
    candidates += [f'Capsule rule: {r}' for r in kit['capsule']['rules']]
    candidates += [f'Capsule must cover: {c}' for c in kit['capsule']['must_cover']]
    if kit['beat']:
        candidates.append('Pages to beat (hosts only): ' + ', '.join(b['host'] for b in kit['beat']) + '.')
    candidates += [f'Site fix for a heartside build session: {f["gate"] or "a site gate"}'
                   + (f' on {f["host"]}' if f['host'] else '') + f': {f["fix"]}'
                   for f in kit['site_fixes'] if ai_answers.for_heartside(f)]
    kept = [c for c in candidates if _passes(growth, state, day, c)]
    dropped = len(candidates) - len(kept)
    if not title:
        return None, dropped + 1
    gap = GAP_WORDS.get(kit['gap_class'])
    lines = [title, 'Brief: AEO-Engine\'s win kit for this question' + (f' ({gap})' if gap else '')
             + '. Draft to docs/GEO-AEO.md section 4 in Heartside\'s own words; the kit is a brief, never copy.']
    lines += kept
    lines.append('Link for the one honest mention of Heartside: ' + growth.tracked('https://heartside.io/', creative_id))
    lines.append(demand(match['seed'] if match and isinstance(match.get('seed'), str) else question))
    text = '\n'.join(lines)
    if not _passes(growth, state, day, text, creative_id):
        return None, dropped + len(lines)
    target = kit['target']
    # AEO-Engine suggests `/answers/<slug>` for every new page (62-kits.ts, suggestedPath), a path a Shopify store
    # cannot serve: Heartside's Answers library is the blog at /blogs/answers/<handle> (jobs/answers.md step 5), so a
    # suggested path is used only when it is already there, and otherwise the handle is the job's own rule.
    path = target['suggested_path']
    url = target['url'] if target['url'] and target['kind'] == 'update_page' else (
        'https://heartside.io' + path if path and BLOG_PATH.fullmatch(path) else ANSWERS_URL + handle(question))
    priority = kit['priority']
    return {'platform': 'store', 'creative_id': creative_id,
            'target_name': 'Answers library: ' + (match['id'] if match else 'a new question') + ', from AEO-Engine\'s win kit',
            'target_url': url,
            'why': ('AEO-Engine\'s win kit' + (f', priority {priority:g}' if priority is not None else '')
                    + ', taken before bank order (jobs/answers.md step 2).'),
            'text': text}, dropped


def answers_brief(root, growth, state, day, now=None):
    """The Wednesday Answers brief: two questions, AEO-Engine's win kits first (best priority first), then bank order.

    The hosted runner has no writer: it briefs; an authoring session drafts. Kits come from what the daily Control
    Center run, or `growth.py cc kits`, kept under gitignored local/ (engine/ai_answers.py); this runner never
    contacts Control Center. A kit for a placement on another site only (`off_site_only`) is not a page to write
    here and is passed over, counted. Without kits the brief is the bank's next two questions, as before. The
    result carries counts and bank ids only, never a kit's words: it is printed in the public Actions log.
    """
    bank = json.loads((Path(root) / 'knowledge/aeo-question-bank.json').read_text())
    rows = [q for q in bank['questions'] if isinstance(q, dict) and isinstance(q.get('question'), str)]
    numbers = [int(q['id'][1:]) for q in rows if re.fullmatch(r'q\d{2,3}', str(q.get('id')))]
    fresh = max(numbers, default=0) + 1
    items, ids, covered, dropped_lines, dropped_kits, off_site = [], [], set(), 0, 0, 0
    for kit in ai_answers.saved_kits(root, now):
        if len(items) == 2:
            break
        if kit['target']['kind'] == 'off_site_only':
            off_site += 1  # a placement on another site, not a page of the Answers library
            continue
        question = kit['question'] or kit['title']
        match = next((q for q in rows if ai_answers.question_key(q['question']) == ai_answers.question_key(question)), None)
        number = int(match['id'][1:]) if match and re.fullmatch(r'q\d{2,3}', str(match.get('id'))) else fresh
        if number > 999:
            dropped_kits += 1
            continue
        item, dropped = kit_item(kit, match, number, growth, state, day)
        dropped_lines += dropped
        if item is None:
            dropped_kits += 1
            continue
        if match:
            ids.append(match['id'])
        else:
            fresh += 1
        covered.add(ai_answers.question_key(question))
        items.append(item)
    used = len(items)
    nxt = sorted((q for q in rows if q.get('status') in ('todo', 'refresh') and ai_answers.question_key(q['question']) not in covered),
                 key=lambda q: (q['status'] != 'refresh', q['priority']))[:2 - used]
    items += [{'platform': 'store', 'target_name': 'Answers library: ' + q['id'],
               'target_url': ANSWERS_URL + handle(q['question']),
               'why': 'Next ' + q['status'] + ' question in tier ' + str(q['tier']) + ' (docs/GEO-AEO.md section 4).',
               'text': 'Title: ' + q['question'] + '\nBrief: draft to docs/GEO-AEO.md section 4, leading to ' + q['leads_to'] + '.\n' + demand(q['seed'])}
              for q in nxt]
    held = None if used else ai_answers.kits_hold(root)
    headline = ('Answers library: the next two questions to draft, AEO-Engine\'s win kits first' if used
                else 'Answers library: the next two questions to draft' + (f' (held: {held})' if held else ''))
    pack = evidence_pack(state, day, 'answers', headline, items)
    return pack, {'questions': ids + [q['id'] for q in nxt], 'kits': used, 'kits_dropped': dropped_kits,
                  'kit_lines_dropped': dropped_lines, 'kits_off_site': off_site, 'published': 0,
                  'kits_hold': held}


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
            spec = campaign(root, db, day, state)
            write_json(out / 'spec.json', spec)
            pack, manifest = media.render(root, spec, state, growth.check_pack, day=day, link_builder=growth.tracked)
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
                write_json(out / 'social.json', social.status(db))
            result = {'data_access': 'Imported aggregate ledger only. Native dashboards and the Shopify connector are session capabilities, not credentials in this runner.'}
        elif job == 'radar':
            report = social.status(db)
            pack = evidence_pack(state, day, 'radar', 'Demand evidence, engagement tests and the first-follower monitor', [
                {'platform': 'other', 'target_name': 'Public search suggestions', 'why': 'A research input, not evidence of sales or volume.', 'text': demand()}]
                + ([{'platform': 'other', 'target_name': 'Engagement tests and first followers',
                     'why': 'Recorded social history (growth.py social status); each line names its owner and next action.',
                     'text': '\n'.join(social.lines(report))}] if social.lines(report) else []))
            result = {'native_comments': 'not_available', 'social_open': [t['test_id'] for t in report['tests'] if t['stage'] not in ('evaluated', 'held', 'cancelled')]}
        elif job == 'store':
            ready = offers.catalog(state)
            pack = evidence_pack(state, day, 'conversion', 'Public store readiness and acquisition handoff', [
                {'platform': 'other', 'target_name': 'Product readiness', 'target_url': 'https://github.com/krishanraja/heartside/pull/13',
                 'text': json.dumps(ready, indent=2) + '\nProduct fixes belong in heartside. No store setting was changed.'}])
            result = {'ready_gifts': sum(bool(o['ready']) for o in ready), 'canonical_gifts': len(ready)}
        elif job == 'answers':
            pack, result = answers_brief(root, growth, state, day)
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
        raise ValueError('job must be one of the declared jobs in automations.json, or all')
    due = [(name, day) for name in names if job == 'all' or job == name] if job else due_jobs(config, now)
    index = assets.local_path(root, 'local/automation/index.json')
    with lease(root, now):
        current = growth.sync(quiet=True) if growth else {}
        if growth and not current.get('rules_ok'):
            raise ValueError('STOP: current product rules changed; previous packs must not be reused')
        bank_fingerprint = ledger.digest({str(p.relative_to(root)): assets.sha256(p) for p in sorted((Path(root) / 'campaigns').glob('*.json'))} | ({'hooks': assets.sha256(Path(root) / 'config/hooks.json')} if (Path(root) / 'config/hooks.json').exists() else {}))
        base_fingerprint = ledger.digest({'runner': 3, 'campaign_bank': bank_fingerprint, 'renderer': media.VERSION, 'renderer_source': media.renderer_fingerprint(), 'sha': current.get('sha'),
                                          'store': current.get('store'), 'homepage_v3': current.get('homepage_v3')})
        history = json.loads(index.read_text()) if index.exists() else {}
        results = []
        for name, date in due:
            key = date + '/' + name
            prior = history.get(key, {})
            fingerprint = base_fingerprint
            if name == 'answers' and (kits := ai_answers.saved_kits(root, now)):
                # Kits that arrive later the same day rebuild the brief; only their digest is in the index.
                fingerprint = ledger.digest({'source': fingerprint, 'kits': kits})
            if name in {'numbers', 'report'}:
                with closing(ledger.connect(Path(root) / 'local/engine.sqlite3')) as db:
                    rows = [dict(r) for r in db.execute('SELECT * FROM metrics ORDER BY platform,source,start,end,timezone')]
                fingerprint = ledger.digest({'source': fingerprint, 'metrics': rows})
                if name == 'report':
                    with closing(ledger.connect(Path(root) / 'local/engine.sqlite3')) as db:
                        insights.setup(db)
                        creative_rows = [dict(r) for r in db.execute('SELECT creative_id,revision,status,updated_at,published_url FROM creatives ORDER BY creative_id,revision')]
                        insight_rows = [dict(r) for r in db.execute('SELECT * FROM insights ORDER BY creative_id,revision,source')]
                    fingerprint = ledger.digest({'source': fingerprint, 'creatives': creative_rows, 'insights': insight_rows})
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
                # Never a provider's response body or a token: the type, and the engine's own reason (failure_reason).
                history[key].update(status='failed', error_type=type(error).__name__)
                if reason := failure_reason(error):
                    history[key]['error'] = reason
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
