"""The joke lab: many jokes per slot, screened before a single frame is made, and Krish's verdicts as the teacher.

Krish, 2026-11-17, after a day of one inherited idea polished across seven cuts: "No, it's not funny - the post
that is already live on this topic is 10x better", "that prior video worked because it was a parody of shameless
LinkedIn influencers, but real dog behavior", and "are you actually enhancing the fucking brain of this fucking
repository where we fucking produce the fucking videos?" This file is that brain for the joke itself.

Where the funny was lost on 17 Nov (session read end to end): at the idea (a retread of the live F38), at the
script (one draft, never challenged), at judging (session notes talked the judge to 9) and at iteration (seven cuts
changed pictures, never the words). Each command below closes one of those:

    python3 factory/jokelab.py brief  TOPIC [--n 30] [--slot ID]   the generator sub-agent's brief: write wide, many families
    python3 factory/jokelab.py screen CANDIDATES.json [--live]     gates before any build: copy rules, retread of a live post,
                                                                     the three-part core, real dog behavior; --live adds the
                                                                     humour engine's reading through Control Center
    python3 factory/jokelab.py show   RUN                           the ranked shortlist and every rejection with its reason
    python3 factory/jokelab.py cut    RUN CAND --score N --words FILE   log a build cut; warns when the score moves but the joke does not
    python3 factory/jokelab.py verdict RUN CAND yes|no "his words"  Krish's verdict, kept where the next brief and ranking read it
    python3 factory/jokelab.py taste                                what his verdicts say so far, by family and by mechanism

The order is fixed: brief, screen, tier 2 judge on the script alone (factory/panel.py) for the shortlist only, Krish,
then the build. No credit is spent on a joke that has not passed its screen and a 9 on the words (floor
spend-means-nine). Runs are kept in local/jokelab/ (rule 9); verdicts are Krish's own words and go to the tracked
factory/bank/verdicts.jsonl from an interactive session only.

The humour engine (krishanraja/humour-engine) understands the joke: its reading, its mechanism, the words that
carry it, the context it needs. It holds no taste. Krish's taste lives in docs/HUMOUR.md, ai-harness krish-voice
references/humour.md and his verdicts here; this file joins them.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUNS = os.environ.get('HEARTSIDE_JOKELAB_DIR', f'{ROOT}/local/jokelab')
VERDICTS = os.environ.get('HEARTSIDE_JOKELAB_VERDICTS', f'{HERE}/bank/verdicts.jsonl')
ANCHORS = f'{HERE}/bank/anchors.json'
FLOOR = f'{HERE}/floor.json'
LOCKS = f'{HERE}/locks'
SPRINTS = f'{HERE}/sprints'

# Families of joke. Breadth is forced across them so one inherited idea can never be the whole slate.
# prior: what this account's own numbers and Krish's verdicts say so far (docs/audits/2026-11-15-interest-vs-paid.md,
# section 3: the alibi family earned 68 to 126 reactions, shares and saves per 1,000 against medians of 29 and 40;
# Krish 17 Nov on F38: parody in the words, real dog behavior on screen). A prior is a starting weight, replaced by
# measured results as verdicts and readings arrive (taste()).
FAMILIES = {
    'alibi': {'prior': 3.0, 'what': 'the evidence first (the crime scene in frame), then the deadpan denial or inflated '
                                    'human explanation ("He has an alibi.", "He would like it noted...")'},
    'format_parody': {'prior': 2.5, 'what': 'the words parody a self-important human format (LinkedIn post, memo, policy, '
                                            'press statement, TED talk) while the dog does an ordinary real dog thing'},
    'rule_lawyer': {'prior': 2.0, 'what': 'the dog has read the rule very carefully and obeys its letter while destroying '
                                          'its spirit'},
    'status_puncture': {'prior': 1.5, 'what': 'the most self-important dog undone by his own behavior, caught on camera'},
    'group_roast': {'prior': 1.5, 'what': 'dog best mates roast one of their own in a group chat that escalates (F34)'},
    'literal_staging': {'prior': 1.0, 'what': 'every word of a line everyone knows staged literally, one beat a second'},
    'escalation_list': {'prior': 1.0, 'what': 'a ranked list or timeline where each item is a bigger offence than the last, '
                                              'each following from the one before'},
}
MIN_FAMILIES = 4
SHORTLIST = 4
RETREAD = 0.42          # char 4-gram similarity to a live post above which a candidate is a retread
DUPLICATE = 0.6         # similarity between two candidates above which the weaker is dropped
REQUIRED = ('id', 'family', 'title', 'observation', 'stupid_premise', 'cruel_payoff', 'dog_does', 'words', 'closest_live_post')

# A dog doing a human act on screen. Krish's 17 Nov rule keeps the parody in the words; literal_staging (the 9 to 5
# lip-sync with hidden human arms, his pick of 10 Nov) is the one family where it is the premise.
HUMAN_ACT = re.compile(r'\b(hoodie|vest|suit|tie|glasses|sunglasses|laptop|typ(?:es|ing)|holds? (?:a|the) (?:phone|mug|coffee|cup)|'
                       r'drinks? coffee|lifts? weights|human arms?|wears?|wearing|dressed)\b', re.I)
TOKEN = re.compile(r"[a-z0-9']+")

# The format a live post owns. Wording can differ completely while the premise is the same (17 Nov: "4:00 a.m. Up before
# the sun." against F38's "Up at 4. Aligned with stakeholders by 5:32"), so a format is matched on its shape.
FORMAT_SIGNATURES = {
    'F38-F40 dog routines': ('a timestamped routine', lambda c: sum(bool(re.match(r'\s*\d{1,2}(:\d{2})?\s*(a\.?m\.?|p\.?m\.?|\.|,)', w, re.I))
                                                                     for w in c.get('words') or []) >= 2
                             or bool(re.search(r"\b(4|four) ?a\.?m\.? routine|morning routine\b", candidate_text(c), re.I))),
    'F34': ('a dogs\' group chat', lambda c: bool(re.search(r'group chat|whatsapp|\bchat\b', candidate_text(c) + ' ' + c.get('dog_does', ''), re.I))
            and c.get('family') != 'group_roast'),
    'yt:u7s47cIeh6M': ('a song staged literally with human arms', lambda c: bool(re.search(r'9 to 5|hidden (person|human)|human arms', c.get('dog_does', ''), re.I))),
}


# ---------------------------------------------------------------- reading the repository's memory

def _load(path, default):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def live_posts():
    """Every post already live or locked, as (id, text), so a candidate can be held against it."""
    out = []
    a = _load(ANCHORS, {})
    for t in a.get('tens', []):
        out.append((t['id'], t.get('what', '')))
    if os.path.isdir(LOCKS):
        lines = {x.get('id'): x.get('text', '') for x in _load(f'{HERE}/bank/lines.json', {}).get('lines', []) if isinstance(x, dict)}
        for name in sorted(os.listdir(LOCKS)):
            if name.endswith('.json'):
                lid = _load(f'{LOCKS}/{name}', {}).get('id', name[:-5])
                out.append((lid, spec_text(_load(f'{HERE}/specs/{lid}.json', {}), lines)))
    if os.path.isdir(SPRINTS):
        for name in sorted(os.listdir(SPRINTS)):
            if name.endswith('.json'):
                for s in _load(f'{SPRINTS}/{name}', {}).get('slots', []):
                    if s.get('stage') in ('filed', 'row_approved', 'live', 'read_72h'):
                        out.append((s['id'], f"{s.get('title', '')}. {s.get('premise', '')} {s.get('payoff', '')} {s.get('filed_caption', '')}"))
    out += [(f'audit:{i}', line) for i, line in enumerate(LIVE_FIRST_LINES)]
    return out


def spec_text(spec, lines):
    """What a locked post actually says and shows: its title and lines from the bank, and each shot's picture."""
    parts = [lines.get(spec.get('title'), '')]
    for row in spec.get('shots', []) + spec.get('messages', []):
        parts.append(lines.get(row.get('line'), ''))
        parts.append(row.get('picture', ''))
    return ' '.join(p for p in parts if p).strip() or spec.get('note', '')


