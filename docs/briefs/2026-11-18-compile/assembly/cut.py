#!/usr/bin/env python3
"""Cut a finished Heartside studio film from a brief and the chosen Kling takes (16 to 22 Nov sprint).

    python3 cut.py build d1-alibi-03 --takes s1=t2,s2=t1 [--end RENDER | --no-end] [--hold 3.0]
                         [--in s2=0.3] [--frame s1=1.08:0.5:0.6] [--label-y 360] [--style stroke|panel]
    python3 cut.py gate  d1-alibi-03      re-run every gate on the last build
    python3 cut.py parse d1-alibi-03      show what was read from the brief

Inputs: briefs/<id>.md and kling3/<id>_s<shot>_t<take>.mp4 beside this folder. A take may be `placeholder`
(a plain card marked PLACEHOLDER; the file is named *.PLACEHOLDER.mp4, tagged on every frame and never postable)
or a path to a clip.

Why not factory/build.py: its templates take still frames and approved bank lines only (a film needs a voice and
every word from bank/lines.json), so a clip with brief labels cannot pass `lock.py check`. This tool reuses what
fits instead: the house regions, end hold and export preset (engine/creative_ui.py), the caption wrapping and
layout manifest (factory/ui_layout.py), the house copy rules and render bank (factory/lock.py), `lock.py media`,
`codex/check_picture.py` and `factory/panel.py sheet`. It edits no tracked file.

What it makes, in local/media/studio/<id>/ of the growth repository:
- each shot conformed to 1080x1920 by one uniform scale and a crop (never a stretch), trimmed to the brief;
- the brief's labels burned at one fixed place (text top y 360, Karla 800 at 54 px, centred x 140 to 820);
- the store's own render as the end card, scaled and pushed in only, held 3 to 4 s;
- no audio track (the song is added in the app); H.264 in the house export preset.
"""
import argparse, hashlib, json, math, os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent
BRIEFS, KLING = STUDIO / 'briefs', Path(os.environ.get('HEARTSIDE_KLING', Path.home() / '.scratch' / 'heartside-studio-2026-11-16' / 'kling3'))
REPO = Path(os.environ.get('HEARTSIDE_REPO', r'C:\Users\krish\dev\growth-heartside'))
LIB = Path(os.environ.get('HEARTSIDE_ASSETS', REPO / 'local' / 'assets' / 'library'))
OUT = Path(os.environ.get('HEARTSIDE_STUDIO_OUT', REPO / 'local' / 'media' / 'studio'))
sys.path[:0] = [str(REPO), str(REPO / 'factory')]

from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402
import ui_layout  # noqa: E402  (factory: caption wrapping, layout manifest, end hold)
from engine.creative_ui import (CRITICAL, HOOK, END_HOLD, FFMPEG_VIDEO, HOOK_WORDS, CAPTION_SIZE,  # noqa: E402
                                REVISION, layout_errors, media_errors, words)

W, H, FPS = 1080, 1920, 30
LABEL_Y = HOOK[1]                       # text top y 360: the top band since 12 Nov (codex/README.md)
FLOOR_BAND = (250, 1250)                # floor fixed-label-position
LABEL_X = (HOOK[0], HOOK[2])            # centred between x 140 and 820
LH = round(CAPTION_SIZE * 1.18)
AUDIO_ONLY = re.compile(r'no audio stream|no sound|audio codec|audio \d+ Hz|audio channels|true peak', re.I)


def font(size=CAPTION_SIZE, weight=800):
    f = ImageFont.truetype(str(LIB / 'fonts' / 'Karla.ttf'), size)   # the factory's label face: CAPB in build.py
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.file_digest(fh, 'sha256').hexdigest()


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f'{cmd[0]} failed: {r.stderr[-1500:]}')
    return r.stdout


def probe(path):
    j = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path]))
    v = next(s for s in j['streams'] if s['codec_type'] == 'video')
    num, _, den = v.get('r_frame_rate', '0/1').partition('/')
    return {'w': v['width'], 'h': v['height'], 'dur': float(v.get('duration') or j['format']['duration']),
            'fps': float(num) / float(den or 1), 'audio': any(s['codec_type'] == 'audio' for s in j['streams'])}


