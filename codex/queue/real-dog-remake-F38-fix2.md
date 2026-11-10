---
card: real-dog-remake-F38-fix2
title: F38 - new aligned stare and a moving yawn; labels easier to read
spend_id: none (Codex weekly allowance)
max_minutes: 15
max_calls: 25
write_allow: [out/F38.mp4, out/F38_cover.jpg, out/notes.md, build.py]
---
## Goal

The judge scored the fix1 cut 8. Make these changes in `build.py` and rebuild. Everything else stays as it is.

1. **Shot 8 (5:32 AM · aligned, 11.9 to 13.7 s):** source `clips/c8new.mp4` from in 1.0, cropped in source pixels
   (720x1280) to x 180 to 540, y 140 to 780 (360x640), then scaled to 1080x1920. The label stays at its current anchor
   (y 1450.5).
2. **Shot 11 (2:00 PM · rise and grind, 17.2 to 20.2 s):** replace the still with `clips/c11yawn.mp4` from in 0.0
   (exactly 3.0 s; never use footage after 3.0 s, because the face changes after that). No push-in. The label stays
   where it is.
3. **Labels, all shots:** keep the font, size and colour. Add a soft drop shadow (black, 45% opacity, blur radius 6 px,
   offset 0, 3 px) under the existing outline, so labels read on light backgrounds.
4. **Shot 2 label (4:05 AM · cold plunge):** move it up to anchor y 1250 so it clears the splash.
5. **Shot 7 label (5:31 AM · stakeholder alignment):** move it down to anchor y 1500 so it clears the window frame.

## Floor

As card real-dog-remake-F38: `real-scruffy-dogs`, `real-dogs` (crop and scale only), `text-clear-of-faces`,
`no-badges`, no audio. `every-beat-moves`: there are no stills left.

## Acceptance

python3 -c "import subprocess;d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/F38.mp4']));print('ok' if abs(d-21.7)<0.15 else d)"

## Return

The rebuilt `out/F38.mp4` and `out/notes.md` updated.
