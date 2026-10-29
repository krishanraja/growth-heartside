"""Acceptance checks for heartside's breed example batch, made by Codex in this repository.

Heartside's brief (design/examples-2026-10-29-breeds/README.md at the pinned
commit) says what to make. This checks that what came back is exactly that:
the names, sizes, transparency, counts, limits, credits and manifest. Whether a
painting is the right dog, in its tone, with no words, stays a person's review.
"""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = 'assets/heartside-examples-2026-10-29'
HEARTSIDE_COMMIT = 'eccc695c44d98008d5989bd118089acd762e465f'  # branch claude/product-launch-readiness-mlh1bc
BATCH = 'design/examples-2026-10-29-breeds'
JOBS_SHA256 = '84b831df9ceed6a904e1d0d455c9369f6a3a91ee0d318304c1439048a1205445'
RATIOS = {'1x1': (1080, 1080), '4x5': (1080, 1350), '9x16': (1080, 1920)}
SCENES = ('studio', 'home', 'hand')
KINDS = {'painting', 'cutout', 'crop', 'mockup', 'set'}
USES = {'site', 'ad', 'social', 'character'}
GIFTS = {'mug', 'blanket', 'portrait'}
PHOTO_HOSTS = ('unsplash.com', 'pexels.com')
LIMITS = {1: {'painting': 6, 'cutout': 6, 'scene': 18, 'set': 0},
          2: {'painting': 18, 'cutout': 18, 'scene': 54, 'set': 6}}
RECORDS = {'manifest.json', 'credits.json', 'failures.json', 'review.md', 'jobs.json', 'README.md'}


def batch(root):
    """The job list at the pinned heartside commit, kept beside the assets."""
    local = Path(root) / ROOT / 'jobs.json'
    if not local.exists():
        url = f'https://raw.githubusercontent.com/krishanraja/heartside/{HEARTSIDE_COMMIT}/{BATCH}/jobs.json'
        with urllib.request.urlopen(url, timeout=60) as response:
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(response.read())
    if hashlib.sha256(local.read_bytes()).hexdigest() != JOBS_SHA256:
        raise ValueError(f'{ROOT}/jobs.json is not the job list at heartside {HEARTSIDE_COMMIT[:7]}; delete it and run again')
    return json.loads(local.read_text())['jobs']


def expected(jobs, stage, only=None):
    """Every file the stage should produce (or just one job's, for a pilot), with what each must be."""
    out = {}
    chosen = [j for j in jobs if j['stage'] <= stage and (only is None or j['id'] == only)]
    for job in chosen:
        size = tuple(int(x) for x in job['size'].split('x'))
        meta = {'job': job['id'], 'breed': job['breed'], 'style': job['style'], 'tone': job['tone'], 'gift': job['format']}
        out[f'photos/{job["dog"]}.jpg'] = {'kind': 'photo', 'dog': job['dog']}
        out[f'paintings/{job["id"]}.png'] = {**meta, 'kind': 'painting', 'size': size}
        out[f'cutouts/{job["id"]}.png'] = {**meta, 'kind': 'cutout', 'size': size, 'alpha': True}
        for ratio, dims in RATIOS.items():
            out[f'crops/{job["id"]}-{ratio}.png'] = {**meta, 'kind': 'crop', 'size': dims, 'ratio': ratio}
            for scene in SCENES:
                out[f'mockups/{job["id"]}/{scene}-{ratio}.png'] = {**meta, 'kind': 'mockup', 'size': dims, 'scene': scene, 'ratio': ratio}
    for dog in sorted({j['dog'] for j in chosen}):
        mine = [j for j in jobs if j['dog'] == dog]
        if stage >= 2 and all(j['stage'] <= stage for j in mine) and {j['format'] for j in mine} >= GIFTS:
            for ratio, dims in RATIOS.items():
                out[f'mockups/{dog}-set/home-{ratio}.png'] = {'kind': 'set', 'job': dog, 'breed': mine[0]['breed'],
                                                              'size': dims, 'scene': 'home', 'ratio': ratio}
    return out


def image_problems(path, spec):
    from PIL import Image
    try:
        with Image.open(path) as image:
            image.load()
            size, mode = image.size, image.mode
            alpha = image.getchannel('A') if 'A' in image.getbands() else None
            small = image.convert('RGB')
            small.thumbnail((256, 256))
            colors = len(small.getcolors(256 * 256) or ())
            fmt = image.format
    except (OSError, ValueError) as e:
        return [f'not a readable image ({e.__class__.__name__})']
    problems = []
    if spec['kind'] == 'photo':
        if fmt != 'JPEG':
            problems.append('the photo must be a JPEG')
        if min(size) < 800:
            problems.append(f'the photo is {size[0]}x{size[1]}; at least 800 px on the short side')
        return problems
    if fmt != 'PNG':
        problems.append('must be a PNG')
    if size != spec['size']:
        problems.append(f'is {size[0]}x{size[1]}, must be {spec["size"][0]}x{spec["size"][1]}')
    if spec.get('alpha'):
        if alpha is None:
            problems.append('a cutout needs a transparent background (no alpha channel)')
        else:
            clear = sum(alpha.histogram()[:8]) / (size[0] * size[1])
            if not 0.05 <= clear <= 0.95:
                problems.append(f'a cutout should be part transparent; {clear:.0%} of it is clear')
    elif colors < 1000:
        problems.append(f'looks blank or flat ({colors} colors): a template, a tile or a failed render')
    return problems


