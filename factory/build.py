"""Build finished posts from specs: chat, search, roast and film templates.

    HEARTSIDE_ASSETS=... HEARTSIDE_OUT=... python3 factory/build.py factory/specs/F10.json [...]

Every word comes from bank/lines.json by id and every product image from bank/renders.json, so a
spec cannot carry free text. Run `lock.py check` before and `lock.py gate` after.
"""
import json, os, sys, textwrap
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import lock

NAMES = {'lab': 'Lab', 'shepherd': 'Shepherd', 'frenchie': 'Frenchie', 'dachshund': 'Dachshund', 'golden': 'Golden', 'doodle': 'Doodle'}
TINTS = [(237, 231, 220), (225, 236, 243), (240, 228, 240), (246, 232, 214)]


def T(lid, spec):
    return lock.resolve(lid, spec)


def mug(breed):
    return next(r for r in lock.RENDERS.values() if r['breed'] == breed and r['product'] == 'mug')


def sfx_mix(work, total, end_t, music, level, events, voice=None, voice_level=1.0):
    """Music bed (dips under the end chime and fades), optional voice on top, timed SFX."""
    pop = f'{work}/pop.wav'; key = f'{work}/key.wav'; sting = f'{work}/sting.wav'
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=1320:duration=0.07', '-af', 'afade=t=out:st=0.01:d=0.06,volume=0.5', '-ar', '44100', '-ac', '2', pop])
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=0.03:c=pink:a=0.6', '-af', 'highpass=f=1800,afade=t=out:st=0.005:d=0.025', '-ar', '44100', '-ac', '2', key])
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=784:duration=0.35', '-f', 'lavfi', '-i', 'sine=frequency=1175:duration=0.35',
         '-filter_complex', '[0][1]amix=inputs=2,afade=t=out:st=0.02:d=0.33,volume=0.6', '-ar', '44100', '-ac', '2', sting])
    lib = {'pop': (pop, 0.6), 'key': (key, 0.35), 'sting': (sting, 0.55), 'scratch': (f'{AU}/s_scratch.mp3', 0.7)}
    inputs = ['-i', f'{AU}/{music}', '-i', f'{AU}/s_shimmer.mp3']
    filt = [f"[0:a]atrim=0:{total + 0.5},asetpts=PTS-STARTPTS,volume='if(lt(t,{end_t}),{level},{level}*0.6)':eval=frame,afade=t=in:d=0.4,afade=t=out:st={total - 2.5}:d=2.5[m]",
            f"[1:a]atrim=0:4,asetpts=PTS-STARTPTS,volume=0.8,afade=t=in:d=0.4,afade=t=out:st=2.6:d=1.4,adelay={int(end_t * 1000 + 200)}|{int(end_t * 1000 + 200)}[c]"]
    labels = ['[m]', '[c]']; idx = 2
    if voice:
        inputs += ['-i', f'{AU}/{voice}']; filt.append(f'[{idx}:a]aresample=44100,aformat=channel_layouts=stereo,volume={voice_level}[v]'); labels.append('[v]'); idx += 1
    for k, (t, kind, *rest) in enumerate(events):
        if kind in lib:
            src, vol = lib[kind]
        elif kind == 'gavel':
            src = f'{work}/gavel.wav'; vol = 0.9
            run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=95:duration=0.25', '-f', 'lavfi', '-i', 'anoisesrc=d=0.05:c=brown:a=0.8',
                 '-filter_complex', '[0]afade=t=out:st=0.02:d=0.22[a];[1]lowpass=f=1200[b];[a][b]amix=inputs=2,volume=1.6', '-ar', '44100', '-ac', '2', src])
        elif kind == 'creak':
            src = f'{work}/creak.wav'; vol = 0.8
            run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=210:duration=0.5', '-af', 'vibrato=f=18:d=0.9,tremolo=f=30:d=0.6,afade=t=in:d=0.05,afade=t=out:st=0.3:d=0.2,volume=0.7', '-ar', '44100', '-ac', '2', src])
        else:
            src, vol = f'{AU}/{kind}', 0.6
        if rest: vol = rest[0]
        ms = int(t * 1000); inputs += ['-i', src]
        filt.append(f'[{idx}:a]aresample=44100,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[e{k}]'); labels.append(f'[e{k}]'); idx += 1
    filt.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9,loudnorm=I=-16:TP=-1.5[o]')
    run(['ffmpeg', '-y'] + inputs + ['-filter_complex', ';'.join(filt), '-map', '[o]', '-t', f'{total:.2f}', '-ar', '44100', f'{work}/sound.m4a'])


