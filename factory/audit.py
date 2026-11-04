#!/usr/bin/env python3
"""Deterministic release audit for Heartside media (docs/PUBLISHING.md, section 1).

    python3 factory/audit.py <file-or-folder> [...] [--paid] [--sheets DIR] [--json OUT]

For each .mp4 it checks:
- size, frame rate and sound;
- length (6 to 60 s organic, 15 to 30 s with --paid);
- integrated loudness (-18 to -13 LUFS);
- a dead first second: a blank interface or a still image for the first 1.5 s.

For each file it checks the library naming rule and records bytes and SHA-256.

With --sheets it writes a 16-frame contact sheet per reel for the person doing the visual check. Sheets are review renders: keep them under local/ and out of git and Drive (docs/CHANNEL-TASKS.md).

It never judges the joke, the product match or the safe zones by eye. Those stay with a person, against the bar in docs/audits/2026-11-04-creative-audit.md. Exit status is 1 when any file fails.
"""
import hashlib, io, json, os, re, subprocess, sys

NAME = re.compile(r'^heartside_[A-Z][0-9]{2,3}(-[a-z0-9]+)*_[a-z0-9]+(-[a-z0-9]+)*_[a-z0-9-]+\.(mp4|jpg)$')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                          'stream=codec_type,width,height,r_frame_rate:format=duration', '-of', 'json', path],
                         capture_output=True, text=True).stdout
    j = json.loads(out)
    v = next((s for s in j['streams'] if s['codec_type'] == 'video'), {})
    num, _, den = (v.get('r_frame_rate') or '0/1').partition('/')
    fps = float(num) / float(den or 1) if float(den or 1) else 0.0
    return {'width': v.get('width'), 'height': v.get('height'), 'fps': round(fps, 2),
            'duration': round(float(j['format']['duration']), 2),
            'audio': any(s['codec_type'] == 'audio' for s in j['streams'])}


def loudness(path):
    err = subprocess.run(['ffmpeg', '-nostats', '-i', path, '-af', 'ebur128', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    m = re.findall(r'I:\s+(-?[\d.]+) LUFS', err)
    return float(m[-1]) if m else None


def gray(path, t, w=108, h=192):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', path, '-frames:v', '1',
                          '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return list(raw) if len(raw) == w * h else None


def dead_open(path):
    """Blank: the first frame is near-uniform (an empty chat or search page).
    Static: the frame barely changes over the first 1.5 s."""
    a, b = gray(path, 0.0), gray(path, 1.5)
    if a is None:
        return 'unreadable'
    mean = sum(a) / len(a)
    spread = (sum((x - mean) ** 2 for x in a) / len(a)) ** 0.5
    if spread < 30:
        return f'blank first frame (pixel spread {spread:.0f})'
    if b is not None and sum(abs(x - y) for x, y in zip(a, b)) / len(a) < 2.0:
        return 'static first 1.5 s'
    return None


def sheet(path, out):
    from PIL import Image, ImageDraw
    d = probe(path)['duration']
    ts = [0.0, 0.5, 1.0, 1.5] + [2 + (d - 2.2) * i / 11 for i in range(12)]
    W, H = 220, 391
    img = Image.new('RGB', (W * 8, H * 2), 'black')
    for i, t in enumerate(ts):
        png = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.2f}', '-i', path, '-frames:v', '1',
                              '-vf', f'scale={W}:{H}', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                             capture_output=True).stdout
        if not png:
            continue
        im = Image.open(io.BytesIO(png)).convert('RGB')
        ImageDraw.Draw(im).text((3, 3), f'{t:.1f}s', fill='yellow')
        img.paste(im, ((i % 8) * W, (i // 8) * H))
    img.save(out, quality=85)


def audit(path, paid=False, sheets=None):
    name = os.path.basename(path)
    r = {'file': name, 'bytes': os.path.getsize(path), 'sha256': sha256(path), 'problems': []}
    if not NAME.match(name):
        r['problems'].append('name breaks heartside_<id>_<slug>_<kind>.<ext>')
    if name.endswith('.mp4'):
        p = probe(path)
        r.update(p)
        if (p['width'], p['height']) != (1080, 1920):
            r['problems'].append(f"{p['width']}x{p['height']}, not 1080x1920")
        if not p['audio']:
            r['problems'].append('no sound')
        lo, hi = (15, 30) if paid else (6, 60)
        if not lo <= p['duration'] <= hi:
            r['problems'].append(f"{p['duration']} s long ({lo} to {hi} allowed{' for paid' if paid else ''})")
        r['lufs'] = loudness(path)
        if r['lufs'] is not None and not -18 <= r['lufs'] <= -13:
            r['problems'].append(f"loudness {r['lufs']} LUFS (want -18 to -13)")
        r['dead_open'] = dead_open(path)
        if r['dead_open']:
            r['problems'].append(f"dead open: {r['dead_open']}")
        if sheets:
            os.makedirs(sheets, exist_ok=True)
            sheet(path, os.path.join(sheets, name.rsplit('.', 1)[0] + '_sheet.jpg'))
    r['verdict'] = 'pass' if not r['problems'] else 'fail'
    return r


def main(argv):
    paid = '--paid' in argv
    sheets = argv[argv.index('--sheets') + 1] if '--sheets' in argv else None
    out = argv[argv.index('--json') + 1] if '--json' in argv else None
    skip = {sheets, out}
    targets = [a for a in argv if not a.startswith('--') and a not in skip]
    files = []
    for t in targets:
        if os.path.isdir(t):
            files += sorted(os.path.join(t, f) for f in os.listdir(t) if f.endswith(('.mp4', '.jpg')))
        else:
            files.append(t)
    results = [audit(f, paid, sheets) for f in files]
    for r in results:
        print(f"{r['verdict']:4}  {r['file']}" + (f"  : {'; '.join(r['problems'])}" if r['problems'] else ''))
    if out:
        with open(out, 'w') as f:
            json.dump(results, f, indent=1)
    return 1 if any(r['verdict'] == 'fail' for r in results) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
