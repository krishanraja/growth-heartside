"""Cache brand files from exactly the synced product commit and the approved live product renders."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request
from urllib.parse import urlparse


SOURCES = {
    'logo': 'assets/heartside-logo.png',
    'display_font': 'tools/fonts/HS-Fraunces-SemiBold.ttf',
    'body_font': 'tools/fonts/DMSans-Regular.ttf',
}

# The current product renders, read from the live store's own gallery (heartside
# docs/SYNC.md: live Shopify product records are the current product truth). Each
# is a Printful mockup with an example dog, reviewed on 29 Oct 2026 at heartside
# 54b6b0e; every frame that shows one carries an Example label. Blank templates
# and checkout tiles are never used. A role whose image leaves the gallery stops
# the render instead of falling back to anything else.
PRODUCT_IMAGES = {
    'blanket': ('blanket', 'heartside-word-free-blanket-example',
                'An example of the word-free sherpa blanket, painted with an example dog.'),
    'portrait_black': ('portrait', '6adf25082493a', 'An example portrait in a black frame, painted with an example dog.'),
    'portrait_white': ('portrait', '6adf2504bc174', 'An example portrait in a white frame, painted with an example dog.'),
    'portrait_oak': ('portrait', '6adf250b670c5', 'An example portrait in a red oak frame, painted with an example dog.'),
    'portrait_unframed': ('portrait', '6ae0433aaaee2', 'An example unframed portrait, painted with an example dog.'),
    'mug_front': ('mug', '6ae2d892c1504', 'An example illustrated mug with a black interior, painted with an example dog.'),
    'mug_back': ('mug', '6ae2d897b7ba7', 'The other side of the example mug, with the painting wrapping around.'),
}


def product_image(store, role):
    """The live gallery image for an approved role: its URL, product and gift, or a ValueError."""
    gift, stem, _ = PRODUCT_IMAGES[role]
    word = re.compile(r'\b' + re.escape(gift) + r'\b', re.I)
    products = [p for p in (store or []) if word.search(p.get('title', ''))]
    if len(products) != 1:
        raise ValueError(f'the {gift} is not one product in the live catalog, so {role} cannot be used')
    images = [i for i in products[0].get('images') or []
              if urlparse(i.get('src', '')).path.rsplit('/', 1)[-1].startswith(stem)]
    if len(images) != 1:
        raise ValueError(f'the approved {role} image is no longer in the live {gift} gallery')
    return {'url': images[0]['src'], 'product': products[0]['url'], 'gift': gift}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_path(root, path):
    root = Path(root).resolve()
    candidate = (root / path).resolve()
    if not candidate.is_relative_to(root / 'local'):
        raise ValueError('generated files must stay under local/')
    return candidate


def painted(path):
    """A painted render has thousands of colors; a blank template or checkout tile has a few hundred.
    Measured on 29 Oct 2026: renders 13,000 to 36,000 at 256 px, blanks and tiles 1,000 to 2,400."""
    from PIL import Image
    with Image.open(path) as image:
        image = image.convert('RGB')
        image.thumbnail((256, 256))
        return len(image.getcolors(256 * 256) or ()) >= 8000


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'growth-heartside'}), timeout=60) as response:
        return response.read()


def prepare(root, sha, checkout=None, store=None):
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
                content = fetch(f'https://raw.githubusercontent.com/krishanraja/heartside/{sha}/{source}')
            temporary = destination.with_suffix(destination.suffix + '.tmp')
            temporary.write_bytes(content)
            temporary.replace(destination)
        records[role] = {'path': str(destination.relative_to(root)), 'sha256': sha256(destination),
                         'source': source, 'heartside_sha': sha,
                         'rights': 'Heartside brand files at the synced product commit'}
    for role, (gift, _, description) in PRODUCT_IMAGES.items():
        live = product_image(store, role)
        suffix = Path(urlparse(live['url']).path).suffix or '.img'
        destination = folder / (role + suffix)
        old = previous.get('assets', {}).get(role, {})
        if not (destination.exists() and old.get('source') == live['url'] and old.get('sha256') == sha256(destination)):
            temporary = destination.with_suffix(destination.suffix + '.tmp')
            temporary.write_bytes(fetch(live['url']))
            temporary.replace(destination)
        if not painted(destination):
            raise ValueError(f'the {role} image looks like a blank template or a tile, not a painted render')
        records[role] = {'path': str(destination.relative_to(root)), 'sha256': sha256(destination),
                         'source': live['url'], 'product': live['product'], 'gift': gift, 'heartside_sha': sha,
                         'example': True, 'description': description,
                         'rights': 'Heartside live product gallery example (a Printful mockup with an example dog); shown only with an Example label'}
    manifest = {'heartside_sha': sha, 'assets': records}
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest
