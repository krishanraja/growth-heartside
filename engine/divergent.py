"""Consulting divergent-thinker, the fleet's divergent thinking engine, through Control Center.

Control Center serves it to this engine on one route, `POST /api/growth/engines/heartside/divergent`, on the engine's
own bearer (control-center PR 963). The engine uses it in three places, and only while Control Center's capabilities
say `features.divergent: true`. Until then nothing here makes a call, raises or changes a result: it says
"divergent-thinker is not served" once, quietly, and the engine runs exactly as before.

1. **Recovery plays at U4 and U5** (`recovery`). The protocol asks an engine with nothing proposed for "at U4 one bold
   swing, at U5 three unconventional recovery plays, each different in kind" (ENGINE-PROTOCOL.md, "The directive's
   order", step 5). When the live report would carry no proposal, the engine is not held and its own number is at U4
   or U5, it asks `diverge` once a day for three strategy sparks, built from live store truth and the North Star line,
   never a customer's details. Every spark passes this engine's own copy and claims checks (`growth.problems`) and
   the walls below before it is proposed. One ask per engine at a time still holds on his list, so the best spark
   that passes becomes one plan behind `strategy`; the others stay in the report's activity, by title.
2. **The joke lab's screen** (`factory/jokelab.py screen`): `score` with the live posts and floor lines as the
   obvious, zero model calls, so a candidate too close to them (`rejected_gravity`) or repeating what shipped
   (`rejected_archive`) is rejected before any judge reads it.
3. **What went live** (`growth.py events import`): the live captions, public brand words only, go to `record`, so
   divergent-thinker never hands them back and later scores flag repeats.

The walls: the engine proposes, Krish decides. A spark becomes a plan on his list and nothing more; nothing here
posts, sends or spends, and the diverge call (about 25 model calls, about $1.30, capped by Control Center at one a
day) runs only in a live report run. The bearer is the engine's own and is never printed, logged or written.
"""
import datetime as dt
import json
import os
from pathlib import Path
import re

from .control_center import Client, ProtocolError, sha256

ENGINE_ID = 'growth-heartside'
NAMESPACE, JOKES = ENGINE_ID, ENGINE_ID + ':jokes'
DEFAULT_URL = 'https://controlcenter.krishraja.com'
MARKER = 'local/control-center/divergent.json'
DIVERGE_TIMEOUT, SCORE_TIMEOUT = 300, 60
IDEAS_MAX, OBVIOUS_MAX, RECORD_MAX = 100, 30, 200
OBVIOUS_CHARS, IDEA_CHARS = 400, 1000
OPEN_DAYS = 7
NOT_SERVED = 'divergent-thinker is not served by Control Center yet (features.divergent is off), so it was not consulted.'
REJECTS = {'rejected_gravity': 'too close to what live posts and Krish\'s floor already say (divergent-thinker, rejected_gravity)',
           'rejected_archive': 'repeats what Heartside already shipped (divergent-thinker, rejected_archive)'}
GENERIC_CLICHES = ('Post more often', 'Run paid ads', 'Gift products to influencers', 'Offer a discount code')
CLOSE_EVENT = 'plan_decided'
PROPOSAL_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9:._-]{0,119}$')

# Walls a spark is read against before it reaches Krish, on top of the copy and claims checks. The first two are the
# two plays of the 18 Nov live run that read well and could not go out: one used strangers' photos without consent,
# one pitched AI-made portraits to communities that ban AI art.
PHOTO = r'(?:photos?|pictures?|pics|images?|snaps?|selfies|videos?|clips?)'
OTHERS = (r"(?:strangers?|other (?:people|owners|accounts|creators)|someone else|people|owners|dog owners|customers?|buyers?"
          r"|followers?|commenters?|fans|users|the public|neighbou?rs?|passers-?by)")
