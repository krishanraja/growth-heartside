---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-04
head: 172be13
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

## Where it is right now (as of 2026-11-04)

<!-- north-star-state {"week_of": "2026-10-26", "week_target": 200, "current": 0, "current_as_of": "2026-10-29", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 4, "urgency_reason": "at 0% of this week's target"} --> **North Star number: U4, far behind.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 29 Oct; the store's only order in the window was fully refunded), against $200 this week, on the way to $25,000 by 28 December 2026. A bold swing every day; work that does not move the number waits.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own product renders with an Example label; none uses Biscuit. Heartside's whole-store number is $24 over the trailing 28 days (heartside `NOW.md`, read 29 Oct); the organic share is still not measured.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`), and its scheduled workflows ran green on 22 Oct: the draft engine, the hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` (GitHub Actions readback, 22 Oct).

Live:

- The production handoff identifies the three motion candidates (F04, F05, F12), their unchanged Drive originals and the separate F12 paid opening pair by SHA-256. The candidates await exact-file creative decisions. Paid activation is held. (2026-11-04)
- All twelve organic posts (F01 to F07, F10 to F12, with F06 in three breeds) are locked by Krish and pass `lock.py gate`; the lock page shows them locked (2026-11-03).
- The social library is in Krish's Drive (`Heartside/05_Social-Library`, map in `docs/DRIVE-MAP.md`): one Codex README, the posting strategy, the schedule Sheet with captions, tracked links and lock fingerprints, and each post's media in `Posts/<post id>/`. Krish's home computer files the media (`factory/send_library.py`, 39 files read back byte for byte); the zip is a backup. Codex posts only rows Krish marks `approved = yes` (2026-11-03).
- Sound is locked for all ten approved concepts and the lock system (joke bank, render catalog, fingerprinted locks, copy, breed, media and drift gates, independent reviewer, 5-then-1-in-10 trust ramp) builds every post from a spec (2026-11-02).
- Five channel guides separate posts made to be shared from posts made to earn shop visits; dog POV and product posts stay in one schedule (`docs/CHANNEL-TASKS.md`, 2026-11-03).
- The seven channel tasks run inside the radar, daily pack, store and report jobs, mapped by `crew/registry.json` (2026-10-30).
- All 24 breed examples and 6 bundle shots from heartside's painter v15 are approved, with the ledger of sha256s and prompts, mirrored in Drive (2026-10-30).
- Eight scheduled jobs in `automations.json` run on GitHub Actions (`.github/workflows/engine.yml`); the Control Center loop runs on protocol 1.16.0, with prepaid credits spent by a daily session (`docs/CREDITS-SESSION.md`, `docs/control-center/`). Paid external generation stays off with a zero default budget; generation inside Krish's prepaid-credit allocation counts as authorised (`0303ffb`; `docs/PROVIDERS.md`).

Waiting or not measured:

- The last live report in the repo (19 Oct) was held: `net_sales_usd` was stale because imported Shopify reports stop at 16 Oct, `organic_orders` is not measured, and conversion editions waited for the V3 homepage (`docs/GET-GOING.md`, "This engine"). Heartside's chat homepage went public on 19 Oct (heartside `9ea7e34`); whether the hold has released is not recorded here.

## What changed recently

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

- Next (2026-11-04): Read the three owner decisions on the private board before proposing a replacement master.
- **Waiting on Krish:** set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Steps 2 and 3 of `docs/GET-GOING.md` may need a credential only Krish can add for a daily Shopify import; the step says to report a hold naming the secret.
- North Star check (2026-11-04): holds.

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
