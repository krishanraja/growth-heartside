"""Render the current product renders into a reviewable pack. No AI calls or spend."""
import datetime as dt
from functools import lru_cache
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid
from zoneinfo import ZoneInfo

from . import assets, ledger, sound, offers, creative_ui


VERSION = 10   # 12 Nov corpus profile: geometry, export preset and layout manifests
REQUIRED_ROLES = {'reel', 'cover', 'story_1', 'story_2', 'story_3', 'pin_1', 'pin_2', 'subtitles', 'soundtrack', 'facebook_reel', 'tiktok_reel', 'carousel_1', 'carousel_2', 'carousel_3',
                  'reel_layout', 'facebook_reel_layout', 'tiktok_reel_layout'}
PUSH = 1.02   # the slow push-in on each card scales its words too, so their recorded boxes include it


@lru_cache(maxsize=1)
def runtime_fingerprint():
    import PIL
    import zlib
    version = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True).stdout.splitlines()[0]
    return {'ffmpeg': version, 'pillow': PIL.__version__, 'zlib': zlib.ZLIB_VERSION}


def renderer_fingerprint():
    return ledger.digest({name: assets.sha256(Path(__file__).with_name(name))
                          for name in ('media.py', 'assets.py', 'sound.py', 'voice.py', 'creative_ui.py')})


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
    """Draw wrapped copy inside `box`; returns the box the words actually occupy (None for no words)."""
    from PIL import ImageFont
    left, top, right, bottom = box
    if not (text or '').strip():
        return None
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
            width = max(draw.textlength(line, font=font) for line in lines)
            return (left, top, left + width, top + line_height * len(lines))
    raise ValueError('copy does not fit without making the text too small')


def pushed(box, size, zoom=PUSH):
    """A box as the centre push-in leaves it at its largest."""
    cx, cy = size[0] / 2, size[1] / 2
    return (cx - (cx - box[0]) * zoom, cy - (cy - box[1]) * zoom, cx + (box[2] - cx) * zoom, cy + (box[3] - cy) * zoom)


def card(root, source_assets, scene, size, layout='recognition', record=None, hook=False):
    from PIL import Image, ImageDraw, ImageOps
    width, height = size
    scale = width / 1080
    out = Image.new('RGB', size, '#FBF6F1')
    draw = ImageDraw.Draw(out)
    path = lambda role: assets.local_path(root, source_assets[role]['path'])
    logo = Image.open(path('logo')).convert('RGBA')
    vertical = size == (1080, 1920)
    if vertical:
        # Corpus profile: a small mark in the logo region, the hook in the hook region, the real
        # product and the words inside the critical box; right edges leave room for the push-in.
        left, right = creative_ui.HOOK[0], 810
        logo_xy, headline_box = (creative_ui.LOGO[0] + 12, creative_ui.LOGO[1] + 14), (left, 440, right, 680)   # the mark stays in its region at full push-in
        picture_box = (left + 20, None, right - 20, 924)   # starts under the headline it follows
        text_box = (creative_ui.SUBTITLES[0], creative_ui.SUBTITLES[1], right, creative_ui.SUBTITLES[3])
    else:
        # Feed/Pin compositions have their own geometry, not a Reels rail overlay.
        left, right = int(width * .1), int(width * .9)
        logo_xy = (left, int(height * .06))
        headline_box = (left, int(height * .16), right, int(height * .32))
        picture_box = (left, int(height * .34), right, int(height * .72))
        text_box = (left, int(height * .76), right, int(height * .94))
    logo.thumbnail((int(200 * scale), int(56 * scale)) if vertical else (int(230 * scale), int(70 * scale)), Image.Resampling.LANCZOS)
    out.paste(logo, logo_xy, logo)
    marks = [('logo', (logo_xy[0], logo_xy[1], logo_xy[0] + logo.width, logo_xy[1] + logo.height), None)]
    drawn = block(draw, scene['headline'], headline_box, path('display_font'), int(64 * scale), int(64 * scale), '#121010')
    if drawn:
        marks.append(('hook' if hook else 'title', drawn, scene['headline']))
    if picture_box[1] is None:
        picture_box = (picture_box[0], int(drawn[3]) + 16 if drawn else headline_box[1], picture_box[2], picture_box[3])
    roles = scene['asset'] if isinstance(scene['asset'], list) else [scene['asset']]
    if len(roles) == 1:
        photo = Image.open(path(roles[0])).convert('RGB')
    else:
        # Two real renders side by side, each whole and unaltered.
        photo = Image.new('RGB', (1400, 700), '#FBF6F1')
        for index, role in enumerate(roles):
            picture = ImageOps.contain(Image.open(path(role)).convert('RGB'), (690, 690), Image.Resampling.LANCZOS)
            photo.paste(picture, (index * 700 + (700 - picture.width) // 2, (700 - picture.height) // 2))
    box = picture_box
    photo = ImageOps.contain(photo, (box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    at = ((box[0] + box[2] - photo.width) // 2, (box[1] + box[3] - photo.height) // 2)
    out.paste(photo, at)
    marks.append(('product', (at[0], at[1], at[0] + photo.width, at[1] + photo.height), None))
    drawn = block(draw, scene['text'], text_box, path('body_font'), int(54 * scale), int(48 * scale), '#121010')
    if drawn:
        marks.append(('text', drawn, scene['text']))
    if record is not None:
        record.extend(marks)
    # Krish, 2 Nov: no Example badges. Product pixels remain unaltered.
    return out


def reel_layout(marks_by_scene, scenes):
    """The layout manifest of a reel built from vertical cards, with every box at its pushed-in size."""
    elements, t = [{'role': 'background', 'box': [0, 0, 1080, 1920], 'start': 0, 'end': sum(s['seconds'] for s in scenes)}], 0
    for marks, scene in zip(marks_by_scene, scenes):
        for role, box, text in marks:
            e = {'role': role, 'box': [round(v, 1) for v in pushed(box, (1080, 1920))], 'start': t, 'end': t + scene['seconds']}
            if text:
                e['text'] = text
            elements.append(e)
        t += scene['seconds']
    last = marks_by_scene[-1] if marks_by_scene else []
    ending = 'product' if any(role == 'product' for role, _, _ in last) else 'none'
    return {'profile': creative_ui.REVISION, 'canvas': [1080, 1920], 'duration': t, 'ending': ending, 'elements': elements}


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    return f'{milliseconds // 3600000:02}:{milliseconds // 60000 % 60:02}:{milliseconds // 1000 % 60:02},{milliseconds % 1000:03}'


def scene_problems(scenes, claim_problems=None):
    """heartside's claims rules on each scene as a viewer reads the frame: the gift it shows, then its words. Over a
    portrait, "With a short note from the dog." reads as a portrait with a note on it (Ruling, Krish, 2026-10-31:
    every gift is artwork only, the note comes in the box). claim_problems: growth.claim_problems unless given."""
    if claim_problems is None:
        home = str(Path(__file__).resolve().parents[1])  # the repository's growth.py, never a render root
        if home not in sys.path:
            sys.path.insert(0, home)
        import growth
        claim_problems = growth.claim_problems
    out = []
    for n, scene in enumerate(scenes, 1):
        roles = scene['asset'] if isinstance(scene['asset'], list) else [scene['asset']]
        gifts = ' and '.join(dict.fromkeys(assets.PRODUCT_IMAGES[r][0] for r in roles))
        words = f"{gifts} {scene.get('headline') or ''}\n{scene.get('text') or ''}"
        out += [f'scene {n}: {why}' for why in claim_problems(words)]
    return out


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
    in_frame = scene_problems(scenes)
    if in_frame:
        raise ValueError('; '.join(in_frame))
    if intent == 'buy':
        declared = spec.get('offers')
        gift = next((o for o in offers.catalog(state) if o['ready'] and o['kind'] == 'gift'
                     and isinstance(declared, list) and len(declared) == 1 and isinstance(declared[0], dict)
                     and declared[0].get('id') == o['id']), None)
        shown = {assets.PRODUCT_IMAGES[r][0] for s in scenes for r in (s['asset'] if isinstance(s['asset'], list) else [s['asset']])}
        if (not offers.fresh_store(state) or not gift or set(declared[0]) - {'id', 'quantity', 'unit_price'}
                or declared[0].get('quantity', 1) != 1 or gift['id'] not in shown
                or spec.get('destination') != gift['product']['url'] or not link_builder):
            raise ValueError('purchase media requires one live gift that the film shows, its exact product page, one declared unit and tracked links')
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
        narration_seconds = float(audio_probe['format']['duration'])
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
        files, subtitle_parts, elapsed, marks = {}, [], 0, []
        for i, scene in enumerate(scenes, 1):
            filename = f'story-{i}.png'; marks.append([])
            card(root, source['assets'], scene, (1080, 1920), layout, record=marks[-1], hook=i == 1).save(work / filename)
            files[f'story_{i}'] = filename
            subtitle_parts.append(f'{i}\n{timestamp(elapsed)} --> {timestamp(elapsed + scene["seconds"])}\n{scene["headline"]}\n{scene["text"]}\n')
            elapsed += scene['seconds']
        shutil.copyfile(work / 'story-1.png', work / 'cover.png')
        files['cover'] = 'cover.png'
        for i in (1, 2):
            filename = f'pin-{i}.png'
            card(root, source['assets'], scenes[i - 1], (1000, 1500), layout).save(work / filename)
            files[f'pin_{i}'] = filename
        if narration:   # timed cues of at most 7 words, never the whole transcript at once (corpus 6.1)
            cues = creative_ui.segments(narration['transcript'], 0, narration_seconds)   # timed to the voice, not the film
            subtitle_parts = [f'{k}\n{timestamp(a)} --> {timestamp(b)}\n{text}\n' for k, (text, a, b) in enumerate(cues, 1)]
        (work / 'subtitles.srt').write_text('\n'.join(subtitle_parts))
        files['subtitles'] = 'subtitles.srt'
        # Animate the approved photograph/card without altering the print design.
        # House working region only. Native UI evidence is required before release.
        elapsed = 0
        segments = []
        for i, scene in enumerate(scenes, 1):
            frames = round(scene['seconds'] * 30)
            segment = f'segment-{i}.mp4'
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', f'story-{i}.png',
                            '-vf', f"zoompan=z='1+{PUSH - 1:.2f}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=1080x1920:fps=30,format=yuv420p",
                            '-an', *creative_ui.FFMPEG_VIDEO, '-threads', '2', segment],
                           cwd=work, check=True, capture_output=True)
            segments.append(f"file '{segment}'")
            elapsed += scene['seconds']
        (work / 'segments.txt').write_text('\n'.join(segments) + '\n')
        sound.score(work / 'score.wav', duration, [scenes[0]['seconds'], scenes[0]['seconds'] + scenes[1]['seconds']])
        files['soundtrack'] = 'score.wav'
        audio_args = ['-i', str(assets.local_path(root, narration['path']))] if narration else []
        # A -2.5 dBFS sample ceiling before the 48 kHz AAC encode keeps the true peak under -1 dBTP.
        limit = 'aresample=48000,alimiter=limit=0.75:attack=2:release=60:level=false'
        audio_filter = (['-filter_complex', f'[1:a]volume=0.25[music];[2:a]apad[voice];[music][voice]amix=inputs=2:duration=first:normalize=0,{limit}[a]', '-map', '0:v', '-map', '[a]']
                        if narration else ['-filter_complex', f'[1:a]{limit}[a]', '-map', '0:v', '-map', '[a]'])
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '1',
                        '-i', 'segments.txt', '-i', 'score.wav', *audio_args, *audio_filter,
                        '-t', str(duration), '-c:v', 'copy', *creative_ui.FFMPEG_AUDIO,
                        '-movflags', '+faststart', 'reel.mp4'], cwd=work, check=True, capture_output=True)
        (work / 'reel-layout.json').write_text(json.dumps(reel_layout(marks, scenes), indent=1) + '\n')
        files['reel_layout'] = 'reel-layout.json'
        # Each native film has its own opening card, not just a renamed caption.
        for platform in ('facebook', 'tiktok'):
            hook = spec.get('native_hooks', {}).get(platform, scenes[0]['headline'])
            native_scene = {**scenes[0], 'headline': hook}
            # Validate all visible native text through the same checker.
            native_copy = {**pack, 'kind': 'radar', 'items': [public_item('\n'.join('Hook: ' + line for line in hook.splitlines()))]}
            if check_copy(native_copy, state.get('price_points', []), state=state):
                raise ValueError('native hook fails copy checks')
            opening = []
            card(root, source['assets'], native_scene, (1080, 1920), layout, record=opening, hook=True).save(work / f'{platform}-opening.png')
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', 'reel.mp4', '-i', f'{platform}-opening.png',
                            '-filter_complex', f"[0:v][1:v]overlay=enable='lt(t,{scenes[0]['seconds']})'[v]",
                            '-map', '[v]', '-map', '0:a', *creative_ui.FFMPEG_VIDEO, '-threads', '2',
                            '-c:a', 'copy', '-movflags', '+faststart', f'{platform}.mp4'], cwd=work, check=True, capture_output=True)
            files[platform + '_reel'] = platform + '.mp4'
            # The opening card is overlaid unzoomed; later scenes keep the reel's pushed boxes.
            native = reel_layout([[]] + marks[1:], scenes)
            native['elements'] += [{'role': r, 'box': list(b), 'start': 0, 'end': scenes[0]['seconds'], **({'text': x} if x else {})}
                                   for r, b, x in opening]
            (work / f'{platform}-layout.json').write_text(json.dumps(native, indent=1) + '\n')
            files[platform + '_reel_layout'] = f'{platform}-layout.json'
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
        for name in ('reel.mp4', 'facebook.mp4', 'tiktok.mp4'):   # the corpus export preset, on the files themselves
            export = creative_ui.media_errors(work / name)[0]
            if export:
                raise ValueError(f'{name} fails the export preset: ' + '; '.join(export))
        if narration:
            shutil.copyfile(assets.local_path(root, narration['path']), work / 'narration.wav')
            files['narration'] = 'narration.wav'
        manifest = {'version': VERSION, 'renderer_source': renderer_fingerprint(), 'runtime': runtime_fingerprint(), 'creative_id': creative_id, 'revision': revision,
                    'ui_policy_revision': creative_ui.REVISION,
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
