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

## Motion templates rendered by HyperFrames (15 November 2026)

`hf.py` builds the `note` template (the dog's gift line arriving word by word on a paper note, then the real render)
with HyperFrames, an HTML-to-video renderer pinned in `hyperframes/`. It adds browser type and easing and nothing
else: the spec carries line ids and a render like any other, `lock.py check` gates it first, and the finished file
passes `codex/check_picture.py` and `lock.py media` and a pixel check on the product. See
[`hyperframes/README.md`](hyperframes/README.md).

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

## Generated dog stills: the roller and the still check (15 November 2026)

Krish, 10 November 2026: "The dogs in all these videos look way too perfect and not real, and slightly scruffy enough." (floor `real-scruffy-dogs`). Asked plainly for a dog, an image model hands back the same brushed, well-lit pet every time. So a generated dog still's prompt is rolled by `dog_roll.py`, never written by hand. The roller draws every attribute from `bank/dog_pools.json` with the operating system's randomness:

- the breed or mix, coat colour and its real flaws, age, build and collar;
- the room or yard, where the owner's phone is and how far away;
- the clutter, the light and its white-balance cast;
- 3 to 5 iPhone processing artifacts.

Its avoid list blocks the polished look and every floor rule a prompt can break. It keeps no breed or setting twice in a batch, and remembers recent rolls in `local/`. The joke is never rolled: what the dog does is the approved script's beat, passed verbatim.

The route, for every generated dog still:

1. **Read the floor.** `python3 growth.py floor --format still`.
2. **Script first.** Write the beat against `docs/HUMOUR.md` and score it at tier 2. Only a 9 on paper is generated (floor `spend-means-nine`).
3. **Roll.** `python3 growth.py still roll --count N [--slot S01 | --breed golden] [--setting kitchen] [--action "<the beat, verbatim>"] [--frame video]`. `--list` shows the breed and setting keys. Send each prompt and its `aspect_ratio` to the generator untouched. To change anything, lock a flag and roll again: an edited prompt fails the check by its SHA-256.
4. **Reserve.** `python3 growth.py still reserve <roll id> --script-score 9 --by "<the maker>" --credits <the provider's quote> --quote-source "<where it was read>" --quoted-at <ISO time> --allocation "<the approved share>" --credit-allowance <its credits>`. This runs the prompt-stage check first and reserves nothing if the still is held. It then reserves through the provider ledger (`docs/PROVIDERS.md`), with the exact prompt in the brief. In a session with the Control Center connector, the spend is also booked with `reserve_credit_spend` (`docs/CREDITS-SESSION.md`).
5. **Generate, once.** `python3 growth.py provider transition <request id> submitted`. Generate with the record's prompt and aspect ratio exactly. Then `provider transition <request id> completed --receipt <receipt.json>`.
6. **Review independently.** A judge who is not the maker reads the still at full size and on a contact sheet.
   - `python3 growth.py still review <roll id> --template > review.json` prints every verdict the floor is owed.
   - Answer each with `pass`, `hold` or `n/a` (an `n/a` says why), and add the tier 2 score and its reason.
   - Then `python3 growth.py still review <roll id> review.json`. It binds the file by its SHA-256 and runs the check.
7. **Only a pass goes on Krish's review board.** `python3 growth.py still check <roll id>` re-runs the check at any time (`--stage prompt` before the spend).

Every failure names its floor entry and Krish's own words. What the check reads (`engine/stills.py`):

| Floor entry | What code checks |
|---|---|
| `real-scruffy-dogs` | The prompt is the roller's, unedited, with its realism block (a phone photo, coat flaws, clutter, 3 to 5 artifacts) and its avoid items. It asks for no polished look, and the credits were reserved for this exact prompt |
| `real-dogs` | The avoid list guards against extra, missing or merged legs, paws, tails, ears or eyes |
| `no-badges` | No words, sign, label, logo or watermark asked for in the frame |
| `real-product` | No mug, blanket, portrait, painting, framed picture or card drawn |
| `troll-not-mild` | No human smile, grin, wink or side-eye on the dog |
| `dog-does-dog-things`, `one-trend-one-scene` | No human arms or hands on the dog; nothing upright on its hind legs or choreographed |
| `no-ai-label` | Nothing in the record asks for the platforms' AI label |
| `spend-means-nine` | A tier 2 script score of 9 before the spend, and a finished score of 9 before the board |
| `ten-out-of-ten` | A score and its reason on the still |
| every still entry whose check is a review | A recorded verdict from a reviewer who is not the maker; a `hold` holds the still |
| `lock.py` STANDING | No chestnut or red dachshund, and Buddy never drawn |

Every check is keyed to a floor entry that must exist. A new still entry Krish adds to `floor.json` is owed a verdict at once.

## The joke lab (17 November 2026)

`factory/jokelab.py` decides what joke gets made. The judging panel below decides whether it was made well. On 17 Nov
one inherited idea, a retread of the live F38, went through seven cuts. The judge score climbed from 7 to 9 on
pictures alone, and Krish said: "No, it's not funny - the post that is already live on this topic is 10x better". The
lab closes each step where that went wrong:

| Step | Command | What it stops |
|---|---|---|
| Write wide | `jokelab.py brief TOPIC --n 30` | One inherited idea as the whole slate. The brief carries his formula ("the parody is in the words, and the dog does real dog behavior"), the core, the floor's quotes, every live post, and weighted families: alibi, format parody, rule lawyer, status puncture, group roast, literal staging, escalation list. The alibi family leads because it earned 68 to 126 reactions per 1,000 against medians of 29 and 40 (`docs/audits/2026-11-15-interest-vs-paid.md`) |
| Screen | `jokelab.py screen CANDIDATES.json [--live]` | Retreads of a live or locked post, judged on its real words and pictures. A dog doing a human act outside literal staging. Rule 5 copy breaches, through `growth.py problems`. A missing core part. Near duplicates. A slate under 12 candidates or under 4 families. With `--live`, the humour engine (krishanraja/humour-engine) reads each joke through Control Center's humour route on `CONTROL_CENTER_ENGINE_TOKEN` and rejects it when it finds no supported reading, no stupid premise, no payoff with an edge, or more than one outside reference. It also flags a payoff spent before the last line |
| Judge the words | `panel.py brief tier2` on the shortlist only | Polishing an idea that is not funny on paper. Only the top four go to the judge |
| Build, cut by cut | `jokelab.py cut RUN CAND --score N --words FILE` | Exits 1 and warns after three cuts with the same words, or when the score rose and the words did not |
| Learn | `jokelab.py verdict RUN CAND yes\|no "his words"`, `jokelab.py taste` | Forgetting him. Each verdict moves its family's weight in the next brief and ranking. A family or mechanism becomes a rule only on two or more agreeing verdicts, so one no is never a rule. A no still goes to `floor.json` and his taste ledger as before |

Install for `--live`: `pip install -r requirements-humour.txt && pip install --no-deps -r requirements-humour-engine.txt`.
Without it, or without the token, `screen` runs the code gates and says so. Runs are kept in `local/jokelab/`. His
verdicts go to `bank/verdicts.jsonl`, from interactive sessions only. The humour engine holds no taste: Krish's taste is
`docs/HUMOUR.md`, ai-harness `krish-voice` references/humour.md, the floor and these verdicts.

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
