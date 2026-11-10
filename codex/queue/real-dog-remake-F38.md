---
card: real-dog-remake-F38
title: Re-cut F38 "4 AM routine" with the new real-looking golden, same beats, timing and labels
spend_id: none (Codex weekly allowance)
max_minutes: 25
max_calls: 40
write_allow: [out/*, build.py]
---
## Goal

Krish approved F38 and then held it because the dog looked AI-perfect ("way too perfect and not real"). Rebuild it with
new clips of a scruffy, real-looking golden (`inputs/clips/`). Keep everything else identical to the approved reel
`inputs/F38_original.mp4`: the 12 shots, their exact timings, the label words, and the label style and position on each
shot. Write `build.py` (Python 3, Pillow, ffmpeg) and run it.

**Output:** 1080x1920, 30 fps, H.264 yuv420p, no audio track, 21.7 s. Hard cuts only. Each clip is scaled to cover
1080x1920 with a centre crop, at normal speed.

| # | Start-end (s) | Label (exact) | Source | In (s) |
|---|---|---|---|---|
| 1 | 0.0-1.2 | 4:00 AM · rise | clips/c1.mp4 | 0.0 |
| 2 | 1.2-3.4 | 4:05 AM · cold plunge | clips/c2.mp4 | 1.5 |
| 3 | 3.4-5.4 | 4:15 AM · 5K run | clips/c3.mp4 | 1.0 |
| 4 | 5.4-7.4 | 4:45 AM · meditation | clips/c4.mp4 | 0.5 |
| 5 | 7.4-8.7 | 5:00 AM · journaling | clips/c5.mp4 | 0.5 |
| 6 | 8.7-10.3 | 5:30 AM · planning my day | clips/c68.mp4 | 0.0 |
| 7 | 10.3-11.9 | 5:31 AM · stakeholder alignment | clips/c7.mp4 | 0.5 |
| 8 | 11.9-13.7 | 5:32 AM · aligned | clips/c68.mp4 | 3.1 |
| 9 | 13.7-15.0 | 7:00 AM · networking | clips/c9.mp4 | 0.3 |
| 10 | 15.0-17.2 | 9:00 AM · deep work | clips/c1011.mp4 | 1.0 |
| 11 | 17.2-20.2 | 2:00 PM · rise and grind | still_3811.png, slow push-in 1.00 to 1.06 | - |
| 12 | 20.2-21.7 | 4:00 AM · day 2 | clips/c1.mp4 | 2.5 |

**Labels:** match the original exactly. For each shot, open `inputs/F38_original.mp4` at the same moment and copy the
label's font look, size, colour, shadow and position (some sit near the top, some lower down, chosen to stay off the
dog's face). If a copied position would cover the new dog's eyes or face, move it the shortest distance up or down to
clear the face, and record the move in `out/notes.md`.

**Cover:** `out/F38_cover.jpg`, the frame at 6.4 s (the meditation beat), with its label, as in the original cover.

## Floor

- `real-scruffy-dogs`, `real-dogs`: use the clips as given; never generate, retouch or beautify a dog.
- `text-clear-of-faces`: no label covers a dog's eyes or face.
- `no-lyric-captions`, `no-novelty-sfx`, `no-badges`: no audio track, and no badge, logo or URL.
- `every-beat-moves`: shot 11 is the one still. Note it in `out/notes.md` so Claude can replace it with a clip later.
- Clip 9 must stop by 1.6 s into its source (a hand enters the frame after 2.5 s).

## Acceptance

python3 -c "import subprocess;d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/F38.mp4']));print('ok' if abs(d-21.7)<0.15 else d)"

## Return

`out/F38.mp4`, `out/F38_cover.jpg`, and `out/notes.md` (each label's position, any moves, shot 11 noted).