# First lines of live posts read in docs/audits/2026-11-15-interest-vs-paid.md (public brand posts).
LIVE_FIRST_LINES = [
    'First snow of the year. The snowman lasted twenty minutes.',
    'Somebody unrolled the whole roll. He has an alibi.',
    'Effective immediately, the cat runs this department.',
    'The gingerbread house was left unsupervised for one minute.',
    'Clean sheets day. He would like it noted that he was never on the bed.',
    'Up at 4. Aligned with stakeholders by 5:32',
]


def floor_lines():
    d = _load(FLOOR, {'entries': []})
    return [(e['id'], (e.get('words') or [''])[0], e.get('rule', '')) for e in d.get('entries', []) if e.get('words')]


def humour_core():
    h = _load(ANCHORS, {}).get('humour') or {}
    return h.get('core', 'an intelligent observation, an utterly stupid premise, and a slightly cruel payoff'), \
        h.get('traits', []), h.get('limits', [])


# ---------------------------------------------------------------- similarity

def _grams(text, n=4):
    t = ' '.join(TOKEN.findall((text or '').lower()))
    return {t[i:i + n] for i in range(max(0, len(t) - n + 1))}


def similarity(a, b):
    ga, gb = _grams(a), _grams(b)
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / min(len(ga), len(gb))


