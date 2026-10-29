"""Render the current product renders into a reviewable pack. No AI calls or spend."""
import datetime as dt
from functools import lru_cache
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid
from zoneinfo import ZoneInfo

from . import assets, ledger, sound, offers


VERSION = 8
REQUIRED_ROLES = {'reel', 'cover', 'story_1', 'story_2', 'story_3', 'pin_1', 'pin_2', 'subtitles', 'soundtrack', 'facebook_reel', 'tiktok_reel', 'carousel_1', 'carousel_2', 'carousel_3'}


@lru_cache(maxsize=1)
def runtime_fingerprint():
    import PIL
    import zlib
    version = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True).stdout.splitlines()[0]
    return {'ffmpeg': version, 'pillow': PIL.__version__, 'zlib': zlib.ZLIB_VERSION}


def renderer_fingerprint():
    return ledger.digest({name: assets.sha256(Path(__file__).with_name(name))
                          for name in ('media.py', 'assets.py', 'sound.py', 'voice.py')})


def copy_digest(item):
    data = {k: item.get(k) for k in ('platform', 'text', 'intent', 'alt_text')}
    if item.get('intent') == 'buy':
        data['offers'] = item.get('offers')
    return ledger.digest(data)


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
            copy = {item['creative_id']: copy_digest(item)
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


def card(root, source_assets, scene, size, layout='recognition'):
    from PIL import Image, ImageDraw, ImageOps
    width, height = size
    scale = width / 1080
    out = Image.new('RGB', size, '#FBF6F1')
    draw = ImageDraw.Draw(out)
    path = lambda role: assets.local_path(root, source_assets[role]['path'])
    logo = Image.open(path('logo')).convert('RGBA')
    logo.thumbnail((int(310 * scale), int(105 * scale)), Image.Resampling.LANCZOS)
    out.paste(logo, (int(72 * scale), int(height * .055)), logo)
    block(draw, scene['headline'], (int(width * .067), int(height * .15), int(width * .91), int(height * .29)),
          path('display_font'), int(82 * scale), int(52 * scale), '#121010')
    roles = scene['asset'] if isinstance(scene['asset'], list) else [scene['asset']]
    if len(roles) == 1:
        photo = Image.open(path(roles[0])).convert('RGB')
    else:
        # Two real renders side by side, each whole and unaltered.
        photo = Image.new('RGB', (1400, 700), '#FBF6F1')
        for index, role in enumerate(roles):
            picture = ImageOps.contain(Image.open(path(role)).convert('RGB'), (690, 690), Image.Resampling.LANCZOS)
            photo.paste(picture, (index * 700 + (700 - picture.width) // 2, (700 - picture.height) // 2))
    box = (int(width * .067), int(height * .31), int(width * .91), int(height * .69))
    photo = ImageOps.contain(photo, (box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    out.paste(photo, ((box[0] + box[2] - photo.width) // 2, (box[1] + box[3] - photo.height) // 2))
    block(draw, scene['text'], (int(width * .067), int(height * .735), int(width * .91), int(height * .79)),
          path('body_font'), int(42 * scale), int(30 * scale), '#121010')
    # Brand Book: label every example. The gallery dog is never a customer's dog.
    block(draw, 'EXAMPLE · shown with an example dog',
          (int(width * .067), int(height * .705), int(width * .92), int(height * .73)),
          path('body_font'), int(28 * scale), int(24 * scale), '#5A4A44')
    return out


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    return f'{milliseconds // 3600000:02}:{milliseconds // 60000 % 60:02}:{milliseconds // 1000 % 60:02},{milliseconds % 1000:03}'


def render(root, spec, state, check_copy, checkout=None, day=None, link_builder=None):
    if not state or not state.get('rules_ok'):
        raise ValueError('sync Heartside and resolve any STOP before producing media')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise ValueError('install FFmpeg (ffmpeg and ffprobe) before rendering')
    intent = spec.get('intent')
    if spec.get('version') != 1 or intent not in {'audience', 'buy'}:
        raise ValueError('the renderer requires an audience or verified purchase campaign')
    scenes = spec.get('scenes')
    if not isinstance(scenes, list) or len(scenes) != 3:
        raise ValueError('this template needs three scenes')
    for scene in scenes:
        roles = scene.get('asset') if isinstance(scene.get('asset'), list) else [scene.get('asset')]
        if not 1 <= len(roles) <= 2 or any(r not in assets.PRODUCT_IMAGES for r in roles):
            raise ValueError('each scene must show one or two approved current product renders')
    if intent == 'buy':
        declared = spec.get('offers')
        gift = next((o for o in offers.catalog(state) if o['ready'] and o['kind'] == 'gift' and o['id'] in offers.LEAD_GIFTS
                     and isinstance(declared, list) and len(declared) == 1 and isinstance(declared[0], dict)
                     and declared[0].get('id') == o['id']), None)
        shown = {assets.PRODUCT_IMAGES[r][0] for s in scenes for r in (s['asset'] if isinstance(s['asset'], list) else [s['asset']])}
        if (not offers.fresh_store(state) or not gift or set(declared[0]) - {'id', 'quantity', 'unit_price'}
                or declared[0].get('quantity', 1) != 1 or gift['id'] not in shown
                or spec.get('destination') != gift['product']['url'] or not link_builder):
            raise ValueError('purchase media requires one live lead gift (the blanket or the portrait) that the film shows, its exact product page, one declared unit and tracked links')
    day = dt.date.fromisoformat(day) if day else dt.datetime.now(ZoneInfo('America/New_York')).date()
    # The same concept keeps its number in each native edition.
    stem = f'{spec["pillar"]}_REEL_{spec["concept"]}_{spec["hook"]}_V{spec["variation"]}_{day:%Y%m%d}'
    creative_id = 'IG_' + stem
    layout = spec.get('layout', 'recognition')
    if layout != 'recognition':
        raise ValueError('unknown approved media layout')
    duration = 0
    for scene in scenes:
        seconds = scene.get('seconds')
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not 1 <= seconds <= 10:
            raise ValueError('each scene must last between 1 and 10 seconds')
        duration += seconds
    if duration > 20:
        raise ValueError('the example film must be at most 20 seconds')
    items = []
    for platform, prefix in [('instagram', 'IG'), ('facebook', 'FB'), ('tiktok', 'TT')]:
        items.append({'platform': platform, 'creative_id': prefix + '_' + stem, 'intent': intent,
                      'why': spec['mechanism'], 'text': spec['captions'][platform]})
    for i in range(2):
        items.append({'platform': 'pinterest', 'creative_id': f'PIN_{spec["pillar"]}_PIN_{spec["concept"]}_{spec["hook"]}_V{spec["variation"] + i}_{day:%Y%m%d}',
                      'intent': intent, 'why': spec['mechanism'], 'text': spec['captions']['pinterest'][i]})
    items.append({'platform': 'instagram', 'creative_id': 'IG_' + stem.replace('_REEL_', '_STORY_'),
                  'intent': intent, 'why': spec['mechanism'],
                  'text': '\n'.join(s['headline'] + '\n' + s['text'] for s in scenes)})
    if intent == 'buy':
        for item in items:
            item['offers'] = spec['offers']
            link = link_builder(spec['destination'], item['creative_id'])
            item['text'] = item['text'].replace('{link}', link)
            if link not in item['text']:
                item['text'] += '\n' + link
    def public_item(text):
        item = {'platform': 'other', 'text': text}
        if intent == 'buy':
            item['offers'] = spec['offers']
            item['text'] += '\nCopy: ' + link_builder(spec['destination'], creative_id)
        return item
    scene_alt = []
    for scene in scenes:
        roles = scene['asset'] if isinstance(scene['asset'], list) else [scene['asset']]
        description = ' '.join(assets.PRODUCT_IMAGES[r][2] for r in roles)
        scene_alt.append(description + ' Text: ' + scene['headline'] + ' ' + scene['text'])
    pin_index = 0
    for item in items:
        item['alt_text'] = scene_alt[pin_index] if item['platform'] == 'pinterest' else ' '.join(scene_alt)
        if item['platform'] == 'pinterest':
            pin_index += 1
    pack = {'pack_date': day.isoformat(), 'kind': 'daily', 'venture': 'heartside', 'heartside_sha': state['sha'],
            'headline': spec['title'] + ': rendered ' + intent + ' pack, review before posting', 'items': items}
    errors = check_copy(pack, state.get('price_points', []), state=state)
    for item in items:
        alt_pack = {**pack, 'kind': 'radar', 'items': [public_item('\n'.join('Copy: ' + line for line in item['alt_text'].splitlines()))]}
        errors += check_copy(alt_pack, state.get('price_points', []), state=state)
    if errors:
        raise ValueError('; '.join(errors))
    source = assets.prepare(root, state['sha'], checkout, state.get('store'))
    narration = None
    narration_file = spec.get('narration')
    if spec.get('voiceover'):
        if narration_file:
            raise ValueError('choose one narration source')
        voice_copy = {**pack, 'kind': 'radar', 'items': [public_item('\n'.join('Voiceover: ' + line for line in spec['voiceover'].splitlines()))]}
        if check_copy(voice_copy, state.get('price_points', []), state=state):
            raise ValueError('local narration transcript fails copy checks')
        from . import voice
        narration_file = str(voice.synthesize(root, spec['voiceover'], state['sha'], duration).relative_to(root))
    if narration_file:
        receipt = assets.local_path(root, narration_file)
        narration = json.loads(receipt.read_text())
        if (narration.get('role') != 'narration' or not (narration.get('status') == 'approved' or (narration.get('provider') == 'kokoro-local' and narration.get('status') == 'draft_local_synthesis'))
                or narration.get('source_sha') != state['sha'] or not narration.get('transcript')):
            raise ValueError('narration needs approved provenance bound to the current product SHA')
        audio_path = assets.local_path(root, narration['path'])
        if assets.sha256(audio_path) != narration['sha256']:
            raise ValueError('narration checksum changed')
        narration_copy = {**pack, 'kind': 'radar', 'items': [public_item('\n'.join('Voiceover: ' + line for line in narration['transcript'].splitlines()))]}
        if check_copy(narration_copy, state.get('price_points', []), state=state):
            raise ValueError('narration transcript fails copy checks')
        audio_probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-of', 'json', str(audio_path)], check=True, capture_output=True).stdout)
        if float(audio_probe['format']['duration']) > duration:
            raise ValueError('narration is longer than the film; adjust the scene timing, never cut off speech')
        source['narration'] = narration
    revision = ledger.digest({'renderer': VERSION, 'renderer_source': renderer_fingerprint(), 'runtime': runtime_fingerprint(), 'spec': spec, 'day': day.isoformat(), 'assets': source})
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
            card(root, source['assets'], scene, (1080, 1920), layout).save(work / filename)
            files[f'story_{i}'] = filename
            subtitle_parts.append(f'{i}\n{timestamp(elapsed)} --> {timestamp(elapsed + scene["seconds"])}\n{scene["headline"]}\n{scene["text"]}\n')
            elapsed += scene['seconds']
        shutil.copyfile(work / 'story-1.png', work / 'cover.png')
        files['cover'] = 'cover.png'
        for i in (1, 2):
            filename = f'pin-{i}.png'
            card(root, source['assets'], scenes[i - 1], (1000, 1500), layout).save(work / filename)
            files[f'pin_{i}'] = filename
        if narration:
            import textwrap
            subtitle_parts = [f'1\n{timestamp(0)} --> {timestamp(duration)}\n' + '\n'.join(textwrap.wrap(narration['transcript'], 42)) + '\n']
        (work / 'subtitles.srt').write_text('\n'.join(subtitle_parts))
        files['subtitles'] = 'subtitles.srt'
        # Animate the approved photograph/card without altering the print design.
        # Text remains inside the common safe zone throughout the 2% push-in.
        elapsed = 0
        segments = []
        for i, scene in enumerate(scenes, 1):
            frames = round(scene['seconds'] * 30)
            segment = f'segment-{i}.mp4'
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', f'story-{i}.png',
                            '-vf', f"zoompan=z='1+0.02*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=1080x1920:fps=30,format=yuv420p",
                            '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-threads', '2', segment],
                           cwd=work, check=True, capture_output=True)
            segments.append(f"file '{segment}'")
            elapsed += scene['seconds']
        (work / 'segments.txt').write_text('\n'.join(segments) + '\n')
        sound.score(work / 'score.wav', duration, [scenes[0]['seconds'], scenes[0]['seconds'] + scenes[1]['seconds']])
        files['soundtrack'] = 'score.wav'
        audio_args = ['-i', str(assets.local_path(root, narration['path']))] if narration else []
        audio_filter = (['-filter_complex', '[1:a]volume=0.25[music];[2:a]apad[voice];[music][voice]amix=inputs=2:duration=first:normalize=0[a]', '-map', '0:v', '-map', '[a]']
                        if narration else ['-map', '0:v', '-map', '1:a'])
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '1',
                        '-i', 'segments.txt', '-i', 'score.wav', *audio_args, *audio_filter,
                        '-t', str(duration), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
                        '-movflags', '+faststart', 'reel.mp4'], cwd=work, check=True, capture_output=True)
        # Each native film has its own opening card, not just a renamed caption.
        for platform in ('facebook', 'tiktok'):
            hook = spec.get('native_hooks', {}).get(platform, scenes[0]['headline'])
            native_scene = {**scenes[0], 'headline': hook}
            # Validate all visible native text through the same checker.
            native_copy = {**pack, 'kind': 'radar', 'items': [public_item('\n'.join('Hook: ' + line for line in hook.splitlines()))]}
            if check_copy(native_copy, state.get('price_points', []), state=state):
                raise ValueError('native hook fails copy checks')
            card(root, source['assets'], native_scene, (1080, 1920), layout).save(work / f'{platform}-opening.png')
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', 'reel.mp4', '-i', f'{platform}-opening.png',
                            '-filter_complex', f"[0:v][1:v]overlay=enable='lt(t,{scenes[0]['seconds']})'[v]",
                            '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-threads', '2',
                            '-c:a', 'copy', '-movflags', '+faststart', f'{platform}.mp4'], cwd=work, check=True, capture_output=True)
            files[platform + '_reel'] = platform + '.mp4'
        for i, scene in enumerate(scenes, 1):
            name = f'carousel-{i}.png'
            card(root, source['assets'], scene, (1080, 1350), layout).save(work / name)
            files[f'carousel_{i}'] = name
        probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                                          '-of', 'json', str(work / 'reel.mp4')], check=True, capture_output=True).stdout)
        video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        if (video['width'], video['height']) != (1080, 1920) or abs(float(probe['format']['duration']) - duration) > .2:
            raise ValueError('rendered video failed its dimensions or duration check')
        files['reel'] = 'reel.mp4'
        if narration:
            shutil.copyfile(assets.local_path(root, narration['path']), work / 'narration.wav')
            files['narration'] = 'narration.wav'
        manifest = {'version': VERSION, 'renderer_source': renderer_fingerprint(), 'runtime': runtime_fingerprint(), 'creative_id': creative_id, 'revision': revision,
                    'heartside_sha': state['sha'], 'intent': intent, 'needs_human_review': True,
                    'audio': 'Original locally synthesized score' + (' with synthetic narration requiring human review' if narration else '; captions-first, no speech'), 'duration_seconds': duration,
                    'copy_sha256': {item['creative_id']: copy_digest(item) for item in items},
                    'sources': source, 'files': {role: {'path': str((target / name).relative_to(root)),
                                                       'sha256': assets.sha256(work / name)} for role, name in files.items()}}
        for pattern in ('segment-*.mp4', '*-opening.png', 'segments.txt'):
            for scratch in work.glob(pattern):
                scratch.unlink()
        (work / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        if target.exists():
            target.rename(parent / (target.name + '-previous-' + uuid.uuid4().hex[:8]))
        work.rename(target)
    production['sha256'] = assets.sha256(manifest_path)
    pack['production'] = production
    return pack, manifest
