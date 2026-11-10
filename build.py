#!/usr/bin/env python3
"""Assemble approved timelines. Run --contact-sheet, inspect media, then supply
out/review.json: {"F46": {"cover_shot": 3, "cover_reason": "...",
"shots": {"1": {"label_y": 300, "reason": "..."}, ...}} , ...}.
Shot numbers are one-based. Reasons record visual inspection, not guesses.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out'
IDS = [f'F{i}' for i in range(46, 51)]
INK = '#1F1A17'
CREAM = '#F4EFE6'

def run(args):
    subprocess.run([str(a) for a in args], check=True)

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))

def font(path, size, bold=False):
    f = ImageFont.truetype(str(path), size)
    if bold:
        try:
            axes = f.get_variation_axes()
            f.set_variation_by_axes([700 if a['name'] == b'Weight' else a['default'] for a in axes])
        except OSError:
            if 'bold' not in f.getname()[1].lower():
                raise ValueError('Karla must be bold or expose a weight axis')
    return f

def pill(layer, text, f, y, title=False):
    d = ImageDraw.Draw(layer)
    box = d.textbbox((0, 0), text, font=f)
    w, h = box[2]-box[0], box[3]-box[1]
    if not title and w > 760:
        raise ValueError(f'Label exceeds 760 px at 52 px: {text} ({w})')
    if 108+w+44 > 1080:
        raise ValueError(f'Title exceeds canvas: {text}')
    d.rounded_rectangle((108, y, 108+w+44, y+h+24), radius=22,
                        fill=INK if title else (255, 255, 255, 235))
    d.text((130-box[0], y+12-box[1]), text, font=f, fill=CREAM if title else INK)


def sample(src, shot, t, target):
    if shot['kind'] == 'clip':
        run(['ffmpeg', '-v', 'error', '-y', '-ss', str(shot.get('in', 0)+t), '-i', src,
             '-frames:v', '1', target])
        return Image.open(target).convert('RGB')
    return Image.open(src).convert('RGB')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs', type=Path, default=ROOT/'inputs')
    ap.add_argument('--review', type=Path, default=OUT/'review.json')
    ap.add_argument('--contact-sheet', action='store_true')
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    inp = args.inputs.resolve()
    # Checkout contains metadata only. This fallback identifies missing media precisely.
    timelines = inp if inp.exists() else ROOT/'codex/inputs/dog-things-wave-3'
    missing = []
    specs = {}
    for id in IDS:
        p = timelines/f'{id}.json'
        if not p.is_file():
            missing.append(str(p)); continue
        specs[id] = json.loads(p.read_text())
        for s in specs[id]['shots']:
            p = inp/s['src']
            if not p.is_file(): missing.append(str(p))
    for name in ['Karla.ttf', 'Fraunces.ttf']:
        if not (inp/name).is_file(): missing.append(str(inp/name))
    for tool in ['ffmpeg', 'ffprobe']:
        if not shutil.which(tool): missing.append(f'executable: {tool}')
    if missing:
        message = '# Build blocked\n\nMissing required inputs:\n\n' + '\n'.join(f'- `{p}`' for p in dict.fromkeys(missing))
        message += '\n\nNo reels or covers rendered. Cover beats and label moves cannot be chosen without viewing the approved media.\nCurrent Heartside status is unknown: sync failed due to DNS resolution.\n'
        (OUT/'notes.md').write_text(message)
        print(message)
        return 1
    karla = font(inp/'Karla.ttf', 52, True)
    fraunces = font(inp/'Fraunces.ttf', 64)
    work = OUT/'work'
    work.mkdir(exist_ok=True)
    if args.contact_sheet:
        for id, spec in specs.items():
            sheet = Image.new('RGB', (810, len(spec['shots'])*520), CREAM)
            d = ImageDraw.Draw(sheet)
            for i, s in enumerate(spec['shots']):
                for j, portion in enumerate([0, .5, .99]):
                    im = sample(inp/s['src'], s, s['seconds']*portion, work/'sample.png')
                    im = ImageOps.fit(im, (270, 480))
                    sheet.paste(im, (270*j, i*520))
                d.text((5, i*520+482), f"{i+1}: {s.get('label')} (start/middle/end)", fill=INK)
            sheet.save(OUT/f'{id}_inspection.jpg')
        print('Inspect sheets and full clips, then write out/review.json before rendering.')
        return 0
    if not args.review.exists():
        raise ValueError('Visual review required: run --contact-sheet and supply out/review.json; see build.py docstring')
    reviews = json.loads(args.review.read_text())
    notes = ['# Assembly notes', 'Product shots use the requested end_label at y=190; the render itself has no overlaid text.']
    for id, spec in specs.items():
        review = reviews[id]
        cover = int(review['cover_shot'])
        assert 1 <= cover <= len(spec['shots']) and review['cover_reason']
        parts = []
        elapsed = 0
        cover_time = 0
        for i, s in enumerate(spec['shots'], 1):
            n = round(s['seconds']*30)
            assert abs(n/30-s['seconds']) < 1e-6
            overlay = Image.new('RGBA', (1080, 1920))
            if s['label']:
                r = review['shots'][str(i)]
                y = r['label_y']
                assert y in (300, 1300) and r['reason']
                pill(overlay, s['label'], karla, y)
                if y == 1300: notes.append(f"{id} shot {i}, {s['label']}: moved to y=1300. {r['reason']}")
            if s['kind'] == 'product':
                assert s['seconds'] == 3.5
                if spec.get('end_label'): pill(overlay, spec['end_label'], fraunces, 190, True)
            elif i == 1:
                pill(overlay, spec['title'], fraunces, 190, True)
            op = work/f'{id}_{i}_overlay.png'
            overlay.save(op)
            src = inp/s['src']
            dest = work/f'{id}_{i}.mp4'
            base = ['ffmpeg', '-v', 'error', '-y']
            if s['kind'] == 'clip':
                assert float(probe(src)['format']['duration']) >= s.get('in', 0)+s['seconds']
                base += ['-ss', s.get('in', 0), '-i', src]
                vf = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1'
            elif s['kind'] == 'still':
                base += ['-i', src]
                vf = f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1+0.06*on/{max(n-1,1)}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s=1080x1920:fps=30,setsar=1"
            else:
                im = Image.open(src).convert('RGB')
                im.thumbnail((900,1500), Image.Resampling.LANCZOS)
                bg = Image.new('RGB', (1080,1920), CREAM)
                bg.paste(im, ((1080-im.width)//2,(1920-im.height)//2))
                p = work/f'{id}_product.png'; bg.save(p)
                base += ['-loop', '1', '-framerate', '30', '-i', p]
                vf = 'setsar=1'
            run(base+['-i', op, '-filter_complex', f'[0:v]{vf}[base];[base][1:v]overlay=0:0,format=yuv420p[v]', '-map', '[v]', '-an', '-frames:v', n, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-threads', '2', dest])
            parts.append(dest)
            if i == cover: cover_time = elapsed+s['seconds']/2
            elapsed += s['seconds']
        assert abs(elapsed-spec['total_seconds']) < 1e-6
        listing = work/f'{id}_concat.txt'
        listing.write_text(''.join(f"file '{p.name}'\n" for p in parts))
        output = OUT/f'{id}.mp4'
        run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',listing,'-c','copy','-an','-movflags','+faststart',output])
        data = probe(output)
        v = data['streams'][0]
        assert len(data['streams']) == 1 and v['codec_name'] == 'h264'
        assert (v['width'],v['height'],v['pix_fmt'],v['r_frame_rate']) == (1080,1920,'yuv420p','30/1')
        assert abs(float(data['format']['duration'])-spec['total_seconds']) <= .2
        run(['ffmpeg','-v','error','-y','-ss',str(cover_time),'-i',output,'-frames:v','1','-q:v','2',OUT/f'{id}_cover.jpg'])
        notes.append(f"{id} cover: shot {cover}, {spec['shots'][cover-1]['label']}, middle at {cover_time:.3f}s. {review['cover_reason']}")
    notes.append('Verified: durations, 1080x1920, 30 fps, H.264 yuv420p, one video stream and no audio. Final frame-by-frame face/action clearance review remains required.')
    (OUT/'notes.md').write_text('\n\n'.join(notes)+'\n')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