def candidate_text(c):
    return ' '.join([c.get('title', ''), c.get('stupid_premise', ''), ' '.join(c.get('words') or []), c.get('last_line', '')])


def words_hash(words):
    return hashlib.sha256('\n'.join(words or []).strip().encode()).hexdigest()[:16]


# ---------------------------------------------------------------- the brief

def brief(topic, n=30, slot=None):
    core, traits, limits = humour_core()
    weights = family_weights()
    lines = [
        f"You write jokes for Heartside's social videos and stills. Topic or slot: {topic}" + (f' (slot {slot})' if slot else '') + '.',
        f'Write {n} different candidates, not variations of one. Use at least {MIN_FAMILIES} of the families below, '
        'and give the families with the higher weight more of the slate. Two candidates may not share a premise.',
        '',
        "Krish's formula (17 Nov, his words): the parody is in the words, and the dog does real dog behavior on screen. "
        'No dressed-up dogs, no dogs doing human acts, except in literal_staging. Every dog must be able to be a real, '
        'slightly scruffy pet filmed on a phone.',
        f'The core every candidate needs: {core}. Write each part as one plain sentence; if you cannot, drop the candidate.',
        'Traits: ' + '; '.join(traits) + '.' if traits else '',
        'Limits: ' + '; '.join(limits) + '.' if limits else '',
        'The opening shot decides: average watch is 2 to 5 seconds on every channel (audit 15 Nov). Put the evidence or '
        'the absurd fact in the first second.',
        '',
        'Families (weight from the numbers and Krish\'s verdicts so far):',
    ]
    lines += [f'- {k} (weight {weights[k]:.1f}): {v["what"]}' for k, v in FAMILIES.items()]
    lines += ['', 'Already live or locked. A candidate that repeats one of these is rejected unless it is clearly funnier, '
                  'and you must name the closest one in closest_live_post (Krish, 17 Nov: "the post that is already live '
                  'on this topic is 10x better"):']
    lines += [f'- {i}: {t[:180]}' for i, t in live_posts()]
    lines += ['', "What Krish rejected, in his words. Do not write anything one of these would catch:"]
    lines += [f'- {i}: "{w}" -> {r}' for i, w, r in floor_lines()]
    past = [v for v in read_verdicts() if v.get('verdict') == 'no']
    if past:
        lines += ['', 'Jokes he has already said no to in the joke lab:']
        lines += [f'- [{v.get("family")}] {v.get("title")}: "{v.get("words_said", "")}"' for v in past[-15:]]
    lines += ['', "Heartside's rules still bind (AGENTS.md rule 5): US spelling, no em dashes, no exclamation marks, no swearing, "
                  'no jokes about a dog dying, ageing, illness or abandonment, never mocking the buyer.',
              '', 'Reply as JSON only, a list of objects with exactly these keys:',
              '{"id": "c01", "family": "<one of the families>", "title": "...", "observation": "the true thing about dogs or '
              'people this rests on", "stupid_premise": "...", "cruel_payoff": "...", "dog_does": "the real dog behavior on '
              'screen, shot by shot", "words": ["on-screen line 1", "line 2", "..."], "last_line": "the payoff line", '
              '"closest_live_post": "<id from the list above, or none>", "why_new": "one sentence"}',
              'Name closest_live_post honestly. If it is not none, add "beats_live": why this is clearly funnier than that post, '
              'or the candidate is rejected as a retread.']
    return '\n'.join(x for x in lines if x is not None)


