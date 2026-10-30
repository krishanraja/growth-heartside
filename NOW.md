---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-10-30
head: 1525043
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

## Where it is right now (as of 2026-10-30)

<!-- north-star-state {"week_of": "2026-10-26", "week_target": 200, "current": 0, "current_as_of": "2026-10-29", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 4, "urgency_reason": "at 0% of this week's target"} --> **North Star number: U4, far behind.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 29 Oct; the store's only order in the window was fully refunded), against $200 this week, on the way to $25,000 by 28 December 2026. A bold swing every day; work that does not move the number waits.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own product renders with an Example label; none uses Biscuit. Heartside's whole-store number is $24 over the trailing 28 days (heartside `NOW.md`, read 29 Oct); the organic share is still not measured.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`), and its scheduled workflows ran green on 22 Oct: the draft engine, the hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` (GitHub Actions readback, 22 Oct).

Live:

- Krish approved all 24 breed examples and 6 bundle shots, regenerated from heartside's painter v15 (merged to heartside's release branch in PR #79), each with cutout, crops and studio, home and hand mockups; the ledger records every approved painting's sha256 and exact prompt, the old set is superseded, and the shared Drive folder mirrors it. The engine now has real product imagery on all three gifts for its first concepts. (2026-10-30)
- A worker session is upgrading heartside's painter pipeline on branch claude/painter-pipeline-v15 (blanket scattered pattern, breed-character and tone composer), to a pull request with tests and a prepared test board, generating no images and touching nothing live. The breed example launch is held until that lands. (2026-10-29)
- A control test (47 generations, two photos, 3 tones, 6 styles, 4 kinds of chat answer, 3 products) showed heartside's long painter prompt reuses the customer photo's pose and face, so tone and style barely show. A short brief built from the chat's own fields, with each tone owning pose, camera and staging, fixes it; the proposal, builder and evidence are in docs/briefs/painter-prompt/. Stage 1 examples are complete and ready for review; stage 2 is on hold. (2026-10-29)
- Stage 1 breed examples: the four portrait jobs (golden, lab, frenchie, doodle) are complete (painting, cutout, 3 crops, 9 mockups, contact sheet, manifest) on branch codex/heartside-examples-2026-10-29. The two blanket jobs (dachshund, shepherd) have paintings, cutouts and crops, but their home and tall-studio mockups fail the bar: the print is pasted flat across the sofa fold. The painting prompts were rewritten from heartside's 5,500-character rulebook to directed briefs of about 1,200 characters, which fixed the photo-copied face and pose (standard and prompts in review/prompts/stage1-v7/BAR.md on the review branch). (2026-10-29)
- The breed example launch set is 15 approved paintings (8 mugs, 7 portraits across all six dogs and four tones), each with cutout, crops, nine product mockups and a contact sheet, in assets/heartside-examples-2026-10-29/ with the approvals ledger beside it, and the same set in Drive under 00_Brand-Assets/02_Imagery/Product-Examples. The 8 blankets and 6 bundle shots are held for heartside's painter v15 (scattered pattern) and AI fabric mockups; the shepherd Hilarious portrait is dropped. Old artwork is purged from the repository and Drive. (2026-10-29)
- Heartside's prepaid credits are spent by a daily scheduled session (`docs/CREDITS-SESSION.md`) that reserves and settles each generation through Control Center, on protocol 1.16.0 (prepaid credits, `docs/control-center/`; walls in `docs/CONTROL-CENTER-BRIEF.md`). The runner reports credits_spent only for a spend of its own. (2026-10-29)
- Eight scheduled jobs in `automations.json` (sync, numbers, radar, the daily pack, creators, the weekly Answers drafts, store and search, the weekly report), executed on GitHub Actions by `.github/workflows/engine.yml` (`AGENTS.md`, "The schedule").
- The Control Center loop on protocol 1.2.0: a daily directive, one report, Krish's decisions read back by digest (`docs/control-center/ENGINE-PROTOCOL.md`; `b1a14af`). The first live run, on 19 Oct, succeeded (`docs/GET-GOING.md`).
- Answers batch 1 published on heartside, and updated on 22 Oct to quote the new dog voice (`d664d54`, `68940b1`).
- Paid external generation stays off with a zero default budget; since 22 Oct, generation inside prepaid credits within a weekly allocation Krish approved counts as authorised (`0303ffb`; `docs/PROVIDERS.md`).

Waiting or not measured:

- The last live report in the repo (19 Oct) was held: `net_sales_usd` was stale because imported Shopify reports stop at 16 Oct, `organic_orders` is not measured, and conversion editions waited for the V3 homepage (`docs/GET-GOING.md`, "This engine"). Heartside's chat homepage went public on 19 Oct (heartside `9ea7e34`); whether the hold has released is not recorded here.

