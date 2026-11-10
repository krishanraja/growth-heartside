"""Build finished posts from specs: chat, search, roast, film and still templates.

    HEARTSIDE_ASSETS=... HEARTSIDE_OUT=... python3 factory/build.py factory/specs/F10.json [...]

Every word comes from bank/lines.json by id and every product image from bank/renders.json, so a
spec cannot carry free text. Run `lock.py check` before and `lock.py gate` after.
"""
import json, os, sys, textwrap
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from common import _border_color, _cutout
import lock
import ui_layout


def _ui_v1(spec):
    locked, _ = lock.lock_for(spec)
    return ui_layout.enabled(spec, locked, lock.fingerprint(spec))

NAMES = {'lab': 'Lab', 'shepherd': 'Shepherd', 'frenchie': 'Frenchie', 'dachshund': 'Dachshund', 'golden': 'Golden', 'doodle': 'Doodle'}
TINTS = [(237, 231, 220), (225, 236, 243), (240, 228, 240), (246, 232, 214)]


def T(lid, spec):
    return lock.resolve(lid, spec)


def mug(breed):
    return next(r for r in lock.RENDERS.values() if r['breed'] == breed and r['product'] == 'mug')


def sfx_mix(work, total, end_t, music, level, events, voice=None, voice_level=1.0, soft_at=None, music_start=0.0):
    """Music bed (dips under the end chime and fades), optional voice on top, timed SFX."""
    pop = f'{work}/pop.wav'; key = f'{work}/key.wav'; sting = f'{work}/sting.wav'
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=1320:duration=0.07', '-af', 'afade=t=out:st=0.01:d=0.06,volume=0.5', '-ar', '44100', '-ac', '2', pop])
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=0.03:c=pink:a=0.6', '-af', 'highpass=f=1800,afade=t=out:st=0.005:d=0.025', '-ar', '44100', '-ac', '2', key])
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=784:duration=0.35', '-f', 'lavfi', '-i', 'sine=frequency=1175:duration=0.35',
         '-filter_complex', '[0][1]amix=inputs=2,afade=t=out:st=0.02:d=0.33,volume=0.6', '-ar', '44100', '-ac', '2', sting])
    lib = {'pop': (pop, 0.6), 'key': (key, 0.35), 'sting': (sting, 0.55), 'scratch': (f'{AU}/s_scratch.mp3', 0.7)}
    inputs = ['-i', f'{AU}/{music}', '-i', f'{AU}/s_shimmer.mp3']
    dip = end_t if soft_at is None else min(soft_at, end_t)
    filt = [f"[0:a]atrim={music_start}:{music_start + total + 0.5},asetpts=PTS-STARTPTS,volume='if(lt(t,{dip}),{level},{level}*0.6)':eval=frame,afade=t=in:d=0.4,afade=t=out:st={total - 2.5}:d=2.5[m]",
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
        elif kind == 'boom':
            src = f'{work}/boom.wav'; vol = 0.9
            run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=52:duration=0.7', '-f', 'lavfi', '-i', 'sine=frequency=104:duration=0.25',
                 '-filter_complex', '[0]afade=t=out:st=0.05:d=0.65[a];[1]afade=t=out:st=0.01:d=0.24,volume=0.5[b];[a][b]amix=inputs=2,volume=2.2', '-ar', '44100', '-ac', '2', src])
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


def end_clip(spec, work, renders, hold):
    """The ending: the real product, moving, with no slogan, URL or badge (Krish, 2 Nov: organic posts)."""
    options = {'box': ui_layout.CRITICAL, 'critical_box': ui_layout.CRITICAL} if _ui_v1(spec) else {}
    return product_clip(renders, f'{work}/end.mp4', hold, end_png=f'{work}/end.png', **options)


def join(parts, out):
    with open(out + '.txt', 'w') as fh:
        fh.write(''.join(f"file '{p}'\n" for p in parts))
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', out + '.txt', '-c', 'copy', out])