WALLS = [
    (re.compile(r'\b' + OTHERS + r"(?:'s|s'|’s|s’|')?\s+(?:own\s+|real\s+|public\s+)?(?:dogs?(?:'s|s'|’s)?\s+)?" + PHOTO + r'\b'
                r'|\b' + PHOTO + r'\s+(?:of|from)\s+(?:strangers|other people|people|owners|followers|customers|the public|their)\b'
                r'|\b(?:scrape|scraping|repost|reposting|screenshot|screenshotting|pull|pulling|grab|grabbing)\s+(?:\w+\s+){0,3}' + PHOTO + r'\b',
                re.I),
     'builds on other people\'s photos or dogs: that needs their recorded permission, which this engine cannot hold or '
     'check (AGENTS.md rule 6; the 18 Nov live run)'),
    (re.compile(r'(?=.*\b(?:subreddits?|r/\w+|reddit|communit(?:y|ies)|forums?|groups?|clubs?|discord|meetups?|breed clubs?)\b)'
                r'(?=.*\b(?:ai|a\.i\.|generated|portraits?|paintings?|artwork|art)\b)', re.I | re.S),
     'takes the AI-made art into a community, and many dog and art communities ban AI art or selling; a person reads that '
     'community\'s own rules first (the 18 Nov live run)'),
    (re.compile(r'\b(?:mass|bulk|cold)[- ](?:dms?|messages?|messaging|outreach|emails?|comments?)\b|\bautomated (?:dms?|messages|comments|replies|outreach)\b'
                r'|\bdm(?:s|ing)?\s+(?:\d+|hundreds|dozens|every|all)\b|\bfollow[- ](?:chasing|for[- ]follow|unfollow)\b', re.I),
     'outreach in bulk: no mass outreach, automated messages or follow chasing (AGENTS.md rule 7)'),
    (re.compile(r'\b(?:run|buy|launch|place|start|test)\s+(?:\w+\s+){0,2}?(?:paid\s+)?(?:ads?|boosts?|ad campaigns?)\b|\bad spend\b'
                r'|\bpaid (?:ads?|boosts?|promotion|placements?)\b|\bpay(?:ing)? (?:creators|influencers)\b', re.I),
     'spends money: the budget is $0 and a spend is its own ask behind the spend wall (AGENTS.md rule 1)'),
    (re.compile(r'\b(?:ai|a\.i\.|generated|synthetic|fake)[- ](?:people|persons?|customers?|buyers?|reviewers?|reviews?|testimonials?'
                r'|ugc|influencers?|avatars?|owners?)\b', re.I),
     'an AI person as a customer, reviewer or testimonial, which is never allowed (AGENTS.md rule 4)'),
    (re.compile(r"\b(?:customer|buyer|order|shopper)s?(?:'|’)?s?\s+(?:names?|emails?|addresses|data|lists?|details|photos?|answers?)\b"
                r'|\b(?:email|text|message)\s+(?:our|the|past|every)\s+(?:customers|buyers)\b', re.I),
     'uses customers\' details, which never leave the store (AGENTS.md rule 6)'),
]


def served(features):
    """True only when Control Center's capabilities say the divergent route is live for this engine."""
    return isinstance(features, dict) and features.get('divergent') is True


def call(client, body, timeout=SCORE_TIMEOUT):
    """One POST to the route. Returns the body on ok, or raises ProtocolError with a lower_snake code."""
    return client.divergent(body, timeout=timeout)


def client_from_env(env=None):
    """The engine's own client, or None when no bearer is set here. Never prints or keeps the token."""
    env = os.environ if env is None else env
    token = (env.get('CONTROL_CENTER_ENGINE_TOKEN') or '').strip()
    if not token:
        return None
    try:
        return Client((env.get('CONTROL_CENTER_URL') or '').strip() or DEFAULT_URL, token, 'heartside')
    except ProtocolError:
        return None


def served_client(env=None):
    """(client, note): a client when the route is served, else None and a one-line reason. Never raises."""
    client = client_from_env(env)
    if client is None:
        return None, 'divergent-thinker not consulted: no Control Center engine token in this environment.'
    try:
        features = client.capabilities()
    except ProtocolError as error:
        return None, f'divergent-thinker not consulted: Control Center capabilities unread ({error.code}).'
    except Exception as error:  # noqa: BLE001 - a cut connection is a note, never a failed run
        return None, f'divergent-thinker not consulted: Control Center capabilities unread ({type(error).__name__}).'
    if not served(features):
        return None, NOT_SERVED
    return client, None


