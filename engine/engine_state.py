"""Protocol 1.20.0: Krish's instruction and this engine's state, for Control Center.

Ruling (Krish, 2026-11-11): every growth engine's priorities, obsessions, next
steps and outstanding items feed live across Control Centre, and Krish
instructs each engine with his next best action, which starts it.

What this module reads, and from where (docs/control-center/ENGINE-PROTOCOL.md,
"Krish's instruction and the engine's state (1.20.0)"):

- `krish_instruction` from the directive. Only its id leaves this module, with
  at most a SHA-256 digest of the words: this repository and its Actions logs
  are public, so his words are never printed, logged, committed or reported.
- `priorities` from this repository's North Star (docs/NORTH_STAR.md, with
  Control Center's own reading of the number from the directive when it sends
  one), then the product constraints the report already holds, then the
  standing recommendations in recommendations.json.
- `obsessions` only from Krish's own quoted aims in this repository's docs.
  Each quote below is checked against its file at run time and dropped when it
  is no longer there, so nothing is invented and nothing goes stale.
- `next_steps` from the first unticked step of docs/GET-GOING.md, then NOW.md's
  "What is next and what is waiting on Krish".

Every line is one plain line with no address or phone number (the same check
Control Center makes, `lineCarriesContact`); a line that fails it is left out
rather than refusing the whole report. A field with no source is left out.
Nothing here posts, sends, publishes or spends, and an instruction never
authorises any of that: walled work still goes to Krish as a proposal.
"""
import datetime as dt
import hashlib
from pathlib import Path
import re
from zoneinfo import ZoneInfo

VERSION = '1.20.0'
LONDON = ZoneInfo('Europe/London')
INSTRUCTION_ID = re.compile(r'^ki_[0-9a-f]{24}$')
KEY = re.compile(r'^[a-z][a-z0-9_]{0,63}$')
YMD = re.compile(r'^\d{4}-\d{2}-\d{2}$')
LINE_MAX, ACK_LINE_MAX = 200, 280
PRIORITIES_MAX, OBSESSIONS_MAX, NEXT_STEPS_MAX, ACKS_MAX = 5, 3, 5, 5
HELD = 'Krish has held this engine'  # the start of Control Center's HELD_RULE
NORTH_STAR_OBJECTIVE = 'organic_net_sales_usd'

# Control Center's own guards (src/lib/growthEngines.ts, EMAIL_IN_TEXT and hasPhone).
EMAIL_IN_TEXT = re.compile(r'[^\s@]+@[^\s@]+\.[a-z]{2,}', re.I)
PHONE_RUN = re.compile(r'\+?\d[\d\s().-]{8,}\d')
CONTROL = re.compile(r'[\x00-\x1f\x7f]')

# Krish's own words, quoted in this repository's docs. Each is reported only
# while it is still in its file, whitespace aside. (quote, since, file)
OBSESSIONS = (
    ('By 31 December 2026, organic posts sell more Heartside gifts than paid ads ever have, and every winning format '
     'was found by this engine and approved by Krish in one press.', '2026-10-18', 'docs/NORTH_STAR.md'),
    ('I want to build an autonomous browser based growth engine that can be run from anywhere (codex or cowork), '
     'solely focused on getting this business to 10k a month with minimal paid CAC', '2026-10-14', 'AGENTS.md'),
    ('Ensure the growth engine is always across what the main heartside repository is doing at any point in time',
     '2026-10-14', 'AGENTS.md'),
)

RECEIVED = ('Received in the daily report run. That run only reads and reports and acts on no words, so nothing has '
            'started yet: a working session on growth-heartside has to take it up.')
HELD_LINE = 'Engine held: it starts once Krish releases it in Control Center.'


# ---------------------------------------------------------------------------
# Lines.
# ---------------------------------------------------------------------------
def carries_contact(text):
    """An email address, or a run of ten digits or more that reads as a phone number."""
    return bool(EMAIL_IN_TEXT.search(text)) or any(
        len(re.sub(r'\D', '', run)) >= 10 for run in PHONE_RUN.findall(text))


def plain(text):
    """Markdown emphasis and code marks out, whitespace on one line."""
    return ' '.join(str(text).replace('**', '').replace('`', '').split())


def fit(text, limit):
    """Whole sentences up to the limit; a first sentence longer than that is cut at a word, never mid-word."""
    if len(text) <= limit:
        return text
    cut = text[:limit + 1]
    end = cut.rfind('. ')
    if end > 0:
        return cut[:end + 1]
    cut = text[:limit]
    return cut[:cut.rfind(' ')].rstrip(' ,;:') if ' ' in cut else cut


def line(text, limit=LINE_MAX):
    """One plain line Control Center accepts, or None."""
    out = fit(plain(text), limit)
    if not out or CONTROL.search(out) or carries_contact(out):
        return None
    return out


