"""Generated dog stills: the floor's still checks, applied to a rolled prompt and its record.

Krish, 10 Nov 2026: "The dogs in all these videos look way too perfect and not real, and slightly scruffy
enough." (floor real-scruffy-dogs). A generated dog still starts as a roll from factory/dog_roll.py, sent to
the generator untouched, and this module holds it to the floor at two points:

- prompt: before any credit is reserved. What code can read in the prompt itself (the realism block and the
  avoid list, no product drawn, no words in the frame, no human expression, arms or hind-leg choreography on
  the dog, no chestnut or red dachshund) and a tier 2 script score of 9 recorded first (spend-means-nine).
- review: before the still reaches Krish's review board. All of the above, plus the generated file bound by
  its SHA-256 to a completed reservation of this exact prompt, a reviewer who is not the maker, a verdict on
  every still entry of the floor whose check is a review, and a finished score of 9 with its reason.

A failure names the floor entry and Krish's own words, so the reason a still is held is his, never ours.
The checks read factory/floor.json live: an entry Krish adds for stills is owed a verdict at once.
"""
import hashlib
import json
from pathlib import Path
import re

from . import floor as floor_mod, ledger

ROLLER = 'factory/dog_roll.py'
FORMAT = 'still'
STAGES = ('prompt', 'review')
VERDICTS = ('pass', 'hold', 'n/a')
SECTIONS = ('iPhone', 'The dog:', 'Coat:', 'Also in shot:', 'The light:', 'What the phone does to the picture:', 'a real pet')
STANDING = 'lock.py STANDING'
STANDING_TEXT = ('no chestnut or red dachshund in a generated frame (it can read as Buddy, and no Buddy image is '
                 'approved)')

# What a prompt may never ask for, by the floor entry that forbids it. Read after the avoid list and every
# negated clause ("no readable labels", "not a show dog") are taken out, so a prohibition never trips its own ban.
BANS = {
    'real-product': [(r'\b(?:mugs?|blankets?|sherpa|portraits?|paintings?|canvas(?:es)?|framed|picture frames?|cards?|'
                      r'ornaments?|posters?|heartside)\b',
                      'the prompt draws a product, or something that could pass for one ({m}); the product is only '
                      'ever the store\'s own render, composited afterwards')],
    'no-badges': [(r'\b(?:badges?|watermarks?|logos?|slogans?|captions?|subtitles?|lettering|labels?|text|signs?|'
                   r'written|writing|words?)\b',
                   'the prompt asks for words or a mark in the frame ({m}); on-screen words are set in post'),
                  (r'"', 'the prompt quotes words, which a generator draws as text')],
    'troll-not-mild': [(r'\b(?:smil\w*|grin|grins|grinning|grinned|smirk\w*|side-?eye\w*|wink\w*|laugh\w*|frown\w*|'
                        r'pout\w*|raised eyebrows?|eyebrows? raised)\b',
                        'the prompt asks for a human facial expression on the dog ({m})')],
    'dog-does-dog-things': [(r"\b(?:human|person'?s?|owner'?s|someone'?s|people'?s|its|his|her|their|the dog'?s)\s+"
                             r"(?:arms?|hands?|fingers?)\b",
                             'the prompt puts human arms or hands on the dog ({m})')],
    'one-trend-one-scene': [(r'\b(?:on (?:its|his|her|their|two) (?:hind|back) legs|on two legs|hind-legs?|bipedal|'
                             r'standing upright|walking upright|choreograph\w*|dance moves?|dancing)\b',
                             'the prompt asks for the dog upright or doing human choreography ({m})')],
    'real-scruffy-dogs': [(r'\b(?:groomed|glossy|show[- ]dog|studio|ring light|bokeh|cinematic|DSLR|professional photo\w*|'
                           r'immaculate|pristine|flawless|perfect fur|catalogue|catalog|stock photo)\b',
                           'the prompt asks for the polished look ({m})')],
}
NEGATED = re.compile(r"\b(?:not|no|never|without|don't|do not)\b[^,.;:]*", re.I)
DACHSHUND = re.compile(r'\b(?:dachshunds?|doxies?|doxie|dachsies?|wiener dogs?|weiner dogs?|sausage dogs?)\b', re.I)
RED = re.compile(r'\b(?:chestnut|red|reddish|ginger|fox-red|copper|auburn|cinnamon|mahogany|rust|rusty)\b', re.I)
BUDDY = re.compile(r'\bbuddy\b', re.I)
AI_LABEL = re.compile(r'\b(?:AI[- ]?(?:generated)?\s+(?:label|tag|disclosure|info)|made with AI|AI info)\b', re.I)
TURN_ON = re.compile(r'\b(?:turn(?:ed|s)? on|switch(?:ed|es)? on|enable[ds]?|set|add(?:ed|s)?|apply|tick(?:ed)?|'
                     r'toggle[ds]?|mark(?:ed)?)\b', re.I)
