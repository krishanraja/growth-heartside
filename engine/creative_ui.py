"""House composition defaults and evidence-bound placement review, never a publisher.

Source: Social_Creative_UI_Best_Practices.docx v1, 2026-11-06.
Coordinates are starting points on the creative canvas, not platform guarantees.
Run `python -m engine.creative_ui --help` for the release check.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

REVISION = 'social-ui-2026-11-06-v1'
CRITICAL = (108, 288, 864, 1152)
SUBTITLES = (108, 960, 864, 1120)
CAPTION_SIZE = 54
MAX_CHAT_MESSAGES = 3
TIKTOK_PHOTO_BACKGROUND = (36, 32, 27)
TIKTOK_PHOTO_TEXT = (246, 241, 231)
PRESETS = {
    'instagram': {'reel': (1080, 1920), 'story': (1080, 1920), 'image': (1080, 1350), 'carousel': (1080, 1350)},
    'tiktok': {'video': (1080, 1920), 'image': (1080, 1920), 'carousel': (1080, 1920)},
    'facebook': {'reel': (1080, 1920), 'image': (1080, 1350), 'carousel': (1080, 1350)},
    'threads': {'image': (1080, 1350), 'video': (1080, 1920)},
    'x': {'image': (1080, 1350), 'video': (1080, 1920)},
    'pinterest': {'image': (1000, 1500), 'video': (1080, 1920)},
}
STATES = {'normal', 'stress', 'expanded', 'opening', 'busiest', 'ending', 'playback', 'cover'}
SURFACES = {
    'instagram': {'feed', 'profile'}, 'tiktok': {'feed', 'search_entry', 'non_owner'},
    'facebook': {'feed', 'page', 'opened_player'}, 'threads': {'timeline', 'opened_media'},
    'x': {'timeline', 'opened_media'}, 'pinterest': {'home_search', 'close_up'},
}
CHECKS = ('no_normal_overlap', 'crop_and_brand', 'sound_off', 'captions_correct',
          'native_caption_collision', 'contrast_and_phone_reading', 'reading_time',
          'concise_description', 'alt_text', 'destination', 'music_rights',
          'disclosures', 'no_fake_controls_or_watermarks', 'upload_route')
METADATA = ('asset_id', 'revision', 'platform', 'placement', 'mode', 'objective', 'account',
            'description', 'destination', 'hashtags_or_topic', 'alt_text', 'caption_route',
            'logo_variant', 'music_rights', 'disclosures', 'attachments', 'crop_anchors',
            'upload_route', 'devices', 'campaign', 'policy_revision', 'critical_region', 'exports')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_sha(path):
    with open(path, 'rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def contained(box, region=CRITICAL):
    return (isinstance(box, (list, tuple)) and len(box) == 4
            and all(type(v) in (int, float) and math.isfinite(v) for v in box)
            and region[0] <= box[0] < box[2] <= region[2]
            and region[1] <= box[1] < box[3] <= region[3])


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
        roles = set()
        for entry in exports:
            local_file(root, entry)
            roles.add(entry['role'])
            if entry['role'] in ('media', 'cover'):
                dims = entry.get('dimensions')
                if not isinstance(dims, list) or len(dims) != 2 or any(type(v) is not int or v <= 0 for v in dims):
                    raise ValueError('record export dimensions on the media canvas')
                if entry['role'] == 'media' and not contained(release.get('critical_region'), (0, 0, *dims)):
                    problems.append('critical region must fit the exported creative canvas')
        if not {'media', 'cover', 'transcript'} <= roles:
            problems.append('include media, separate cover and corrected transcript (or explicit no-speech transcript)')
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
            or not any(e.get('role') == 'cover' and e.get('sha256') == manifest['files']['cover']['sha256'] for e in release['exports'])):
        return ['placement review does not match this creative/platform/media revision']
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
