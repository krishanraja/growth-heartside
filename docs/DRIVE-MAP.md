# Heartside's Drive: what is where, and who may write it

Read from live Drive on 2026-11-09, after Krish restructured it that morning. Krish, 2026-11-09: "Folder 3A is where we're iterating on creatives, and folder 3B is where they're ready for production." Krish, 2026-11-03: "be strict on what goes where as codex tends to sprawl drives quite easily". This map is the rule. Anything not listed here does not get created. When a rule here and a habit disagree, the rule wins. If a file needs a new home, ask Krish first and add it here.

Folders are found by ID, never by name: two other folders in Drive are also called "Heartside", and four are called `03_Social-and-Ads`. Folder IDs survive a rename and a move.

## The tree

```
My Drive / Ventures / Active Ventures / Heartside/          1QInHx-RNx9fXYdc0KSvTYRcuGTZHxcVh   Krish's. Read only.
├── 00_Brand-Assets/                                         19LX5N9op38Ejx1yGPjqbXX7wU1CrwKIp   Krish's. Read only. Brand Book PDF and START-HERE.txt
├── 01_Identity/                                             1aNXPwYwUS7WE0qJJCOVv2V51ztV3e86l   Krish's. Read only. Logo, icons, favicons, Fonts/, CANVA-BRAND-KIT-GUIDE.md
├── 02_Imagery/                                              1wW4iVFScNvz_-JnD5nO4eHJKnCjemlSe   Krish's. Read only.
│   ├── Product-Examples/                                    1ZMucIvPsyCcI6tJ8C0BEWWnKE_JBiPDz   the approved product artwork; read its 00-READ-ME.txt first
│   └── Photos/                                              1Wwm8wo3M5XavxgNPMeLYyVCQG3YQi2Vd   stock dog photos, not product artwork
├── 03a_Social-Production/                                   1Z2FeYx2hoBX0z8vP5jTHaGV0kBbsI9Fg   ITERATING. Creatives in progress. Never posted from.
│   ├── Profiles/                                            1IW_1t17jwCepQ-3TxuSRopE1sOPBO-gd   Krish's. Read only.
│   ├── Product-mockups/                                     1oIx6f9TvmL2OOFjAqgvHQS1B18nE4xWK   Krish's. Read only.
│   └── YYYY-MM-DD_<Maker>-<Topic>/                                                             one folder per working session (rules below)
│       e.g. 2026-11-09_Codex-Creative-Session_Not-for-Publishing/  1gwVjIYoDAJSEshJ4dBFJ5Sq_XL-rG1GW   Codex's archive of 7 to 9 Nov
├── 03b_Social-Schedule/                                     1AHZLgwj1nHemNJeP56fQU6iTpgIEALzZ   READY. What Codex posts from. Was 05_Social-Library.
│   ├── 00 README for Codex                (Doc)             1KQrrlXEHk6QwoEdlm30zuGWBw22uNoxTHuNbCZoXFyU   The one live instructions (3 Nov 17:45).
│   ├── 01 Posting strategy                (Doc)             1OT8Cx18mbSpxrDq4c_Buj63JbMon2WfD2nOJMtREojg
│   ├── 02 Schedule and captions           (Sheet)           15rHaDxdYtdK4eFmUC4GSbBGAnhlSOO0K67Gl0NozIdU   F03, F05, F06 x3, F07, F10, F11, F12, 4 to 8 Nov
│   ├── 02c Schedule and captions (F01 F02 F04) (Sheet)      1L-bCycPmND3OLm0lo7FJVrPi1xV92deLw-sJVoz0cn8   locked 3 Nov, 9 and 10 Nov
│   ├── 02d Schedule and captions (F13)    (Sheet)           1eY_iFenDdrsMuSlSoexKUEYjDQ41eX5GJ5lSd7CFfdg   F13 photo, 3 Nov
│   └── Posts/                                               1boYZjB7ma-1YIcKzSl51usdYuNk6faHO
│       ├── F01/ … F07/, F10/ … F13/, F06-frenchie/, F06-dachshund/, F06-lab/   locked 3 Nov (F13 1poEUrkd3Cd5t4ah7JjnrNMfvY2WyB71e)
│       ├── F17/ … F24/                                                          filed 5 Nov
│       ├── F25/ … F27/                                                          filed 7 Nov
│       │   └── heartside_<id>_<slug>_<kind>.<ext>                               the post's media, nothing else
├── 04_Decks/                                                1oqA94p1gx-Yxo8xO7WJ_8ZMz-Oi6Qu5P   Krish's. Read only.
├── 09_OLD - Historical-and-Source/                          1BJkmC3-Hk6WkSl0MeQjgoWRtEcAvpmiB   Krish's. Read only. Superseded identity, Biscuit, ornament, old scenes. Never reused as current.
├── _Archive/                                                1zPLSgX44QaIZK6gwmnnRz7lr60kzg9qQ   Krish's. Read only.
└── POSITIONING.md, V3-GIFTS-FROM-YOUR-DOG.md, SYNC.md                                           Krish's. Read only.
```

F17 to F27 are in `Posts/`, but the live README lists only 02, 02c and 02d, and those Sheets were last changed on 3 and 4 Nov, before F17 was filed on 5 Nov. Their folders existing does not make them postable: only an `approved = yes` row in a Sheet the live README lists does.

## The one-way path: 03a to 03b

A creative moves in one direction only.

1. **Iterate in 03a.** Drafts, review renders, contact sheets, review pages, rejected versions and the notes about them go in a dated session folder in `03a_Social-Production`.
2. **Krish locks it.** He approves the exact files on the lock page (the claude.ai artifact) and the lock is recorded in `factory/locks`. Nothing in 03a is approved because it is in Drive, however finished it looks.
3. **The engine sends the locked files to 03b.** `python3 factory/send_library.py <library folder>` files the release media in `03b_Social-Schedule/Posts/<post id>/`, and the engine adds the rows to a `02…` Sheet.
4. **Krish marks the row `approved = yes`, and Codex posts it.**

Nothing is ever copied, moved or dragged from 03a into 03b, by a person, Codex or a connector. A file in 03b always comes from the lane, rebuilt from the locked spec and checked against its sha256. Nothing in 03a is posted, scheduled, linked from a Schedule row or treated as a source of truth for what is live.

## Who writes what

| Where | Who writes it | How | Nobody else |
|---|---|---|---|
| `Heartside/` outside 03a and 03b | Krish only | by hand | The engine and Codex never create, move, rename or delete anything here |
| `03a_Social-Production/Profiles/`, `Product-mockups/` | Krish only | by hand | Read only for everyone else |
| `03a_Social-Production/` session folders | the growth engine (Drive connector) and Codex | one new dated folder per working session | Only the session that created a folder writes into it, and only while that session runs. Afterwards it is read only. No files loose at 03a's top level |
| `03b_Social-Schedule/` top level | the growth engine only | the Drive connector | Exactly the files in the tree above, plus a new `02<letter>` Sheet when a batch needs one (below). No other files and no new folders |
| `03b_Social-Schedule/Posts/<post id>/` | Krish's home computer only | `python3 factory/send_library.py <library folder>` through content-engine's library lane | No one uploads, copies or makes a folder here by hand or through a connector. It is never edited or deleted from a session; the home computer writes new versions beside changed ones |
| `02…` Sheets, columns `status`, `live_url`, `notes`, and a `Results` tab | Codex only | after it posts | Codex changes no other column, row or file |
| `02…` Sheets, column `approved` | Krish only | by hand | The engine never writes `yes` |

## The rules for a 03a session folder

1. **One folder per working session**, named `YYYY-MM-DD_<Maker>-<Topic>`, with the New York date the session started. `<Maker>` is `Engine`, `Codex` or `Claude`; `<Topic>` is a few words joined by hyphens. Add `_Not-for-Publishing` if the folder could be mistaken for release media. Never one folder per file, and never a folder inside another session's folder.
2. **A `START-HERE.md` at its top**, written first: what the session was making, which post ids or concepts it covers, where it stopped, what Krish decided, and the one next step. Say in its first line that nothing in the folder is approved for publishing.
3. **Anything inside is fine for iterating**: renders, frames, stills, voice reads the session made, contact sheets, review HTML, prompts, manifests, zips. Reference post ids by the same ids the lane uses (`F28`, `F06-frenchie`) so a later session can find them.
4. **Never in 03a**, or anywhere in Drive: licensed music or stems, credentials or upload envelopes, browser profiles, and anything from an order, checkout or customer (rule 6 in `AGENTS.md`).
5. **A later round is a new folder**, not an edit of the old one. Old folders stay where they are; only Krish moves or deletes them, for example into `09_OLD` or `_Archive`.

