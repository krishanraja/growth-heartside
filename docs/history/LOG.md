# History log

Newest first. Entries are written by the docs steward (see the steward link in
NOW.md) and by humans doing the same job by hand. Nothing in this file
describes current behaviour; NOW.md and the state doc do.

## 2026-11-06

- rolled from NOW.md (Where it is right now): the seven channel tasks run inside the radar, daily pack, store and report jobs, mapped by `crew/registry.json` (2026-10-30).
- rolled from NOW.md (Where it is right now): all 24 breed examples and 6 bundle shots from heartside's painter v15 are approved, with the ledger of sha256s and prompts, mirrored in Drive (2026-10-30).
- stamped at `836ad8a`: fixed the audit's `where_too_many` finding (9 bullets, limit 8). No product commit landed since.

## 2026-11-05

- reconciled at `836ad8a`: head re-stamped. The three 2026-11-03 closeout notes were malformed again (headings and free-form lines the fold cannot place), so they were rewritten to Status, Next and North Star check lines and folded; their content was already in NOW.md, so the three duplicate bullets and the stale Next line the fold added were removed by hand.

## 2026-11-04

- reconciled at `172be13`: head re-stamped; the three closeout notes of 2026-11-03 could not be folded (malformed, left for a person) and were read into NOW.md by hand. Fixed the audit's `too_long`, `recent_too_many` and `where_too_many` findings; superseded "Where it is right now" items are condensed in NOW.md, detail in git history.
- rolled from NOW.md: 2026-11-02 posts carry line ids only, never free text; a line Krish has not approved, or one edited after he approved it, cannot reach a post (Krish, 2 Nov).
- rolled from NOW.md: 2026-11-02 the funny bar now asks for a laugh every 3 to 4 seconds, a picture that is funny muted, and four comic modes in rotation (Krish, 2 Nov).
- rolled from NOW.md: 2026-11-02 no more voting boards; Krish sees only finished posts and one status page (Krish, 2 Nov).
- rolled from NOW.md: 2026-11-02 Krish unlocked the ElevenLabs share and set connector use to always approve (2 Nov). The walls on posting, sending and new money are unchanged.
- rolled from NOW.md: 2026-11-01 Krish approved the platform, ruled that all three tones run in rotation at once ("we dont have enough time to test and learn"), and confirmed 3 Dec 11:59 pm ET as the order-by line for the $12 printed Christmas card only (Rulings, Krish, 2026-11-01).
- rolled from NOW.md: 2026-10-29 Hilarious may use theatrical staging but never invents the dog's toys, food, clothes, habits or places (Ruling, Krish, 2026-10-29).
- rolled from NOW.md: 2026-10-29 The short directed-brief prompt method is the fix proposed for heartside's painter prompt; the examples check's --only flag wrongly flags other jobs' files (fix in growth.py awaits Krish).
- rolled from NOW.md: 2026-10-29 Heartside's painter moved from the 5,500-character rulebook to the directed brief (recipes v10 to v14), driven by this engine's control test and the 24 example paintings.
- rolled from NOW.md: 2026-10-29 **Creative direction set, and Codex briefed for heartside's breed examples.** Real life, then the painting: photographic AI worlds, the real product always real, one hero allowed to morph a dog into its artwork. Five posts a day per platform once running. Codex makes stage 1 (six breeds) under a card with a strict acceptance checker (`engine/examples.py`); stage 2 waits for review and Krish's yes. Shoppable tags go to a heartside session.
- rolled from NOW.md: 2026-10-29 **Organic attribution is live: $0 from organic posts over the trailing 28 days.** The read-only Shopify app is installed; the first read found one store order in the window, fully refunded, so net sales are $0. Net sales subtract refunds and never count a fully refunded order. Buffer's own link tags count as organic social. Buffer's link shortening is off on all three Heartside channels, so the engine's tags reach the store intact.
- rolled from NOW.md: 2026-10-29 **Organic attribution is built and waiting on read-only order access.** `growth.py attribution` classifies orders as engine-tagged (post family known), organic social, organic search, paid, pending or direct, over the trailing 28 days and the last full week, and stores aggregates only; the Control Center `organic_orders` objective reads it, missing until the first live read.
- rolled from NOW.md: 2026-10-29 **The engine caught up with heartside's relaunch and is off STOP** (branch `claude/canva-integration-plan-cpy1p2`). Rules now come from heartside's current sources; `check` refuses Biscuit, every exclamation mark, the worn lines and stacked fragments. Prices come from the canon's configured baseline, cross-checked against the live store; a disagreement holds the gift. Purchase drafts may sell any live gift the film shows; Krish ruled the same day that the mug sells equally. The renderer uses the store's own renders, refuses blank templates and tiles, and labels every frame Example. The Shopify store handle left every tracked file for the `HEARTSIDE_SHOP_DOMAIN` repository variable, with a test that fails if a handle returns; it remains in git history. `docs/GEO-AEO.md` facts and prices are current, and it no longer claims free shipping to every US address.
- rolled from NOW.md: 2026-10-27 **Heartside relaunched, and this engine is on STOP until it catches up** (`docs/briefs/2026-10-27-heartside-revamp-impact.md`). Sync at heartside `bea22ce` found that the four rule sections it checks had moved into heartside's history. The renderer still uses the retired Biscuit and the old mug photos. A Heartside Canva brand kit exists but has not been updated.
- rolled from NOW.md: 2026-10-27 **The architecture plan is now v3, reviewed three times, and still proposed, not built** (`docs/briefs/2026-10-27-architecture.md`). It has 14 specialists. `learn` owns what works, `librarian` owns the Drive `Heartside/Growth` folder, and `audience` owns followers. GA comes from Control Center. Codex posts approved batches through Buffer from Krish's PC, and Claude orchestrates and checks. The failure register is filed at `docs/REGISTER.md`, and the Canva design-system Cowork prompt at `docs/briefs/2026-10-27-cowork-canva-design-system.md` (the brand-kit prompt is superseded). heartside.io has been on its password page ("Opening soon") since some time after 23 Oct; Krish says it is deliberate until heartside PR #50.

## 2026-10-31

- reconciled at `df31a80`: head re-stamped after the 24-example set, channel tasks and canon sync. Fixed the audit (`too_long`, `where_too_many`) by rolling superseded items out of "Where it is right now"; the "Next action" for Codex stage 1 is done and removed.
- rolled from NOW.md (Where it is right now, superseded by the 30 Oct approval of all 24 examples from painter v15): A worker session is upgrading heartside's painter pipeline on branch claude/painter-pipeline-v15 (blanket scattered pattern, breed-character and tone composer), to a pull request with tests and a prepared test board, generating no images and touching nothing live. The breed example launch is held until that lands. (2026-10-29)
- rolled from NOW.md (Where it is right now, superseded by the 30 Oct approval of all 24 examples from painter v15): A control test (47 generations, two photos, 3 tones, 6 styles, 4 kinds of chat answer, 3 products) showed heartside's long painter prompt reuses the customer photo's pose and face, so tone and style barely show. A short brief built from the chat's own fields, with each tone owning pose, camera and staging, fixes it; the proposal, builder and evidence are in docs/briefs/painter-prompt/. Stage 1 examples are complete and ready for review; stage 2 is on hold. (2026-10-29)
- rolled from NOW.md (Where it is right now, superseded by the 30 Oct approval of all 24 examples from painter v15): Stage 1 breed examples: the four portrait jobs (golden, lab, frenchie, doodle) are complete (painting, cutout, 3 crops, 9 mockups, contact sheet, manifest) on branch codex/heartside-examples-2026-10-29. The two blanket jobs (dachshund, shepherd) have paintings, cutouts and crops, but their home and tall-studio mockups fail the bar: the print is pasted flat across the sofa fold. The painting prompts were rewritten from heartside's 5,500-character rulebook to directed briefs of about 1,200 characters, which fixed the photo-copied face and pose (standard and prompts in review/prompts/stage1-v7/BAR.md on the review branch). (2026-10-29)
- rolled from NOW.md (Where it is right now, superseded by the 30 Oct approval of all 24 examples from painter v15): The breed example launch set is 15 approved paintings (8 mugs, 7 portraits across all six dogs and four tones), each with cutout, crops, nine product mockups and a contact sheet, in assets/heartside-examples-2026-10-29/ with the approvals ledger beside it, and the same set in Drive under 00_Brand-Assets/02_Imagery/Product-Examples. The 8 blankets and 6 bundle shots are held for heartside's painter v15 (scattered pattern) and AI fabric mockups; the shepherd Hilarious portrait is dropped. Old artwork is purged from the repository and Drive. (2026-10-29)

## 2026-10-30

