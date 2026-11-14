"""AI answers through AEO-Engine, the one specialist (protocol 1.22.0, and proposed 1.23.0 where served).

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
- asks again, replacing the request on file, when the bank's valid questions
  are no longer the ones on file. Where the request carries its `digest`
  (proposed 1.23.0), that means the digest of the bank's list (`digest`,
  Control Center's own definition) differs from it, and this engine's last ask
  was not for exactly that list (the short digest the newest such line in its
  own recent reports carries, read back), so two readings that never meet
  cannot ask every day, and a bank that changes back is asked for again.
  Without one, it means the bank holds more valid questions than the request
  carries (`request.questions`). Valid is the protocol's own test, mirrored here: 8 to
  300 characters, never an address, a link or a number. Without that mirror,
  Control Center would keep fewer questions than were sent, the two would
  never meet, and the engine would ask again every day;
- says so in one line when today's directive does not serve AI answers, so a
  request that was never filed is never silent;
- says so in one line, and asks nothing, when the directive serves AI answers
  but carries no `ai_answers` block to read: the protocol leaves it out when
  Control Center could not read the standing, so it never means "no request on
  file", and a request on file is never replaced on a guess.

Where Control Center serves the detail (`features.ai_answers_detail`, proposed
1.23.0; Ruling, Krish, 2026-11-13: AEO's win kits reach him through each
venture's own growth engine), the run also:

- reads AEO's win kits in the standing (`kits`), says how many in one line,
  and keeps them for the Wednesday Answers brief under the gitignored
  `local/control-center/` (`save`, `saved_kits`), never in a committed file
  and never in the checkpoint;
- tells AEO which answers have shipped: the bank's published rows with their
  URL and date (`shipped`), sent with every request it files, and on their
  own (`mode: append`) once per change of that list. A change is known by
  the short digest in the line it reports, read back from its own last 10
  reports (`Reported`: a mark that ages out is told again, harmlessly);
  unknown counts as not told, so a shipped answer is never left out.

Until Control Center serves the detail, none of that happens and the requests
are exactly as before (a request is told apart by its digest only once Control
Center serves one). Everything is read loosely: a missing or malformed field
means no kits, never an error. This repository and its Actions logs are public,
so the report's lines carry counts only, never a question or a kit's words.

The Wednesday Answers job then briefs its two answers from AEO's kits, best
priority first, then from what AEO found: the questions another site is cited
first on, and AEO's moves (`misses_and_moves`). Never fatal: a failed read or
request is one line in the report, and the run goes on. Asking is not
spending; AEO asks at its own research run, under its own cap.
"""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import urllib.parse

BANK = 'knowledge/aeo-question-bank.json'
CACHE = 'local/control-center/ai-answers.json'
DOMAINS = ('heartside.io',)
MAX_QUESTIONS = 25
MAX_KITS = 5
KIT_DAYS = 8  # a saved reading older than this is not briefed from
NOTE = 'Gifts from your dog: an illustrated mug, a sherpa blanket or a portrait, with a note in the dog\'s own voice.'
NOT_SERVED = "AI answers: not served by today's directive."
UNREAD = "AI answers: Heartside's standing could not be read today, so nothing was asked."
SETTLED = ('AI answers: the request on file still reads differently from the bank after this engine asked for exactly '
           'these questions, so it is not asked again until the bank changes.')
# Control Centre's own test for a buyer question (CONTACT in its src/lib/aiAnswers.ts, as
# growth-makeyourmindup's engine/ai_answers.py mirrors it): never an address, a link or a number.
CONTACT = re.compile(r'@|https?://|www\.|\+?\d[\d\s().-]{7,}\d', re.I)
# JavaScript's \s and String.prototype.trim, exactly: Python's own str.split() also splits on \x1c-\x1f and \x85,
# and keeps \ufeff, so the digest uses this set and never str.split().
JS_SPACE = re.compile('[\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]+')
SURROGATE = re.compile('[\ud800-\udfff]')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
HOST = re.compile(r'^(?=.{4,253}$)[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$')
OWN_URL = re.compile(r'^https://(?:www\.)?heartside\.io(/[A-Za-z0-9/_-]*)?$')
PATH = re.compile(r'^/[a-z0-9][a-z0-9/_-]{0,199}$')
DATE = re.compile(r'^(\d{4}-\d{2}-\d{2})(?:T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2}))?$')
GAPS = ('no_page', 'not_retrieved', 'retrieved_not_cited', 'cited_not_first')
TARGETS = ('new_page', 'update_page', 'off_site_only')
HEARTSIDE_REPOS = ('heartside', 'krishanraja/heartside')


