---
card: dog-things-wave-3
title: Assemble five silent, labelled dog-does-dog-things reels (F46 to F50) from approved stills and clips
spend_id: 1cfc68d6-34db-488d-8842-df5b65f9b4f0
max_minutes: 40
max_calls: 60
write_allow: [out/*, build.py]
---
## Goal

Build five vertical reels for Heartside's TikTok, Instagram and Facebook, one per timeline file in `inputs/`
(`F46.json` to `F50.json`). The working directory is the card's work folder (the cloud session's scratchpad, not
the repository, because the media stays out of the public repo). The scripts and approval are in
`docs/briefs/2026-11-10-dog-things-wave-3.md` (Krish's Yes on the board, 10 Nov). Each reel parodies a human video format
played completely straight. The label against what the dog actually does is the joke.

Write one script, `build.py` (Python 3 with Pillow and ffmpeg), and run it. For each timeline:

1. **Canvas.** 1080x1920, 30 fps, H.264 yuv420p, no audio track (the song is added in each app at posting).
2. **Shots, in order, each exactly its `seconds`:**
   - `still`: the image scaled to cover 1080x1920 (center crop), with a slow push-in from 1.00 to 1.06 scale across
     the shot.
   - `clip`: the mp4 from its `in` second for `seconds`, scaled to cover 1080x1920 (center crop). No speed change.
   - `product`: the store render on a flat background of `#F4EFE6`, scaled to fit inside 900x1500 and centered,
     with no push-in, no text, no badge and no border. The pixels are never altered beyond scaling.
   - Hard cuts only: no transitions, fades or zooms between shots.
3. **Labels** (every shot whose `label` is not null), drawn on the frame:
   - one line in Karla (`inputs/Karla.ttf`) at weight 700, 52 px;
   - ink `#1F1A17` on a white rounded pill (radius 22, padding 22 px horizontal and 12 vertical, 92% opacity);
   - left edge at x = 108, top at y = 300. If that box would cover the dog's eyes or face in that shot, move it to
     y = 1300 instead, and say in `out/notes.md` which shots moved and why.
   - Never shrink the type to fit; no label is wider than 760 px at 52 px.
4. **Title** on shot 1 only: the timeline's `title` in Fraunces (`inputs/Fraunces.ttf`) at 64 px, cream `#F4EFE6`
   on an ink `#1F1A17` pill, top at y = 190, left at x = 108, above the shot's label. On a product shot, the
   timeline's `end_label` (if any) shows the same way at the top instead of a title.
5. **Output** `out/<id>.mp4`, plus `out/<id>_cover.jpg`: the frame at the middle of the funniest beat, which is the
   shot whose label is listed in `out/notes.md` as the cover. Choose it by looking: the beat where the label and
   the behavior clash hardest.

## Floor

- `real-dogs`: the stills and clips are already checked; do not generate or alter any dog.
- `real-product`: F47 and F50 end on the store's own render (`doodle-sentimental-portrait.jpg`,
  `heartside-christmas-card.jpg`), unaltered and held for the full 3.5 s. No other product appears.
- `text-clear-of-faces`: no label or title covers a dog's eyes or face, or the main action, in any frame.
- `no-lyric-captions` and `no-novelty-sfx`: no song words on screen, and no audio track at all.
- `no-badges`: no badge, watermark, logo or URL anywhere.
- `chat-builds-like-whatsapp` does not apply (these are not chats).

## Drive

Nothing goes to Drive from this card. The session that queued it checks the outputs, files the ones Krish approves
through `factory/send_library.py`, and puts them on his review board.

## Acceptance

python3 -c "import json,subprocess,sys;bad=[];[bad.append(i) for i in ['F46','F47','F48','F49','F50'] if abs(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/'+i+'.mp4']))-json.load(open('inputs/'+i+'.json'))['total_seconds'])>0.2];print('ok' if not bad else bad);sys.exit(1 if bad else 0)"

## Return

The five mp4s and covers in `out/`, `out/notes.md` (the cover beat per reel, any label that moved and why), and
anything that could not be done.