def _strings(values, limit, chars):
    out = []
    for value in values:
        text = ' '.join(str(value or '').split())[:chars]
        if text and text not in out:
            out.append(text)
        if len(out) == limit:
            break
    return out


def banned_words(growth):
    return list(dict.fromkeys(list(growth.BANNED) + list(growth.SLOP)))


# ---------------------------------------------------------------------------
# score and record (zero model calls).
# ---------------------------------------------------------------------------
def score(client, problem, ideas, obvious, banned=(), namespace=JOKES):
    """Each idea's result, in the order given (up to IDEAS_MAX at a time), or raises ProtocolError."""
    ideas = [' '.join(str(i).split())[:IDEA_CHARS] for i in ideas]
    obvious = _strings(obvious, OBVIOUS_MAX, OBVIOUS_CHARS)
    out = []
    for start in range(0, len(ideas), IDEAS_MAX):
        chunk = ideas[start:start + IDEAS_MAX]
        body = {'op': 'score', 'problem': problem, 'ideas': chunk, 'obvious': obvious, 'namespace': namespace}
        if banned:
            body['bannedWords'] = list(banned)
        answer = call(client, body)
        results = answer.get('results')
        if not isinstance(results, list):
            raise ProtocolError('invalid_divergent_response')
        if len(results) == len(chunk):
            out += results
        else:  # matched by title when Control Center leaves one out
            by_title = {r.get('title'): r for r in results if isinstance(r, dict)}
            out += [by_title.get(idea) for idea in chunk]
    return out


def record(client, items, label, namespace=JOKES):
    """Tell divergent-thinker what shipped. Returns how many were sent, or raises ProtocolError."""
    items = _strings(items, RECORD_MAX, IDEA_CHARS)
    if not items:
        return 0
    answer = call(client, {'op': 'record', 'items': items, 'label': label[:120], 'namespace': namespace})
    if answer.get('ok') is not True:
        raise ProtocolError('invalid_divergent_response')
    return len(items)


def screen_scorer(env=None):
    """For the joke lab: (scorer, note). scorer(problem, ideas, obvious, banned) -> results, or None when not served."""
    client, note = served_client(env)
    if client is None:
        return None, note

    def scorer(problem, ideas, obvious, banned=()):
        return score(client, problem, ideas, obvious, banned, JOKES)
    return scorer, 'divergent-thinker scored the screen (zero model calls).'


def rejection(result):
    """The screen's reason to reject one candidate from its score result, or None."""
    status = result.get('status') if isinstance(result, dict) else None
    return REJECTS.get(status)


# ---------------------------------------------------------------------------
# What went live.
# ---------------------------------------------------------------------------
def live_captions(root, events, results):
    """The public brand words of events newly applied by this import: a live engagement's text, a published creative's
    caption when its pack is on this machine. Never anything else in a record."""
    applied = {r.get('event_id') for r in results or [] if isinstance(r, dict) and r.get('status') == 'applied'}
    out, published = [], []
    for event in events or []:
        if not isinstance(event, dict) or event.get('event_id') not in applied:
            continue
        rec = event.get('record') if event.get('type') == 'social' else None
        if isinstance(rec, dict) and rec.get('kind') == 'engagement' and rec.get('stage') == 'live_verified' and isinstance(rec.get('text'), str):
            out.append(rec['text'])
        elif event.get('type') == 'creative_status' and event.get('status') == 'published':
            published.append(event.get('creative_id'))
    if published:
        from .protocol import caption_index
        index = caption_index(root)
        for cid in published:
            items = index.get(cid) or []
            if items:
                out.append(items[-1]['text'])
    return [t for t in out if t.strip()]


def record_live(root, events, results, env=None, today=None):
    """After `events import`: send what went live to `record` under the jokes namespace. Returns one quiet line."""
    captions = live_captions(root, events, results)
    if not captions:
        return 'divergent-thinker: nothing newly live to record.'
    client, note = served_client(env)
    if client is None:
        return note
    try:
        n = record(client, captions, f'live {(today or dt.date.today()).isoformat()}', JOKES)
    except ProtocolError as error:
        return f'divergent-thinker did not record what went live ({error.code}); the import itself stands.'
    return f'divergent-thinker recorded {n} live caption(s) under {JOKES}, so they are never handed back.'


