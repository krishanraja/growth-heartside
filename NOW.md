---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-17
head: 7c251e6
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

## Where it is right now (as of 2026-11-17)

<!-- north-star-state {"week_of": "2026-11-09", "week_target": 1417, "current": 0, "current_as_of": "2026-11-12", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 5, "urgency_reason": "under 40% of the week's target two weeks running (0% now)"} --> **North Star number: U5, stalled.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 12 Nov by the engine's own attribution read; the store's one order in the window, $45, came direct), against $1,417 this week, on the way to $50,000 by 28 December 2026. Everything else pauses unless it moves the number.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own gallery pictures, unaltered and with no label (Krish, 2 Nov), re-pinned on 12 Nov after heartside rebuilt its galleries; none uses Biscuit. The organic share is measured by the engine's own attribution read (`growth.py attribution`) and reported to Control Center as `organic_net_sales_usd` from 12 Nov.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`). The hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` run green; the draft engine's day pack failed every day from 30 Oct to 12 Nov, because the product renders it pinned on 29 Oct had left the live galleries, and renders again from the 12 Nov re-pin (GitHub Actions readback and local renders for 12 to 18 Nov, 12 Nov).

Live:

- Every joke now starts in the joke lab (factory/jokelab.py). It writes about 30 candidates across weighted families led by the alibi family the 15 Nov audit measured, and screens them before any build: retreads of live posts (by wording, by format, and by the writer's own closest-post answer), dressed-up dogs, rule 5 copy, the three-part core and near duplicates. With --live the humour engine reads each through Control Center's humour route. It stops the build loop where the score moves and the words do not, and learns from Krish's verdicts. On the 17 Nov slate it rejects d1-absurd-01 as an F38 retread and shortlists the four concepts he approved. (2026-11-17)
- HyperFrames and Claude Ads evaluated (docs/audits/2026-11-15-hyperframes-and-claude-ads.md). HyperFrames is integrated narrowly as factory/hf.py and the note template, pinned and without telemetry, and its test render passed every factory gate with the product's pixels intact; Claude Ads is not installed, and its scoring method is re-implemented as engine/ad_audit.py (growth.py ads audit, ads_audit.json in the Sunday report), which caught 6 of 6 seeded boost breaches and, from this repository's own record, flags the 11 to 13 Nov Facebook burst as having no boost on record. (2026-11-15)
- AGENTS.md and docs/CHANNEL-TASKS.md say where each kind of Codex work runs (Ruling, Krish, 2026-11-15): film and still builds are content production, cards built by his PC's lane and never shown in Codex Desktop; the Publishing, Engagement and Audience desks are driven only from a Claude session on his own computer, visible in his Codex Desktop app. (2026-11-15)
- `AGENTS.md` rule 4 now lets an AI person appear in a Heartside post under Krish's ruling of 15 Nov (Ruling, Krish, 2026-11-15: AI people may be used anywhere, with his explicit yes before one is used and again on the finished asset before it goes out; no AI labels anywhere): his yes before it is used in a named piece and his yes on the finished asset, each with his words, never through concept-level approval; never a customer, buyer, reviewer or testimonial, never holding or reviewing the product as a customer would; no AI label. `factory/floor.json` (`ai-person-two-yeses`, `no-ai-label`, `no-badges`) and `growth.py claims` (`ai-label`, `ai-person`, `not-a-real-customer`) agree, with self-test checks that prove it, and the docs that asked for a platform AI label (`docs/PUBLISHING.md`, `docs/PAID-BOOSTS.md` gate 6) now say never switch one on. The review queue's `d9-ai-label` ask stays open for Krish. (2026-11-15)
- Claude and Codex division written in (Ruling, Krish, 2026-11-15): Codex does the film builds and the social legwork in a session Krish watches in Codex Desktop, records `post_check` (cover, caption, call to action) and `boost` readings as events (`engine/social.py`), and never writes Drive; Claude writes the Sheet. The Sunday report now carries "What worked, what did not, and why" with paid split from organic, shown to Krish as a check-in. First analysis: `docs/audits/2026-11-15-interest-vs-paid.md` (alibi family wins; no paid visit has produced a cart add; the 11 to 13 Nov Facebook traffic burst is not in the boost record). (2026-11-15)
- Heartside's decision, spend, copy and delete asks now reach Krish's one list (I-24). review/queue.json holds the 19 open asks from docs/plans/A1.md; the daily Control Center run proposes the top 3 behind their wall, reads his answers back by id, stops asking an answered one and reports "Answers to apply". The review board keeps posts and their media. (2026-11-14)
- The day pack, radar, creators and store jobs are off the schedule (Krish, 14 Nov, item 5.6). Four jobs stay scheduled: sync, numbers, answers and the Sunday report; the four run only when named. (2026-11-14)

Waiting or not measured:

- The 12 Nov live report (05:11 UTC) was held: `net_sales_usd` is missing because no imported Shopify window covers this London month (`docs/GET-GOING.md`, step 2), `organic_orders` read 0, and conversion editions were held only because the homepage check read the 19 Oct chat's marker, not the journey homepage public since 29 Oct (heartside `3df57cc`). That check is fixed (12 Nov), so the next report releases the hold and also carries `organic_net_sales_usd`.

## What changed recently

- 2026-11-17 Krish declined d1-absurd-01 on 17 Nov ("No, it's not funny - the post that is already live on this topic is 10x better") and asked for the fix to be built into this repository; the joke, not the pictures, is now what gets iterated.
- 2026-11-16 the Publishing desk's Sunday check could not run: Codex's in-app browser returned "Browser is not available: iab", so none of the 23 Sunday placements got a native read of media, thumbnail, caption or call to action. Four channel monitor events record the access gap (`docs/social/2026-11-16-publishing.json`) and say plainly that no post_check, metric, zero or delivery failure is inferred; no Drive write or post was made (`7c251e6`).
- 2026-11-15 the audience-comments skill, its taste record (it names people who commented, by handle) and the 7 Nov approval packet were left out: the skill has the session post comments, which rule 1 forbids, and the packet is stale.
- 2026-11-15 copied from content-engine (krishanraja/content-engine#719), where it was tested live on 15 Nov.
- 2026-11-13 the Order Loop's claims gate now refuses words on a gift, handmade, uninspected quality, delivery promises and deal wording after an adversarial review found the first gate passed whole captions instead of checking each sentence; four day-pack captions that put a note on the gift were corrected (`1a3ae46`, `a0bcede`, `61184ad`).
- 2026-11-13 Heartside now tells AEO-Engine why it was not asked, re-asks when its bank grows, and reads AEO's win kits once Control Center serves them (Krish, 13 November).
- 2026-11-12 Krish, 2026-11-12: "make sure everything's a cohesive system and that the project documentation is 100% up to date with absolutely nothing old or misleading left in there".
- 2026-11-12 Krish, 12 Nov: "Ensure all social media posts adhere to these best practices." Placement left the lock fingerprint, so all 16 factory specs moved onto the profile and keep their locks; Codex labels move from text top y 300 to y 360.
- 2026-11-12 a docs and bug audit on Krish's question of 12 Nov; the nine closeout notes the fold could not read moved to docs/history, so the fold runs again.
- 2026-11-11 Krish asked that every growth engine's priorities, obsessions and next steps feed Control Center live and that he can instruct each engine ("Get building", 11 Nov); his words never leave engine/engine_state.py.
- 2026-11-11 Krish found TikTok's commercial songs can only be added in the phone app.
- 2026-11-11 Krish found copying captions from the Doc into Instagram fiddly.

## What is next and what is waiting on Krish

- Next (2026-11-17): Run the next slot through the joke lab end to end: brief to a sub-agent, screen --live on CONTROL_CENTER_ENGINE_TOKEN, tier 2 on the shortlist's words, Krish's verdicts recorded with jokelab.py verdict.
- Earlier next (2026-11-15): Codex reads Ads Manager and every Boost history for 1 Oct to 15 Nov as boost records with objective, destination_url and approval, so the boost audit can judge the F10 pilot and settle the 11 to 13 Nov burst.
- **Waiting on Krish** (listed 2026-11-13, not re-checked 2026-11-14): set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Step 2 of `docs/GET-GOING.md` (a daily Shopify sales import, so `net_sales_usd` is measured) may need a credential only Krish can add; the step says to report a hold naming the secret.
- North Star check (2026-11-17): holds.

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
- `docs/HANDOFF.md` where it says the public catalog does not offer the four V3 gifts, and that product work is in heartside PR #13; `STRATEGY.md` also points at PR #13. Heartside's chat-led store went live on 19 Oct (heartside `docs/history/HANDOFF-2026-10-21.md`, section 3), and heartside's own `NOW.md`, not that pull request, holds its product state.
- `docs/HANDOFF.md` on "seven" jobs: it is the 17 Oct record; `automations.json`, `AGENTS.md` and `README.md` have eight since the Answers job of 2026-10-21 (`70fa624`).
- `docs/briefs/2026-10-22-media-credits.md` on its creative direction: see "What is next" above.
- Briefs in `docs/briefs/` that ask for an Example label on product pictures (the 27 Oct revamp impact, the 29 Oct creative direction, the 2 Nov sound and scripts): Krish ruled on 2 Nov "We never need EXAMPLE badges anywhere" (`AGENTS.md`, rule 4).
- Anything in `docs/history/`, including `2026-10-22-HEARTSIDE-NOW.md`: the record, not current guidance.
