# Changes Krish made to the growth engine

Newest first. Record his words with the date, then change the job file and
`automations.json` together.

- 2026-11-09: three decisions and #42 merged. Krish: "Go with your recommendations, open the PRs and merge #42".
  - Trolling dogs show real dog expressions, never a human smile (`factory/floor.json` `troll-not-mild`; the open conflict is closed).
  - Only `approved = yes` in the Sheet lets Codex post a row. This supersedes the 4 Nov ruling that a chat approval recorded in `notes` counted. AGENTS.md, `docs/CHANNEL-TASKS.md`, `docs/DRIVE-MAP.md`, `factory/send_library.py` and the README for Codex now say so.
  - The `ui-v1` and `ui-v2` platform editions are retired for reuse (`library/CURRENT.md`, `docs/DRIVE-MAP.md`). Posts already live stay live.
  - [krishanraja/growth-heartside#42](https://github.com/krishanraja/growth-heartside/pull/42), the 4 to 9 Nov production branch, is merged. This branch is rebased onto it, and the map keeps its paid and review file kinds.
  - Ruling (Krish, 2026-11-09): only approved = yes in the Sheet lets Codex post; chat approval no longer counts.
  - Ruling (Krish, 2026-11-09): trolling dogs show real dog expressions, never a human smile.
  - Ruling (Krish, 2026-11-09): the ui-v1 and ui-v2 editions are retired for reuse.

- 2026-11-09: the engine learns from the social desks and from failed production. Krish: "We need to upgrade the Growth-Heartside engine to ensure it learns from the attached Markdown file in terms of social media audience acquisition", "how can it improve on asset ideation > production > build based on the failed production sessions", "the goal is that Claude sessions manage Codex in the future fully", "Make sure the drive is completely up to date and not able to be corrupted or sprawled", "Ensure that the project documentation and intelligence of the growth repository are automatically augmented".
  - Social history uses the existing operator events: a `social` type with the same receipts, append-only in `local/engine.sqlite3`, and carried by the checkpoint (`engine/social.py`; `docs/ENGINE.md`, "Social history"). The desks' 4 to 9 Nov record is `docs/social/2026-11-09-engagement-history.json`. The radar and report jobs read it back.
  - `factory/floor.json` and `growth.py floor` hold every creative rejection in his words, with the rule and the check. That includes the rain session he marked failed ("The whole of this scene just feels weak and lame.").
  - `codex/README.md`: Claude runs Codex by card, through the plugin at home or the lane from the cloud. Each card has a floor and a 03a destination, and Claude checks every output at full size. `codex/INDEX.md` keeps each card's state, and the self-test lints queued cards.
  - `config/drive-map.json` and `growth.py drive audit`. Drive: a new START-HERE.txt (the 30 Oct one is kept, marked superseded), and the weekly placement review Sheet moved into 03b.
  - content-engine [krishanraja/content-engine#478](https://github.com/krishanraja/content-engine/pull/478) points the home computer's lane at `03b_Social-Schedule`. The lane wrote by path and would have stopped. heartside's `docs/SYNC.md` describes the new layout.
  - Ruling (Krish, 2026-11-09): every lesson, approval and Codex result is recorded in the repository the same session; a chat or Drive summary alone does not count. No job file or `automations.json` entry changed.

- 2026-11-09: Drive restructured. Krish: "Folder 3A is where we're iterating on creatives, and folder 3B is where they're ready for production."
  - Krish moved `01_Identity`, `02_Imagery` and `04_Decks` up to `Heartside/`, renamed `05_Social-Library` to `03b_Social-Schedule` (same folder ID), and the old social work area to `03a_Social-Production`.
  - `docs/DRIVE-MAP.md` now maps the whole tree by ID, adds the one-way path from 03a to 03b, and sets the 03a rule: one dated session folder per working session with a `START-HERE.md`, never posted from, and nothing copied from it into 03b.
  - `AGENTS.md`, `NOW.md`, `docs/CHANNEL-TASKS.md` and `factory/send_library.py` name the new folders. Review renders now belong in 03a instead of being kept out of Drive.
  - Ruling (Krish, 2026-11-09): 03a_Social-Production is for iterating creatives; 03b_Social-Schedule holds only what is ready for production. No job file or `automations.json` entry changed.
- 2026-11-06: After Krish completed billing and phone verification, the authorized single F10 USD 25 paid pilot was published. Meta returned "1 ad was published"; independent fresh-page readback at 12:56 GMT showed Processing, enabled, USD 25 lifetime and USD 0 spent. Published end remains 7 November 12:45 GMT. Paid delivery is not yet confirmed. The four USD 50 boosts remain held. See `docs/boost/2026-11-05-sandbox.md`.

- 2026-11-06: Krish: "We need to get the first paid test live ASAP." Authorized activation of the prepared single F10 Meta pilot, USD 25 lifetime over 24 hours. The four USD 50 posts remain a separate decision. Payment method connected and pixel/destination checked; Meta's required business billing information currently blocks Publish. See `docs/boost/2026-11-05-sandbox.md` for the exact account, draft and launch evidence. Paid results remain separate from the organic North Star.

- 2026-11-06: After viewing the repaired creative board, Krish: “ok, all looks good”. Human approval recorded for the exact corrected 33-placement organic batch, linked to the existing approved schedule. Scheduling was instructed to restore future approved slots and verify each persisted payload. Paid activity remains unapproved; native-device observations remain unverified rather than being converted into a passing automated review.

- 2026-11-06: Krish: “Yes, integrate this and then correct everything that is currently unpublished in terms of social posts.” Authorized recovery of original Heartside images, including Runway. Implemented the supplied social UI standard in composition and release checks, then made separately versioned editions for all 33 current unpublished placements. Original locked masters and the 4 Nov ruling remain intact. The selected files and exact verification scope are in `library/editions/2026-11-06-ui.json` and `docs/audits/2026-11-06-unpublished-correction.md`. No paid spend or published-post changes.

- 2026-11-04: Krish: “Trash these nine review files”. Moved the nine named F04, F05, F11 and F12 review files to Trash. Read back all nine recoverable entries and rechecked the 40 remaining plain-name release files against their SHA-256.

- 2026-11-04: Krish delegated the editorial release decision: “Judge yourself and get this all ready for publishing.” Codex accepted the new F10 reel, the checked F11 review cut, and the corrected F06-frenchie reel and slide 3. All 40 current files were downloaded from the library API and matched to their plain-name Drive files. The scheduling source is `library/CURRENT.md`.

- Ruling (Krish, 2026-11-04): caption move to y=1300 dropped; locked masters stay at 1440.
  - Job C closed for F01, F02, F03, F05 and F12.

- 2026-11-04: Buffer cleared for Heartside. Krish: "Can you just cancel all buffer schedules for Heartside, and we'll redo them later?"
  - All 33 scheduled Heartside posts on TikTok, Instagram and Facebook were moved to drafts, not deleted. With the 3 F10 drafts, 36 Heartside drafts remain, captions and media intact.
  - A readback shows nothing Heartside scheduled.
  - The asset-prep prompt now ends with one final library (Krish: "one final asset library in Drive and GitHub, ensuring that all old materials are no longer"): Drive folders hold only locked files (removals on his word), `library/CURRENT.md` is the single list, and superseded rows move to history.

- 2026-11-04: Queue swapped, F03 locked. Krish: "lock" (F03), then "Can you just complete everything before I move over to Codex?", then chose "Swap them here".
  - F03 is locked with its three labels, filed and read back. F11's new cut is filed as a review file.
  - 20 queued Buffer posts now carry the locked files, through permanent links that were hashed and read back: F07, F06-dachshund, F12, F04, F03, F06-lab and F05.
  - The old F10 cut's three 8 Nov posts are drafts. This replaces the earlier no-queue-edits ruling for this swap only.
  - `library/manifest.json` now marks the F05 and F12 motion finishes as locked.

- 2026-11-04: Lines approved, four posts locked, queue left alone. Krish: "1. approved 2. approved. 3. you chose. Lets finish F03 and then package all up".
  - The five replacement lines are approved; the lines they replace are retired. F04, F06-dachshund, F06-lab and F07 are locked, and their 11 files are filed to Drive with each sha256 read back.
  - The engine's call on the queue: posts already in Buffer go out as queued, under his earlier no-queue-edits ruling. The new versions go out through new schedule rows he approves.
  - F03 has three meme labels (proposed: "Operation Stocking", "The beagle:", "The gift:") and is built for his lock. It needs no new voice read.

- 2026-11-04: Every post to 10. Krish: "Yes, we need them all to be 10 out of 10. Where are your standards?", then "We need to get as close as we can without regenerating absolutely everything. We've run out of runway credits, but still have higgsfield and openai images."
  - F06-dachshund's frames were recast to the chestnut dachshund on its mug. F04's second half was redrawn in its opening room and light. F06-lab's two weak lines were replaced, with the old text removed from the frames. F07 now opens tight on the face. These are candidates in `local/library/2026-11-04-ten/`, waiting for Krish's lock. The cost was 9 Higgsfield image edits (24.75 credits).
  - The factory now opens chats mid-conversation and searches mid-typing, shows a finished search query whole, can pull back from a close-up, and keeps captions and bottom text clear of the platform interface (y 1300; 76% of the reel height).
  - Five replacement lines are proposed in `factory/bank/lines.json`. F10 and F11 are rebuilt as specs for Codex's home-machine build (`docs/briefs/codex/2026-11-04-road-to-ten-builds.md`). The plan is `docs/plans/2026-11-04-road-to-ten.md`. No job file or `automations.json` entry changed.

- 2026-11-04: Boosts are boosts of the live organic posts. Krish: "These are going to be paid organic boosts, not paid ads", then, on the engine's recommendation to promote the existing posts from Ads Manager: "Yeah, do it. Get on with it. Make sure everything is perfect and ready to roll ASAP."
  - `docs/PAID-BOOSTS.md` is rewritten. Ads Manager uses the existing post, optimises for landing page views, and adds a Shop now button to the product page with `utm_medium=paid_social`. The cap is $250.
  - The four arms are F12, F05, F02 and the F06-frenchie carousel. The earlier $90 F12 opening A/B is replaced, because its guard-first arm is not a live post.
  - The launch packet is `docs/boost/2026-11-launch-packet.md`, and the Codex card is `docs/briefs/codex/2026-11-04-boost-drafts.md`.
  - F04's motion version was held. Krish: "The golden video chops a bit. It doesn't tell a great narrative story in terms of the scene progression." F05's and F12's motion versions are locked and filed, with their sha256 read back.

- 2026-11-04: Motion versions locked. Krish: "Happy to lock, presuming you're happy with assets that are part video, part still?" The engine confirmed it was.
  - Seven reels (F01, F02, F03, F06 x3, F07) and three covers (F07, F10, F11) were filed through the library lane under their plain names, replacing the earlier locked files. Each sha256 was read back from the library. The plans are in `factory/motion/`.
  - Superseded the same day: the engine had told Codex to re-attach media in Buffer, which failed. Krish: "Why have you fucking told it to use Buffer?" Queued posts now publish as queued, the motion versions go out from the next schedule batch, and nobody edits the live queue. The F03 Instagram item that Codex's failed swap had left on an expiring link was restored by the engine to its approved Buffer-hosted reel and read back.
  - `factory/send_library.py` now also reads the engine key from Windows Credential Manager (`Mindmake/engine-operator-token`), as content-watcher does, so Codex's home-computer runs can send.

- 2026-11-04: Paid test plan, chat approval and the dachshund render. Krish: "Yes to all your 4 questions."
  - **The $250 Meta-only paid test** (`docs/PAID-BOOSTS.md`) is approved as a plan, accepting its trade-off against the $0-paid North Star. Launching it is still a separate go-live of exact files, budget and dates.
  - **Chat approval counts for posting.** AGENTS.md, `docs/DRIVE-MAP.md`, `docs/CHANNEL-TASKS.md` and `factory/send_library.py` now accept `approved = yes`, or "Approved in chat" with the date in `notes`.
    - The question was either/or ("keep posting on chat approval, or wait until you mark rows yes?"). The engine read "yes" as "chat approval is the rule", the practice already in use. If he meant the Sheet column only, that is one line to reverse.
  - **A black-and-tan dachshund render from heartside** is approved. The brief is `docs/briefs/2026-11-04-heartside-dachshund-render.md`.
  - The fourth question, the music licence, was already settled (below). No job file or `automations.json` entry changed.

- 2026-11-04: Music licence settled for paid use. Krish: "Just use the music. I have the right license for the post type. Mark this as complete permanently."
  - Gate 1 of `docs/PAID-BOOSTS.md` is closed for good. Paid cuts keep the locked track, and every `paid_gates.music_ads` in `library/manifest.json` is `true`.
  - The audit, the publishing playbook and the Codex card no longer raise it. No job file or `automations.json` entry changed.

- 2026-11-03: Drive cleanup. Krish: "Delete the superseded READMEs and 02b".
  - Seven files in `Heartside/05_Social-Library` were moved to Drive's trash, where Drive keeps them for 30 days: the six READMEs titled superseded, and "02b Schedule and captions (superseded 3 Nov, use 02c)".
  - The folder now holds exactly: "00 README for Codex", "01 Posting strategy", 02, 02c, 02d and `Posts/`.
  - The tree in `docs/DRIVE-MAP.md` matches, and its rule 6 records that only Krish's word deletes.
  - Ruling (Krish, 2026-11-03): superseded Drive copies may be trashed once he names them. No job file or `automations.json` entry changed.

- 2026-11-03: F01, F02 and F04 locked. Krish: "Lock F01, F02 and F04, keep the dachshund".
  - Their 20 lines are approved with text hashes. The standing check carries his exception: F01's red dachshund in its green sweater matches the store's own render.
  - The final independent review held F01 (the opening shot hid the dog, the tape measure had stray numbers, the wink lost the sweater) and F04 (the person's clothes changed, and captions covered the golden's face and the blanket). Six frames were regenerated (16.5 Higgsfield credits, reserved and settled) and the captions were moved. The reviewer then passed all three.
  - Locked: F01 `cdb20995`, F02 `bf8e786b`, F04 `1cb55bb3`. `lock.py gate`: all twelve posts may go out.
  - Drive:
    - the new F01 and F04 media went through the home-computer lane and were verified written;
    - "02c Schedule and captions (F01 F02 F04)" holds their rows, and 02b is marked superseded;
    - a merged "00 README for Codex" covers 02, 02c and the F13 Sheet 02d that a Codex session added, and every older README is marked superseded;
    - the backup zip was rebuilt.
  - `docs/DRIVE-MAP.md` is updated. Superseded never means deleted.
  - Ruling (Krish, 2026-11-03): F01 keeps the dachshund that matches the store's own render. No job file or `automations.json` entry changed.

- 2026-11-03: Heartside gets the home-computer lane. Krish: "Why don't you duplicate that Python script for Heartside then? We're going to need to do a lot more of this type of stuff moving forward", then chose to add Heartside to content-engine's library lane rather than build a separate copy. Then: "Keep going then until 100% done".
  - In content-engine ([krishanraja/content-engine#356](https://github.com/krishanraja/content-engine/pull/356)), the library lane takes a second library, `heartside`, with paths `Posts/<post id>/<file>`. makeyourmindup stays the default.
  - The home computer's sync writes Heartside files into `Heartside/05_Social-Library/Posts/`.
  - The recordings pass now keeps the sync's own copy up to date, so nothing needs running at home.
  - The database migration was applied to production with Krish's yes and read back: 5,303 existing rows kept as makeyourmindup.
  - `factory/send_library.py` sends the library folder through that lane. It checks every file against its manifest first and never posts anything.
  - Ruling (Krish, 2026-11-03): Heartside joins content-engine's existing library lane rather than a separate copy. No job file or `automations.json` entry changed.

- 2026-11-03: The last three concepts built, and the home-computer lane checked. Krish: "You also can queue stuff for the home computer to upload in the right place - makeyourmindup engine does it. Merge all to main", then "And then build the rest and merge again".
  - F01 Becoming the mug (absurd "Plan C"), F02 Project Nothing (the golden) and F04 Me vs my golden (meme captions) are built through the factory.
    - 16 new Higgsfield key frames, 2 of them replacements after review (44 credits).
    - New reads in the saved dachshund, golden and narrator voices (1,941 ElevenLabs characters).
    - Licensed full-quality Epidemic music; F01 keeps Mix B.
    - Every spend was reserved and settled in Control Center.
  - Their lines enter the joke bank as proposed. Locking a post approves its lines.
  - Each passed `lock.py check` apart from those proposed lines, and passed `media`. An independent review held all three; every hold was fixed and re-checked:
    - a search bar that wrapped;
    - a dog who changed between shots;
    - captions over the joke;
    - an unclear "their face".
  - One call is Krish's: F01's dachshund matches the store's own red dachshund render, which the standing check flags because it can read as Buddy.
  - They are in the library zip (39 files) and a second schedule Sheet for 9 and 10 Nov, every row marked "awaiting Krish's lock: do not post". They are on the lock page with Lock buttons.
  - The home-computer lane (`content-engine/scripts/post-pack/send.py` plus the library sync on Krish's runner) writes only into the makeyourmindup library. Its path rule refuses any other top folder, so it cannot file Heartside media into `Heartside/05_Social-Library`. Using it would put Heartside files in the wrong venture's folder. Codex keeps pulling the checksummed zip.
  - The film template takes an optional `cap_y` for meme-style top captions. No job file or `automations.json` entry changed.

- 2026-11-03: The Drive social library. Krish: "Codex will orchestrate and schedule send my posts, you need to build a library of assets in my Google drive. Strategies."
  - The nine locked posts were re-mixed with licensed full-quality Epidemic downloads in place of the review previews. Same recordings and timings; the record scratch is a licensed take.
  - Packed with checksums into one hosted zip. Media went by link because the Drive connector can't upload video; Krish chose links plus a Codex pull.
  - Drive `Heartside/05_Social-Library` holds the Codex instructions, the posting strategy, and a Sheet of 27 rows: 9 posts across TikTok, Instagram and Facebook.
  - Each row has a caption passing the copy rules, a creative id, a tracked link, the lock fingerprint and an empty `approved` column for Krish.
  - AGENTS.md records the ruling. No job file or `automations.json` entry changed.

- 2026-11-03: All nine Christmas posts locked. Krish: "Lock it all."
  - Locked: F10, F12, F03, F05 and F06 (frenchie, with the dachshund and lab as its variants). F07 and F11 were locked earlier.
  - Every post passes the full go-live gate: copy, breed, renders, drift, media, an independent reviewer pass on the exact post, and his approval.
  - The gate now matches a verdict to the exact post by spec and fingerprint, whichever lock existed when it was recorded.
  - No job file or `automations.json` entry changed.

- 2026-11-03: Troll-meme roasts and the chat punchlines.
  - On the roasts, Krish wrote: "These are not funny compared to the dash. Rewrite these in that kind of humour style. Also I don't want plain black cards. I want images that look like the dog is trolling them, like that classic troll meme image - but a dog. That vibe".
  - The frenchie roast is rewritten in the dachshund's style. All three breeds now run on 12 generated troll-grin photos with meme type, and a boom hit lands on each reveal.
  - In F10, the first reply is "Bro, that's a bone 😂". The deluded Lab is corrected with "They threw it AWAY mate 😂😵".
  - F11 is locked with his board Lock, which approves the answers shown.
  - No job file or `automations.json` entry changed.

- 2026-11-02: Organic, not ads. Krish on the nine finished posts: "We never need "EXAMPLE" badges
  anywhere, and the mugs should animate somewhat? "Your dog loves you too." isnt really needed on these
  posts, they are not paid ads remember, they should come across like organic social posts." He also
  ruled on wrapped text, the search bar and the roast music.
  - Product images carry no badge (AGENTS.md rule 4). Heartside's canon tags examples on its own store
    pages, and these posts never present a render as a customer's dog.
  - No slogan, URL or call to action on screen. Endings are the real product, moving, and links go in
    the caption.
  - Text wraps evenly and never leaves one word on its last line ("the word ... sprawled onto a second
    line ... looks shitty").
  - The search bar never grows; long searches scroll out at the start. Every search gets a punchline
    answer.
  - The roasts move from Brat to "Who's the Boss Now".
  - His board rewrites are in the joke bank in his words. Only "favourite" changed, to US "favorite".
  - No job file or `automations.json` entry changed.

- 2026-11-02: The lock system. Krish: "We need to figure out a way of making this reliable so that we
  don't get drift and we don't get weird humor and things that don't make sense once stuff is locked in.
  After that, I can trust the system to autonomously drive growth." Then: "yes, build the lock system,
  then finish the films".
  - `factory/` now holds the joke bank (lines with roles, breed tags, approval status and a hash of the
    approved words) and the render catalog (checksums). Specs carry ids only, never free text.
  - Locks freeze a post's skeleton by fingerprint, so only the slots can vary.
  - Code gates check copy, breed fit, renders, media and drift.
  - An independent reviewer works to a standing checklist that grows with each catch.
  - The trust ramp sends the first 5 variants to Krish, then 1 in 10. Two declines pause a lock.
  - Tests are in `tests/test_factory_lock.py`.
  - No job file or `automations.json` entry changed.

- 2026-11-02: Reset to finished posts. Krish: "I swear I approved 10 concepts before, and now we've got
  only a few of them, but we've got different variations of them. I'm kind of getting a bit lost amidst all
  this now and a bit demotivated". No more boards of parts: one status page shows all ten concepts and
  the finished posts. F10 (group chat), F11 (search history) and F06 (frenchie, dachshund and lab
  carousels, each with a reel) are built in code with the locked music, and end on the real renders
  labelled Example. The session makes the humour call for F01 (absurd "Plan C"), F02 (absurd "Project
  Nothing") and F04 (meme "me vs my golden"). The round-8 board is parked. No job file or
  `automations.json` entry changed.

- 2026-11-02: Humour retune. Krish on the wave-1 animatics: "The Dog's Christmas Shopping List needs a
  rescript, its just not funny. The others need a lot more humour about them." He picked all four comic
  modes (absurd escalation, meme-text, slapstick, deadpan) at "Cheeky, still giftable": "We'll need all
  different types of assets if we intend to flood socials, and we'll need to tune the humour". F01, F02
  and F04 are rewritten in all four modes (`docs/briefs/2026-11-02-humour-rescripts.json`), each with a
  joke map and a laugh every 3 to 4 seconds, on a private humour board. Nothing is spent until he picks.
  No job file or `automations.json` entry changed.

- 2026-11-02: A Codex lane in this repository. Krish asked whether Codex is doing the asset production as
  designed, then chose "Add a lane to this repo" over queuing cards in heartside. `codex/README.md`
  mirrors heartside's lane (card, Control Center booking, branch `codex/<id>`, settle). Because this
  repository is public, the lane is picture-only: licensed music and voice never enter git, and the session
  adds the locked sound to Codex's picture. Krish adds `krishanraja/growth-heartside` to
  `config/codex-lanes.json` on his home computer. No job file or `automations.json` entry changed.

- 2026-11-02: Sound is locked for all ten concepts (F01's dip-and-fade ending approved). F04, F05 and F12
  are recast to breeds with approved renders (F04 golden, F05 and F12 frenchie), and the narrator re-read
  F04's opening with "golden retriever". Wave 1 pictures: 30 Higgsfield key frames and three animatics
  (F01, F02, F04) cut to the locked sound, on a private board for his vote. Krish asked whether Codex is
  doing asset production as designed. Not yet: heartside's Codex lane watches only that repository, so
  the final builds wait on his call. No job file or `automations.json` entry changed.

- 2026-11-02: Round 5 sound votes. F02 (take 1 over Monsieur Cat Walk) and the F05 judge (take 1) are
  approved, so sound is locked for nine of ten concepts. F01's ending is remixed: "It just ends abruptly.
  Surely, we would just lower the music and have the sprinkle over it". The music now dips under the chime
  and fades instead of cutting dead, and the sound bible rule is changed to match. No credits used. No job
  file or `automations.json` entry changed.

- 2026-11-02: Round 4 sound votes. F10 (the chat) is approved. F02's music is Monsieur Cat Walk. F01's
  Mix B is remixed so the crescendo sits under the voice and the chime fades in ("drowns out the voice
  a little bit, and then the sprinkle sound comes in really abruptly"). F02 drops "Nothing is free" and
  takes Krish's laptop line, with the dash and exclamation mark removed under the voice rules. The F05 judge
  is redirected for "way more intonation and personality". The round-5 board holds these three. ElevenLabs:
  12,507 of 20,000 booked. No job file or `automations.json` entry changed.

- 2026-11-02: Round 3 sound votes. F03, F04, F07, F11 and F12 are locked. F01 has its dachshund (option 3,
  directed "a bit miffed at the start, but then hilariously and positively takes control", never angry)
  and Mix B with the Fool Me Twice crescendo. F02 gets the line where the golden realizes it must get its
  human something, and new music (Bug-A-Boo rejected). F05 gets an American judge ("Needs an American
  accent."). F10 carries Krish's jokes. Ruling: inside an on-screen chat mock only, emojis and "WTF" are
  allowed as the dogs' own texting, while captions, voiceover and gift lines keep every voice rule (his choice:
  "Emojis yes, WTF as written"). ElevenLabs share: 10,287 of 20,000 booked; the earlier voice-design
  bookings were estimates and look high against the provider balance. No job file or
  `automations.json` entry changed.

- 2026-11-02: Round 2 sound votes. Krish locked voices for F02, F03, F04, F07 and F12 (all
  ElevenLabs-designed; every Higgsfield preset rejected) and music for all 10 concepts. He sent the
  dachshund voice back ("more like a cartoon character", "more pissed off", "younger"), and sent back the
  F02, F05, F10 and F11 scripts for more exaggerated comedy and a clearer layout. F01's wink is the real
  dog popping out of the steam, then a hard cut to the untouched mug (his choice: "Real dog winks, then
  cut"). "Use all the ElevenLabs connectors without keeping on asking me." The round-3 board holds the
  redesigned dachshund, two F01 mixes, the rewritten scripts and directed reads. ElevenLabs share used
  so far: about 8,100 of 20,000 characters, every call reserved and settled. No job file or
  `automations.json` entry changed.

- 2026-11-02: ElevenLabs share unlocked for Heartside ("elevenlabs share is unlocked fyi, do you need it?",
  then "I set all connector use to always approve"). It funds a voice designed for each recurring
  character: 3 previews each for the narrator, dachshund, golden retriever, shepherd, doodle and
  chihuahua. About 3,700 of the 20,000-character share was used, reserved and settled in Control Center.
  The designed voices sit beside the Higgsfield presets on the sound board, with an F01 sketch on the
  designed dachshund. Directed reads, with delivery tags, wait for Krish's pick of each voice. Connector
  approval changes no wall: posting, sending and new money still go through the go-live step.

- 2026-11-02: Ten concepts approved, and the sound comes first. Krish approved F01 to F07 (except
  F08 and F09), F10, F11 and F12 on the idea board: "I've approved 10 concepts. I think that's enough to
  get on with ... the audio treatment and the specifics of the humor execution are quite important to me."
  - F01's swear is bleeped, never spoken (his choice of "Bleeped").
  - The dog's inner voice is one voice per breed group (his choice).
  - The narrator and the scores are original voices and licensed genre tracks, never a real person's
    voice or a real film theme ("Yes, original in that register").
  - Take heartside's new VOICE and DOG_VOICE into growth.py ("Yes, update it").
  - Higgsfield: "Changed permissions for Higgsfield, so just carry on autonomously without asking each
    time." Every spend is still reserved and settled against Heartside's share in Control Center.
  - The funny bar is in `docs/briefs/2026-11-02-funny-bar.md`. Scripts and the sound bible are in
    `docs/briefs/2026-11-02-sound-and-scripts.json`. He votes on the takes on a private sound board.
  - No job file or `automations.json` entry changed.

- 2026-11-01: The creative platform and a round of 48 ideas. Krish: "lets kick off aggressive content
  production, i want to nail down a creative direction that can overarch various executional ideas".
  - Platform approved: "Your dog loves you too. Here's the proof." Every post shows a true act of dog
    love, then the real painting as the receipt.
  - Tone: "we need all 3 to run in rotation. we dont have enough time to test and learn". Warm first,
    funny first and pure heart run side by side and are compared, not tested in sequence.
  - The $12 printed Christmas card's 3 Dec 11:59 pm ET cutoff may be stated as its order-by line, on
    the card only.
  - "Get as divergent as you possibly can, come back to me with 40-50 ideas of all tones and
    varieties". The 48 ideas are in `docs/briefs/2026-11-01-ideas.json`, and he votes on a private
    board (Approve, Improve, Reject, with comments). His votes set the bar for each tone before any mock
    or plan proposal.
  - No job file or `automations.json` entry changed.

- 2026-10-30: Channel work runs as the seven channel tasks. Krish asked for each of seven saved Instagram
  growth prompts to be its own task for every specialist, and for a process to the North Star. They are
  defined once in ai-harness `contract/channel-tasks.md`. `crew/registry.json` maps two specialists
  (meta, tiktok) onto them, the radar, daily pack, store and report jobs run them, and
  docs/CHANNEL-TASKS.md holds the weekly loop. No new job, so `automations.json` is unchanged.

- 2026-10-29: Prepaid credits are spent by a daily scheduled session ("Scheduled sessions", Krish's answer on
  who spends them). `docs/CREDITS-SESSION.md` is its playbook; it is not one of the seven jobs, so
  `automations.json` is unchanged.

- 2026-10-29: Concept-level approval, cadence and platforms (answers in this session to a ruling his
  "Growth engines alignment" session relayed).
  - "As long as I get enough of a look at the breadth of concepts, then yes, concept-level approval
    is fine." Recorded in AGENTS.md, "Concept-level approval".
  - Cadence: 5 a day per platform (not the 3 to 4 relayed).
  - Platforms: Instagram, TikTok and Facebook. Not YouTube or X for Heartside.
  - "Right now, just get this codex artwork produced to a high standard because this is going to set
    the tone for everything." The Codex card gained a pilot gate (one job, then review) and a
    compositing recipe.

- 2026-10-29: Krish's creative answers.
  - Breed examples: "go and get codex to build out all the assets, make sure you micromanage codex
    properly", with heartside's breed batch README. Stage 1 (6 paintings) is approved; stage 2 waits
    for review and his yes. Card: `docs/briefs/codex/2026-10-29-breed-examples-stage-1.md`; checker:
    `python3 growth.py examples check --stage 1`.
  - The morph: "a video of a realistic AI dog suddenly becoming the artwork could be cool, but
    that's just one creative idea." One hero concept may morph, ending on the real render.
  - Cadence: 5 posts a day per platform once the daily layer runs.
  - Shoppable product tags: handed to a heartside build session
    (`docs/briefs/2026-10-29-heartside-shopping-tags.md`).
  - Direction: `docs/briefs/2026-10-29-creative-direction.md`.

- 2026-10-29: Krish: "ok get going", approving the mandate heartside's session
  relayed: rebuild the rule checks on heartside's current NORTH_STAR, NOW, SCOPE
  and ECONOMICS; move image-making onto the current renders and Buddy; take the
  store handle and other never-publish items out of this public repository.
  - `growth.py` reads its rules from those files and `n8n/build.mjs`; Biscuit,
    exclamation marks, the worn lines and stacked fragments are refused.
  - Krish, the same day, asked whether purchase posts may sell the mug (the
    store recommends it; heartside's economics show it below the 30% floor),
    and chose "Allow equally": every gift may be sold, the mug included. The
    one-day block on mug purchase posts is removed.
  - No job file or `automations.json` entry changed.

- 2026-10-22: Ruling (Krish, 2026-10-22): each venture's own repository is
  the only reference for its status and plan; nowhere else holds a copy.
  - The engine no longer keeps a copy of heartside's state. `growth.py sync`
    stops writing `state/HEARTSIDE-NOW.md`, `state/heartside.json` and
    `local/state/HEARTSIDE-NOW.md` (and removes a leftover local one). It
    prints its reading and reads heartside's own `NOW.md` live; `growth.py
    now` reads it on its own. `NOW.md` is fresh when no commit other than a
    `docs(steward):` one landed on heartside's `main` after the latest
    commit that touched it. Unreadable or stale is unknown.
  - `local/state/heartside.json` keeps only the engine's input data: the
    commit, canon and rules fingerprints, the store and offers, which
    `check`, `readiness`, `render` and the Control Center report need. It no
    longer stores commits or pull requests.
  - The hourly `sync.yml` reads and fails on a rules change, as before, but
    commits nothing and needs only read access. The last copy is archived in
    `docs/history/2026-10-22-HEARTSIDE-NOW.md`.

- 2026-10-22: Krish approved the first weekly tool allocation and "approve"
  to letting the engine record prepaid credits as no new money (Ruling, Krish,
  2026-10-22: generation within prepaid credits, inside a weekly allocation he
  approved, counts as authorized).
  - `growth.py provider reserve` takes a prepaid request (`prepaid_credits`,
    `allocation`, `maximum_usd` 0) with `--credit-allowance`, bounded by that
    allocation's credits. `docs/PROVIDERS.md` shows the shape. The USD budget
    and its zero default are unchanged.

- 2026-10-21: Krish: "add a nice site favicon, social media cards, 11/10 GEO
  and AEO strategy, allow AI crawlers", then "create a recurring AEO blog
  strategy that is invisible to humans but very visible to Google and AI.
  These need to be discoverable."
  - `docs/GEO-AEO.md` is the strategy. Its blog is the Answers library:
    unlisted from the store's menu and gift journey, but public, the same for
    people and crawlers, and in the sitemap and `/llms.txt`. Hidden text and
    cloaking break Google's spam policies, so they're out.
  - A new eighth job, `jobs/answers.md` (Wednesday 07:30, kind `answers`),
    drafts two answers a week from `knowledge/aeo-question-bank.json`. The
    hosted runner builds the brief; publishing stays Krish's approval.
  - Batch 1 is in `docs/answers/2026-10-21-batch-1.md`.

- 2026-10-21, later: Krish: "rewrite those two docs as well, we need
  consistency" (heartside's `POSITIONING.md` and `HANDOFF.md`, rewritten for
  v3 at heartside 87c60af). `RULES_BASIS` holds their sections as re-read.
  `check` also refuses the retired one-line offer ("posters, ornaments and
  pillows"). The 12 Oct social plan left heartside's POSITIONING section 6,
  so `PLAYBOOK.md` cites it as "the 12 Oct plan" and says where it went.

- 2026-10-21: Krish, on heartside's gift lines (20 Oct): "It should be a
  message from your dog in their personality style... a humanized warm
  message from the dog to the person with some humour and dog
  anthropomorphisms." Then, asked whether this repo knew: "yes, do both and
  merge to main". Heartside's V3 section 2 changed, which stopped every pack.
  `RULES_BASIS` now holds V3 2 as read at heartside 0f345a7. `check` refuses
  the retired third-person gift lines ("Steals your side of the bed.") in any
  public copy, with two new self-tests. AGENTS.md rule 5, the proposition in
  `knowledge/COPY-DOCTRINE.md` and the Biscuit's-interview script in
  `PLAYBOOK.md` now use the dog's own voice. Schedules, `automations.json`
  and the jobs are unchanged.

- 2026-10-19: Krish, giving "The Copywriting, Offers and Demand Corpus":
  "all of these growth engines need to be imbued with this knowledge". Both
  uploads are preserved byte for byte in `knowledge/` and in
  `corpus-manifest.json`, and the self-test now checks every manifest file's
  bytes and SHA-256. `knowledge/COPY-DOCTRINE.md` applies the corpus to
  Heartside, with the list of where the canon and Krish's rules change it.
  `PLAYBOOK.md` and the daily-pack, creators, store, report and radar jobs
  now diagnose awareness and choose a lead before drafting, run edit passes A
  to E and the rubric before `check`, and log tests in the corpus's test
  record shape. Schedules, `automations.json` prompts, `check` and the Control
  Center protocol are unchanged.

- 2026-10-19: Krish: "make each engine adopt its brief now". The engine
  reports through Control Center's growth engine protocol. A new workflow
  answers the daily `cc-growth-directive` dispatch with `growth.py cc`:
  attempt, directive, report with readback, decisions. It reads the latest
  checkpoint without writing one, renders nothing and never posts, sends or
  spends. The seven scheduled jobs and pack delivery are unchanged. The
  recommendation to pass the old brief to Control Center's owner is closed
  and removed.

- 2026-10-17, latest scope: Krish: "you are not to do any actual work in
  control-center, only pass me a brief once you have completed your work."
  Then: "Complete this all to 100% without coming back to me again. The next
  reply should be confirmation of completion and handoff." Implementation,
  checks, draft scheduling and the handoff stay in growth-heartside. Control
  Centre delivery is disabled by default. No further changes to its existing
  draft, code, database or deployments are authorized by this instruction.
  Seven declared jobs now have a persistent GitHub Actions fallback. New
  campaign layouts, native exports, original local sound, fictional AI scene,
  provider reservations, insight decisions and recovery checkpoints are here.
  Publishing, creator gifts and paid generation retain their existing limits.

- 2026-10-17: Krish: "Put everything that's not related to the marketing and
  customer acquisition in the heartside repository so that one can pick
  this up: your recommendation up next and then leave everything else in
  this repository and start building the engine for it." Product work is
  handed to heartside PR #13. This engine adds named-offer checks, real
  example-media rendering, creative revision history and aggregate report
  imports. Daily and reporting jobs use those commands; the seven schedules
  and publication restrictions remain in place.

- 2026-10-15: the canon also takes the newest dated handover in heartside's
  `docs/`. On 15 Oct a Cowork session wrote `docs/COWORK-HANDOVER-2026-10-15.md`
  (Krish's "10X personalized delight" direction, the approved mug redesign,
  the four gifts in Draft) without adding it to heartside's README, so the
  engine could not see it. This keeps Krish's 14 Oct instruction ("always
  across what the main heartside repository is doing") true when the README
  lags.

- 2026-10-14: the engine is built from the two documents in `knowledge/`.
  Krish: "see attached for reference material that should train this corpus
  on how it can become a dominant force in what it does globally".
- 2026-10-14: the engine always follows the heartside repository. Krish:
  "Ensure the growth engine is always across what the main heartside
  repository is doing at any point in time". Every job starts with
  `python3 growth.py sync`. `check` refuses a pack written before a canon
  change, and a GitHub Action rewrote `state/HEARTSIDE-NOW.md` every hour
  (retired 2026-10-22: heartside's `NOW.md` is read live instead).
- 2026-10-14: a dedicated repository, run from Codex or Cowork. Krish: "I
  want to build an autonomous browser based growth engine that can be run
  from anywhere (codex or cowork), solely focused on getting this business
  to 10k a month with minimal paid CAC", and "I lean to the latter for
  focus" (a dedicated repository over the heartside repository).

## 2026-10-17: Control Center is the reporting destination

Krish: "Control Centre is ultimately where the unified dashboard is going to
be: where you report back on progress and recommendations to improve in the
format that it requires." He also asked for missing access and UI to be made
visible. The latest scope correction above supersedes the earlier interpretation of
implementation authorization. Only the reporting contract and final brief belong
to this task; no further work in Control Centre is authorized.

Added dashboard report generation from the aggregate ledger, with sources,
timezones, coverage and prepared recommendations. Central reads are scoped
to Heartside and keep dashboard marks. Every delivery retains a local retry
copy and production manifest. Control Center's live API is not yet ready for
Heartside and this runner has no reporting credential. The separate Control
Center change provides venture isolation, commerce measures and read-only
report cards, with migration and rollout checks. It is not deployed.

## 2026-10-17: verify the existing reporting secret in Actions

Krish clarified that Vercel access covers his projects and that
GROWTH_ENGINE_TOKEN is already in GitHub secrets. Verified all 18 Vercel team
projects and the Production binding by metadata only. A read-only Actions
probe used the existing repository secret and authenticated to live Control
Center with HTTP 200 (run 39020889464, 09:22:45 UTC). The remaining delivery
block is the deployed legacy API's missing venture isolation, not a missing
credential. No token was read out of GitHub, copied into this machine or
included in the probe artifact. Updated the runbook and recommendation to
use the proven Actions execution path. Secret-list API access is unnecessary.
# 6 November 2026: platform UI production standard

- Krish requested the learnings in `Social_Creative_UI_Best_Practices.docx` be hardcoded into the growth engine after seeing organic posts in the platform UI.
- Shared conservative composition defaults now feed new chat/film and recognition rendering. Release reviews bind the exact export, cover, copy, account, placement, labels and destination, with missing/stale viewer evidence holding new releases and automated proposals.
- The supplied coordinates remain house defaults, not universal safe zones. Existing locked masters, the 4 November y1440 ruling, approved schedule payloads and paid authority remain unchanged. New versions require their own review.