# ---------------------------------------------------------------- screening

def _copy_problems(c):
    sys.path.insert(0, ROOT)
    try:
        import growth  # the one copy check (rule 5); never a second list here
    except Exception as e:  # noqa: BLE001
        return [f'copy check unavailable: {type(e).__name__}']
    text = '\n'.join((c.get('words') or []) + ([c['last_line']] if c.get('last_line') else []))
    return growth.problems({'platform': 'tiktok', 'text': text})


def gates(c, live, kept):
    """Deterministic reasons to reject one candidate, and warnings that only lower its rank."""
    reject, warn = [], []
    missing = [k for k in REQUIRED if not c.get(k)]
    if missing:
        reject.append(f'missing {", ".join(missing)}')
    if c.get('family') not in FAMILIES:
        reject.append(f'family "{c.get("family")}" is not one of {", ".join(FAMILIES)}')
    for part in ('observation', 'stupid_premise', 'cruel_payoff'):
        if c.get(part) and len(TOKEN.findall(c[part])) < 4:
            reject.append(f'{part} is not a real sentence')
    reject += [f'copy: {p}' for p in _copy_problems(c)]
    if c.get('family') != 'literal_staging' and c.get('dog_does') and HUMAN_ACT.search(c['dog_does']):
        reject.append(f'the dog does a human act on screen ("{HUMAN_ACT.search(c["dog_does"]).group(0)}"); '
                      'the parody belongs in the words (Krish, 17 Nov)')
    text = candidate_text(c)
    best = max(((similarity(text, t), i) for i, t in live), default=(0.0, None))
    c['_closest'] = {'id': best[1], 'similarity': round(best[0], 3)}
    retread = []
    if best[0] >= RETREAD:
        retread.append(f'its words are close to live post {best[1]} (similarity {best[0]:.2f})')
    for live_id, (shape, match) in FORMAT_SIGNATURES.items():
        if match(c):
            retread.append(f'it uses {shape}, the format of live post {live_id}')
    declared = (c.get('closest_live_post') or 'none').strip()
    if declared.lower() not in ('none', 'no', 'n/a', ''):
        retread.append(f'its writer named live post {declared} as its closest')
    if retread:
        c['_retread'] = retread
        if not (c.get('beats_live') or '').strip():
            reject.append('retread: ' + '; '.join(retread) + '. A retread reaches Krish only when it is clearly funnier '
                          '(17 Nov). Write a new idea, or give beats_live: why this beats that post')
        else:
            warn.append('retread kept on its beats_live argument; the judge must compare it with the live post')
    for k in kept:
        s = similarity(text, candidate_text(k))
        if s >= DUPLICATE:
            reject.append(f'near duplicate of {k["id"]} ({s:.2f})')
            break
    n = len(c.get('words') or [])
    if n > 6:
        warn.append(f'{n} on-screen lines; the laugh should land by the third (floor funny-bar: a laugh every 3 to 4 s)')
    return reject, warn


