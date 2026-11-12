# Every post against the 12 Nov corpus

Krish, 12 Nov 2026: "Ensure all social media posts adhere to these best practices." The corpus is
[knowledge/social-media-creative-production-corpus-2026-11-12.md](../../knowledge/social-media-creative-production-corpus-2026-11-12.md)
(SHA-256 `483cf6c3...5c93`). This engine now runs it as profile `social-corpus-2026-11-12-v2`
([docs/CREATIVE-UI.md](../CREATIVE-UI.md)). This audit records where every existing post stands against it,
what was measured and what was only read from records.

## What now holds a post

Every renderer records what it draws (a layout manifest bound to the file's SHA-256), and the gates check it:

| Rule (corpus section) | Where it holds |
|---|---|
| Hook, subtitles, labels, chat, faces, product and mark inside x 120 to 820, y 330 to 1180 (3.5) | `layout_errors`, called by `lock.py media`, `lock.py gate`, the release check and `codex/check_picture.py` |
| Subtitles 1 or 2 lines, at most 7 words a timed segment, 44 to 64 px (6.1) | the film renderer splits each voice line; `layout_errors` holds a breach |
| Opening hook at most 12 words (target 3 to 7); frame 1 is never a logo or an empty slate (4.1) | `layout_errors`; search posts open mid-typing |
| Product end beat 3 to 4 s and moving, never a dead outro (5), keeping Krish's 3 s floor `endings-land` | renderers clamp the hold; `layout_errors` and `check_picture.py` hold it |
| Labels in one fixed place (Krish's floor `fixed-label-position`) | `layout_errors`, `check_picture.py` (`label_box`) |
| Feed slides keep a 70 px design margin (8) | `layout_errors` on every still slide |
| H.264 yuv420p BT.709, constant frame rate, at most 12 Mbps, AAC 48 kHz stereo, true peak at or under -1 dBTP (10) | `export_errors` in `lock.py media`, `factory/audit.py`, `check_picture.py` |
| Cover keeps face and headline inside the central 3:4 crop (7) | inside the critical box by construction; the reviewer brief checks the actual grid |
| Native preview with UI, captions and description before release (11) | unchanged: the placement review in `docs/CREATIVE-UI.md` |

Organic posts still carry no on-screen CTA (Krish, 2 Nov): the corpus's "one next action" goes in the post
description.

The other lanes follow it too: `factory/lipsync_cut.py` refuses a premise or label outside the box or overlapping
another, defaults labels to text top y 360 and fits the end render inside the box for 3 to 4 s; `factory/splice.py`
writes AAC 48 kHz stereo. `factory/repair_ui.py` keeps its original audio bitstream by design (its verification
depends on it), so its editions go through `factory/audit.py` like any other file.

## Results

Measured here on 12 Nov, from the public asset library rebuilt with `factory/fetch_library.py` (the licensed
end chime and music stubbed with silence, so these are proof renders, never release files).

| Post | Verdict | Evidence |
|---|---|---|
| F34, F34-doodle, F34-golden, F34-dachshund (chat) | **Pass** | Built under the corpus profile; `lock.py media` ok on all four (layout, export, end beat). Content lock still matches. Contact sheet checked by eye: chat, header and product inside the box, clear of the right rail, top tabs and bottom caption. |
| Seven campaigns in `campaigns/` (21 reels) | **Pass** | Rendered with fixture fonts; every reel's layout and export pass. Headlines may now take three lines; the mark sits inside the logo region at full push-in. |
| F11 (search) | **Fails: content** | All seven searches are too long for one readable line inside the box: 645 to 1224 px needed, 560 available at the 40 px floor. The renderer refuses it. Needs shorter lines from Krish or retiring the format. |
| F10 (chat) | **Fails: Krish's floors** | Layout and export pass, but now that it runs the current profile it breaks `no-novelty-sfx` (a scratch effect on a message) and opens on three bubbles over an empty screen (`chat-builds-like-whatsapp`). Fixing the sound is a content change, so it needs Krish's yes. |
| F01 (film) | **Fails: drift (pre-existing)** | Its spec no longer matches its lock on the original code too (`9abd142...` against `cdb2099...`, spec edited 4 Nov). A finding for Krish, as before. |
| F02, F03, F04, F05, F07, F12 (films), F06 roasts | **Not rendered here** | Their frames and voice reads are not in the public library. Locks still match. Under the corpus profile each voice line becomes 7 to 13 timed segments a film (the longest lines run 14 to 16 words), F04's captions at y 200 and y 1300 move to y 330 and y 1020, and every end beat is 4.0 s. Build them where the frames live, then `lock.py gate`. |

### Media already filed in Drive 03b (50 post folders, F01 to F59)

All of it was made before the corpus. Not measured here: that needs each file downloaded. From the records:

- **Factory reels F01 to F12** were muxed at 44.1 kHz and put whole voice lines on screen at once
  (subtitles at y 1300 to 1440; the 4 Nov ruling kept F01, F02, F03, F05 and F12 at y 1440, under TikTok's
  caption). They fail the subtitle region, the 7-word segment rule and the 48 kHz preset.
- **Codex reels F38 to F50** drew labels with text top at y 300, the top-band default of 10 Nov. That is 30 px
  above the corpus box. F38's middle position (text top about y 1050) is inside it.
- **F13 and F17 to F24** are 1260x773, 1920x1656 and 1920x2186 images: not one of the corpus formats
  (9:16, 4:5, 3:4, 1:1). They are live and stay live; they are not reused.
- **Sprint 120 filed slots** (21) were made through the Codex and lip-sync lanes before 12 Nov.

To measure them, on the computer that holds the library:

```sh
python3 factory/audit.py <03b Posts folder> --json local/audits/2026-11-12-03b.json
```

and for each Codex reel with its timeline, `python3 codex/check_picture.py <reel> <timeline>`.

## What stays as it is

- Posts already live stay live. Nothing here edits a live or queued post, a Sheet row or a lock.
- Content locks keep their approvals: placement is not part of a lock's fingerprint any more, so a rebuilt
  edition under the corpus profile is the same approved post in a new place. Every rebuilt file is a new
  release and still needs the placement review and Krish's `approved = yes` before Codex posts it.
- Codex posts only rows Krish approved. Whether pre-corpus rows not yet live should wait for rebuilt editions
  is his call, on the review board (`decision-corpus-hold-queue`).
