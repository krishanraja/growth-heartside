"""AI answers through AEO-Engine, the one specialist (protocol 1.22.0).

Ruling (Krish, 2026-11-12): "AEO-Engine becomes the one specialist that every
venture's growth engine calls for its AI-answer work. Each venture's tile
shows its own AI-answer standing, the separate 'mind/make, AI answers' tile
goes, and Control Centre's own AI-answer checks and Heartside's separate
Answers job fold into AEO."

So this engine never asks an AI assistant itself. Each run:

- reads Heartside's own AI-answer standing from the directive (`ai_answers`),
  which AEO-Engine's fortnightly research wrote, and says it in one line;
- asks AEO, once, to track Heartside's buyer questions (the question bank in
  knowledge/aeo-question-bank.json, best first, at most 25) through
  `POST answers`, when Heartside has no request on file. The first request
  names heartside.io, so Control Center can make Heartside's subject;
- asks again, replacing the request on file, when the bank holds more valid
  questions than that request carries (`request.questions`), so a bank that
  grew is tracked whole. Valid is the protocol's own test, mirrored here: 8 to
  300 characters, never an address, a link or a number. Without that mirror,
  Control Center would keep fewer questions than were sent, the counts would
  never meet, and the engine would ask again every day;
- says so in one line when today's directive does not serve AI answers, so a
  request that was never filed is never silent;
- says so in one line, and asks nothing, when the directive serves AI answers
  but carries no `ai_answers` block to read: the protocol leaves it out when
  Control Center could not read the standing, so it never means "no request on
  file", and a request on file is never replaced on a guess.

The Wednesday Answers job then drafts its two answers from what AEO found:
the questions another site is cited first on, and AEO's moves
(`misses_and_moves`). Never fatal: a failed read or request is one line in
the report, and the run goes on. Asking is not spending; AEO asks at its own
research run, under its own cap.
"""
import json
import re
from pathlib import Path

BANK = 'knowledge/aeo-question-bank.json'
DOMAINS = ('heartside.io',)
MAX_QUESTIONS = 25
NOTE = 'Gifts from your dog: an illustrated mug, a sherpa blanket or a portrait, with a note in the dog\'s own voice.'
NOT_SERVED = "AI answers: not served by today's directive."
UNREAD = "AI answers: Heartside's standing could not be read today, so nothing was asked."
# Control Centre's own test for a buyer question (CONTACT in its src/lib/aiAnswers.ts, as
# growth-makeyourmindup's engine/ai_answers.py mirrors it): never an address, a link or a number.
CONTACT = re.compile(r'@|https?://|www\.|\+?\d[\d\s().-]{7,}\d', re.I)


def valid(text):
    """A question AEO's route takes: 8 to 300 characters, never an address, a link or a number."""
    return isinstance(text, str) and 8 <= len(text) <= 300 and not CONTACT.search(text)


def _key(text):
    """One key per question however it is cased or punctuated, so a near repeat is sent once."""
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', text.lower()).split())


def questions(root):
    """The bank's valid buyer questions, best first (priority, then tier), each once, at most 25."""
    try:
        bank = json.loads((Path(root) / BANK).read_text())
    except (OSError, ValueError):
        return []
    if not isinstance(bank, dict):
        return []
    rows = [q for q in bank.get('questions') or [] if isinstance(q, dict) and isinstance(q.get('question'), str)]
    rows.sort(key=lambda q: (q.get('priority') or 99, q.get('tier') or 9, str(q.get('id') or '')))
    out, seen = [], set()
    for q in rows:
        text = ' '.join(q['question'].split())
        if valid(text) and _key(text) not in seen:
            seen.add(_key(text))
            out.append(text)
    return out[:MAX_QUESTIONS]


def standing(directive):
    """Heartside's standing from the served directive, or None when it carries none (before 1.22.0, or unread)."""
    body = (directive or {}).get('directive') or {}
    block = body.get('ai_answers')
    return block.get('standing') if isinstance(block, dict) else None


