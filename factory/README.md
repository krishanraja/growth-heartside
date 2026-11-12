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

Assets stay out of git, because the repository is public and the music is licensed. Rebuild the library in any session with `python3 factory/fetch_library.py <dir> --shimmer-url <signed Epidemic url>` (sources and checksums in `factory/bank/library-sources.json`); it rebuilt F34 byte for byte on 10 Nov. Set `HEARTSIDE_ASSETS` to a folder holding `renders/`, `frames/`, `audio/` and `fonts/`. The ledger goes to `local/factory/ledger.json` (`HEARTSIDE_LEDGER`), and posts go to `local/media/factory` (`HEARTSIDE_OUT`).

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
3. `python3 factory/lock.py media SPEC MP4`. This checks the post is 1080x1920 with sound, 6 to 60 seconds long, between -18 and -13 LUFS, in the export preset of the 12 Nov corpus, ends on the product card held 3 to 4 seconds, and that its layout manifest (written by the renderer, bound to the file's SHA-256) keeps every hook, subtitle, label, chat and product inside the corpus regions (`docs/CREATIVE-UI.md`).
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
Every template now renders in the 12 Nov corpus profile (`ui_profile: social-corpus-2026-11-12-v2`), which
every spec declares. Placement is not part of a lock's fingerprint, so moving a locked post onto the profile
keeps its approval; a content change still needs a new one.
`lock.py gate` requires `--release` and `--review` evidence for the specific
placement. A file-level media audit alone is never release clearance.

## Generated dog photography: review before export

Krish, 8 November 2026: "These dogs look fake and sometimes malformed."
Apply this production review before selecting a generated source, then repeat
it on the final platform crop. This operational correction does not constitute
approval of a new taste rule or the corrected artwork.

- Inspect full resolution and phone-size composition. Check scale against
  furniture and people, limb attachments, joints, paws, tails, ordinary
  occlusion, and believable contact with the ground or supporting surface.
- Use natural breed expressions and physically plausible poses. Do not force
  human smiles or side-eye, stretch bodies, or invent anatomy to stage a joke.
  The situation and caption must carry the humor.
- Reject unclear anatomy; cropping a defect out of view is not a repair.
  Prefer an ordinary pose to a complicated pose that reads as synthetic.
- Record visual observations against the exact export. Dimensions, hashes and
  copy checks do not establish realism or creative quality. Keep unresolved
  candidates held; do not infer acceptance from successful rendering.
- Label fictional generated scenes honestly in review records. Never present
  them as real customers, testimonials or documentary evidence.

See [the 8 November correction packet](../docs/briefs/2026-11-08-organic-anatomy-correction.md).

## The judging panel (10 November 2026)

Krish asked for a simple panel that holds every output to 10/10 without burning tokens or hours. `factory/panel.py`
runs it in four tiers:

- **Tier 0: code.** The sprint slot, its spec and its media. Free.
- **Tier 1: a Haiku sub-agent.** Six yes-or-no floor questions (`bank/anchors.json`) asked of one tiled image of up
  to four contact sheets (`panel.py batch`). One read per call: three separate reads cost about 142k tokens on
  10 Nov.
- **Tier 2: a Sonnet sub-agent.** Scores only Tier 1's survivors against the tens in `bank/anchors.json` and Krish's
  floor quotes. Only 9 and above reach his review page.
- **Tier 3: views at 72 hours.**

Every verdict and Krish's own yes or no go to `local/factory/panel.jsonl`; `panel.py agreement` shows how often the
panel matched him. Below 80%, the anchors are rebuilt before the next batch. Its first live run on 10 Nov failed
three dance shots on `payoff`: a dance alone is not a joke, so the post gained an ending gag.