def mux(work, sid):
    final = f'{OUTDIR}/{sid}.mp4'
    run(['ffmpeg', '-y', '-i', f'{work}/picture.mp4', '-i', f'{work}/sound.m4a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', final])
    return final


def end_card(spec, work, renders):
    sub = T(spec['end']['sub'], spec) if spec['end'].get('sub') else None
    im = product_card(renders, T(spec['end']['super'], spec), sub=sub); im.save(f'{work}/end.png'); return f'{work}/end.png'


# ---------------------------------------------------------------- chat
def chat(spec, work):
    cast = spec['cast']; slots = list(cast)
    AV = {k: avatar(mug(b)['file'], tuple(mug(b)['face'])) for k, b in cast.items()}
    TOP, BOTTOM, LEFT = 300, 1760, 60

    def bubble(m):
        who = m['who']; d0 = ImageDraw.Draw(Image.new('RGB', (10, 10)))
        if 'render' in m:
            body = Image.new('RGBA', (700, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(body, 'RGBA')
            d.rounded_rectangle((0, 0, 699, 639), 34, fill=(255, 255, 255, 255), outline=(220, 212, 200), width=2)
            p = Image.open(f"{R}/{m['render']}").convert('RGB'); p.thumbnail((660, 520), Image.LANCZOS)
            mask = Image.new('L', p.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, p.width - 1, p.height - 1), 26, fill=255)
            px = 20 + (660 - p.width) // 2; body.paste(p, (px, 20), mask)
            d.rounded_rectangle((px + 16, 36, px + 176, 82), 8, fill=(20, 18, 15, 190)); d.text((px + 30, 40), 'EXAMPLE', font=SMALL, fill=(255, 255, 255))
            d.text((30, 556), 'heartside.io', font=bold(F('Karla.ttf', 36), 800), fill=STAMP)
        else:
            text = T(m['line'], spec); lines = wrap_rich(d0, text, BODY, 46, 660)
            bw = int(max(text_width(d0, l, BODY, 46) for l in lines)) + 64; bh = 62 * len(lines) + 40
            body = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(body)
            d.rounded_rectangle((0, 0, bw - 1, bh - 1), 34, fill=TINTS[slots.index(who) % 4] + (255,))
            for i, l in enumerate(lines):
                draw_rich(body, (32, 18 + i * 62), l, BODY, 46, INK)
        blk = Image.new('RGBA', (W - LEFT * 2, body.height + 44), (0, 0, 0, 0))
        ImageDraw.Draw(blk).text((118, 0), NAMES[cast[who]], font=NAME, fill=(130, 120, 110))
        blk.paste(AV[who], (0, blk.height - 88), AV[who]); blk.paste(body, (110, 40), body)
        return blk

    def screen(blocks):
        im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, W, 250), fill=(250, 246, 238)); d.line((0, 250, W, 250), fill=(225, 216, 202), width=2)
        for i, k in enumerate(slots):
            a = AV[k].resize((70, 70)); im.paste(a, (W // 2 - 28 * len(slots) + i * 56, 40), a)
        t = T(spec['title'], spec); tw = d.textlength(t, font=TITLE); d.text(((W - tw) / 2, 130), t, font=TITLE, fill=INK)
        s = f'{len(slots)} dogs'; sw = d.textlength(s, font=SMALL); d.text(((W - sw) / 2, 186), s, font=SMALL, fill=(140, 130, 120))
        y = BOTTOM
        for b in reversed(blocks):
            y -= b.height + 22
            if y < TOP: break
            im.paste(b, (LEFT, y), b)
        d.rectangle((0, 1790, W, H), fill=(250, 246, 238)); d.line((0, 1790, W, 1790), fill=(225, 216, 202), width=2)
        d.rounded_rectangle((60, 1820, W - 60, 1890), 35, fill=(255, 255, 255), outline=(225, 216, 202), width=2)
        d.text((100, 1834), 'Message', font=bold(F('Karla.ttf', 34), 500), fill=(170, 160, 150))
        return im

    frames, blocks, events, t = [], [], [], 0.6
    screen([]).save(f'{work}/c00.png'); frames.append((f'{work}/c00.png', 0.6))
    for i, m in enumerate(spec['messages']):
        blocks.append(bubble(m)); p = f'{work}/c{i + 1:02d}.png'; screen(blocks).save(p)
        frames.append((p, m['dur'])); events.append((t, m.get('sfx', 'pop'))); t += m['dur']
    endp = end_card(spec, work, spec['end']['renders']); hold = spec['end'].get('hold', 4.5)
    frames.append((endp, hold)); frames_to_video(frames, f'{work}/picture.mp4')
    sfx_mix(work, t + hold, t, spec['music'], spec.get('music_level', 0.45), events)
    return mux(work, spec['id']), t + hold


# ---------------------------------------------------------------- search
def search(spec, work):
    SEARCH = bold(F('Karla.ttf', 62), 700); HIST = bold(F('Karla.ttf', 50), 500)
    RES = F('Fraunces.ttf', 120); RES.set_variation_by_axes([72, 650, 50, 0])
    m = mug(spec['breed']); AVA = avatar(m['file'], tuple(m['face']), size=100)

    def frame(query, typed, history, result=None, cursor=True):
        im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im, 'RGBA')
        d.text((70, 150), 'Search', font=bold(F('Karla.ttf', 64), 800), fill=INK); im.paste(AVA, (W - 170, 130), AVA)
        lines = wrap_rich(d, query[:typed], SEARCH, 62, W - 300) if typed else ['']
        box_h = max(140, 78 * len(lines) + 62)
        d.rounded_rectangle((60, 260, W - 60, 260 + box_h), 70, fill=(255, 255, 255), outline=(205, 195, 180), width=4)
        d.ellipse((100, 302, 150, 352), outline=(120, 110, 100), width=6); d.line((143, 345, 165, 367), fill=(120, 110, 100), width=7)
        for i, l in enumerate(lines):
            d.text((190, 290 + i * 78), l, font=SEARCH, fill=INK)
        if cursor:
            lx = 190 + d.textlength(lines[-1], font=SEARCH) + 6; ly = 290 + (len(lines) - 1) * 78
            d.rectangle((lx, ly + 6, lx + 5, ly + 72), fill=STAMP)
        y = 260 + box_h + 40
        if result == '@END':
            p = Image.open(f"{R}/{spec['end_render']}").convert('RGB'); p.thumbnail((900, 1100), Image.LANCZOS)
            px = (W - p.width) // 2; im.paste(p, (px, y + 20))
            d.rounded_rectangle((px + 24, y + 44, px + 230, y + 104), 10, fill=(20, 18, 15, 190)); d.text((px + 44, y + 52), 'EXAMPLE', font=SMALL, fill=(255, 255, 255))
            d.text((90, y + 40 + p.height), 'Top result', font=SMALL, fill=(140, 130, 120))
            d.text((90, y + 90 + p.height), T(spec['end']['super'], spec), font=RES, fill=INK)
            tw = d.textlength('heartside.io', font=SMALL); d.text((W - 90 - tw, y + 150 + p.height), 'heartside.io', font=SMALL, fill=STAMP)
            return im
        if result:
            d.rounded_rectangle((60, y, W - 60, y + 300), 30, fill=(255, 255, 255), outline=(225, 216, 202), width=2)
            d.text((100, y + 30), 'Top result', font=SMALL, fill=(140, 130, 120))
            d.text((100, y + 100), result, font=RES if len(result) < 10 else bold(F('Karla.ttf', 84), 800), fill=INK); y += 340
        d.text((70, y + 10), 'Recent searches', font=bold(F('Karla.ttf', 34), 800), fill=(140, 130, 120)); y += 70
        for h in reversed(history):
            hl = wrap_rich(d, h, HIST, 50, W - 230)
            d.ellipse((80, y + 6, 116, y + 42), outline=(170, 160, 150), width=4); d.line((98, y + 14, 98, y + 26), fill=(170, 160, 150), width=4); d.line((98, y + 26, 108, y + 32), fill=(170, 160, 150), width=4)
            for k, l in enumerate(hl):
                d.text((150, y + k * 62), l, font=HIST, fill=(110, 100, 90))
            y += 62 * len(hl) + 40
            if y > H - 120: break
        return im

    frames, events, t, history, n = [], [], 0.4, [], 0
    frame('', 0, []).save(f'{work}/k0000.png'); frames.append((f'{work}/k0000.png', 0.4))
    qs = spec['queries']
    for qi, q in enumerate(qs):
        text = T(q['line'], spec); last = qi == len(qs) - 1; step = 2 if len(text) > 40 else 1
        for c in range(step, len(text) + step, step):
            n += 1; p = f'{work}/k{n:04d}.png'; frame(text, min(c, len(text)), history).save(p)
            frames.append((p, 0.05)); events.append((t, 'key')); t += 0.05
        n += 1; p = f'{work}/k{n:04d}.png'; frame(text, len(text), history, cursor=False).save(p); frames.append((p, 0.35)); t += 0.35
        if last:
            events.append((t - 0.1, 'scratch')); end_t = t
            n += 1; p = f'{work}/end.png'; frame(text, len(text), history, '@END', cursor=False).save(p); frames.append((p, spec['end'].get('hold', 5.0))); t += spec['end'].get('hold', 5.0)
        else:
            events.append((t, 'sting')); res = T(q['result'], spec) if q.get('result') else None
            n += 1; p = f'{work}/k{n:04d}.png'; frame(text, len(text), history, res, cursor=False).save(p); frames.append((p, q['hold'])); t += q['hold']
            history.append(text)
    frames_to_video(frames, f'{work}/picture.mp4')
    sfx_mix(work, t, end_t, spec['music'], spec.get('music_level', 0.42), events)
    return mux(work, spec['id']), t


# ---------------------------------------------------------------- roast (carousel plus reel)
def roast(spec, work):
    CW, CH = 1080, 1350; breed = spec['breed']; rd = lock.RENDERS[spec['render']]
    HEAD = F('Fraunces.ttf', 96); HEAD.set_variation_by_axes([72, 700, 50, 0])
    LINE = F('Fraunces.ttf', 84); LINE.set_variation_by_axes([72, 560, 50, 0]); TAG = bold(F('Karla.ttf', 34), 800)

    def label(d, x, y):
        d.rounded_rectangle((x, y, x + 164, y + 50), 8, fill=(20, 18, 15, 190)); d.text((x + 16, y + 6), 'EXAMPLE', font=SMALL, fill=(255, 255, 255))

    def centered(d, lines, font, y, lh):
        for i, l in enumerate(lines):
            tw = d.textlength(l, font=font); d.text(((CW - tw) / 2, y + i * lh), l, font=font, fill=INK)
    slides = []
    im = Image.new('RGB', (CW, CH), CREAM); d = ImageDraw.Draw(im, 'RGBA')
    src = Image.open(f"{R}/{spec['render']}").convert('RGB'); cx, cy = rd['crop']; r = 225
    crop = src.crop((cx - r, cy - r, cx + r, cy + r)).resize((760, 760), Image.LANCZOS)
    mask = Image.new('L', crop.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, 759, 759), 40, fill=255)
    im.paste(crop, ((CW - 760) // 2, 120), mask); label(d, (CW - 760) // 2 + 20, 140)
    centered(d, textwrap.wrap(T(spec['title'], spec), 22), HEAD, 940, 112); slides.append(im)
    for i, lid in enumerate(spec['lines']):
        soft = lock.LINES[lid]['role'] == 'roast.soft'
        im = Image.new('RGB', (CW, CH), CREAM if soft else (36, 32, 27)); d = ImageDraw.Draw(im, 'RGBA')
        wl = wrap_rich(d, T(lid, spec), LINE, 84, 900); y0 = (CH - 104 * len(wl)) / 2 - 40
        d.text((90, y0 - 120), f'{i + 1}/{len(spec["lines"])}', font=TAG, fill=STAMP)
        for k, w in enumerate(wl):
            d.text((90, y0 + k * 104), w, font=LINE, fill=INK if soft else (246, 241, 231))
        d.text((90, CH - 130), f'Love, your {breed}', font=TAG, fill=STAMP if soft else (170, 160, 150)); slides.append(im)
    im = Image.new('RGB', (CW, CH), CREAM); d = ImageDraw.Draw(im, 'RGBA')
    centered(d, textwrap.wrap(T(spec['end']['super'], spec), 22), HEAD, 90, 112)
    p = Image.open(f"{R}/{spec['render']}").convert('RGB'); p.thumbnail((900, 960), Image.LANCZOS)
    px = (CW - p.width) // 2; im.paste(p, (px, 330)); label(d, px + 20, 350)
    tw = d.textlength('heartside.io', font=TAG); d.text(((CW - tw) / 2, CH - 70), 'heartside.io', font=TAG, fill=STAMP); slides.append(im)
    frames = []
    for i, s in enumerate(slides):
        s.save(f'{work}/slide{i + 1}.png')
        v = Image.new('RGB', (W, H), s.getpixel((5, 5))); v.paste(s, (0, (H - CH) // 2))
        v.save(f'{work}/end.png' if i == len(slides) - 1 else f'{work}/v{i + 1}.png')
        frames.append((f'{work}/end.png' if i == len(slides) - 1 else f'{work}/v{i + 1}.png', spec['durs'][i]))
    frames_to_video(frames, f'{work}/picture.mp4')
    starts = [sum(spec['durs'][:i]) for i in range(len(slides))]; total = sum(spec['durs'])
    sfx_mix(work, total, starts[-1], spec['music'], spec.get('music_level', 0.5), [(starts[1] - 0.08, 'scratch', 0.6)])
    return mux(work, spec['id']), total


# ---------------------------------------------------------------- film
CAPB = bold(F('Karla.ttf', 54), 800)


def _cover(path, crop_top=0.0):
    im = Image.open(path).convert('RGB')
    if crop_top: im = im.crop((0, int(im.height * crop_top), im.width, im.height))
    r = max(W / im.width, H / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def _caption(im, text, y=1440):
    if not text: return im
    d = ImageDraw.Draw(im, 'RGBA'); lines = textwrap.wrap(text, 28); lh = 70; h = lh * len(lines) + 44
    d.rounded_rectangle((60, y, W - 60, y + h), 24, fill=(20, 18, 15, 185))
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=CAPB); d.text(((W - tw) / 2, y + 22 + i * lh), l, font=CAPB, fill=(255, 255, 255))
    return im


def _render_shot(name, cap):
    im = Image.new('RGB', (W, H), CREAM)
    p = Image.open(f'{R}/{name}').convert('RGB'); p.thumbnail((900, 1150), Image.LANCZOS)
    x, y = (W - p.width) // 2, 180; im.paste(p, (x, y)); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((x + 24, y + 24, x + 212, y + 80), 10, fill=(20, 18, 15, 190)); d.text((x + 42, y + 32), 'EXAMPLE', font=SMALL, fill=(255, 255, 255))
    return _caption(im, cap)


def film(spec, work):
    parts, t0 = [], 0.0
    for i, s in enumerate(spec['shots']):
        dur = s['until'] - t0; t0 = s['until']; cap = T(s['line'], spec) if s.get('line') else None
        if s.get('render'):
            im = _render_shot(s['render'], cap); zoom = '1'
        else:
            im = _caption(_cover(f"{FR}/{s['frame']}", s.get('crop_top', 0)), cap); zoom = 'min(zoom+0.0007,1.08)'
        png = f'{work}/s{i:02d}.png'; im.save(png); n = round(dur * 30); out = f'{work}/s{i:02d}.mp4'
        run(['ffmpeg', '-y', '-loop', '1', '-i', png, '-vf', f"scale=2160:3840,zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps=30,format=yuv420p",
             '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out]); parts.append(out)
    end_t = t0; hold = spec['end'].get('hold', 4.2); total = end_t + hold
    endp = end_card(spec, work, spec['end']['renders'])
    run(['ffmpeg', '-y', '-loop', '1', '-i', endp, '-vf', 'format=yuv420p', '-frames:v', str(round(hold * 30)), '-r', '30', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', f'{work}/end.mp4'])
    parts.append(f'{work}/end.mp4')
    with open(f'{work}/list.txt', 'w') as fh:
        fh.write(''.join(f"file '{p}'\n" for p in parts))
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt', '-c', 'copy', f'{work}/picture.mp4'])
    sfx_mix(work, total, end_t, spec['music'], spec.get('music_level', 0.2), [tuple(e) for e in spec.get('sfx', [])], voice=spec['voice'])
    return mux(work, spec['id']), total


TEMPLATES = {'chat': chat, 'search': search, 'roast': roast, 'film': film}

if __name__ == '__main__':
    preview = '--preview' in sys.argv  # build a held post so Krish can judge its proposed lines in place; never posted
    for p in [a for a in sys.argv[1:] if not a.startswith('--')]:
        spec = json.load(open(p, encoding='utf-8'))
        probs, _ = lock.check(spec)
        if probs and not preview:
            print(f"{spec['id']}: held before building ({len(probs)} problem(s)); run lock.py check"); continue
        work = f"{OUTDIR}/{spec['id']}"; os.makedirs(work, exist_ok=True)
        f, t = TEMPLATES[spec['template']](spec, work); print(f, round(t, 2))