# ---------------------------------------------------------------- the brief
def section(text, name):
    m = re.search(rf'^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)', text, re.M | re.S)
    return m.group(1) if m else ''


def parse(bid):
    path = BRIEFS / f'{bid}.md'
    text = path.read_text(encoding='utf-8')
    shots = [{'n': int(m[1]), 'tag': (m[2] or '').strip(), 'dur': float(m[3])}
             for m in re.finditer(r'^### Shot (\d+)(?: \(([^)]*)\))?: ([\d.]+) s', text, re.M)]
    labels = [{'start': float(a), 'end': float(b), 'text': t.strip()}
              for a, b, t in re.findall(r'^- ([\d.]+) to ([\d.]+) s: "(.*)"\s*$', section(text, 'On-screen labels'), re.M)]
    m = re.search(r'^- Product: ([^,]+), store render `([^`]+)`', text, re.M)
    product = {'type': m[1].strip(), 'render': m[2]} if m else None
    m = re.search(r'^- Length: ([\d.]+) s(?:, payoff by ([\d.]+) s)?', text, re.M)
    cap = re.search(r'```(?:text)?\n(.*?)```', section(text, 'Caption'), re.S)
    breeds = re.findall(r'^- Dog [A-Z]: ([^,]+),', text, re.M)
    if not shots:
        raise SystemExit(f'{path}: no "### Shot N: D s" headings')
    return {'id': bid, 'brief': str(path), 'brief_sha256': sha(path), 'shots': shots, 'labels': labels,
            'product': product, 'length': float(m[1]) if m else None,
            'payoff_by': float(m[2]) if m and m[2] else None,
            'caption': cap.group(1).strip() if cap else '', 'dogs': breeds}


def kv(arg, cast=str):
    out = {}
    for part in filter(None, (arg or '').split(',')):
        k, _, v = part.partition('=')
        out[int(k.strip().lstrip('sS'))] = cast(v.strip())
    return out


def frame_opt(v):   # zoom:focus_x:focus_y, e.g. 1.08:0.5:0.65 (focus 0 = keep the top/left edge, 1 = bottom/right)
    p = [float(x) for x in v.split(':')]
    return {'zoom': p[0], 'fx': p[1] if len(p) > 1 else 0.5, 'fy': p[2] if len(p) > 2 else 0.5}