def readable(directive):
    """Whether the directive carries a standing to read: an `ai_answers` block whose `standing` is null or a dict.
    The protocol leaves the block out when Control Center could not read the standing (1.22.0), never a guess."""
    block = ((directive or {}).get('directive') or {}).get('ai_answers')
    return isinstance(block, dict) and 'standing' in block and (block['standing'] is None or isinstance(block['standing'], dict))


def served(directive):
    """Whether the directive serves AI answers at all (features.ai_answers)."""
    body = (directive or {}).get('directive') or {}
    return bool((body.get('features') or {}).get('ai_answers')) or isinstance(body.get('ai_answers'), dict)


def short_day(ymd):
    months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    try:
        y, m, d = (int(x) for x in str(ymd)[:10].split('-'))
        return f'{d} {months[m - 1]}'
    except (ValueError, IndexError):
        return str(ymd)


def line(s):
    """Heartside's AI answers in one line, the words Control Center's tile uses."""
    if not s:
        return 'AI answers: not tracked yet.'
    latest = s.get('latest')
    if latest:
        n = latest.get('asked')
        return f'AI answers: cited first on {latest.get("cited_first")} of {n} question{"" if n == 1 else "s"}, {short_day(latest.get("as_of"))}.'
    request = s.get('request') or {}
    if request.get('state') == 'open':
        n = request.get('questions')
        return f'AI answers: AEO tracks {n} question{"" if n == 1 else "s"} from its next research run.'
    return 'AI answers: tracked, not asked yet.' if s.get('tracked') else 'AI answers: not tracked yet.'


def misses_and_moves(s):
    """What the Answers job drafts from: the questions another site is cited first on, then AEO's moves."""
    if not s:
        return []
    out = [m.get('question') for m in s.get('misses') or [] if isinstance(m, dict) and m.get('question')]
    out += [m.get('target_query') or m.get('title') for m in s.get('moves') or [] if isinstance(m, dict) and (m.get('target_query') or m.get('title'))]
    seen, unique = set(), []
    for q in out:
        if q not in seen:
            seen.add(q)
            unique.append(q)
    return unique


def on_file(s):
    """How many questions the request on file carries, or None when there is none or its count cannot be read."""
    request = (s or {}).get('request')
    if not isinstance(request, dict):
        return None
    n = request.get('questions')
    return n if isinstance(n, int) and not isinstance(n, bool) else None


def sync(client, directive, root):
    """One line on Heartside's AI answers, asking AEO first when Heartside has no request on file, or again
    when the bank holds more valid questions than the request on file. A standing that could not be read asks
    nothing. Never raises."""
    if not served(directive):
        return [NOT_SERVED]
    if not readable(directive):
        return [UNREAD]
    s = standing(directive)
    lines = [line(s)]
    filed = bool(s and s.get('request'))
    asked = questions(root)
    if filed:
        count = on_file(s)
        # Re-ask only on a readable count the bank now beats; an unreadable one never asks every day.
        if count is None or len(asked) <= count:
            return lines
    elif not asked:
        return lines + ['No buyer question is in the bank to ask AEO about yet.']
    try:
        out = client.answers_request({'questions': asked, 'domains': list(DOMAINS), 'note': NOTE})
    except Exception as error:  # noqa: BLE001 - one line, never a failed run
        code = getattr(error, 'code', 'answers_request_failed')
        return lines + [f'Could not ask AEO-Engine to track Heartside\'s buyer questions ({code}); the next run asks again.']
    n = out.get('questions', len(asked)) if isinstance(out, dict) else len(asked)
    if filed:
        return lines + [f'Asked AEO-Engine again to track {n} of Heartside\'s buyer questions, replacing the request on file '
                        f'for {count}, from its next research run.']
    return lines + [f'Asked AEO-Engine to track {n} of Heartside\'s buyer questions from its next research run.']