def valid(text):
    """A question AEO's route takes: 8 to 300 characters, never an address, a link or a number."""
    return isinstance(text, str) and 8 <= len(text) <= 300 and not CONTACT.search(text)


def question_key(text):
    """One key per question however it is cased or punctuated, so a near repeat is sent once."""
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', text.lower()).split())


def _rows(root):
    """The bank's question rows, best first (priority, then tier), or none when it cannot be read."""
    try:
        bank = json.loads((Path(root) / BANK).read_text())
    except (OSError, ValueError):
        return []
    if not isinstance(bank, dict) or not isinstance(bank.get('questions'), list):
        return []
    rows = [q for q in bank['questions'] if isinstance(q, dict) and isinstance(q.get('question'), str)]
    rank = lambda v, worst: v if isinstance(v, (int, float)) and not isinstance(v, bool) and v else worst  # noqa: E731
    rows.sort(key=lambda q: (rank(q.get('priority'), 99), rank(q.get('tier'), 9), str(q.get('id') or '')))
    return rows


def questions(root):
    """The bank's valid buyer questions, best first (priority, then tier), each once, at most 25."""
    out, seen = [], set()
    for q in _rows(root):
        text = clean(q['question'])
        if valid(text) and question_key(text) not in seen:
            seen.add(question_key(text))
            out.append(text)
    return out[:MAX_QUESTIONS]


def clean(text):
    """A question as Control Center's digest reads it: trimmed, internal whitespace one space (JavaScript's \\s)."""
    return JS_SPACE.sub(' ', text).strip(' ')


def digest(texts):
    """Control Center's `request.digest` of a list of questions (proposed 1.23.0), exactly.

    Each question trimmed, with internal whitespace collapsed to one space (JavaScript's \\s), sorted by code point,
    serialised as compact JSON with non-ASCII left unescaped (JSON.stringify; json.dumps with separators (',', ':')
    and ensure_ascii False), UTF-8 encoded, SHA-256 in lowercase hex. A lone surrogate is escaped as JSON.stringify
    escapes it, so the digest never fails.
    """
    norm = sorted(clean(t) for t in texts)
    text = SURROGATE.sub(lambda m: '\\u%04x' % ord(m.group()), json.dumps(norm, separators=(',', ':'), ensure_ascii=False))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def on_record(s):
    """The request on file's `digest`, or None when it carries none (before 1.23.0) or it is not a lowercase SHA-256."""
    request = s.get('request') if isinstance(s, dict) else None
    value = request.get('digest') if isinstance(request, dict) else None
    return value if isinstance(value, str) and HEX64.match(value) else None


def _body(directive):
    body = directive.get('directive') if isinstance(directive, dict) else None
    return body if isinstance(body, dict) else {}


def _features(directive):
    features = _body(directive).get('features')
    return features if isinstance(features, dict) else {}


def standing(directive):
    """Heartside's standing from the served directive, or None when it carries none (before 1.22.0, or unread)."""
    block = _body(directive).get('ai_answers')
    return block.get('standing') if isinstance(block, dict) else None


def readable(directive):
    """Whether the directive carries a standing to read: an `ai_answers` block whose `standing` is null or a dict.
    The protocol leaves the block out when Control Center could not read the standing (1.22.0), never a guess."""
    block = _body(directive).get('ai_answers')
    return isinstance(block, dict) and 'standing' in block and (block['standing'] is None or isinstance(block['standing'], dict))


