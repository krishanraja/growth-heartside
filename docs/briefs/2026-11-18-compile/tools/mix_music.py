"""Mix each film's music bed from music.json onto its silent master (run from the repository root).

    python -I docs/briefs/2026-11-18-compile/tools/mix_music.py [film ...]

Writes local/media/studio/<film>/<film>_music.mp4 beside the silent master <film>.mp4. Each bed is loudness
normalized to -16 LUFS; where the plan names stop_at, the music cuts (0.15 s fade) on the payoff and the rest
plays in silence; otherwise it fades out over the last 0.6 s. A bed with from/to plays only in that window.
Run it only after Krish has approved the music (music.json "status")."""
import json, os, subprocess, sys

REPO = os.getcwd()
plan = json.load(open(os.path.join(REPO, 'docs/briefs/2026-11-18-compile/music.json'), encoding='utf-8'))
MUS = os.path.join(REPO, plan['local_dir'])
want = set(sys.argv[1:])
films = {}
for b in plan['beds']:
    films.setdefault(b['film'], []).append(b)
for film, beds in films.items():
    if want and film not in want:
        continue
    src = os.path.join(REPO, 'local/media/studio', film, film + '.mp4')
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src]).decode())
    inputs, chains = ['-i', src], []
    for k, b in enumerate(beds, 1):
        inputs += ['-i', os.path.join(MUS, b['file'])]
        start = b.get('from', 0.0)
        end = min(b.get('stop_at', b.get('to', dur)), dur)
        length = end - start
        fade = 0.15 if ('stop_at' in b or 'to' in b) else 0.6
        chains.append(f"[{k}:a]loudnorm=I=-16:TP=-1.5:LRA=11,atrim=0:{length:.3f},afade=t=out:st={max(length - fade, 0):.3f}:d={fade},"
                      f"adelay={int(start * 1000)}:all=1,apad=whole_dur={dur:.3f}[a{k}]")
    mix = ''.join(f'[a{k}]' for k in range(1, len(beds) + 1))
    graph = ';'.join(chains) + f";{mix}amix=inputs={len(beds)}:normalize=0,atrim=0:{dur:.3f}[aout]"
    out = os.path.join(REPO, 'local/media/studio', film, film + '_music.mp4')
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', graph, '-map', '0:v', '-map', '[aout]',
                           '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', out])
    print(film, '->', os.path.relpath(out, REPO))
