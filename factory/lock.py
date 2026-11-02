"""The lock system: once Krish approves a finished post, it cannot drift.

Ruling (Krish, 2026-11-02): "We need to figure out a way of making this reliable so that we don't get
drift and we don't get weird humor and things that don't make sense once stuff is locked in."

    python3 factory/lock.py check  SPEC          static gates (bank, breed fit, renders, copy, lock)
    python3 factory/lock.py media  SPEC MP4      media gates on the rendered file
    python3 factory/lock.py brief  SPEC          the sense-check brief for the independent reviewer
    python3 factory/lock.py lock   SPEC --by "Krish's words"   freeze an approved post (interactive only)
    python3 factory/lock.py record SPEC VERDICT [--note ...]   reviewer-pass | reviewer-hold |
                                                               krish-approve | krish-decline
    python3 factory/lock.py gate   SPEC MP4      everything above, plus the trust ramp: may it go out?

How it holds:
1. A lock freezes a post's skeleton: its structure, timings, music, sound, product type and every
   line's role. Its fingerprint is the sha256 of that skeleton. A variant must produce the same
   fingerprint, so only the slots can change.
2. Slots: which dog plays which part (cast or breed), which approved line fills a role, which real
   render of the same product type closes it. Voiced films freeze their lines too.
3. Every line comes from bank/lines.json, approved, and tagged for the breed that says it.
4. Every product image is a file in bank/renders.json, byte for byte, for the right breed.
5. The house copy rules from growth.py run on every line.
6. An independent reviewer reads the brief and records pass or hold. Code gates decide; the
   reviewer only catches what code cannot.
7. Trust ramp: the first 5 variants of a lock go to Krish; then 1 in 10. A Krish decline retires
   the variant's line and breed pairs; two declines pause the lock.
The ledger is local (local/factory/ledger.json): scheduled runs change no tracked file (rule 9).
"""
import argparse, copy, hashlib, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BANK = json.load(open(f'{HERE}/bank/lines.json', encoding='utf-8'))
LINES = {l['id']: l for l in BANK['lines']}
RENDERS = {r['file']: r for r in json.load(open(f'{HERE}/bank/renders.json'))['renders']}
LEDGER = os.environ.get('HEARTSIDE_LEDGER', f'{ROOT}/local/factory/ledger.json')
LIB = os.path.abspath(os.environ.get('HEARTSIDE_ASSETS', f'{ROOT}/local/assets/library'))
OUT = os.path.abspath(os.environ.get('HEARTSIDE_OUT', f'{ROOT}/local/media/factory'))
RAMP_FIRST, RAMP_EVERY, PAUSE_AFTER = 5, 10, 2


_G = None


def _growth():
    global _G
    if _G: return _G
    spec = importlib.util.spec_from_file_location('growth', f'{ROOT}/growth.py')
    g = importlib.util.module_from_spec(spec); argv = sys.argv; sys.argv = ['growth.py']
    if ROOT not in sys.path: sys.path.insert(0, ROOT)
    try:
        spec.loader.exec_module(g)
    finally:
        sys.argv = argv
    _G = g
    return g


def ledger():
    try:
        return json.load(open(LEDGER))
    except (FileNotFoundError, json.JSONDecodeError):
        return {'records': [], 'retired': []}


def save_ledger(d):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(d, open(LEDGER, 'w'), indent=1)


