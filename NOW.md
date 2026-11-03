---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-03
head: df31a80
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

## Where it is right now (as of 2026-11-03)

<!-- north-star-state {"week_of": "2026-10-26", "week_target": 200, "current": 0, "current_as_of": "2026-10-29", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 4, "urgency_reason": "at 0% of this week's target"} --> **North Star number: U4, far behind.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 29 Oct; the store's only order in the window was fully refunded), against $200 this week, on the way to $25,000 by 28 December 2026. A bold swing every day; work that does not move the number waits.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own product renders with an Example label; none uses Biscuit. Heartside's whole-store number is $24 over the trailing 28 days (heartside `NOW.md`, read 29 Oct); the organic share is still not measured.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`), and its scheduled workflows ran green on 22 Oct: the draft engine, the hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` (GitHub Actions readback, 22 Oct).

Live:

- Five channel guides distinguish posts made to be shared from posts made to earn shop visits. The existing social library and schedules remain authoritative. (2026-11-03)
- F07 and F11 are locked, and both pass the full go-live gate. The F06 roasts are rebuilt for all three breeds: Krish's dachshund-style humour, troll-grin photos and meme type. F10 carries his "Bro, that's a bone" and "They threw it AWAY mate" lines. All nine pass the media gates. (2026-11-03)
- The social library is in Krish's Drive (Heartside/05_Social-Library). It holds: - the Codex instructions; - the posting strategy; - a 27-row schedule Sheet with captions that pass the copy rules, tracked links and lock fingerprints; - one checksummed zip of the nine locked posts, re-mixed with licensed full-quality audio. Codex posts approved rows; Krish fills the approved column. (2026-11-03)
- All nine Christmas posts are locked by Krish and pass the full go-live gate: F03, F05, F06 (frenchie, dachshund, lab), F07, F10, F11, F12. The lock page shows all nine as locked. (2026-11-03)
- Sound is locked for all ten approved concepts. Wave 1 animatics (F01, F02, F04) are on Krish's board: 30 Higgsfield key frames (82.5 credits, settled) cut to the locked sound, each ending on the real store render. F04, F05 and F12 are recast to the golden and the frenchie. heartside's Codex lane does not cover this repository yet, so the final builds wait on Krish's call. (2026-11-02)
- Krish approved 10 funny concepts (F01-F07 without F08/F09, F10, F11, F12). The engine is off STOP: growth.py takes in heartside's new VOICE and DOG_VOICE, and sync reads rules as current. A private sound board holds second-by-second scripts for all 10, three voice takes per character (18 takes, 14.4 Higgsfield credits, reserved and settled), licensed music candidates, and a rough F01 sound sketch. The funny bar is in docs/briefs/2026-11-02-funny-bar.md. (2026-11-02)
- Sound is locked for nine of ten concepts. F01's ending is remixed so the music dips under the wink and the sprinkle and fades out. It waits on Krish's one vote on the round-6 board. ElevenLabs: 12,507 of 20,000 booked. Higgsfield: 2,368 credits free for key frames. (2026-11-02)
- Sound is locked for seven of the ten concepts (F03, F04, F06, F07, F10, F11, F12). Round 5 holds the final three: the remixed F01 (crescendo under the voice, soft chime), F02 with Krish's laptop line over Monsieur Cat Walk, and a theatrical American judge for F05. ElevenLabs: 12,507 of 20,000 booked, 7,493 left. (2026-11-02)
- Sound is locked for F03, F04, F07, F11 and F12. Round 4 holds the last four open items: the finished F01 sound (the saved Heartside dachshund in Mix B), F02 with its connecting line and three new tracks, an American judge for F05, and the F10 chat with Krish's jokes. ElevenLabs: 10,287 of the 20,000-character share is booked, 9,713 remain, and about 2,000 more finishes everything. (2026-11-02)
- Krish's round-2 sound votes are in. Voices are locked for F02, F03, F04, F07 and F12, and music for all 10 approved concepts. The round-3 board holds a redesigned cartoon dachshund (3 options), two F01 mixes with the crescendo and the wink, rewritten F02, F05, F10 and F11 scripts, and 12 directed reads with his chosen voices. About 8,100 of the 20,000 ElevenLabs characters are used, all reserved and settled. (2026-11-02)
- All nine posts rebuilt to Krish's notes, and every one passes the media gates: - no badges, and no slogans or URLs on screen; - mugs and scenes move with their real pixels intact; - text wraps evenly with no lone words; - the search bar is fixed, and every search has an answer; - the roasts use new music; - his board rewrites are in the joke bank. (2026-11-02)
- The lock system is built and tested: approved joke bank with breed tags and hashed wording, checksummed render catalog, fingerprinted locks, copy, breed, media and drift gates, an independent reviewer with a standing checklist, and a 5-then-1-in-10 trust ramp. All nine finished posts (F10, F11, F06 x3, F07, F12, F03, F05) build from specs through it; the reviewer held F05 twice and both catches were fixed. (2026-11-02)
- Krish found the wave-1 animatics not funny enough. F01, F02 and F04 are rewritten in four comic modes (12 scripts, a laugh every 3 to 4 seconds, joke maps, copy checks clean) on his round-8 humour board. Nothing is spent until he picks. The Codex lane is in the repo and waits for him to add it to codex-lanes.json. (2026-11-02)
- Reset to finished posts after Krish got lost in the boards of parts. F10, F11 and F06 (three breeds, carousel plus reel each) are finished in code with the locked music, copy checks clean, and they sit on one private status page with all ten concepts. F07, F12, F03 and F05 are next, then F01, F04 and F02 with the humour picks made by the session. (2026-11-02)
- The sound board now has 3 ElevenLabs-designed voices per character (narrator, dachshund, golden, shepherd, doodle, chihuahua) beside the Higgsfield presets, plus an F01 sketch on the designed dachshund voice. About 3,700 of the 20,000-character ElevenLabs share is used, reserved and settled. Krish has not voted yet. (2026-11-02)
- 48 divergent ideas (16 funny, 16 warm, 16 pure heart) under the approved platform "Your dog loves you too. Here's the proof." are in docs/briefs/2026-11-01-ideas.json and on Krish's private voting board; every public line passes heartside's voice checks. The sync at heartside 93780ae says STOP because VOICE and DOG_VOICE in n8n/build.mjs changed, so no pack passes until growth.py takes them in. (2026-11-01)
- The seven channel tasks run inside the radar, daily pack, store and report jobs, mapped by crew/registry.json and checked by growth.py --self-test. Nothing posts. (2026-10-30)
- Krish approved all 24 breed examples and 6 bundle shots, regenerated from heartside's painter v15 (merged to heartside's release branch in PR #79), each with cutout, crops and studio, home and hand mockups; the ledger records every approved painting's sha256 and exact prompt, the old set is superseded, and the shared Drive folder mirrors it. The engine now has real product imagery on all three gifts for its first concepts. (2026-10-30)
- Heartside's prepaid credits are spent by a daily scheduled session (`docs/CREDITS-SESSION.md`) that reserves and settles each generation through Control Center, on protocol 1.16.0 (prepaid credits, `docs/control-center/`; walls in `docs/CONTROL-CENTER-BRIEF.md`). The runner reports credits_spent only for a spend of its own. (2026-10-29)
- Eight scheduled jobs in `automations.json` (sync, numbers, radar, the daily pack, creators, the weekly Answers drafts, store and search, the weekly report), executed on GitHub Actions by `.github/workflows/engine.yml` (`AGENTS.md`, "The schedule").
- The Control Center loop on protocol 1.2.0: a daily directive, one report, Krish's decisions read back by digest (`docs/control-center/ENGINE-PROTOCOL.md`; `b1a14af`). The first live run, on 19 Oct, succeeded (`docs/GET-GOING.md`).
- Answers batch 1 published on heartside, and updated on 22 Oct to quote the new dog voice (`d664d54`, `68940b1`).
- Paid external generation stays off with a zero default budget; since 22 Oct, generation inside prepaid credits within a weekly allocation Krish approved counts as authorised (`0303ffb`; `docs/PROVIDERS.md`).

