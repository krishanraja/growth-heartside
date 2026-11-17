#!/usr/bin/env python3
"""Roll a generated dog still's prompt: a real pet on the owner's phone, never the same dog twice.

Krish, 10 Nov 2026: "The dogs in all these videos look way too perfect and not real, and slightly scruffy
enough." (factory/floor.json, real-scruffy-dogs). Asked plainly for a dog, an image model hands back the same
brushed, well-lit pet every time. So nothing about the dog or the photo is left to the model or to the session.
Each of these is drawn here from factory/bank/dog_pools.json with the operating system's randomness:

- the breed or mix, its coat colour and real flaws, its age, build and collar;
- the room or yard, where the owner holds the phone and how far off;
- the clutter around the dog, the light and the colour cast it leaves on the phone;
- 3 to 5 marks of the phone's own processing.

The avoid list closes off the polished look and every floor rule a prompt can break. A short memory under
local/ keeps one batch from reusing the breeds and settings of the last few.

The joke is never rolled: what the dog is doing comes from the approved script (--action, verbatim), which is
judged against docs/HUMOUR.md and scored 9 at tier 2 before any credit is spent. The roller carries the look.

    python3 growth.py floor --format still               read first, every session
    python3 growth.py still roll [--count N] [--breed KEY[,KEY]] [--setting KEY[,KEY]] [--action TEXT]
                                 [--expression TEXT] [--coat COLOUR] [--frame photo|video] [--aspect 3:4]
                                 [--slot S01 [--manifest FILE]] [--json] [--list]
    python3 factory/dog_roll.py ...                      the same, without the engine's entry point

A prompt goes to the generator untouched, with its aspect_ratio. growth.py still check compares it with the
SHA-256 taken when it was rolled, so any edit holds the still: to change something, lock it with a flag and
roll again. Each roll is kept as a record in local/factory/dog-rolls/<roll id>.json, which
`growth.py still reserve`, `review` and `check` carry forward.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from random import SystemRandom
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from engine import stills  # noqa: E402

POOLS = os.path.join(HERE, 'bank', 'dog_pools.json')
ROLLS = os.environ.get('HEARTSIDE_DOG_ROLLS', os.path.join(ROOT, 'local', 'factory', 'dog-rolls'))
HISTORY = os.environ.get('HEARTSIDE_DOG_HISTORY', os.path.join(ROOT, 'local', 'factory', 'dog-roll-history.json'))
SPRINT = os.path.join(HERE, 'sprints', '2026-11-S120.json')
KEEP = {'breeds': 12, 'settings': 6, 'conditions': 10}
MAX_COUNT = 12
COATS = {'short': 'a short coat', 'double': 'a thick double coat', 'long': 'a long coat', 'curly': 'a curly coat',
         'wire': 'a wiry coat', 'silky': 'a silky coat'}
LENS = ("the main lens's plain view, about 24mm equivalent, with no stretched edges; held by hand, not on a "
        'tripod; a small sensor, so nearly everything is in focus and whatever is behind the dog is almost as crisp')
USE = ('Send prompt and aspect_ratio to the generator untouched. Any edit, however small, fails growth.py still '
       'check by its SHA-256: to change something, lock it with a flag and roll again. Reserve the credits first '
       '(growth.py still reserve).')

# ---------------------------------------------------------------------------- drawing

RNG = SystemRandom()  # reads the operating system's entropy, so no two runs follow the same sequence


def one_of(options):
    """One option, every option equally likely."""
    options = tuple(options)
    return options[RNG.randrange(len(options))]


def some_of(options, fewest, most):
    """Between `fewest` and `most` different options (never more than there are), in the order drawn."""
    options = tuple(options)
    return RNG.sample(options, min(len(options), RNG.randint(fewest, most)))


def by_weight(rows):
    """One value from [value, weight] rows, each as likely as its weight."""
    return RNG.choices([value for value, _ in rows], [weight for _, weight in rows])[0]


def unused(keys, taken, recent):
    """The keys neither this batch nor recent batches have used; failing that, the ones this batch has not
    used; failing that, every key."""
    for barred in (set(taken) | set(recent), set(taken)):
        left = [key for key in keys if key not in barred]
        if left:
            return left
    return list(keys)


def in_words(things):
    """'a', 'a and b', or 'a, b, and c'."""
    things = [t for t in things if t]
    if len(things) < 3:
        return ' and '.join(things)
    return f'{", ".join(things[:-1])}, and {things[-1]}'


def upper_first(text):
    return text[:1].upper() + text[1:]


def article(word):
    return 'an' if word[:1].lower() in 'aeiou' else 'a'


# ---------------------------------------------------------------------------- the memory under local/

def load_history(path):
    try:
        with open(path, encoding='utf-8') as fh:
            saved = json.load(fh)
    except (OSError, ValueError):
        saved = {}
    return {k: list(saved.get(k, [])) for k in KEEP}


def save_history(path, memory):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump({k: memory[k][-n:] for k, n in KEEP.items()}, f, indent=1)
    os.replace(tmp, path)


# ---------------------------------------------------------------------------- locks

def load_pools(path=POOLS):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def breed_keys(pools, wanted=None):
    """The breeds a roll may draw: every one not lock_only, or exactly the ones named (by key or alias)."""
    table = {b['key']: b for b in pools['breeds']}
    if not wanted:
        return [k for k, b in table.items() if not b.get('lock_only')]
    out = []
    for name in wanted:
        n = name.strip().lower().replace('-', ' ').replace('_', ' ')   # keys like terrier_mix match as written
        match = next((k for k, b in table.items() if n in (k.replace('_', ' '), b['label'].lower(), *b['aliases'])), None)
        if not match:
            raise ValueError(f'no breed {name!r} in factory/bank/dog_pools.json (keys: {", ".join(table)}); add it there')
        out.append(match)
    return out


def slot_breed(slot_id, manifest=SPRINT):
    """The breed a sprint slot names, held to the sprint's own dachshund rule (factory/sprint.py)."""
    with open(manifest, encoding='utf-8') as fh:
        m = json.load(fh)
    slot = next((s for s in m['slots'] if s.get('id') == slot_id), None)
    if slot is None:
        raise ValueError(f'{slot_id}: no such slot in {os.path.basename(manifest)}')
    if slot.get('breed') == 'dachshund' and not slot.get('breed_ok'):
        raise ValueError(f'{slot_id}: no chestnut or red dachshund in a generated frame (it reads as Buddy); '
                         'pick another breed')
    return slot.get('breed')


