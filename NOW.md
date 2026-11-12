---
repo: krishanraja/growth-heartside
product: Heartside growth engine
as_of: 2026-11-12
head: 6906156
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

## Where it is right now (as of 2026-11-12)

<!-- north-star-state {"week_of": "2026-11-09", "week_target": 1417, "current": 0, "current_as_of": "2026-11-12", "current_source": "Shopify Admin API orders through growth.py attribution (read-only app), organic posts, trailing 28 days", "urgency": 5, "urgency_reason": "under 40% of the week's target two weeks running (0% now)"} --> **North Star number: U5, stalled.** Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them: $0 (measured 12 Nov by the engine's own attribution read; the store's one order in the window, $45, came direct), against $1,417 this week, on the way to $50,000 by 28 December 2026. Everything else pauses unless it moves the number.

**Off STOP since 29 Oct.** The rule checks are rebuilt on heartside's current sources at `54b6b0e` (NORTH_STAR's number, SCOPE's non-negotiables, ECONOMICS's 26 Oct ruling, NOW's never-publish list, and Buddy's and the gift lines' voice in `n8n/build.mjs`), and `python3 growth.py sync` reads rules as current. The live catalog binds the blanket ($129), the portrait ($59 or $119), the mug ($45) and the $29 Artist's touch at canon prices (`python3 growth.py readiness`, 29 Oct). The seven campaigns render from the live store's own gallery pictures, unaltered and with no label (Krish, 2 Nov), re-pinned on 12 Nov after heartside rebuilt its galleries; none uses Biscuit. The organic share is measured by the engine's own attribution read (`growth.py attribution`) and reported to Control Center as `organic_net_sales_usd` from 12 Nov.

Lifecycle: live. The engine is merged and active on `main` (`docs/HANDOFF.md`). The hourly sync with heartside, the Control Center directive at 05:10 UTC and `check` run green; the draft engine's day pack failed every day from 30 Oct to 12 Nov, because the product renders it pinned on 29 Oct had left the live galleries, and renders again from the 12 Nov re-pin (GitHub Actions readback and local renders for 12 to 18 Nov, 12 Nov).

Live:

- the Control Center loop speaks protocol 1.20.0 where Control Center serves it: it acks Krish's instruction (krish_instruction) as received by id only, first in its activity, and reports priorities, obsessions and next_steps from this repository's own files; every wake's run id carries its GitHub run id, so a second wake the same day is its own report. (2026-11-11)
- Krish posts every commercial-song TikTok (F28, F40, F42, F43, F41, F44, F38 repost) from his phone; README v5.9 tells Codex so, and Sheet 04, Doc 04a and the Phone Posts page are rebuilt from live 02r with London times. (2026-11-11)
- Krish's phone posts have a one-tap Copy caption page (claude.ai/artifact/3aFjdFNWvHEeMJCKVDERSu) and Doc 04a now has real hyperlinks; the page's source is factory/schedule/phone-posts.html. (2026-11-11)
- 02t is approved by Krish (M2:M46 yes), so Codex posts the 15 photo reels with music from 13 Nov; F38 v4 is queued at the bottom of Sheet 04 and Doc 04a as Krish's own repost on Wed 18 Nov (TikTok 18:00, Instagram 18:05, Facebook 18:10 ET, new tracked link FB_ENT_REEL_C150_H01_V4_20261118). (2026-11-11)
- Sheet 04 and Doc 04a now carry F28 as the beagle howl v2, with the new caption and the falsetto sync at 2.7 s, for Krish's 08:05 and 08:10 ET posts today. (2026-11-11)
- Krish approved D as the official Heartside icon. The unchanged raster master, favicon/app exports and ZIP are ready in docs/brand/. Official avatars and conversion bios are live and read back on Instagram, Facebook, TikTok and Pinterest; Facebook cover is replaced. Website implementation is Krish's. (2026-11-10)
- Eight scheduled jobs in `automations.json` run on GitHub Actions (`.github/workflows/engine.yml`); Control Center protocol 1.20.0; paid external generation stays off with a zero default budget (`docs/CREDITS-SESSION.md`, `docs/PROVIDERS.md`).

