---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-07
head: 836ad8a
lifecycle: live
production_url: none
state_doc: docs/HANDOFF.md
history_log: docs/history/LOG.md
truth_files: []
authority_order: [Heartside's canon at the synced commit (krishanraja/heartside read through python3 growth.py sync), AGENTS.md, PLAYBOOK.md, docs/ENGINE.md, BROWSER.md, docs/GET-GOING.md, docs/HANDOFF.md, knowledge/README.md]
steward: https://github.com/krishanraja/ai-harness/blob/main/docs/steward/RUNBOOK.md
never_publish: [any credential or the name of any secret, the Control Center engine token, any customer's name or email or address or dog or photo or typed answer, any named creator or the creator shortlist, Krish's personal email address, provider credit balances]
---
# Heartside growth engine: where it is right now

## What it is

The Heartside growth engine drafts the organic marketing that is meant to take Heartside, gifts from your dog, to $10,000 of Shopify net sales in a calendar month with low paid acquisition cost (`README.md`). A Python engine (`growth.py`, `engine/`) on GitHub Actions reads the heartside repository and the live store before every job, renders native Reels, TikToks, Stories, carousels and Pins with captions and subtitles, packages them as reviewable packs, keeps a creative and evidence history, and reports to Control Center through the growth engine protocol (`README.md`; `docs/ENGINE.md`). It never posts, sends, follows, orders, changes the store or spends on its own; the one exception is a go-live Krish approved on his list in Control Center, taken live exactly as approved (`AGENTS.md`, "Autonomy" and rule 1).

## Who it is for and why it matters for Mindmake

It is an internal engine, not sold. Its customer is Heartside: the US dog owner buying a gift that sounds like their dog (heartside's `docs/NORTH_STAR.md`). Its North Star is that by 31 December 2026 organic posts sell more Heartside gifts than paid ads ever have, with every winning format found by the engine and approved by Krish in one press (`docs/NORTH_STAR.md`).

What it proves for Mindmake: an AI engine can run a store's acquisition with a person holding every wall. Angles a writer can use:

- **Autonomy is given where it is deserved.** Krish's ruling of 19 Oct: the engine shows its plan, he approves, it builds up to go-live and asks him to review; repeated declines or poor work are how it loses autonomy (`AGENTS.md`, "Autonomy"; `8ba5523`).
- **Facts only from four places.** The live store, heartside's canon at the synced commit, a platform page read today, or the thread being answered; a missing number is "not shown", never a guess (`AGENTS.md`, rules 3 and 8).
- **It stops itself when the product changes.** When heartside ruled on 20 Oct that gift lines are the dog talking, every pack stopped until the engine took the ruling in (`ca52b75`).
- **Idle credits are not a reason to generate** (`docs/briefs/2026-10-22-media-credits.md`, "Counterpoint to carry").

Objection it answers: "An AI marketing engine will spam and invent." Here it drafts, checks every pack against the store and the canon, and cannot publish without a press bound to the exact payload (`docs/CONTROL-CENTER-BRIEF.md`).

## Where it is right now (as of 2026-11-07)

<!-- north-star-state {"week_of": "2026-10-26", "week_target": 200, "current": 0, "current_as_of": "2026-10-29", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 4, "urgency_reason": "at 0% of this week's target"} --> **North Star number: U4, far behind.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 29 Oct; the store's only order in the window was fully refunded), against $200 this week, on the way to $25,000 by 28 December 2026. A bold swing every day; work that does not move the number waits.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own product renders with an Example label; none uses Biscuit. Heartside's whole-store number is $24 over the trailing 28 days (heartside `NOW.md`, read 29 Oct); the organic share is still not measured.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`), and its scheduled workflows ran green on 22 Oct: the draft engine, the hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` (GitHub Actions readback, 22 Oct).

Live:

- All five organic comedy concepts prepared as 14 local image exports covering 15 platform placements, with captions, revised alt text, hashes and a browser-verified review board. Cheese now sleeps with a snoring cue; the liked stick r3 source is unchanged. F25–F27's earlier hold is preserved pending the revised batch decision. No new exports uploaded or queued. (2026-11-07)
- Krish approved OG-01/02/04 on 7 November; produced F25/F26/F27 as eight checked files for nine organic placements. Uploaded all eight through the established library lane and independently downloaded matching bytes and SHA-256. Production board loads all files. Drive filing and native placement checks remain with Scheduling; no queue or live-post receipt claimed. (2026-11-07)
- Recovered clean sources and approved motion, produced 38 selected UI-edition files, and handed off 33 exact unpublished draft replacements. Library API and CDN bytes match local hashes; Drive names, sizes and parents were read back. Preview-driven typography, contrast, cover metadata and AI-disclosure corrections are recorded in the correction audit. All postings remain held for native release review; no published edits or paid spend. (2026-11-06)
- Replaced the broken remote-media file preview with a local review board at http://127.0.0.1:8767/. All22 images loaded in the browser; all8 reels reached playable readiness and were started through visible Play buttons. Responsive390px and desktop views have no horizontal overflow. Exact38 selected delivery files retain their hashes. Social drafts and approval states were not changed. (2026-11-06)
- Implemented the supplied social UI standard in shared composition defaults, factory chat/film helpers, recognition rendering, exact-payload placement review, factory release gating and automated post-proposal gating. Existing locked specifications, media hashes and scheduled posts are unchanged. Native viewer and physical-device acceptance of new creatives is not yet performed. (2026-11-06)
- Five original organic concept mocks and exact Instagram/Facebook captions prepared locally for one consolidated review; all five images load on the review board. Paid monitoring and scheduling ownership handed to the existing threads. None of this new batch is approved, scheduled or published. Reviewed an example-only DOG_VOICE change and refreshed its fingerprint; all 152 self-tests pass with explicit UTF-8, plus ten copy checks and five media checks. Native previews remain unverified. (2026-11-06)
- Krish approved the corrected creative board with "ok, all looks good". All 33 organic placements restored and independently verified: 11 per platform, 6-8 November, exact approved text, ordered media, titles, covers, alt text, AI disclosures and metadata. The 37 superseded drafts remain unchanged and excluded. Native-device evidence remains unverified. The separate USD 25 F10 paid pilot is published after billing and phone verification. Fresh Meta readback at 12:56 GMT shows Processing, enabled, USD 25 lifetime and USD 0 spent. Published end: 7 November 12:45 GMT. Publication is verified; paid delivery is not yet verified. Exact evidence: `docs/boost/2026-11-05-sandbox.md`. (2026-11-06)
- F17–F24 are locked for organic release and verified in the Heartside library. Buffer readback confirmed four Instagram and four Facebook posts scheduled through Saturday, 7 November. (2026-11-05)
- 18 Runway motion clips are made for the locked posts F01 to F07, all checked against their Higgsfield key frames: 15 pass, 8 of them only within a cut window, and 3 are held. The 2 made on 4 Nov on Krish's yes left 18 Runway credits; verdicts and task ids are in docs/history/2026-11-04-runway-motion-verdicts.md. (2026-11-04)
- Every post Krish locked on 4 Nov is filed to Drive and is what the Buffer queue will publish: F03, F04, F05, F06-dachshund, F06-lab, F07 and F12 were swapped onto permanent links and read back, and F02, F06-frenchie and F11 already carried their locked files. The old F10 cut's 8 Nov posts are drafts. F11's new cut waits for his lock. (2026-11-04)
- Organic queueing was authorized and delegated to the scheduling chat. The four-post paid plan is ready for review. (2026-11-04)
- All 12 locked reels are audited frame by frame. Krish locked motion versions of F01, F02, F03, F05, F06 x3, F07 and F12, plus new F07, F10 and F11 covers; they are filed to Drive with their sha256 read back, and F04's motion is held on his note. Boosts are boosts of the live organic posts (Ads Manager, existing post): a $250 test on F12, F05, F02 and the F06-frenchie carousel, with the launch packet ready. (2026-11-04)
- All 40 current social assets matched in Drive and the library API. Nine approved review copies are in Trash. The scheduling chat has the verified full index. (2026-11-04)
- The production handoff identifies the three motion candidates (F04, F05, F12), their unchanged Drive originals and the separate F12 paid opening pair by SHA-256. The candidates await exact-file creative decisions. Paid activation is held. (2026-11-04)
- All twelve organic posts (F01 to F07, F10 to F12, with F06 in three breeds) are locked by Krish and pass `lock.py gate`; the lock page shows them locked (2026-11-03).
- The social library is in Krish's Drive (`Heartside/05_Social-Library`, map in `docs/DRIVE-MAP.md`): one Codex README, the posting strategy, the schedule Sheet with captions, tracked links and lock fingerprints, and each post's media in `Posts/<post id>/`. Krish's home computer files the media (`factory/send_library.py`, 39 files read back byte for byte); the zip is a backup. Codex posts only rows Krish marks `approved = yes` (2026-11-03).
- Sound is locked for all ten approved concepts and the lock system (joke bank, render catalog, fingerprinted locks, copy, breed, media and drift gates, independent reviewer, 5-then-1-in-10 trust ramp) builds every post from a spec (2026-11-02).
- Five channel guides separate posts made to be shared from posts made to earn shop visits; dog POV and product posts stay in one schedule (`docs/CHANNEL-TASKS.md`, 2026-11-03).
- Eight scheduled jobs in `automations.json` run on GitHub Actions (`.github/workflows/engine.yml`); the Control Center loop runs on protocol 1.16.0, with prepaid credits spent by a daily session (`docs/CREDITS-SESSION.md`, `docs/control-center/`). Paid external generation stays off with a zero default budget; generation inside Krish's prepaid-credit allocation counts as authorised (`0303ffb`; `docs/PROVIDERS.md`).

Waiting or not measured:

- The last live report in the repo (19 Oct) was held: `net_sales_usd` was stale because imported Shopify reports stop at 16 Oct, `organic_orders` is not measured, and conversion editions waited for the V3 homepage (`docs/GET-GOING.md`, "This engine"). Heartside's chat homepage went public on 19 Oct (heartside `9ea7e34`); whether the hold has released is not recorded here.

## What changed recently

- 2026-11-07 Stronger visual executions for date night, rain and friendship; larger TikTok photographs after checking the initial layouts. Exact packet: docs/briefs/2026-11-07-five-organic-ready.md and its JSON review receipt. Local board: http://127.0.0.1:8769/five-revised.html. Fifteen copy checks and fourteen image decode/dimension checks pass; all fourteen browser images load. Native and physical-device QA remain unverified.
- 2026-11-07 Approval and immutable mock hashes are recorded; feed compositions preserved, TikTok layouts split where the reveal benefits. OG-03/05 remain unapproved. All 152 self-tests and nine copy checks pass.
- 2026-11-06 The supplied document is now enforced in shared layout, source-repair, photo-card and release-evidence paths. Earlier locks and the 4 November caption ruling remain intact. Current selected index: library/editions/2026-11-06-ui.json. Audit: docs/audits/2026-11-06-unpublished-correction.md.
- 2026-11-06 factory/review_board.py serves only manifest-selected files and generated posters on loopback, supports video byte ranges, and gives each concept a readable name, full-size media links and platform captions. The old local review.html now points to the working board. The private closeout generator uses this renderer so it cannot recreate the broken remote grid.
- 2026-11-06 Clean exports and paid mocks had not proved organic readability. New releases require normal/stress/crop/playback evidence tied to exact media and metadata. Sync on 6 Nov found changed DOG_VOICE rules in heartside at 602813d605; production STOP remains intact. The live store returned 429, so current sales/product availability were not remeasured here.
- 2026-11-06 This session concentrates on creative production and verified inspiration. The later 6 November routing clarification supersedes the initial handoff: Scheduling owns paid monitoring and owned-post reporting; Audience Growth owns new-follower acquisition and comment-test outcomes.
- 2026-11-04 the passing clips are on a Codex card, docs/briefs/codex/2026-11-04-motion-cut-F01-F07.md, so the locked posts can open on motion instead of a still.
- 2026-11-04 factory/build.py and factory/splice.py; factory/bank/lines.json; factory/locks F03, F04, F06-dachshund, F06-lab, F07; factory/specs; factory/motion/F03-labels.json; library/manifest.json; docs/plans/2026-11-04-road-to-ten.md; docs/briefs/codex/2026-11-04-road-to-ten-builds.md; CHANGES.md.
- 2026-11-04 Aligned the boost packet to the approved organic slots; verified the four product URLs and proposed a $200 first test with one approval.
- 2026-11-04 docs/PAID-BOOSTS.md (organic boosts, gates, the test); docs/boost/2026-11-launch-packet.md; docs/PUBLISHING.md; docs/BOOST-LIBRARY.md and library/manifest.json; factory/audit.py, factory/splice.py and factory/motion/ (motion splices). factory/send_library.py now reads the Windows credential. The live Buffer queue is not edited.
- 2026-11-04 Released F10, F11, and the corrected Frenchie reel and slide 3. Closed job C and indexed the final library.
- 2026-11-03 all twelve posts locked on Krish's word ("Lock F01, F02 and F04, keep the dachshund"), after a final independent review and its fixes; Drive carries one live Codex README and every older README and 02b are marked superseded (`f41ac27`, `172be13`).
- 2026-11-03 Heartside media reaches Drive through content-engine's library lane (content-engine PR #356) instead of a hand-run step, because the existing home-computer lane wrote only into makeyourmindup's library (`873a749`).
- 2026-11-03 roasts take the dachshund's blunt, cheeky humour, and slides are troll-meme dog photos, not plain cards (Krish, 3 Nov).
- 2026-11-03 Codex orchestrates and schedules posting from the Drive library (Krish, 3 Nov). AGENTS.md records it.
- 2026-11-03 the gate matches reviewer and Krish verdicts to the exact post by spec and fingerprint.
- 2026-11-02 Krish ruled that F04, F05 and F12 are recast to breeds with approved product renders (Ruling, Krish, 2026-11-02).
- 2026-11-02 Krish ruled that F01's swear is bleeped, the dog's inner voice is one voice per breed group, sound-alikes are original voices and licensed genre tracks, and Higgsfield work runs without asking each time (Rulings, Krish, 2026-11-02).
- 2026-11-02 the sound bible now says endings dip and fade rather than cut dead (Krish, 2 Nov).
- 2026-11-02 Krish's round-4 notes set two rules for every mix: the voice always sits on top of the music, and sound effects fade in rather than hitting abruptly.
- 2026-11-02 Krish ruled that emojis and "WTF" are allowed inside on-screen chat mocks only, never in captions, voiceover or gift lines (Ruling, Krish, 2026-11-02).
- 2026-11-02 Krish ruled that F01's wink is done by the real dog before a hard cut to the untouched mug, and that ElevenLabs runs without asking (Rulings, Krish, 2026-11-02).
- 2026-11-02 product images carry no badge, and posts are organic with no on-screen call to action (Krish, 2 Nov). AGENTS.md rule 4 is updated.

## What is next and what is waiting on Krish

- Next (2026-11-07): Obtain the consolidated revised-batch release decision, then reconcile the two new library IDs and exact final filenames with Scheduling before native upload checks and queueing.
- **Waiting on Krish:** set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Steps 2 and 3 of `docs/GET-GOING.md` may need a credential only Krish can add for a daily Shopify import; the step says to report a hold naming the secret.
- North Star check (2026-11-07): holds.

## Read next

1. Heartside's own canon, through `python3 growth.py sync` (and heartside's `NOW.md`, read live): it beats everything in this repository (`AGENTS.md`, rule 2).
2. `AGENTS.md`: the whole operating brief, Krish's rulings and the rules that never bend.
3. `PLAYBOOK.md`: the organic commerce operating system, applied to Heartside.
4. `docs/ENGINE.md`: production, reporting and the Control Center loop.
5. `BROWSER.md`: what a session may and may never do in Krish's signed-in browser.
6. `docs/GET-GOING.md`: the build, as a checklist.
7. `docs/HANDOFF.md`: what was delivered on 17 Oct and its verification.
8. `knowledge/README.md` and `knowledge/COPY-DOCTRINE.md`: the reference corpus and how it applies to copy.

## Do not trust

- `docs/CONTROL-CENTRE-BRIEF.md`: superseded on 2026-10-18 by `docs/CONTROL-CENTER-BRIEF.md`, as its own banner says.
- `docs/HANDOFF.md` where it says the public catalog does not offer the four V3 gifts, and that product work is in heartside PR #13; `README.md`, `STRATEGY.md` and `docs/ENGINE.md` also point at PR #13. Heartside's chat-led store went live on 19 Oct (heartside `docs/HANDOFF.md` section 3), and heartside's own docs, not that pull request, hold its product state.
- `README.md` and `docs/HANDOFF.md` on "seven" jobs: `automations.json` and `AGENTS.md` have eight since the Answers job of 2026-10-21 (`70fa624`).
- `docs/GET-GOING.md`, "Where things stand (2026-10-19)", on protocol 1.1.0: the repository speaks 1.2.0 since 2026-10-21 (`b1a14af`).
- `docs/briefs/2026-10-22-media-credits.md` on its creative direction: see "What is next" above.
- Anything in `docs/history/`, including `2026-10-22-HEARTSIDE-NOW.md`: the record, not current guidance.
