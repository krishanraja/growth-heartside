# History log

Newest first. Entries are written by the docs steward (see the steward link in
NOW.md) and by humans doing the same job by hand. Nothing in this file
describes current behaviour; NOW.md and the state doc do.

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
