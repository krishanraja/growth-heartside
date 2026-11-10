---
card: real-dog-remake-F38-fix3
title: F38 - pre-dawn grade on the early beats, labels off faces, longer aligned stare
spend_id: none (Codex weekly allowance)
max_minutes: 15
max_calls: 25
write_allow: [out/F38.mp4, out/F38_cover.jpg, out/notes.md, build.py]
---
## Goal

The judge scored the fix2 cut 8. Make these changes in `build.py` and rebuild. Nothing else changes.

1. **Pre-dawn grade, shots 1 to 8 (0.0 to 13.7 s) and shot 12 (day 2):** make them read as before sunrise. Lower the
   exposure about 1.2 stops, cool the white balance toward blue (about -12 on a warm-cool scale), and lift the
   shadows slightly so the dog stays readable. Apply the same grade to every pixel of a shot; never retouch the dog.
   Shots 9 to 11 (7 AM onward) stay as they are.
2. **Labels off faces:**
   - shot 8 "5:32 AM · aligned" and shot 11 "2:00 PM · rise and grind" move to the top band (anchor y 250);
   - shot 2 "4:05 AM · cold plunge" moves to anchor y 250, above the dog's head.
3. **Longer stare:** shot 8 runs 11.9 to 14.2 s (0.5 s longer). Shot 9 (networking) moves to 14.2 to 15.1 s, still
   from in 0.0, and shot 10 (deep work) to 15.1 to 17.2 s, from in 0.6. The total stays 21.7 s.

## Floor

As card real-dog-remake-F38: no retouching of dogs (a whole-frame grade only), `text-clear-of-faces`, no audio.

## Acceptance

python3 -c "import subprocess;d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/F38.mp4']));print('ok' if abs(d-21.7)<0.15 else d)"

## Return

The rebuilt `out/F38.mp4` and `out/notes.md` updated.
