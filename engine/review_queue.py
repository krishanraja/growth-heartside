"""Heartside's asks on Krish's one list (I-24, Ruling, Krish, 2026-11-14).

`review/queue.json` holds each decision, spend, copy or delete ask. The daily Control Center
run proposes each open one behind its wall (strategy, or spend with its amount), as a plan
whose exact words are the question with what a yes and a no each do, in priority order. His
answers are read back by id and bound to the words' hash: an answer on the current words stops
the ask and is reported as an answer to apply until a session applies it and records it under
`answer`. Nothing here posts, sends, spends or deletes.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re

PATH = 'review/queue.json'
SCHEMA = 'heartside-review-queue/1'
KINDS = {'decision': 'strategy', 'copy': 'strategy', 'delete': 'strategy', 'spend': 'spend'}
ID = re.compile(r'^heartside:ask:[a-z0-9][a-z0-9._-]{0,90}$')
DAY = re.compile(r'^\d{4}-\d{2}-\d{2}$')
LIMITS = {'title': 160, 'question': 2000, 'on_yes': 2000, 'on_no': 2000}


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def load(root):
    """The queue's items in priority order, or [] when there is no queue. A malformed item is refused."""
    path = Path(root) / PATH
    if not path.exists():
        return []
    doc = json.loads(path.read_text())
    if doc.get('schema') != SCHEMA or not isinstance(doc.get('items'), list):
        raise ValueError(f'{PATH}: not a {SCHEMA} document')
    seen = set()
    for item in doc['items']:
        problem = _problem(item)
        if problem or item['id'] in seen:
            raise ValueError(f'{PATH}: {item.get("id") if isinstance(item, dict) else item}: {problem or "a second item with this id"}')
        seen.add(item['id'])
    return sorted(doc['items'], key=lambda i: i['priority'])


def per_report(root):
    path = Path(root) / PATH
    return int(json.loads(path.read_text()).get('per_report', 3)) if path.exists() else 0


def _problem(item):
    if not isinstance(item, dict) or not ID.match(str(item.get('id', ''))):
        return 'needs an id heartside:ask:<lower-case slug>'
    if item.get('kind') not in KINDS:
        return 'kind is decision, spend, copy or delete'
    if not isinstance(item.get('priority'), int) or item['priority'] < 1:
        return 'priority is a whole number from 1'
    for key, limit in LIMITS.items():
        if not isinstance(item.get(key), str) or not item[key].strip() or len(item[key]) > limit:
            return f'{key} is required, up to {limit} characters'
    amount = item.get('amount_usd')
    if item['kind'] == 'spend' and not (isinstance(amount, (int, float)) and not isinstance(amount, bool) and amount > 0):
        return 'a spend ask names its amount in amount_usd'
    if item['kind'] != 'spend' and amount is not None:
        return 'only a spend ask carries an amount'
    if not DAY.match(str(item.get('asked_on', ''))):
        return 'asked_on is a date'
    answer = item.get('answer')
    if answer is not None and not (isinstance(answer, dict) and answer.get('decision') in ('approved', 'declined', 'done')
                                   and all(answer.get(k) for k in ('decided_at', 'applied_on', 'where'))):
        return 'an applied answer records decision, decided_at, applied_on and where'
    return None


def exact_payload(item):
    return f'{item["question"]}\n\nOn yes: {item["on_yes"]}\nOn no: {item["on_no"]}'


def payload_sha256(item):
    """Bound to the words he answers: the question, both outcomes, the amount and the id."""
    body = {k: item.get(k) for k in ('id', 'kind', 'question', 'on_yes', 'on_no', 'amount_usd')}
    return hashlib.sha256(_canonical(body).encode()).hexdigest()


def open_items(items):
    return [i for i in items if i.get('answer') is None]


def since(items, now):
    """The time to read decisions from: the oldest open ask's day, or None when nothing is open."""
    days = [i['asked_on'] for i in open_items(items)]
    return min(days) + 'T00:00:00Z' if days else None


def latest(decisions):
    out = {}
    for d in decisions or []:
        if isinstance(d, dict) and isinstance(d.get('proposal_id'), str):
            if d['proposal_id'] not in out or str(d.get('decided_at')) > str(out[d['proposal_id']].get('decided_at')):
                out[d['proposal_id']] = d
    return out


def to_apply(items, decisions):
    """Open asks Krish answered on their current words, by id. His words never leave Control Center here."""
    found = latest(decisions)
    out = []
    for item in open_items(items):
        d = found.get(item['id'])
        if d and d.get('decision') in ('approved', 'declined', 'done') and d.get('payload_sha256') == payload_sha256(item):
            out.append({'id': item['id'], 'decision': d['decision'], 'decided_at': d.get('decided_at'), 'amended': bool(d.get('amended'))})
    return out


def proposals(items, decisions, limit):
    """The open, unanswered asks as walled plans, in priority order, at most `limit` of them."""
    answered = {a['id'] for a in to_apply(items, decisions)}
    out = []
    for item in open_items(items):
        if item['id'] in answered:
            continue
        why = f'{item["question"]} Source: {item["source"]}.'
        out.append({'proposal_id': item['id'], 'title': item['title'], 'why': why[:1000], 'kind': 'prepared',
                    'wall': KINDS[item['kind']], 'amount_usd': item.get('amount_usd'), 'channel': None, 'objective_key': None,
                    'exact_payload': exact_payload(item), 'payload_sha256': payload_sha256(item), 'evidence': [],
                    'close_condition': {'event': 'krish_answered', 'reference': 'His answer on this exact payload, applied by a session and recorded in ' + PATH},
                    'expires_at': None, 'stage': 'plan', 'parent_proposal_id': None})
    return out[:limit]


def line(applying):
    if not applying:
        return 'Answers to apply: 0.'
    return f'Answers to apply: {len(applying)} (' + ', '.join(
        f'{a["id"]} {a["decision"]}{" amended" if a["amended"] else ""}' for a in applying) + ').'


def status(root, decisions):
    """The session start read: what is open, and each answer still to apply (or that decisions were unread)."""
    items = load(root)
    open_ = open_items(items)
    lines = [f'{len(open_)} open ask(s) in {PATH}, {len(items) - len(open_)} applied.']
    if decisions is None:
        lines.append('Decisions unread: no answer is known, so none is applied. Read them with the engine token (growth.py cc queue).')
    else:
        applying = to_apply(items, decisions)
        lines.append(line(applying))
        lines += [f'  apply {a["id"]}: {a["decision"]}{" (his amended version, read it in Control Center)" if a["amended"] else ""}, '
                  f'decided {a["decided_at"]}; record it under answer in {PATH}.' for a in applying]
    return '\n'.join(lines)
