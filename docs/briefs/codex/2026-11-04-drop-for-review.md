# Codex card: send your motion candidates where the growth engine can read them

Written on 4 Nov 2026 by the growth engine's Claude session. Krish: "drop assets in your folder of choosing".

The engine reads Heartside's Drive library through content-engine's `GET /api/library/file`, which serves only `Posts/<post id>/<file>`. So you send your candidates into their post folders under the **review kinds**, through the library lane. The review kinds are `review-reel` and `review-cover` (`docs/DRIVE-MAP.md`). Nothing else changes. Everything the engine built this session is already done; you only send what exists only on your machine.

## Hard lines

- **Never post, schedule or boost a review file.** No schedule row may name a `review-` file.
- **Never send a file under the plain `reel` or `cover` name.** That would replace the locked post Codex is scheduling from.
- Send only through `factory/send_library.py`. No connector uploads, no new folders, nothing in `Heartside/` outside `Posts/`.
- **No spend, no new generation.**

## 1. Gather these files (1080x1920 masters, not the 720 board exports)

| Post | Your file | Send it as |
|---|---|---|
| F04 | `work/mobile-review/motion/F04-motion-master1080.mp4` | `heartside_F04_me-vs-my-golden_review-reel.mp4` |
| F04 | its motion cover | `heartside_F04_me-vs-my-golden_review-cover.jpg` |
| F05 | `work/mobile-review/motion/F05-motion-master1080.mp4` | `heartside_F05_court-of-the-couch_review-reel.mp4` |
| F05 | its motion cover | `heartside_F05_court-of-the-couch_review-cover.jpg` |
| F12 | `work/mobile-review/motion/F12-motion-master1080.mp4` | `heartside_F12_head-of-security_review-reel.mp4` |
| F12 | its motion cover | `heartside_F12_head-of-security_review-cover.jpg` |
| F12 | `f12-parcel-first.mp4` (arm A, the control) | `heartside_F12_head-of-security_review-reel-a.mp4` |
| F12 | `f12-guard-first.mp4` (arm B, the opening Krish approved) | `heartside_F12_head-of-security_review-reel-b.mp4` |

- If a 1080 master does not exist for one of these, send nothing for it and say so.
- If any other finished candidate exists only on your machine, add it with the same naming and list it in the report.

## 2. Send them

1. Put the files in one folder, with a `manifest.json` listing `[{"post", "file", "bytes", "sha256"}]` for each file.
2. Run `python3 factory/send_library.py <folder> --dry-run`. It must report every file checked and nothing sent.
3. Run `python3 factory/send_library.py <folder>`.
4. Confirm each file reached `Posts/<post id>/` in Drive, with the same bytes.

## 3. Report back (paste into the growth session)

For each file, report:
- its library path;
- its SHA-256;
- the board review ID it came from;
- its source (which motion edit, which arm).

Also report anything you could not send, and why.

## What happens next (the engine, not you)

The growth engine:
1. reads each file through the library;
2. audits it with `factory/audit.py`, Content Watcher and a frame-by-frame review;
3. scores it against the bar in `docs/audits/2026-11-04-creative-audit.md`;
4. puts the motion-or-still choice to Krish.

After he locks, the engine sends the locked files under their plain names, and you re-attach media for any row not yet published (`docs/plans/2026-11-04-road-to-posting.md`, step 4).
