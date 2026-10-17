"""Render approved product photos into a reviewable pack. No AI calls or spend."""
import datetime as dt
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid
from zoneinfo import ZoneInfo

from . import assets, ledger


VERSION = 3
REQUIRED_ROLES = {'reel', 'cover', 'story_1', 'story_2', 'story_3', 'pin_1', 'pin_2', 'subtitles'}


def verify(root, production, pack=None):
    if not isinstance(production, dict):
        return ['a daily pack needs rendered production files (growth.py render)']
    try:
        path = assets.local_path(root, production['manifest'])
        if assets.sha256(path) != production['sha256']:
            return ['production manifest changed after the pack was built']
        manifest = json.loads(path.read_text())
        if manifest.get('version') != VERSION:
            return ['production manifest has an unsupported renderer version']
        if pack is not None:
            if manifest['heartside_sha'] != pack.get('heartside_sha'):
                return ['production was rendered against a different product commit']
            ids = {item.get('creative_id') for item in pack.get('items', []) if isinstance(item, dict)}
            if manifest['creative_id'] not in ids:
                return ['production belongs to a different creative']
            copy = {item['creative_id']: ledger.digest({k: item.get(k) for k in ('platform', 'text', 'intent')})
                    for item in pack['items'] if isinstance(item, dict) and item.get('creative_id')}
            if any(copy.get(cid) != value for cid, value in manifest['copy_sha256'].items()):
                return ['native copy changed after rendering; change the spec and render a new revision']
        if not REQUIRED_ROLES <= manifest['files'].keys():
            return ['production manifest is missing required deliverables']
        for entry in manifest['files'].values():
            if assets.sha256(assets.local_path(root, entry['path'])) != entry['sha256']:
                return ['a rendered file changed or is incomplete: ' + entry['path']]
        return []
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return ['production files or their checksums could not be verified']


def wrap_text(draw, text, font, width):
    result = []
    for paragraph in text.split('\n'):
        line = ''
        for word in paragraph.split():
            if draw.textlength(word, font=font) > width:
                raise ValueError('a word does not fit the image safe zone')
            attempt = (line + ' ' + word).strip()
            if line and draw.textlength(attempt, font=font) > width:
                result.append(line); line = word
            else:
                line = attempt
        result.append(line)
    return result


def block(draw, text, box, font_path, size, minimum, color):
    from PIL import ImageFont
    left, top, right, bottom = box
    for current in range(size, minimum - 1, -2):
        font = ImageFont.truetype(str(font_path), current)
        try:
            lines = wrap_text(draw, text, font, right - left)
        except ValueError:
            continue
        line_height = int(current * 1.25)
        if line_height * len(lines) <= bottom - top:
            for i, line in enumerate(lines):
                draw.text((left, top + i * line_height), line, fill=color, font=font, stroke_width=0)
            return
    raise ValueError('copy does not fit without making the text too small')