# ---------------------------------------------------------------------------
# Recovery plays at U4 and U5 (the cc report path).
# ---------------------------------------------------------------------------
def own_urgency(body, root):
    """This engine's own urgency, 1 to 5: the directive's north_star.own first, then NOW.md's state line. None if unread."""
    star = (body or {}).get('north_star')
    own = star.get('own') if isinstance(star, dict) else None
    value = own.get('urgency') if isinstance(own, dict) else None
    if value in (1, 2, 3, 4, 5):
        return value
    try:
        text = (Path(root) / 'NOW.md').read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None
    match = re.search(r'<!-- north-star-state (\{.*?\}) -->', text)
    try:
        value = json.loads(match.group(1)).get('urgency') if match else None
    except ValueError:
        return None
    return value if value in (1, 2, 3, 4, 5) else None


def plan_cliches(root):
    """The current U5 plays, from the newest order-loop plan's "The three U5 recovery plays", plus the generic ones."""
    plays = []
    for path in sorted(Path(root).glob('docs/plans/*order-loop*.md'), reverse=True):
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        match = re.search(r'^## The three U5 recovery plays\s*$(.*?)(?=^## |\Z)', text, re.M | re.S)
        if not match:
            continue
        for item in re.split(r'^\d+\.\s+', match.group(1), flags=re.M)[1:]:
            words = ' '.join(item.replace('**', '').split())
            if words:
                plays.append(words[:300])
        break
    return plays + list(GENERIC_CLICHES)


def problem_text(state, north_star, organic):
    """The problem, from live store truth and the North Star line. Counts and public prices only, never a customer."""
    from . import offers
    gifts = []
    for gift in offers.catalog(state):
        if not gift.get('ready'):
            continue
        prices = ' or '.join(f'${c / 100:g}' for c in gift.get('prices_cents') or [gift.get('price_cents')] if c)
        gifts.append(f'{gift.get("name") or gift.get("id")} ({prices})')
    sells = ', '.join(gifts) if gifts else 'a mug, a sherpa blanket and a portrait'
    reading = organic.get('value') if isinstance(organic, dict) else None
    reading = f'${reading:,}' if isinstance(reading, (int, float)) else 'not measured'
    return (f'Heartside (heartside.io) sells gifts from your dog to US buyers, made to order: {sells}. Each gift is '
            'artwork only, painted from a photo of the buyer\'s dog, with a short note from the dog in the box. '
            f'{north_star or "The North Star is organic net sales."} Organic net sales over the trailing 28 days: '
            f'{reading}. Find recovery plays that could make organic posts sell gifts before Christmas with $0 of paid '
            'ads. The walls: no customer data, nothing posted, sent or spent without Krish\'s yes, no invented reviews, '
            'ratings or scarcity, the product on screen is always the real design, and no other person\'s photos '
            'without their permission.')


def spark_text(spark):
    return '\n'.join(str(spark.get(k) or '') for k in ('title', 'mechanism', 'whyNonObvious', 'firstStep') if spark.get(k))


def spark_problems(spark, growth, price_points=()):
    """Every reason this engine refuses one spark: its own copy and claims checks, then the walls."""
    text = spark_text(spark)
    if not text.strip():
        return ['it has no words']
    out = list(growth.problems({'platform': 'email', 'text': text}, price_points))
    out += [why for rx, why in WALLS if rx.search(text)]
    return list(dict.fromkeys(out))


def spark_label(spark, run_id):
    return f'divergent-thinker spark {spark.get("id") or spark.get("rank")}, run {run_id}'


def _fit(text, limit):
    text = ' '.join(str(text or '').split())
    if len(text) <= limit:
        return text
    cut = text[:limit]
    return cut[:cut.rfind(' ')].rstrip(' ,;:') if ' ' in cut else cut


