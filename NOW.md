---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-14
head: 97a1a1d
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

## Where it is right now (as of 2026-11-14)

<!-- north-star-state {"week_of": "2026-11-09", "week_target": 1417, "current": 0, "current_as_of": "2026-11-12", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 5, "urgency_reason": "under 40% of the week's target two weeks running (0% now)"} --> **North Star number: U5, stalled.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 12 Nov by the engine's own attribution read; the store's one order in the window, $45, came direct), against $1,417 this week, on the way to $50,000 by 28 December 2026. Everything else pauses unless it moves the number.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own gallery pictures, unaltered and with no label (Krish, 2 Nov), re-pinned on 12 Nov after heartside rebuilt its galleries; none uses Biscuit. The organic share is measured by the engine's own attribution read (`growth.py attribution`) and reported to Control Center as `organic_net_sales_usd` from 12 Nov.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`). The hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` run green; the draft engine's day pack failed every day from 30 Oct to 12 Nov, because the product renders it pinned on 29 Oct had left the live galleries, and renders again from the 12 Nov re-pin (GitHub Actions readback and local renders for 12 to 18 Nov, 12 Nov).

Live:

- the Saturday store job writes one line per gift (id, title, canonical price, ready or why not) instead of pasting the whole catalog, so its pack passes the engine's own check; it had failed four runs on 14 Nov (over 6,000 characters, untracked store links). (2026-11-14)
- docs/control-center/ is Control Center's protocol bundle 1.33.0, byte for byte (bundle_sha256 4b7175a8aebbb8979eaefbeea1b7f0f44f2cffa0bbba9cea341da784fe7fde4d), the last protocol version of 14 November. (2026-11-14)
- docs/control-center/ is Control Center's protocol bundle 1.28.0, byte for byte (bundle_sha256 b0dfa0d7aaa10aea0de45fb5f7dcc241c62bef70766f0fed9c6351d69af1b791), with bundle.json and a hash test that fails an edit in place (integration plan I-11). (2026-11-14)
- The engine now proposes a post only on a channel Krish approved for posting (`config/channels.json`: Instagram, Facebook, TikTok); a creative for Pinterest or any other channel is held with its reason, never put on his list. Before this, `post_proposals` would have turned an approved pin into a go-live, although docs/CHANNEL-TASKS.md says Pinterest is not a posting channel. The pins on Heartside's Pinterest did not come through the engine: Buffer (read 14 Nov) shows four, none queued; the three of 12 and 13 November repeat the Instagram captions, were created outside Buffer, and landed about 26 to 28 minutes after each Instagram post, the pattern of Pinterest's own auto-publish from Instagram, an account setting. Also: the report's credits line names docs/CREDITS-SESSION.md instead of a jobs/credits.md that never existed and no longer claims a daily spend; "proposed 1.23.0" labels read 1.26.0, the version Control Center shipped (behaviour keys on the `ai_answers_detail` flag); the run summary lists what it withdrew. Verified live: a synthetic Control Center run on main at d9ff14b sent no proposals and read back a matching report; the Codex reservation of 10 November is already settled (`not_open`). (2026-11-14)
- The Wednesday Answers job no longer falls back to bank order in silence when it cannot see AEO-Engine's kits. `engine.yml` gains a read-only step on Wednesdays (or a manual `answers` run) that runs `growth.py cc kits`; the existing Control Center engine token reaches it only once the repository variable `ANSWERS_READS_KITS` is `yes`. Without the token, or when the standing cannot be read, the brief's headline says it is held and why. Docs made true against live state: the Heartside credits scheduled task is disabled on purpose (it last ran 4 November), and GET-GOING names the protocol copy as 1.22.0 at 36df34bc. Re-pinning that copy to Control Center's current head was not possible from this session: it cannot read the control-center repository. (2026-11-14)
- The daily Control Center report no longer re-sends the two advice proposals it had sent every day since 19 October (`heartside:rec:product-readiness`, `heartside:rec:measurement`): `recommendations.json` is empty, and the report takes both back through `withdrawn` (1.10.0) once capabilities serve it, read from a new capabilities call because the directive never carries that flag. A recommendation may now carry a plan behind a wall (`stage: plan`, its exact words in `exact_payload`, the digest bound to them); none is written. The runner's read-only orders read now counts paid orders still unfulfilled more than 7 days after purchase, and the report raises a "Paid orders not shipped within a week" hold when any exist: the heartside order workflows keep no successful runs since 10 November, so this is the outcome check that still sees them. Read on 14 Nov: one paid order since 1 November, fulfilled; none unfulfilled. (2026-11-14)
- `python3 growth.py paths <schedule.csv>` reports each Schedule row's counted path to an order (tracked link, registered code, tracked profile link, or none) and prints a tracked profile URL per platform under a reserved creative id (`<P>_OFFER_BIO_C900`), which attribution counts in the engine tier. Read on 14 Nov from the 02t Sheet: only the Facebook rows carry a counted path; the Instagram and TikTok rows say "link in bio". `config/profile-links.json` records which profiles Krish has set (none yet), and the 02t builder then names that URL in the link column. No code, caption or post was created. (2026-11-14)
- The daily run now says when the directive does not serve AI answers ("AI answers: not served by today's directive."), which is why no request to AEO-Engine was ever filed: Control Center holds none for Heartside on 13 November. A standing Control Center could not read is never taken as no request on file, and the run re-asks AEO only when the bank's valid questions outgrow the request on file or, once served, the request's digest differs. Once Control Center serves features.ai_answers_detail (proposed protocol 1.23.0; Ruling, Krish, 2026-11-13: AEO's win kits reach him through each venture's own growth engine), `growth.py cc kits` keeps AEO's kits in the gitignored local/control-center/ai-answers.json, the Wednesday Answers brief takes the top two kits before bank order, and published bank rows are told to AEO as shipped, once per change. Logs carry counts only. (2026-11-13)
- One plan now holds everything lined up for this engine: docs/plans/A1.md consolidates the Order Loop exhibit, LOOP.md, GET-GOING's open steps, the review board's waiting items, the Codex queue, Sprint 120, SCHEDULE, PAID-BOOSTS, REGISTER and the briefs, with duplicates merged, stale items closed, and the unbuilt steps (buy lane in production, batch Sheet builder, Day 0 reads, Buffer reader, ledger and registry, test-card reader, autonomy loop) written as briefs. GET-GOING points to it. (2026-11-13)
- The Order Loop plan is built in its first three steps and merged to main (pull requests #78 and #79): the claims gate refuses words on a gift, handmade, uninspected quality, delivery promises and deal wording, and corrected four day-pack captions that put a note on the gift; net_sales_usd is measured from the runner's own read through a London-month window; untagged Meta visits are unverified until the ads questions are answered; and factory/loop.py ranks the buy lane on fields each platform shows, with orders as a gate. The exhibit, rulings and test cards are in docs/plans/2026-11-13-order-loop.md. (2026-11-13)
- Heartside's AI answers are AEO-Engine's, the one AI-answers specialist (Ruling, Krish, 2026-11-12): the daily Control Center run asks AEO once to track the question bank's buyer questions with heartside.io and reads Heartside's standing back (protocol 1.22.0, engine/ai_answers.py); the Wednesday Answers job drafts from AEO's misses and moves, and the monthly hand panel is retired into AEO. The protocol copy in docs/control-center/ is Control Center's at 36df34bc (protocol 1.22.0). (2026-11-13)
- Eight scheduled jobs in `automations.json` run on GitHub Actions (`.github/workflows/engine.yml`); Control Center protocol 1.20.0; paid external generation stays off with a zero default budget (`docs/CREDITS-SESSION.md`, `docs/PROVIDERS.md`).

Waiting or not measured:

- The 12 Nov live report (05:11 UTC) was held: `net_sales_usd` is missing because no imported Shopify window covers this London month (`docs/GET-GOING.md`, step 2), `organic_orders` read 0, and conversion editions were held only because the homepage check read the 19 Oct chat's marker, not the journey homepage public since 29 Oct (heartside `3df57cc`). That check is fixed (12 Nov), so the next report releases the hold and also carries `organic_net_sales_usd`.

## What changed recently

- 2026-11-13 the Order Loop's claims gate now refuses words on a gift, handmade, uninspected quality, delivery promises and deal wording after an adversarial review found the first gate passed whole captions instead of checking each sentence; four day-pack captions that put a note on the gift were corrected (`1a3ae46`, `a0bcede`, `61184ad`).
- 2026-11-13 Heartside now tells AEO-Engine why it was not asked, re-asks when its bank grows, and reads AEO's win kits once Control Center serves them (Krish, 13 November).
- 2026-11-12 Krish, 2026-11-12: "make sure everything's a cohesive system and that the project documentation is 100% up to date with absolutely nothing old or misleading left in there".
- 2026-11-12 Krish, 12 Nov: "Ensure all social media posts adhere to these best practices." Placement left the lock fingerprint, so all 16 factory specs moved onto the profile and keep their locks; Codex labels move from text top y 300 to y 360.
- 2026-11-12 a docs and bug audit on Krish's question of 12 Nov; the nine closeout notes the fold could not read moved to docs/history, so the fold runs again.
- 2026-11-11 Krish asked that every growth engine's priorities, obsessions and next steps feed Control Center live and that he can instruct each engine ("Get building", 11 Nov); his words never leave engine/engine_state.py.
- 2026-11-11 Krish found TikTok's commercial songs can only be added in the phone app.
- 2026-11-11 Krish found copying captions from the Doc into Instagram fiddly.
- 2026-11-10 The first 127-character Instagram candidate hid its CTA behind more despite fitting the editor limit. The shorter version passed public readback; the profile-audit acceptance now checks native truncation as well as character count. No website, post, spend or account-type change.
- 2026-11-10 TikTok's username, caption and stickers start about y 1340, so the y 1450 label spot only worked on Instagram; the chat floor in factory/ui_layout.py moved from 1480 to 1250.
- 2026-11-10 the library lane filed the v2 cuts into new F38-real and F41-real folders because the manifest named the post F38-real; the manifest post must match the existing Posts folder.
- 2026-11-10 AGENTS points to the official assets. Profile review history, exact approval, asset hashes, live readbacks and link-feature limits are recorded in docs/profile-pages/2026-11-10/ROLLOUT.md. Facebook Learn more retains the verified tracked destination; Buy now would require a new store integration.
- 2026-11-10 Krish found F38 labels under Instagram's caption area, so labels now sit in one fixed, visible place.

## What is next and what is waiting on Krish

- Next (2026-11-14): read the next hourly draft engine run; the store job should complete and the run go green.
- **Waiting on Krish** (listed 2026-11-13, not re-checked 2026-11-14): set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Step 2 of `docs/GET-GOING.md` (a daily Shopify sales import, so `net_sales_usd` is measured) may need a credential only Krish can add; the step says to report a hold naming the secret.
- North Star check (2026-11-14): holds.

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
