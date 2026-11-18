---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-18
head: 72a1236
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

## Where it is right now (as of 2026-11-18)

<!-- north-star-state {"week_of": "2026-11-09", "week_target": 1417, "current": 0, "current_as_of": "2026-11-12", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 5, "urgency_reason": "under 40% of the week's target two weeks running (0% now)"} --> **North Star number: U5, stalled.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 12 Nov by the engine's own attribution read; the store's one order in the window, $45, came direct), against $1,417 this week, on the way to $50,000 by 28 December 2026. Everything else pauses unless it moves the number.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own gallery pictures, unaltered and with no label (Krish, 2 Nov), re-pinned on 12 Nov after heartside rebuilt its galleries; none uses Biscuit. The organic share is measured by the engine's own attribution read (`growth.py attribution`) and reported to Control Center as `organic_net_sales_usd` from 12 Nov.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`). The hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` run green; the draft engine's day pack failed every day from 30 Oct to 12 Nov, because the product renders it pinned on 29 Oct had left the live galleries, and renders again from the 12 Nov re-pin (GitHub Actions readback and local renders for 12 to 18 Nov, 12 Nov).

Live:

- The heartside-* video skills carry every failure from the 17 to 18 Nov night run: Codex stop errors mapped to fixes, the Chrome and MCP credit routes, and a tier 2 brief that lists every live post so a retread cannot score 9 on its words (`factory/panel.py`, tested). (2026-11-18)
- The Audience desk's comment craft from the 4 to 7 Nov pilot is on main as the `heartside-audience-comments` skill (source in `.agents/skills`, copy in `.claude/skills`), salvaged from the unmerged branch `codex/audience-comment-skill` without any handle. The 15 Nov salvage left it out because the session then posted itself; the 16 Nov ruling ("Approve batches, Codex posts") now covers comments, so the craft is kept and posting follows rule 1's batch exception. The other eight stranded or merged branches held nothing main lacks and were deleted at their reviewed commits. (2026-11-18)
- Eight video-production skills are in `.agents/skills/heartside-*` (the source, read by Codex), with exact copies in `.claude/skills/` for Claude Code; the self-test now fails while a copy differs. They were built from the 17 Nov sprint session's transcript, the Codex studio thread and the studio log, plus the first skills session's hand-over. `AGENTS.md` points to them, and the floor gains five process entries plus one quote on `higgsfield-browser-ui-only`. A proposal for a fleet Codex-thread skill is in `docs/proposals/`. With the knowledge `.docx` hash check skipped (it was already failing), 341 self-test checks pass. (2026-11-17)
- Auto-merge now merges on either copy of the check workflow (push or pull_request). Before, when the push-event run finished last it was skipped, and a green pull request never merged (growth-heartside #117, growth-makeyourmindup #129 on 17 Nov). (2026-11-17)
- The humour engine is on call in this repository: `factory/jokelab.py check`, `compare` and `doctor`, with an AGENTS.md rule saying when to consult it. (2026-11-17)
- The 16 to 22 Nov velocity sprint is running on Krish's second machine (17 Nov). Day 1's four new pieces are built from Kling 3.0 Unlimited clips (credits unchanged at 952.35) and each ends on a blanket painted from the film's own dog by heartside.io's own painter (internal-paint, 8 of 30 paints used). None has cleared the panel yet: tier 2 scored d1-absurd-01 8 (v3) then 7 (v4), d1-warm-02 7, d1-note-01 7; d1-warm-01 has no end card yet. Nothing is on the review board and nothing has been posted, so no organic sale is attributable to the sprint yet. (2026-11-16)
- Every joke now starts in the joke lab (factory/jokelab.py). It writes about 30 candidates across weighted families led by the alibi family the 15 Nov audit measured, and screens them before any build: retreads of live posts (by wording, by format, and by the writer's own closest-post answer), dressed-up dogs, rule 5 copy, the three-part core and near duplicates. With --live the humour engine reads each through Control Center's humour route. It stops the build loop where the score moves and the words do not, and learns from Krish's verdicts. On the 17 Nov slate it rejects d1-absurd-01 as an F38 retread and shortlists the four concepts he approved. (2026-11-17)

Waiting or not measured:

- The 12 Nov live report (05:11 UTC) was held: `net_sales_usd` is missing because no imported Shopify window covers this London month (`docs/GET-GOING.md`, step 2), `organic_orders` read 0, and conversion editions were held only because the homepage check read the 19 Oct chat's marker, not the journey homepage public since 29 Oct (heartside `3df57cc`). That check is fixed (12 Nov), so the next report releases the hold and also carries `organic_net_sales_usd`.

## What changed recently

- 2026-11-18 the heartside video skills, the panel's live-post list and new floor words (real-scruffy-dogs, check-in-every-15-minutes, orchestrate-without-babysitting). No studio, Codex, Higgsfield or board action.
- 2026-11-18 .agents/skills/heartside-audience-comments/SKILL.md, .claude/skills/heartside-audience-comments/SKILL.md, AGENTS.md (one sentence). Remote branches deleted: ccr-21e182e5-psq1vi, claude/canva-integration-plan-cpy1p2, claude/i25-drive-library, claude/i25-drive-library-v2, codex/dog-things-wave-3, codex/dog-things-wave-3-fix1, codex/tiktok-link-eligibility-20261111, growth/2026-11-16-sprint. No Drive, Codex or platform action.
- 2026-11-17 the Publishing desk could not read the 23 Sunday placements or the 17 Nov ones: Codex's in-app browser was unavailable. Channel monitor events (`docs/social/2026-11-16-publishing.json`, `docs/social/2026-11-17-publishing.json`) record only the access gap, with no post_check, metric or delivery failure inferred. Both closeout notes stay in `now-notes/` until the fold runs (their North Star lines are now in the fold's form). Next: resume native checks in the visible local Publishing session once browser access returns.
- 2026-11-17 .agents/skills/ (8 skills, source), .claude/skills/ (8 copies), growth.py (self-test: skill copies match), AGENTS.md (one section), factory/floor.json (5 entries, 1 quote), docs/proposals/2026-11-17-codex-desktop-studio-skill.md. No Drive, Higgsfield, Codex or platform action.
- 2026-11-17 factory/jokelab.py, tests/test_jokelab.py, AGENTS.md, factory/README.md, CHANGES.md.
- 2026-11-16 On 17 Nov the studio resumed from Drive 03a. Codex Desktop holds any thread Krish opens, so codex_thread.mjs send is refused ("active writer") and a script-opened thread cannot reach Desktop's in-app browser; `codex queue --thread <id> --message <text>` hands the turn to Desktop and works (durable fix in ai-harness#280). Nano Banana Pro was not Unlimited, so photoreal shots ran as Kling 3.0 text-to-video from each brief's own prompt (Krish's correction, floor read-unlimited-before-ordering). The painter silently hangs on "Still painting" when a photo is under 700 px tall (Teeinblue validation in the console, no message to the buyer): a heartside store finding. The tier 2 panel has no warm anchor, so sentiment pieces are scored against the humour tens.
- 2026-11-17 Krish declined d1-absurd-01 on 17 Nov ("No, it's not funny - the post that is already live on this topic is 10x better") and asked for the fix to be built into this repository; the joke, not the pictures, is now what gets iterated.
- 2026-11-16 the Publishing desk's Sunday check could not run: Codex's in-app browser returned "Browser is not available: iab", so none of the 23 Sunday placements got a native read of media, thumbnail, caption or call to action. Four channel monitor events record the access gap (`docs/social/2026-11-16-publishing.json`) and say plainly that no post_check, metric, zero or delivery failure is inferred; no Drive write or post was made (`7c251e6`).

## What is next and what is waiting on Krish

- Next (2026-11-18): Run the next studio session from `heartside-video-production` with a Sonnet model, and judge every 9-on-words script again as a film before it reaches the board.
- Earlier next (2026-11-15): Codex reads Ads Manager and every Boost history for 1 Oct to 15 Nov as boost records with objective, destination_url and approval, so the boost audit can judge the F10 pilot and settle the 11 to 13 Nov burst.
- **Waiting on Krish** (listed 2026-11-13, not re-checked 2026-11-14): set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Step 2 of `docs/GET-GOING.md` (a daily Shopify sales import, so `net_sales_usd` is measured) may need a credential only Krish can add; the step says to report a hold naming the secret.
- North Star check (2026-11-18): holds.

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
