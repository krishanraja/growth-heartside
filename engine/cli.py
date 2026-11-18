"""Commands share the existing growth.py entrypoint and local/ boundary."""
from contextlib import closing
import json
import sys
from pathlib import Path

from . import assets, ledger, offers


COMMANDS = {'readiness', 'assets', 'render', 'metrics', 'creatives', 'ledger', 'dashboard', 'reporting-access', 'run', 'snapshot', 'insights', 'provider', 'bundle', 'events', 'library', 'cc', 'attribution', 'examples', 'social', 'drive', 'floor', 'still', 'ads'}


def add_commands(sub):
    ex = sub.add_parser('examples', help='Check the breed example batch against heartside\'s brief'); ex.add_argument('action', choices=['check']); ex.add_argument('--stage', type=int, required=True); ex.add_argument('--only', help='one job id, for the pilot')
    sub.add_parser('attribution', help='Read which orders came from organic posts, as aggregates (docs/ENGINE.md)')
    library = sub.add_parser('library'); library.add_argument('--date'); library.add_argument('--heartside-dir')
    soc = sub.add_parser('social', help='Engagement tests and the first-follower monitor: what is outstanding and who owns it (engine/social.py)')
    soc.add_argument('action', choices=['status']); soc.add_argument('--json', action='store_true')
    ads = sub.add_parser('ads', help="Audit every recorded boost against Krish's boost rulings, with evidence coverage (engine/ad_audit.py). Reads only.")
    ads.add_argument('action', choices=['audit']); ads.add_argument('--traffic', help='an aggregate sessions file: sessions by channel and period (docs/PAID-BOOSTS.md)')
    ads.add_argument('--boosts', help='boost records as JSON (a list, or an events file); default: the ones imported into local/engine.sqlite3')
    ads.add_argument('--now', help='ISO time to audit at (default: now)'); ads.add_argument('--json', action='store_true')
    drive = sub.add_parser('drive', help="Check a Drive listing against config/drive-map.json (docs/DRIVE-MAP.md)")
    drive.add_argument('action', choices=['audit']); drive.add_argument('listing')
    floor = sub.add_parser('floor', help="What Krish rejected and the check each rejection added (factory/floor.json)")
    floor.add_argument('--format', dest='fmt', help='only the entries for one format: reel, still, carousel, meme, comment, card')
    still = sub.add_parser('still', help='A generated dog still: roll its prompt, reserve its credits, bind its review, check it against the floor (factory/README.md)')
    steps = still.add_subparsers(dest='step', required=True)
    from factory import dog_roll
    dog_roll.add_arguments(steps.add_parser('roll', help='roll real-pet dog still prompts (factory/dog_roll.py)'))
    res = steps.add_parser('reserve', help='check a roll at the prompt stage, then reserve its prepaid credits (docs/PROVIDERS.md)')
    res.add_argument('roll', help='a roll id (dog-...) or a roll record file')
    res.add_argument('--script-score', type=float, required=True, help='the tier 2 score of the script on paper, before any spend')
    res.add_argument('--by', required=True, help='who made the still (the maker; the reviewer must be someone else)')
    res.add_argument('--provider', default='higgsfield')
    res.add_argument('--credits', required=True, help="the provider's own quote for this still, in credits")
    res.add_argument('--quote-source', required=True); res.add_argument('--quoted-at', required=True, help='ISO time with offset, within 24 hours')
    res.add_argument('--allocation', required=True, help='the approved allocation or prepaid share it spends from')
    res.add_argument('--credit-allowance', required=True, help='the credits that allocation approved for this provider')
    rev = steps.add_parser('review', help="bind the generated file and the independent reviewer's verdicts, then check for the review board")
    rev.add_argument('roll'); rev.add_argument('file', nargs='?', help='the review file (see --template)')
    rev.add_argument('--template', action='store_true', help='print the review file to fill in: every verdict the floor is owed')
    chk = steps.add_parser('check', help="the floor's still checks on one roll; exit 1 names each failure with Krish's words")
    chk.add_argument('roll'); chk.add_argument('--stage', choices=['prompt', 'review'], default='review')
    events = sub.add_parser('events'); events.add_argument('action', choices=['import']); events.add_argument('file')
    sub.add_parser('reporting-access')
    cc = sub.add_parser('cc', help='Control Center protocol loop: start, run, finish; kits keeps AEO-Engine\'s win kits; queue lists answers to apply (docs/ENGINE.md)')
    cc.add_argument('action', choices=['start', 'run', 'finish', 'kits', 'queue']); cc.add_argument('--mode', choices=['live', 'synthetic'], default='synthetic')
    cc.add_argument('--code', help='lower_snake failure code for finish')
    run = sub.add_parser('run'); run.add_argument('--job'); run.add_argument('--now'); run.add_argument('--force', action='store_true')
    snap = sub.add_parser('snapshot'); commands = snap.add_subparsers(dest='action', required=True)
    exp = commands.add_parser('export'); exp.add_argument('file')
    imp = commands.add_parser('restore'); imp.add_argument('file'); imp.add_argument('--replace', action='store_true')
    insight = sub.add_parser('insights'); commands = insight.add_subparsers(dest='action', required=True)
    imp = commands.add_parser('import'); imp.add_argument('file')
    commands.add_parser('decisions')
    provider = sub.add_parser('provider'); commands = provider.add_subparsers(dest='action', required=True)
    commands.add_parser('status')
    reserve = commands.add_parser('reserve'); reserve.add_argument('file'); reserve.add_argument('--monthly-budget', default='0'); reserve.add_argument('--credit-allowance')
    transition = commands.add_parser('transition'); transition.add_argument('request_id'); transition.add_argument('status'); transition.add_argument('--receipt')
    imp = commands.add_parser('import'); imp.add_argument('request_id'); imp.add_argument('file'); imp.add_argument('role'); imp.add_argument('provenance')
    bundle = sub.add_parser('bundle'); bundle.add_argument('pack'); bundle.add_argument('file')
    dashboard = sub.add_parser('dashboard'); dashboard.add_argument('--start', required=True); dashboard.add_argument('--end', required=True); dashboard.add_argument('--timezone', required=True); dashboard.add_argument('--date')
    sub.add_parser('readiness')
    cache = sub.add_parser('assets'); cache.add_argument('--heartside-dir')
    render = sub.add_parser('render'); render.add_argument('file'); render.add_argument('--date'); render.add_argument('--heartside-dir')
    metrics = sub.add_parser('metrics'); commands = metrics.add_subparsers(dest='action', required=True)
    imp = commands.add_parser('import'); imp.add_argument('file')
    report = commands.add_parser('report'); report.add_argument('--start', required=True); report.add_argument('--end', required=True); report.add_argument('--timezone', required=True)
    creatives = sub.add_parser('creatives'); commands = creatives.add_subparsers(dest='action', required=True)
    commands.add_parser('list')
    mark = commands.add_parser('mark'); mark.add_argument('creative_id'); mark.add_argument('revision'); mark.add_argument('status', choices=list(ledger.TRANSITIONS)); mark.add_argument('--url')
    backup = sub.add_parser('ledger'); commands = backup.add_subparsers(dest='action', required=True)
    backup = commands.add_parser('backup'); backup.add_argument('file')