# ---------------------------------------------------------------------------- one dog

def extra_avoid(breed_key, breed, color, age, place, video):
    """Avoid items that only some rolls need, by what was drawn."""
    out = []
    if breed_key == 'westie' or 'white' in color or 'cream' in color:
        out.append('fur blown out to featureless white')
    if age.startswith('young, under a year'):
        out.append('a cartoonish, big-eyed puppy look')
    if breed['coat'] == 'curly':
        out.append('a fresh salon cut')
    if place.get('outdoor'):
        out.append('a cinematic sunset glow or an HDR sky')
    if breed_key == 'dachshund':
        out.append('a chestnut, red or ginger coat')
    if video:
        out.append('motion blur smeared across the whole frame')
    return out


def compose(pools, breed_key, setting_key, locks, batch_flaws, recent_flaws):
    """Draw one dog and its photo, and write the prompt that describes them."""
    breed = next(b for b in pools['breeds'] if b['key'] == breed_key)
    place = pools['settings'][setting_key]
    video = locks.get('frame') == 'video'

    color = locks.get('coat') or one_of(breed['colors'])
    age = by_weight(pools['ages'])
    body = one_of(pools['builds'])
    fits = [c['text'] for c in pools['coat_conditions'] if breed['coat'] in c['coats'] or 'any' in c['coats']]
    flaws = []
    for _ in range(RNG.randint(1, 2)):
        flaw = one_of(unused(fits, batch_flaws + flaws, recent_flaws))
        if flaw not in flaws:
            flaws.append(flaw)
    collar = one_of(pools['collars'])
    phone = one_of(pools['iphones'])
    held, distance = one_of(place['placements'])
    framing = one_of(pools['frames'])
    clutter = ([one_of(place['base'])] if place.get('base') else []) + some_of(place['details'], 3, 5)
    behind = one_of(place['beyond'])
    light = one_of(place['light'])
    beat = (locks.get('action') or '').strip().rstrip('.')
    doing = beat or one_of(place['spots'])
    face = (locks.get('expression') or '').strip().rstrip('.') or (None if beat else one_of(pools['expressions']))

    if video:
        opening = (f'A single vertical 9:16 frame taken from a clip the owner shot on {article(phone)} {phone} at 4K '
                f'30fps, standard 1x lens, the phone {held}, {distance} from the dog.')
    else:
        opening = (f'A vertical snapshot on {article(phone)} {phone} in plain Photo mode, standard 1x lens, with no '
                f'background blur, the phone {held}, {distance} from the dog.')
    dog = ' '.join(part for part in (
        f'The dog: {article(color)} {color} {breed["label"]}, {age}, {body}, {place["setting"]}.',
        f'What it is doing: {doing}.',
        f'Its face: {face}, the way a real dog looks.' if face else '',
        f'Coat: {COATS[breed["coat"]]}. Its real flaws: {"; ".join(flaws)}.',
        upper_first(collar) + '.',
        f'Framing: {framing}.',
    ) if part)
    scene = f'Also in shot: {in_words(clutter)}. Behind it: {behind}. The light: {light["look"]}.'

    shrink = 'light HEVC video' if video else 'light HEIC'
    artifacts = [a.replace('{compression}', shrink) for a in some_of(pools['artifacts'], 3, 5)]
    glare = pools['highlights']
    marks = [pools['cast_lines'][light['cast']], *artifacts,
             one_of(glare['bright_source'] if light['bright_source'] else glare['daylight'])]
    if light['cast'] == 'fluorescent' and RNG.randrange(2):
        marks.append(glare['flicker'])
    camera = f'What the phone does to the picture: {LENS}; ' + '; '.join(marks) + '.'
    seen = 'clip the owner shot' if video else 'photo the owner took'
    feel = (f'It has to pass for a real pet in a {seen}, straight off the camera roll with no filter, edit or '
            "retouch: someone's own dog, not a show dog.")

    avoid = [a['text'] for a in pools['avoid_base']] + extra_avoid(breed_key, breed, color, age, place, video)
    prompt = '\n\n'.join((f'{opening} {dog}', scene, camera, feel, 'Avoid: ' + '; '.join(avoid) + '.'))
    sha = stills.sha256_text(prompt)
    roll_id = 'dog-' + hashlib.sha256(f'{sha}:{RNG.getrandbits(64):016x}'.encode()).hexdigest()[:12]
    return {
        'roller': stills.ROLLER, 'roll_id': roll_id,
        'rolled_at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
        'summary': f'{color} {breed["label"]}, {age}, {setting_key.replace("_", " ")}, {light["look"]}',
        'attributes': {'breed': breed_key, 'breed_label': breed['label'], 'color': color, 'coat': breed['coat'],
                       'age': age, 'build': body, 'conditions': flaws, 'collar': collar, 'setting': setting_key,
                       'doing': doing, 'action_from_script': bool(beat), 'expression': face,
                       'placement': held, 'distance': distance, 'framing': framing, 'details': clutter,
                       'beyond': behind, 'light': light['look'], 'cast': light['cast'],
                       'bright_source': light['bright_source'], 'iphone': phone, 'artifacts': artifacts,
                       'frame': 'video' if video else 'photo'},
        'aspect_ratio': locks.get('aspect') or ('9:16' if video else '3:4'),
        'prompt': prompt, 'prompt_sha256': sha, 'avoid': avoid, 'use': USE, 'stage': 'rolled',
    }