def proposal_for(spark, run_id, urgency, now):
    """One spark as a plan behind strategy, shaped as recommendations.json's plans are (stage plan, exact_payload)."""
    safe_run = re.sub(r'[^A-Za-z0-9._-]', '-', str(run_id))[:60] or 'run'
    pid = f'heartside:divergent:{safe_run}:{spark.get("rank") or 1}'
    if not PROPOSAL_ID.match(pid):
        raise ValueError('divergent proposal id')
    title = _fit(f'Recovery play: {spark.get("title")}', 160)
    plan = '\n'.join(line for line in [
        f'Recovery play at U{urgency}: {_fit(spark.get("title"), 300)}',
        '',
        f'How it works: {_fit(spark.get("mechanism"), 1500)}',
        f'Why it is not the obvious move: {_fit(spark.get("whyNonObvious"), 1500)}',
        f'First step: {_fit(spark.get("firstStep"), 1000)}',
        f'The conventional version it replaces: {_fit(spark.get("conventionalTwin"), 600)}' if spark.get('conventionalTwin') else None,
        '',
        f'Made by divergent-thinker through Control Center ({spark_label(spark, run_id)}, kind {spark.get("kind") or "not given"}, '
        f'lens {spark.get("lens") or "not given"}, {"survived" if spark.get("survivedAttack") else "did not face or survive"} '
        'its attack round). It passed this engine\'s copy and claims checks.',
        'Nothing is posted, sent or spent from this plan. Once you approve it, the engine builds it up to go-live and asks you again.',
    ] if line is not None)[:8000]
    why = _fit(f'{spark.get("whyNonObvious") or ""} Next: {spark.get("firstStep") or "build the first step"}', 1000)
    payload = {'title': title, 'why': why, 'plan': plan}
    return {'proposal_id': pid, 'title': title, 'why': why, 'kind': 'prepared', 'wall': 'strategy', 'amount_usd': None,
            'channel': None, 'objective_key': 'organic_net_sales_usd', 'exact_payload': plan,
            'payload_sha256': sha256(payload), 'evidence': [{'label': spark_label(spark, run_id), 'url': None}],
            'close_condition': {'event': CLOSE_EVENT, 'reference': _fit(spark.get('title'), 500)},
            'expires_at': (now + dt.timedelta(days=OPEN_DAYS)).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'stage': 'plan', 'parent_proposal_id': None}


def _marker(root):
    try:
        return json.loads((Path(root) / MARKER).read_text())
    except (OSError, ValueError):
        return {}


def _mark(root, day):
    path = Path(root) / MARKER
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'last_diverge_day': day}) + '\n')


def open_spark(reports, decisions, now):
    """The spark plan a recent live report proposed and Krish has not declined, or None. Unread reports are unknown."""
    declined = {d.get('proposal_id') for d in decisions or [] if isinstance(d, dict) and d.get('decision') == 'declined'}
    for report in reports or []:
        run = str(report.get('run_id') or '') if isinstance(report, dict) else ''
        day = re.match(r'^heartside:(\d{4}-\d{2}-\d{2}):', run)
        try:
            if not day or (now.date() - dt.date.fromisoformat(day.group(1))).days > OPEN_DAYS:
                continue
        except ValueError:
            continue
        for entry in report.get('activity') or []:
            text = entry.get('line') if isinstance(entry, dict) else entry
            found = re.search(r'heartside:divergent:[A-Za-z0-9:._-]+', text) if isinstance(text, str) else None
            if found and text.startswith('Proposed divergent-thinker') and found.group(0).rstrip('.') not in declined:
                return found.group(0).rstrip('.')
    return None