PREMISE = {'incongruity', 'absurd_reasoning', 'personification', 'literalisation', 'exaggeration', 'self_defeating_logic',
           'misdirection'}
PAYOFF = {'reversal', 'irony', 'sarcasm', 'understatement', 'self_defeating_logic', 'misdirection', 'callback'}
CRUEL_TARGETS = {'self', 'other_person', 'behaviour', 'institution', 'convention', 'fictional_person'}


def triad(result, words):
    """Read the humour engine's analysis against Krish's three-part core. Returns (ok, notes, labels)."""
    notes, labels = [], {}
    if not result or result.get('comic_reading') is None:
        return None, ['humour engine gave no reading'], labels
    reading = result['comic_reading']
    if reading != 'supported':
        return False, [f'the engine reads it as {reading}: no joke a stranger would get'], labels
    main = [i for i in result.get('interpretations', []) if i.get('supported_reading')]
    if not main:
        return False, ['no grounded comic reading'], labels
    i = next((x for x in main if x.get('is_main')), main[0])
    labels = {k: v for k, v in (i.get('labels_by_axis') or {}).items() if v}
    mech = set(labels.get('mechanism', []))
    modes = set(labels.get('rhetorical_mode', []))
    ok = True
    if not (i.get('expectations') or i.get('connecting_logic')):
        ok = False; notes.append('no observation: the engine found no expectation the joke plays against')
    if not (mech & PREMISE or modes & {'absurdism', 'parody', 'satire'}):
        ok = False; notes.append(f'no stupid premise in the mechanisms it found ({", ".join(sorted(mech)) or "none"})')
    target = (i.get('target_and_subject') or {}).get('target')
    if not (mech & PAYOFF or target in CRUEL_TARGETS):
        ok = False; notes.append('no payoff with an edge: nothing reverses, and nothing is the target')
    ev = {e['evidence_id']: e for e in result.get('evidence', [])}
    last_seg = f'w{len(words)}'
    if words and not any(ev.get(r, {}).get('segment_id') == last_seg for r in i.get('evidence_refs', [])):
        notes.append('the payoff evidence is not in the last line: the joke may be spent early (floor: the back half went soft)')
    jumps = [d for d in result.get('context_dependencies', []) if d.get('required') and d.get('source_kind') in ('cultural', 'topical')]
    if len(jumps) > 1 or result.get('missing_context'):
        ok = False; notes.append('needs more than one outside reference to land (HUMOUR.md limit: no jump the viewer cannot follow in the first second)')
    return ok, notes, labels


def engine_request(c):
    words = c.get('words') or []
    segs = [{'segment_id': f'w{n}', 'text': w, 'sequence': n} for n, w in enumerate(words, 1)]
    return {
        'request_id': f'jokelab:{c["id"]}',
        'focus_segment_ids': [s['segment_id'] for s in segs],
        'segments': segs,
        'context': {'provided_facts': [f'On screen, a real dog: {c.get("dog_does", "")}', 'Format: a short vertical social video, words on screen'],
                    'audience_description': 'US dog owners on TikTok and Instagram'},
        'tasks': ['comprehension'],
        'provider_policy': {'allowed_provider_ids': ['controlcenter'], 'allow_external_inference': True},
        'budget': {'max_model_calls': 1, 'max_input_tokens': 9000, 'max_output_tokens': 2000},
    }


