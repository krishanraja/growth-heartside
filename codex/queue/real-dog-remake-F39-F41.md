---
card: real-dog-remake-F39-F41
title: Re-cut F39 "gym era" and F41 "Christmas shopping" with the new real-looking dogs
spend_id: none (Codex weekly allowance)
max_minutes: 30
max_calls: 50
write_allow: [out/*, build.py]
---
## Goal

Krish approved F39 and F41, then asked for them remade because the AI dogs looked "way too perfect and not real".
Rebuild each from the new clips in `inputs/F39/` and `inputs/F41/`. Keep the approved reels (`inputs/F39_original.mp4`,
`inputs/F41_original.mp4`) as the reference for text style and placement. Write `build.py` (Python 3, Pillow, ffmpeg)
and run it.

**Both reels:** 1080x1920, 30 fps, H.264 yuv420p, no audio track. Hard cuts only. Each clip is scaled to cover with a
centre crop, at normal speed, unless a crop is given. Every clip is 720x1280, and crops are in those source pixels.
Never use footage outside the given windows; several clips go wrong after them.

**Text:** copy the font look, size, colour, outline and position from the original at the same moment. Add a soft drop
shadow (black, 45% opacity, blur 6 px, offset 0, 3 px). Never put text over a dog's eyes, face or mouth: if a copied
position would, move it the shortest distance clear and note it in `out/notes.md`.

### F39 (17.7 s): title "My dog's gym era" on shot 1 only, no other labels

| # | Start-end | Source | In |
|---|---|---|---|
| 1 | 0.0-1.6 | F39/1_warmup.mp4 | 0.0 |
| 2 | 1.6-3.0 | F39/2_deadlift.mp4 | 0.0 |
| 3 | 3.0-5.7 | F39/3_bench.mp4 | 0.0 |
| 4 | 5.7-7.5 | F39/4_mirror.mp4 | 0.5 |
| 5 | 7.5-8.3 | F39/5_6_sprint_ball.mp4 | 0.0 |
| 6 | 8.3-9.1 | F39/5_6_sprint_ball.mp4 | 0.9 |
| 7 | 9.1-10.7 | F39/7_reps.mp4 | 0.5 |
| 8 | 10.7-11.5 | F39/8_ropes.mp4 | 0.0 |
| 9 | 11.5-12.4 | F39/9_protein.mp4 | 0.0 |
| 10 | 12.4-13.5 | F39/10_hydration.mp4 | 0.0 |
| 11 | 13.5-16.5 | F39/11_12_recovery.mp4 | 0.0 |
| 12 | 16.5-17.7 | F39/11_12_recovery.mp4, cropped to x 140-500, y 560-1200 | 3.0 |

Cover `out/F39_cover.jpg`: the frame at 2.3 s (the log drag), with the title off.

### F41 (21.6 s): a date label on every dog shot

| # | Start-end | Label (exact) | Source | In |
|---|---|---|---|---|
| 1 | 0.0-2.0 | Dec 1 · the list | F41/1_list.mp4 | 0.0 |
| 2 | 2.0-4.8 | Dec 3 · shopping | F41/2_shopping.mp4 | 0.0 |
| 3 | 4.8-6.8 | Dec 3 · found the one | F41/3_found.mp4 | 0.0 |
| 4 | 6.8-9.3 | Dec 10 · gift wrapping | F41/4_wrapping.mp4 | 0.0 |
| 5 | 9.3-12.3 | Dec 24 · quality control | F41/5_6_quality_no_notes.mp4 | 0.0 |
| 6 | 12.3-14.3 | Dec 24 · no notes | F41/5_6_quality_no_notes.mp4 | 3.0 |
| 7 | 14.3-18.0 | Dec 25 · your real gift | F41/7_real_gift.mp4 | 0.0 |
| 8 | 18.0-21.6 | (none) | mug-real-lab.jpg | - |

Shot 8 is the store's real mug render. Lay it out exactly as the original's product shot (open
`inputs/F41_original.mp4` at 19.5 s: same background colour, scale and position). Scale only: never recolour, redraw
or edit its pixels. No text, badge or border, and no push-in.

Cover `out/F41_cover.jpg`: the frame at 13.3 s (no notes), with its label.

## Floor

- `real-scruffy-dogs`, `real-dogs`: clips are used as given (crop and scale only).
- `real-product`: the mug render is unaltered (sha256 883a5570...dda9d), held 3.6 s.
- `text-clear-of-faces`, `no-badges`, `no-lyric-captions`, `no-novelty-sfx`: no audio track.
- `every-beat-moves`: every dog shot is a clip.

## Acceptance

python3 -c "import subprocess;g=lambda f:float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]));a,b=g('out/F39.mp4'),g('out/F41.mp4');print('ok' if abs(a-17.7)<0.15 and abs(b-21.6)<0.15 else (a,b))"

## Return

`out/F39.mp4`, `out/F41.mp4`, both covers, and `out/notes.md`.
