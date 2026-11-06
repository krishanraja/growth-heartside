"""Shared helpers for the post factory: type, emoji, avatars, product end cards, video assembly.

Assets live outside git (this repository is public and the music is licensed). Point
HEARTSIDE_ASSETS at a folder holding renders/ (the live store's renders), frames/
(generated key frames), audio/ (licensed music, SFX and voice reads) and fonts/
(Fraunces, Karla, Courier Prime, all OFL). It defaults to local/assets/library.
"""
import itertools, math, os, re, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from textfit import EMOJI_RE, runs, text_width, wrap_rich, balanced_wrap, lone_word

LIB = os.path.abspath(os.environ.get('HEARTSIDE_ASSETS', os.path.join(os.path.dirname(__file__), '..', 'local', 'assets', 'library')))
OUTDIR = os.path.abspath(os.environ.get('HEARTSIDE_OUT', os.path.join(os.path.dirname(__file__), '..', 'local', 'media', 'factory')))
A = LIB + '/fonts'; R = LIB + '/renders'; FR = LIB + '/frames'; AU = LIB + '/audio'
W, H = 1080, 1920
CREAM, INK, STAMP, PAPER = (246, 241, 231), (36, 32, 27), (184, 50, 42), (255, 253, 248)
F = lambda f, s: ImageFont.truetype(f'{A}/{f}', s)
emoji_font = f'{A}/NotoColorEmoji.ttf'
EMO = ImageFont.truetype(emoji_font if os.path.isfile(emoji_font) else '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)


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


def avatar(render, center, r=130, size=88):
    im = Image.open(f'{R}/{render}').convert('RGB')
    cx, cy = center
    crop = im.crop((cx - r, cy - r, cx + r, cy + r)).resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new('RGBA', (size, size)); out.paste(crop, (0, 0), mask)
    return out


def _ease_back(p):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def _layout(n, box):
    x0, y0, x1, y1 = box
    if n == 1:
        return [box]
    cols = 2; rows = (n + 1) // 2; gap = 30
    cw = (x1 - x0 - gap) // 2; ch = (y1 - y0 - gap * (rows - 1)) // rows
    out = []
    for i in range(n):
        r, c = divmod(i, cols)
        if n % 2 and i == n - 1:
            out.append(((x0 + x1 - cw) // 2, y0 + r * (ch + gap), (x0 + x1 + cw) // 2, y0 + r * (ch + gap) + ch))
        else:
            out.append((x0 + c * (cw + gap), y0 + r * (ch + gap), x0 + c * (cw + gap) + cw, y0 + r * (ch + gap) + ch))
    return out


def _border_color(img):
    import numpy as np
    a = np.asarray(img.convert('RGB'), dtype=float); e = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(e, axis=0))


def _cutout(img, tone, tol=10):
    """Make the render's own plain backdrop transparent, only where it touches the image edge, so
    the mug, its painting and its shadow keep every pixel and no box shows (review, 2 Nov)."""
    import numpy as np
    a = np.asarray(img.convert('RGB'), dtype=float)
    dist = np.abs(a - np.array(tone, dtype=float)).max(axis=2)
    near = Image.fromarray(((dist <= tol) * 255).astype('uint8'))
    w, h = near.size
    for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        if near.getpixel(xy) == 255:
            ImageDraw.floodfill(near, xy, 128)
    region = np.asarray(near) == 128
    alpha = np.where(region, np.clip((dist - 2) / (tol - 2), 0, 1) * 255, 255).astype('uint8')
    out = img.convert('RGBA'); out.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.2)))
    return out


def _feather(size, r=36):
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rectangle((r, r, size[0] - r, size[1] - r), fill=255)
    return m.filter(ImageFilter.GaussianBlur(r / 2))


