"""Commands share the existing growth.py entrypoint and local/ boundary."""
from contextlib import closing
import json
from pathlib import Path

from . import assets, ledger, offers


COMMANDS = {'readiness', 'assets', 'render', 'metrics', 'creatives', 'ledger', 'dashboard', 'reporting-access', 'run', 'snapshot', 'insights', 'provider', 'bundle', 'events', 'library', 'cc', 'attribution'}


def add_commands(sub):
    sub.add_parser('attribution', help='Read which orders came from organic posts, as aggregates (docs/ENGINE.md)')
    library = sub.add_parser('library'); library.add_argument('--date'); library.add_argument('--heartside-dir')
    events = sub.add_parser('events'); events.add_argument('action', choices=['import']); events.add_argument('file')
    sub.add_parser('reporting-access')
    cc = sub.add_parser('cc', help='Control Center protocol loop: start, run, finish (docs/ENGINE.md)')
    cc.add_argument('action', choices=['start', 'run', 'finish']); cc.add_argument('--mode', choices=['live', 'synthetic'], default='synthetic')
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
    if args.cmd == 'attribution':
        from contextlib import closing
        from . import attribution, ledger
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            result = attribution.run(db)
        if result['status'] in ('hold', 'current'):
            print(result['status'].upper() + ': ' + result['reason'])
            return
        for name, reading in result['windows'].items():
            print(f"{name} {reading['start']} to {reading['end']} ({reading['timezone']}): organic {reading['organic']['orders']} orders, "
                  f"${reading['organic']['net_sales']:,.2f} of store ${reading['store']['net_sales']:,.2f} "
                  f"({reading['store']['orders']} orders); pending {reading['tiers']['pending']['orders']}, "
                  f"paid {reading['tiers']['paid']['orders']}")
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
    if args.cmd == 'events':
        from . import operations
        with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
            print(json.dumps(operations.apply(root, db, json.loads(Path(args.file).read_text())), indent=2))
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
