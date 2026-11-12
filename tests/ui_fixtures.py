"""Synthetic UI evidence for tests only. Never a real creative approval."""
import datetime as dt
import json
import os
from pathlib import Path
from engine import creative_ui as ui


def font_path():
    from PIL import ImageFont
    for name in ('DejaVuSans.ttf', str(Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/arial.ttf')):
        try:
            return ImageFont.truetype(name, 20).path
        except OSError:
            pass
    raise RuntimeError('install DejaVu Sans or Arial for layout tests')


def layout(**changes):
    """A synthetic layout manifest that passes the corpus profile: a hook, a subtitle and the product."""
    data = {'profile': ui.REVISION, 'canvas': [1080, 1920], 'duration': 10.0, 'ending': 'product', 'elements': [
        {'role': 'picture', 'box': [0, 0, 1080, 1920], 'start': 0, 'end': 6.5},
        {'role': 'hook', 'box': [160, 380, 800, 520], 'start': 0, 'end': 2, 'text': 'Your dog has notes'},
        {'role': 'subtitle', 'box': [130, 960, 820, 1100], 'start': 2, 'end': 6.5, 'text': 'I saw what you did', 'lines': 1, 'px': 54},
        {'role': 'product', 'box': [150, 400, 790, 1100], 'start': 6.5, 'end': 10.0}]}
    data.update(changes)
    return data


def evidence(root, asset_id='F99', revision='a' * 64, description='A concise scene.',
             media_path=None, platform='tiktok', today=dt.date(2026, 11, 6)):
    root = Path(root)
    folder = root / 'local/creative-ui' / revision
    folder.mkdir(parents=True, exist_ok=True)
    paths = {}
    for role in ('media', 'cover', 'transcript', 'capture', 'layout'):
        path = Path(media_path) if role == 'media' and media_path else folder / (role + '.bin')
        if not path.exists():
            path.write_bytes(json.dumps(layout()).encode() if role == 'layout' else ('synthetic ' + role).encode())
        paths[role] = {'path': str(path.relative_to(root)), 'sha256': ui.file_sha(path)}
    release = {key: [] for key in ui.METADATA}
    release.update(asset_id=asset_id, revision=revision, policy_revision=ui.REVISION,
                   campaign='synthetic-test', platform=platform,
                   placement='video' if platform == 'tiktok' else 'reel', mode='organic',
                   objective='test', account='synthetic account', description=description,
                   destination='', alt_text='A dog.', caption_route='corrected track',
                   logo_variant='supplied', music_rights='test licence', upload_route='test composer',
                   devices=['android'], critical_region=list(ui.CRITICAL),
                   exports=[{'role': role, **paths[role], **({'dimensions': [1080, 1920]} if role != 'transcript' else {})}
                            for role in ('media', 'cover', 'transcript', 'layout')])
    review = ui.review_stub(release)
    review.update(reviewer='synthetic test reviewer', checked_on=today.isoformat(),
                  overlay_captured_on=today.isoformat(), environment='synthetic Android viewer, version test',
                  checks={key: 'pass' for key in ui.CHECKS}, unverified=[],
                  observations=[{'device': 'android', 'state': state,
                                 'verdict': 'observed' if state == 'expanded' else 'pass',
                                 'evidence': [paths['capture']]}
                                for state in sorted(ui.STATES | ui.SURFACES[platform])])
    for suffix, content in (('release', release), ('review', review)):
        (folder / f'{asset_id}.{suffix}.json').write_text(json.dumps(content), encoding='utf-8')
    return release, review