def product_clip(renders, out_mp4, dur, bg=None, box=(60, 160, W - 60, 1760), overlay=None, end_png=None, fps=30, critical_box=None):
    """The real store renders, pixels untouched, moving like a phone video. A scene render
    (portrait, blanket) fills the frame with a slow push-in. A mug sits on its own backdrop colour
    with feathered edges, drops in with a small settle, then floats and sways while the camera
    pushes in. No badge, no text (Krish, 2 Nov: organic posts; the mugs should animate).
    `overlay(img, t)` may draw a caption."""
    imgs = [Image.open(f'{R}/{p}').convert('RGB') for p in renders]
    scene = len(renders) == 1 and 'mug' not in renders[0] and bg is None
    n = round(dur * fps)
    proc = subprocess.Popen(['ffmpeg', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out_mp4],
                            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if scene:
        src = imgs[0]; r0 = max(W / src.width, H / src.height)
        back = src.resize((round(src.width * r0), round(src.height * r0)), Image.BICUBIC)
        bx, by = (back.width - W) // 2, (back.height - H) // 2
        back = back.crop((bx, by, bx + W, by + H)).filter(ImageFilter.GaussianBlur(28))
        back = Image.blend(back, Image.new('RGB', (W, H), (20, 18, 15)), 0.25)
        fit = min((W - 60) / src.width, 1500 / src.height)
        if critical_box:
            x0, y0, x1, y1 = critical_box
            fit = min((x1 - x0) / src.width, (y1 - y0) / src.height) / 1.08
    else:
        cols = [_border_color(i) for i in imgs]
        tone = tuple(sum(c[k] for c in cols) // len(cols) for k in range(3))
        if bg is not None:   # inside a UI (a search result): the product sits in its own card
            base = bg.copy(); ImageDraw.Draw(base).rounded_rectangle(box, 30, fill=tone)
        else:
            base = Image.new('RGB', (W, H), tone)
        items = []
        for img, (x0, y0, x1, y1) in zip(imgs, _layout(len(imgs), box)):
            p = img.copy(); p.thumbnail((int((x1 - x0) * 0.98), int((y1 - y0) * 0.98)), Image.LANCZOS)
            p = _cutout(p, _border_color(p))
            items.append((p, ((x0 + x1) // 2, (y0 + y1) // 2)))
    last = None
    for f in range(n):
        t = f / fps
        if scene:
            p = min(t / 0.5, 1); s = fit * (0.94 + 0.06 * _ease_back(p)) * (1.0 + 0.05 * t / max(dur, 0.1))
            im = src.resize((round(src.width * s), round(src.height * s)), Image.BICUBIC)
            frame = back.copy()
            if critical_box:
                cx, cy = (critical_box[0] + critical_box[2]) / 2, (critical_box[1] + critical_box[3]) / 2
                frame.paste(im, (round(cx - im.width / 2), round(cy - im.height / 2)))
            else:
                frame.paste(im, ((W - im.width) // 2, (H - im.height) // 2 - 60))
        else:
            frame = base.copy(); push = 1 + 0.035 * t / max(dur, 0.1)
            for i, (img, (cx, cy)) in enumerate(items):
                p = min(max((t - i * 0.14) / 0.6, 0), 1)
                if p <= 0:
                    continue
                s = (0.82 + 0.18 * _ease_back(p)) * push
                ang = 1.4 * math.sin(2 * math.pi * t / 3.2 + i) * p
                dy = (1 - _ease_back(p)) * 260 + 7 * math.sin(2 * math.pi * t / 2.6 + i) * p
                im = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BICUBIC).rotate(ang, Image.BICUBIC, expand=True)
                frame.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2 + dy)), im)
        if overlay:
            frame = overlay(frame, t)
        proc.stdin.write(frame.convert('RGB').tobytes()); last = frame
    proc.stdin.close(); proc.wait()
    if end_png:
        last.save(end_png)
    return out_mp4


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
         '-frames:v', str(round(sum(seconds for _, seconds in frames) * fps)),
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out_noaudio])
