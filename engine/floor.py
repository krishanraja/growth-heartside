"""The rejection floor (factory/floor.json): what Krish rejected, in his words, and the check each rejection added."""
import json
from pathlib import Path

CATEGORIES = {'performance', 'sound', 'joke', 'process', 'presentation', 'product', 'bar', 'story', 'generation', 'concept'}


def load(root, fmt=None):
    data = json.loads((Path(root) / 'factory/floor.json').read_text())
    entries = data['entries']
    if fmt:
        if fmt not in data['formats']:
            raise ValueError(f'format must be one of {data["formats"]}')
        entries = [e for e in entries if fmt in e['applies_to']]
    return {'entries': entries, 'open_conflicts': data.get('open_conflicts', [])}


def errors(data):
    out, seen = [], set()
    for e in data['entries']:
        at = e.get('id', '?')
        if at in seen:
            out.append(f'{at}: duplicate id')
        seen.add(at)
        if not {'id', 'date', 'made', 'words', 'category', 'rule', 'check', 'applies_to'} <= set(e):
            out.append(f'{at}: missing a field')
            continue
        if e['category'] not in CATEGORIES:
            out.append(f'{at}: unknown category')
        if not set(e['applies_to']) <= set(data['formats']) or not e['applies_to']:
            out.append(f'{at}: applies_to must name formats')
        if not e['check'].split(':')[0] in ('code', 'review', 'process'):
            out.append(f'{at}: check starts with code:, review: or process:')
        if not e['words'] and e['category'] != 'generation' and not e.get('said'):
            out.append(f'{at}: no exact words; say where the rejection is recorded in said')
        if any(not isinstance(w, str) or not w.strip() for w in e['words']):
            out.append(f'{at}: words are his exact quotes')
    return out


def lines(data):
    out = []
    for e in data['entries']:
        said = ' / '.join(f'"{w}"' for w in e['words']) or e.get('said') or '(held by the engine itself)'
        out.append(f"{e['id']} ({e['date']}, {e['category']}): {said}\n  rule: {e['rule']}\n  check: {e['check']}")
    for c in data['open_conflicts']:
        out.append(f"OPEN CONFLICT {' vs '.join(c['between'])}: {c['what']}")
    return out
