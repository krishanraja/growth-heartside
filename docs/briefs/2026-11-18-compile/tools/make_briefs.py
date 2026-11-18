"""Write the studio briefs and cut.py commands for the compile round from films.json (run from the repository root)."""
import json, os, subprocess
from pathlib import Path
REPO = Path.cwd()
STUDIO = REPO / 'docs' / 'briefs' / '2026-11-18-compile'
FOOT = REPO / 'local' / 'footage'
films = json.load(open(REPO / 'docs/briefs/2026-11-18-compile/films.json', encoding='utf-8'))['films']
manifest = {c['id']: c for c in json.load(open(REPO / 'docs/briefs/2026-11-18-footage/manifest.json', encoding='utf-8'))['clips']}
held_dir = FOOT / 'ready' / 'held'; held_dir.mkdir(exist_ok=True)
ENDCARD = REPO / 'local/paint/out/st-gy-09-terrier-blanket.png'
cmds = []
for f in films:
    takes, ins, shots_md = [], [], []
    total = 0.0
    for i, (cid, tin, dur) in enumerate(f['shots'], 1):
        c = manifest[cid]
        path = FOOT / 'ready' / f"{cid}_{c['slug']}.mp4"
        if i == len(f['shots']) and f.get('hold_last'):
            held = held_dir / f"{cid}_{c['slug']}_held.mp4"
            subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-ss', str(tin), '-t', str(dur), '-i', str(path),
                                   '-vf', f"tpad=stop_mode=clone:stop_duration={f['hold_last']}", '-an',
                                   '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', str(held)])
            path, tin, dur = held, 0.0, dur + f['hold_last']
        takes.append(f"s{i}={path.relative_to(REPO).as_posix()}")
        if tin:
            ins.append(f"s{i}={tin}")
        beats = '; '.join(b for t, b in c['beats'])
        shots_md.append(f"### Shot {i}: {dur:.1f} s, 9:16, 1080p, 1 take\n- {cid} (`{c['asset'][:8]}`, {c['model']}), from {tin:.1f} s: {beats}\n")
        total += dur
    gary = any('Gary' in d for s in f['shots'] for d in manifest[s[0]]['dogs'])
    doug = any('Doug' in d for s in f['shots'] for d in manifest[s[0]]['dogs'])
    dogs = []
    if gary: dogs.append('- Dog A: gray and white scruffy terrier mix, adult, Gary')
    if doug: dogs.append('- Dog B: chocolate shaggy poodle and spaniel mix, adult, Doug')
    if not dogs: dogs.append('- Dog A: tan-faced scruffy terrier mix, adult, bedroom')
    labels = '\n'.join(f'- {a:.1f} to {b:.1f} s: "{t}"' for a, b, t in f['labels'])
    brief = f"""# {f['id']}: {f['title']}

- Register: photoreal (one register, never blurred)
- Lane: humour (reach)
- Slot: compile round 18 Nov (footage not gated on the judge's 9; Ruling, Krish, 2026-11-18)
- Length: {total:.1f} s, payoff by {total:.1f} s
- Platform intent: Instagram Reels and TikTok first, Facebook paired

{chr(10).join(dogs)}

## Premise
{f['premise']}

## HUMOUR test
- Intelligent observation: {f['observation']}.
- Utterly stupid premise: {f['stupid']}.
- Slightly cruel payoff: {f['cruel']}.

## On-screen labels
Top band, centered, text top at y 360 of 1080x1920, one font and size, the same spot for the whole reel.

{labels}

## Shots

{chr(10).join(shots_md)}
## Caption

```text
{f['caption']}
```
"""
    (STUDIO / 'briefs' / f"{f['id']}.md").write_text(brief, encoding='utf-8', newline='\n')
    cmd = ['python', 'docs/briefs/2026-11-18-compile/assembly/cut.py', 'build', f['id'], '--takes', ','.join(takes)]
    if ins: cmd += ['--in', ','.join(ins)]
    cmd += ['--end', ENDCARD.relative_to(REPO).as_posix(), '--ground', 'plain'] if f['end'] else ['--no-end']
    cmds.append(cmd)
json.dump(cmds, open(STUDIO / 'cut_cmds.json', 'w'), indent=1)
print('\n'.join(' '.join(c) for c in cmds))