# ---------------------------------------------------------------- drawing
def label_png(text, path, y, style):
    """One label on a clear 1080x1920 layer at the fixed place; refused, never shrunk, if it needs a third line."""
    f = font(); im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if style == 'panel':   # the factory's own subtitle panel (ui_layout.caption), text top at y
        ui_layout.caption(im, text, f, y - 10)
        lines = ui_layout.caption_lines(d, text, f, ui_layout.SUBTITLES[2] - ui_layout.SUBTITLES[0] - 48)
        box = (ui_layout.SUBTITLES[0], y - 10, ui_layout.SUBTITLES[2], y - 10 + 2 * ui_layout.CAPTION_LINE_HEIGHT + 32)
    else:                  # white with a dark stroke, as factory/lipsync_cut.py draws format labels
        lines = ui_layout.caption_lines(d, text, f, LABEL_X[1] - LABEL_X[0])
        if len(lines) > 2:
            raise SystemExit(f'label {text!r} needs more than two lines: rewrite it, do not shrink it')
        for i, line in enumerate(lines):
            tw = d.textlength(line, font=f)
            d.text(((LABEL_X[0] + LABEL_X[1] - tw) / 2, y + i * LH), line, font=f, fill='white',
                   stroke_width=max(4, CAPTION_SIZE // 11), stroke_fill='black')
        box = (LABEL_X[0], y - 4, LABEL_X[1], y + 2 * LH + 8)   # the label's place (two lines), the same for every label
    im.save(path)
    return [int(v) for v in box], lines


def placeholder_png(path, shot):
    im = Image.new('RGB', (W, H), (48, 48, 48)); d = ImageDraw.Draw(im)
    for x in range(-H, W, 160):   # hazard stripes: nobody mistakes this for a shot
        d.polygon([(x, H), (x + 60, H), (x + 60 + H, 0), (x + H, 0)], fill=(70, 62, 30))
    big, small = font(120), font(54)
    for text, f, y, fill in (('PLACEHOLDER', big, 860, (230, 40, 40)), (f'shot {shot} not generated', small, 1010, 'white'),
                             ('DO NOT POST', small, 1080, 'white')):
        tw = d.textlength(text, font=f)
        d.text(((W - tw) / 2, y), text, font=f, fill=fill, stroke_width=4, stroke_fill='black')
    im.save(path)


def tag_png(path):
    """A red tag on every frame of a film that holds a placeholder (outside the content region)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = font(44)
    d.rectangle((0, 1560, W, 1640), fill=(200, 20, 20, 255))
    t = 'PLACEHOLDER  DO NOT POST'; d.text(((W - d.textlength(t, font=f)) / 2, 1572), t, font=f, fill='white')
    im.save(path)


def border_tone(img):
    import numpy as np
    a = np.asarray(img, dtype=float)
    e = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(e, axis=0)), float(e.std(axis=0).max())


PAINT_PRINT = 'https://cdnx.teeinblue.com/r2/customers/uploads/'
PAINT_BASE = 'https://cdn.teeinblue.com/users/333342/mockup-layers/'


def render_path(render):
    """An approved store render by name, or a painted end card: a .png from heartside.io's own painter
    (local/paint/out), laid out as the product page lays it, with its .json record beside it."""
    p = Path(render)
    return p if p.suffix == '.png' and p.exists() else LIB / 'renders' / render


def painted_problems(render, dogs):
    """The painted end card's provenance: the record beside it, the file unchanged since, the store's own
    renderer for both layers, and the film's own dog."""
    p = Path(render); rec_path = p.with_suffix('.json'); probs = []
    if not rec_path.exists():
        return [f'{p.name}: no painter record beside it'], None
    r = json.loads(rec_path.read_text(encoding='utf-8'))
    if r.get('png_sha256') != sha(p):
        probs.append(f'{p.name}: file differs from its painter record')
    if not str(r.get('print', '')).startswith(PAINT_PRINT) or not str(r.get('base_layer', '')).startswith(PAINT_BASE):
        probs.append(f'{p.name}: layers are not from the store product renderer')
    if 'utm_source=internal-paint' not in str(r.get('page', '')):
        probs.append(f'{p.name}: not painted through the tagged internal-paint flow')
    if r.get('dog', '').lower() not in ' '.join(dogs).lower():
        probs.append(f"{p.name}: painted a {r.get('dog')}, the film's dogs are {', '.join(dogs)}")
    return probs, r


def end_card(render, work, hold, ground='auto'):
    """The store's render, pixels untouched: one uniform scale per frame and a slow push-in (1.00 to 1.04),
    inside the critical box. A plain-backdrop render (mug, card) sits on its own backdrop tone; a scene render
    on a blurred, darkened copy of itself, as factory/common.product_clip lays a scene out."""
    src = Image.open(render_path(render)).convert('RGB')
    tone, spread = border_tone(src)
    if ground == 'plain':   # floor real-product: a clean store render on a plain ground (tier 1, 17 Nov)
        back = Image.new('RGB', (W, H), (241, 236, 229))
    elif spread < 6:
        back = Image.new('RGB', (W, H), tone)
    else:
        r0 = max(W / src.width, H / src.height)
        back = src.resize((math.ceil(src.width * r0), math.ceil(src.height * r0)), Image.BICUBIC)
        bx, by = (back.width - W) // 2, (back.height - H) // 2
        back = back.crop((bx, by, bx + W, by + H)).filter(ImageFilter.GaussianBlur(28))
        back = Image.blend(back, Image.new('RGB', (W, H), (20, 18, 15)), 0.25)
    x0, y0, x1, y1 = CRITICAL
    fit = min((x1 - x0) / src.width, (y1 - y0) / src.height) / 1.045   # the push-in ends inside the box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    n = round(hold * FPS); out = work / 'end.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '8', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-colorspace', 'bt709', str(out)], stdin=subprocess.PIPE)
    union = None; last = None
    for k in range(n):
        s = fit * (1 + 0.04 * k / max(n - 1, 1))
        im = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
        fr = back.copy(); ox, oy = round(cx - im.width / 2), round(cy - im.height / 2)
        fr.paste(im, (ox, oy)); box = (ox, oy, ox + im.width, oy + im.height)
        union = box if union is None else (min(union[0], box[0]), min(union[1], box[1]), max(union[2], box[2]), max(union[3], box[3]))
        p.stdin.write(fr.tobytes()); last = (fr, box)
    p.stdin.close(); p.wait()
    last[0].save(work / 'end.png')
    return out, union, last[1]


# ---------------------------------------------------------------- build
def build(a):
    b = parse(a.id)
    takes, ins, frames = kv(a.takes), kv(a.ins, float), kv(a.frame, frame_opt)
    out_dir = OUT / a.id; out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / 'work'; work.mkdir(exist_ok=True)
    for old in out_dir.glob(f'{a.id}*.mp4'):
        old.unlink()   # one current build per brief; never leave a stale cut beside the new one
    render = None if a.no_end else (a.end or (b['product'] or {}).get('render'))
    plate = a.plate_hold
    shots, t = [], 0.0
    for s in b['shots']:
        take = takes.get(s['n'])
        if take is None:
            raise SystemExit(f"shot {s['n']}: no take chosen (--takes s{s['n']}=t1, or s{s['n']}=placeholder)")
        dur = plate if (render and 'plate' in s['tag'].lower()) else s['dur']   # a plate: its empty patch, then the render
        sh = {'n': s['n'], 'tag': s['tag'], 'dur': dur, 'start': round(t, 3), 'in': ins.get(s['n'], 0.0), 'take': take}
        if take.lower() == 'placeholder':
            sh['src'] = str(work / f"ph_s{s['n']}.png"); placeholder_png(sh['src'], s['n']); sh['placeholder'] = True
        else:
            src = Path(take) if os.path.sep in take or '/' in take else KLING / f"{a.id}_s{s['n']}_{take}.mp4"
            if not src.exists():
                raise SystemExit(f'shot {s["n"]}: {src} not found')
            pr = probe(src)
            if pr['dur'] + 1e-3 < sh['in'] + dur - 1 / pr['fps']:
                raise SystemExit(f"shot {s['n']}: {src.name} runs {pr['dur']:.2f} s, the brief needs {dur} s from {sh['in']} s")
            fo = frames.get(s['n'], {'zoom': 1.0, 'fx': 0.5, 'fy': 0.5})
            k = max(W / pr['w'], H / pr['h']) * fo['zoom']            # one uniform scale: never a stretch
            sw, shh = math.ceil(pr['w'] * k / 2) * 2, math.ceil(pr['h'] * k / 2) * 2
            cx, cy = round((sw - W) * fo['fx']), round((shh - H) * fo['fy'])
            sh.update(src=str(src), src_sha256=sha(src), source=f"{pr['w']}x{pr['h']}@{pr['fps']:g}", scale=round(k, 5),
                      scaled=f'{sw}x{shh}', crop=[cx, cy, W, H], **fo)
        shots.append(sh); t += dur
    body = round(t, 3)
    labels = []
    for i, l in enumerate(b['labels']):
        if l['end'] > body + 1e-6:
            raise SystemExit(f"label {l['text']!r} runs to {l['end']} s, past the last shot at {body} s")
        box, lines = label_png(l['text'], work / f'label{i}.png', a.label_y, a.style)
        labels.append({**l, 'box': box, 'lines': lines, 'png': str(work / f'label{i}.png')})
    placeholder = any(s.get('placeholder') for s in shots)
    hold = ui_layout.end_hold(a.hold) if render else 0.0
    end = None
    if render:
        end_mp4, union, last_box = end_card(render, work, hold, getattr(a, 'ground', 'auto'))
        end = {'render': render, 'hold': hold, 'box': list(union), 'last_box': list(last_box), 'mp4': str(end_mp4),
               'png': str(work / 'end.png')}
    # One ffmpeg graph: conform, trim and cut the shots, burn the labels, append the end card, encode once.
    cmd, graph, idx = ['ffmpeg', '-y', '-v', 'error'], [], 0
    for i, s in enumerate(shots):
        n = round(s['dur'] * FPS)
        if s.get('placeholder'):
            cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f"{s['dur'] + 0.5:.3f}", '-i', s['src']]
            graph.append(f'[{idx}:v]scale={W}:{H},setsar=1,fps={FPS},format=yuv420p,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]')
        else:
            sw, shh = s['scaled'].split('x')
            cmd += ['-ss', f"{s['in']:.3f}", '-t', f"{s['dur'] + 0.5:.3f}", '-i', s['src']]
            graph.append(f"[{idx}:v]scale={sw}:{shh}:flags=lanczos,crop={W}:{H}:{s['crop'][0]}:{s['crop'][1]},setsar=1,"
                         f"fps={FPS},format=yuv420p,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]")
        idx += 1
    graph.append(''.join(f'[v{i}]' for i in range(len(shots))) + f'concat=n={len(shots)}:v=1:a=0[b0]')
    cur = 'b0'
    for i, l in enumerate(labels):
        cmd += ['-loop', '1', '-i', l['png']]
        graph.append(f"[{cur}][{idx}:v]overlay=0:0:shortest=1:enable='gte(t,{l['start'] - 0.0005})*lt(t,{l['end'] - 0.0005})'[b{i + 1}]")
        cur = f'b{i + 1}'; idx += 1
    if end:
        cmd += ['-i', end['mp4']]
        graph.append(f'[{idx}:v]setsar=1,fps={FPS},format=yuv420p[e];[{cur}][e]concat=n=2:v=1:a=0[f0]'); cur = 'f0'; idx += 1
    if placeholder:
        tag = work / 'tag.png'; tag_png(tag); cmd += ['-loop', '1', '-i', tag]
        graph.append(f'[{cur}][{idx}:v]overlay=0:0:shortest=1[f1]'); cur = 'f1'; idx += 1
    graph.append(f'[{cur}]setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[out]'); cur = 'out'
    total = round(body + hold, 3)
    final = out_dir / (f'{a.id}.PLACEHOLDER.mp4' if placeholder else f'{a.id}.mp4')
    cmd += ['-filter_complex', ';'.join(graph), '-map', f'[{cur}]', '-an', *FFMPEG_VIDEO,
            '-frames:v', str(round(total * FPS)), '-movflags', '+faststart', final]
    run(cmd)
    # The layout manifest the factory gates read, bound to this exact file.
    lay = ui_layout.Layout()
    for s in shots:
        lay.add('picture', (0, 0, W, H), s['start'], s['start'] + s['dur'], Path(s['src']).name)
    for l in labels:
        lay.add('label', l['box'], l['start'], l['end'], l['text'], lines=len(l['lines']), px=CAPTION_SIZE)
    if end:
        lay.add('product', end['box'], body, total, render); lay.ending = 'product'
    else:
        lay.ending = 'none'
    lay.duration = total; lay.media_sha256 = sha(final); lay.save(out_dir / 'layout.json')
    # The picture-card timeline codex/check_picture.py reads: one segment per change of shot or label.
    cuts = sorted({0.0, body, *[s['start'] for s in shots], *[x for l in labels for x in (l['start'], l['end'])]})
    segs = []
    for x, y in zip(cuts, cuts[1:]):
        if y - x < 1e-6 or x >= body:
            continue
        lab = next((l for l in labels if l['start'] <= x < l['end']), None)
        shot = next(s for s in shots if s['start'] <= x < s['start'] + s['dur'] + 1e-6)
        seg = {'seconds': round(y - x, 3), 'src': Path(shot['src']).name}
        if lab:
            seg.update(label=lab['text'], label_box=lab['box'])
        segs.append(seg)
    if end:
        segs.append({'seconds': hold, 'product': render})
    (out_dir / 'timeline.json').write_text(json.dumps({'id': a.id, 'shots': segs}, indent=1), encoding='utf-8')
    (out_dir / 'caption.txt').write_text(b['caption'] + '\n', encoding='utf-8')
    rec = {'tool': 'assembly/cut.py', 'brief': b, 'shots': shots, 'labels': [{k: v for k, v in l.items() if k != 'png'} for l in labels],
           'end': end, 'body_seconds': body, 'total_seconds': total, 'label_y': a.label_y, 'style': a.style,
           'placeholder': placeholder, 'postable': False, 'media': str(final), 'media_sha256': lay.media_sha256,
           'ui_profile': REVISION, 'audio': 'none: the song is added in the app'}
    (out_dir / 'build.json').write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8')
    print(final, f'{total:.2f} s')
    return gate(a)


# ---------------------------------------------------------------- gates
def gate(a):
    out_dir = OUT / a.id; rec = json.loads((out_dir / 'build.json').read_text(encoding='utf-8'))
    final = Path(rec['media']); b = rec['brief']; res = []

    def add(name, problems=(), review=None, waived=()):
        res.append({'gate': name, 'hold': list(problems), 'waived': list(waived), 'review': review})

    import lock   # factory: house copy rules, render bank, media gate
    g = lock._growth()
    # 1. House copy rules (growth.py, via lock.copy_problems) on every label and the caption.
    p = [f"label {l['text']!r}: {x}" for l in rec['labels'] for x in lock.copy_problems(g, l['text'], 'label')]
    p += [f'caption {line!r}: {x}' for line in b['caption'].splitlines() if line.strip() for x in lock.copy_problems(g, line, 'caption')]
    p += [f'{line!r}: asks for or carries an AI label (floor no-ai-label)' for line in [l['text'] for l in rec['labels']] + b['caption'].splitlines()
          if re.search(r'\bAI\b|ai[- ]generated|made with ai', line, re.I)]
    add('copy (growth.py house rules, no-ai-label)', p)
    # 2. Labels: one fixed place inside the floor band and the critical box, at most 2 lines and 12 words.
    p = []
    tops = {l['box'][1] for l in rec['labels']}
    if len(tops) > 1:
        p.append(f'labels sit at {sorted(tops)}: one fixed place for the whole reel')
    for l in rec['labels']:
        x0, y0, x1, y1 = l['box']
        if not (CRITICAL[0] <= x0 and x1 <= CRITICAL[2] and CRITICAL[1] <= y0 and y1 <= CRITICAL[3]):
            p.append(f"label {l['text']!r} box {l['box']} leaves the critical box {CRITICAL}")
        if not (FLOOR_BAND[0] <= y0 and y1 <= FLOOR_BAND[1]):
            p.append(f"label {l['text']!r} leaves the floor band y {FLOOR_BAND}")
        if words(l['text']) > HOOK_WORDS:
            p.append(f"label {l['text']!r}: {words(l['text'])} words (at most {HOOK_WORDS})")
    add('labels (fixed-label-position)', p, review='step through every labelled frame: the label never touches a dog\'s eyes or mouth (text-clear-of-faces); recrop with --frame, never move the label')
    # 3. The real product: an approved store render, byte for byte.
    p, product_note = [], None
    if rec['end']:
        painted = Path(rec['end']['render']).suffix == '.png' and Path(rec['end']['render']).exists()
        r = None if painted else lock.RENDERS.get(rec['end']['render'])
        f = render_path(rec['end']['render'])
        if painted:
            pp, _ = painted_problems(rec['end']['render'], b['dogs']); p.extend(pp)
        if not painted and not r:
            p.append(f"{rec['end']['render']}: not an approved store render (factory/bank/renders.json)")
        elif not painted and (not f.exists() or sha(f) != r['sha256']):
            p.append(f"{rec['end']['render']}: file differs from the approved render")
        if painted or (r and f.exists() and sha(f) == r['sha256']):
            import numpy as np   # the encoded end frame against the composited render: pixels scaled only
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-sseof', '-0.05', '-i', str(final), '-frames:v', '1', '-f', 'rawvideo',
                                  '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
            got = np.frombuffer(raw, np.uint8)
            if got.size == W * H * 3:
                x0, y0, x1, y1 = rec['end']['last_box']
                ref = np.asarray(Image.open(rec['end']['png']).convert('RGB'), dtype=float)[y0:y1, x0:x1]
                diff = float(np.abs(got.reshape(H, W, 3).astype(float)[y0:y1, x0:x1] - ref).mean())
                if diff > 6:
                    p.append(f'the product in the last frame differs from the store render by {diff:.1f} levels on average (want 6 or under)')
                product_note = f'last-frame product vs store render: {diff:.2f} levels mean difference (scale and push-in only)'
            else:
                p.append('could not read the last frame')
        breed = (r or {}).get('breed')
        dogs = ' '.join(b['dogs']).lower()
        if breed and breed != 'any' and breed not in dogs:
            p.append(f"the render shows a {breed}, the film's dogs are {', '.join(b['dogs'])}")
    else:
        p.append('no product end card: every film holds the real product at least 3 s (floor endings-land, audit rule 3); pass --end RENDER')
    add('real product end card (real-product, endings-land)', p, review=product_note)
    # 4. The layout manifest against the 12 Nov corpus profile.
    lay = json.loads((out_dir / 'layout.json').read_text(encoding='utf-8'))
    probs, notes = layout_errors(lay)
    if lay.get('media_sha256') != sha(final):
        probs.append('the layout manifest belongs to another build')
    add('layout (engine.creative_ui.layout_errors)', probs, review='; '.join(notes) or None)
    # 5. Export preset on the encoded file.
    probs, notes = media_errors(final)
    add('export preset (engine.creative_ui.media_errors)', [x for x in probs if not AUDIO_ONLY.search(x)],
        waived=[x + ' (silent by design: the song is added in the app)' for x in probs if AUDIO_ONLY.search(x)],
        review='; '.join(notes) or None)
    # 6. factory/lock.py media, bound to this build's manifest and end frame.
    spec = {'id': a.id, 'template': 'film', '_layout': str(out_dir / 'layout.json'), '_end_png': rec['end']['png'] if rec['end'] else ''}
    probs = lock.media(spec, str(final))
    add('lock.py media', [x for x in probs if not AUDIO_ONLY.search(x.replace('export: ', ''))],
        waived=[x + ' (silent by design)' for x in probs if AUDIO_ONLY.search(x.replace('export: ', ''))])
    # 7. codex/check_picture.py, the picture-card acceptance.
    r = subprocess.run([sys.executable, str(REPO / 'codex' / 'check_picture.py'), str(final), str(out_dir / 'timeline.json')],
                       capture_output=True, text=True, cwd=REPO)
    lines = [x for x in r.stdout.strip().splitlines() if x and x != 'ok']
    add('codex/check_picture.py', [x for x in lines if not AUDIO_ONLY.search(x)],
        waived=[x + ' (silent by design)' for x in lines if AUDIO_ONLY.search(x)])
    # 8. Timing: the brief's length, payoff by second 4, 8 to 12 s before the end card (audit rule 3), under 60 s.
    p, body, total = [], rec['body_seconds'], rec['total_seconds']
    if b['length'] and abs(body - b['length']) > 0.05 and not any('plate' in s['tag'].lower() for s in rec['shots']):
        p.append(f"cut runs {body} s, the brief says {b['length']} s")
    if total >= 60:
        p.append(f'{total} s long (under 60)')
    payoff = next((s['start'] for s in rec['shots'] if 'payoff' in s['tag'].lower()), None)
    if b['payoff_by'] and payoff is not None and payoff > b['payoff_by']:
        p.append(f"the payoff shot starts at {payoff} s, after {b['payoff_by']} s")
    add('timing (brief, audit rule 3)', p, review=None if 8 <= body <= 12 else f'{body} s before the end card (rule 3 wants 8 to 12)')
    # 9. Placeholder guard.
    add('placeholder guard', ['holds a PLACEHOLDER shot: never post this file'] if rec['placeholder'] else [])
    held = any(x['hold'] for x in res)
    rec['gates'] = res; rec['verdict'] = 'held' if held else 'passes code gates; needs the full-size review'
    (out_dir / 'build.json').write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8')
    for x in res:
        state = 'HOLD' if x['hold'] else 'PASS'
        print(f"{state:5} {x['gate']}")
        for y in x['hold']:
            print(f'        hold: {y}')
        for y in x['waived']:
            print(f'      waived: {y}')
        if x['review']:
            print(f"      review: {x['review']}")
    print('REVIEW (not code): real-dogs anatomy at full size; text-clear-of-faces on every labelled frame; the cut lands; deadpan-labels; the song is chosen in the app')
    # The contact sheet the panel reads, plus full-size guide frames (floor band 250/1250 red, critical box green).
    sheet = run([sys.executable, str(REPO / 'factory' / 'panel.py'), 'sheet', str(final), '--out', str(out_dir / 'sheet.png')]).strip()
    guides(rec, out_dir)
    print('sheet', sheet)
    print('verdict', rec['verdict'])
    return 1 if held else 0


def guides(rec, out_dir):
    """Full-size frames at every label and the end card, with the floor band and the critical box drawn on."""
    final = rec['media']; gdir = out_dir / 'frames'; gdir.mkdir(exist_ok=True)
    for old in gdir.glob('*.png'):
        old.unlink()
    times = sorted({round((l['start'] + l['end']) / 2, 2) for l in rec['labels']} | {round(s['start'] + 0.2, 2) for s in rec['shots']}
                   | ({round(rec['body_seconds'] + 0.2, 2), round(rec['total_seconds'] - 0.1, 2)} if rec['end'] else set()))
    thumbs = []
    for t in times:
        p = gdir / f'{t:05.2f}s.png'
        run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t:.2f}', '-i', final, '-frames:v', '1', p])
        im = Image.open(p).convert('RGB'); d = ImageDraw.Draw(im)
        for y in FLOOR_BAND:
            d.line((0, y, W, y), fill=(255, 0, 0), width=3)
        d.rectangle(CRITICAL, outline=(0, 255, 0), width=3)
        d.text((10, 10), f'{t:.2f}s', fill=(255, 255, 0), font=font(40))
        im.save(p); thumbs.append(im)
    cols = 4; tw = 360; th = 640; rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * tw, rows * th))
    for i, im in enumerate(thumbs):
        sheet.paste(im.resize((tw, th), Image.LANCZOS), ((i % cols) * tw, (i // cols) * th))
    sheet.save(out_dir / 'guides.png')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=('build', 'gate', 'parse')); ap.add_argument('id')
    ap.add_argument('--takes', help='s1=t2,s2=t1 (or s1=placeholder, or s1=<path to a clip>)')
    ap.add_argument('--in', dest='ins', help='in-points in seconds, s2=0.3')
    ap.add_argument('--frame', help='recrop a shot: s1=zoom:focus_x:focus_y, e.g. s1=1.1:0.5:0.7 pushes the dog down from the label')
    ap.add_argument('--end', help='end-card render from factory/bank/renders.json (default: the brief\'s Product line)')
    ap.add_argument('--no-end', action='store_true', help='no end card (the gates hold it: floor endings-land)')
    ap.add_argument('--ground', choices=['auto', 'plain'], default='auto', help='end-card ground: auto (house layout) or plain cream behind the unaltered render')
    ap.add_argument('--hold', type=float, default=END_HOLD[0], help='end-card hold, 3 to 4 s')
    ap.add_argument('--plate-hold', type=float, default=1.0, help='seconds of a "product plate" shot before the render')
    ap.add_argument('--label-y', type=int, default=LABEL_Y, help='label text top (360, or about 1050 just under the middle)')
    ap.add_argument('--style', choices=('stroke', 'panel'), default='stroke')
    a = ap.parse_args()
    if a.cmd == 'parse':
        print(json.dumps(parse(a.id), indent=1, ensure_ascii=False)); return 0
    if a.cmd == 'gate':
        return gate(a)
    return build(a)


if __name__ == '__main__':
    sys.exit(main())
