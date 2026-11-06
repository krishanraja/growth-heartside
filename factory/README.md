# The post factory and its lock

Krish, 2 Nov 2026: "We need to figure out a way of making this reliable so that we don't get drift and
we don't get weird humor and things that don't make sense once stuff is locked in. After that, I can
trust the system to autonomously drive growth."

One approved post becomes many by changing only its slots. Nothing else can move.

## The pieces

| File | What it holds |
|---|---|
| `bank/lines.json` | Every word a post may show or say. Each line has a role, the breeds it is true for, and a status. Approved lines carry a hash of their exact words, so an edit un-approves them. |
| `bank/renders.json` | The real store renders a post may show, with checksums, breed and product. |
| `specs/` | One spec per post: a template, line ids, render files, timings, music and sound. There is no free text. |
| `locks/` | A locked post: its fingerprint, Krish's words approving it, and its slots. |
| `build.py` | Templates: `chat`, `search`, `roast` (carousel plus reel) and `film` (key frames, voice, music). |
| `lock.py` | The gates, the reviewer brief, the ledger and the trust ramp. |

Assets stay out of git, because the repository is public and the music is licensed. Set `HEARTSIDE_ASSETS` to a folder holding `renders/`, `frames/`, `audio/` and `fonts/`. The ledger goes to `local/factory/ledger.json` (`HEARTSIDE_LEDGER`), and posts go to `local/media/factory` (`HEARTSIDE_OUT`).

## How a post goes out

1. `python3 factory/lock.py check SPEC`. This is the static gate. It holds a post for any of these:
   - a line that is not in the bank;
   - a line Krish has not approved, or one edited since he approved it;
   - a line said by a breed it is not tagged for;
   - a line retired after a decline;
   - a house copy rule from `growth.py` that fails;
   - a render that is not the approved file, byte for byte, or one that shows another breed;
   - shots that end before the voice does;
   - drift from the lock's fingerprint.
2. `python3 factory/build.py SPEC`. It refuses a held spec. `--preview` builds one anyway, only so Krish can judge proposed lines in place.
3. `python3 factory/lock.py media SPEC MP4`. This checks the post is 1080x1920 with sound, 6 to 60 seconds long, between -18 and -13 LUFS, and ends on the product card held for at least 3 seconds.
4. `python3 factory/lock.py brief SPEC` gives an independent reviewer the beats plus the standing checks. The reviewer has never seen the maker's reasoning and looks at the actual frames. Record its verdict with `lock.py record SPEC reviewer-pass` or `reviewer-hold`. When a reviewer catches something new, it joins `STANDING` in `lock.py`.
5. `python3 factory/lock.py gate SPEC MP4` runs everything above, plus the trust ramp:
   - the first 5 variants of every lock go to Krish, then 1 in 10;
   - `krish-decline` retires that variant's line and breed pairs;
   - two declines pause the lock.
6. Only then does the post become a Control Center go-live, under concept-level approval.

## Locking and slots

`lock.py lock SPEC --by "<Krish's words>"` freezes an approved post. Its fingerprint is the sha256 of the post's skeleton: every line is replaced by its role, every render by its product type, and the cast and breed by slot names.

A variant passes only if it has the same skeleton, which means:

| Template | What may vary |
|---|---|
| Chat, search, roast | Which dog plays which part, which approved line fills each role, and which real render of the same product closes it |
| Film | Nothing but the end render. The voice is recorded, so its lines are frozen |

## Adding humour

New lines enter `bank/lines.json` as `proposed`, tagged with their role and breeds. They reach Krish in batches, approve or kill. Only an approved line can ever appear in a post.
# Platform UI acceptance (6 November 2026)

Read [the creative UI contract](../docs/CREATIVE-UI.md) before each new build.
Chat and film defaults now use the shared house working region. Exact locked
masters keep their geometry; opt an intentional revision into
`ui_profile: social-ui-2026-11-06-v1` and obtain a new approval.
`lock.py gate` requires `--release` and `--review` evidence for the specific
placement. A file-level media audit alone is never release clearance.
