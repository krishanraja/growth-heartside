"""Commands share the existing growth.py entrypoint and local/ boundary."""
from contextlib import closing
import json
from pathlib import Path

from . import assets, ledger, offers


COMMANDS = {'readiness', 'assets', 'render', 'metrics', 'creatives', 'ledger', 'dashboard'}


def add_commands(sub):
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
    state = growth.load_state()
    if args.cmd in ('assets', 'readiness', 'render', 'dashboard') and not state:
        raise ValueError('run growth.py sync first')
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
        pack, manifest = media.render(root, spec, state, growth.check_pack, args.heartside_dir, args.date)
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
