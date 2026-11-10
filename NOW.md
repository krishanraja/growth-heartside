---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-10
head: 10e1c3e
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

## Where it is right now (as of 2026-11-10)

<!-- north-star-state {"week_of": "2026-10-26", "week_target": 200, "current": 0, "current_as_of": "2026-10-29", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 4, "urgency_reason": "at 0% of this week's target"} --> **North Star number: U4, far behind.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 29 Oct; the store's only order in the window was fully refunded), against $200 this week, on the way to $25,000 by 28 December 2026. A bold swing every day; work that does not move the number waits.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own product renders with an Example label; none uses Biscuit. Heartside's whole-store number is $24 over the trailing 28 days (heartside `NOW.md`, read 29 Oct); the organic share is still not measured.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`), and its scheduled workflows ran green on 22 Oct: the draft engine, the hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` (GitHub Actions readback, 22 Oct).

Live:

- the fixed-label F38 and F41 v2 cuts sit in Posts/F38 and Posts/F41, the old cuts are renamed SUPERSEDED_, and Sheet 04 and Doc 04a are rebuilt with the v2 links (new IDs in docs/DRIVE-MAP.md). (2026-11-10)
- Krish approved D as the official Heartside icon. The unchanged raster master, favicon/app exports and ZIP are ready in docs/brand/. Official avatars and conversion bios are live and read back on Instagram, Facebook, TikTok and Pinterest; Facebook cover is replaced. Website implementation is Krish's. (2026-11-10)
- F38 and F41 are rebuilt with every label in F38's "4:00 AM · rise" spot and filed to Drive as _v2; floor rule fixed-label-position applies to every reel. (2026-11-10)
- Photo batch and F28 replacement: three rounds of script judging stalled at 8 (P9, P10 and P12 dropped at 7). P2 was made (0.5 Higgsfield); its script scored 9 but the photo was judged 7. Seven scripts, the F28 diva-beagle clip and the P2 photo are on Krish's board as yes/no. Heartside's Higgsfield share has about 15.6 left; Runway is at 5. (2026-11-10)
- Instagram and Facebook song reels (24 posts) are Krish's to post from his phone, because Meta's music catalogue is only in the apps. README v5.2 sends Codex to TikTok Studio for TikTok songs, and to Meta Business Suite only for NO SONG rows. Drive Sheet "04 Phone posts" lists each phone post with links, caption, song settings and steps. Nothing is approved in 02r yet, so Codex has scheduled nothing. (2026-11-10)
- Krish ruled the dogs must look real ("way too perfect and not real", floor real-scruffy-dogs) and the AI label stays off. He asked for F30, F38, F39, F41 and F45 to be remade, and later said "JUST DO IT NOW", so Runway was spent past the Control Center share. In all: Higgsfield 11.5 (settled) and Runway 675 (225 settled in Control Center, 450 spent directly on his word). The Runway account is at 5 and the Control Center share needs reconciling. F38 (judged 8 four times, level with the original) and F41 (8) are on the board as his call. F39 is held at 7 and needs new clips. F45 has stills but no motion (no credits). The F30 decision is on the board. F38 is held in 02q. (2026-11-10)
- All Sprint posts are ready for Codex in one Sheet, 02r (57 rows, 19 posts, read back 928 of 928 cells). README v5.1 gives every song post's track, start, volume, sync and length, the in-platform steps and a sync check, and rules out Buffer for song rows and the AI label. The real-dog F38 and F41 and the F30-pepper slide are filed through the library lane. F30-pepper was judged 8 (three takes); F39 and F45 are held until real-dog remakes reach 9. 02q and README v4 are marked superseded. The Google Sheets and Docs connectors refused this session, so the Sheet and README went through Drive. (2026-11-10)
- Wave 3 (F46 to F50, five dog-does-dog-things reels) is the first card through the Codex lane. Its 34 stills and 12 Runway clips are made and checked (Higgsfield 8.5 and Runway 300 credits, settled), and Codex is assembling the reels from codex/queue/dog-things-wave-3.md. 02q holds every filed Sprint post, ready for Codex once Krish types approved = yes. (2026-11-10)
- Volume build stopped at the budget floor after fifteen batches: seven posts filed for Krish's yes through the library lane and on his review board, approved blank: F30 pumpkin pie (02g, 21 Nov), F31 gingerbread corgi (02h, 12 Dec), F32 flour ghost lab (02i, 28 Nov), F33 snowman lab (02j, 19 Dec), F35 package frenchie and F36 pillowcase collie (02l, 2 Dec and 30 Nov), F37 toilet-roll dachshund (02m, 24 Nov). Batches 9 to 15 filed nothing: the stills plateaued at 8 and the one clip scored 6, with reasons in docs/briefs/2026-11-10-volume-build-batch-9-15-record.md. The engine's Higgsfield share is at 124.85 of 2,400 for the cycle, under the brief's 230 reserve; this session spent 175.00, all settled. Then, on Krish's yes, three F34 chat variants (golden, dachshund, doodle) were built from existing photos at F34's fingerprint, scored 8 to 9; Krish approved them ("i approve them all"), and they are filed as F34-golden, F34-dachshund and F34-doodle with 02n, approved blank (docs/briefs/2026-11-10-F34-chat-variants-record.md). Nothing published; Krish's hold stands. (2026-11-10)
- Sprint 120 is approved and publishing has started. F28 (the dog 80s dance on Bronski Beat's Smalltown Boy) is in 03b Posts/F28, scheduled in 02e for 12 Nov on all three platforms, waiting only for Krish's approved = yes. The live README for Codex (1tKnG8ex3Us2W6wCWXB_-yQh0Wf24oQR8Hkvk_4UIS64) has Codex add each song in the browser in TikTok Studio and Meta Business Suite. The judging panel (factory/panel.py) and the lane fix (content-engine#497) are in place. A safety check refused letting the engine mark approvals itself, so that stays with Krish. (2026-11-10)
- Eight dog-does-dog-things reels are approved by Krish and filed: F38 to F45 through the library lane, with 24 rows in 02p (approved blank for Krish; 02o superseded). First slots: F38 12 Nov, F39 13 Nov, F40 16 Nov, F43 17 Nov, F41 21 Nov (signature, mug link), F44 22 Nov, F45 23 Nov, F42 27 Nov. Higgsfield 8.85 left until 24 Nov; Runway 980 left. The human-arms lip-syncs (S12, HAL-02 to HAL-07) are retired in favor of this format. (2026-11-10)
- Krish's review board is live (docs/REVIEW-BOARD.md), with seven items waiting: F34, F28 and F29 approvals, the publishing hold, the F34 order-by line, the stray F33 files and the first paid tranche. (2026-11-10)
- F34, the face-blanket roast, is filed in 03b Posts/F34 and 02k for 13 Nov (approved left for Krish), and locked as the structure for every dog group chat post; nothing is published. (2026-11-10)
- Krish's humour profile (docs/HUMOUR.md) is the anchor for every build: AGENTS.md, the briefs and the tier 2 judge all carry it, and a piece missing its observation, stupid premise or cruel payoff cannot score 9. (2026-11-10)
- Claude sessions here show Krish a ChatGPT sign-in link and code whenever Codex is signed out (.claude/hooks/codex-login.sh at session start, cloud included); his subscription, never an API key (Krish, 2026-11-10). (2026-11-10)
- The engine restores the social desks' history and Krish's rejections from the repository alone: `growth.py social status` (the two first-follower engagement tests, approved 7 Nov, publication not yet verified; Instagram and Pinterest followers watched, 0 at 8 Nov 17:37 UTC, unknown since) and `growth.py floor` (20 rejections in his words, each with rule and check). `growth.py drive audit` reports 0 errors and 65 warnings on 9 Nov. Codex runs only by card, checked by Claude (`codex/INDEX.md`). (2026-11-09)
- Drive: creatives iterate in `03a_Social-Production`, release media and schedules live in `03b_Social-Schedule` (was `05_Social-Library`, same ID); map in `docs/DRIVE-MAP.md`. Codex posts only rows Krish marks `approved = yes`. (2026-11-09)
- Gaps found on 9 Nov, for Krish: no schedule row has `approved = yes` yet all 38 rows were posted on chat approvals; F17 to F24 are live with no schedule row; the publishing desk left four duplicates and three TikTok pairs in Buffer ERROR. Decided the same day ("Go with your recommendations"): only `approved = yes` lets Codex post; `ui-v1`/`ui-v2` editions are retired. PR #42 is merged.
- Organic comedy batch of 7 to 8 Nov: OG-01/02/04 approved on 7 Nov and produced as F25 to F27 (eight files, hashes read back from Drive). OG-03 Cheese and OG-05 stick were revised and, with the anatomy correction of 8 Nov, remain unapproved and unpublished; the revised five-post batch awaits his decision (`docs/briefs/2026-11-07-five-organic-ready.md`, `docs/briefs/2026-11-08-organic-anatomy-correction.md`).
- Krish approved the corrected creative board on 6 Nov ("ok, all looks good"); 33 organic placements were restored and verified, 11 per platform, 6 to 8 Nov. The social UI standard now gates new releases (`docs/CREATIVE-UI.md`); native-device evidence is unverified. The USD 25 F10 paid pilot was published 7 Nov 12:45 GMT; delivery was Processing with USD 0 spent at the last readback (`docs/boost/2026-11-05-sandbox.md`).
- All twelve organic posts (F01 to F07, F10 to F12) are locked by Krish and pass `lock.py gate`; motion versions are filed to Drive. 18 Runway clips are checked: 15 pass, 3 held (`docs/history/2026-11-04-runway-motion-verdicts.md`). Boosts are of live organic posts only; the $250 launch packet waits on his yes (`docs/PAID-BOOSTS.md`).
- The lock system (joke bank, render catalog, fingerprinted locks, copy, breed, media and drift gates, independent reviewer, 5-then-1-in-10 trust ramp) builds every post from a spec; five channel guides in `docs/CHANNEL-TASKS.md` keep shareable and shop-visit posts in one schedule.
- Eight scheduled jobs in `automations.json` run on GitHub Actions (`.github/workflows/engine.yml`); Control Center protocol 1.16.0; paid external generation stays off with a zero default budget (`docs/CREDITS-SESSION.md`, `docs/PROVIDERS.md`).

Waiting or not measured:

- The last live report in the repo (19 Oct) was held: `net_sales_usd` was stale because imported Shopify reports stop at 16 Oct, `organic_orders` is not measured, and conversion editions waited for the V3 homepage (`docs/GET-GOING.md`, "This engine"). Heartside's chat homepage went public on 19 Oct (heartside `9ea7e34`); whether the hold has released is not recorded here.

## What changed recently

- 2026-11-10 the library lane filed the v2 cuts into new F38-real and F41-real folders because the manifest named the post F38-real; the manifest post must match the existing Posts folder.
- 2026-11-10 AGENTS points to the official assets. Profile review history, exact approval, asset hashes, live readbacks and link-feature limits are recorded in docs/profile-pages/2026-11-10/ROLLOUT.md. Facebook Learn more retains the verified tracked destination; Buy now would require a new store integration.
- 2026-11-10 Krish found F38 labels under Instagram's caption area, so labels now sit in one fixed, visible place.
- 2026-11-10 the judge loop stopped converging, so Krish's board decides the scripts at 8 rather than more rounds.
- 2026-11-10 v5.1 wrongly sent Instagram and Facebook songs to Meta Business Suite; Krish ruled "I add songs on my phone".
- 2026-11-10 dog reels now need real-looking scruffy pets and motion in every beat. Credit spend needs a 9 on the script first. Krish overrode the Runway share cap for these remakes.
- 2026-11-10 02r replaces 02q; F30 becomes F30-pepper (Krish's board Yes); F38 and F41 post as the real-dog remakes.
- 2026-11-10 the denial-and-evidence meme cleared the bar seven times and then plateaued at 8; an unedited-phone-photo prompt fixes the AI look; motion on a single gag fails the video bar; Krish's humour profile (docs/HUMOUR.md) now anchors every build, and the denial meme lacks its "utterly stupid premise".
- 2026-11-10 Krish asked for 120 posts at a $50,000 profit target, with songs added in the platform by Codex in the browser.
- 2026-11-10 every session now adds ready work to the board as a Yes or No item, and reads Krish's answers from it instead of asking in chat.
- 2026-11-10 Krish scored the P04 sample 9 and locked it; his chat rules are on the floor (lads banter, no novelty sound, WhatsApp build, mates' typing), and F34 is now the tier 2 anchor for chat posts.
- 2026-11-10 the judge brief now scores humour fit against the profile, with tests.
- 2026-11-09 This protects approved work and the creative bar; it adds no sales by itself, and the number is still $0 (U4).
- 2026-11-09 This keeps the post pipeline from stalling; it moves no sales number by itself.
- 2026-11-07 Stronger visual executions for date night, rain and friendship; larger TikTok photographs after checking the initial layouts. Exact packet: docs/briefs/2026-11-07-five-organic-ready.md and its JSON review receipt. Local board: http://127.0.0.1:8769/five-revised.html. Fifteen copy checks and fourteen image decode/dimension checks pass; all fourteen browser images load. Native and physical-device QA remain unverified.
- 2026-11-07 Approval and immutable mock hashes are recorded; feed compositions preserved, TikTok layouts split where the reveal benefits. OG-03/05 remain unapproved. All 152 self-tests and nine copy checks pass.
- 2026-11-06 The supplied document is now enforced in shared layout, source-repair, photo-card and release-evidence paths. Earlier locks and the 4 November caption ruling remain intact. Current selected index: library/editions/2026-11-06-ui.json. Audit: docs/audits/2026-11-06-unpublished-correction.md.
- 2026-11-06 factory/review_board.py serves only manifest-selected files and generated posters on loopback, supports video byte ranges, and gives each concept a readable name, full-size media links and platform captions. The old local review.html now points to the working board. The private closeout generator uses this renderer so it cannot recreate the broken remote grid.
- 2026-11-06 Clean exports and paid mocks had not proved organic readability. New releases require normal/stress/crop/playback evidence tied to exact media and metadata. Sync on 6 Nov found changed DOG_VOICE rules in heartside at 602813d605; production STOP remains intact. The live store returned 429, so current sales/product availability were not remeasured here.
- 2026-11-03 Codex orchestrates and schedules posting from the Drive library (Krish, 3 Nov). AGENTS.md records it.
- 2026-11-02 Krish ruled that F04, F05 and F12 are recast to breeds with approved product renders (Ruling, Krish, 2026-11-02).
- 2026-11-02 product images carry no badge, and posts are organic with no on-screen call to action (Krish, 2 Nov). AGENTS.md rule 4 is updated.

## What is next and what is waiting on Krish

- Next (2026-11-10): Krish decides whether to repost F38 and whether to trash the two empty stray folders.
- **Waiting on Krish:** set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Steps 2 and 3 of `docs/GET-GOING.md` may need a credential only Krish can add for a daily Shopify import; the step says to report a hold naming the secret.
- North Star check (2026-11-10): holds.

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