Waiting or not measured:

- The 12 Nov live report (05:11 UTC) was held: `net_sales_usd` is missing because no imported Shopify window covers this London month (`docs/GET-GOING.md`, step 2), `organic_orders` read 0, and conversion editions were held only because the homepage check read the 19 Oct chat's marker, not the journey homepage public since 29 Oct (heartside `3df57cc`). That check is fixed (12 Nov), so the next report releases the hold and also carries `organic_net_sales_usd`.

## What changed recently

- 2026-11-11 Krish asked that every growth engine's priorities, obsessions and next steps feed Control Center live and that he can instruct each engine ("Get building", 11 Nov); his words never leave engine/engine_state.py.
- 2026-11-11 Krish found TikTok's commercial songs can only be added in the phone app.
- 2026-11-11 Krish found copying captions from the Doc into Instagram fiddly.
- 2026-11-10 The first 127-character Instagram candidate hid its CTA behind more despite fitting the editor limit. The shorter version passed public readback; the profile-audit acceptance now checks native truncation as well as character count. No website, post, spend or account-type change.
- 2026-11-10 TikTok's username, caption and stickers start about y 1340, so the y 1450 label spot only worked on Instagram; the chat floor in factory/ui_layout.py moved from 1480 to 1250.
- 2026-11-10 the library lane filed the v2 cuts into new F38-real and F41-real folders because the manifest named the post F38-real; the manifest post must match the existing Posts folder.
- 2026-11-10 AGENTS points to the official assets. Profile review history, exact approval, asset hashes, live readbacks and link-feature limits are recorded in docs/profile-pages/2026-11-10/ROLLOUT.md. Facebook Learn more retains the verified tracked destination; Buy now would require a new store integration.
- 2026-11-10 Krish found F38 labels under Instagram's caption area, so labels now sit in one fixed, visible place.
- 2026-11-10 the judge loop stopped converging, so Krish's board decides the scripts at 8 rather than more rounds.
- 2026-11-10 v5.1 wrongly sent Instagram and Facebook songs to Meta Business Suite; Krish ruled "I add songs on my phone".
- 2026-11-10 dog reels now need real-looking scruffy pets and motion in every beat. Credit spend needs a 9 on the script first. Krish overrode the Runway share cap for these remakes.
- 2026-11-10 02r replaces 02q; F30 becomes F30-pepper (Krish's board Yes); F38 and F41 post as the real-dog remakes.

## What is next and what is waiting on Krish

- Next (2026-11-11): the daily report run acts on no words, so an instruction stays received until a working session takes it up; Krish decides how a session reads the open instruction.
- **Waiting on Krish:** set the three Heartside Buffer channels to New York time with US morning, lunch and evening slots (Buffer's tools here cannot change channel settings). a heartside build session for shoppable product tags (`docs/briefs/2026-10-29-heartside-shopping-tags.md`). Rule on the US groomer list. Every post, send and spend still needs his yes at that moment.
- **Still to rewrite:** `PLAYBOOK.md` and `STRATEGY.md` carry a 29 Oct banner saying heartside's canon wins; their Biscuit-era passages are rewritten in the docs pass.
- **Rule on the media brief's creative direction before it is proposed.** `docs/briefs/2026-10-22-media-credits.md` asks for "your dog's performance review" stills "in the V2 voice" and a "$12 product" in which "the dog reads your review". Heartside's V3 retired the HR review builder and the poster range (heartside `docs/V3-GIFTS-FROM-YOUR-DOG.md`), and heartside's canon beats this repository (`AGENTS.md`, rule 2).
- Step 2 of `docs/GET-GOING.md` (a daily Shopify sales import, so `net_sales_usd` is measured) may need a credential only Krish can add; the step says to report a hold naming the secret.
- North Star check (2026-11-12): holds.

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
