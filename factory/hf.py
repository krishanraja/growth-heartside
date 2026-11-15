"""Motion templates rendered by HyperFrames (HTML to video), held to the same gates as factory/build.py.

    HEARTSIDE_ASSETS=... python3 factory/hf.py SPEC [--preview]

Why this exists (evaluation of 15 Nov 2026, factory/hyperframes/README.md): HyperFrames draws type with a real
browser's layout and easing, so word-by-word text and kinetic type cost a few lines of HTML instead of hand-drawn
Pillow frames. It is used only for what it adds: the words still come from factory/bank/lines.json by id, the
product from factory/bank/renders.json byte for byte, and the finished file passes the same checks as any other
post (lock.py check before, codex/check_picture.py after) plus a pixel check that the product was not altered.

How it is contained:
- the CLI is pinned in factory/hyperframes/package-lock.json (npm ci --ignore-scripts) and run from there;
- its telemetry, update check, auto-install and skill installs are switched off, and HOME points at
  local/hyperframes/.home, so nothing is written to the user's home and its pinned browser downloads once;
- GSAP and the fonts are local files, so nothing is fetched at render time;
- frames come out as PNG and are encoded with the corpus export preset (engine/creative_ui.py), never through its
  JPEG intermediate frames.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, time
from PIL import Image, ImageChops, ImageFilter, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
import lock
import ui_layout
from engine import sound
from engine.creative_ui import FFMPEG_VIDEO, FFMPEG_AUDIO

HF = os.path.join(HERE, 'hyperframes')
BIN = os.path.join(HF, 'node_modules', '.bin', 'hyperframes')
FPS = 30
TEMPLATES = {
    # template: (directory, label box, note seconds, product seconds, product rectangle at its first frame)
    'note': ('note', [150, 380, 820, 980], 5.6, 3.5, (170, 380, 770, 1130)),
}
PUSH = 1.08   # the template's push-in on the product; the layout records the product at its largest


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def environment():
    """One contained home for every build, under local/: the pinned browser downloads once and nothing is written
    to the user's own home. The opt-out is set twice: in the environment, and persisted in that home's config."""
    env = dict(os.environ)
    home = os.path.join(ROOT, 'local', 'hyperframes', '.home'); os.makedirs(home, exist_ok=True)
    env.update(HOME=home, CI='1', HYPERFRAMES_NO_TELEMETRY='1', DO_NOT_TRACK='1', HYPERFRAMES_NO_UPDATE_CHECK='1',
               HYPERFRAMES_NO_AUTO_INSTALL='1', HYPERFRAMES_SKIP_SKILLS='1',
               HYPERFRAMES_CONFIG_DIR=os.path.join(home, '.hyperframes'), HYPERFRAMES_MEDIA_HOME=os.path.join(home, 'media'))
    config = os.path.join(home, '.hyperframes', 'config.json')
    if not os.path.exists(config) or json.load(open(config)).get('telemetryEnabled') is not False:
        subprocess.run([BIN, 'telemetry', 'disable'], check=True, env=env, capture_output=True)
    return env


def backdrop(src, out):
    """The same softened backdrop factory/common.py product_clip draws behind a scene render. Only the backdrop is
    blurred; the product above it is the untouched file."""
    W, H = 1080, 1920
    im = Image.open(src).convert('RGB'); r = max(W / im.width, H / im.height)
    back = im.resize((round(im.width * r), round(im.height * r)), Image.BICUBIC)
    x, y = (back.width - W) // 2, (back.height - H) // 2
    back = back.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(28))
    Image.blend(back, Image.new('RGB', (W, H), (20, 18, 15)), 0.25).save(out)


def psnr(a, b):
    diff = ImageChops.difference(a, b); stat = ImageStat.Stat(diff)
    mse = sum(v ** 2 for v in stat.rms) / 3
    bias = [round(x - y, 2) for x, y in zip(ImageStat.Stat(a).mean, ImageStat.Stat(b).mean)]
    return (round(10 * __import__('math').log10(255 ** 2 / mse), 2) if mse else float('inf')), bias


def fidelity(src, frame, rect):
    """Compare the product as drawn with the store file resized to the same rectangle (Pillow, Lanczos): a filter,
    colour shift or redraw shows as a low PSNR or a mean bias; resampling alone does not."""
    x0, y0, x1, y1 = rect
    ref = Image.open(src).convert('RGB').resize((x1 - x0, y1 - y0), Image.LANCZOS)
    got = Image.open(frame).convert('RGB').crop(rect)
    value, bias = psnr(got, ref)
    return {'psnr_db': value, 'mean_bias_rgb': bias}


def build(spec_path, preview=False):
    spec = json.load(open(spec_path, encoding='utf-8'))
    if spec.get('template') not in TEMPLATES:
        raise SystemExit(f"hf.py builds only {', '.join(TEMPLATES)}; {spec.get('template')} is a factory/build.py template")
    problems, warnings = lock.check(spec)
    if problems and not preview:
        raise SystemExit('HELD by lock.py check:\n' + '\n'.join(problems))
    folder, label_box, note_s, product_s, rect = TEMPLATES[spec['template']]
    render = spec['end']['renders'][0]
    src = os.path.join(lock.LIB, 'renders', render)
    if sha(src) != lock.RENDERS[render]['sha256']:
        raise SystemExit(f'{render}: not the approved store file')
    text = lock.resolve(spec['line'], spec)
    build = os.path.join(ROOT, 'local', 'hyperframes', spec['id'])
    shutil.rmtree(build, ignore_errors=True)
    os.makedirs(os.path.join(build, 'assets', 'fonts'))
    shutil.copy(os.path.join(HF, folder, 'index.html'), build)
    shutil.copy(os.path.join(HF, 'node_modules', 'gsap', 'dist', 'gsap.min.js'), os.path.join(build, 'assets'))
    shutil.copy(os.path.join(lock.LIB, 'fonts', 'Fraunces.ttf'), os.path.join(build, 'assets', 'fonts'))
    # The product reaches Chrome already scaled to its first-frame rectangle the way factory/common.py scales it
    # (Pillow, Lanczos) and lossless, so Chrome draws it 1:1 there; measured on 15 Nov, letting Chrome downscale the
    # JPEG itself cost 3.3 dB on the product after encoding against the existing pipeline.
    x0, y0, x1, y1 = rect
    Image.open(src).convert('RGB').resize((x1 - x0, y1 - y0), Image.LANCZOS).save(os.path.join(build, 'assets', 'product.png'))
    backdrop(src, os.path.join(build, 'assets', 'backdrop.png'))
    variables = {'line': text, 'product': 'assets/product.png', 'backdrop': 'assets/backdrop.png'}
    json.dump(variables, open(os.path.join(build, 'variables.json'), 'w'), ensure_ascii=False)
    frames = os.path.join(build, 'frames')
    env = environment()
    started = time.monotonic()
    subprocess.run([BIN, 'render', build, '--variables-file', os.path.join(build, 'variables.json'), '--strict-variables',
                    '--format', 'png-sequence', '--fps', str(FPS), '--output', frames, '--no-browser-gpu', '--quiet'],
                   check=True, env=env, cwd=build)
    rendered = time.monotonic() - started
    pngs = sorted(f for f in os.listdir(frames) if f.endswith('.png'))
    out_dir = os.path.abspath(os.environ.get('HEARTSIDE_OUT', os.path.join(ROOT, 'local', 'media', 'factory')))
    os.makedirs(out_dir, exist_ok=True)
    mp4 = os.path.join(out_dir, f"{spec['id']}.mp4")
    listing = os.path.join(build, 'frames.txt')
    with open(listing, 'w') as fh:
        fh.write(''.join(f"file '{os.path.join(frames, p)}'\nduration {1 / FPS:.6f}\n" for p in pngs))
    total = len(pngs) / FPS
    words = len(text.split())
    if spec.get('music'):   # the locked sound mix from the library (licensed audio never enters git)
        bed, bed_note = os.path.join(lock.LIB, 'audio', spec['music']), spec['music']
    else:                   # engine/sound.py's original local score, a note on each word, the paw and the cut
        bed, bed_note = os.path.join(build, 'score.wav'), 'placeholder: engine/sound.py local score, not a creative choice'
        rest = max(words - 3, 0)   # the template shows three words from frame one, then one every 0.16 s
        beats = [0.25 + i * 0.16 for i in range(rest)] + [0.25 + rest * 0.16 + 0.45, note_s]
        sound.score(bed, total, beats)
    started = time.monotonic()
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', listing, '-i', bed,
                    '-map', '0:v', '-map', '1:a', '-vf', f'fps={FPS},format=yuv420p', *FFMPEG_VIDEO,
                    '-af', 'loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,alimiter=limit=0.75:attack=2:release=60:level=false,apad',
                    *FFMPEG_AUDIO, '-t', f'{total:.3f}', '-movflags', '+faststart', mp4], check=True)
    encoded = time.monotonic() - started
    # The same manifest and end frame factory/build.py writes, so lock.py media and gate read a note like any post.
    x0, y0, x1, y1 = rect; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; hw, hh = (x1 - x0) * PUSH / 2, (y1 - y0) * PUSH / 2
    layout = ui_layout.Layout()
    layout.add('hook', label_box, 0.0, note_s, text)
    layout.add('product', (cx - hw, cy - hh, cx + hw, cy + hh), note_s, total, render)
    layout.ending, layout.duration, layout.media_sha256 = 'product', total, sha(mp4)
    os.makedirs(os.path.join(out_dir, spec['id']), exist_ok=True)
    layout.save(os.path.join(out_dir, spec['id'], 'layout.json'))
    shutil.copy(os.path.join(frames, pngs[-1]), os.path.join(out_dir, spec['id'], 'end.png'))
    gate = lock.media(dict(spec, _layout=os.path.join(out_dir, spec['id'], 'layout.json'),
                           _end_png=os.path.join(out_dir, spec['id'], 'end.png')), mp4)
    timeline = {'shots': [{'seconds': note_s, 'label': text, 'label_box': label_box},
                          {'seconds': product_s, 'product': render}], 'label_box': label_box}
    tl_path = os.path.join(build, 'timeline.json')
    json.dump(timeline, open(tl_path, 'w'), ensure_ascii=False, indent=1)
    picture = subprocess.run([sys.executable, os.path.join(ROOT, 'codex', 'check_picture.py'), mp4, tl_path],
                             capture_output=True, text=True)
    first = round(note_s * FPS)   # the product's first frame: scale 1, whole-pixel position
    still = os.path.join(build, 'encoded-first-product-frame.png')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', mp4, '-vf', f'select=eq(n\\,{first})', '-frames:v', '1', still], check=True)
    result = {'id': spec['id'], 'template': spec['template'], 'preview': preview, 'held_by_lock_check': problems,
              'warnings': warnings, 'line': spec['line'], 'render': render, 'mp4': mp4, 'mp4_sha256': sha(mp4),
              'frames': len(pngs), 'seconds': total, 'render_seconds': round(rendered, 1), 'encode_seconds': round(encoded, 1),
              'check_picture': picture.stdout.strip() or picture.stderr.strip(), 'check_picture_ok': picture.returncode == 0,
              'lock_media': gate or 'ok', 'sound': bed_note,
              'render_sha256': lock.RENDERS[render]['sha256'],
              'product_fidelity': {'png_frame': fidelity(src, os.path.join(frames, pngs[first]), rect),
                                   'encoded_frame': fidelity(src, still, rect)},
              'hyperframes': json.load(open(os.path.join(HF, 'package-lock.json')))['packages']['node_modules/hyperframes']['version'],
              'telemetry': 'off', 'home': env['HOME']}
    json.dump(result, open(os.path.join(build, 'result.json'), 'w'), indent=1)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--preview', action='store_true')
    a = ap.parse_args()
    print(json.dumps(build(a.spec, a.preview), indent=1, ensure_ascii=False))
