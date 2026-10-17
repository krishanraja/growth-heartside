"""A downloadable review artifact, not another hosted dashboard or publisher."""
import html
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from . import assets, media


def bundle(root, pack, destination):
    errors = media.verify(root, pack.get('production'), pack)
    if errors:
        raise ValueError('; '.join(errors))
    manifest = json.loads(assets.local_path(root, pack['production']['manifest']).read_text())
    destination = assets.local_path(root, destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
        stage = Path(temporary)
        (stage / 'pack.json').write_text(json.dumps(pack, indent=2) + '\n')
        (stage / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        licenses = Path(root) / 'docs/VOICE-LICENSES.md'
        if licenses.exists():
            shutil.copyfile(licenses, stage / 'voice-provenance.md')
        links = []
        for role, entry in manifest['files'].items():
            source = assets.local_path(root, entry['path'])
            name = role + source.suffix
            shutil.copyfile(source, stage / name)
            links.append(f'<li><a download href="{html.escape(name)}">{html.escape(role)}</a></li>')
        entries = []
        for item in pack['items']:
            text = html.escape(item['text'])
            alt = html.escape(item.get('alt_text', ''))
            entries.append(f'<article><h2>{html.escape(item["creative_id"])}</h2><pre>{text}</pre><details><summary>Alt text</summary><pre>{alt}</pre></details></article>')
        content = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Heartside creative review</title><style>body{{font:17px/1.5 system-ui;margin:24px auto;max-width:900px;padding:0 16px;background:#fbf6f1;color:#211b18}}video{{width:100%;max-height:70vh}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}article{{border-top:1px solid #d8cfc7;margin:24px 0}}h2{{font-size:16px;overflow-wrap:anywhere}}a{{color:#6b3043}}</style>
<h1>{html.escape(pack['headline'])}</h1><p>Draft only. Review product truth, legibility, spelling, audio and the AI example disclosure. Nothing is approved or published by generation.</p>
<video controls preload="metadata" poster="cover.png" src="reel.mp4"></video><h2>Download native files</h2><ul>{''.join(links)}</ul>
<p>Instagram: reel.mp4 and cover.png. Facebook: facebook_reel.mp4. TikTok: tiktok_reel.mp4. Stories: story_1 to story_3. Pinterest: pin_1 and pin_2. Carousel: carousel_1 to carousel_3. Captions are below.</p>
<p>Product source: {html.escape(manifest['heartside_sha'])}<br>Creative revision: {html.escape(manifest['revision'])}<br>Audio: {html.escape(manifest['audio'])}</p>{''.join(entries)}
<p>After reviewing, use growth.py creatives mark with the exact creative ID and revision. Record a real platform URL only after publishing by hand. A new revision requires a new review.</p></html>'''
        (stage / 'review.html').write_text(content)
        with zipfile.ZipFile(destination.with_suffix('.tmp'), 'w', zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(stage.iterdir()):
                archive.write(file, file.name)
        destination.with_suffix('.tmp').replace(destination)
    return {'path': str(destination.relative_to(root)), 'sha256': assets.sha256(destination), 'creative_revision': manifest['revision']}