NEGATION = re.compile(r"\b(?:not|never|don't|do not|no|off|without|leave)\b", re.I)


class Held(ValueError):
    """The floor held the still. `failures` are the checks it failed, each naming its floor entry."""

    def __init__(self, failures):
        self.failures = failures
        super().__init__('; '.join(lines(failures)))


def load_floor(root):
    return json.loads((Path(root) / 'factory/floor.json').read_text(encoding='utf-8'))


def load_pools(root):
    return json.loads((Path(root) / 'factory/bank/dog_pools.json').read_text(encoding='utf-8'))


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def split(prompt):
    """The prompt's positive part and its avoid list (its last paragraph, items separated by '; ')."""
    paragraphs = prompt.strip().split('\n\n')
    if not paragraphs or not paragraphs[-1].startswith('Avoid: '):
        return prompt, []
    items = paragraphs[-1][len('Avoid: '):].rstrip('.').split('; ')
    return '\n\n'.join(paragraphs[:-1]), [i.strip() for i in items if i.strip()]


def affirmative(text):
    """The text with every negated clause taken out: what the prompt actually asks the generator for."""
    return NEGATED.sub(' ', text)


def entries(floor_data):
    return {e['id']: e for e in floor_data['entries']}


def words(entry):
    if entry is None:
        return '(no floor entry)'
    return ' / '.join(f'"{w}"' for w in entry['words']) or entry.get('said') or '(held by the engine itself)'


def coverage(floor_data, pools):
    """Every floor id this module and the pools' avoid list key a check to. Each must exist in the floor."""
    keyed = set(BANS) | {'real-scruffy-dogs', 'real-dogs', 'spend-means-nine', 'ten-out-of-ten', 'no-ai-label'}
    keyed |= {a['floor'] for a in pools['avoid_base'] if a['floor']}
    missing = sorted(keyed - set(entries(floor_data)))
    if missing:
        raise ValueError(f'the still check names floor entries that are not in factory/floor.json: {", ".join(missing)}')
    return keyed


def owed(floor_data):
    """The floor's still entries whose check is a review: each needs a recorded verdict before the board."""
    return [e for e in floor_data['entries'] if FORMAT in e['applies_to'] and 'review:' in e['check']]


def _strings(value, skip=('prompt',)):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            if k not in skip:
                yield from _strings(v, ())
    elif isinstance(value, list):
        for v in value:
            yield from _strings(v, ())