def engine_reader(transport=None):
    """The humour engine through Control Center's humour route, on this engine's own bearer. None when unavailable."""
    token = os.environ.get('CONTROL_CENTER_ENGINE_TOKEN') or os.environ.get('HUMOUR_ENGINE_CC_BEARER')
    if not token:
        return None
    os.environ.setdefault('HUMOUR_ENGINE_CC_BEARER', token)
    os.environ.setdefault('HUMOUR_ENGINE_CC_ENGINE', 'heartside')
    if os.environ.get('CONTROL_CENTER_URL'):
        os.environ.setdefault('HUMOUR_ENGINE_CC_URL', os.environ['CONTROL_CENTER_URL'])
    try:
        from humour_engine.analysis.core import EngineDeps, analyse
        from humour_engine.contracts.analysis import AnalysisRequest
        from humour_engine.models.providers import ControlCenterProvider
    except ImportError:
        return None
    deps = EngineDeps(providers={'controlcenter': ControlCenterProvider(transport=transport)}, max_calls_per_request=1)

    def read(c):
        res = analyse(AnalysisRequest.model_validate(engine_request(c)), deps)
        return json.loads(res.model_dump_json())
    return read


def screen(candidates, reader=None, now=None):
    """Gate, read and rank. Returns the run record (never writes)."""
    live = live_posts()
    weights = family_weights()
    fit = taste_fit()
    kept, rejected = [], []
    for c in candidates:
        reject, warn = gates(c, live, kept)
        if reject:
            rejected.append({'id': c.get('id'), 'title': c.get('title'), 'family': c.get('family'), 'reasons': reject})
            continue
        c['_warnings'] = warn
        kept.append(c)
    for c in kept:
        c['_engine'] = None
        if reader:
            try:
                res = reader(c)
            except Exception as e:  # noqa: BLE001 - recorded, never fatal
                res = {'status': 'failed', 'errors': [{'code': type(e).__name__}]}
            ok, notes, labels = triad(res, c.get('words') or [])
            c['_engine'] = {'ok': ok, 'notes': notes, 'labels': labels, 'mode': res.get('analysis_mode'),
                            'status': res.get('status'), 'analysis_id': res.get('analysis_id')}
            if ok is False:
                rejected.append({'id': c['id'], 'title': c.get('title'), 'family': c.get('family'), 'reasons': [f'engine: {n}' for n in notes]})
    survivors = [c for c in kept if not (c['_engine'] and c['_engine']['ok'] is False)]
    for c in survivors:
        s = weights.get(c['family'], 1.0)
        s += 2.0 * (1 - c['_closest']['similarity'])
        s += fit.get(c['family'], 0.0)
        if c['_engine'] and c['_engine']['ok']:
            s += 1.0
            for m in c['_engine']['labels'].get('mechanism', []):
                s += fit.get(f'mechanism:{m}', 0.0)
        s -= 0.5 * len(c.get('_warnings', []))
        c['_score'] = round(s, 3)
    survivors.sort(key=lambda c: -c['_score'])
    fams = Counter(c.get('family') for c in candidates if c.get('family') in FAMILIES)
    problems = []
    if len(candidates) < 12:
        problems.append(f'only {len(candidates)} candidates; write wide (the brief asks for 30)')
    if len(fams) < MIN_FAMILIES:
        problems.append(f'only {len(fams)} families ({", ".join(fams)}); one idea polished is how 17 Nov was lost')
    return {
        'at': (now or dt.datetime.now(dt.timezone.utc)).isoformat(timespec='seconds'),
        'engine': 'read' if reader else 'not read (no Control Center token or humour-engine not installed)',
        'counts': {'candidates': len(candidates), 'rejected': len(rejected), 'shortlist': min(SHORTLIST, len(survivors))},
        'slate_problems': problems,
        'shortlist': [_public(c) for c in survivors[:SHORTLIST]],
        'reserve': [_public(c) for c in survivors[SHORTLIST:]],
        'rejected': rejected,
    }


def _public(c):
    out = {k: v for k, v in c.items() if not k.startswith('_')}
    out.update({'score': c.get('_score'), 'closest_live': c.get('_closest'), 'warnings': c.get('_warnings', []),
                'engine': c.get('_engine'), 'words_sha': words_hash(c.get('words'))})
    return out


