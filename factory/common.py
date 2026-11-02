"""Shared helpers for the post factory: type, emoji, avatars, product end cards, video assembly.

Assets live outside git (this repository is public and the music is licensed). Point
HEARTSIDE_ASSETS at a folder holding renders/ (the live store's renders), frames/
(generated key frames), audio/ (licensed music, SFX and voice reads) and fonts/
(Fraunces, Karla, Courier Prime, all OFL). It defaults to local/assets/library.
"""
import os, re, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont

LIB = os.path.abspath(os.environ.get('HEARTSIDE_ASSETS', os.path.join(os.path.dirname(__file__), '..', 'local', 'assets', 'library')))
OUTDIR = os.path.abspath(os.environ.get('HEARTSIDE_OUT', os.path.join(os.path.dirname(__file__), '..', 'local', 'media', 'factory')))
A = LIB + '/fonts'; R = LIB + '/renders'; FR = LIB + '/frames'; AU = LIB + '/audio'
W, H = 1080, 1920
CREAM, INK, STAMP, PAPER = (246, 241, 231), (36, 32, 27), (184, 50, 42), (255, 253, 248)
F = lambda f, s: ImageFont.truetype(f'{A}/{f}', s)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
EMOJI_RE = re.compile('([\U0001F300-\U0001FAFF☀-➿☕])')


def bold(f, wght):
    try:
        f.set_variation_by_axes([wght])
    except Exception:
        pass
    return f


BODY = bold(F('Karla.ttf', 44), 500)
NAME = bold(F('Karla.ttf', 30), 800)
TITLE = bold(F('Karla.ttf', 40), 800)
MONO = F('CourierPrime.ttf', 46)
SUPER = F('Fraunces.ttf', 80)
try:
    SUPER.set_variation_by_axes([72, 650, 50, 0])
except Exception:
    pass
SMALL = bold(F('Karla.ttf', 32), 700)


def emoji_img(ch, size):
    im = Image.new('RGBA', (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=EMO, embedded_color=True)
    im = im.crop(im.getbbox() or (0, 0, 1, 1))
    r = size / max(im.height, 1)
    return im.resize((max(1, round(im.width * r)), size), Image.LANCZOS)


def runs(text):
    return [p for p in EMOJI_RE.split(text) if p]


def text_width(d, text, font, size):
    w = 0
    for p in runs(text):
        if EMOJI_RE.fullmatch(p):
            w += size + 6
        else:
            w += d.textlength(p, font=font)
    return w


def draw_rich(im, xy, text, font, size, fill):
    d = ImageDraw.Draw(im)
    x, y = xy
    for p in runs(text):
        if EMOJI_RE.fullmatch(p):
            e = emoji_img(p, size)
            im.paste(e, (int(x), int(y + 4)), e)
            x += e.width + 6
        else:
            d.text((x, y), p, font=font, fill=fill)
            x += d.textlength(p, font=font)


def wrap_rich(d, text, font, size, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if text_width(d, t, font, size) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def avatar(render, center, r=130, size=88):
    im = Image.open(f'{R}/{render}').convert('RGB')
    cx, cy = center
    crop = im.crop((cx - r, cy - r, cx + r, cy + r)).resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new('RGBA', (size, size)); out.paste(crop, (0, 0), mask)
    return out


def product_card(renders, super_text, sub=None):
    """The real store renders, untouched, each labelled Example, on cream."""
    im = Image.new('RGB', (W, H), CREAM)
    d = ImageDraw.Draw(im, 'RGBA')
    lines = textwrap.wrap(super_text, 18)
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=SUPER); d.text(((W - tw) / 2, 180 + i * 98), l, font=SUPER, fill=INK)
    top = 200 + 98 * len(lines) + 40
    n = len(renders)
    if n == 1:
        boxes = [(70, top, W - 70, 1700)]
    else:
        boxes = []
        cols = 2; cw = (W - 70 * 2 - 30) // 2; ch = (1700 - top - 30 * ((n + 1) // 2 - 1)) // ((n + 1) // 2)
        for i in range(n):
            r, c = divmod(i, cols)
            if n % 2 and i == n - 1:
                boxes.append(((W - cw) // 2, top + r * (ch + 30), (W + cw) // 2, top + r * (ch + 30) + ch))
            else:
                boxes.append((70 + c * (cw + 30), top + r * (ch + 30), 70 + c * (cw + 30) + cw, top + r * (ch + 30) + ch))
    for path, (x0, y0, x1, y1) in zip(renders, boxes):
        p = Image.open(f'{R}/{path}').convert('RGB'); p.thumbnail((x1 - x0, y1 - y0), Image.LANCZOS)
        px, py = x0 + (x1 - x0 - p.width) // 2, y0 + (y1 - y0 - p.height) // 2
        im.paste(p, (px, py))
        d.rounded_rectangle((px + 16, py + 16, px + 180, py + 66), 8, fill=(20, 18, 15, 190))
        d.text((px + 32, py + 22), 'EXAMPLE', font=SMALL, fill=(255, 255, 255))
    if sub:
        tw = d.textlength(sub, font=SMALL); d.text(((W - tw) / 2, 1740), sub, font=SMALL, fill=INK)
    tw = d.textlength('heartside.io', font=SMALL); d.text(((W - tw) / 2, 1800), 'heartside.io', font=SMALL, fill=STAMP)
    return im


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def frames_to_video(frames, out_noaudio, fps=30):
    """frames: list of (png_path, seconds). Hard cuts, no zoom (UI screens)."""
    lst = out_noaudio + '.txt'
    with open(lst, 'w') as fh:
        for p, s in frames:
            fh.write(f"file '{p}'\nduration {s:.3f}\n")
        fh.write(f"file '{frames[-1][0]}'\n")
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', f'fps={fps},format=yuv420p,scale={W}:{H}',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out_noaudio])
