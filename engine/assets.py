"""Cache approved product assets from exactly the synced product commit."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request


SOURCES = {
    'mug_dog': 'docs/evidence/cowork-2026-10-15/mug/shopify-image-1-dog-face.jpg',
    'mug_note': 'docs/evidence/cowork-2026-10-15/mug/shopify-image-2-note-face.jpg',
    'biscuit': 'assets/v2/biscuit-headshot.jpg',
    'logo': 'assets/heartside-logo.png',
    'display_font': 'tools/fonts/HS-Fraunces-SemiBold.ttf',
    'body_font': 'tools/fonts/DMSans-Regular.ttf',
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_path(root, path):
    root = Path(root).resolve()
    candidate = (root / path).resolve()
    if not candidate.is_relative_to(root / 'local'):
        raise ValueError('generated files must stay under local/')
    return candidate


def prepare(root, sha, checkout=None):
    if not re.fullmatch('[0-9a-f]{40}', sha or ''):
        raise ValueError('assets require the full synced product commit')
    folder = local_path(root, 'local/assets/' + sha)
    manifest_path = folder / 'manifest.json'
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    records = {}
    folder.mkdir(parents=True, exist_ok=True)
    for role, source in SOURCES.items():
        destination = folder / (role + Path(source).suffix)
        old = previous.get('assets', {}).get(role, {})
        if not (destination.exists() and old.get('sha256') == sha256(destination)):
            if checkout:
                result = subprocess.run(['git', '-C', str(Path(checkout).resolve()), 'show', f'{sha}:{source}'],
                                        capture_output=True, check=True)
                content = result.stdout
            else:
                url = f'https://raw.githubusercontent.com/krishanraja/heartside/{sha}/{source}'
                with urllib.request.urlopen(url, timeout=60) as response:
                    content = response.read()
            temporary = destination.with_suffix(destination.suffix + '.tmp')
            temporary.write_bytes(content)
            temporary.replace(destination)
        records[role] = {'path': str(destination.relative_to(root)), 'sha256': sha256(destination),
                         'source': source, 'heartside_sha': sha,
                         'rights': 'Heartside approved example assets; see product canon and assets/README.md'}
    # A generated fictional scene lives in this growth repository, never in the
    # product asset catalog. Its provenance and visible disclosure remain explicit.
    fictional = Path(root) / 'assets/fictional/biscuit-entryway.json'
    if fictional.exists():
        provenance = json.loads(fictional.read_text())
        source_path = Path(root) / provenance['path']
        if sha256(source_path) != provenance['sha256']:
            raise ValueError('fictional source asset checksum changed')
        destination = folder / 'biscuit_entryway.png'
        destination.write_bytes(source_path.read_bytes())
        records['biscuit_entryway'] = {**provenance, 'path': str(destination.relative_to(root)), 'heartside_sha': sha}
    manifest = {'heartside_sha': sha, 'assets': records}
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest
