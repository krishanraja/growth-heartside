---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-20
head: 8c98174
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

## Where it is right now (as of 2026-11-20)

<!-- north-star-state {"week_of": "2026-11-09", "week_target": 1417, "current": 0, "current_as_of": "2026-11-12", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 5, "urgency_reason": "under 40% of the week's target two weeks running (0% now)"} --> **North Star number: U5, stalled.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 12 Nov by the engine's own attribution read; the store's one order in the window, $45, came direct), against $1,417 this week, on the way to $50,000 by 28 December 2026. Everything else pauses unless it moves the number.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own gallery pictures, unaltered and with no label (Krish, 2 Nov), re-pinned on 12 Nov after heartside rebuilt its galleries; none uses Biscuit. The organic share is measured by the engine's own attribution read (`growth.py attribution`) and reported to Control Center as `organic_net_sales_usd` from 12 Nov.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`). The hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` run green; the draft engine's day pack failed every day from 30 Oct to 12 Nov, because the product renders it pinned on 29 Oct had left the live galleries, and renders again from the 12 Nov re-pin (GitHub Actions readback and local renders for 12 to 18 Nov, 12 Nov).

Live:

- Krish said yes to all four asks (19 Nov). Applied: 19 Instagram memes in Buffer are now 8 s reels with the premium end card (reel-cNN.mp4 in release buffer-media-2026-11-18); 21 posts moved from 13:00 to 23:30 UTC; new bio set and read back live. Dashboard read and audit verified (5,319 views, 100% non-followers, 6 profile visits, 1 link tap). Pinning needs the app: the web menu has no pin. Comment batch: 4 posts passed the screen; Krish approved; all 4 posted and verified live (docs/social/2026-11-19-comments.json). Humour engine was unavailable for them. (2026-11-19)
- 12 new Gary and Doug clips were generated on Kling 3.0 pro, each pinned to a start and an end still of the same dog; 10 pass frame by frame, the rug-flop passes from 2.5 s, and the tug-of-war failed twice (Gary drifts into a groomed schnauzer), so the couple film now ends on the chew theft. The register is docs/briefs/2026-11-18-influencer/new-shots-manifest.csv; 168.5 credits spent against Krish's 200 cap. (2026-11-18)
- 105 posts scheduled in Buffer for 18 to 25 Nov (15 a day: 5 each on TikTok, Instagram, Facebook). 14 videos: the three influencer-parody films with the new premium end card (endcard.py), Customs, Alarm, and the nine approved reels from 02r with cleared Epidemic tracks baked in (F34 x4, F40 to F44). 21 still memes: Codex built-in image generation (realistic only; c08 and c34 rejected for AI anatomy), joke lab run stills-1118, rendered with factory/meme.py. Media hosted as the public GitHub release buffer-media-2026-11-18 (Krish chose it). Plan with every Buffer id: docs/social/2026-11-18-buffer-week.json. F28 and F29 held (their joke depends on the named song). (2026-11-18)
- A full inventory is at docs/inventory/2026-11-18-inventory.html: about 54 posts live, 20,874 views, 12 followers, $0 organic sales, nothing posted since 15 Nov 23:31 UTC, and 11 reels Krish approved in 02r (F28, F34 x4, F40 to F44, F29 on IG and FB) never posted. (2026-11-18)
- The engine can consult divergent-thinker through Control Center, dormant until Control Center serves `features.divergent` (control-center PR 963, merged 18 Nov). At U4 or U5 with nothing proposed, the live daily report asks it once a day for three recovery plays, holds any that fail this engine's copy, claims and consent checks (strangers' photos and AI art pitched into communities are walls, from the 18 Nov live run), and proposes the best one as a plan behind `strategy` with a `divergent-thinker spark <rank>, run <runId>` evidence item; the others stay in the activity. The joke lab's screen rejects `rejected_gravity` and `rejected_archive` candidates through its zero-call `score`, and `events import` records what went live. Until the flag is on, nothing is called and each place says so in one line (`engine/divergent.py`, `docs/ENGINE.md`, "Consulting divergent-thinker"). Any session can also consult it at will with `python3 growth.py divergent <op>` (`map`, `provoke`, `challenge`, `diverge`, `score`, `record`): it prints Control Center's JSON, exits 1 when `score` flags an idea and 2 when not served, held, capped or unreachable, and never writes to his list. (2026-11-18)

Waiting or not measured:

- The 12 Nov live report (05:11 UTC) was held: `net_sales_usd` is missing because no imported Shopify window covers this London month (`docs/GET-GOING.md`, step 2), `organic_orders` read 0, and conversion editions were held only because the homepage check read the 19 Oct chat's marker, not the journey homepage public since 29 Oct (heartside `3df57cc`). That check is fixed (12 Nov), so the next report releases the hold and also carries `organic_net_sales_usd`.

## What changed recently

- 2026-11-19 Instagram conversion strategy (`docs/strategy/2026-11-19-ig-conversion.md`): the pasted audit was checked against the live store and the dashboard. Its catalog claim and free-preview hook were false; reach was real (5,319 views, 100% non-followers, 1 link tap). Krish said yes to memes-to-reels, the evening slot, the new bio and a first comment batch, all applied.
- 2026-11-19 A scheduled workflow (`.github/workflows/humour.yml`) runs the joke lab's live screen on a candidates file with Control Center's bearer from the repository secret, so a session on any machine gets the humour engine's reads without the token on that machine. It writes no engine state and posts nothing.
- 2026-11-19 The canon block in `AGENTS.md` moved to v2026.11.18.7, which adds the divergent-thinker consult rule.
- 2026-11-18 Krish ruled every clip is pinned at both ends and tested before a batch (floor pin-both-ends), and the humour engine now runs live from his PC.
- 2026-11-18 Krish ruled the influencer-parody format the house series; the storyboards follow F38's recipe (one stereotype, about 13 active real-dog shots).
- 2026-11-18 The only format that broke out is F38's (a real dog under a deadpan routine parody, with a song); a reset (freeze generation, ship the approved backlog, fix attribution) is proposed to Krish.
- 2026-11-18 The review board moved to https://claude.ai/artifact/6kGmidNyYAnRwiSdzAtcr4, and posts that need a recognisable in-app song go on his phone posts page.
- 2026-11-18 engine-made recovery plays at U5 for Krish to approve in one press; it moves no sale by itself.

## What is next and what is waiting on Krish

- Next (2026-11-19): Krish pins the guest-room reel in the app; read the reels and comments at 24 h, 72 h and 7 days; build pins 2 and 3.
- Earlier next (2026-11-15): Codex reads Ads Manager and every Boost history for 1 Oct to 15 Nov as boost records with objective, destination_url and approval, so the boost audit can judge the F10 pilot and settle the 11 to 13 Nov burst.
- **Waiting on Krish** (listed 2026-11-13, not re-checked 2026-11-14): set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Step 2 of `docs/GET-GOING.md` (a daily Shopify sales import, so `net_sales_usd` is measured) may need a credential only Krish can add; the step says to report a hold naming the secret.
- North Star check (2026-11-19): holds.

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
