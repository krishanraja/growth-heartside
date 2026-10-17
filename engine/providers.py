"""Provider requests are durable reservations; uncertain submissions never auto-repeat.

MCP generators run in the connected authoring session. The unattended runner uses
only checked reusable assets. No API key is copied out of a connector or dashboard.
"""
import datetime as dt
from decimal import Decimal
import json
from pathlib import Path
import re
import shutil

from . import assets, ledger

PROVIDERS = {'openai': {'copy', 'image'}, 'gemini': {'copy', 'image'},
             'higgsfield': {'image', 'motion', 'voice'}, 'elevenlabs': {'voice', 'music', 'sound'},
             'heygen': {'motion', 'voice'}, 'imagegen': {'image'}}


def setup(db):
    db.executescript('''CREATE TABLE IF NOT EXISTS provider_requests(
      request_id TEXT PRIMARY KEY, provider TEXT NOT NULL, capability TEXT NOT NULL,
      fingerprint TEXT NOT NULL, source_sha TEXT NOT NULL, month TEXT NOT NULL, currency TEXT NOT NULL,
      maximum TEXT NOT NULL, actual TEXT, status TEXT NOT NULL,
      created_at TEXT NOT NULL, receipt TEXT);
    ''')


def money(value):
    if isinstance(value, bool):
        raise ValueError('cost must be a finite nonnegative decimal')
    try:
        number = Decimal(str(value))
    except Exception:
        raise ValueError('cost must be a finite nonnegative decimal') from None
    if not number.is_finite() or number < 0:
        raise ValueError('cost must be a finite nonnegative decimal')
    return number


def reserve(db, request, monthly_budget='0', day=None):
    setup(db)
    allowed = {'provider', 'capability', 'brief', 'source_sha', 'maximum_usd', 'quote_source', 'quote_observed_at'}
    if set(request) != allowed or request['capability'] not in PROVIDERS.get(request['provider'], set()):
        raise ValueError('use an allowlisted provider/capability and the exact request schema')
    if not re.fullmatch(r'[a-f0-9]{40}', str(request['source_sha'])):
        raise ValueError('provider request needs the synced full product SHA')
    if not isinstance(request['brief'], str) or not request['brief'].strip() or len(request['brief']) > 12000:
        raise ValueError('brief must contain only approved marketing material')
    stamp = dt.datetime.now(dt.timezone.utc)
    quote = dt.datetime.fromisoformat(request['quote_observed_at'].replace('Z', '+00:00'))
    if not quote.tzinfo or not dt.timedelta(0) <= stamp - quote <= dt.timedelta(hours=24):
        raise ValueError('a current cost quote with an offset is required')
    if not str(request['quote_source']).strip():
        raise ValueError('quote source is required')
    maximum, budget = money(request['maximum_usd']), money(monthly_budget)
    day = dt.date.fromisoformat(day) if day else stamp.date()
    month = day.strftime('%Y-%m')
    fingerprint = ledger.digest({k: request[k] for k in ('provider', 'capability', 'brief', 'source_sha')})
    request_id = ledger.digest({'month': month, 'request': fingerprint})
    # Serializes concurrent budget reservations across processes.
    db.execute('BEGIN IMMEDIATE')
    try:
        existing = db.execute('SELECT * FROM provider_requests WHERE request_id=?', (request_id,)).fetchone()
        if existing:
            db.commit()
            return dict(existing)
        rows = db.execute("SELECT maximum,actual FROM provider_requests WHERE month=? AND status!='cancelled'", (month,))
        committed = sum((money(row['actual'] if row['actual'] is not None else row['maximum']) for row in rows), Decimal(0))
        if committed + maximum > budget:
            raise ValueError('configured monthly generation budget would be exceeded; no request submitted')
        db.execute('INSERT INTO provider_requests VALUES(?,?,?,?,?,?,?,?,?,?,?,NULL)',
                   (request_id, request['provider'], request['capability'], fingerprint, request['source_sha'], month, 'USD',
                    str(maximum), None, 'reserved', ledger.now(),))
        db.commit()
    except BaseException:
        db.rollback()
        raise
    return dict(db.execute('SELECT * FROM provider_requests WHERE request_id=?', (request_id,)).fetchone())


def transition(db, request_id, status, receipt=None):
    setup(db)
    with db:
        row = db.execute('SELECT * FROM provider_requests WHERE request_id=?', (request_id,)).fetchone()
        if not row:
            raise ValueError('unknown provider request')
        allowed = {'reserved': {'submitted', 'cancelled'}, 'submitted': {'completed', 'failed', 'unknown'},
                   'unknown': {'completed', 'failed'}, 'failed': set(), 'completed': set(), 'cancelled': set()}
        if status not in allowed.get(row['status'], set()):
            raise ValueError('invalid transition; submitted/unknown requests must not be submitted again')
        actual = None
        if status in {'completed', 'failed'}:
            if not isinstance(receipt, dict) or set(receipt) != {'job_id', 'actual_usd', 'observed_at'}:
                raise ValueError('terminal receipt needs job_id, actual_usd and observed_at')
            observed = dt.datetime.fromisoformat(receipt['observed_at'].replace('Z', '+00:00'))
            if not observed.tzinfo or not str(receipt['job_id']).strip():
                raise ValueError('receipt needs a real job ID and offset timestamp')
            actual = str(money(receipt['actual_usd']))
            # Record overruns honestly; a higher actual blocks subsequent reservations.
        changed = db.execute('UPDATE provider_requests SET status=?,actual=?,receipt=? WHERE request_id=? AND status=?',
                   (status, actual, ledger.canonical(receipt) if receipt else None, request_id, row['status']))
        if changed.rowcount != 1:
            raise ValueError('provider request changed concurrently; no duplicate submission is permitted')


def import_asset(root, db, request_id, file, role, provenance):
    setup(db)
    row = db.execute('SELECT * FROM provider_requests WHERE request_id=?', (request_id,)).fetchone()
    if not row or row['status'] != 'completed':
        raise ValueError('only a confirmed completed provider job can supply a reusable asset')
    permitted = {'image': {'fictional_scene'}, 'motion': {'fictional_motion'},
                 'voice': {'narration'}, 'music': {'soundtrack'}, 'sound': {'soundtrack'}}
    if role not in permitted.get(row['capability'], set()):
        raise ValueError('AI media cannot replace product photos, print files or customer evidence')
    if not isinstance(provenance, dict) or set(provenance) != {'description', 'rights', 'disclosure', 'transcript'}:
        raise ValueError('asset requires description, rights, disclosure and transcript (empty for nonspeech)')
    if not all(isinstance(v, str) for v in provenance.values()) or not all(provenance[k].strip() for k in ('description', 'rights', 'disclosure')):
        raise ValueError('media provenance must be explicit')
    source = Path(file)
    if source.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.mp4', '.mp3', '.wav', '.m4a'}:
        raise ValueError('unsupported reusable media format')
    checksum = assets.sha256(source)
    destination = assets.local_path(root, f'local/provider-assets/{request_id}/{checksum}{source.suffix.lower()}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.copyfile(source, destination)
    record = {'path': str(destination.relative_to(root)), 'sha256': checksum, 'role': role,
              'provider': row['provider'], 'request_id': request_id, 'source_sha': row['source_sha'],
              'status': 'needs_human_review', **provenance}
    record_path = destination.with_suffix(destination.suffix + '.json')
    record_path.write_text(json.dumps(record, indent=2) + '\n')
    return record_path