# ---------------------------------------------------------------- chat
def chat(spec, work):
    cast = spec['cast']; slots = list(cast)
    native = _ui_v1(spec)
    body_font = bold(F('Karla.ttf', 54), 500) if native else BODY
    text_width_max = 570 if native else 660
    AV = {k: avatar(mug(b)['file'], tuple(mug(b)['face'])) for k, b in cast.items()}
    TOP, BOTTOM, LEFT = 300, 1760, 60

    def bubble(m):
        who = m['who']; d0 = ImageDraw.Draw(Image.new('RGB', (10, 10)))
        if 'photo' in m:   # a photo the dog sends: no card, just the rounded picture (social-ui profile only)
            p = Image.open(f"{FR}/{m['photo']}").convert('RGB'); p.thumbnail((400, 400), Image.LANCZOS)   # leaves room for the reply under it
            body = Image.new('RGBA', p.size, (0, 0, 0, 0))
            mask = Image.new('L', p.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, p.width - 1, p.height - 1), 30, fill=255)
            body.paste(p, (0, 0), mask)
        elif 'render' in m:
            bw, bh = (634, 400) if native else (700, 560)   # native: the link preview and one reply share the screen
            body = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(body, 'RGBA')
            d.rounded_rectangle((0, 0, bw - 1, bh - 1), 34, fill=(255, 255, 255, 255), outline=(220, 212, 200), width=2)
            p = Image.open(f"{R}/{m['render']}").convert('RGB'); p.thumbnail((bw - 40, bh - 40), Image.LANCZOS)
            mask = Image.new('L', p.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, p.width - 1, p.height - 1), 26, fill=255)
            px = 20 + (bw - 40 - p.width) // 2; body.paste(p, (px, 20), mask)
        else:
            text = T(m['line'], spec); lines = balanced_wrap(d0, text, body_font, text_width_max, 54 if native else 46)
            bw = int(max(text_width(d0, l, body_font, 54 if native else 46) for l in lines)) + 64; bh = 66 * len(lines) + 40 if native else 62 * len(lines) + 40
            if native and bw > 646:
                raise ValueError('chat text crosses the working region; split the beat')
            body = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(body)
            d.rounded_rectangle((0, 0, bw - 1, bh - 1), 34, fill=TINTS[slots.index(who) % 4] + (255,))
            for i, l in enumerate(lines):
                draw_rich(body, (32, 18 + i * (66 if native else 62)), l, body_font, 54 if native else 46, INK)
        blk = Image.new('RGBA', (756 if native else W - LEFT * 2, body.height + 44), (0, 0, 0, 0))
        ImageDraw.Draw(blk).text((118, 0), NAMES[cast[who]], font=NAME, fill=(130, 120, 110))
        blk.paste(AV[who], (0, blk.height - 88), AV[who]); blk.paste(body, (110, 40), body)
        return blk

    def screen(blocks):
        if native:
            return ui_layout.chat_screen(blocks, T(spec['title'], spec), list(AV.values()), TITLE, SMALL, PAPER)
        im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, W, 250), fill=(71, 61, 52)); d.line((0, 250, W, 250), fill=(225, 216, 202), width=2)
        for i, k in enumerate(slots):
            a = AV[k].resize((70, 70)); im.paste(a, (W // 2 - 28 * len(slots) + i * 56, 40), a)
        t = T(spec['title'], spec); tw = d.textlength(t, font=TITLE); d.text(((W - tw) / 2, 130), t, font=TITLE, fill=PAPER)
        s = f'{len(slots)} dogs'; sw = d.textlength(s, font=SMALL); d.text(((W - sw) / 2, 186), s, font=SMALL, fill=(234, 226, 214))
        visible = []
        room = BOTTOM - TOP
        for block in reversed(blocks):
            if block.height + 22 > room: break
            visible.append(block)
            room -= block.height + 22
        y = TOP + room // 2
        for block in reversed(visible):
            im.paste(block, (LEFT, y), block)
            y += block.height + 22
        d.rectangle((0, 1790, W, H), fill=(250, 246, 238)); d.line((0, 1790, W, 1790), fill=(225, 216, 202), width=2)
        d.rounded_rectangle((60, 1820, W - 60, 1890), 35, fill=(255, 255, 255), outline=(225, 216, 202), width=2)
        d.text((100, 1834), 'Message', font=bold(F('Karla.ttf', 34), 500), fill=(170, 160, 150))
        return im

    frames, blocks, events, t = [], [], [], 0.6
    n0 = max(1, spec.get('open_with', 0)) if native else spec.get('open_with', 0)
    if n0:
        blocks = [bubble(m) for m in spec['messages'][:n0]]; t = sum(m['dur'] for m in spec['messages'][:n0])
        screen(blocks).save(f'{work}/c00.png'); frames.append((f'{work}/c00.png', t)); events.append((0.0, 'pop'))
    else:
        screen([]).save(f'{work}/c00.png'); frames.append((f'{work}/c00.png', 0.6))
    for i, m in enumerate(spec['messages']):
        if i < n0: continue
        blocks.append(bubble(m)); p = f'{work}/c{i + 1:02d}.png'; screen(blocks).save(p)
        frames.append((p, m['dur'])); events.append((t, m.get('sfx', 'pop'))); t += m['dur']
    hold = spec['end'].get('hold', 4.5)
    frames_to_video(frames, f'{work}/chat.mp4'); end_clip(spec, work, spec['end']['renders'], hold)
    join([f'{work}/chat.mp4', f'{work}/end.mp4'], f'{work}/picture.mp4')
    sfx_mix(work, t + hold, t, spec['music'], spec.get('music_level', 0.45), events)
    return mux(work, spec['id']), t + hold


# ---------------------------------------------------------------- search
def search(spec, work):
    SEARCH = bold(F('Karla.ttf', 62), 700); HIST = bold(F('Karla.ttf', 50), 500)
    RES = F('Fraunces.ttf', 120); RES.set_variation_by_axes([72, 650, 50, 0])
    RESL = bold(F('Karla.ttf', 76), 800)
    m = mug(spec['breed']); AVA = avatar(m['file'], tuple(m['face']), size=100)
    BAR = (60, 260, W - 60, 400); TX = 190; TW = BAR[2] - 70 - TX   # the bar never grows

    def bar_text(d, text):
        """What a phone search field shows: the tail that fits, the start scrolled out of view."""
        while text and d.textlength(text, font=SEARCH) > TW:
            text = text[1:]
        return text

    def answer_block(d, y, result):
        f, size = (RES, 120) if d.textlength(result, font=RES) <= W - 200 else (RESL, 76)
        lines = balanced_wrap(d, result, f, W - 200, size); lh = 140 if f is RES else 92
        h = 130 + lh * len(lines)
        d.rounded_rectangle((60, y, W - 60, y + h), 30, fill=(255, 255, 255), outline=(225, 216, 202), width=2)
        d.text((100, y + 30), 'Top result', font=SMALL, fill=(140, 130, 120))
        for i, l in enumerate(lines):
            d.text((100, y + 86 + i * lh), l, font=f, fill=INK)
        return y + h + 40

    def bar_font(d, text):
        """A finished query is shown whole: the type shrinks until it fits (never cut off at the start)."""
        size = 62
        while size > 34 and d.textlength(text, font=bold(F('Karla.ttf', size), 700)) > TW + 25:   # a finished query has no cursor, so it may use the bar's right padding
            size -= 2
        return bold(F('Karla.ttf', size), 700)

    def frame(query, typed, history, result=None, cursor=True):
        im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im, 'RGBA')
        d.text((70, 150), 'Search', font=bold(F('Karla.ttf', 64), 800), fill=INK); im.paste(AVA, (W - 170, 130), AVA)
        d.rounded_rectangle(BAR, 70, fill=(255, 255, 255), outline=(205, 195, 180), width=4)
        d.ellipse((100, 302, 150, 352), outline=(120, 110, 100), width=6); d.line((143, 345, 165, 367), fill=(120, 110, 100), width=7)
        if cursor:
            shown = bar_text(d, query[:typed]); fnt = SEARCH
        else:
            shown = query[:typed]; fnt = bar_font(d, shown)
        d.text((TX, 330 - fnt.size // 2 - 4), shown, font=fnt, fill=INK)
        if cursor:
            lx = TX + d.textlength(shown, font=SEARCH) + 6; d.rectangle((lx, 300, lx + 5, 366), fill=STAMP)
        y = BAR[3] + 40
        if result:
            y = answer_block(d, y, result)
        d.text((70, y + 10), 'Recent searches', font=bold(F('Karla.ttf', 34), 800), fill=(140, 130, 120)); y += 70
        for h in reversed(history):
            hl = balanced_wrap(d, h, HIST, W - 230, 50)
            d.ellipse((80, y + 6, 116, y + 42), outline=(170, 160, 150), width=4); d.line((98, y + 14, 98, y + 26), fill=(170, 160, 150), width=4); d.line((98, y + 26, 108, y + 32), fill=(170, 160, 150), width=4)
            for k, l in enumerate(hl):
                d.text((150, y + k * 62), l, font=HIST, fill=(110, 100, 90))
            y += 62 * len(hl) + 40
            if y > H - 120: break
        return im

    frames, events, t, history, n = [], [], 0.4, [], 0
    open_typed = spec.get('open_typed', 0)   # open mid-typing: frame 1 already shows this share of the first query
    if open_typed or spec.get('open_on_result'):
        t = 0.0
    else:
        frame('', 0, []).save(f'{work}/k0000.png'); frames.append((f'{work}/k0000.png', 0.4))
    qs = spec['queries']; end_t = None
    for qi, q in enumerate(qs):
        text = T(q['line'], spec); last = qi == len(qs) - 1; step = 2 if len(text) > 40 else 1
        c0 = max(step, int(len(text) * open_typed)) if (qi == 0 and open_typed) else step
        if qi == 0 and spec.get('open_on_result') and not last:   # frame 1 is the first joke, query and answer together
            res = T(q['result'], spec) if q.get('result') else None
            n += 1; p = f'{work}/k{n:04d}.png'; frame(text, len(text), history, res, cursor=False).save(p); frames.append((p, q['hold'])); t += q['hold']
            events.append((0.0, 'sting')); history.append(text); continue
        for c in range(c0, len(text) + step, step):
            n += 1; p = f'{work}/k{n:04d}.png'; frame(text, min(c, len(text)), history).save(p)
            frames.append((p, 0.05)); events.append((t, 'key')); t += 0.05
        n += 1; p = f'{work}/k{n:04d}.png'; frame(text, len(text), history, cursor=False).save(p); frames.append((p, 0.35)); t += 0.35
        res = T(q['result'], spec) if q.get('result') else None
        if last:
            events.append((t - 0.1, 'scratch')); end_t = t
            bg = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(bg, 'RGBA')
            d.text((70, 150), 'Search', font=bold(F('Karla.ttf', 64), 800), fill=INK); bg.paste(AVA, (W - 170, 130), AVA)
            d.rounded_rectangle(BAR, 70, fill=(255, 255, 255), outline=(205, 195, 180), width=4)
            d.ellipse((100, 302, 150, 352), outline=(120, 110, 100), width=6); d.line((143, 345, 165, 367), fill=(120, 110, 100), width=7)
            fnt = bar_font(d, text); d.text((TX, 330 - fnt.size // 2 - 4), text, font=fnt, fill=INK)
            y = BAR[3] + 40
            if res:
                y = answer_block(d, y, res)
            hold = spec['end'].get('hold', 5.0)
            frames_to_video(frames, f'{work}/typing.mp4')
            product_clip([spec['end_render']], f'{work}/end.mp4', hold, bg=bg, box=(60, y, W - 60, H - 60), end_png=f'{work}/end.png')
            join([f'{work}/typing.mp4', f'{work}/end.mp4'], f'{work}/picture.mp4'); t += hold
        else:
            events.append((t, 'sting'))
            n += 1; p = f'{work}/k{n:04d}.png'; frame(text, len(text), history, res, cursor=False).save(p); frames.append((p, q['hold'])); t += q['hold']
            history.append(text)
    sfx_mix(work, t, end_t, spec['music'], spec.get('music_level', 0.42), events)
    return mux(work, spec['id']), t


# ---------------------------------------------------------------- roast (carousel plus reel)
def roast(spec, work):
    """Carousel plus reel. With `frames`, each slide is a photo of the dog trolling you with the line
    in meme type over it (Krish, 3 Nov: "images that look like the dog is trolling them, like that
    classic troll meme image - but a dog"). The last slide is the real mug."""
    CW, CH = 1080, 1350; breed = spec['breed']
    native = _ui_v1(spec)
    MEME = F('Anton.ttf', 96)

    def meme(photo, text, w, h, pos='top'):
        """The photo filling w x h, with the line in meme type laid out for that frame (never cropped)."""
        im = Image.open(f'{FR}/{photo}').convert('RGB')
        r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        x, y = (im.width - w) // 2, (im.height - h) // 2; im = im.crop((x, y, x + w, y + h))
        if native:
            # A new edition keeps static meme text inside the house working
            # region. Old locks retain their exact original type and geometry.
            d = ImageDraw.Draw(im)
            font = bold(F('Karla.ttf', 54), 800)
            left, right = (132, 840) if h > 1500 else (90, 990)
            top = 320 if h > 1500 else 154
            lines = []; line = ''
            for word in text.split():
                trial = (line + ' ' + word).strip()
                if d.textlength(trial, font=font) > right - left - 48 and line:
                    lines.append(line); line = word
                else:
                    line = trial
            if line: lines.append(line)
            if len(lines) > 4 or any(d.textlength(line, font=font) > right-left-48 for line in lines):
                raise ValueError('split the meme beat; do not shrink the text')
            d.rounded_rectangle((left, top, right, top + len(lines)*64+28), 20, fill=(20,18,15))
            for i,line in enumerate(lines):
                d.text(((left+right-d.textlength(line,font=font))/2,top+8+i*64),line,font=font,fill='white')
            return im
        d = ImageDraw.Draw(im); size = 96
        while True:
            f = F('Anton.ttf', size); lines = balanced_wrap(d, text.upper(), f, w - 120, size)
            if (len(lines) <= 3 and max(d.textlength(l, font=f) for l in lines) <= w - 120) or size <= 60: break
            size -= 6
        lh = int(size * 1.12); top = 60 if pos == 'top' else h - 60 - lh * len(lines) - int(h * 0.04)
        if pos == 'bottom' and h > w * 1.5: top = int(h * 0.76) - lh * len(lines)   # end above the reel's caption and username zone
        if pos == 'top' and h > w * 1.5: top = int(h * 0.12)   # clear of the app's own top bar in a reel
        for i, l in enumerate(lines):
            tw = d.textlength(l, font=f)
            d.text(((w - tw) / 2, top + i * lh), l, font=f, fill=(255, 255, 255), stroke_width=max(4, size // 14), stroke_fill=(0, 0, 0))
        return im
    texts = [T(spec['title'], spec)] + [T(l, spec) for l in spec['lines']]
    pos = spec.get('text_pos', ['top'] * len(spec['frames']))
    slides = [meme(fr, tx, CW, CH, ps) for fr, tx, ps in zip(spec['frames'], texts, pos)]
    p = Image.open(f"{R}/{spec['render']}").convert('RGB')   # the real mug on its own backdrop tone: no panel
    tone = _border_color(p); im = Image.new('RGB', (CW, CH), tone)
    p.thumbnail((864, 1000) if native else (980, 1230), Image.LANCZOS); cp = _cutout(p, _border_color(p))
    im.paste(cp, ((CW - p.width) // 2, (CH - p.height) // 2), cp); slides.append(im)
    parts = []
    for i, s in enumerate(slides[:-1]):
        s.save(f'{work}/slide{i + 1}.png')
        meme(spec['frames'][i], texts[i], W, H, pos[i]).save(f'{work}/v{i + 1}.png'); n = round(spec['durs'][i] * 30); out = f'{work}/v{i + 1}.mp4'
        vf = f'scale={W}:{H},fps=30,format=yuv420p' if native else f"scale=2160:3840,zoompan=z='min(zoom+0.0012,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps=30,format=yuv420p"
        run(['ffmpeg', '-y', '-loop', '1', '-i', f'{work}/v{i + 1}.png', '-vf', vf,
             '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out]); parts.append(out)
    slides[-1].save(f'{work}/slide{len(slides)}.png')
    options = {'box': (132,310,840,1110), 'critical_box': (132,310,840,1110)} if native else {}
    product_clip([spec['render']], f'{work}/end.mp4', spec['durs'][-1], end_png=f'{work}/end.png', **options); parts.append(f'{work}/end.mp4')
    join(parts, f'{work}/picture.mp4')
    starts = [sum(spec['durs'][:i]) for i in range(len(slides))]; total = sum(spec['durs'])
    booms = [(t + 0.02, 'boom') for t in starts[:-1]]
    sfx_mix(work, total, starts[-1], spec['music'], spec.get('music_level', 0.5), booms, soft_at=starts[len(slides) - 2])
    return mux(work, spec['id']), total


# ---------------------------------------------------------------- film
CAPB = bold(F('Karla.ttf', 54), 800)


def _cover(path, crop_top=0.0):
    im = Image.open(path).convert('RGB')
    if crop_top: im = im.crop((0, int(im.height * crop_top), im.width, im.height))
    r = max(W / im.width, H / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def _caption(im, text, y=1300):   # Legacy geometry only; not a platform safety guarantee.
    if not text: return im
    d = ImageDraw.Draw(im, 'RGBA'); lines = balanced_wrap(d, text, CAPB, W - 200, 54); lh = 70; h = lh * len(lines) + 44
    d.rounded_rectangle((60, y, W - 60, y + h), 24, fill=(20, 18, 15, 185))
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=CAPB); d.text(((W - tw) / 2, y + 22 + i * lh), l, font=CAPB, fill=(255, 255, 255))
    return im


def film(spec, work):
    parts, t0 = [], 0.0
    native = _ui_v1(spec)
    draw_caption = (lambda im, text, y: ui_layout.caption(im, text, CAPB, y)) if native else _caption
    default_y = ui_layout.SUBTITLES[1] if native else 1300
    for i, s in enumerate(spec['shots']):
        dur = s['until'] - t0; t0 = s['until']; cap = T(s['line'], spec) if s.get('line') else None
        out = f'{work}/s{i:02d}.mp4'
        if s.get('render'):   # a real render mid-film: moving, captioned, no badge
            options = {'box': (132,310,840,930), 'critical_box': (132,310,840,930)} if native else {}
            product_clip([s['render']], out, dur, overlay=lambda im, t, c=cap, y=s.get('cap_y', default_y): draw_caption(im, c, y), end_png=f'{work}/s{i:02d}.png', **options)
        else:
            im = draw_caption(_cover(f"{FR}/{s['frame']}", s.get('crop_top', 0)), cap, s.get('cap_y', default_y))
            png = f'{work}/s{i:02d}.png'; n = round(dur * 30)
            if s.get('pull'):   # a hook: open tight on the subject, then pull back to the whole picture; the caption stays still
                z0, (fx, fy) = s['pull']['zoom'], s['pull']['focus']
                _cover(f"{FR}/{s['frame']}", s.get('crop_top', 0)).save(png)
                cap_png = f'{work}/s{i:02d}_cap.png'; draw_caption(Image.new('RGBA', (W, H), (0, 0, 0, 0)), cap, s.get('cap_y', default_y)).save(cap_png)
                z = f"max(1,{z0}-({z0}-1)*min(1,on/{max(1, round(n * 0.8))}))"
                run(['ffmpeg', '-y', '-loop', '1', '-i', png, '-loop', '1', '-i', cap_png, '-filter_complex',
                     f"[0]scale=2160:3840,zoompan=z='{z}':x='max(0,min(iw-iw/zoom,{fx}*iw-iw/zoom/2))':y='max(0,min(ih-ih/zoom,{fy}*ih-ih/zoom/2))':d={n}:s={W}x{H}:fps=30[v];[v][1]overlay=0:0:shortest=1,format=yuv420p",
                     '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out])
                parts.append(out); continue
            if native:
                # Move the clean picture only. Scaling baked captions also scales
                # their measured bounds beyond the placement's working region.
                _cover(f"{FR}/{s['frame']}", s.get('crop_top', 0)).save(png)
                cap_png = f'{work}/s{i:02d}_cap.png'
                draw_caption(Image.new('RGBA', (W, H)), cap, s.get('cap_y', default_y)).save(cap_png)
                run(['ffmpeg', '-y', '-loop', '1', '-i', png, '-loop', '1', '-i', cap_png, '-filter_complex',
                     f"[0]scale=2160:3840,zoompan=z='min(zoom+0.0007,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps=30[v];[v][1]overlay=0:0:shortest=1,format=yuv420p",
                     '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out])
                parts.append(out); continue
            im.save(png)
            run(['ffmpeg', '-y', '-loop', '1', '-i', png, '-vf', f"scale=2160:3840,zoompan=z='min(zoom+0.0007,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps=30,format=yuv420p",
                 '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out])
        parts.append(out)
    end_t = t0; hold = spec['end'].get('hold', 4.2); total = end_t + hold
    end_clip(spec, work, spec['end']['renders'], hold); parts.append(f'{work}/end.mp4')
    join(parts, f'{work}/picture.mp4')
    sfx_mix(work, total, end_t, spec['music'], spec.get('music_level', 0.2), [tuple(e) for e in spec.get('sfx', [])], voice=spec['voice'])
    return mux(work, spec['id']), total


def still_post(spec, work):
    import still
    folder, n = still.build(spec, work, T, FR, R, bold(F('Karla.ttf', 54 if spec['aspect'] == '4:5' else 50), 800))
    return folder, n


TEMPLATES = {'chat': chat, 'search': search, 'roast': roast, 'film': film, 'still': still_post}

if __name__ == '__main__':
    preview = '--preview' in sys.argv  # build a held post so Krish can judge its proposed lines in place; never posted
    for p in [a for a in sys.argv[1:] if not a.startswith('--')]:
        spec = json.load(open(p, encoding='utf-8'))
        probs, _ = lock.check(spec)
        if probs and not preview:
            print(f"{spec['id']}: held before building ({len(probs)} problem(s)); run lock.py check"); continue
        work = f"{OUTDIR}/{spec['id']}"; os.makedirs(work, exist_ok=True)
        f, t = TEMPLATES[spec['template']](spec, work); print(f, round(t, 2))
