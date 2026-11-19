"""Still meme renderer: one photo, one line, the house meme look (Krish, 18 Nov: "whip up rapid still image memes").

A white band on top holds the line in black (the format dog meme pages use, legible in the feed and in a DM),
the photo fills the rest of a 1080x1350 (4:5) frame, cropped to fill, never stretched, and a small
@yourdoghasnotes mark sits bottom left on the photo so a reshare carries the account.

usage: python factory/meme.py PHOTO "LINE" OUT.jpg [--focus 0.5]
       python factory/meme.py --batch specs.json   (a list of {photo, line, out, focus?})
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'local/assets/library/fonts/Karla.ttf'
W, H = 1080, 1350
PAD = 56
MARK = '@yourdoghasnotes'


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(photo, line, out, focus=0.5):
    probe = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    size = 56
    while True:
        f = ImageFont.truetype(str(FONT), size)
        f.set_variation_by_axes([700])
        lines = wrap(probe, line, f, W - 2 * PAD)
        if len(lines) <= 3 or size <= 40:
            break
        size -= 4
    lh = round(size * 1.22)
    band = PAD + lh * len(lines) + PAD - round(size * 0.2)
    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    y = PAD - round(size * 0.12)
    for ln in lines:
        d.text((PAD, y), ln, font=f, fill=(16, 16, 16))
        y += lh
    src = Image.open(photo).convert('RGB')
    ph = H - band
    s = max(W / src.width, ph / src.height)
    im = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    x0 = (im.width - W) // 2
    y0 = round((im.height - ph) * focus)
    canvas.paste(im.crop((x0, y0, x0 + W, y0 + ph)), (0, band))
    mf = ImageFont.truetype(str(FONT), 26)
    mf.set_variation_by_axes([600])
    mark = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    m = ImageDraw.Draw(mark)
    m.text((PAD - 22 + 2, H - 58 + 2), MARK, font=mf, fill=(0, 0, 0, 110))
    m.text((PAD - 22, H - 58), MARK, font=mf, fill=(255, 255, 255, 215))
    canvas.paste(mark, (0, 0), mark)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=93)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--batch':
        for s in json.loads(Path(a[1]).read_text(encoding='utf-8')):
            print(render(s['photo'], s['line'], s['out'], s.get('focus', 0.5)))
    else:
        focus = float(a[a.index('--focus') + 1]) if '--focus' in a else 0.5
        print(render(a[0], a[1], a[2], focus))
