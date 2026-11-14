"""Audit Heartside's Drive every run from the listing Control Center serves (fleet integration I-25, protocol 1.35.0).

Ruling (Krish, 2026-11-14): Control Center reads folder names and file titles (never contents) under Ventures once a
day (D16). The directive's `library` carries the folders and file titles under the root config/drive-map.json declares
(`drive_map`, drive-map/1), so the daily run checks Drive with drive_audit.audit instead of waiting for a session to
save a listing by hand (docs/DRIVE-MAP.md, "Auditing").

Unknown is never clean: a part that is absent, not available or carries no root comes back as `unknown` with its
reason, and nothing is checked. The problems are written under gitignored local/ only; the run prints counts, never a
title, because the Actions logs are public. A Heartside file outside the Heartside folder is beyond the listing, so a
session's own audit still covers that one check.
"""
import json
from pathlib import Path

from . import drive_audit

FOLDER = drive_audit.FOLDER
OUT = 'local/drive/library-audit.json'


def listing(directive):
    """The directive's library as drive_audit's listing (id, title, mimeType, parentId), or (None, reason) when unknown."""
    body = directive.get('directive') if isinstance(directive, dict) else None
    part = body.get('library') if isinstance(body, dict) else None
    if not isinstance(part, dict):
        return None, 'not_served'
    if part.get('available') is not True or part.get('complete') is not True:
        return None, str(part.get('reason') or 'not_available')
    roots = part.get('roots') if isinstance(part.get('roots'), list) else []
    if not roots:
        return None, 'no_roots'
    items = []
    for root in roots:
        folder_id = {}
        for f in root.get('folders') or []:
            folder_id[f.get('folder')] = f.get('id')
            items.append({'id': f.get('id'), 'title': str(f.get('name') or ''), 'mimeType': FOLDER, 'parentId': f.get('parent_id')})
        for x in root.get('files') or []:
            items.append({'id': x.get('id'), 'title': x.get('title', ''), 'mimeType': x.get('mime', ''), 'parentId': folder_id.get(x.get('folder'))})
    return items, None


def check(root, directive, drive_map=None):
    """Audit the served listing. Returns counts only: {state, errors, warnings, items} or {state: 'unknown', reason}."""
    items, why = listing(directive)
    if items is None:
        return {'state': 'unknown', 'reason': why}
    try:
        drive_map = drive_map or json.loads((Path(root) / 'config/drive-map.json').read_text())
        problems = drive_audit.audit(drive_map, items)
    except (ValueError, KeyError, TypeError, StopIteration, OSError) as error:  # an audit never fails the run
        return {'state': 'unknown', 'reason': f'audit_error: {type(error).__name__}'}
    out = Path(root) / OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'as_of': ((directive.get('directive') or {}).get('library') or {}).get('as_of'), 'problems': problems}, indent=2))
    return {'state': 'checked', 'errors': sum(p.startswith('ERROR') for p in problems),
            'warnings': sum(p.startswith('WARN') for p in problems), 'items': len(items)}
