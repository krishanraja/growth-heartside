"""Build a new UI edition from hash-bound clean sources and an immutable audio master.

This never changes a lock or publishes. The input plan names every source, caption,
frame boundary and allowed layout change. Native placement review remains separate.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import ui_layout
from common import F, bold, product_clip, run, W, H
from build import _cover, join
import lock

FONT = bold(F('Karla.ttf', 54), 800)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def caption_beats(text):
    """Keep every word, in order; split at readable two-line phrase boundaries."""
    if not text.strip():
        return []
    try:
        ui_layout.caption(Image.new('RGBA', (W, H)), text, FONT)
        return [' '.join(text.split())]
    except ValueError:
        pass
    # Preserve short spoken sentences as complete units before considering a
    # word-count split. Otherwise a greedy fit can strand a word like "couch".
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) > 1:
        return [beat for sentence in sentences for beat in caption_beats(sentence)]
    words, result = text.split(), []
    while words:
        fits = []
        for count in range(1, len(words) + 1):
            phrase = ' '.join(words[:count])
            try:
                ui_layout.caption(Image.new('RGBA', (W, H)), phrase, FONT)
            except ValueError:
                continue
            fits.append(count)
        if not fits:
            raise ValueError('caption contains an unrenderable word')
        end = max(fits)
        if 0 < len(words) - end < 3:
            balanced = [n for n in fits if len(words) - n >= 3 and n >= 3]
            if balanced:
                end = max(balanced)
        punctuation = [n for n in fits if 2 <= n <= end
                       and words[n - 1].endswith(('.', '!', '?', ',', ';', ':'))]
        if end < len(words) and punctuation:
            end = max(punctuation)
        result.append(' '.join(words[:end]))
        words = words[end:]
    assert ' '.join(result) == ' '.join(text.split())
    return result


def check_source(item):
    path = Path(item['path'])
    if sha(path) != item['sha256']:
        raise ValueError(f'source hash changed: {path.name}')
    return path


def render_shot(shot, directory):
    frames = shot['frames']
    picture = directory / 'picture.mp4'
    base = directory / 'base.mp4'
    directory.mkdir(parents=True, exist_ok=True)
    base_key = directory / 'base-key.txt'
    source_key = hashlib.sha256(json.dumps({k:v for k,v in shot.items()
        if k not in ('caption_y', 'beats', 'labels')},sort_keys=True).encode()).hexdigest()
    check_source(shot['source'])
    try:
        cached = json.loads(base_key.read_text())
    except (FileNotFoundError, ValueError):
        cached = {}
    if base.exists() and cached.get('input') == source_key and cached.get('sha256') == sha(base):
        pass
    elif 'product' in shot:
        check_source(shot['source'])
        # Reserve a caption band below the product. Leave room for motion overshoot.
        box = (132, 310, 840, 930) if shot.get('text') else (132, 310, 840, 1110)
        product_clip([shot['product']], str(base), frames / 30, box=box, critical_box=box)
    else:
        source = check_source(shot['source'])
        if source.suffix.lower() in ('.mp4', '.mov'):
            args = ['-ss', str(shot.get('in', 0)), '-i', str(source)]
            clip_frames = shot.get('clip_frames', frames)
            vf = (f'trim=end_frame={clip_frames},setpts=PTS-STARTPTS,scale=1080:1920,'
                  f'fps=30,tpad=stop_mode=clone:stop_duration={frames / 30},format=yuv420p')
        else:
            still = directory / 'source.png'
            _cover(str(source), shot.get('crop_top', 0)).save(still)
            args = ['-loop', '1', '-i', str(still)]
            if shot.get('pull'):
                z0, (fx, fy) = shot['pull']['zoom'], shot['pull']['focus']
                z = f'max(1,{z0}-({z0}-1)*min(1,on/{max(1, round(frames * .8))}))'
                xy = f"x='max(0,min(iw-iw/zoom,{fx}*iw-iw/zoom/2))':y='max(0,min(ih-ih/zoom,{fy}*ih-ih/zoom/2))'"
            else:
                z = 'min(zoom+0.0007,1.08)'
                xy = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            vf = f"scale=2160:3840,zoompan=z='{z}':{xy}:d={frames}:s=1080x1920:fps=30,format=yuv420p"
        run(['ffmpeg', '-y'] + args + ['-vf', vf, '-an', '-frames:v', str(frames),
            '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast', '-crf', '19', str(base)])
    base_key.write_text(json.dumps({'input': source_key, 'sha256': sha(base)}))
    beats = shot.get('beats') or caption_beats(shot.get('text', ''))
    if not beats and not shot.get('labels'):
        return base, []
    inputs, filters, receipts = ['-i', str(base)], [], []
    total_weight = sum(len(b.split()) for b in beats)
    consumed = 0
    overlays = []
    for beat in beats:
        start = round(frames * consumed / total_weight)
        consumed += len(beat.split())
        end = round(frames * consumed / total_weight)
        overlays.append((beat, start, end, shot.get('caption_y', 960), 'caption'))
    overlays.extend((label['text'], label['start_frame'], label['end_frame'], label.get('y', 300), 'label')
                    for label in shot.get('labels', []))
    for idx, (text, start, end, y, role) in enumerate(overlays, 1):
        panel = directory / f'panel-{idx}.png'
        ui_layout.caption(Image.new('RGBA', (W, H)), text, FONT, y).save(panel)
        inputs += ['-loop', '1', '-i', str(panel)]
        previous = '[0:v]' if idx == 1 else f'[v{idx-1}]'
        filters.append(f"{previous}[{idx}:v]overlay=0:0:enable='gte(n,{start})*lt(n,{end})'[v{idx}]")
        receipts.append(dict(text=text, start_frame=start, end_frame=end, y=y, role=role))
    run(['ffmpeg', '-y'] + inputs + ['-filter_complex', ';'.join(filters), '-map', f'[v{len(overlays)}]',
        '-frames:v', str(frames), '-an', '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast',
        '-crf', '19', '-pix_fmt', 'yuv420p', str(picture)])
    return picture, receipts


def validate_plan(plan):
    # A UI edition may reflow the bank's words, but cannot rewrite its joke or
    # silently change a scene boundary while borrowing the old approval.
    spec = json.loads((Path(__file__).parent / 'specs' / (plan['id'] + '.json')).read_text(encoding='utf-8'))
    if spec['template'] == 'film':
        lines = [lock.resolve(s['line'], spec) if s.get('line') else '' for s in spec['shots']]
        ends = [round(s['until'] * 30) for s in spec['shots']]
    elif spec['template'] == 'roast':
        lines = [lock.resolve(x, spec) for x in [spec['title']] + spec['lines']]
        ends = [round(sum(spec['durs'][:i + 1]) * 30) for i in range(len(lines))]
    else:
        raise ValueError('source repair supports only film and roast editions')
    assert len(plan['shots']) == len(lines) + 1
    start = 0
    for shot, text, end in zip(plan['shots'], lines, ends):
        assert ' '.join(shot.get('text', '').split()) == ' '.join(text.split()), 'approved caption wording changed'
        assert shot['frames'] == end - start, 'approved shot timing changed'
        if shot.get('beats'):
            assert ' '.join(shot['beats']) == ' '.join(text.split()), 'caption beats changed words'
        start = end
    return plan


def build(plan_path):
    plan_path = Path(plan_path)
    plan = validate_plan(json.loads(plan_path.read_text(encoding='utf-8')))
    master = check_source(plan['master'])
    out = Path(plan['output'])
    out.mkdir(parents=True, exist_ok=True)
    video = next(s for s in probe(master)['streams'] if s['codec_type'] == 'video')
    expected = int(video['nb_frames'])
    assert sum(s['frames'] for s in plan['shots']) == expected, 'timeline must match the approved master'
    parts, receipt = [], []
    for i, shot in enumerate(plan['shots']):
        part, beats = render_shot(shot, out / f'shot-{i:02d}')
        parts.append(str(part))
        receipt.append(dict(shot=i, frames=shot['frames'], captions=beats))
        print(plan['id'], i, 'rendered', flush=True)
    picture = out / 'picture.mp4'
    join(parts, str(picture))
    result = out / f"{plan['id']}-ui-v1.mp4"
    run(['ffmpeg', '-y', '-i', str(picture), '-i', str(master), '-map', '0:v:0', '-map', '1:a:0',
         '-c', 'copy', '-movflags', '+faststart', str(result)])
    final_video = next(s for s in probe(result)['streams'] if s['codec_type'] == 'video')
    assert int(final_video['nb_frames']) == expected
    audio_hashes = []
    for path in (master, result):
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
                                       '-c:a', 'copy', '-f', 'adts', '-'])
        audio_hashes.append(hashlib.sha256(raw).hexdigest())
    assert audio_hashes[0] == audio_hashes[1], 'approved audio changed'
    data = dict(id=plan['id'], plan_sha256=sha(plan_path), master=plan['master'],
                media=dict(path=str(result), sha256=sha(result), frames=expected),
                audio_sha256=audio_hashes[0], shots=receipt,
                native_review='pending', status='candidate')
    (out / 'render-receipt.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plans', nargs='+')
    args = parser.parse_args()
    for path in args.plans:
        result = build(path)
        print(result['media']['path'], flush=True)