## The rules for a new post in 03b

1. **Post id.**
   - A new concept takes the next free number. F27 is the highest in `Posts/` today, so the next is `F28`. Check `Posts/` and `factory/specs` before choosing. Never reuse a number, even for a retired concept.
   - A variant of a locked concept is `<id>-<breed>`, for example `F06-frenchie`. Ids match `[A-Z][0-9]{2,3}(-[a-z0-9]+)*`, and the lane refuses anything else.
2. **File names** are `heartside_<id>_<slug>_<kind>.<ext>`:
   - `<slug>` is lowercase words joined by hyphens, the same for every file of the post.
   - `<kind>` is one of:
     - `reel` (mp4);
     - `cover` (jpg);
     - `slide1` to `slide5` (jpg).
   - Nothing else goes in a post folder: no source files, no drafts, no captions files, no subfolders. Those belong in a 03a session folder.
3. **Media.** Add the locked files to the library folder and to its `manifest.json` (post, file, bytes, sha256). Then run `send_library.py`. The home computer files them within about 20 minutes. Check `03b_Social-Schedule/Posts/<post id>/` afterwards (by folder ID `1boYZjB7ma-1YIcKzSl51usdYuNk6faHO`): if a new `05_Social-Library` folder appeared instead, the lane is still writing by the old name, so stop and tell Krish.
4. **A changed version** keeps its name and is sent again. The home computer replaces its own earlier copy in place. Never send a "v2" or "final" file name.
5. **Schedule rows.**
   - A post scheduled for the first time gets its rows in a new Sheet `02<next letter> Schedule and captions (<ids>)`, with the same 16 columns as `02`. The next letter is `e`.
   - The connectors cannot edit Sheets they did not create, so one batch gets one Sheet, and never one per post.
   - Rows for a post not yet locked say `awaiting Krish's lock: do not post` in `notes`.
   - The live README lists every `02…` Sheet. Update it in the same step.
6. **Superseded never means deleted.** A Sheet or README that a newer one replaces is renamed "(superseded <date>, use …)" and kept. Codex never posts from it and the engine never edits it. Only Krish deletes: on 3 Nov he had the six superseded READMEs and 02b moved to Drive's trash ("Delete the superseded READMEs and 02b"). The engine trashes a file only on his word for that named file, never permanently.
7. **The README.**
   - If its text changes, the growth engine writes a new "00 README for Codex" and renames the old one "(superseded <date>, use the newer one)". There is only ever one live copy.
   - Superseded copies are never edited. Krish may delete them.
8. **A retired post**
   - stays where it is;
   - gets `retired` in `notes` on its rows;
   - is never deleted or moved by the engine or Codex.

## What is deliberately not in Drive

- The **lock page** (claude.ai artifact) is where Krish locks posts and approves lines.
- The **joke bank, specs and locks** live in this repository: `factory/bank`, `factory/specs` and `factory/locks`.
- **Licensed music** and anything carrying a credential stay on the machine that builds. Every other build source may be kept in a 03a session folder.
- The **checksummed zip backup** is hosted outside Drive and linked from the README.

## History

- 2026-11-09: Krish flattened `00_Brand-Assets`. `01_Identity`, `02_Imagery` and `04_Decks` moved up to `Heartside/`; `03_Social-and-Ads` became `03a_Social-Production`; `05_Social-Library` became `03b_Social-Schedule`; `05_OLD - Historical-and-Source` became `09_OLD - Historical-and-Source`. The library kept its ID (`1AHZLgwj…`), so Drive links to it still work. The old names are read from `00_Brand-Assets/START-HERE.txt` (30 Oct), which Krish has not yet updated.
- 2026-11-03: the first map, with `05_Social-Library` as the only folder the engine and Codex used.