Waiting or not measured:

- The last live report in the repo (19 Oct) was held: `net_sales_usd` was stale because imported Shopify reports stop at 16 Oct, `organic_orders` is not measured, and conversion editions waited for the V3 homepage (`docs/GET-GOING.md`, "This engine"). Heartside's chat homepage went public on 19 Oct (heartside `9ea7e34`); whether the hold has released is not recorded here.

## What changed recently

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
- 2026-11-02 posts carry line ids only, never free text; a line Krish has not approved, or one edited after he approved it, cannot reach a post (Krish, 2 Nov).
- 2026-11-02 the funny bar now asks for a laugh every 3 to 4 seconds, a picture that is funny muted, and four comic modes in rotation (Krish, 2 Nov).
- 2026-11-02 no more voting boards; Krish sees only finished posts and one status page (Krish, 2 Nov).
- 2026-11-02 Krish unlocked the ElevenLabs share and set connector use to always approve (2 Nov). The walls on posting, sending and new money are unchanged.
- 2026-11-01 Krish approved the platform, ruled that all three tones run in rotation at once ("we dont have enough time to test and learn"), and confirmed 3 Dec 11:59 pm ET as the order-by line for the $12 printed Christmas card only (Rulings, Krish, 2026-11-01).
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

- Next (2026-11-03): Put the first owned, approved single-image creative through the library lane and verify its schedule rows before measuring sends and visits separately.
- **Waiting on Krish:** set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Steps 2 and 3 of `docs/GET-GOING.md` may need a credential only Krish can add for a daily Shopify import; the step says to report a hold naming the secret.
- North Star check (2026-11-03): holds.

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