def served(directive):
    """Whether the directive serves AI answers at all (features.ai_answers)."""
    return bool(_features(directive).get('ai_answers')) or isinstance(_body(directive).get('ai_answers'), dict)


def detailed(directive):
    """Whether Control Center serves the standing's detail: kits, the request's digest, and `shipped` and `mode` on
    `POST answers` (features.ai_answers_detail, proposed 1.23.0). Only a literal true switches it on."""
    return _features(directive).get('ai_answers_detail') is True


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


# ---------------------------------------------------------------------------
# AEO's win kits (proposed 1.23.0): a brief, never copy. Read loosely, kept small.
# ---------------------------------------------------------------------------
def _text(value, limit=300):
    """One line of text, whitespace collapsed, or None when it is not a string, is empty or is over the limit."""
    if not isinstance(value, str):
        return None
    text = ' '.join(value.split())
    return text if 0 < len(text) <= limit else None


def _texts(value, limit=300, most=8):
    return [t for t in (_text(v, limit) for v in (value if isinstance(value, list) else [])) if t][:most]


def _host(host, url=None):
    """A bare lowercase host, from `host` or else from `url`, or None."""
    candidates = [host]
    if isinstance(url, str):
        try:
            candidates.append(urllib.parse.urlsplit(url).hostname)
        except ValueError:
            pass
    for candidate in candidates:
        if isinstance(candidate, str):
            name = candidate.strip().lower().removeprefix('www.')
            if HOST.match(name):
                return name
    return None


def _number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) else None


def _kit(raw):
    """One kit, cleaned to the fields this engine briefs from, or None. Reading a cleaned kit again gives it back."""
    if not isinstance(raw, dict):
        return None
    question, title = _text(raw.get('question')), _text(raw.get('title'), 200)
    if not (question or title):
        return None
    target = raw.get('target') if isinstance(raw.get('target'), dict) else {}
    url = target.get('url') if isinstance(target.get('url'), str) and OWN_URL.match(target['url']) else None
    path = target.get('suggested_path') if isinstance(target.get('suggested_path'), str) and PATH.match(target['suggested_path']) else None
    capsule = raw.get('capsule') if isinstance(raw.get('capsule'), dict) else {}
    beat, hosts = [], set()
    for page in raw.get('beat') if isinstance(raw.get('beat'), list) else []:
        host = _host(page.get('host'), page.get('url')) if isinstance(page, dict) else None
        if host and host not in hosts:
            hosts.add(host)
            beat.append({'host': host})
    fixes = []
    for fix in raw.get('site_fixes') if isinstance(raw.get('site_fixes'), list) else []:
        if not isinstance(fix, dict):
            continue
        cleaned = {'gate': _text(fix.get('gate'), 60), 'host': _host(fix.get('host'), fix.get('url')),
                   'fix': _text(fix.get('fix')), 'owner_repo': _text(fix.get('owner_repo'), 120)}
        if cleaned['fix']:
            fixes.append(cleaned)
    gap = raw.get('gap_class')
    kind = target.get('kind')
    return {'kit_id': _text(raw.get('kit_id'), 120), 'query_id': _text(raw.get('query_id'), 120),
            'question': question, 'title': title, 'priority': _number(raw.get('priority')),
            'gap_class': gap if gap in GAPS else None,
            'target': {'kind': kind if kind in TARGETS else None, 'url': url,
                       'host': _host(target.get('host'), url), 'suggested_path': path},
            'capsule': {'rules': _texts(capsule.get('rules')), 'must_cover': _texts(capsule.get('must_cover'), 200)},
            'h2s': _texts(raw.get('h2s'), 120, 6), 'beat': beat[:3], 'site_fixes': fixes[:5]}


