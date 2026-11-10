---
card: photo-posts-with-music
title: Turn 15 approved photo posts into 8 s vertical videos with their licensed Epidemic track built in
spend_id: none (Codex weekly allowance)
max_minutes: 25
max_calls: 40
write_allow: [out/*, build.py]
---
## Goal

Krish, 10 Nov: "try having them all be posted/postable with music - even the stills". Each photo post becomes a short
video that any platform (or Codex in a browser) can post with its music already in it. Write `build.py` (Python 3,
Pillow, ffmpeg) and run it.

For each `inputs/slides/<post>.jpg` (15 files, each 1080x1350: a text band over a photo) with
`inputs/music/<post>.mp3` and its start second in `inputs/music.json` ({"<post>": start_seconds}):

1. **Canvas:** 1080x1920 at 30 fps, background `#FAF7F1` (the slide's own band color). The slide is centered
   horizontally, with its top at y = 285 so it sits inside every platform's safe area. It is scaled 1:1, never
   stretched or recolored.
2. **Motion:** a slow, smooth push-in on the whole slide from 1.00 to 1.04 over the full length, centered on the
   slide. The background stays still.
3. **Length:** 8.0 s.
4. **Audio:** the track from its start second for 8.0 s, AAC 192 kbps, stereo. Fade in over 0.3 s and out over the
   last 0.8 s. Normalize each track to about -14 LUFS integrated (ffmpeg `loudnorm`), so posts sound even.
5. **Output:** `out/<post>.mp4` (H.264 yuv420p, faststart) and `out/<post>_cover.jpg` (the first frame).

## Floor

- The slide's pixels are never edited: scale for the push-in only, no recolor, no added text, badge, logo or URL.
- `no-lyric-captions`: no words other than those already on the slide.
- Every track is a licensed Epidemic Sound recording supplied in `inputs/music/`; use no other audio.

## Acceptance

python3 -c "import glob,subprocess,sys;bad=[f for f in glob.glob('out/*.mp4') if abs(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))-8.0)>0.1];n=len(glob.glob('out/*.mp4'));print('ok' if n==15 and not bad else (n,bad));sys.exit(0 if n==15 and not bad else 1)"

## Return

The 15 mp4s and covers in `out/`, and `out/notes.md` with each post's measured loudness.
