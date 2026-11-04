# The uniform creative library: one folder, one naming rule, one manifest

Krish asked on 4 Nov 2026 to "get everything into one uniform folder with uniform naming conventions and assets and manifest, so codex can begin planning the paid boost tests".

## One folder

The folder is the one that already exists: Drive `Heartside/05_Social-Library/Posts/<post id>/` (`docs/DRIVE-MAP.md`).
- Every release file of a post, organic or paid, lives in its post's folder.
- No second library and no new Drive folder: that keeps the Drive map's "no sprawl" rule, and Codex has exactly one place to look.

Who may write there is unchanged. Only Krish's home computer writes `Posts/`, through `python3 factory/send_library.py <library folder>` with a `manifest.json` beside the files. No session or connector uploads there by hand.

Sources stay out of the library, as the Drive map already says:
- Runway clips;
- Higgsfield frames;
- review renders and contact sheets;
- Codex's private board exports.

A source enters the library only as part of a finished, approved master.

## One naming rule

`heartside_<post id>_<slug>_<kind>.<ext>`, matched by `factory/audit.py` and the lane.

| kind | What it is | Use |
|---|---|---|
| `reel` | The organic master, 1080x1920 mp4. When Krish locks a motion version it replaces this file under the same name (Drive map rule 4: never "v2") | organic |
| `cover` | The organic cover, 1080x1920 jpg | organic |
| `slide1` to `slide5` | Carousel slides, jpg | organic |
| `paid-reel` | A paid cut: 15 to 30 s, subtitles in the paid safe zone, a CTA end card, the locked music track (`docs/PAID-BOOSTS.md`) | paid |
| `paid-reel-a`, `paid-reel-b`, … | Arms of one paid test that differ only in the stated variable (for example the F12 opening pair) | paid |
| `paid-cover` | The paid cut's cover, if the ad needs one | paid |

- The post id and slug never change.
- A breed variant is its own post id (`F06-lab`).
- A new concept takes the next free number.

## One manifest

`library/manifest.json` in this repository records every library asset and every candidate on its way in. It holds no customer data and no media. Codex updates it when it audits, cuts or posts. The engine reads it to plan.

Each entry has these fields:

| Field | Meaning |
|---|---|
| `asset`, `post`, `kind`, `use`, `file` | Identity, from the naming rule |
| `drive_id`, `library_path` | Where it lives once it is in `Posts/` (empty while it is a candidate) |
| `bytes`, `sha256` | The exact file. A post or boost may use only the file with this hash |
| `status` | `locked`, `candidate`, `paid-candidate`, `paid-approved`, `live`, `retired` or `held: <reason>` |
| `lock_fingerprint` | The `factory/locks/<id>.json` fingerprint it was built from |
| `source` | `factory`, `codex-motion` or another builder |
| `audit` | How it was checked, the `factory/audit.py` verdict, organic and paid scores out of 10 against the bar in `docs/audits/2026-11-04-creative-audit.md`, the finding, and the date |
| `product` | The product and dog shown in the ending: it must match the dog in the story |
| `paid_gates` | For paid assets only, each gate of `docs/PAID-BOOSTS.md` as `true`, `false` or `null` (not yet checked) |

**A paid asset is boostable only when every `paid_gates` value is `true`.** One of those gates is Krish's named spend approval, written as his words and the date.

## How the manifest stays true

- Codex runs `python3 factory/audit.py <folder> --json <out>` on every master before the asset moves to a new status, then copies `bytes`, `sha256` and the verdict into the manifest.
- A hash in the manifest that differs from the file means the file wins and the entry is stale. Fix the entry before using the file.
- The 4 Nov manifest has hashes only for the files this session could download (6 reels and 12 covers). The other entries say "not yet". Carousel slides and the F13 photo are still to be added from Codex's audit run.