# ---------------------------------------------------------------------------- a batch

def roll(count=1, breeds=None, settings=None, action=None, expression=None, coat=None, frame='photo', aspect=None,
         history=HISTORY, out=ROLLS, pools=None, floor_data=None):
    """Roll `count` dogs: no breed or setting repeated in the batch, and none of the recent ones where the pools
    allow. Each roll passes the floor's prompt checks before it is returned; a lock that breaks one is refused."""
    if not 1 <= count <= MAX_COUNT:
        raise ValueError(f'roll 1 to {MAX_COUNT} dogs at a time')
    if frame not in ('photo', 'video'):
        raise ValueError('frame is photo or video')
    pools = pools or load_pools()
    floor_data = floor_data or stills.load_floor(ROOT)
    breed_pool = breed_keys(pools, breeds)
    if settings:
        bad = [s for s in settings if s not in pools['settings']]
        if bad:
            raise ValueError(f'no setting {", ".join(bad)} (settings: {", ".join(pools["settings"])})')
    setting_pool = list(settings or pools['settings'])
    memory = load_history(history) if history else {k: [] for k in KEEP}
    locks = {'action': action, 'expression': expression, 'coat': coat, 'frame': frame, 'aspect': aspect}
    chosen = {k: [] for k in KEEP}
    rolls = []
    for _ in range(count):
        breed = one_of(unused(breed_pool, chosen['breeds'], [] if breeds else memory['breeds']))
        setting = one_of(unused(setting_pool, chosen['settings'], [] if settings else memory['settings']))
        rec = compose(pools, breed, setting, locks, chosen['conditions'], memory['conditions'])
        held = stills.content(rec, floor_data, pools)
        if held:
            known = stills.entries(floor_data)
            raise ValueError('the roll breaks the floor; change the lock, never the prompt: ' + '; '.join(
                f'{i} ({stills.words(known.get(i))}): {r}' if i in known else f'{i}: {r}' for i, r in held))
        chosen['breeds'].append(breed)
        chosen['settings'].append(setting)
        chosen['conditions'].extend(rec['attributes']['conditions'])
        rolls.append(rec)
    if history:
        save_history(history, {k: memory[k] + chosen[k] for k in KEEP})
    if out:
        os.makedirs(out, exist_ok=True)
        for rec in rolls:
            with open(os.path.join(out, rec['roll_id'] + '.json'), 'w', encoding='utf-8') as f:
                json.dump(rec, f, indent=1, ensure_ascii=False)
    return rolls


