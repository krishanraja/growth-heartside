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
  names heartside.io, so Control Center can make Heartside's subject.

The Wednesday Answers job then drafts its two answers from what AEO found:
the questions another site is cited first on, and AEO's moves
(`misses_and_moves`). Never fatal: a failed read or request is one line in
the report, and the run goes on. Asking is not spending; AEO asks at its own
research run, under its own cap.
"""
import json
from pathlib import Path

BANK = 'knowledge/aeo-question-bank.json'
DOMAINS = ('heartside.io',)
MAX_QUESTIONS = 25
NOTE = 'Gifts from your dog: an illustrated mug, a sherpa blanket or a portrait, with a note in the dog\'s own voice.'


def questions(root):
    """The bank's buyer questions, best first (priority, then tier), at most 25, each 8 to 300 characters."""
    try:
        bank = json.loads((Path(root) / BANK).read_text())
    except (OSError, ValueError):
        return []
    rows = [q for q in bank.get('questions', []) if isinstance(q, dict) and isinstance(q.get('question'), str)]
    rows.sort(key=lambda q: (q.get('priority') or 99, q.get('tier') or 9, q.get('id') or ''))
    out = []
    for q in rows:
        text = ' '.join(q['question'].split())
        if 8 <= len(text) <= 300 and text not in out:
            out.append(text)
    return out[:MAX_QUESTIONS]


def standing(directive):
    """Heartside's standing from the served directive, or None when it carries none (before 1.22.0, or unread)."""
    body = (directive or {}).get('directive') or {}
    block = body.get('ai_answers')
    return block.get('standing') if isinstance(block, dict) else None


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


def sync(client, directive, root):
    """One line on Heartside's AI answers, asking AEO first when Heartside has no request on file. Never raises."""
    if not served(directive):
        return []
    s = standing(directive)
    lines = [line(s)]
    if s and s.get('request'):
        return lines
    asked = questions(root)
    if not asked:
        return lines + ['No buyer question is in the bank to ask AEO about yet.']
    try:
        out = client.answers_request({'questions': asked, 'domains': list(DOMAINS), 'note': NOTE})
    except Exception as error:  # noqa: BLE001 - one line, never a failed run
        code = getattr(error, 'code', 'answers_request_failed')
        return lines + [f'Could not ask AEO-Engine to track Heartside\'s buyer questions ({code}); the next run asks again.']
    return lines + [f'Asked AEO-Engine to track {out.get("questions", len(asked))} of Heartside\'s buyer questions from its next research run.']