# ---------------------------------------------------------------- skeleton and fingerprint
def uses(spec):
    """Every (line id, breed that says it) and every render the post shows."""
    t = spec['template']; lines, renders = [], []
    if t == 'chat':
        for m in spec['messages']:
            if 'line' in m:
                lines.append((m['line'], spec['cast'][m['who']]))
            if 'render' in m:
                renders.append((m['render'], spec['cast'][m['who']]))
        lines.append((spec['title'], 'any'))
        renders += [(r, 'cast') for r in spec['end']['renders']]
    elif t == 'search':
        lines += [(q['line'], spec['breed']) for q in spec['queries']] + [(q['result'], spec['breed']) for q in spec['queries'] if q.get('result')]
        renders += [(spec['end_render'], spec['breed'])]
    elif t == 'roast':
        lines += [(spec['title'], spec['breed'])] + [(l, spec['breed']) for l in spec['lines']]
        renders += [(spec['render'], spec['breed'])]
    elif t == 'film':
        lines += [(s['line'], spec['breed']) for s in spec['shots'] if s.get('line')]
        renders += [(s['render'], spec['breed']) for s in spec['shots'] if s.get('render')]
        renders += [(r, spec['breed']) for r in spec['end']['renders']]
    if spec.get('end', {}).get('super'):
        lines.append((spec['end']['super'], 'any'))
    if spec.get('end', {}).get('sub'):
        lines.append((spec['end']['sub'], 'any'))
    return lines, renders


def skeleton(spec):
    """The spec with every slot replaced by what it must stay: a line by its role, a render by its
    product type, the cast and breed by their names only. Voiced films keep their lines."""
    s = copy.deepcopy(spec); voiced = 'voice' in spec
    for k in ('id', 'title_note', 'variant_of', 'note'):
        s.pop(k, None)

    def walk(x):
        if isinstance(x, dict):
            out = {}
            for k, v in x.items():
                if k in ('line', 'result', 'title', 'super', 'sub') and isinstance(v, str) and v in LINES and not voiced:
                    out[k] = 'role:' + LINES[v]['role']
                elif k in ('render', 'end_render') and isinstance(v, str):
                    out[k] = 'product:' + RENDERS.get(v, {}).get('product', '?')
                elif k == 'renders':
                    out[k] = ['product:' + RENDERS.get(r, {}).get('product', '?') for r in v]
                elif k == 'lines' and isinstance(v, list) and not voiced:
                    out[k] = ['role:' + LINES.get(l, {}).get('role', '?') for l in v]
                elif k == 'cast':
                    out[k] = sorted(v)
                elif k == 'breed' and not voiced:
                    out[k] = 'slot'
                else:
                    out[k] = walk(v)
            return out
        if isinstance(x, list):
            return [walk(i) for i in x]
        return x
    return walk(s)