def add_arguments(ap):
    ap.add_argument('--count', default=1, type=int, metavar='N', help=f'how many dogs, {MAX_COUNT} at most')
    ap.add_argument('--breed', help='lock the breed to a key or alias from dog_pools.json; give several, separated by commas, to draw among them')
    ap.add_argument('--setting', help='lock the setting to a key from dog_pools.json; give several, separated by commas, to draw among them')
    ap.add_argument('--action', dest='beat', help="what the dog is doing, verbatim from the approved script beat")
    ap.add_argument('--expression', help="lock the dog's expression (a real dog's, never a human one)")
    ap.add_argument('--coat', help="lock the coat colour, e.g. to match the store render the post ends on")
    ap.add_argument('--frame', choices=['photo', 'video'], default='photo',
                    help='a phone photo, or a frame from a phone video (a motion beat\'s start frame)')
    ap.add_argument('--aspect', help='the generator aspect ratio (default 3:4 for a photo, 9:16 for a video frame)')
    ap.add_argument('--slot', help='a sprint slot id (S01, V001): lock the breed it names')
    ap.add_argument('--manifest', default=SPRINT, help='the sprint manifest for --slot')
    ap.add_argument('--json', help='print each roll record as JSON', action='store_true')
    ap.add_argument('--list', help='show the breed and setting keys the locks take', action='store_true')


def show_keys(pools):
    print('Breeds (--breed):')
    for b in pools['breeds']:
        print(f'  {b["key"]:<20} {b["label"]}' + ('  [lock only]' if b.get('lock_only') else ''))
    print('Settings (--setting):')
    for key, place in pools['settings'].items():
        print(f'  {key:<20} {place["setting"]}')


def run(args, pools=None):
    pools = pools or load_pools()
    if args.list:
        show_keys(pools)
        return []
    breeds = args.breed.split(',') if args.breed else None
    if args.slot:
        if breeds:
            raise ValueError('--slot names its own breed; leave --breed off')
        named = slot_breed(args.slot, args.manifest)
        breeds = [named] if named else None
    settings = [s.strip() for s in args.setting.split(',')] if args.setting else None
    print('Read the floor first: python3 growth.py floor --format still', file=sys.stderr)
    rolls = roll(args.count, breeds, settings, args.beat, args.expression, args.coat, args.frame, args.aspect, pools=pools)
    if args.json:
        sys.stdout.write(json.dumps(rolls, indent=2, ensure_ascii=False) + '\n')
        return rolls
    for n, r in enumerate(rolls, 1):
        print(f'--- dog {n} of {len(rolls)}: {r["roll_id"]}, aspect {r["aspect_ratio"]} ---')
        print(r['summary'] + '\n')
        print(r['prompt'] + '\n')
    return rolls


def main(argv=None):
    ap = argparse.ArgumentParser(description='Roll prompts for generated dog stills that look like real pets on a phone.')
    add_arguments(ap)
    try:
        run(ap.parse_args(argv))
    except ValueError as e:
        sys.exit(f'Not rolled: {e}')


if __name__ == '__main__':
    main()