def read(root, path):
    try:
        return (Path(root) / path).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None


def section(text, heading):
    """The body under a `## heading` (matched at its start), up to the next `## `."""
    if not text:
        return ''
    match = re.search(r'^## ' + re.escape(heading) + r'.*$', text, re.M)
    if not match:
        return ''
    rest = text[match.end():]
    end = re.search(r'^## ', rest, re.M)
    return rest[:end.start()] if end else rest


def bullets(body):
    """Top-level `- ` bullets, each joined with its indented continuation lines."""
    out = []
    for raw in body.splitlines():
        if raw.startswith('- '):
            out.append(raw[2:].strip())
        elif out and raw.startswith((' ', '\t')) and raw.strip():
            out[-1] += ' ' + raw.strip()
    return out


# ---------------------------------------------------------------------------
# Krish's instruction (directive.krish_instruction, 1.20.0).
# ---------------------------------------------------------------------------
def features(body):
    value = (body or {}).get('features')
    return value if isinstance(value, dict) else {}


def serves_state(body):
    """Send the new report fields only when the served directive says so."""
    return features(body).get('engine_state') is True


def held(body):
    action = (body or {}).get('next_action') or {}
    return isinstance(action, dict) and str(action.get('instruction') or '').startswith(HELD)


def instruction(body):
    """The open instruction as {id, digest}, or None. The words go no further than this function."""
    value = (body or {}).get('krish_instruction')
    if not isinstance(value, dict) or not INSTRUCTION_ID.match(str(value.get('id', ''))):
        return None
    words = value.get('words')
    if not isinstance(words, str) or not words.strip():
        return None
    return {'id': value['id'], 'words_sha256': hashlib.sha256(words.encode('utf-8')).hexdigest()}


def received_before(reports, instruction_id):
    """Whether one of this engine's own earlier live reports already said it received this id.

    `reports` is Control Center's `GET reports?recent=<n>` list, or None when it could not be read;
    unknown counts as not received, and Control Center ignores a repeated received ack.
    """
    for report in reports or []:
        activity = report.get('activity') if isinstance(report, dict) else None
        for entry in activity if isinstance(activity, list) else []:
            text = entry.get('line') if isinstance(entry, dict) else entry
            if isinstance(text, str) and text.startswith('Received') and f'instruction {instruction_id}' in text:
                return True
    return False


def instruction_lines(body, now, before):
    """The activity line that goes first, and the acks this run sends, for the open instruction."""
    found = instruction(body)
    if not found:
        return [], []
    iid, at = found['id'], now.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    if not serves_state(body):  # never claim a receipt the report cannot carry
        return [f'Read Krish\'s instruction {iid}; this directive does not take acks yet, so none is sent.'], []
    if before:
        activity = [f'Krish\'s instruction {iid} is still open; it was received in an earlier report.']
        acks = []
    else:
        activity = [f'Received Krish\'s instruction {iid} (its id only: his words stay in Control Center).']
        acks = [{'instruction_id': iid, 'state': 'received', 'line': RECEIVED, 'at': at, 'evidence_url': None}]
    if held(body):
        acks.append({'instruction_id': iid, 'state': 'blocked', 'line': HELD_LINE, 'at': at, 'evidence_url': None})
        activity.append(f'Instruction {iid} is blocked: this engine is held in Control Center.')
    elif before:
        activity[0] += ' This run only reads and reports, so it has not started on it.'
    return activity, acks


# ---------------------------------------------------------------------------
# Priorities: the North Star, then the constraint, then the recommendations.
# ---------------------------------------------------------------------------
def north_star(root):
    """The metric block of docs/NORTH_STAR.md, read with the standard library only."""
    text = read(root, 'docs/NORTH_STAR.md') or ''
    block = re.search(r'```yaml north-star-metric\n(.*?)```', text, re.S)
    if not block:
        return None
    body = block.group(1)

    def field(name):
        match = re.search(r'^' + name + r':\s*"?([^"\n]+?)"?\s*$', body, re.M)
        return match.group(1).strip() if match else None
    ladder = [(dt.date.fromisoformat(d), float(v)) for d, v in re.findall(r'-\s*\[(\d{4}-\d{2}-\d{2}),\s*([\d.]+)\]', body)]
    try:
        target = float(field('target'))
    except (TypeError, ValueError):
        target = None
    metric, deadline = field('metric'), field('deadline')
    if not metric or target is None or not deadline or not YMD.match(deadline):
        return None
    return {'metric': metric, 'unit': field('unit') or '', 'target': target, 'deadline': deadline, 'ladder': sorted(ladder)}