# ---------------------------------------------------------------- cuts: catch polishing pictures

def cut_warning(cuts):
    """cuts: [{'cut', 'score', 'words_sha'}] in order. The 17 Nov loop: seven cuts, the words never changed, and a
    model's score climbed from 7 to 9 on pictures alone. Returns a warning string or None."""
    if len(cuts) < 2:
        return None
    same = [c for c in cuts if c['words_sha'] == cuts[0]['words_sha']]
    if len(same) == len(cuts) and len(cuts) >= 3:
        return (f'{len(cuts)} cuts with the same words. The joke has not changed; only pictures have. Go back to the '
                'shortlist or write new words before another cut (17 Nov: seven cuts, still not funny).')
    first, last = cuts[0], cuts[-1]
    if last['words_sha'] == first['words_sha'] and (last['score'] or 0) > (first['score'] or 0):
        return ('the score rose with the same words: a picture moved a model, not the joke. Re-judge the script alone '
                '(panel.py brief tier2 on the words) before this reaches Krish.')
    return None


# ---------------------------------------------------------------- verdicts and taste

def read_verdicts(path=None):
    path = path or VERDICTS
    out = []
    if os.path.exists(path):
        for line in open(path, encoding='utf-8'):
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    return out


def family_weights(verdicts=None):
    """Priors moved by Krish's verdicts: each yes adds, each no takes away, never below 0.2."""
    w = {k: v['prior'] for k, v in FAMILIES.items()}
    for v in verdicts if verdicts is not None else read_verdicts():
        f = v.get('family')
        if f in w:
            w[f] = max(0.2, w[f] + (0.5 if v.get('verdict') == 'yes' else -0.5))
    return w


def taste_fit(verdicts=None):
    """Signed preference by family and by engine mechanism from his verdicts, needing two agreeing verdicts before it
    counts (one rejection is never a rule; HUMOUR.md and the humour engine's profile rules)."""
    tally = defaultdict(lambda: [0, 0])
    for v in verdicts if verdicts is not None else read_verdicts():
        keys = [v.get('family')] + [f'mechanism:{m}' for m in (v.get('labels') or {}).get('mechanism', [])]
        for k in keys:
            if k:
                tally[k][0 if v.get('verdict') == 'yes' else 1] += 1
    fit = {}
    for k, (yes, no) in tally.items():
        if yes + no >= 2 and abs(yes - no) >= 2:
            fit[k] = 0.75 * (1 if yes > no else -1)
    return fit


def taste():
    vs = read_verdicts()
    if not vs:
        return 'No joke-lab verdicts yet. The first ones come from Krish on the review board.'
    by = defaultdict(Counter)
    for v in vs:
        by[v.get('family')][v.get('verdict')] += 1
    lines = [f'{len(vs)} verdicts.']
    lines += [f'- {f}: {c["yes"]} yes, {c["no"]} no' for f, c in sorted(by.items(), key=lambda x: str(x[0]))]
    fit = taste_fit(vs)
    if fit:
        lines.append('Rules the ranking now uses (two or more agreeing verdicts): ' +
                     ', '.join(f'{k} {"+" if s > 0 else "-"}' for k, s in sorted(fit.items())))
    return '\n'.join(lines)


# ---------------------------------------------------------------- run files

def run_path(run):
    return f'{RUNS}/{run}.json'


def save_run(run, rec):
    os.makedirs(RUNS, exist_ok=True)
    with open(run_path(run), 'w', encoding='utf-8') as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
    return run_path(run)


def load_run(run):
    rec = _load(run_path(run), None)
    if rec is None:
        raise SystemExit(f'no run {run} in {RUNS}')
    return rec


def find(rec, cand):
    for c in rec.get('shortlist', []) + rec.get('reserve', []):
        if c.get('id') == cand:
            return c
    raise SystemExit(f'{cand} is not on the shortlist or in reserve')


