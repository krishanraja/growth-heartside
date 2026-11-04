#!/usr/bin/env python3
"""Swap a still opener in a finished master for its approved motion clip.

    python3 factory/splice.py MASTER OUT PLAN.json

PLAN.json is a list of shots to replace, each
{"start": 0, "dur": 2.4, "clip": "path.mp4", "clip_in": 0, "clip_dur": 2.4,
 "text": "...", "style": "meme"|"caption", "cap_y": 1300, "pos": "top"}.
Each replaces the master's video from start to start+dur with CLIP from clip_in. When clip_dur
(the clip's passing window) is shorter than dur, the clip is slowed to fit (at most 1.3x).
- The clip is scaled and cropped to 1080x1920 (Lanczos, a light sharpen).
- The shot's words are burned back on, drawn exactly as the factory draws them:
  - `meme`: Anton, white with a black stroke, as roast() lays it out;
  - `caption`: Karla 800 in the dark rounded box, as _caption() lays it out.
- The rest of the master's video and the whole audio track are kept byte for byte (stream copy), so the locked voice, music and timing are unchanged.

Fonts come from HEARTSIDE_ASSETS/fonts, as for build.py (Anton, Karla, Fraunces, Courier Prime; all OFL).

The output is a candidate. It replaces a locked reel only after Krish locks it, and it must pass `factory/audit.py` and `factory/lock.py media` first.
"""
import argparse, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw  # noqa: E402
from common import F, bold, W, H  # noqa: E402
from textfit import balanced_wrap  # noqa: E402


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"{' '.join(cmd[:3])}…: {r.stderr[-600:]}")
    return r.stdout


def meme_layer(text, pos='top'):
    """Transparent 1080x1920 layer with the roast title, laid out as build.roast().meme()."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); size = 96
    while True:
        f = F('Anton.ttf', size); lines = balanced_wrap(d, text.upper(), f, W - 120, size)
        if (len(lines) <= 3 and max(d.textlength(l, font=f) for l in lines) <= W - 120) or size <= 60:
            break
        size -= 6
    lh = int(size * 1.12)
    top = int(H * 0.12) if pos == 'top' else int(H * 0.76) - lh * len(lines)   # bottom text ends above the reel's caption zone, as build.roast()
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=f)
        d.text(((W - tw) / 2, top + i * lh), l, font=f, fill=(255, 255, 255, 255),
               stroke_width=max(4, size // 14), stroke_fill=(0, 0, 0, 255))
    return im


def caption_layer(text, y=1300):
    """Transparent layer with the film subtitle, laid out as build._caption()."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im, 'RGBA')
    capb = bold(F('Karla.ttf', 54), 800)
    lines = balanced_wrap(d, text, capb, W - 200, 54); lh = 70; h = lh * len(lines) + 44
    d.rounded_rectangle((60, y, W - 60, y + h), 24, fill=(20, 18, 15, 185))
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=capb); d.text(((W - tw) / 2, y + 22 + i * lh), l, font=capb, fill=(255, 255, 255, 255))
    return im


VF = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
      "unsharp=5:5:0.6:5:5:0.0")
ENC = ['-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', '30', '-pix_fmt', 'yuv420p']


def clip_segment(sh, out, t):
    dur = sh['dur']; cin = sh.get('clip_in', 0.0); cdur = sh.get('clip_dur', dur)
    stretch = dur / cdur
    if stretch > 1.3:
        raise SystemExit(f"{sh['clip']}: passing window {cdur}s cannot fill {dur}s (more than 1.3x)")
    vf = f"{VF},setpts={stretch:.4f}*PTS,fps=30,format=yuv420p"
    inputs = ['-ss', f'{cin:.3f}', '-t', f'{cdur:.3f}', '-i', sh['clip']]
    if sh.get('text'):
        layer = meme_layer(sh['text'], sh.get('pos', 'top')) if sh.get('style') == 'meme' else caption_layer(sh['text'], sh.get('cap_y', 1300))
        png = f'{t}/layer{sh["start"]}.png'; layer.save(png)
        run(['ffmpeg', '-y', *inputs, '-i', png, '-filter_complex', f'[0:v]{vf}[v];[v][1:v]overlay=0:0,format=yuv420p[o]',
             '-map', '[o]', '-t', f'{dur:.3f}', *ENC, out])
    else:
        run(['ffmpeg', '-y', *inputs, '-vf', vf, '-t', f'{dur:.3f}', *ENC, out])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('master'); ap.add_argument('out'); ap.add_argument('plan')
    a = ap.parse_args(argv)
    import json
    plan = sorted(json.load(open(a.plan)), key=lambda x: x['start'])
    total = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.master]))
    with tempfile.TemporaryDirectory() as t:
        parts, pos = [], 0.0
        for i, sh in enumerate(plan + [{'start': total, 'dur': 0}]):
            if sh['start'] - pos > 0.02:   # the master's own picture between replacements
                out = f'{t}/m{i:02d}.mp4'
                run(['ffmpeg', '-y', '-ss', f'{pos:.3f}', '-t', f'{sh["start"] - pos:.3f}', '-i', a.master, '-vf', 'fps=30', *ENC, out])
                parts.append(out)
            if sh['dur']:
                out = f'{t}/c{i:02d}.mp4'; clip_segment(sh, out, t); parts.append(out)
            pos = sh['start'] + sh['dur']
        with open(f'{t}/list.txt', 'w') as fh:
            fh.writelines(f"file '{p}'\n" for p in parts)
        run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', f'{t}/list.txt', '-c', 'copy', f'{t}/video.mp4'])
        run(['ffmpeg', '-y', '-i', f'{t}/video.mp4', '-i', a.master, '-map', '0:v', '-map', '1:a', '-c', 'copy',
             '-shortest', '-movflags', '+faststart', a.out])
    print(a.out)


if __name__ == '__main__':
    main()