def amount(value, unit):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    number = f'{value:,.0f}' if float(value).is_integer() else f'{value:,.2f}'
    return f'${number}' if unit == 'USD' else f'{number} {unit}'.strip()


def north_star_line(root, body, now):
    """One line: the number, its deadline, this week's rung and, when Control Center read it, where it is."""
    star = north_star(root)
    if not star:
        return None
    unit = star['unit']
    text = f'{star["metric"]}: {amount(star["target"], unit)} by {star["deadline"]}.'
    block = (body or {}).get('north_star')
    own = block.get('own') if isinstance(block, dict) else None
    own = own if isinstance(own, dict) else {}
    today = now.astimezone(LONDON).date()
    rung = amount(own.get('week_target'), unit) or next(
        (amount(v, unit) for d, v in reversed(star['ladder']) if d <= today), None)
    current = amount(own.get('current'), unit)
    urgency = own.get('urgency') if own.get('urgency') in (1, 2, 3, 4, 5) else None
    if rung:
        text += f' This week\'s rung is {rung}'
        text += f'; read {current}' if current else ''
        text += f' (U{urgency}).' if urgency else '.'
    return text


def priorities(root, body, now, constraints, recommendations):
    """At most 5, ranked: the North Star, each product constraint, each standing recommendation."""
    keys = {o.get('key') for o in (body or {}).get('objectives') or [] if isinstance(o, dict)}
    candidates = [(north_star_line(root, body, now), NORTH_STAR_OBJECTIVE if NORTH_STAR_OBJECTIVE in keys else None)]
    candidates += [(reason, None) for reason in constraints]
    candidates += [(rec.get('title'), rec.get('objective_key')) for rec in recommendations if isinstance(rec, dict)]
    out, seen = [], set()
    for text, key in candidates:
        clean = line(text) if text else None
        if not clean or clean in seen:
            continue
        seen.add(clean)
        out.append({'rank': len(out) + 1, 'line': clean, 'objective_key': key if isinstance(key, str) and KEY.match(key) else None})
        if len(out) == PRIORITIES_MAX:
            break
    return out


# ---------------------------------------------------------------------------
# Obsessions: only his quoted words, while they are still in their file.
# ---------------------------------------------------------------------------
def obsessions(root):
    out = []
    for quote, since, path in OBSESSIONS:
        text = read(root, path)
        if text is None or ' '.join(quote.split()) not in ' '.join(text.split()):
            continue
        clean = line(f'"{quote}"')
        if clean and clean.endswith('"'):  # never a cut quote
            out.append({'line': clean, 'since': since})
    return out[:OBSESSIONS_MAX]


# ---------------------------------------------------------------------------
# Next steps: the first unticked build step, then NOW.md's "What is next".
# ---------------------------------------------------------------------------
def first_unticked_step(root):
    body = section(read(root, 'docs/GET-GOING.md'), 'The build')
    match = re.search(r'^- \[ \] \*\*Step (\d+)[^*]*\*\*\s*(.+)$', body, re.M)
    if not match:
        return None
    what = plain(match.group(2))
    stop = min([i for i in (what.find(': '), what.find('. ')) if i > 0] or [len(what)])
    return f'Build step {match.group(1)} (docs/GET-GOING.md): {what[:stop].rstrip(".")}.'


def now_next(root):
    """NOW.md's next steps, each with who it waits on, read from its own words."""
    out = []
    for bullet in bullets(section(read(root, 'NOW.md'), 'What is next and what is waiting on Krish')):
        text = plain(bullet)
        if not text or text.startswith('North Star check'):
            continue
        when = None
        dated = re.match(r'^Next \((\d{4}-\d{2}-\d{2})\):\s*(.+)$', text)
        if dated:
            when, text = dated.group(1), dated.group(2)
        # Who it waits on, from its own words: one that names Krish, or asks for a ruling ("Rule on ..."),
        # which only he makes (AGENTS.md, "Krish decides"), is his; the rest is the engine's own work.
        waits_on = 'krish' if re.search(r'\bKrish\b', text) or text.startswith('Rule on ') else 'engine'
        out.append((text, waits_on, when))
    return out


def next_steps(root):
    steps = []
    step = first_unticked_step(root)
    if step:
        steps.append((step, 'engine', None))
    steps += now_next(root)
    out = []
    for text, waits_on, when in steps:
        clean = line(text)
        if clean:
            out.append({'line': clean, 'waits_on': waits_on, 'when': when if when and YMD.match(when) else None})
        if len(out) == NEXT_STEPS_MAX:
            break
    return out


def state(root, body, now, constraints, recommendations):
    """The engine's state fields, each left out when it has no source."""
    fields = {'priorities': priorities(root, body, now, constraints, recommendations),
              'obsessions': obsessions(root), 'next_steps': next_steps(root)}
    return {k: v for k, v in fields.items() if v}