def run(args, growth):
    root = Path(growth.HERE)
    if args.cmd == 'examples':
        from . import examples
        errors, status = examples.check(root, args.stage, args.only)
        done = sum(v == 'done' for v in status.values())
        failed = sorted(k for k, v in status.items() if v.startswith('failed'))
        print(f'stage {args.stage}{" (" + args.only + ")" if args.only else ""}: {done} of {len(status)} files done, {len(failed)} reported failed, {len(errors)} problems')
        for k in failed:
            print(f'  failed {k}: {status[k][8:]}')
        for e in errors:
            print('  ' + e)
        if errors:
            raise SystemExit(1)
        print('ready for review')
        return
    if args.cmd == 'attribution':
        from . import attribution
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            result = attribution.run(db)
        if result['status'] in ('hold', 'current'):
            print(result['status'].upper() + ': ' + result['reason'])
            return
        for name, reading in result['windows'].items():
            print(f"{name} {reading['start']} to {reading['end']} ({reading['timezone']}): organic {reading['organic']['orders']} orders, "
                  f"${reading['organic']['net_sales']:,.2f} of store ${reading['store']['net_sales']:,.2f} "
                  f"({reading['store']['orders']} orders); pending {reading['tiers']['pending']['orders']}, "
                  f"paid {reading['tiers']['paid']['orders']}; fully refunded {reading['fully_refunded_orders']}")
            print('  by group: ' + ', '.join(f"{t} {v['orders']}" for t, v in reading['tiers'].items()))
        print('stored')
        return
    if args.cmd == 'reporting-access':
        from . import control_center
        result = control_center.probe(growth.BASE, growth.token())
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result['authenticated'] else 1)
    if args.cmd == 'cc':
        from . import protocol
        raise SystemExit(protocol.main(root, growth, args.action, args.mode, args.code))
    if args.cmd == 'run':
        from . import runner
        import datetime as dt
        stamp = dt.datetime.fromisoformat(args.now.replace('Z', '+00:00')) if args.now else None
        result = runner.tick(root, growth, stamp, args.job, args.force)
        print(json.dumps(result, indent=2))
        if any(r['status'] == 'failed' for r in result['results']):
            raise SystemExit(1)
        return
    if args.cmd == 'snapshot':
        from . import state_store
        result = state_store.export(root, args.file) if args.action == 'export' else state_store.restore(root, args.file, args.replace)
        print(json.dumps(result, indent=2)); return
    if args.cmd == 'bundle':
        from . import review
        pack = json.loads(Path(args.pack).read_text())
        print(json.dumps(review.bundle(root, pack, args.file), indent=2)); return
    if args.cmd in {'provider', 'insights'}:
        from . import providers, insights
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            if args.cmd == 'insights':
                result = insights.import_observation(db, json.loads(Path(args.file).read_text())) if args.action == 'import' else insights.decisions(db)
            elif args.action == 'status':
                providers.setup(db)
                result = {'automatic_paid_requests': False, 'default_monthly_budget_usd': '0',
                          'capabilities': {k: sorted(v) for k, v in providers.PROVIDERS.items()},
                          'requests': [dict(r) for r in db.execute('SELECT request_id,provider,capability,maximum,actual,status,allocation,credits_maximum,credits_actual FROM provider_requests')]}
            elif args.action == 'reserve':
                result = providers.reserve(db, json.loads(Path(args.file).read_text()), args.monthly_budget, credit_allowance=args.credit_allowance)
            elif args.action == 'transition':
                providers.transition(db, args.request_id, args.status, json.loads(Path(args.receipt).read_text()) if args.receipt else None)
                result = {'recorded': True, 'provider_submitted_by_this_command': False}
            else:
                result = str(providers.import_asset(root, db, args.request_id, args.file, args.role, json.loads(Path(args.provenance).read_text())))
            print(json.dumps(result, indent=2)); return
    if args.cmd == 'social':
        from . import social
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            report = social.status(db)
        print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else '\n'.join(social.lines(report) or ['No social history recorded. Import it: growth.py events import <file>.']))
        return
    if args.cmd == 'ads':
        from . import ad_audit, social
        import datetime as dt
        if args.boosts:
            doc = json.loads(Path(args.boosts).read_text())
            records = [e.get('record', e) for e in (doc if isinstance(doc, list) else doc.get('events', []))]
            boosts = [social.validate(dict(r)) for r in records if r.get('kind') == 'boost']
        else:
            with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
                boosts = social.rows(db, 'boost')
        traffic = json.loads(Path(args.traffic).read_text()) if args.traffic else None
        report = ad_audit.audit(boosts, traffic, social.when(args.now) if args.now else dt.datetime.now(dt.timezone.utc))
        print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else '\n'.join(ad_audit.lines(report)))
        return
    if args.cmd == 'drive':
        from . import drive_audit
        problems = drive_audit.audit(json.loads((root / 'config/drive-map.json').read_text()), json.loads(Path(args.listing).read_text()))
        print('\n'.join(problems) if problems else 'Drive matches the map.')
        raise SystemExit(1 if problems else 0)
    if args.cmd == 'floor':
        from . import floor
        entries = floor.load(root, args.fmt)
        print('\n'.join(floor.lines(entries)))
        return
    if args.cmd == 'still':
        return still(args, growth, root)
    if args.cmd == 'events':
        from . import operations
        from . import divergent
        events = json.loads(Path(args.file).read_text())
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            results = operations.apply(root, db, events)
        print(json.dumps(results, indent=2))
        # What went live goes to divergent-thinker's archive (record, zero model calls) once Control Center serves it.
        print(divergent.record_live(root, events, results), file=sys.stderr)
        return
    state = growth.load_state()
    if args.cmd in ('assets', 'readiness', 'render', 'dashboard') and not state:
        raise ValueError('run growth.py sync first')
    if args.cmd == 'library':
        from . import library
        if not state:
            raise ValueError('run growth.py sync first')
        stale = growth.freshness({'heartside_sha': state['sha']}, state, growth.head_sha, growth.raw, growth.docs_listing)
        if stale:
            raise ValueError('; '.join(stale))
        result = library.build(root, state, growth.check_pack, args.heartside_dir, args.date, link_builder=growth.tracked)
        stale = growth.freshness({'heartside_sha': state['sha']}, state, growth.head_sha, growth.raw, growth.docs_listing)
        if stale:
            raise ValueError('; '.join(stale))
        print(json.dumps(result, indent=2)); return
    if args.cmd == 'readiness':
        print(json.dumps({'heartside_sha': state['sha'], 'store_snapshot_fresh': offers.fresh_store(state),
                          'homepage_v3': state.get('homepage_v3'), 'gifts': offers.catalog(state)}, indent=2))
        return
    if args.cmd == 'assets':
        print(json.dumps(assets.prepare(root, state['sha'], args.heartside_dir), indent=2))
        return
    if args.cmd == 'render':
        from . import media
        spec = json.loads(Path(args.file).read_text())
        # Rendering must not use a stale product canon, even when assets are cached.
        stale = growth.freshness({'heartside_sha': state['sha']}, state, growth.head_sha, growth.raw, growth.docs_listing)
        if stale:
            raise ValueError('; '.join(stale))
        pack, manifest = media.render(root, spec, state, growth.check_pack, args.heartside_dir, args.date, link_builder=growth.tracked)
        errors = media.verify(root, pack['production'], pack)
        if errors:
            raise ValueError('; '.join(errors))
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            for item in pack['items']:
                ledger.record_render(db, item['creative_id'], manifest['revision'], spec, manifest)
        output = assets.local_path(root, 'local/drafts/' + manifest['creative_id'] + '-' + manifest['revision'][:16] + '.json')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(pack, indent=2) + '\n')
        print(f'Rendered for human review: {pack["production"]["manifest"]}')
        print(f'Pack: {output.relative_to(root)}')
        print('Check and store: python3 growth.py post ' + str(output.relative_to(root)))
        return
    with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
        if args.cmd == 'dashboard':
            from . import dashboard
            for path in dashboard.write(root, db, state, args.start, args.end, args.timezone, args.date):
                print('Report draft: ' + str(path.relative_to(root)))
            print('Run check and post on each draft. Reports are not social posts. Delivery requires Control Center venture support and runner authentication.')
        elif args.cmd == 'metrics' and args.action == 'import':
            document = json.loads(Path(args.file).read_text())
            changed = ledger.import_report(db, document)
            print('aggregate report stored' if changed else 'aggregate report unchanged (not counted twice)')
        elif args.cmd == 'metrics':
            print(json.dumps(ledger.summary(db, args.start, args.end, args.timezone), indent=2))
        elif args.cmd == 'creatives' and args.action == 'list':
            rows = db.execute('SELECT creative_id,revision,status,updated_at,published_url FROM creatives ORDER BY updated_at DESC,creative_id').fetchall()
            print(json.dumps([dict(row) for row in rows], indent=2))
        elif args.cmd == 'creatives':
            if args.status in {'approved', 'published'}:
                from . import operations
                operations.validate_creative(root, db, args.creative_id, args.revision)
            ledger.mark(db, args.creative_id, args.revision, args.status, args.url)
            print('Recorded locally. This command never publishes.')
        else:
            path = assets.local_path(root, args.file)
            source = (root / 'local/engine.sqlite3').resolve()
            if path == source or path.exists():
                raise ValueError('choose a new local/ backup file, different from the working database')
            path.parent.mkdir(parents=True, exist_ok=True)
            ledger.backup(db, path)
            print('consistent ledger backup: ' + str(path.relative_to(root)))