def kits(s):
    """AEO's win kits in a standing, best priority first (the highest number: AEO-Engine's `kitPriority` is class
    weight x demand x winnability, and its own `buildKits` sorts highest first; a kit with none goes last), each
    question once, at most 5. A standing with no kits, or a malformed one, gives none, never an error."""
    raw = s.get('kits') if isinstance(s, dict) else None
    ranked = []
    for i, entry in enumerate(raw if isinstance(raw, list) else []):
        kit = _kit(entry)
        if kit and question_key(kit['question'] or kit['title']):
            p = kit['priority']
            ranked.append(((0, -p, i) if p is not None else (1, 0, i), kit))
    ranked.sort(key=lambda r: r[0])
    found, seen = [], set()
    for _, kit in ranked:  # a repeated question keeps its best-ranked kit, the highest priority
        key = question_key(kit['question'] or kit['title'])
        if key not in seen:
            seen.add(key)
            found.append(kit)
    return found[:MAX_KITS]


def for_heartside(fix):
    """Whether a site fix is Heartside's to make: its owner names the heartside repository, or no owner at all."""
    owner = (fix.get('owner_repo') or '').lower()
    return not owner or owner in HEARTSIDE_REPOS


def save(root, found, now=None):
    """Keep the kits for the Wednesday brief under gitignored local/control-center/ (not in the checkpoint). Never raises."""
    now = now or dt.datetime.now(dt.timezone.utc)
    path = Path(root) / CACHE
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps({'saved_at': now.isoformat(timespec='seconds'), 'kits': found}, ensure_ascii=False))
        temporary.replace(path)
        return True
    except (OSError, TypeError, ValueError):
        return False


KITS_HOLD = 'local/control-center/kits-hold.json'


def hold_kits(root, reason):
    """Record why this machine could not read AEO's kits, so the Wednesday brief says so instead of silently using
    bank order. Words only, never a token. Never raises."""
    try:
        path = Path(root) / KITS_HOLD
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({'reason': str(reason)[:300]}))
    except OSError:
        pass


def clear_kits_hold(root):
    try:
        (Path(root) / KITS_HOLD).unlink()
    except OSError:
        pass


def kits_hold(root):
    """The recorded reason AEO's kits were not read on this machine, or None."""
    try:
        return json.loads((Path(root) / KITS_HOLD).read_text()).get('reason') or None
    except (OSError, ValueError, AttributeError):
        return None


def saved_kits(root, now=None):
    """The kits the last read kept (`save`), or none when there are none, they are over 8 days old, or unreadable."""
    try:
        data = json.loads((Path(root) / CACHE).read_text())
        saved = dt.datetime.fromisoformat(data['saved_at'])
    except (OSError, ValueError, KeyError, TypeError):
        return []
    now = now or dt.datetime.now(dt.timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=dt.timezone.utc)  # a clock given with no offset (`growth.py run --now`) is read as UTC
    if saved.tzinfo is None or not dt.timedelta(0) <= now - saved <= dt.timedelta(days=KIT_DAYS):
        return []
    return kits({'kits': data.get('kits')})


def fetch(client, root):
    """Read Heartside's standing on its own (GET answers) and keep its kits for the Wednesday brief (`growth.py cc
    kits`). Read only. One line, counts only. Never raises."""
    s = client.answers_standing()
    if not isinstance(s, dict):
        hold_kits(root, 'no AI-answer standing could be read from Control Center')
        return 'AI answers: no standing could be read for Heartside, so no kit was kept.'
    if not isinstance(s.get('kits'), list):
        clear_kits_hold(root)  # read, and Control Center serves no kits yet: not a hold
        return 'AI answers: Control Center does not serve AEO-Engine\'s kits yet, so none was kept.'
    found = kits(s)
    if not save(root, found):
        hold_kits(root, 'AEO-Engine\'s kits could not be kept on this machine')
        return 'AI answers: AEO-Engine\'s kits could not be kept on this machine.'
    clear_kits_hold(root)
    return kits_line(found)


def kits_line(found):
    n = len(found)
    if not n:
        return 'AEO-Engine has no win kit for Heartside yet.'
    return f'AEO-Engine has {n} win kit{"" if n == 1 else "s"} for Heartside; the Wednesday Answers brief takes the best two.'


