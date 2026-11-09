# Heartside's Drive: what is where, and who may write it

Read from live Drive on 2026-11-03. Krish: "be strict on what goes where as codex tends to sprawl drives quite easily". This map is the rule. Anything not listed here does not get created. When a rule here and a habit disagree, the rule wins. If a file needs a new home, ask Krish first and add it here.

Folders are found by ID, never by name: two other folders in Drive are also called "Heartside".

## The tree

```
My Drive / Ventures / Active Ventures / Heartside/          1QInHx-RNx9fXYdc0KSvTYRcuGTZHxcVh   Krish's. Read only.
├── 00_Brand-Assets/                                         19LX5N9op38Ejx1yGPjqbXX7wU1CrwKIp   Krish's. Read only.
├── _Archive/                                                1zPLSgX44QaIZK6gwmnnRz7lr60kzg9qQ   Krish's. Read only.
├── POSITIONING.md, V3-GIFTS-FROM-YOUR-DOG.md, SYNC.md                                           Krish's. Read only.
└── 05_Social-Library/                                       1AHZLgwj1nHemNJeP56fQU6iTpgIEALzZ   The only folder the growth engine and Codex use.
    ├── 00 README for Codex                (Doc)             1KQrrlXEHk6QwoEdlm30zuGWBw22uNoxTHuNbCZoXFyU   The one live instructions (3 Nov 17:45).
    ├── 01 Posting strategy                (Doc)             1OT8Cx18mbSpxrDq4c_Buj63JbMon2WfD2nOJMtREojg
    ├── 02 Schedule and captions           (Sheet)           15rHaDxdYtdK4eFmUC4GSbBGAnhlSOO0K67Gl0NozIdU   F03, F05, F06 x3, F07, F10, F11, F12, 4 to 8 Nov
    ├── 02c Schedule and captions (F01 F02 F04) (Sheet)      1L-bCycPmND3OLm0lo7FJVrPi1xV92deLw-sJVoz0cn8   locked 3 Nov, 9 and 10 Nov
    ├── 02d Schedule and captions (F13)    (Sheet)           1eY_iFenDdrsMuSlSoexKUEYjDQ41eX5GJ5lSd7CFfdg   F13 photo, 3 Nov
    └── Posts/                                               1boYZjB7ma-1YIcKzSl51usdYuNk6faHO
        ├── F01/ … F13/, F06-frenchie/, F06-dachshund/, F06-lab/    one folder per post id (F13 1poEUrkd3Cd5t4ah7JjnrNMfvY2WyB71e)
        │   └── heartside_<id>_<slug>_<kind>.<ext>                  the post's media, nothing else
```

## Who writes what

### Session archive exception — 9 November 2026

Krish explicitly requested this session's summary and all created/iterated assets
be stored in a separate schema-compatible Drive subfolder without interfering
with live posts. Authorized destination:
`Heartside/_Archive/2026-11-09_Codex-Creative-Session_Not-for-Publishing/`
([Drive folder](https://drive.google.com/drive/folders/1gwVjIYoDAJSEshJ4dBFJ5Sq_XL-rG1GW)).
This bounded exception permits the session source/iteration backup and summary
there; it does not expand permissions for other folders or alter the live library.
Archive files are never a publishing input. Read START-HERE.md for the held
artwork status and ASSET-INVENTORY.csv for the exact archived paths/checksums.

| Where | Who writes it | How | Nobody else |
|---|---|---|---|
| `Heartside/` outside `05_Social-Library` | Krish only | by hand | The engine and Codex never create, move, rename or delete anything here |
| `05_Social-Library/` top level | the growth engine only | the Drive connector | Exactly the files in the tree above, plus a new `02<letter>` Sheet when a batch needs one (below). No other files and no new folders |
| `Posts/<post id>/` | Krish's home computer only | `python3 factory/send_library.py <library folder>` through content-engine's library lane | No one uploads, copies or makes a folder here by hand or through a connector. It is never edited or deleted from a session; the home computer writes new versions beside changed ones |
| `02…` Sheets, columns `status`, `live_url`, `notes`, and a `Results` tab | Codex only | after it posts | Codex changes no other column, row or file |
| `02…` Sheets, column `approved` | Krish only | by hand. His approval in chat also counts, recorded by Codex in `notes` as "Approved in chat" with the date (Ruling, Krish, 2026-11-04) | The engine never writes `yes` |

## The rules for a new post

1. **Post id.**
   - A new concept takes the next free number: `F13`, `F14` and so on. Never reuse a number, even for a retired concept.
   - A variant of a locked concept is `<id>-<breed>`, for example `F06-frenchie`. Ids match `[A-Z][0-9]{2,3}(-[a-z0-9]+)*`, and the lane refuses anything else.
2. **File names** are `heartside_<id>_<slug>_<kind>.<ext>`:
   - `<slug>` is lowercase words joined by hyphens, the same for every file of the post.
   - `<kind>` is one of:
     - `reel` (mp4);
     - `cover` (jpg);
     - `slide1` to `slide5` (jpg);
     - `paid-reel`, `paid-reel-a`, `paid-reel-b` (mp4) and `paid-cover` (jpg): paid cuts, kept in the same post folder (Krish, 4 Nov: "one uniform folder with uniform naming conventions"). They are used only under `docs/PAID-BOOSTS.md` and recorded in `library/manifest.json` (`docs/BOOST-LIBRARY.md`).
     - `review-reel` (mp4) and `review-cover` (jpg): a candidate waiting for Krish's lock, so the growth engine can read it through the library (Krish, 4 Nov: "drop assets in your folder of choosing"). **Never posted, never scheduled.** Once Krish locks it, the engine sends the locked file again as `reel` or `cover` (rule 4). The review file stays, and the manifest marks it `superseded`.
   - Nothing else goes in a post folder: no source files, no drafts, no captions files, no subfolders.
3. **Media.** Add the files to the library folder and to its `manifest.json` (post, file, bytes, sha256). Then run `send_library.py`. The home computer files them within about 20 minutes. Check the Drive folder afterwards.
4. **A changed version** keeps its name and is sent again. The home computer replaces its own earlier copy in place. Never send a "v2" or "final" file name.
5. **Schedule rows.**
   - A post scheduled for the first time gets its rows in a new Sheet `02<next letter> Schedule and captions (<ids>)`, with the same 16 columns as `02`.
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
- The **build sources** (frames, voice reads, licensed music) stay on the machine that builds. They are never in Drive or git.
- The **checksummed zip backup** is hosted outside Drive and linked from the README.