def _score(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def content(record, floor_data, pools):
    """What the floor can read in the rolled prompt itself. [(floor id, reason)]."""
    coverage(floor_data, pools)
    out = []
    prompt = record.get('prompt')
    if not isinstance(prompt, str) or not prompt.strip():
        return [('real-scruffy-dogs', 'the record carries no prompt')]
    positive, avoid = split(prompt)
    said = affirmative(positive)
    if record.get('roller') != ROLLER:
        out.append(('real-scruffy-dogs', f'the prompt did not come from {ROLLER}; roll it, never hand-write one'))
    if record.get('prompt_sha256') != sha256_text(prompt):
        out.append(('real-scruffy-dogs', 'the prompt is not the one the roller returned (its SHA-256 differs); '
                                         'use a rolled prompt exactly, or roll again'))
    if record.get('avoid') != avoid:
        out.append(('real-scruffy-dogs', 'the avoid list in the record differs from the one in the prompt'))
    for marker in SECTIONS:
        if marker not in positive:
            out.append(('real-scruffy-dogs', f'the prompt has lost its realism block ("{marker}" is missing)'))
    a = record.get('attributes') or {}
    if not a.get('conditions'):
        out.append(('real-scruffy-dogs', 'the dog has no real coat flaw rolled (scruffy, shedding, a bed-head tuft)'))
    if len(a.get('details') or []) < 3:
        out.append(('real-scruffy-dogs', 'fewer than three pieces of ordinary household clutter in the frame'))
    if not 3 <= len(a.get('artifacts') or []) <= 5:
        out.append(('real-scruffy-dogs', 'the prompt needs 3 to 5 phone processing artifacts'))
    for item in pools['avoid_base']:
        if item['floor'] and item['text'] not in avoid:
            out.append((item['floor'], f'the avoid list is missing "{item["text"]}"'))
    for fid, bans in BANS.items():
        for pattern, reason in bans:
            m = re.search(pattern, said, re.I)
            if m:
                out.append((fid, reason.format(m=m.group(0))))
    for sentence in re.split(r'[.\n]', positive):
        if DACHSHUND.search(sentence) and RED.search(affirmative(sentence)):
            out.append((STANDING, f'{STANDING_TEXT}: "{sentence.strip()}"'))
    if a.get('breed') == 'dachshund' and RED.search(str(a.get('color', ''))):
        out.append((STANDING, f'{STANDING_TEXT}: the rolled coat is {a["color"]}'))
    if BUDDY.search(positive):
        out.append((STANDING, 'Buddy is never drawn: no Buddy image is approved (AGENTS.md rule 4)'))
    for text in _strings(record):
        for sentence in re.split(r'[.\n;]', text):
            if AI_LABEL.search(sentence) and TURN_ON.search(sentence) and not NEGATION.search(sentence):
                out.append(('no-ai-label', f'the record asks for the platforms\' AI label: "{sentence.strip()}"'))
    return out


def request_brief(record):
    """The provider brief a dog still is reserved under: the roll and its exact prompt, nothing else."""
    return (f'Heartside dog still {record["roll_id"]} (prompt sha256 {record["prompt_sha256"]}), '
            f'generated from this prompt exactly as rolled by {ROLLER}:\n\n{record["prompt"]}')


def fingerprint(record):
    """The provider ledger's fingerprint for this record's reservation (engine/providers.py, reserve)."""
    r = record.get('reservation') or {}
    return ledger.digest({'provider': r.get('provider'), 'capability': r.get('capability'),
                          'brief': request_brief(record), 'source_sha': r.get('source_sha')})


def check(record, stage, floor_data, pools, request_row=None, root=None):
    """Every failure for one still at one stage, as [{'id', 'words', 'reason'}]. Empty means it passes."""
    if stage not in STAGES:
        raise ValueError(f'stage must be one of {", ".join(STAGES)}')
    found = content(record, floor_data, pools)
    score = _score(record.get('script_score'))
    if score is None or score < 9:
        found.append(('spend-means-nine', f'no tier 2 script score of 9 recorded before the spend '
                                          f'(found {record.get("script_score")!r})'))
    if stage == 'review':
        found += _review(record, floor_data, request_row, root)
    known = entries(floor_data)
    out = []
    for fid, reason in found:
        if fid == 'record':
            out.append({'id': 'record', 'words': None, 'reason': reason})
        elif fid == STANDING:
            out.append({'id': STANDING, 'words': None, 'reason': reason})
        else:
            out.append({'id': fid, 'words': words(known.get(fid)), 'reason': reason})
    return out


def _review(record, floor_data, request_row, root):
    out = []
    image = record.get('image') or {}
    if not image.get('path') or not image.get('sha256'):
        out.append(('record', 'no generated image is bound to this roll (growth.py still review ROLL REVIEW.json)'))
    elif root is not None:
        path = Path(root) / image['path'] if not Path(image['path']).is_absolute() else Path(image['path'])
        if not path.is_file():
            out.append(('record', f'the generated image is not on this machine: {image["path"]}'))
        elif hashlib.sha256(path.read_bytes()).hexdigest() != image['sha256']:
            out.append(('record', 'the generated image has changed since it was reviewed (SHA-256 differs)'))
    res = record.get('reservation') or {}
    if not res.get('request_id'):
        out.append(('record', 'no credit reservation for this roll: reserve it first (growth.py still reserve)'))
    elif request_row is None:
        out.append(('record', f'reservation {res["request_id"]} is not in this machine\'s provider ledger'))
    else:
        if request_row.get('status') != 'completed':
            out.append(('record', f'reservation {res["request_id"]} is {request_row.get("status")}, not completed '
                                  '(growth.py provider transition, with the receipt)'))
        if request_row.get('fingerprint') != fingerprint(record):
            out.append(('real-scruffy-dogs', 'the credits were reserved for a different prompt than this record carries'))
    review = record.get('review') or {}
    by, maker = str(review.get('by') or '').strip(), str(record.get('made_by') or '').strip()
    if not by:
        out.append(('record', 'the review names no reviewer'))
    elif maker and by.lower() == maker.lower():
        out.append(('record', 'the reviewer is the maker; an independent judge reviews every still'))
    verdicts = review.get('verdicts') or {}
    for e in owed(floor_data):
        v = verdicts.get(e['id'])
        if not isinstance(v, dict) or v.get('verdict') not in VERDICTS:
            out.append((e['id'], f'no review verdict recorded ({e["check"]})'))
        elif v['verdict'] == 'hold':
            out.append((e['id'], f'held by the reviewer: {v.get("note") or "no note"}'))
        elif v['verdict'] == 'n/a' and not str(v.get('note') or '').strip():
            out.append((e['id'], 'marked n/a with no note saying why it does not apply'))
    final = _score(review.get('score'))
    if final is None or final < 9:
        out.append(('spend-means-nine', f'the finished still scored {review.get("score")!r} at tier 2; only a 9 '
                                        'goes to Krish'))
    if final is None or not str(review.get('reason') or '').strip():
        out.append(('ten-out-of-ten', 'the review carries no score and reason'))
    return out


def lines(failures):
    out = []
    for f in failures:
        if f['words'] is None:
            out.append(f'{f["id"]}: {f["reason"]}')
        else:
            out.append(f'{f["id"]} ({f["words"]}): {f["reason"]}')
    return out


def template(floor_data):
    """A review file to fill in: every verdict the floor is owed for a still, with the check it answers."""
    return {'image': 'local/... the generated file, exactly as downloaded',
            'by': 'the reviewer (never the maker)',
            'verdicts': {e['id']: {'verdict': 'pass | hold | n/a', 'note': '', 'check': e['check']} for e in owed(floor_data)},
            'score': None, 'reason': ''}


def reserve(db, record, source_sha, request, credit_allowance, floor_data, pools):
    """Check the roll at the prompt stage, then reserve its credits through the provider ledger.

    `request` holds the quote: provider, credits, quote_source, quote_observed_at, allocation. The brief is this
    roll's exact prompt, so the reservation's fingerprint binds the credits to it. Nothing is generated here.
    """
    from . import providers
    failures = check(record, 'prompt', floor_data, pools)
    if failures:
        raise Held(failures)
    reservation = {'provider': request['provider'], 'capability': 'image', 'source_sha': source_sha}
    staged = dict(record, reservation=reservation)
    row = providers.reserve(db, {
        'provider': request['provider'], 'capability': 'image', 'brief': request_brief(staged), 'source_sha': source_sha,
        'maximum_usd': '0', 'quote_source': request['quote_source'], 'quote_observed_at': request['quote_observed_at'],
        'prepaid_credits': str(request['credits']), 'allocation': request['allocation']}, credit_allowance=credit_allowance)
    reservation['request_id'] = row['request_id']
    staged['stage'] = 'reserved'
    return staged, row


def attach(record, review, root):
    """Bind the generated file and the independent review to the roll. The file is hashed as it is now."""
    if not isinstance(review, dict) or set(review) - {'image', 'by', 'verdicts', 'score', 'reason'}:
        raise ValueError('a review file holds image, by, verdicts, score and reason only')
    path = Path(review.get('image') or '')
    full = path if path.is_absolute() else Path(root) / path
    if not full.is_file():
        raise ValueError(f'the generated image is not here: {path}')
    try:
        shown = str(full.resolve().relative_to(Path(root).resolve()))
    except ValueError:
        shown = str(full)
    out = dict(record)
    out['image'] = {'path': shown, 'sha256': hashlib.sha256(full.read_bytes()).hexdigest()}
    out['review'] = {k: review.get(k) for k in ('by', 'verdicts', 'score', 'reason')}
    out['stage'] = 'reviewed'
    return out
