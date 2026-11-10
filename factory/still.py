"""The still template: one photo or a carousel of photos, each with its line set above it.

Built for the meme and share posts of a sprint (docs/plans/2026-11-10-sprint-120.md), where a spec per
post is generated from the sprint manifest by factory/sprint.py. Every word still comes from
bank/lines.json by id and every product image from bank/renders.json, so nothing here takes free text.

Layout rules, each from Krish's floor (python3 growth.py floor --format still):
- text-clear-of-faces: the line sits in a band above the photo, never on it, so no word can cover a
  dog's eyes or the action. `focus_y` (0 top to 1 bottom) picks which part of the photo the crop keeps.
- no-badges / real-product: an optional last slide shows the store's own render, scaled only, on a
  plain ground, with no words, badge or call to action.
- A line that does not fit three readable lines is refused: rewrite it, never shrink it.
"""
from PIL import Image, ImageDraw, ImageOps

SIZES = {'4:5': (1080, 1350), '9:16': (1080, 1920)}
# 9:16 is TikTok photo mode: words and the dog stay inside its tested content region
# (engine/creative_ui.CRITICAL); the feed has no overlaid controls.
TEXT_BOX = {'4:5': (72, 1008), '9:16': (108, 864)}
BAND_TOP = {'4:5': 44, '9:16': 288}
# TikTok photo mode lays its caption and controls over the lower frame, so the photo stops above them.
PHOTO_BOTTOM = {'4:5': 1350, '9:16': 1400}
PAPER, INK = (250, 247, 241), (24, 22, 19)
GROUND = (237, 231, 220)
LINE_GAP = 1.22
MAX_LINES = 3


def wrap(draw, text, font, width):
    """The fewest lines that fit, split as evenly as possible; never one word alone on the last line.

    Raises if the line needs more than MAX_LINES: rewrite it, never shrink it.
    """
    words = text.split()
    w = lambda ws: draw.textlength(' '.join(ws), font=font)
    for n in range(1, MAX_LINES + 1):
        best = None

        def split(start, left, acc):
            nonlocal best
            if left == 1:
                last = words[start:]
                if not last or w(last) > width or (n > 1 and len(last) < 2):
                    return
                lines = acc + [last]
                score = max(w(l) for l in lines) - min(w(l) for l in lines)
                if best is None or score < best[0]:
                    best = (score, [' '.join(l) for l in lines])
                return
            for end in range(start + 1, len(words) - left + 2):
                if w(words[start:end]) > width:
                    break
                split(end, left - 1, acc + [words[start:end]])
        split(0, n, [])
        if best:
            return best[1]
    raise ValueError(f'line does not fit {MAX_LINES} readable lines; rewrite it, do not shrink it: {text!r}')


def cover(photo, size, focus_y=0.5):
    """Scale to fill `size`, then crop, keeping the part of the photo `focus_y` names."""
    w, h = size
    r = max(w / photo.width, h / photo.height)
    im = photo.resize((round(photo.width * r), round(photo.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = round((im.height - h) * min(max(focus_y, 0.0), 1.0))
    return im.crop((x, y, x + w, y + h))


def slide(photo, text, font, aspect, focus_y=0.5, style='band'):
    """One slide: the line in a paper band, the photo filling everything below it."""
    W, H = SIZES[aspect]
    canvas = Image.new('RGB', (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    band_bottom = 0
    if text and style == 'band':
        left, right = TEXT_BOX[aspect]
        lines = wrap(draw, text, font, right - left)
        size = font.size if hasattr(font, 'size') else 50
        lh = round(size * LINE_GAP)
        top = BAND_TOP[aspect]
        for i, l in enumerate(lines):
            draw.text(((left + right - draw.textlength(l, font=font)) / 2, top + i * lh), l, font=font, fill=INK)
        band_bottom = top + len(lines) * lh + 36
    elif text:
        raise ValueError('a line needs the band style; style none carries no words')
    pic = cover(photo.convert('RGB'), (W, PHOTO_BOTTOM[aspect] - band_bottom), focus_y)
    canvas.paste(pic, (0, band_bottom))
    return canvas


def product_slide(render, aspect, margin=90):
    """The real store render, scaled only (AGENTS.md rule 4), centred on a plain ground. No words."""
    W, H = SIZES[aspect]
    canvas = Image.new('RGB', (W, H), GROUND)
    fitted = ImageOps.contain(render.convert('RGB'), (W - 2 * margin, H - 2 * margin), Image.LANCZOS)
    canvas.paste(fitted, ((W - fitted.width) // 2, (H - fitted.height) // 2))
    return canvas


def build(spec, work, resolve, frames_dir, renders_dir, font):
    """Write slide-01.png ... into `work`; returns (folder, slide count)."""
    import os
    os.makedirs(work, exist_ok=True)
    for f in os.listdir(work):
        if f.startswith('slide-') and f.endswith('.png'):
            os.remove(os.path.join(work, f))
    n = 0
    for sl in spec['slides']:
        n += 1
        text = resolve(sl['line'], spec) if sl.get('line') else ''
        im = slide(Image.open(f"{frames_dir}/{sl['frame']}"), text, font, spec['aspect'],
                   sl.get('focus_y', 0.5), sl.get('style', 'band'))
        im.save(f'{work}/slide-{n:02d}.png', optimize=True)
    for r in spec.get('end', {}).get('renders', [])[:1]:
        n += 1
        product_slide(Image.open(f'{renders_dir}/{r}'), spec['aspect']).save(f'{work}/slide-{n:02d}.png', optimize=True)
    return work, n
