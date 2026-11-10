---
card: real-dog-remake-F38-fix1
title: F38 re-cut - punch in on the aligned stare, trim networking and the 5K run
spend_id: none (Codex weekly allowance)
max_minutes: 15
max_calls: 25
write_allow: [out/F38.mp4, out/F38_cover.jpg, out/notes.md, build.py]
---
## Goal

The tier 2 judge scored `out/F38.mp4` (card real-dog-remake-F38) 8. Three changes are needed, all in the edit. Change
`build.py` and rebuild. Every other shot, label, style and timing stays as it is.

1. **Shot 3 (4:15 AM · 5K run):** source `clips/c3.mp4` from in 0.0 instead of 1.0. Later frames drift to a different
   dog.
2. **Shot 8 (5:32 AM · aligned):** a punch-in on the stare. Source `clips/c68.mp4` from in 3.1, cropped in source pixels
   (720x1280) to the box x 160 to 520, y 300 to 940 (360x640), then scaled to 1080x1920. Hold the same 11.9 to 13.7 s.
   The label stays where it is now (anchor y 1450.5), clear of the face, which now sits at about y 390 to 1020.
3. **Shot 9 (7:00 AM · networking):** now 13.7 to 14.6 s (0.9 s), source `clips/c9.mp4` from in 0.0. The two dogs
   merge later in the clip.
4. **Shot 10 (9:00 AM · deep work):** now 14.6 to 17.2 s (2.6 s), source `clips/c1011.mp4` from in 0.6, so the reel
   stays 21.7 s.

The cover stays the frame at 6.4 s.

## Floor

As card real-dog-remake-F38: `real-scruffy-dogs`, `real-dogs` (crop and scale only, no retouching),
`text-clear-of-faces`, `no-badges`, no audio.

## Acceptance

python3 -c "import subprocess;d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/F38.mp4']));print('ok' if abs(d-21.7)<0.15 else d)"

## Return

The rebuilt `out/F38.mp4`, and `out/notes.md` updated with the four changes.