## What changed recently

- 2026-10-29 Hilarious may use theatrical staging but never invents the dog's toys, food, clothes, habits or places (Ruling, Krish, 2026-10-29).
- 2026-10-29 The short directed-brief prompt method is the fix proposed for heartside's painter prompt; the examples check's --only flag wrongly flags other jobs' files (fix in growth.py awaits Krish).
- 2026-10-29 Heartside's painter moved from the 5,500-character rulebook to the directed brief (recipes v10 to v14), driven by this engine's control test and the 24 example paintings.
- 2026-10-29 **Creative direction set, and Codex briefed for heartside's breed examples.** Real life, then the painting: photographic AI worlds, the real product always real, one hero allowed to morph a dog into its artwork. Five posts a day per platform once running. Codex makes stage 1 (six breeds) under a card with a strict acceptance checker (`engine/examples.py`); stage 2 waits for review and Krish's yes. Shoppable tags go to a heartside session.
- 2026-10-29 **Organic attribution is live: $0 from organic posts over the trailing 28 days.** The read-only Shopify app is installed; the first read found one store order in the window, fully refunded, so net sales are $0. Net sales subtract refunds and never count a fully refunded order. Buffer's own link tags count as organic social. Buffer's link shortening is off on all three Heartside channels, so the engine's tags reach the store intact.
- 2026-10-29 **Organic attribution is built and waiting on read-only order access.** `growth.py attribution` classifies orders as engine-tagged (post family known), organic social, organic search, paid, pending or direct, over the trailing 28 days and the last full week, and stores aggregates only; the Control Center `organic_orders` objective reads it, missing until the first live read.
- 2026-10-29 **The engine caught up with heartside's relaunch and is off STOP** (branch `claude/canva-integration-plan-cpy1p2`). Rules now come from heartside's current sources; `check` refuses Biscuit, every exclamation mark, the worn lines and stacked fragments. Prices come from the canon's configured baseline, cross-checked against the live store; a disagreement holds the gift. Purchase drafts may sell any live gift the film shows; Krish ruled the same day that the mug sells equally. The renderer uses the store's own renders, refuses blank templates and tiles, and labels every frame Example. The Shopify store handle left every tracked file for the `HEARTSIDE_SHOP_DOMAIN` repository variable, with a test that fails if a handle returns; it remains in git history. `docs/GEO-AEO.md` facts and prices are current, and it no longer claims free shipping to every US address.
- 2026-10-27 **Heartside relaunched, and this engine is on STOP until it catches up** (`docs/briefs/2026-10-27-heartside-revamp-impact.md`). Sync at heartside `bea22ce` found that the four rule sections it checks had moved into heartside's history. The renderer still uses the retired Biscuit and the old mug photos. A Heartside Canva brand kit exists but has not been updated.
- 2026-10-27 **The architecture plan is now v3, reviewed three times, and still proposed, not built** (`docs/briefs/2026-10-27-architecture.md`). It has 14 specialists. `learn` owns what works, `librarian` owns the Drive `Heartside/Growth` folder, and `audience` owns followers. GA comes from Control Center. Codex posts approved batches through Buffer from Krish's PC, and Claude orchestrates and checks. The failure register is filed at `docs/REGISTER.md`, and the Canva design-system Cowork prompt at `docs/briefs/2026-10-27-cowork-canva-design-system.md` (the brand-kit prompt is superseded). heartside.io has been on its password page ("Opening soon") since some time after 23 Oct; Krish says it is deliberate until heartside PR #50.

## What is next and what is waiting on Krish

- Next (2026-10-30): Krish runs `docs/briefs/2026-10-29-heartside-showcase-handover.md` in a heartside session to bring the approved set into the store; next painter improvement is the shared Over the top frame, which makes the breeds look samey.
- **Next action:** Codex makes stage 1 of heartside's breed examples (6 paintings, with cutouts, crops and mockups) from `docs/briefs/codex/2026-10-29-breed-examples-stage-1.md`, on its own branch; Claude checks the return with `python3 growth.py examples check --stage 1` and a frame-by-frame review before Krish's review. Then the daily layer from `docs/briefs/2026-10-29-creative-direction.md`: 5 posts a day per platform, starting with "Translate your dog" carousels.
- **Waiting on Krish:** start Codex on this repository with the one line "Run docs/briefs/codex/2026-10-29-breed-examples-stage-1.md". Set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). A heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Steps 2 and 3 of `docs/GET-GOING.md` may need a credential only Krish can add for a daily Shopify import; the step says to report a hold naming the secret.
- North Star check (2026-10-30): holds.

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