def recovery(*, root, growth, client, body, features, state, organic, north_star, held, mode, now,
             price_points=(), recent_reports=None):
    """Recovery plays when nothing else is proposed. Returns {'proposals': [...], 'activity': [...]}, both possibly empty.

    `recent_reports` is a callable returning this engine's recent live reports (or raising ProtocolError). The caller
    has already found the report would carry no proposal.
    """
    out = {'proposals': [], 'activity': []}
    urgency = own_urgency(body, root)
    if urgency not in (4, 5) or held or mode != 'live':
        return out
    if not served(features):
        out['activity'].append(NOT_SERVED)
        return out
    day = now.astimezone(dt.timezone.utc).date().isoformat()
    if _marker(root).get('last_diverge_day') == day:
        out['activity'].append('divergent-thinker was already asked for recovery plays today; it is asked once a day.')
        return out
    try:
        waiting = open_spark(recent_reports() if recent_reports else None, (body or {}).get('decisions_since'), now)
    except ProtocolError as error:
        out['activity'].append(f'divergent-thinker not consulted: this engine\'s recent reports were unread ({error.code}), '
                               'so a recovery play already waiting on Krish could not be ruled out.')
        return out
    if waiting:
        out['activity'].append(f'divergent-thinker not consulted: its recovery play {waiting} still waits on Krish.')
        return out
    request = {'op': 'diverge', 'problem': problem_text(state, north_star, organic), 'count': 3, 'target': 'strategy',
               'temperament': 'balanced', 'cliches': plan_cliches(root), 'bannedWords': banned_words(growth),
               'namespace': NAMESPACE,
               'context': 'Heartside\'s own number is at U%d. The engine drafts and Krish approves every plan, post, send and spend.' % urgency}
    _mark(root, day)  # counted before the call, so a cut connection never asks twice in a day
    try:
        answer = call(client, request, timeout=DIVERGE_TIMEOUT)
    except ProtocolError as error:
        out['activity'].append(f'divergent-thinker gave no recovery plays this run ({error.code}).')
        return out
    sparks = [s for s in answer.get('sparks') or [] if isinstance(s, dict)]
    run_id = str(answer.get('runId') or 'unknown')
    out['activity'].append(f'At U{urgency} with nothing proposed, asked divergent-thinker for three recovery plays, each '
                           f'different in kind (run {run_id}; its model calls are on Control Center\'s daily cap of one).')
    sparks.sort(key=lambda s: s.get('rank') if isinstance(s.get('rank'), int) else 99)
    chosen = None
    for spark in sparks:
        refused = spark_problems(spark, growth, price_points)
        name = _fit(spark.get('title'), 120)
        if refused:
            out['activity'].append(f'Held divergent-thinker spark {spark.get("rank")} ("{name}"): ' + '; '.join(refused[:3]) + '.')
        elif chosen is None:
            chosen = proposal_for(spark, run_id, urgency, now)
            out['proposals'].append(chosen)
            out['activity'].append(f'Proposed divergent-thinker recovery play {chosen["proposal_id"]} ("{name}") behind strategy.')
        else:
            out['activity'].append(f'Kept divergent-thinker spark {spark.get("rank")} ("{name}") in reserve: one ask at a time.')
    if not sparks:
        out['activity'].append(f'divergent-thinker returned no sparks (run {run_id}).')
    elif chosen is None:
        out['activity'].append('No divergent-thinker spark passed this engine\'s checks, so none is proposed.')
    return out


# ---------------------------------------------------------------------------
# At will: `growth.py divergent <op>`, for any session in this repository.
# ---------------------------------------------------------------------------
OPS = ('map', 'provoke', 'challenge', 'diverge', 'score', 'record')
GENERATING = ('map', 'provoke', 'challenge', 'diverge')  # model calls: refused while Krish holds the engine
OP_TIMEOUTS = {'diverge': DIVERGE_TIMEOUT, 'provoke': 120, 'challenge': 120, 'map': 90}
LANE = re.compile(r'^[a-z0-9][a-z0-9-]{0,39}$')  # Control Center's namespace rule: lowercase letters, digits and hyphens


class Refused(Exception):
    """An at-will call that does not go out: the one-line reason goes to stderr and the command exits 2."""


def read_list(path):
    """A JSON list of strings, or one item per non-blank line."""
    text = Path(path).read_text(encoding='utf-8')
    try:
        value = json.loads(text)
    except ValueError:
        value = None
    if isinstance(value, list):
        return [' '.join(str(v).split()) for v in value if str(v).strip()]
    if value is not None:
        raise Refused(f'{path} is JSON but not a list')
    return [' '.join(line.split()) for line in text.splitlines() if line.strip()]


def namespace_for(lane):
    if lane is None:
        return NAMESPACE
    if not LANE.match(lane):
        raise Refused('--lane takes lowercase letters, digits, - and _ (up to 40)')
    return f'{NAMESPACE}:{lane}'


