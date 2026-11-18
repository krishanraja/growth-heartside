"""Build ready/ from docs/briefs/2026-11-18-footage/manifest.json: trimmed 1080x1920 30fps silent clips,
a poster still at each clip's payoff, a timestamped sheet of each ready file, and manifest.csv."""
import csv, json, os, subprocess, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
FOOT = os.path.join(REPO, 'local', 'footage')
m = json.load(open(os.path.join(REPO, 'docs', 'briefs', '2026-11-18-footage', 'manifest.json'), encoding='utf-8'))
for d in ('ready', 'ready/posters', 'ready/sheets'):
    os.makedirs(os.path.join(FOOT, d), exist_ok=True)
vf = 'scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,setsar=1'
rows = []
for c in m['clips']:
    name = f"{c['id']}_{c['slug']}"
    src = os.path.join(FOOT, c['src'])
    out = os.path.join(FOOT, 'ready', name + '.mp4')
    dur = round(c['out'] - c['in'], 2)
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-ss', str(c['in']), '-i', src, '-t', str(dur), '-an',
                           '-vf', vf, '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                           '-movflags', '+faststart', out])
    poster = os.path.join(FOOT, 'ready', 'posters', name + '.jpg')
    pt = min(max(c['poster'] - c['in'], 0), dur - 0.1)
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-ss', str(pt), '-i', out, '-frames:v', '1', '-q:v', '2', poster])
    subprocess.check_call([sys.executable, '-I', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sheet.py'), out,
                           os.path.join(FOOT, 'ready', 'sheets', name + '.jpg')], stdout=subprocess.DEVNULL)
    real = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]).decode())
    rows.append({'id': c['id'], 'file': f"ready/{name}.mp4", 'seconds': round(real, 2), 'dogs': ' + '.join(c['dogs']),
                 'setting': c['setting'], 'beats': ' | '.join(f"{t:.1f}s {b}" for t, b in c['beats']),
                 'payoff_s': c['payoff'], 'fault': c['fault'], 'verdict': c['verdict'], 'model': c['model'],
                 'source': c['src'], 'source_in_out': f"{c['in']}-{c['out']}", 'higgsfield_asset': c['asset']})
    print(name, round(real, 2))
with open(os.path.join(FOOT, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('rows', len(rows))

# One-page index of every ready clip's poster.
import glob
from PIL import Image, ImageDraw, ImageFont
posters = sorted(glob.glob(os.path.join(FOOT, 'ready', 'posters', '*.jpg')))
W, H, cols = 216, 384, 7
rows_n = (len(posters) + cols - 1) // cols
index = Image.new('RGB', (W * cols, (H + 44) * rows_n), 'white')
try:
    font = ImageFont.truetype('arial.ttf', 15)
except Exception:
    font = ImageFont.load_default()
draw = ImageDraw.Draw(index)
for i, p in enumerate(posters):
    x, y = (i % cols) * W, (i // cols) * (H + 44)
    index.paste(Image.open(p).convert('RGB').resize((W, H)), (x, y))
    cid, _, rest = os.path.basename(p)[:-4].partition('_')
    draw.text((x + 4, y + H + 3), cid, fill=(0, 0, 0), font=font)
    draw.text((x + 4, y + H + 22), rest[:28], fill=(60, 60, 60), font=font)
index.save(os.path.join(FOOT, 'INDEX.jpg'), quality=85)
print('index', len(posters))
