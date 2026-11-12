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
# docs/SYNC.md: live Shopify product records are the current product truth).
# Re-pinned on 12 Nov 2026 at heartside 88b8a61 to the gallery pictures Krish
# approved for the three gift pages on 30 and 31 Oct (heartside
# docs/history/LOG.md): the Printful mockups pinned on 29 Oct had left the
# galleries, so every daily pack stopped until then. The blanket and the four
# portrait finishes show the same example black Labrador, so a film that moves
# between them keeps one dog; the portrait finishes are Printful's own photos,
# held up by its model, with the painting composited in. The two mugs show the
# store's lead example dog. Each is shown whole, its pixels unaltered and with
# no badge or label (Krish, 2 Nov: "We never need EXAMPLE badges anywhere"),
# and never as a customer's dog. Blank templates and checkout tiles are never
# used. A role whose image leaves the gallery stops the render instead of
# falling back to anything else; the runner records why (engine/runner.py).
PRODUCT_IMAGES = {
    'blanket': ('blanket', 'home-4x5', 'A word-free sherpa blanket on a sofa, painted with an example black Labrador.'),
    'portrait_black': ('portrait', 'portrait-black', 'A portrait in a black frame, painted with an example black Labrador.'),
    'portrait_white': ('portrait', 'portrait-white', 'A portrait in a white frame, painted with an example black Labrador.'),
    'portrait_oak': ('portrait', 'portrait-red-oak', 'A portrait in a red oak frame, painted with an example black Labrador.'),
    'portrait_unframed': ('portrait', 'portrait-unframed', 'An unframed portrait on a wall, painted with an example black Labrador.'),
    'mug_black': ('mug', 'mug-real-golden', 'An illustrated mug with a black handle and interior, painted with an example golden retriever.'),
    'mug_pink': ('mug', 'mug-pink', 'The same illustrated mug with a pink handle and interior, one of its five colors.'),
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
                         'rights': 'Heartside live product gallery picture with an example dog, approved by Krish for the gift page; shown unaltered with no label'}
    manifest = {'heartside_sha': sha, 'assets': records}
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest
