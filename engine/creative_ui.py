"""House composition profile and evidence-bound placement review, never a publisher.

Profile `social-corpus-2026-11-12-v2` encodes Krish's 12 Nov 2026 corpus
(knowledge/social-media-creative-production-corpus-2026-11-12.md): "Ensure all
social media posts adhere to these best practices." It supersedes the 6 Nov
profile `social-ui-2026-11-06-v1`, whose coordinates are kept below only to read
old evidence. Every coordinate here is a house rule on the creative canvas, not a
platform guarantee: the native preview still decides (corpus, section 3.5).

Renderers record what they draw in a layout manifest; `layout_errors` checks it
against the named regions, and `export_errors` checks the encoded file against
the export preset. Run `python -m engine.creative_ui --help` for the release check.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

REVISION = 'social-corpus-2026-11-12-v2'
CORPUS = 'knowledge/social-media-creative-production-corpus-2026-11-12.md'
CORPUS_SHA256 = '483cf6c3ed3889e8b57279115fa31f9dc948ddb49e7e858aef3d94a2adeb5c93'
LEGACY = {'social-ui-2026-11-06-v1': {'critical': (108, 288, 864, 1152), 'subtitles': (108, 960, 864, 1120)}}

# 1080x1920 regions, corpus section 3.5 (house rule, deliberately narrower than the screen).
VERTICAL = (1080, 1920)
CRITICAL = (120, 330, 820, 1180)      # every hook, subtitle, label, chat, face, product detail and mark
HOOK = (140, 360, 820, 720)           # the opening hook: seen early, clear of top tabs and the right rail
SUBTITLES = (130, 940, 820, 1160)     # timed subtitles: above the bottom metadata, left of the action stack
LOGO = (140, 360, 780, 940)           # a small credit, only if essential; never a watermark at bottom right
FINAL_LINE = (140, 820, 820, 1150)    # a closing payoff line; organic posts carry no on-screen CTA (Krish, 2 Nov)
COVER_GRID = (0, 240, 1080, 1680)     # central 3:4 profile-grid preview model for a 9:16 cover (section 7)

# Feed assets (4:5, 3:4, 1:1): a 70 to 100 px design margin, not an app overlay (section 8).
FEED_INSET = 70
FEED_MARGIN = 90

# Words on screen (sections 4 and 6.1).
CAPTION_SIZE = 54
CAPTION_PX = (44, 64)
CAPTION_LINES = 2
CAPTION_WORDS = 7                     # words per timed subtitle segment
CAPTION_LINE_HEIGHT = 64
HOOK_WORDS = 12                       # hard ceiling; 3 to 7 is the target
HOOK_TARGET_WORDS = 7
HOOK_WINDOW = 3.0                     # the value is visible in the first 3 seconds
TITLE_BEAT = (0.5, 1.5)               # a title beat, never a 3 to 5 second splash
# Krish's floor `endings-land` holds the real product at least 3 s; the corpus
# forbids a long dead outro, so the product end beat is 3 to 4 s and keeps moving.
END_HOLD = (3.0, 4.0)
MAX_CHAT_MESSAGES = 3
TIKTOK_PHOTO_BACKGROUND = (36, 32, 27)
TIKTOK_PHOTO_TEXT = (246, 241, 231)

# Export preset, section 10 (house rule compatible with the platforms' published recommendations).
EXPORT = {'video_codec': 'h264', 'pix_fmt': 'yuv420p', 'fps': (23.9, 60.0), 'audio_codec': 'aac',
          'sample_rate': 48000, 'channels': 2, 'video_mbps': (8.0, 12.0), 'true_peak_dbtp': -1.0,
          'color': 'bt709'}
# Quality-based with a 12 Mbps ceiling: x264 cannot fill flat or still frames up to 8 Mbps without
# filler data the platforms strip, so a low rate on a still is a reviewer note, never padded.
FFMPEG_VIDEO = ['-c:v', 'libx264', '-preset', 'medium', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                '-r', '30', '-crf', '18', '-maxrate', '12M', '-bufsize', '24M',
                '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709']
FFMPEG_AUDIO = ['-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '192k']

PRESETS = {
    'instagram': {'reel': (1080, 1920), 'story': (1080, 1920), 'image': (1080, 1350), 'carousel': (1080, 1350),
                  'image_3x4': (1080, 1440), 'image_1x1': (1080, 1080)},
    'tiktok': {'video': (1080, 1920), 'image': (1080, 1920), 'carousel': (1080, 1920)},
    'facebook': {'reel': (1080, 1920), 'story': (1080, 1920), 'image': (1080, 1350), 'carousel': (1080, 1350),
                 'image_1x1': (1080, 1080)},
    # Preparation guidance only: these channels are not active for Heartside.
    'youtube': {'short': (1080, 1920), 'video': (1920, 1080), 'thumbnail': (1280, 720), 'community': (1080, 1080)},
    'threads': {'image': (1080, 1350), 'video': (1080, 1920)},
    'x': {'image': (1080, 1350), 'video': (1080, 1920)},
    'pinterest': {'image': (1000, 1500), 'video': (1080, 1920)},
}
FEED = {(1080, 1350), (1080, 1440), (1080, 1080)}
STATES = {'normal', 'stress', 'expanded', 'opening', 'busiest', 'ending', 'playback', 'cover'}
SURFACES = {
    'instagram': {'feed', 'profile'}, 'tiktok': {'feed', 'search_entry', 'non_owner'},
    'facebook': {'feed', 'page', 'opened_player'}, 'youtube': {'shorts_player', 'channel_tab'},
    'threads': {'timeline', 'opened_media'}, 'x': {'timeline', 'opened_media'},
    'pinterest': {'home_search', 'close_up'},
}
CHECKS = ('no_normal_overlap', 'crop_and_brand', 'sound_off', 'captions_correct',
          'native_caption_collision', 'contrast_and_phone_reading', 'reading_time',
          'concise_description', 'alt_text', 'destination', 'music_rights',
          'disclosures', 'no_fake_controls_or_watermarks', 'upload_route')
METADATA = ('asset_id', 'revision', 'platform', 'placement', 'mode', 'objective', 'account',
            'description', 'destination', 'hashtags_or_topic', 'alt_text', 'caption_route',
            'logo_variant', 'music_rights', 'disclosures', 'attachments', 'crop_anchors',
            'upload_route', 'devices', 'campaign', 'policy_revision', 'critical_region', 'exports')

# Layout manifest roles. `background` and `picture` may fill the canvas (full bleed is allowed);
# everything else is critical content and must sit inside its region.
ROLES = {'background', 'picture', 'product', 'text', 'hook', 'subtitle', 'label', 'chat', 'title', 'logo'}
WORDS = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\u2019.,:%$-]*")


def words(text):
    return len(WORDS.findall(text or ''))


def inside(box, region):
    return (isinstance(box, (list, tuple)) and len(box) == 4
            and all(type(v) in (int, float) and math.isfinite(v) for v in box)
            and region[0] <= box[0] < box[2] <= region[2]
            and region[1] <= box[1] < box[3] <= region[3])


def _overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def layout_errors(layout):
    """Check a renderer's layout manifest against the corpus. Returns (problems, notes).

    Problems hold the post. Notes are recorded for the reviewer: house targets the corpus states as
    "usually" or "around", which a person judges on the frame. Pixels are never inferred here; the
    manifest is what the renderer drew, so a renderer that does not write one cannot pass.
    """
    problems, notes = [], []
    try:
        if not isinstance(layout, dict):
            raise ValueError('layout manifest must be an object')
        if layout.get('profile') != REVISION:
            problems.append(f"layout drawn under {layout.get('profile') or 'no profile'}, not {REVISION}: rebuild it")
        canvas = tuple(layout.get('canvas') or ())
        duration = float(layout.get('duration') or 0)
        elements = layout.get('elements')
        if not isinstance(elements, list) or not elements:
            raise ValueError('layout manifest lists no elements')
        vertical, feed = canvas == VERTICAL, canvas in FEED
        if not (vertical or feed):
            raise ValueError(f'unsupported canvas {canvas}')
        labels = set()
        for i, e in enumerate(elements):
            role, box = e.get('role'), e.get('box')
            name = f"{role} {e.get('text', '')!r}"[:80] if e.get('text') else str(role)
            if role not in ROLES:
                problems.append(f'element {i}: unknown role {role}'); continue
            if not inside(box, (0, 0, *canvas)):
                problems.append(f'{name}: box {box} is off the {canvas[0]}x{canvas[1]} canvas'); continue
            start, end = float(e.get('start', 0)), float(e.get('end', duration or 0))
            if end < start:
                problems.append(f'{name}: ends before it starts')
            if role in ('background', 'picture'):
                focus = e.get('focus')
                if focus is not None and vertical and not inside(focus, CRITICAL):
                    problems.append(f'{name}: its subject {focus} sits outside the critical box {CRITICAL}')
                continue
            if vertical:
                region = LOGO if role == 'logo' else CRITICAL
                if not inside(box, region):
                    problems.append(f'{name}: {[round(v) for v in box]} leaves the {"logo" if role == "logo" else "critical"} region {region}')
            else:
                region = (FEED_INSET, FEED_INSET, canvas[0] - FEED_INSET, canvas[1] - FEED_INSET)
                if role not in ('product',) and not inside(box, region):
                    problems.append(f'{name}: {[round(v) for v in box]} breaks the {FEED_INSET} px feed margin')
            if role == 'subtitle':
                if e.get('lines', 1) > CAPTION_LINES:
                    problems.append(f'{name}: {e["lines"]} lines (at most {CAPTION_LINES})')
                if words(e.get('text')) > CAPTION_WORDS:
                    problems.append(f'{name}: {words(e.get("text"))} words in one timed segment (at most {CAPTION_WORDS})')
                px = e.get('px')
                if px is not None and not CAPTION_PX[0] <= px <= CAPTION_PX[1]:
                    problems.append(f'{name}: {px} px type (house range {CAPTION_PX[0]} to {CAPTION_PX[1]})')
                if vertical and not inside(box, SUBTITLES):
                    notes.append(f'{name}: outside the subtitle band {SUBTITLES} (moved to protect a face or product; check the frame)')
            if role == 'hook' and start < HOOK_WINDOW:
                n = words(e.get('text'))
                if n > HOOK_WORDS:
                    problems.append(f'{name}: {n} words in the opening hook (at most {HOOK_WORDS})')
                elif n > HOOK_TARGET_WORDS:
                    notes.append(f'{name}: {n} words in the opening hook (target 3 to {HOOK_TARGET_WORDS})')
                if vertical and not inside(box, HOOK):
                    notes.append(f'{name}: opening hook outside the hook region {HOOK}')
            if role == 'label':
                labels.add(round(box[1] / 4))
        if len(labels) > 1:
            problems.append('labels move between shots: keep one fixed position for the whole reel (floor fixed-label-position)')
        # Words that share the screen must not collide (hooks and captions need separate places).
        texty = [e for e in elements if e.get('role') in ('hook', 'subtitle', 'label', 'text', 'title', 'chat', 'logo')]
        for a in range(len(texty)):
            for b in range(a + 1, len(texty)):
                x, y = texty[a], texty[b]
                if (float(x.get('start', 0)) < float(y.get('end', duration)) and float(y.get('start', 0)) < float(x.get('end', duration))
                        and _overlap(x['box'], y['box'])):
                    problems.append(f"{x['role']} and {y['role']} overlap on screen at the same time")
        if duration:
            opening = [e for e in elements if float(e.get('start', 0)) <= 0.05 and e.get('role') not in ('background', 'logo')]
            if not opening:
                problems.append('frame 1 shows only a background or a logo: open on the story (no logo-only cold open)')
            if layout.get('ending') == 'product':
                last = [e for e in elements if e.get('role') == 'product' and abs(float(e.get('end', duration)) - duration) < 0.1]
                held = max((duration - float(e.get('start', 0)) for e in last), default=0)
                if not last:
                    problems.append('the post does not end on the real product')
                elif not END_HOLD[0] - 0.05 <= held <= END_HOLD[1] + 0.05:
                    problems.append(f'product end beat {held:.1f} s (want {END_HOLD[0]:.0f} to {END_HOLD[1]:.0f} s: held, never a dead outro)')
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        problems.append('layout manifest unreadable: ' + str(exc))
    return problems, notes


def segments(text, start, end, max_words=CAPTION_WORDS):
    """Split a spoken line into timed subtitle segments of at most `max_words` words (corpus 6.1),
    breaking at phrase ends where possible and never leaving one word alone. Time is shared by words."""
    words_ = text.split()
    if not words_:
        return []
    chunks, i = [], 0
    while i < len(words_):
        rest = len(words_) - i
        if rest <= max_words:
            chunks.append(words_[i:]); break
        size = max_words
        if rest - size == 1:   # never strand a single word in the last segment
            size -= 1
        for k in range(size, 2, -1):   # prefer to end on punctuation
            if words_[i + k - 1].endswith(('.', '?', ',', ';', ':')) and rest - k != 1:
                size = k; break
        chunks.append(words_[i:i + size]); i += size
    total, out, t = len(words_), [], start
    for c in chunks:
        span = (end - start) * len(c) / total
        out.append((' '.join(c), t, t + span)); t += span
    return out


def probe_media(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def true_peak(path):
    err = subprocess.run(['ffmpeg', '-nostats', '-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    found = re.findall(r'Peak:\s+(-?[\d.]+|-inf) dBFS', err)
    return float(found[-1]) if found and found[-1] != '-inf' else None


def _rate(value):
    num, _, den = str(value or '0/1').partition('/')
    return float(num) / float(den or 1) if float(den or 1) else 0.0


def export_errors(info, peak=None):
    """Check an ffprobe result against the export preset. Returns (problems, notes)."""
    problems, notes = [], []
    streams = info.get('streams', [])
    video = next((s for s in streams if s.get('codec_type') == 'video'), None)
    audio = next((s for s in streams if s.get('codec_type') == 'audio'), None)
    if not video:
        return ['no video stream'], notes
    if video.get('codec_name') != EXPORT['video_codec']:
        problems.append(f"video codec {video.get('codec_name')} (want H.264)")
    if video.get('pix_fmt') != EXPORT['pix_fmt']:
        problems.append(f"pixel format {video.get('pix_fmt')} (want yuv420p)")
    if video.get('field_order') not in (None, 'progressive', 'unknown'):
        problems.append('interlaced video (want progressive)')
    fps, avg = _rate(video.get('r_frame_rate')), _rate(video.get('avg_frame_rate'))
    if not EXPORT['fps'][0] <= fps <= EXPORT['fps'][1]:
        problems.append(f'{fps:.2f} fps (want 24 to 60, the source rate)')
    elif avg and abs(avg - fps) > 0.5:
        problems.append(f'variable frame rate ({avg:.2f} average against {fps:.2f})')
    for key in ('color_primaries', 'color_transfer', 'color_space'):
        if video.get(key) not in (None, 'unknown', 'bt709', 'bt470bg', 'smpte170m'):
            problems.append(f"{key} {video.get(key)} (want BT.709 SDR)")
    duration = float(info.get('format', {}).get('duration') or video.get('duration') or 0)
    rate = float(video.get('bit_rate') or 0) / 1e6
    if rate:
        if rate > EXPORT['video_mbps'][1] * 1.1:
            problems.append(f'video {rate:.1f} Mbps (working default 8 to 12)')
        elif rate < EXPORT['video_mbps'][0] * 0.75:
            notes.append(f'video {rate:.1f} Mbps, under the 8 to 12 working default: fine for still or flat frames; check motion for blocking')
    if not audio:
        problems.append('no audio stream')
    else:
        if audio.get('codec_name') != EXPORT['audio_codec']:
            problems.append(f"audio codec {audio.get('codec_name')} (want AAC)")
        if int(audio.get('sample_rate') or 0) != EXPORT['sample_rate']:
            problems.append(f"audio {audio.get('sample_rate')} Hz (want 48000)")
        if int(audio.get('channels') or 0) != EXPORT['channels']:
            problems.append(f"{audio.get('channels')} audio channels (want stereo)")
    if peak is not None and peak > EXPORT['true_peak_dbtp']:
        problems.append(f'true peak {peak:.1f} dBTP (clipping risk; keep at or under {EXPORT["true_peak_dbtp"]:.0f})')
    return problems, notes


def media_errors(path):
    """The export preset on an encoded file, probed live."""
    try:
        return export_errors(probe_media(path), true_peak(path))
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        return ['media unreadable: ' + str(exc)], []


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_sha(path):
    with open(path, 'rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def contained(box, region=CRITICAL):
    return inside(box, region)


def local_file(root, entry):
    root = Path(root).resolve()
    path = (root / entry['path']).resolve()
    if not path.is_relative_to(root) or not path.is_file() or file_sha(path) != entry['sha256']:
        raise ValueError('missing, outside workspace, or changed evidence/export')
    return path


def review_stub(release):
    """Unreviewed by construction: never populate a pass from a clean render."""
    return {'binding': digest(release), 'reviewer': '', 'checked_on': '',
            'overlay_captured_on': '', 'environment': '', 'campaign': release.get('campaign'),
            'checks': {key: 'unverified' for key in CHECKS}, 'observations': [],
            'unverified': ['native preview and viewer states have not been inspected']}


def errors(root, release, review, today=None):
    """Validate attestations + exact evidence bytes; cannot judge screenshot semantics."""
    problems = []
    today = today or dt.date.today()
    try:
        if not isinstance(release, dict) or not isinstance(review, dict):
            raise ValueError('release and review must be objects')
        missing = [k for k in METADATA if k not in release]
        if missing:
            problems.append('missing handoff fields: ' + ', '.join(missing))
        for key in ('asset_id', 'revision', 'objective', 'account', 'upload_route', 'campaign', 'caption_route', 'logo_variant', 'music_rights'):
            if (not isinstance(release.get(key), str) or not release[key].strip()
                    or release[key].startswith('replace-with-')):
                problems.append('complete ' + key)
        for key in ('description', 'destination', 'alt_text'):
            if not isinstance(release.get(key), str):
                problems.append(key + ' must be text (empty only when inapplicable)')
        for key in ('hashtags_or_topic', 'disclosures', 'attachments', 'crop_anchors'):
            if not isinstance(release.get(key), list):
                problems.append(key + ' must be a list')
        platform, placement = release.get('platform'), release.get('placement')
        if placement not in PRESETS.get(platform, {}):
            problems.append('unsupported platform/placement')
        if release.get('mode') not in ('organic', 'paid'):
            problems.append('name organic or paid explicitly')
        if release.get('policy_revision') != REVISION:
            problems.append('refresh the placement policy revision')
        exports = release.get('exports')
        if not isinstance(exports, list) or not exports:
            raise ValueError('export, separate cover and transcript must be declared')
        roles, media_dims = set(), None
        for entry in exports:
            path = local_file(root, entry)
            roles.add(entry['role'])
            if entry['role'] in ('media', 'cover'):
                dims = entry.get('dimensions')
                if not isinstance(dims, list) or len(dims) != 2 or any(type(v) is not int or v <= 0 for v in dims):
                    raise ValueError('record export dimensions on the media canvas')
                if entry['role'] == 'media':
                    media_dims = tuple(dims)
                    region = release.get('critical_region')
                    if not contained(region, (0, 0, *dims)):
                        problems.append('critical region must fit the exported creative canvas')
                    elif media_dims == VERTICAL and not contained(region, CRITICAL):
                        problems.append(f'critical region {region} is wider than the corpus box {CRITICAL}')
                    elif media_dims in FEED and not contained(region, (FEED_INSET, FEED_INSET, dims[0] - FEED_INSET, dims[1] - FEED_INSET)):
                        problems.append(f'critical region {region} breaks the {FEED_INSET} px feed margin')
            if entry['role'] == 'layout':
                found, _ = layout_errors(json.loads(path.read_text(encoding='utf-8')))
                problems += ['layout: ' + p for p in found]
        if not {'media', 'cover', 'transcript', 'layout'} <= roles:
            problems.append("include media, separate cover, corrected transcript (or explicit no-speech transcript) and the renderer's layout manifest")
        devices = release.get('devices')
        if not isinstance(devices, list) or not devices or not set(devices) <= {'android', 'ios', 'desktop'}:
            raise ValueError('declare devices actually required for this release')
        if review.get('binding') != digest(release):
            problems.append('export/copy/account/placement changed since review')
        if review.get('campaign') != release.get('campaign'):
            problems.append('review belongs to a different campaign')
        for key in ('reviewer', 'environment'):
            if not isinstance(review.get(key), str) or not review[key].strip():
                problems.append('record ' + key)
        checked = dt.date.fromisoformat(review.get('checked_on', ''))
        captured = dt.date.fromisoformat(review.get('overlay_captured_on', ''))
        if not captured <= checked <= today or (today - checked).days > 31 or (today - captured).days > 31:
            problems.append('preview/overlay is future-dated or older than 31 days; inspect again')
        if any(review.get('checks', {}).get(k) != 'pass' for k in CHECKS):
            problems.append('every release checklist item needs an evidenced pass')
        if review.get('unverified') != []:
            problems.append('required viewer evidence remains unverified')
        required = STATES | SURFACES.get(platform, set())
        if placement in ('carousel', 'image'):
            required |= {'all_slides'}
        if placement == 'story':
            required |= {'stickers'}
        if release.get('mode') == 'paid':
            required |= {'ad_preview'}
        seen = set()
        for observation in review.get('observations', []):
            if observation.get('verdict') != ('observed' if observation.get('state') == 'expanded' else 'pass'):
                problems.append('viewer observation held or unverified')
            evidence = observation.get('evidence')
            if not isinstance(evidence, list) or not evidence:
                problems.append('each state needs captured evidence')
            else:
                for entry in evidence:
                    local_file(root, entry)
            seen.add((observation['device'], observation['state']))
        for device in devices:
            absent = required - {s for d, s in seen if d == device}
            if absent:
                problems.append(device + ' missing states: ' + ', '.join(sorted(absent)))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        problems.append('incomplete or invalid placement review: ' + str(exc))
    return problems


def check_files(root, release_path, review_path, expected_media=None, expected_copy=None, today=None, expected_asset_id=None):
    try:
        release = json.loads(Path(release_path).read_text(encoding='utf-8'))
        review = json.loads(Path(review_path).read_text(encoding='utf-8'))
        problems = errors(root, release, review, today=today)
        if expected_media and not any(e.get('role') == 'media' and e.get('sha256') == file_sha(expected_media)
                                      for e in release.get('exports', [])):
            problems.append('review does not cover the file being released')
        if expected_copy is not None and release.get('description') != expected_copy:
            problems.append('review does not cover the final publishing copy')
        if expected_asset_id is not None and release.get('asset_id') != expected_asset_id:
            problems.append('review belongs to another asset')
        return problems
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        return ['placement review unavailable: ' + str(exc)]


def proposal_errors(root, creative_id, revision, item, manifest, today=None):
    base = Path(root) / 'local/creative-ui' / revision / creative_id
    problems = check_files(root, str(base) + '.release.json', str(base) + '.review.json', expected_copy=item['text'], today=today)
    if problems:
        return problems
    release = json.loads(Path(str(base) + '.release.json').read_text(encoding='utf-8'))
    role = {'instagram': 'reel', 'facebook': 'facebook_reel', 'tiktok': 'tiktok_reel'}.get(item['platform'])
    if (release['asset_id'] != creative_id or release['revision'] != revision
            or release['platform'] != item['platform'] or release['mode'] != 'organic'
            or release['alt_text'] != item.get('alt_text', '')
            or not role or release['placement'] != ('video' if item['platform'] == 'tiktok' else 'reel')
            or not any(e.get('role') == 'media' and e.get('sha256') == manifest['files'][role]['sha256'] for e in release['exports'])
            or not any(e.get('role') == 'cover' and e.get('sha256') == manifest['files']['cover']['sha256'] for e in release['exports'])
            or not any(e.get('role') == 'layout' and e.get('sha256') == manifest['files'].get(role + '_layout', {}).get('sha256')
                       for e in release['exports'])):
        return ['placement review does not match this creative/platform/media/layout revision']
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['stub', 'check'])
    parser.add_argument('release', type=Path)
    parser.add_argument('review', type=Path)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    if args.command == 'stub':
        # Exclusive creation protects prior review evidence.
        with args.review.open('x', encoding='utf-8') as handle:
            json.dump(review_stub(json.loads(args.release.read_text(encoding='utf-8'))), handle, indent=2)
        return
    problems = check_files(args.root, args.release, args.review)
    print('\n'.join('HOLD: ' + p for p in problems) if problems else 'PASS: exact placement evidence recorded; publication still needs approval')
    raise SystemExit(bool(problems))


if __name__ == '__main__':
    main()