def check(root, stage, only=None):
    """(errors, status) for the stage, or one job of it: errors that must be fixed, and done or failed per file."""
    if stage not in LIMITS:
        return [f'stage must be one of {sorted(LIMITS)}'], {}
    base = Path(root) / ROOT
    jobs = batch(root)
    if only is not None and not any(j['id'] == only and j['stage'] <= stage for j in jobs):
        return [f'{only} is not a stage {stage} job'], {}
    want = expected(jobs, stage, only)
    errors, status = [], {}
    failures = {}
    if (base / 'failures.json').exists():
        failures = json.loads((base / 'failures.json').read_text())
        if not isinstance(failures, dict) or not all(isinstance(v, str) and v.strip() for v in failures.values()):
            errors.append('failures.json must map each failed file to its reason')
            failures = {}
    present = {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()} - RECORDS
    contact = {r for r in present if r.startswith('contact/') and r.endswith('.jpg')}
    present -= contact
    for job in {want[r]['job'] for r in want if want[r]['kind'] == 'painting'}:
        if f'contact/{job}.jpg' not in contact and f'paintings/{job}.png' in present:
            errors.append(f'contact/{job}.jpg: missing (one review sheet per job)')
    for extra in sorted(present - set(want)):
        errors.append(f'{extra}: not in stage {stage} of the brief (a retry, a later stage or a stray file)')
    for rel, spec in want.items():
        if rel not in present:
            if rel in failures:
                status[rel] = 'failed: ' + failures[rel]
            else:
                errors.append(f'{rel}: missing, and not reported in failures.json')
                status[rel] = 'missing'
            continue
        problems = image_problems(base / rel, spec)
        errors += [f'{rel}: {p}' for p in problems]
        status[rel] = 'done' if not problems else 'wrong'
    kinds = [want[r]['kind'] for r in present & set(want)]
    limits = LIMITS[stage] if stage == 1 else {k: LIMITS[1][k] + LIMITS[2][k] for k in LIMITS[1]}
    counts = {'painting': kinds.count('painting'), 'cutout': kinds.count('cutout'),
              'scene': len({r.rsplit('-', 1)[0] for r in present & set(want) if want[r]['kind'] == 'mockup'}),
              'set': len({r.split('/')[1] for r in present & set(want) if want[r]['kind'] == 'set'})}
    for name, count in counts.items():
        if count > limits[name]:
            errors.append(f'{count} {name}s is over the stage limit of {limits[name]}')
    dogs = sorted({want[r]['dog'] for r in want if want[r]['kind'] == 'photo'})
    try:
        credits = json.loads((base / 'credits.json').read_text())
    except (OSError, ValueError):
        credits = None
        errors.append('credits.json is missing or not JSON')
    if isinstance(credits, dict):
        for dog in dogs:
            c = credits.get(dog) or {}
            if not all(isinstance(c.get(k), str) and c[k].strip() for k in ('photographer', 'source_url', 'licence')):
                errors.append(f'credits.json: {dog} needs photographer, source_url and licence')
            elif not any(h in c['source_url'] for h in PHOTO_HOSTS) or not c['source_url'].startswith('https://'):
                errors.append(f'credits.json: {dog} must come from Unsplash or Pexels')
    elif credits is not None:
        errors.append('credits.json must map each dog to its photo credit')
    try:
        manifest = json.loads((base / 'manifest.json').read_text())
    except (OSError, ValueError):
        manifest = None
        errors.append('manifest.json is missing or not JSON')
    if manifest is not None:
        errors += manifest_problems(manifest, want, present)
    return errors, status


def manifest_problems(manifest, want, present):
    if not isinstance(manifest, list):
        return ['manifest.json must be a list of entries']
    errors, seen = [], set()
    made = {r for r in present & set(want) if want[r]['kind'] != 'photo'}
    for entry in manifest:
        if not isinstance(entry, dict) or not isinstance(entry.get('file'), str):
            errors.append('manifest.json: every entry needs a file'); continue
        rel = entry['file'].removeprefix(ROOT + '/')
        spec = want.get(rel)
        if rel in seen:
            errors.append(f'manifest.json: {rel} is listed twice')
        seen.add(rel)
        if not spec or spec['kind'] == 'photo':
            errors.append(f'manifest.json: {rel} is not a stage file'); continue
        for key in ('job', 'breed', 'style', 'tone', 'gift', 'scene', 'ratio'):
            if key in spec and entry.get(key) != spec[key]:
                errors.append(f'manifest.json: {rel} has {key} {entry.get(key)!r}, expected {spec[key]!r}')
        if entry.get('kind') != spec['kind']:
            errors.append(f'manifest.json: {rel} has kind {entry.get("kind")!r}, expected {spec["kind"]!r}')
        uses = entry.get('uses')
        if not isinstance(uses, list) or not uses or set(uses) - USES:
            errors.append(f'manifest.json: {rel} needs uses from {sorted(USES)}')
    for rel in sorted(made - seen):
        errors.append(f'manifest.json: {rel} is missing')
    return errors