def still(args, growth, root):
    """growth.py still roll | reserve | review | check: a generated dog still from its roll to the review board."""
    from factory import dog_roll
    from . import providers, stills
    if args.step == 'roll':
        dog_roll.run(args)
        return
    floor_data, pools = stills.load_floor(root), stills.load_pools(root)
    if args.step == 'review' and args.template:
        print(json.dumps(stills.template(floor_data), indent=2, ensure_ascii=False))
        return
    given = Path(args.roll)
    path = given if given.suffix == '.json' else Path(dog_roll.ROLLS) / f'{args.roll}.json'
    if not path.is_file():
        raise ValueError(f'no roll record {path}; roll one first (growth.py still roll)')
    record = json.loads(path.read_text(encoding='utf-8'))

    def save(rec):
        path.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')

    def report(failures, stage):
        if failures:
            print(f'HELD at the {stage} stage: {record["roll_id"]}')
            print('\n'.join('  ' + line for line in stills.lines(failures)))
            raise SystemExit(1)
        print(f'PASS at the {stage} stage: {record["roll_id"]} meets the floor\'s still checks.')

    if args.step == 'reserve':
        state = growth.load_state()
        if not state:
            raise ValueError('run growth.py sync first: a reservation names the synced heartside commit')
        record = dict(record, script_score=args.script_score, made_by=args.by)
        request = {'provider': args.provider, 'credits': args.credits, 'quote_source': args.quote_source,
                   'quote_observed_at': args.quoted_at, 'allocation': args.allocation}
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            try:
                record, row = stills.reserve(db, record, state['sha'], request, args.credit_allowance, floor_data, pools)
            except stills.Held as held:
                report(held.failures, 'prompt')
        save(record)
        print(f'Reserved {row["credits_maximum"]} {args.provider} credits as request {row["request_id"]} ({row["status"]}).')
        print('Next, once each: python3 growth.py provider transition ' + row['request_id'] + ' submitted; generate with the '
              'record\'s prompt and aspect_ratio exactly; then transition it completed with the receipt.')
        return
    if args.step == 'review':
        if not args.file:
            raise ValueError('name the review file, or print one to fill in with --template')
        record = stills.attach(record, json.loads(Path(args.file).read_text(encoding='utf-8')), root)
        save(record)
    stage = 'review' if args.step == 'review' else args.stage
    row = None
    request_id = (record.get('reservation') or {}).get('request_id')
    if stage == 'review' and request_id and (root / 'local/engine.sqlite3').exists():
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            providers.setup(db)
            found = db.execute('SELECT * FROM provider_requests WHERE request_id=?', (request_id,)).fetchone()
            row = dict(found) if found else None
    report(stills.check(record, stage, floor_data, pools, row, root), stage)
    if stage == 'review':
        print('It may go on Krish\'s review board (docs/REVIEW-BOARD.md).')
