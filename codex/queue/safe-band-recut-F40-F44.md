---
card: safe-band-recut-F40-F44
title: Re-cut F40, F42, F43 and F44 with every label inside the safe band
spend_id: none (Codex weekly allowance; the clips already exist)
max_minutes: 40
max_calls: 60
write_allow: [out/*, build.py]
---
## Goal

Krish, 10 Nov, on TikTok: "Still not really suitable for TikTok", then "EnSure all captions fit these new rules".
F40 (Monday morning), F42 (Black Friday haul), F43 (9 to 5) and F44 (Sunday reset) carry labels down to y 1450,
under TikTok's username and caption. Rebuild each with the same clips, cuts, timings and words, and every label
centered at one fixed position: the top of the text at y 300 of 1080x1920, one font and size for the whole reel.

**Inputs the queuing session must place first** (they are not in this repository): `inputs/<post>/` with the
Higgsfield clips each film was cut from (the session finds them in Higgsfield generation history; no new spend),
and `inputs/<post>_original.mp4`, the filed reel, as the reference for cut points, words and label style. The filed
reels are in Drive; a session that cannot download them rebuilds the cut list from
`docs/briefs/2026-11-10-dog-does-dog-things-scripts.md` and says so in `out/notes.md`.

**Output:** `out/<post>.mp4` and `out/<post>_cover.jpg` per film, 1080x1920, 30 fps, H.264 yuv420p, no audio, same
length as the original to the frame. `out/notes.md` lists each label, its anchor and the shots.

## Floor

- `fixed-label-position`: every label inside y 250 to 1250, one fixed anchor, never moved shot by shot; recrop a
  shot rather than move a label off a face.
- `text-clear-of-faces`, `real-product`, `no-badges`, `no-lyric-captions`.
- Pixels of any product render unaltered.

## Return

`out/` with four reels, four covers and `notes.md`, plus a contact sheet per reel with lines at y 250 and 1250.
The queuing session checks every frame, then files through the library lane and releases the TikTok hold in the
next README.