def fingerprint(spec):
    return hashlib.sha256(json.dumps(skeleton(spec), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def lock_for(spec):
    lid = spec.get('variant_of') or spec['id']
    p = f'{HERE}/locks/{lid}.json'
    return (json.load(open(p)), p) if os.path.exists(p) else (None, p)


# ---------------------------------------------------------------- static gates
def copy_problems(g, text, kind):
    low = text.lower(); p = []
    if g.EM_DASH.search(text): p.append('em dash')
    if '!' in text: p.append('exclamation mark')
    p += [f'banned word "{w}"' for w in g.BANNED + g.SLOP if re.search(r'\b' + re.escape(w) + r'\b', low)]
    if g.NOT_BUT.search(text): p.append('"not X, but Y" framing')
    if g.SAD.search(text): p.append('death or illness')
    p += [why for rx, why in g.RETIRED if rx.search(text)]
    p += [why for rx, why in g.FAKE_PROOF if rx.search(text)]
    p += [f'UK spelling (use {us})' for rx, us in g.UK if rx.search(text)]
    if g.EMOJI.search(text) and kind != 'chat': p.append('emoji outside a chat bubble')
    return p


def check(spec, quiet=False):
    """Returns (problems, warnings). Problems block; warnings are listed for Krish."""
    g = _growth(); probs, warns = [], []
    retired = {(r['line'], r['breed']) for r in ledger()['retired']}
    lines, renders = uses(spec)
    cast_breeds = set(spec.get('cast', {}).values()) or {spec.get('breed')}
    for lid, breed in lines:
        l = LINES.get(lid)
        if not l:
            probs.append(f'{lid}: not in the joke bank (write it as a proposed line first)'); continue
        if l['status'] != 'approved':
            probs.append(f'{lid} "{l["text"]}": {l["status"]}, not approved by Krish')
        elif l.get('text_sha256') != hashlib.sha256(l['text'].encode()).hexdigest():
            probs.append(f'{lid} "{l["text"]}": edited after Krish approved it (add the new wording as a proposed line)')
        if breed != 'any' and 'any' not in l['breeds'] and breed not in l['breeds']:
            probs.append(f'{lid} "{l["text"]}": said by a {breed}, but tagged only for {", ".join(l["breeds"])}')
        if (lid, breed) in retired or (lid, 'any') in retired:
            probs.append(f'{lid}: retired for {breed} after a decline')
        text = l['text'].replace('{breed}', spec.get('breed') or 'dog')
        probs += [f'{lid} "{text}": {p}' for p in copy_problems(g, text, l['kind'])]
        if l['kind'] in ('gift', 'headline') and g.stacked(text):
            probs.append(f'{lid} "{text}": stacked fragments')
        elif g.stacked(text):
            warns.append(f'{lid} "{text}": stacked short sentences (allowed in spoken dialogue, approved as voiced)')
    for f, breed in renders:
        r = RENDERS.get(f)
        if not r:
            probs.append(f'{f}: not an approved store render'); continue
        path = f'{LIB}/renders/{f}'
        if not os.path.exists(path):
            probs.append(f'{f}: missing from {LIB}/renders')
        elif hashlib.sha256(open(path, 'rb').read()).hexdigest() != r['sha256']:
            probs.append(f'{f}: file differs from the approved render (altered or replaced)')
        want = cast_breeds if breed == 'cast' else {breed}
        if r['breed'] != 'any' and r['breed'] not in want:
            probs.append(f'{f}: shows a {r["breed"]}, but this post is about {", ".join(sorted(want))}')
    if spec['template'] == 'film':
        for s in spec['shots']:
            if s.get('frame') and not os.path.exists(f'{LIB}/frames/{s["frame"]}'):
                probs.append(f'frame {s["frame"]} missing')
            if s.get('frame') and spec.get('frame_breeds', {}).get(s['frame'], spec['breed']) != spec['breed']:
                probs.append(f'frame {s["frame"]} shows another breed')
        last = spec['shots'][-1]['until']; voice = f"{LIB}/audio/{spec['voice']}"
        if os.path.exists(voice):
            dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', voice], capture_output=True, text=True).stdout or 0)
            if last + 0.3 < dur:
                probs.append(f'the shots end at {last}s but the voice runs to {dur:.1f}s')
        else:
            probs.append(f'voice {spec["voice"]} missing')
    lk, _ = lock_for(spec)
    if lk:
        if lk.get('status') == 'paused':
            probs.append(f'lock {lk["id"]} is paused after declines')
        if fingerprint(spec) != lk['fingerprint']:
            probs.append(f'drift: this post no longer matches lock {lk["id"]} (only slots may change)')
    elif spec.get('variant_of'):
        probs.append(f'variant of {spec["variant_of"]}, which is not locked')
    return probs, warns


# ---------------------------------------------------------------- media gates
def probe(mp4):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height:format=duration', '-of', 'json', mp4], capture_output=True, text=True).stdout)
    v = next(s for s in j['streams'] if s['codec_type'] == 'video'); a = [s for s in j['streams'] if s['codec_type'] == 'audio']
    return v['width'], v['height'], float(j['format']['duration']), bool(a)


def media(spec, mp4):
    probs = []
    w, h, dur, has_audio = probe(mp4)
    if (w, h) != (1080, 1920): probs.append(f'{w}x{h}, not 1080x1920')
    if not has_audio: probs.append('no sound')
    if not 6 <= dur <= 60: probs.append(f'{dur:.1f}s long (6 to 60 allowed)')
    out = subprocess.run(['ffmpeg', '-i', mp4, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.findall(r'I:\s+(-?[\d.]+) LUFS', out)
    if m and not -18 <= float(m[-1]) <= -13: probs.append(f'loudness {m[-1]} LUFS (want -18 to -13)')
    # the post must end on the product card, held at least 3 seconds
    end_png = spec.get('_end_png') or f"{OUT}/{spec['id']}/end.png"
    if end_png and os.path.exists(end_png):
        import numpy as np
        from PIL import Image
        ref = np.asarray(Image.open(end_png).convert('L').resize((108, 192)), dtype=float)
        for back in (0.2, 3.0):
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(dur - back, 0):.2f}', '-i', mp4, '-frames:v', '1', '-vf', 'scale=108:192,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
            fr = np.frombuffer(raw, np.uint8).astype(float)
            if fr.size != ref.size or abs(fr.reshape(ref.shape) - ref).mean() > 12:
                probs.append(f'the frame {back}s from the end is not the product end card'); break
    return probs


# ---------------------------------------------------------------- review brief
STANDING = [  # each one was caught by a reviewer on 2 Nov 2026; add new catches here
    'one setting and one cast across the post: no shot that jumps to another place or adds a human where the joke has none',
    'no AI-drawn product: no mug, blanket, portrait or card with lettering or a dog painting except the real render labelled EXAMPLE',
    'no plain blanket or mug in a generated frame that could pass for the product without its design',
    'no chestnut or red dachshund in a generated frame (it can read as Buddy, and no Buddy image is approved)',
    'no stray marks that read as glitches or threats (laser dots, warped text, extra limbs)',
    'avatars and crops show a dog face; captions never cover the key visual or the EXAMPLE label',
    'every emoji, prop and picture matches the word it sits next to',
]
def resolve(lid, spec):
    return LINES[lid]['text'].replace('{breed}', spec.get('breed') or 'dog') if lid in LINES else f'[{lid}]'


def brief(spec):
    out = [f"Sense check for {spec['id']} ({spec['template']}). Look at the actual frames, not these descriptions. For each beat, answer: "
           f"does the picture match the line, and does the joke make sense for this dog? Reply pass, or hold with the frame and the reason. "
           f"Do not judge taste; Krish did.", '', 'Standing checks, every post:'] + [f'- {c}' for c in STANDING] + ['']
    t = spec['template']
    if t == 'chat':
        out.append('Cast: ' + ', '.join(f'{k} is a {v}' for k, v in spec['cast'].items()))
        out += [f"- {spec['cast'][m['who']]}: {resolve(m['line'], spec) if 'line' in m else '[shares a link to ' + m['render'] + ']'}" for m in spec['messages']]
    elif t == 'search':
        out.append(f"The searcher is a {spec['breed']}.")
        out += [f"- searches: {resolve(q['line'], spec)}" + (f" / result: {resolve(q['result'], spec)}" if q.get('result') else '') for q in spec['queries']]
    elif t == 'roast':
        out.append(f"The dog is a {spec['breed']}.")
        out += [f'- {resolve(l, spec)}' for l in [spec['title']] + spec['lines']]
    elif t == 'film':
        out.append(f"The dog is a {spec['breed']}.")
        out += [f"- picture: {s.get('picture', s.get('frame') or 'real render ' + s.get('render', ''))} / line: {resolve(s['line'], spec) if s.get('line') else '(none)'}" for s in spec['shots']]
    out.append(f"- ends on: {', '.join(spec['end'].get('renders', [spec.get('end_render', spec.get('render'))]))} with \"{resolve(spec['end']['super'], spec)}\"")
    return '\n'.join(out)


# ---------------------------------------------------------------- ledger, ramp and gate
def records(lid):
    return [r for r in ledger()['records'] if r['lock'] == lid]


def ramp(spec):
    """Whether this variant may go out on the reviewer's pass, or needs Krish."""
    lk, _ = lock_for(spec)
    if not lk or lk.get('status') != 'locked':
        return 'krish', 'not locked yet'
    if spec['id'] == lk['id']:
        return 'ok', 'the locked master'
    rs = records(lk['id']); shown = [r for r in rs if r['verdict'].startswith('krish-')]
    variants = sorted({r['spec'] for r in rs if r['spec'] != lk['id']})
    if len(shown) < RAMP_FIRST:
        return 'krish', f'{len(shown)} of the first {RAMP_FIRST} variants shown to Krish'
    n = variants.index(spec['id']) + 1 if spec['id'] in variants else len(variants) + 1
    return ('krish', f'spot check: variant {n} (1 in {RAMP_EVERY})') if n % RAMP_EVERY == 0 else ('ok', 'past the ramp')


def record(spec, verdict, note=''):
    d = ledger(); lk, lp = lock_for(spec); lid = lk['id'] if lk else spec['id']
    d['records'].append({'lock': lid, 'spec': spec['id'], 'verdict': verdict, 'note': note, 'fingerprint': fingerprint(spec)})
    if verdict == 'krish-decline':
        lines, _ = uses(spec)
        d['retired'] += [{'line': l, 'breed': b, 'why': note or 'Krish declined ' + spec['id']} for l, b in lines
                         if not (lk and spec['id'] == lk['id']) and b != 'any']
        if lk and sum(r['verdict'] == 'krish-decline' for r in d['records'] if r['lock'] == lid) >= PAUSE_AFTER:
            lk['status'] = 'paused'; json.dump(lk, open(lp, 'w'), indent=1, ensure_ascii=False)
    save_ledger(d)


def gate(spec, mp4):
    probs, warns = check(spec)
    probs += media(spec, mp4)
    rs = [r for r in records((lock_for(spec)[0] or {}).get('id', spec['id'])) if r['spec'] == spec['id'] and r['fingerprint'] == fingerprint(spec)]
    rv = [r['verdict'] for r in rs if r['verdict'].startswith('reviewer-')]
    if not rv or rv[-1] != 'reviewer-pass':
        probs.append('no independent reviewer pass on this exact post')
    who, why = ramp(spec)
    kv = [r['verdict'] for r in rs if r['verdict'].startswith('krish-')]
    if who == 'krish' and (not kv or kv[-1] != 'krish-approve'):
        probs.append(f'needs Krish: {why}')
    if kv and kv[-1] == 'krish-decline':
        probs.append('Krish declined this post')
    return probs, warns


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('spec'); ap.add_argument('arg', nargs='?')
    ap.add_argument('--by', default=''); ap.add_argument('--note', default='')
    a = ap.parse_args(); spec = json.load(open(a.spec, encoding='utf-8'))
    if a.cmd == 'check':
        p, w = check(spec)
        for x in w: print('note:', x)
        for x in p: print('HOLD:', x)
        print(f"{spec['id']}: {'ready' if not p else str(len(p)) + ' problem(s)'}  fingerprint {fingerprint(spec)[:16]}")
        sys.exit(1 if p else 0)
    if a.cmd == 'media':
        p = media(spec, a.arg); [print('HOLD:', x) for x in p]; print('media', 'ok' if not p else 'held'); sys.exit(1 if p else 0)
    if a.cmd == 'brief':
        print(brief(spec)); return
    if a.cmd == 'lock':
        if not a.by:
            sys.exit('lock needs --by with Krish\'s own words approving this post')
        p, _ = check(spec)
        if p:
            [print('HOLD:', x) for x in p]; sys.exit('fix these before locking')
        lk = {'id': spec['id'], 'status': 'locked', 'approved_by': a.by, 'fingerprint': fingerprint(spec),
              'master': os.path.relpath(a.spec, HERE), 'template': spec['template'],
              'slots': {'chat': 'cast, lines by role, link render', 'search': 'breed, lines by role, end render',
                        'roast': 'breed, lines by role, render', 'film': 'end render of the same product and breed'}[spec['template']]}
        json.dump(lk, open(f"{HERE}/locks/{spec['id']}.json", 'w'), indent=1, ensure_ascii=False); print('locked', spec['id'], lk['fingerprint'][:16]); return
    if a.cmd == 'record':
        assert a.arg in ('reviewer-pass', 'reviewer-hold', 'krish-approve', 'krish-decline'), a.arg
        record(spec, a.arg, a.note); print('recorded', a.arg); return
    if a.cmd == 'gate':
        p, w = gate(spec, a.arg)
        for x in w: print('note:', x)
        for x in p: print('HOLD:', x)
        print(f"{spec['id']}: {'may go out' if not p else 'held'}"); sys.exit(1 if p else 0)


if __name__ == '__main__':
    main()