def at_will_body(op, args, growth, today=None):
    """The request body for one at-will op, from the parsed command line. Raises Refused on a usage problem."""
    if op not in OPS:
        raise Refused(f'unknown op {op}')
    get = lambda name: getattr(args, name, None)  # noqa: E731
    problem = ' '.join(str(get('problem') or '').split())
    if op != 'record' and not problem:
        raise Refused(f'{op} needs --problem')
    body = {'op': op, 'namespace': namespace_for(get('lane'))}
    if op != 'record':
        body['problem'] = problem
    if op in ('map', 'provoke', 'challenge', 'diverge') and get('context'):
        body['context'] = get('context')
    if op == 'challenge':
        idea = ' '.join(str(get('idea') or '').split())
        if not idea:
            raise Refused('challenge needs --idea')
        body['idea'] = idea[:IDEA_CHARS]
    if op in ('provoke', 'diverge'):
        if get('count') is not None:
            body['count'] = int(get('count'))
        if get('cliche'):
            body['cliches'] = _strings(get('cliche'), OBVIOUS_MAX, OBVIOUS_CHARS)
        for name in ('target', 'temperament'):
            if get(name):
                body[name] = get(name)
    if op in ('score', 'provoke', 'diverge'):
        body['bannedWords'] = banned_words(growth)
    if op == 'score':
        if not get('ideas_file'):
            raise Refused('score needs --ideas-file')
        ideas = [i[:IDEA_CHARS] for i in read_list(get('ideas_file'))]
        if not ideas or len(ideas) > IDEAS_MAX:
            raise Refused(f'score takes 1 to {IDEAS_MAX} ideas; {get("ideas_file")} has {len(ideas)}')
        body['ideas'] = ideas
        if get('obvious_file'):
            body['obvious'] = _strings(read_list(get('obvious_file')), OBVIOUS_MAX, OBVIOUS_CHARS)
        if get('judge'):
            body['judge'] = True
    if op == 'record':
        if not get('items_file'):
            raise Refused('record needs --items-file')
        items = _strings(read_list(get('items_file')), RECORD_MAX, IDEA_CHARS)
        if not items:
            raise Refused(f'{get("items_file")} has no items')
        body['items'] = items
        body['label'] = f'at will {(today or dt.date.today()).isoformat()}'
    return body


def is_held(client):
    """True when today's directive says Krish holds this engine. Raises Refused when it cannot be read."""
    from . import engine_state
    try:
        directive = client.directive()
    except ProtocolError as error:
        raise Refused(f'divergent-thinker not consulted: the directive was unread ({error.code}), so a hold could not '
                      'be ruled out.') from None
    return engine_state.held((directive or {}).get('directive') or {})


def consult(op, args, growth, client=None, env=None, out=None, err=None, root=None, today=None):
    """Run one at-will op. Prints Control Center's JSON to `out` and returns the exit code: 0 ok, 1 when score flags
    any idea (status not accepted), 2 when not served, held, unreachable, capped, uncalibrated or misused (the reason
    on `err`). Never retries, never writes to Krish's list."""
    import sys
    out, err = out or sys.stdout, err or sys.stderr
    try:
        body = at_will_body(op, args, growth, today)
        if client is None:
            client, note = served_client(env)
            if client is None:
                raise Refused(note)
        else:
            try:
                features = client.capabilities()
            except ProtocolError as error:
                raise Refused(f'divergent-thinker not consulted: Control Center capabilities unread ({error.code}).') from None
            if not served(features):
                raise Refused(NOT_SERVED)
        if op in GENERATING and is_held(client):
            raise Refused(f'Krish holds this engine, so only score and record run; {op} was not asked.')
        if op == 'diverge' and root is not None:
            _mark(root, (today or dt.datetime.now(dt.timezone.utc).date()).isoformat())  # the daily report then skips it
        try:
            answer = call(client, body, timeout=OP_TIMEOUTS.get(op, SCORE_TIMEOUT))
        except ProtocolError as error:
            raise Refused(f'divergent-thinker refused or was unreachable ({error.code}'
                          + (f', HTTP {error.status}' if error.status else '') + ').') from None
    except (Refused, OSError, ValueError) as error:
        print(str(error), file=err)
        return 2
    print(json.dumps(answer, indent=2, ensure_ascii=False), file=out)
    if op == 'score':
        results = answer.get('results') if isinstance(answer, dict) else None
        if not isinstance(results, list) or any(not isinstance(r, dict) or r.get('status') != 'accepted' for r in results):
            return 1
    return 0
