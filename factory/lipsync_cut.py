"""Cut a silent 1080x1920 human-arms lip-sync reel from a timeline JSON (Sprint 120 batch 1, 10 Nov 2026).

    python3 factory/lipsync_cut.py TIMELINE.json

TIMELINE: {"out": path, "font": path to a bold sans (Inter Bold on the build machine),
  "premise": {"text", "y", "size", "until"},            the premise line over shot 1 (sound-off hook)
  "shots": [{"src": clip.mp4 or still.png, "in", "dur", "speed", "caption", "cap_y", "cap_size"}],
  "end": {"render": the store's own render, "dur"}}    held unaltered, scaled only, on its own ground colour

Captions are the sung line, white with a black outline, centred inside x108-972; cap_y is chosen shot by shot so
no word covers a face, the hands or the gag object (floor text-clear-of-faces). speed < 1 slows a trimmed clip so
only its clean window is used; a .png src gets a slow push-in. The reel is silent: the song is added in the app.
The end card carries no text (floor no-badges). Build inputs stay out of git (the repository is public).
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
tl = json.load(open(sys.argv[1])); tmp = tempfile.mkdtemp()
FONT = tl.get('font')
def font(size): return ImageFont.truetype(FONT, size)
def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def text_png(path, items):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for text, y, size in items:
        f = font(size); lines = wrap(d, text, f, 864)
        for i, l in enumerate(lines):
            tw = d.textlength(l, font=f); x = (W - tw) / 2
            d.text((x, y + i * int(size * 1.18)), l, font=f, fill='white', stroke_width=max(4, size // 11), stroke_fill='black')
    im.save(path); return path
segs = []; t = 0.0; pre = tl.get('premise')
for n, s in enumerate(tl['shots']):
    items = []
    if s.get('caption'): items.append((s['caption'], s.get('cap_y', 1180), s.get('cap_size', 60)))
    if pre and t < pre['until']: items.append((pre['text'], pre.get('y', 300), pre.get('size', 66)))
    png = text_png(f'{tmp}/t{n}.png', items); out = f'{tmp}/s{n:02d}.mp4'
    sp = s.get('speed', 1.0); pts = f",setpts=PTS/{sp}" if sp != 1.0 else ''
    vf = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}{pts},fps={FPS},setsar=1[v];[v][1:v]overlay=0:0[o]"
    if pre and t < pre['until'] < t + s['dur']:   # premise ends inside this shot: split the overlay in time
        png2 = text_png(f'{tmp}/u{n}.png', items[:1] if s.get('caption') else [])
        vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}{pts},fps={FPS},setsar=1[v];"
              f"[v][1:v]overlay=0:0:enable='lt(t,{pre['until']-t:.2f})'[a];[a][2:v]overlay=0:0:enable='gte(t,{pre['until']-t:.2f})'[o]")
        cmd = ['ffmpeg', '-y', '-v', 'error', '-ss', str(s.get('in', 0)), '-t', str(s['dur'] * sp + 0.1), '-i', s['src'], '-loop', '1', '-i', png, '-loop', '1', '-i', png2]
    else:
        cmd = ['ffmpeg', '-y', '-v', 'error', '-ss', str(s.get('in', 0)), '-t', str(s['dur'] * sp + 0.1), '-i', s['src'], '-loop', '1', '-i', png]
    cmd += ['-filter_complex', vf, '-map', '[o]', '-t', str(s['dur']), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-r', str(FPS), out]
    if s['src'].endswith('.png'):   # a still: slow push-in, pixels only scaled
        fr = int(s['dur'] * FPS)
        zp = f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},zoompan=z='1+0.06*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s={W}x{H}:fps={FPS},setsar=1[v];[v][1:v]overlay=0:0[o]"
        cmd = ['ffmpeg', '-y', '-v', 'error', '-i', s['src'], '-loop', '1', '-i', png, '-filter_complex', zp, '-map', '[o]', '-t', str(s['dur']), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-r', str(FPS), out]
    subprocess.run(cmd, check=True); segs.append(out); t += s['dur']
e = tl.get('end')
if e:
    r = Image.open(e['render']).convert('RGB'); bg = tuple(e.get('bg') or r.getpixel((8, 8)))
    c = Image.new('RGB', (W, H), bg); r2 = r.resize((W, round(r.height * W / r.width)), Image.LANCZOS) if r.width != W else r
    c.paste(r2, (0, (H - r2.height) // 2)); c.save(f'{tmp}/end.png')
    out = f'{tmp}/end.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', f'{tmp}/end.png', '-t', str(e['dur']), '-r', str(FPS), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', out], check=True)
    segs.append(out)
with open(f'{tmp}/list.txt', 'w') as fh: fh.writelines(f"file '{p}'\n" for p in segs)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/list.txt', '-c', 'copy', '-movflags', '+faststart', tl['out']], check=True)
print(tl['out'])
