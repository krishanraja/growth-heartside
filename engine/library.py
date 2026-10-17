"""Build a portable campaign library from checked production outputs only."""
from contextlib import closing
import html
import json
from pathlib import Path
import tempfile
import zipfile

from . import assets, ledger, media, review


def build(root, state, checker, checkout=None, day=None):
    root = Path(root).resolve()
    out = assets.local_path(root, 'local/handoff'); out.mkdir(parents=True, exist_ok=True)
    records = []
    bank = sorted((root / 'campaigns').glob('*.json'))
    if len(bank) != 7:
        raise ValueError('the library expects the seven reviewed campaign concepts')
    with closing(ledger.connect(root / 'local/engine.sqlite3')) as db:
        for path in bank:
            spec = json.loads(path.read_text())
            pack, manifest = media.render(root, spec, state, checker, checkout, day)
            errors = media.verify(root, pack['production'], pack)
            if errors:
                raise ValueError('; '.join(errors))
            for item in pack['items']:
                ledger.record_render(db, item['creative_id'], manifest['revision'], spec, manifest)
            name = spec['concept']
            archive = out / 'campaigns' / (name + '.zip')
            review.bundle(root, pack, str(archive.relative_to(root)))
            records.append({'concept': name, 'headline': pack['headline'], 'creative_id': manifest['creative_id'],
                            'revision': manifest['revision'], 'files': len(manifest['files'])})
    target = out / 'heartside-campaign-library.zip'
    with tempfile.NamedTemporaryFile(dir=out, suffix='.zip', delete=False) as temporary:
        temporary = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as library:
            for record in records:
                concept = record['concept']
                with zipfile.ZipFile(out / 'campaigns' / (concept + '.zip')) as campaign:
                    for name in campaign.namelist():
                        if Path(name).name != name:
                            raise ValueError('review bundle contains a nonlocal path')
                        library.writestr(concept + '/' + name, campaign.read(name))
            cards = ''.join(f'<article><a href="{r["concept"]}/review.html"><img alt="Draft Heartside campaign {r["concept"]}" src="{r["concept"]}/cover.png"><h2>{html.escape(r["headline"])}</h2></a></article>' for r in records)
            page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Heartside campaign library</title><style>body{font:17px/1.5 system-ui;margin:32px auto;padding:0 20px;max-width:1100px;background:#fbf6f1;color:#211b18}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}img{width:100%;max-height:450px;object-fit:contain}h2{font-size:18px}a{color:#6b3043}article{padding:16px;background:white;border-radius:12px}</style><h1>Gifts from the dog</h1><p>Seven campaign drafts. Choose a concept, open its review pack, watch the native films and download its files and captions. Each includes synthetic narration and clearly fictional Biscuit examples. Review before posting by hand.</p><main>''' + cards + '</main></html>'
            library.writestr('index.html', page)
            library.writestr('library-index.json', json.dumps(records, indent=2))
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return {'path': str(target.relative_to(root)), 'sha256': assets.sha256(target),
            'campaigns': len(records), 'media_files': sum(r['files'] for r in records),
            'heartside_sha': state['sha'], 'needs_human_review': True}