def misses_and_moves(s):
    """What the Answers job drafts from: AEO's kits first, then the questions another site is cited first on, then
    AEO's moves."""
    if not s:
        return []
    out = [k['question'] or k['title'] for k in kits(s)]
    out += [m.get('question') for m in s.get('misses') or [] if isinstance(m, dict) and m.get('question')]
    out += [m.get('target_query') or m.get('title') for m in s.get('moves') or [] if isinstance(m, dict) and (m.get('target_query') or m.get('title'))]
    seen, unique = set(), []
    for q in out:
        if q not in seen:
            seen.add(q)
            unique.append(q)
    return unique


# ---------------------------------------------------------------------------
# What has shipped (proposed 1.23.0): the bank's published answers.
# ---------------------------------------------------------------------------
def shipped(root):
    """The bank's published answers as AEO's `shipped` declarations, `{question, url, shipped_at}`, best first.

    Only a row with status `published`, a valid question, its heartside.io URL and its publish date counts. A row
    missing any of them is left out, never guessed.
    """
    out, seen = [], set()
    for q in _rows(root):
        text = clean(q['question'])
        url, when = q.get('url'), q.get('published')
        if q.get('status') != 'published' or not valid(text) or question_key(text) in seen:
            continue
        if not isinstance(url, str) or not OWN_URL.match(url) or not isinstance(when, str) or not DATE.match(when):
            continue
        try:
            dt.date.fromisoformat(when[:10])
        except ValueError:
            continue
        seen.add(question_key(text))
        out.append({'question': text, 'url': url, 'shipped_at': when})
    return out


