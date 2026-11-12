"""Cut a silent 1080x1920 human-arms lip-sync reel from a timeline JSON (Sprint 120 batch 1, 10 Nov 2026).

    python3 factory/lipsync_cut.py TIMELINE.json

TIMELINE: {"out": path, "font": path to a bold sans (Inter Bold on the build machine),
  "premise": {"text", "y", "size", "until"},            the premise line over shot 1 (sound-off hook)
  "shots": [{"src": clip.mp4 or still.png, "in", "dur", "speed", "label", "label_y"}],
  "end": {"render": the store's own render, "dur"}}    held unaltered, scaled only, on its own ground colour

No lyric captions, ever (Krish, 2026-11-10: "I don't think we ever need subtitles for videos for song lyrics.";
floor no-lyric-captions): a shot with a "caption" is refused.
A shot may carry a "label": the parodied format's own on-screen text, such as "4:00 AM, cold plunge" (Ruling, Krish,
2026-11-10: yes to time-and-activity labels on the 4 AM routine and Monday morning films). Never a sung line. The premise line and labels are the only text, placed clear of faces,
hands and the gag object (floor text-clear-of-faces). speed < 1 slows a trimmed clip so
only its clean window is used; a .png src gets a slow push-in. The reel is silent: the song is added in the app.
The end card carries no text (floor no-badges). Build inputs stay out of git (the repository is public).

12 Nov corpus profile (engine/creative_ui.py): the premise and labels are centred between x 140 and 820 and must sit
inside the critical box (y 330 to 1180), labels default to text top y 360 and stay in one place; the end render is
scaled inside the box and held 3 to 4 s. Text that does not fit is refused, never shrunk.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.creative_ui import CRITICAL, HOOK, END_HOLD  # noqa: E402
W, H, FPS = 1080, 1920, 30
tl = json.load(open(sys.argv[1])); tmp = tempfile.mkdtemp()
if any(s.get('caption') for s in tl['shots']):
    sys.exit('refused: a shot carries a caption; lyric subtitles are never used (floor no-lyric-captions)')
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
    left, right = HOOK[0], HOOK[2]; taken = []
    for text, y, size in items:
        f = font(size); lines = wrap(d, text, f, right - left)
        bottom = y + len(lines) * int(size * 1.18)
        if y < CRITICAL[1] or bottom > CRITICAL[3] or any(d.textlength(l, font=f) > right - left for l in lines):
            sys.exit(f'refused: {text!r} leaves the critical box (x {left} to {right}, y {CRITICAL[1]} to {CRITICAL[3]}); rewrite or move it')
        if any(y < b and a < bottom for a, b in taken):
            sys.exit(f'refused: {text!r} overlaps other on-screen text; give the premise its own y')
        taken.append((y, bottom))
        for i, l in enumerate(lines):
            tw = d.textlength(l, font=f); x = (left + right - tw) / 2
            d.text((x, y + i * int(size * 1.18)), l, font=f, fill='white', stroke_width=max(4, size // 11), stroke_fill='black')
    im.save(path); return path
segs = []; t = 0.0; pre = tl.get('premise')
for n, s in enumerate(tl['shots']):
    items = []
    if s.get('label'): items.append((s['label'], s.get('label_y', HOOK[1]), s.get('label_size', 54)))   # format label, never a lyric
    keep = list(items)
    if pre and t < pre['until']: items.append((pre['text'], pre.get('y', HOOK[1] + 120), pre.get('size', 66)))   # under the label row
    png = text_png(f'{tmp}/t{n}.png', items); out = f'{tmp}/s{n:02d}.mp4'
    sp = s.get('speed', 1.0); pts = f",setpts=PTS/{sp}" if sp != 1.0 else ''
    z = s.get('zoom', 1.0)   # punch-in: crop 1/z of the frame around (cx, cy) and scale back up
    if z != 1.0:
        cx, cy = s.get('cx', 0.5), s.get('cy', 0.35)
        pts += (f",crop={W}/{z}:{H}/{z}:min(max({W}*{cx}-{W}/{z}/2\\,0)\\,{W}-{W}/{z})"
                f":min(max({H}*{cy}-{H}/{z}/2\\,0)\\,{H}-{H}/{z}),scale={W}:{H}")
    vf = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}{pts},fps={FPS},setsar=1[v];[v][1:v]overlay=0:0[o]"
    if pre and t < pre['until'] < t + s['dur']:   # premise ends inside this shot: split the overlay in time
        png2 = text_png(f'{tmp}/u{n}.png', keep)
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
    c = Image.new('RGB', (W, H), bg); bw, bh = CRITICAL[2] - CRITICAL[0], CRITICAL[3] - CRITICAL[1]
    k = min(bw / r.width, bh / r.height); r2 = r.resize((round(r.width * k), round(r.height * k)), Image.LANCZOS)   # scaled only
    c.paste(r2, ((CRITICAL[0] + CRITICAL[2] - r2.width) // 2, (CRITICAL[1] + CRITICAL[3] - r2.height) // 2)); c.save(f'{tmp}/end.png')
    out = f'{tmp}/end.mp4'; hold = min(max(float(e['dur']), END_HOLD[0]), END_HOLD[1])   # at least 3 s, never a dead outro
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', f'{tmp}/end.png', '-t', str(hold), '-r', str(FPS), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', out], check=True)
    segs.append(out)
with open(f'{tmp}/list.txt', 'w') as fh: fh.writelines(f"file '{p}'\n" for p in segs)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/list.txt', '-c', 'copy', '-movflags', '+faststart', tl['out']], check=True)
print(tl['out'])
