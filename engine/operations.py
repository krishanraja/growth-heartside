"""Bounded operator evidence into the hosted ledger; never a social publisher."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from . import assets, insights, ledger, media


def validate_creative(root, db, creative_id, revision):
    root = Path(root).resolve()
    row = db.execute('SELECT manifest FROM creatives WHERE creative_id=? AND revision=?', (creative_id, revision)).fetchone()
    if not row:
        raise ValueError('unknown creative revision')
    manifest = json.loads(row['manifest'])
    first = next(iter(manifest['files'].values()))
    path = assets.local_path(root, str(Path(first['path']).parent / 'manifest.json'))
    if ledger.canonical(json.loads(path.read_text())) != ledger.canonical(manifest):
        raise ValueError('creative manifest changed since generation')
    errors = media.verify(root, {'manifest': str(path.relative_to(root)), 'sha256': assets.sha256(path)})
    if errors:
        raise ValueError('; '.join(errors))


def apply(root, db, events):
    if not isinstance(events, list) or len(events) > 100 or len(ledger.canonical(events)) > 64000:
        raise ValueError('operator evidence must be a bounded array; no raw customer data')
    db.execute('CREATE TABLE IF NOT EXISTS operator_events(event_id TEXT PRIMARY KEY,payload_sha TEXT NOT NULL,applied_at TEXT NOT NULL)')
    db.commit()
    results = []
    for event in events:
        if not isinstance(event, dict) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}', str(event.get('event_id', ''))):
            raise ValueError('each operator event needs a stable event_id')
        fingerprint = ledger.digest(event)
        previous = db.execute('SELECT payload_sha FROM operator_events WHERE event_id=?', (event['event_id'],)).fetchone()
        if previous:
            if previous['payload_sha'] != fingerprint:
                raise ValueError('an event_id cannot be reused for changed evidence')
            results.append({'event_id': event['event_id'], 'status': 'already_applied'})
            continue
        if event.get('type') == 'creative_status':
            if set(event) != {'event_id', 'type', 'creative_id', 'revision', 'status', 'url'}:
                raise ValueError('creative status uses the exact allowlisted schema')
            if event['status'] not in {'reviewed', 'approved', 'published', 'skipped'}:
                raise ValueError('unsupported operator status')
            if not re.fullmatch(r'[a-f0-9]{64}', str(event['revision'])):
                raise ValueError('record the full exact creative revision')
            if event['status'] == 'published':
                url = urlparse(event['url'] or '')
                if url.username or url.password or url.query or url.fragment or url.path in {'', '/'}:
                    raise ValueError('record a canonical publication permalink without credentials, tracking query or fragment')
            if event['status'] in {'approved', 'published'}:
                validate_creative(root, db, event['creative_id'], event['revision'])
            ledger.mark(db, event['creative_id'], event['revision'], event['status'], event['url'])
        elif event.get('type') == 'insight':
            if set(event) != {'event_id', 'type', 'observation'}:
                raise ValueError('insight event uses the exact allowlisted schema')
            insights.import_observation(db, event['observation'])
        else:
            raise ValueError('operator events record only creative status or aggregate insights')
        with db:
            db.execute('INSERT INTO operator_events VALUES(?,?,?)', (event['event_id'], fingerprint, ledger.now()))
        results.append({'event_id': event['event_id'], 'status': 'applied'})
    return results
