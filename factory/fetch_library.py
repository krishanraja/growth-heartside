"""Rebuild the factory asset library (HEARTSIDE_ASSETS) from its public sources, checked by sha256.

    python3 factory/fetch_library.py DEST [--shimmer-url SIGNED_EPIDEMIC_URL]

Sources are in factory/bank/library-sources.json. Store renders must match factory/bank/renders.json byte for byte,
and the chat photos and the end chime must match their recorded sha256; a mismatch is reported and the file is not
kept. The end chime is licensed Epidemic Sound audio: download it with the Epidemic connector and pass the signed url.
"""
import argparse, hashlib, io, json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = json.load(open(f'{HERE}/bank/library-sources.json', encoding='utf-8'))
RENDERS = {r['file']: r['sha256'] for r in json.load(open(f'{HERE}/bank/renders.json'))['renders']}


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('dest'); ap.add_argument('--shimmer-url')
    a = ap.parse_args(); d = os.path.abspath(a.dest); problems = []
    for sub in ('renders', 'fonts', 'frames', 'audio'):
        os.makedirs(f'{d}/{sub}', exist_ok=True)
    urls = []
    for handle in SRC['store_products']:
        urls += [i['src'] for i in json.loads(get(f'https://heartside.io/products/{handle}.json'))['product']['images']]
    for u in urls:
        name = re.sub(r'\?.*', '', u.rsplit('/', 1)[1])
        if name in RENDERS:
            b = get(u)
            if sha(b) == RENDERS[name]:
                open(f'{d}/renders/{name}', 'wb').write(b)
            else:
                problems.append(f'render {name}: the store file no longer matches renders.json (sync, do not substitute)')
    problems += [f'render {n}: not found on the store' for n in RENDERS if not os.path.exists(f'{d}/renders/{n}')]
    for name, u in SRC['fonts'].items():
        open(f'{d}/fonts/{name}', 'wb').write(get(u))
    from PIL import Image
    for name, f in SRC['frames'].items():
        buf = io.BytesIO(); Image.open(io.BytesIO(get(f['url']))).convert('RGB').save(buf, 'JPEG', quality=92)
        if sha(buf.getvalue()) != f['sha256']:
            problems.append(f'frame {name}: re-encoded bytes differ from the recorded sha256 (check it by eye before use)')
        open(f'{d}/frames/{name}', 'wb').write(buf.getvalue())
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-t', '60',
                    f'{d}/audio/m_silent.mp3'], check=True)
    sh = SRC['audio']['s_shimmer.mp3']
    if a.shimmer_url:
        b = get(a.shimmer_url)
        if sha(b) == sh['sha256']:
            open(f'{d}/audio/s_shimmer.mp3', 'wb').write(b)
        else:
            problems.append('s_shimmer.mp3: the download does not match the recorded sha256')
    else:
        problems.append(f"s_shimmer.mp3 missing: download Epidemic sound effect {sh['epidemic_sound_effect']} as MP3 and pass --shimmer-url")
    print(f'library at {d}: {len(os.listdir(d + "/renders"))} renders, {len(os.listdir(d + "/frames"))} frames, '
          f'{len(os.listdir(d + "/fonts"))} fonts, {len(os.listdir(d + "/audio"))} audio')
    for p in problems:
        print('HOLD:', p)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
