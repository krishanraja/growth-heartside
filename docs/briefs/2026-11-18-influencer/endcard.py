"""Premium end card for the influencer-parody films.

Krish, 18 Nov: "the final frame just needs to be a lot more premium and have the heartside icon on it with a
'your dog's gifts for you, link in bio' type CTA".

Burgundy brand ground (the official icon's own colour), the official icon unaltered (scaled only), the store's
painted render with pixels untouched (uniform scale and a 1.00 to 1.04 push-in only), a headline and the CTA,
all inside the critical box (120, 330, 820, 1180), centred.

usage: python endcard.py <film id> [<film id> ...]
Replaces the last `hold` seconds of local/media/studio/<id>/<id>_vo.mp4 and writes <id>_vo_card.mp4.
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
W, H, FPS = 1080, 1920, 30
BG = (158, 26, 69)          # sampled from heartside-icon-master.png
CREAM = (250, 243, 235)
BLUSH = (236, 196, 205)
ICON = ROOT / 'docs/brand/official/heartside-icon-master.png'
FONTS = ROOT / 'local/assets/library/fonts'
CX = 540
HEAD = "Your dog’s gift for you."
CTA = 'LINK IN BIO'
ICON_PX, ICON_Y = 146, 340
BOX_W, BOX_H, BOX_Y = 560, 640, 530      # product: x 260..820, y 530..1170
HEAD_Y, RULE_Y, CTA_Y = 1214, 1302, 1322


def spaced(d, cx, y, text, f, fill, track):
    w = sum(d.textlength(c, font=f) for c in text) + track * (len(text) - 1)
    x = cx - w / 2
    for c in text:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track


def ground():
    g = Image.new('RGB', (W, H), BG)
    glow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(glow).ellipse((CX - 520, 480, CX + 520, 1200), fill=70)
    g = Image.composite(Image.new('RGB', (W, H), (184, 46, 92)), g, glow.filter(ImageFilter.GaussianBlur(160)))
    edge = Image.new('L', (W, H), 90)
    ImageDraw.Draw(edge).ellipse((-260, -120, W + 260, H + 120), fill=0)
    return Image.composite(Image.new('RGB', (W, H), (96, 12, 40)), g, edge.filter(ImageFilter.GaussianBlur(220)))


def frames(render, hold):
    src = Image.open(render).convert('RGB')
    base = ground()
    ic = Image.open(ICON).convert('RGB').resize((ICON_PX, ICON_PX), Image.LANCZOS)
    mask = Image.new('L', (ICON_PX * 4, ICON_PX * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, ICON_PX * 4 - 1, ICON_PX * 4 - 1), fill=255)
    mask = mask.resize((ICON_PX, ICON_PX), Image.LANCZOS)
    ring = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((CX - ICON_PX // 2 - 5, ICON_Y - 5, CX + ICON_PX // 2 + 4, ICON_Y + ICON_PX + 4),
                                 outline=CREAM + (230,), width=3)
    text = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    t = ImageDraw.Draw(text)
    fh = ImageFont.truetype(str(FONTS / 'Fraunces.ttf'), 58)
    fh.set_variation_by_axes([72, 420, 50, 0])
    fc = ImageFont.truetype(str(FONTS / 'Karla.ttf'), 27)
    fc.set_variation_by_axes([600])
    t.text((CX - t.textlength(HEAD, font=fh) / 2, HEAD_Y), HEAD, font=fh, fill=CREAM)
    t.line((CX - 28, RULE_Y, CX + 28, RULE_Y), fill=BLUSH, width=2)
    spaced(t, CX, CTA_Y, CTA, fc, CREAM, 8)
    fit = min(BOX_W / src.width, BOX_H / src.height) / 1.045
    cy = BOX_Y + BOX_H / 2
    n = round(hold * FPS)
    for k in range(n):
        tt = k / FPS
        s = fit * (1 + 0.04 * k / max(n - 1, 1))
        im = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
        ox, oy = round(CX - im.width / 2), round(cy - im.height / 2)
        sh = Image.new('L', (W, H), 0)
        ImageDraw.Draw(sh).rectangle((ox + 6, oy + 22, ox + im.width + 6, oy + im.height + 26), fill=150)
        fr = Image.composite(Image.new('RGB', (W, H), (40, 4, 16)), base, sh.filter(ImageFilter.GaussianBlur(26)))
        fr.paste(im, (ox, oy))
        a_icon = min(1.0, max(0.0, (tt - 0.15) / 0.45))
        a_text = min(1.0, max(0.0, (tt - 0.45) / 0.5))
        if a_icon:
            rl = ring.copy()
            rl.putalpha(ring.getchannel('A').point(lambda v: int(v * a_icon)))
            fr.paste(rl, (0, 0), rl)
            fr.paste(ic, (CX - ICON_PX // 2, ICON_Y), mask.point(lambda v: int(v * a_icon)))
        if a_text:
            tl = text.copy()
            tl.putalpha(text.getchannel('A').point(lambda v: int(v * a_text)))
            fr.paste(tl, (0, 0), tl)
        yield fr


def build(fid):
    d = ROOT / 'local/media/studio' / fid
    b = json.loads((d / 'build.json').read_text(encoding='utf-8'))
    hold = b['end']['hold']
    render = ROOT / b['end']['render']
    vo = d / f'{fid}_vo.mp4'
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(vo)],
                               capture_output=True, text=True).stdout)
    body = round(dur - hold, 3)
    end = d / 'work' / 'end-premium.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264',
                          '-preset', 'medium', '-crf', '10', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-colorspace', 'bt709', str(end)], stdin=subprocess.PIPE)
    last = None
    for fr in frames(render, hold):
        p.stdin.write(fr.tobytes())
        last = fr
    p.stdin.close()
    p.wait()
    last.save(d / 'work' / 'end-premium.png')
    out = d / f'{fid}_vo_card.mp4'
    g = (f'[0:v]trim=end={body},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[a];'
         f'[1:v]setsar=1,fps={FPS},format=yuv420p[e];[a][e]concat=n=2:v=1:a=0,'
         'setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]')
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(vo), '-i', str(end), '-filter_complex', g,
                        '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17',
                        '-c:a', 'copy', '-movflags', '+faststart', str(out)], capture_output=True, text=True)
    print(fid, 'body', body, 'hold', hold, 'ok' if r.returncode == 0 else r.stderr[-500:])


if __name__ == '__main__':
    for fid in sys.argv[1:]:
        build(fid)
