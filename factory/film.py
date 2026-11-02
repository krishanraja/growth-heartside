"""Film template: key frames cut to a voice read and a music bed, captions burned in, ending on the
real product render labelled Example.

    HEARTSIDE_ASSETS=... python3 factory/film.py factory/specs/F07.json [more specs]

A spec is JSON:
  id, voice (audio/ file), music (audio/ file), music_level (under the voice, default 0.2),
  shots: [{until: seconds, frame: frames/ file | render: renders/ file, cap: caption, crop_top: 0-1}],
  sfx:   [{at: seconds, file: audio/ file | synth: "gavel" | "creak", vol}],
  end:   {renders: [renders/ files], super: headline, sub: line, hold: seconds}
Times are seconds from the start of the voice read. The music dips under the end chime and fades
(sound bible, round 5): no hard stops.
"""
import json, os, sys, textwrap
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from common import *

CAPB = bold(F('Karla.ttf', 54), 800)


def cover(path, crop_top=0.0):
    im = Image.open(path).convert('RGB')
    if crop_top:
        im = im.crop((0, int(im.height * crop_top), im.width, im.height))
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def caption(im, text, y=1440):
    if not text:
        return im
    d = ImageDraw.Draw(im, 'RGBA')
    lines = textwrap.wrap(text, 28); lh = 70; h = lh * len(lines) + 44
    d.rounded_rectangle((60, y, W - 60, y + h), 24, fill=(20, 18, 15, 185))
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=CAPB); d.text(((W - tw) / 2, y + 22 + i * lh), l, font=CAPB, fill=(255, 255, 255))
    return im


def render_shot(name, cap):
    """A real store render mid-film: untouched, labelled Example, on cream."""
    im = Image.new('RGB', (W, H), CREAM)
    p = Image.open(f'{R}/{name}').convert('RGB'); p.thumbnail((900, 1150), Image.LANCZOS)
    x, y = (W - p.width) // 2, 180
    im.paste(p, (x, y)); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((x + 24, y + 24, x + 212, y + 80), 10, fill=(20, 18, 15, 190)); d.text((x + 42, y + 32), 'EXAMPLE', font=SMALL, fill=(255, 255, 255))
    return caption(im, cap, y=1440)


def synth(kind, out):
    if kind == 'gavel':
        run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=95:duration=0.25', '-f', 'lavfi', '-i', 'anoisesrc=d=0.05:c=brown:a=0.8',
             '-filter_complex', '[0]afade=t=out:st=0.02:d=0.22[a];[1]lowpass=f=1200[b];[a][b]amix=inputs=2,volume=1.6', '-ar', '44100', '-ac', '2', out])
    elif kind == 'creak':
        run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=frequency=210:duration=0.5', '-af', 'vibrato=f=18:d=0.9,tremolo=f=30:d=0.6,afade=t=in:d=0.05,afade=t=out:st=0.3:d=0.2,volume=0.7', '-ar', '44100', '-ac', '2', out])
    return out


def build(spec):
    sid = spec['id']; work = f'{OUTDIR}/{sid}'; os.makedirs(work, exist_ok=True)
    parts, t0 = [], 0.0
    for i, s in enumerate(spec['shots']):
        dur = s['until'] - t0; t0 = s['until']
        if 'render' in s:
            im = render_shot(s['render'], s.get('cap')); zoom = '1'
        else:
            im = caption(cover(f"{FR}/{s['frame']}", s.get('crop_top', 0)), s.get('cap')); zoom = 'min(zoom+0.0007,1.08)'
        png = f'{work}/s{i:02d}.png'; im.save(png); n = round(dur * 30); out = f'{work}/s{i:02d}.mp4'
        run(['ffmpeg', '-y', '-loop', '1', '-i', png, '-vf',
             f"scale=2160:3840,zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps=30,format=yuv420p",
             '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out])
        parts.append(out)
    end = spec['end']; end_t = t0; hold = end.get('hold', 4.2); total = end_t + hold
    product_card(end['renders'], end['super'], sub=end.get('sub')).save(f'{work}/end.png')
    n = round(hold * 30)
    run(['ffmpeg', '-y', '-loop', '1', '-i', f'{work}/end.png', '-vf', 'format=yuv420p', '-frames:v', str(n), '-r', '30', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', f'{work}/end.mp4'])
    parts.append(f'{work}/end.mp4')
    with open(f'{work}/list.txt', 'w') as fh:
        fh.write(''.join(f"file '{p}'\n" for p in parts))
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt', '-c', 'copy', f'{work}/picture.mp4'])

    lvl = spec.get('music_level', 0.2)
    inputs = ['-i', f"{AU}/{spec['voice']}", '-i', f"{AU}/{spec['music']}", '-i', f'{AU}/s_shimmer.mp3']
    filt = [f"[0:a]aresample=44100,aformat=channel_layouts=stereo,volume={spec.get('voice_level', 1.0)}[v]",
            f"[1:a]atrim=0:{total + 0.5},asetpts=PTS-STARTPTS,volume='if(lt(t,{end_t}),{lvl},{lvl}+0.08)':eval=frame,afade=t=in:d=0.5,afade=t=out:st={total - 2.6}:d=2.6[m]",
            f"[2:a]atrim=0:4,asetpts=PTS-STARTPTS,volume=0.8,afade=t=in:d=0.4,afade=t=out:st=2.6:d=1.4,adelay={int(end_t * 1000 + 150)}|{int(end_t * 1000 + 150)}[c]"]
    labels = ['[v]', '[m]', '[c]']
    for k, e in enumerate(spec.get('sfx', [])):
        src = f"{AU}/{e['file']}" if 'file' in e else synth(e['synth'], f'{work}/sfx{k}.wav')
        inputs += ['-i', src]; ms = int(e['at'] * 1000)
        filt.append(f"[{3 + k}:a]aresample=44100,aformat=channel_layouts=stereo,volume={e.get('vol', 0.6)},adelay={ms}|{ms}[e{k}]"); labels.append(f'[e{k}]')
    filt.append(''.join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9,loudnorm=I=-16:TP=-1.5[o]")
    run(['ffmpeg', '-y'] + inputs + ['-filter_complex', ';'.join(filt), '-map', '[o]', '-t', f'{total:.2f}', '-ar', '44100', f'{work}/sound.m4a'])
    final = f'{OUTDIR}/{sid}.mp4'
    run(['ffmpeg', '-y', '-i', f'{work}/picture.mp4', '-i', f'{work}/sound.m4a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', final])
    return final, total


if __name__ == '__main__':
    for p in sys.argv[1:]:
        f, t = build(json.load(open(p)))
        print(f, round(t, 2))