- reconciled at `1525043`: credits session and protocol 1.16.0 taken in; canon sync `c570c99` and closeout folds are automation and move no head. Fixed the audit's `too_long`, `recent_too_many` and `where_too_many` findings.
- rolled from NOW.md: 2026-10-23 **An unreachable public catalog now reads as unverified, not as four missing gifts** (`398d15d`, PR #19 `e373717`; `engine/offers.py`, `tests/test_offers.py`). A local read of Heartside's `/products.json` returned HTTP 429, and the engine had no way to tell that from the gifts being gone. The scheduled runner's saved snapshot still showed all four (`74a2939`).
- rolled from NOW.md: 2026-10-23 **The North Star now has a number, a weekly ladder and an urgency rating, so every session knows how far behind it is and how hard to push.** Ruling (Krish, 2026-10-23): every repository chases one aggressive number on a weekly ladder, and urgency U1 to U5 sets its intensity. The number and ladder are in `docs/NORTH_STAR.md`; where it stands is the first line under "Where it is right now". Contract: ai-harness `contract/north-star-metric.md`.
- rolled from NOW.md: **2026-10-22: no copy of heartside's status kept here** (`90429c8`, merged in PR #15 as `89e1ec9`). A copy of another repository's status goes stale, so `growth.py sync` stops writing one and reads heartside's own `NOW.md` live; unreadable or stale reads as "unknown" and the text is withheld. The last copy is archived at `docs/history/2026-10-22-HEARTSIDE-NOW.md`. Ruling recorded in the commit.
- rolled from NOW.md: **2026-10-22: a media-credit brief for Higgsfield and Runway** (`dfcc815`): a plan for Krish's list, stills before motion, generating nothing before his yes. It runs ahead of the main build because the Christmas cut-off will not wait (`docs/GET-GOING.md`, Step 0.5).
- rolled from NOW.md: **2026-10-22: prepaid credits inside an approved allocation pass the provider budget** (`0303ffb`). Krish ruled that such generation counts as authorised; publication, ad spend, top-ups and plan changes still need their own approval.
- rolled from NOW.md: **2026-10-22: gift-line examples in the new voice** (`68940b1`). Krish: "update the Answers article". The three published Answers articles now quote real sentences in each dog's own personality, following heartside PR #44.
- rolled from NOW.md: **2026-10-21: protocol 1.2.0 copied from Control Center** (`b1a14af`). It adds "Versions": accept any 1.x back. Legibility and Mindmake required exactly 1.0.0 and stopped reporting for two days when Control Center began serving 1.1.0; this engine already accepted it.
- rolled from NOW.md: **2026-10-21: GEO and AEO strategy and an eighth job** (`70fa624`): `docs/GEO-AEO.md`, a 28-question bank and a weekly Answers job on Wednesdays, with batch 1 drafted for Krish.
- rolled from NOW.md: **2026-10-21: heartside's dog-voice ruling and rewritten positioning taken in** (`ca52b75`, `400d62b`). `check` now refuses the retired third-person gift lines and the retired one-line offer.
- rolled from NOW.md: **2026-10-19: the engine runs autonomously and reports through the one protocol** (`8ba5523`, `a87b932`), with "Get going" as the way a session picks up the plan in `docs/GET-GOING.md` (`70d9236`), and the copywriting, offers and demand corpus wired into the jobs (`c5654b4`).
- rolled from NOW.md: **2026-10-18: the North Star was set** (`bf8b536`, `c51ed5b`), and the Control Center brief replaced the earlier Control Centre handoff (`9790ed7`).
- rolled from NOW.md: **2026-10-17: the engine shipped** (`5c31853`, PR #1) with production, replay and recovery runs recorded in `docs/HANDOFF.md` and `docs/VERIFICATION-2026-10-17.json`.
- rolled from NOW.md (Where it is right now): the 23 Oct local HTTP 429 on `/products.json` (fixed by PR #19, `e373717`); the last held live report of 19 Oct; Step 0 of `docs/GET-GOING.md` complete; PR #15 (`89e1ec9`) merged, so the engine reads heartside's `NOW.md` live.

## 2026-10-28

- stamped at `80d7402`: canon sync `93c4c52` and repository administration `80d7402` are automation and move no head. Fixed the audit's `next_step` finding: the next action now starts with "- Next".

## 2026-10-23

- stamped at `89e1ec9`: PR #15 merged, so NOW.md no longer calls the live read of heartside's `NOW.md` unmerged. `534ea6b` (docs(harness), repository administration) is automation and moves no head.

## 2026-10-22

- reconciled at `16de7ea`: first NOW.md, written by hand at enrolment in the docs steward fleet.
- archived: `docs/history/2026-10-22-HEARTSIDE-NOW.md`, the last copy of heartside's status this engine kept, replaced by a live read of heartside's own `NOW.md` (`90429c8`), because a copy of another repository's status goes stale.