def card(root, source_assets, scene, size):
    from PIL import Image, ImageDraw, ImageOps
    width, height = size
    scale = width / 1080
    out = Image.new('RGB', size, '#FBF6F1')
    draw = ImageDraw.Draw(out)
    path = lambda role: assets.local_path(root, source_assets[role]['path'])
    logo = Image.open(path('logo')).convert('RGBA')
    logo.thumbnail((int(310 * scale), int(105 * scale)), Image.Resampling.LANCZOS)
    out.paste(logo, (int(72 * scale), int(height * .055)), logo)
    block(draw, scene['headline'], (int(width * .067), int(height * .15), int(width * .91), int(height * .31)),
          path('display_font'), int(82 * scale), int(52 * scale), '#121010')
    photo = Image.open(path(scene['asset'])).convert('RGB')
    box = (int(width * .067), int(height * .31), int(width * .91), int(height * .69))
    photo = ImageOps.contain(photo, (box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    out.paste(photo, ((box[0] + box[2] - photo.width) // 2, (box[1] + box[3] - photo.height) // 2))
    block(draw, scene['text'], (int(width * .067), int(height * .735), int(width * .91), int(height * .79)),
          path('body_font'), int(42 * scale), int(30 * scale), '#121010')
    block(draw, 'EXAMPLE · Biscuit is an AI character',
          (int(width * .067), int(height * .705), int(width * .92), int(height * .73)),
          path('body_font'), int(28 * scale), int(24 * scale), '#5A4A44')
    return out


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    return f'{milliseconds // 3600000:02}:{milliseconds // 60000 % 60:02}:{milliseconds // 1000 % 60:02},{milliseconds % 1000:03}'


def render(root, spec, state, check_copy, checkout=None, day=None):
    if not state or not state.get('rules_ok'):
        raise ValueError('sync Heartside and resolve any STOP before producing media')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise ValueError('install FFmpeg (ffmpeg and ffprobe) before rendering')
    if spec.get('version') != 1 or spec.get('intent') != 'audience':
        raise ValueError('the first renderer supports audience example packs only; purchase copy stays gated')
    day = dt.date.fromisoformat(day) if day else dt.datetime.now(ZoneInfo('America/New_York')).date()
    # The same concept keeps its number in each native edition.
    stem = f'{spec["pillar"]}_REEL_{spec["concept"]}_{spec["hook"]}_V{spec["variation"]}_{day:%Y%m%d}'
    creative_id = 'IG_' + stem
    scenes = spec.get('scenes')
    if not isinstance(scenes, list) or len(scenes) != 3:
        raise ValueError('this template needs three scenes')
    duration = 0
    for scene in scenes:
        if scene.get('asset') not in ('mug_dog', 'mug_note', 'biscuit'):
            raise ValueError('scene must use an approved product or Biscuit asset')
        seconds = scene.get('seconds')
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not 1 <= seconds <= 10:
            raise ValueError('each scene must last between 1 and 10 seconds')
        duration += seconds
    if duration > 20:
        raise ValueError('the example film must be at most 20 seconds')
    items = []
    for platform, prefix in [('instagram', 'IG'), ('facebook', 'FB'), ('tiktok', 'TT')]:
        items.append({'platform': platform, 'creative_id': prefix + '_' + stem, 'intent': 'audience',
                      'why': spec['mechanism'], 'text': spec['captions'][platform]})
    for i in range(2):
        items.append({'platform': 'pinterest', 'creative_id': f'PIN_{spec["pillar"]}_PIN_{spec["concept"]}_{spec["hook"]}_V{spec["variation"] + i}_{day:%Y%m%d}',
                      'intent': 'audience', 'why': spec['mechanism'], 'text': spec['captions']['pinterest'][i]})
    items.append({'platform': 'instagram', 'creative_id': 'IG_' + stem.replace('_REEL_', '_STORY_'),
                  'intent': 'audience', 'why': spec['mechanism'],
                  'text': '\n'.join(s['headline'] + '\n' + s['text'] for s in scenes)})
    pack = {'pack_date': day.isoformat(), 'kind': 'daily', 'venture': 'heartside', 'heartside_sha': state['sha'],
            'headline': spec['title'] + ': rendered audience pack, review before posting', 'items': items}
    errors = check_copy(pack, state.get('price_points', []), state=state)
    if errors:
        raise ValueError('; '.join(errors))
    source = assets.prepare(root, state['sha'], checkout)
    revision = ledger.digest({'renderer': VERSION, 'spec': spec, 'day': day.isoformat(), 'assets': source})
    parent = assets.local_path(root, 'local/media/' + creative_id)
    target = parent / revision[:16]
    manifest_path = target / 'manifest.json'
    production = {'manifest': str(manifest_path.relative_to(root))}
    if manifest_path.exists():
        production['sha256'] = assets.sha256(manifest_path)
        if not verify(root, production):
            cached = json.loads(manifest_path.read_text())
            if cached.get('revision') == revision:
                pack['production'] = production
                return pack, cached
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=parent, prefix='.build-') as work:
        work = Path(work)
        files, subtitle_parts, elapsed = {}, [], 0
        for i, scene in enumerate(scenes, 1):
            filename = f'story-{i}.png'
            card(root, source['assets'], scene, (1080, 1920)).save(work / filename)
            files[f'story_{i}'] = filename
            subtitle_parts.append(f'{i}\n{timestamp(elapsed)} --> {timestamp(elapsed + scene["seconds"])}\n{scene["headline"]}\n{scene["text"]}\n')
            elapsed += scene['seconds']
        shutil.copyfile(work / 'story-1.png', work / 'cover.png')
        files['cover'] = 'cover.png'
        for i in (1, 2):
            filename = f'pin-{i}.png'
            card(root, source['assets'], scenes[i - 1], (1000, 1500)).save(work / filename)
            files[f'pin_{i}'] = filename
        (work / 'subtitles.srt').write_text('\n'.join(subtitle_parts))
        files['subtitles'] = 'subtitles.srt'
        # Simple cuts preserve the approved images and exact product typography.
        sequence = []
        for i, scene in enumerate(scenes, 1):
            sequence += [f"file 'story-{i}.png'", f'duration {scene["seconds"]}']
        sequence.append("file 'story-3.png'")
        (work / 'frames.txt').write_text('\n'.join(sequence) + '\n')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '1',
                        '-i', 'frames.txt', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                        '-t', str(duration), '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264',
                        '-preset', 'fast', '-crf', '20', '-threads', '2', '-c:a', 'aac', '-b:a', '128k',
                        '-movflags', '+faststart', 'reel.mp4'], cwd=work, check=True, capture_output=True)
        probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                                          '-of', 'json', str(work / 'reel.mp4')], check=True, capture_output=True).stdout)
        video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        if (video['width'], video['height']) != (1080, 1920) or abs(float(probe['format']['duration']) - duration) > .2:
            raise ValueError('rendered video failed its dimensions or duration check')
        files['reel'] = 'reel.mp4'
        manifest = {'version': VERSION, 'creative_id': creative_id, 'revision': revision,
                    'heartside_sha': state['sha'], 'intent': 'audience', 'needs_human_review': True,
                    'audio': 'silent stereo track; no generated voice or music', 'duration_seconds': duration,
                    'copy_sha256': {item['creative_id']: ledger.digest({k: item.get(k) for k in ('platform', 'text', 'intent')}) for item in items},
                    'sources': source, 'files': {role: {'path': str((target / name).relative_to(root)),
                                                       'sha256': assets.sha256(work / name)} for role, name in files.items()}}
        (work / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        if target.exists():
            target.rename(parent / (target.name + '-previous-' + uuid.uuid4().hex[:8]))
        work.rename(target)
    production['sha256'] = assets.sha256(manifest_path)
    pack['production'] = production
    return pack, manifest
