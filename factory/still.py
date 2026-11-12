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
import json, os, sys
from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.creative_ui import (CRITICAL, HOOK, FEED_MARGIN, REVISION,
                                TIKTOK_PHOTO_BACKGROUND, TIKTOK_PHOTO_TEXT)

SIZES = {'4:5': (1080, 1350), '9:16': (1080, 1920)}
# Corpus profile (engine/creative_ui.py). 9:16 is TikTok photo mode: the line sits in the opening-hook
# region and the photo inside the critical box, on ink so TikTok's white controls stay visible (6 Nov
# Buffer preview). 4:5 is a feed slide: a 90 px design margin, the photo full bleed below the band.
TEXT_BOX = {'4:5': (FEED_MARGIN, 1080 - FEED_MARGIN), '9:16': (HOOK[0], HOOK[2])}
BAND_TOP = {'4:5': FEED_MARGIN, '9:16': HOOK[1]}
PHOTO_BOX = {'4:5': (0, None, 1080, 1350), '9:16': (CRITICAL[0], None, CRITICAL[2], CRITICAL[3])}
PAPER, INK = (250, 247, 241), (24, 22, 19)
GROUND = (237, 231, 220)
GROUNDS = {'4:5': (PAPER, INK), '9:16': (TIKTOK_PHOTO_BACKGROUND, TIKTOK_PHOTO_TEXT)}
LINE_GAP = 1.22
MAX_LINES = 3


def wrap(draw, text, font, width):
    """The fewest lines that fit, split as evenly as possible; never one word alone on the last line.

    Raises if the line needs more than MAX_LINES: rewrite it, never shrink it. A newline in the text is a
    deliberate break (a two-speaker meme: "Me: ..." then "Him: ..."): each part wraps on its own.
    """
    if '\n' in text:
        out = [l for part in text.split('\n') if part.strip() for l in wrap(draw, part, font, width)]
        if len(out) > MAX_LINES:
            raise ValueError(f'line does not fit {MAX_LINES} readable lines; rewrite it, do not shrink it: {text!r}')
        return out
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


def slide(photo, text, font, aspect, focus_y=0.5, style='band', layout=None, first=False):
    """One slide: the line in a band, the photo filling the photo box below it."""
    W, H = SIZES[aspect]
    ground, ink = GROUNDS[aspect]
    canvas = Image.new('RGB', (W, H), ground)
    draw = ImageDraw.Draw(canvas)
    band_bottom = 0 if aspect == '4:5' else CRITICAL[1]
    if text and style == 'band':
        left, right = TEXT_BOX[aspect]
        lines = wrap(draw, text, font, right - left)
        size = font.size if hasattr(font, 'size') else 50
        lh = round(size * LINE_GAP)
        top = BAND_TOP[aspect]
        for i, l in enumerate(lines):
            draw.text(((left + right - draw.textlength(l, font=font)) / 2, top + i * lh), l, font=font, fill=ink)
        band_bottom = top + len(lines) * lh + 36
        if layout is not None:
            layout['elements'].append({'role': 'hook' if first else 'text', 'box': [left, top, right, top + len(lines) * lh],
                                       'start': 0, 'end': 0, 'text': text})
    elif text:
        raise ValueError('a line needs the band style; style none carries no words')
    x0, _, x1, y1 = PHOTO_BOX[aspect]
    if y1 - band_bottom < 300:
        raise ValueError('the line leaves too little room for the photo; rewrite it shorter')
    pic = cover(photo.convert('RGB'), (x1 - x0, y1 - band_bottom), focus_y)
    canvas.paste(pic, (x0, band_bottom))
    if layout is not None:
        # In 9:16 the photo is the dog's face and the action: critical content inside the box.
        layout['elements'].append({'role': 'picture', 'box': [x0, band_bottom, x1, y1], 'start': 0, 'end': 0,
                                   **({'focus': [x0, band_bottom, x1, y1]} if aspect == '9:16' else {})})
    return canvas


def product_slide(render, aspect, margin=FEED_MARGIN, layout=None):
    """The real store render, scaled only (AGENTS.md rule 4), centred on a plain ground. No words.
    In 9:16 it sits inside the critical box, clear of the platform controls."""
    W, H = SIZES[aspect]
    canvas = Image.new('RGB', (W, H), GROUND)
    box = (margin, margin, W - margin, H - margin) if aspect == '4:5' else CRITICAL
    fitted = ImageOps.contain(render.convert('RGB'), (box[2] - box[0], box[3] - box[1]), Image.LANCZOS)
    x, y = (box[0] + box[2] - fitted.width) // 2, (box[1] + box[3] - fitted.height) // 2
    canvas.paste(fitted, (x, y))
    if layout is not None:
        layout['elements'].append({'role': 'product', 'box': [x, y, x + fitted.width, y + fitted.height], 'start': 0, 'end': 0})
    return canvas


def _layout(aspect):
    return {'profile': REVISION, 'canvas': list(SIZES[aspect]), 'duration': 0, 'elements': []}


def build(spec, work, resolve, frames_dir, renders_dir, font):
    """Write slide-01.png ... into `work`, each with its slide-NN.layout.json; returns (folder, slide count)."""
    os.makedirs(work, exist_ok=True)
    for f in os.listdir(work):
        if f.startswith('slide-') and f.endswith('.png'):
            os.remove(os.path.join(work, f))
    for f in os.listdir(work):
        if f.startswith('slide-') and f.endswith('.layout.json'):
            os.remove(os.path.join(work, f))
    n = 0
    for sl in spec['slides']:
        n += 1
        text = resolve(sl['line'], spec) if sl.get('line') else ''
        layout = _layout(spec['aspect'])
        im = slide(Image.open(f"{frames_dir}/{sl['frame']}"), text, font, spec['aspect'],
                   sl.get('focus_y', 0.5), sl.get('style', 'band'), layout, first=n == 1)
        im.save(f'{work}/slide-{n:02d}.png', optimize=True)
        json.dump(layout, open(f'{work}/slide-{n:02d}.layout.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    for r in spec.get('end', {}).get('renders', [])[:1]:
        n += 1
        layout = _layout(spec['aspect'])
        product_slide(Image.open(f'{renders_dir}/{r}'), spec['aspect'], layout=layout).save(f'{work}/slide-{n:02d}.png', optimize=True)
        json.dump(layout, open(f'{work}/slide-{n:02d}.layout.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    return work, n