def show(rec):
    out = [f'Run at {rec["at"]}. Engine: {rec["engine"]}.', json.dumps(rec['counts'])]
    out += [f'SLATE: {p}' for p in rec.get('slate_problems', [])]
    out.append('Shortlist (these, and only these, go to the tier 2 judge on the words):')
    for c in rec['shortlist']:
        out.append(f'  {c["id"]} [{c["family"]}] {c["title"]}  score {c["score"]}  closest live {c["closest_live"]}')
        out += [f'      {w}' for w in c.get('words', [])]
        if c.get('engine'):
            out.append(f'      engine: {"core holds" if c["engine"]["ok"] else c["engine"]["notes"]}')
        out += [f'      warn: {w}' for w in c.get('warnings', [])]
    out.append(f'Rejected: {len(rec["rejected"])}')
    out += [f'  {r["id"]} [{r.get("family")}] {r.get("title")}: {"; ".join(r["reasons"])}' for r in rec['rejected']]
    return '\n'.join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('brief'); b.add_argument('topic'); b.add_argument('--n', type=int, default=30); b.add_argument('--slot')
    s = sub.add_parser('screen'); s.add_argument('candidates'); s.add_argument('--live', action='store_true'); s.add_argument('--run')
    sh = sub.add_parser('show'); sh.add_argument('run')
    c = sub.add_parser('cut'); c.add_argument('run'); c.add_argument('cand'); c.add_argument('--score', type=float); c.add_argument('--words', required=True)
    v = sub.add_parser('verdict'); v.add_argument('run'); v.add_argument('cand'); v.add_argument('verdict', choices=['yes', 'no']); v.add_argument('words')
    sub.add_parser('taste')
    a = p.parse_args(argv)

    if a.cmd == 'brief':
        print(brief(a.topic, a.n, a.slot)); return 0
    if a.cmd == 'screen':
        cands = _load(a.candidates, None)
        if not isinstance(cands, list):
            raise SystemExit(f'{a.candidates}: expected a JSON list of candidates')
        reader = engine_reader() if a.live else None
        if a.live and reader is None:
            print('humour engine not available: set CONTROL_CENTER_ENGINE_TOKEN and pip install -r requirements-humour.txt; '
                  'screening with the code gates only', file=sys.stderr)
        rec = screen(cands, reader)
        run = a.run or dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S')
        rec['run'] = run
        print(show(rec)); print(f'\nsaved {save_run(run, rec)}'); return 0
    if a.cmd == 'show':
        print(show(load_run(a.run))); return 0
    if a.cmd == 'cut':
        rec = load_run(a.run); cand = find(rec, a.cand)
        words = [line.strip() for line in open(a.words, encoding='utf-8') if line.strip()]
        cand.setdefault('cuts', []).append({'cut': len(cand.get('cuts', [])) + 1, 'score': a.score, 'words_sha': words_hash(words)})
        save_run(a.run, rec)
        w = cut_warning(cand['cuts'])
        print(f'cut {len(cand["cuts"])} logged.' + (f'\nWARNING: {w}' if w else '')); return 1 if w else 0
    if a.cmd == 'verdict':
        rec = load_run(a.run); cand = find(rec, a.cand)
        entry = {'at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'run': a.run, 'id': a.cand,
                 'title': cand.get('title'), 'family': cand.get('family'), 'words_sha': cand.get('words_sha'),
                 'labels': (cand.get('engine') or {}).get('labels', {}), 'verdict': a.verdict, 'words_said': a.words}
        os.makedirs(os.path.dirname(VERDICTS), exist_ok=True)
        with open(VERDICTS, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        print(f'recorded. A no also goes into factory/floor.json with his words and to his taste ledger '
              f'(report_to_taste_engine), as AGENTS.md says.\n{taste()}'); return 0
    if a.cmd == 'taste':
        print(taste()); return 0
    return 2


if __name__ == '__main__':
    sys.exit(main())