def shipped_mark(entries):
    """The short digest a report line carries for one shipped list, so the next run knows AEO was told of it."""
    ordered = sorted(entries, key=lambda e: (e['question'], e['url'], e['shipped_at']))
    text = json.dumps(ordered, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return 'shipped list ' + hashlib.sha256(text.encode('utf-8', 'surrogatepass')).hexdigest()[:12]


def questions_mark(asked):
    """The short digest a report line carries for the exact list of questions this engine asked for."""
    return 'questions ' + digest(asked)[:12]


QUESTIONS_MARK = re.compile(r'\((questions [0-9a-f]{12})\)')


class Reported:
    """This engine's own recent live reports (`GET reports?recent=10`, newest first), read at most once a run, searched
    for a mark. Unknown (no reader, or a failed read) is never found: a shipped answer is never left out, and a request
    is never held back on a guess.

    The window is the protocol's: at most the last 10 live reports. So "once per change" is once per change within
    them, and a mark that ages out is acted on again: an unchanged shipped list is appended again (the same entries,
    so AEO's list is unchanged), and a request whose digest never meets the bank is asked for again, each at most once
    per 10 reports, since that line carries its mark afresh. This is deliberate: the reports are the only memory the
    hosted Control Center run keeps (its runner is ephemeral and writes no checkpoint), and a re-tell is harmless."""

    def __init__(self, client):
        self.client, self.lines = client, None

    def has(self, mark):
        """Whether any line in the window carries this mark (shipped lists: AEO appends them, so an older tell holds)."""
        return any(f'({mark})' in text for text in self._read())

    def newest_questions(self):
        """The newest `questions` mark in the window, or None: the list this engine last asked for, which a re-ask
        compares with, so a bank that goes from A to B and back to A asks for A again."""
        for text in self._read():
            found = QUESTIONS_MARK.search(text)
            if found:
                return found.group(1)
        return None

    def _read(self):
        if self.lines is None:
            self.lines = []
            reader = getattr(self.client, 'recent_reports', None)
            try:
                reports = reader(10) if reader else []
            except Exception:  # noqa: BLE001 - unknown is not found
                reports = []
            for report in reports if isinstance(reports, list) else []:
                activity = report.get('activity') if isinstance(report, dict) else None
                for entry in activity if isinstance(activity, list) else []:
                    text = entry.get('line') if isinstance(entry, dict) else entry
                    if isinstance(text, str):
                        self.lines.append(text)
        return self.lines


def on_file(s):
    """How many questions the request on file carries, or None when there is none or its count cannot be read."""
    request = (s or {}).get('request')
    if not isinstance(request, dict):
        return None
    n = request.get('questions')
    return n if isinstance(n, int) and not isinstance(n, bool) else None


def _post(client, body):
    """POST answers. Returns (questions on file, None) or (None, failure code)."""
    try:
        out = client.answers_request(body)
    except Exception as error:  # noqa: BLE001 - one line, never a failed run
        return None, getattr(error, 'code', 'answers_request_failed')
    n = out.get('questions') if isinstance(out, dict) else None
    return (n if isinstance(n, int) and not isinstance(n, bool) else len(body['questions'])), None


def _plural(n, word):
    return f'{n} {word}{"" if n == 1 else "s"}'


def sync(client, directive, root):
    """Heartside's AI answers in a few lines, asking AEO first when Heartside has no request on file, again when the
    bank's valid questions are no longer the ones on file, and, where the detail is served, telling it once of each
    change to what has shipped. A standing that could not be read asks nothing. Lines carry counts only. Never raises."""
    if not served(directive):
        return [NOT_SERVED]
    if not readable(directive):
        return [UNREAD]
    s = standing(directive)
    detail = detailed(directive)
    lines = [line(s)]
    done = []
    if detail:
        found = kits(s)
        save(root, found)
        lines.append(kits_line(found))
        done = shipped(root)
    filed = bool(s and s.get('request'))
    asked = questions(root)
    count = on_file(s)
    recorded = on_record(s)
    reported = Reported(client)
    if filed:
        if recorded is not None:
            changed = bool(asked) and digest(asked) != recorded
            if changed and reported.newest_questions() == questions_mark(asked):
                # This exact list was the last one asked for and the request on file still reads otherwise: never every day.
                lines.append(SETTLED)
                changed = False
        else:
            # Re-ask only on a readable count the bank now beats; an unreadable one never asks every day.
            changed = count is not None and len(asked) > count
        if not changed:
            if detail and done and not reported.has(shipped_mark(done)):
                return lines + _tell_shipped(client, done)
            return lines
    elif not asked:
        return lines + ['No buyer question is in the bank to ask AEO about yet.']
    body = {'questions': asked, 'domains': list(DOMAINS), 'note': NOTE}
    if detail:
        body['mode'] = 'replace'
        if done:
            body['shipped'] = done
    n, code = _post(client, body)
    if code:
        return lines + [f'Could not ask AEO-Engine to track Heartside\'s buyer questions ({code}); the next run asks again.']
    # The marks are digests, never words: the next run reads them back from its own reports.
    marked = f' ({questions_mark(asked)})' if detail or recorded is not None else ''
    carried = f', with {_plural(len(done), "shipped answer")} ({shipped_mark(done)})' if detail and done else ''
    if not filed:
        return lines + [f'Asked AEO-Engine to track {n} of Heartside\'s buyer questions from its next research run{marked}{carried}.']
    if recorded is not None:
        return lines + [f'Asked AEO-Engine again to track {n} of Heartside\'s buyer questions, replacing the request on file, '
                        f'whose questions no longer match the bank, from its next research run{marked}{carried}.']
    return lines + [f'Asked AEO-Engine again to track {n} of Heartside\'s buyer questions, replacing the request on file '
                    f'for {count}, from its next research run{marked}{carried}.']


def _tell_shipped(client, done):
    """Tell AEO which answers have shipped, adding their questions to the request on file (mode append)."""
    body = {'questions': [e['question'] for e in done][:MAX_QUESTIONS], 'domains': list(DOMAINS), 'note': NOTE,
            'mode': 'append', 'shipped': done}
    _, code = _post(client, body)
    if code:
        return [f'Could not tell AEO-Engine which of Heartside\'s answers have shipped ({code}); the next run tells it again.']
    n = len(done)
    return [f'Told AEO-Engine that {n} of Heartside\'s answers {"has" if n == 1 else "have"} shipped ({shipped_mark(done)}).']
