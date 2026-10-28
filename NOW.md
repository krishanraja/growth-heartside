---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-10-28
head: 80d7402
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

## Where it is right now (as of 2026-10-28)

<!-- north-star-state {"week_of": "2026-10-26", "week_target": 200, "current": null, "current_as_of": null, "current_source": null, "urgency": 4, "urgency_reason": "not measured yet (attribution not wired)"} --> **North Star number: U4, far behind.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: not measured yet (attribution not wired), against $200 this week, on the way to $25,000 by 28 December 2026. A bold swing every day; work that does not move the number waits.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`), and its scheduled workflows ran green on 22 Oct: the draft engine, the hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` (GitHub Actions readback, 22 Oct).

Live:

- Eight scheduled jobs in `automations.json` (sync, numbers, radar, the daily pack, creators, the weekly Answers drafts, store and search, the weekly report), executed on GitHub Actions by `.github/workflows/engine.yml` (`AGENTS.md`, "The schedule").
- The Control Center loop on protocol 1.2.0: a daily directive, one report, Krish's decisions read back by digest (`docs/control-center/ENGINE-PROTOCOL.md`; `b1a14af`). The first live run, on 19 Oct, succeeded (`docs/GET-GOING.md`).
- Answers batch 1 published on heartside, and updated on 22 Oct to quote the new dog voice (`d664d54`, `68940b1`).
- Paid external generation stays off with a zero default budget; since 22 Oct, generation inside prepaid credits within a weekly allocation Krish approved counts as authorised (`0303ffb`; `docs/PROVIDERS.md`).

Waiting or not measured:

- On 23 Oct, a local Windows read of Heartside's public `/products.json` returned HTTP 429. PR #19 (`e373717`) makes that local failure read as unverified rather than four missing gifts. A new local sync read all four gifts as available, and the scheduled GitHub runner's saved 11:31 UTC snapshot also contained all four.
- The last live report in the repo (19 Oct) was held: `net_sales_usd` was stale because imported Shopify reports stop at 16 Oct, `organic_orders` is not measured, and conversion editions waited for the V3 homepage (`docs/GET-GOING.md`, "This engine"). Heartside's chat homepage went public on 19 Oct (heartside `9ea7e34`); whether the hold has released is not recorded here.
- Step 0 of `docs/GET-GOING.md` is complete. It corrected stale documentation only; the live report's numbers are unchanged.
- Merged on 22 Oct (PR #15, `89e1ec9`): the engine keeps no copy of heartside's status and reads heartside's `NOW.md` live instead (`90429c8`). The hourly sync commits nothing, and the docs steward runs nightly on this repository.

## What changed recently

- 2026-10-23 **An unreachable public catalog now reads as unverified, not as four missing gifts** (`398d15d`, PR #19 `e373717`; `engine/offers.py`, `tests/test_offers.py`). A local read of Heartside's `/products.json` returned HTTP 429, and the engine had no way to tell that from the gifts being gone. The scheduled runner's saved snapshot still showed all four (`74a2939`).
- 2026-10-23 **The North Star now has a number, a weekly ladder and an urgency rating, so every session knows how far behind it is and how hard to push.** Ruling (Krish, 2026-10-23): every repository chases one aggressive number on a weekly ladder, and urgency U1 to U5 sets its intensity. The number and ladder are in `docs/NORTH_STAR.md`; where it stands is the first line under "Where it is right now". Contract: ai-harness `contract/north-star-metric.md`.
- **2026-10-22: no copy of heartside's status kept here** (`90429c8`, merged in PR #15 as `89e1ec9`). A copy of another repository's status goes stale, so `growth.py sync` stops writing one and reads heartside's own `NOW.md` live; unreadable or stale reads as "unknown" and the text is withheld. The last copy is archived at `docs/history/2026-10-22-HEARTSIDE-NOW.md`. Ruling recorded in the commit.
- **2026-10-22: a media-credit brief for Higgsfield and Runway** (`dfcc815`): a plan for Krish's list, stills before motion, generating nothing before his yes. It runs ahead of the main build because the Christmas cut-off will not wait (`docs/GET-GOING.md`, Step 0.5).
- **2026-10-22: prepaid credits inside an approved allocation pass the provider budget** (`0303ffb`). Krish ruled that such generation counts as authorised; publication, ad spend, top-ups and plan changes still need their own approval.
- **2026-10-22: gift-line examples in the new voice** (`68940b1`). Krish: "update the Answers article". The three published Answers articles now quote real sentences in each dog's own personality, following heartside PR #44.
- **2026-10-21: protocol 1.2.0 copied from Control Center** (`b1a14af`). It adds "Versions": accept any 1.x back. Legibility and Mindmake required exactly 1.0.0 and stopped reporting for two days when Control Center began serving 1.1.0; this engine already accepted it.
- **2026-10-21: GEO and AEO strategy and an eighth job** (`70fa624`): `docs/GEO-AEO.md`, a 28-question bank and a weekly Answers job on Wednesdays, with batch 1 drafted for Krish.
- **2026-10-21: heartside's dog-voice ruling and rewritten positioning taken in** (`ca52b75`, `400d62b`). `check` now refuses the retired third-person gift lines and the retired one-line offer.
- **2026-10-19: the engine runs autonomously and reports through the one protocol** (`8ba5523`, `a87b932`), with "Get going" as the way a session picks up the plan in `docs/GET-GOING.md` (`70d9236`), and the copywriting, offers and demand corpus wired into the jobs (`c5654b4`).
- **2026-10-18: the North Star was set** (`bf8b536`, `c51ed5b`), and the Control Center brief replaced the earlier Control Centre handoff (`9790ed7`).
- **2026-10-17: the engine shipped** (`5c31853`, PR #1) with production, replay and recovery runs recorded in `docs/HANDOFF.md` and `docs/VERIFICATION-2026-10-17.json`.

## What is next and what is waiting on Krish

- Next: resolve the V2 performance-review direction in the media-credit brief against Heartside's current V3 gift canon, then prepare Step 0.5 of `docs/GET-GOING.md` as a reviewable Control Center plan. Do not generate or spend before the plan decision.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Steps 2 and 3 of `docs/GET-GOING.md` may need a credential only Krish can add for a daily Shopify import; the step says to report a hold naming the secret.
- North Star check (2026-10-23): holds.

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
