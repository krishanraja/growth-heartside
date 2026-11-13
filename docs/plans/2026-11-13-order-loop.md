# The Order Loop: first stranger sale, then pour (13 November 2026)

**$0 of $1,417, U5, short by $1,417.** The store-wide number is $45 of $1,084. Next week's rung is $4,862.

Krish approved this plan as the build on 13 November 2026. It aims at both halves of `docs/NORTH_STAR.md`:
organic net sales over the trailing four weeks, and every winning format found by this engine and approved by
him in one press. Nothing posts, sends or spends without his yes; urgency never widens authority.

## What is true today

- The scheduled day pack has never shipped a post. The 55 live placements average 56 views each.
- The viral lane earns $0 by construction: no product on screen, link in bio only (`sprint-120.md`).
- No stranger order is on record. Payments have had no readback since the 28 October mock orders (heartside
  `NOW.md`), so nobody has confirmed the till takes money.
- TikTok has no clickable link and no code is live, so a TikTok-driven order lands in `direct`, uncounted.

## The model, and why there is no 100x in dollars

Counted organic dollars a week = buy placements x views x US share x link taps per view x stranger
conversion x counted share x basket x Christmas factor. Today's upper bound is about $0.50 a week.

| Ladder date | 16 Nov | 23 Nov | 30 Nov | 7 Dec | 14 Dec | 21 Dec | 28 Dec |
|---|---|---|---|---|---|---|---|
| Target | $4,862 | $7,782 | $11,906 | $17,626 | $25,436 | $35,966 | $50,000 |
| Base (tap rate 0.33%, conversion 1%, $45) | $0 | $0.37 | $2 | $5 | $7 | $8 | $8 |
| Breakout plus late gift (1%, 2%, $85) | $0 | $7 | $74 | $312 | $562 | $804 | $838 |

$50,000 needs roughly 44,000 to 600,000 views per buy placement; today's average is 56. Only a borrowed
audience closes that, which is why ruling 11 (creators, by rule) is the lever as large as the gap.

**Reconciliation finding.** The $50,000 came from Sprint 120's plan, where it is net operating profit from
orders placed by 4 December and includes about $13,500 from paid orders (`sprint-120.md`). As this engine's
number it became organic net sales, paid excluded: 5.4 times the store's own 28 December rung. The 28
December trailing window (30 November to 27 December) also drops Black Friday. Krish said on 10 November, "I'm
not accepting moving from 50,000 to 5.9K", so the weekly question leads with plan changes, never a lower
number first.

## What was built (branch `claude/sharp-knuth-2qb0jp`, local until push access is added)

1. **The claims gate** (`growth.py`): no words on a gift, no handmade, no uninspected quality, no delivery
   promise, no deal wording without a live offer. It found the false printed-note claim in four live day-pack
   captions and hooks, now corrected to "the note comes in the box".
2. **Money** (`engine/attribution.py`, `engine/protocol.py`): `net_sales_usd` is measured from the runner's own
   read through a London-month window (GET-GOING Step 2 replaced, no new credential); an untagged Meta visit is
   `unverified`, never organic, until the ads questions are answered; the read runs every six-hour tick.
3. **The decision core** (`factory/loop.py`, `LOOP.md`): like-with-like ranking on fields each platform shows,
   winners only after two matched variants, orders gate and never rank, the reader is never the maker.

Stop rule: if the loop is not running by 20 November, stop coding and run manual Day-0 reads weekly.

## Day 0, read only (in the first session Krish starts)

T0 payments and the last paid checkout; T2 audience country per platform; the store funnel since 27 October;
the F10 pilot readback; Buffer per-post readings of the 55 placements; Printful's 2026 cut-off. Then section 2's
table is re-run per platform and lane on these readings.

## Answered on 13 November

Krish: "1. yes. 2. it does. 3. yes. 4. ask growth repo. 5. yes". The till takes money (his word); the buy lane takes
at least two thirds of slots from 21 November; the ads questions are answered from this repository's record (no
Meta ad runs now, the one pilot was tagged paid); the target stays at $50,000 with borrowed audiences backed. The
day-pack freeze and the six-hourly runner were not asked and still wait. Next to ask: creators by rule (ruling 11).

## The rulings, in order (board items; one Yes or No each)

0. **T0, the till** (a heartside-owned hold): a readback that Shopify Payments takes a real paid checkout.
1. **L1, the buy lane:** from 21 November at least two thirds of slots end on the real product with a counted
   path, led by the blanket, the portrait and bundles; freeze the day pack, radar, creators and store jobs;
   `engine.yml` every six hours; stop filling Sprint 120's reserved slots ahead of evidence.
2. **The ads questions:** are Meta ads running for Heartside now; does every ad link carry
   `utm_medium=paid_social`; and does no boosted Facebook post carry an engine link in its caption? (A boost
   reuses the post's link, so its paid clicks arrive with the engine's organic tags.)
3. **The waiting codes item, amended in place:** family codes on buy rows, aimed at the most-US platform, with
   the bio-link page and the counts-only thank-you survey restored.
4. **"Link in bio" on TikTok:** hold and re-approve the 02t TikTok rows and phone posts that say it.
5. **Unattended reading:** a read-only Buffer key added to `engine.yml` secrets, so the runner reads and ranks.
6. **Caps after 20 November** (default five a day per platform). 7. **The AI label**, with the policy read live.
8. **In-app commercial songs on a business account**, with the policy read live, before T9 scales.
9. **Pinterest as a posting channel.** 10. **Waiting since 29 October:** shoppable product tags, the Buffer
   channels on New York time, and the US groomer list.
11. **Creators, by rule:** a measurable "success" that restarts creators automatically, for example the first
    replicated buy-lane winner plus a T4 interval above a threshold Krish sets.
12. **The weekly U5 plan-or-target question,** with the reconciliation finding above.
13. Later: A5 the late gift from 5 December; A4 the Real Reveal after a likeness pass on his own dog.

## Test cards (read by the reader, never the maker)

| Card | Kill | Graduate |
|---|---|---|
| T0 the till takes money (Day 0) | unverified: nothing scales | verified: proceed |
| T1 buy-lane response, 14 days, 40 or more placements | below 1.5x on two of three platforms with no replicated winner: 80% explore | a replicated winner: 70/20/10 |
| T2 US share, Day 0 then weekly | 60% or more US everywhere: drop the card | under 50%: cap that platform at 3 a day; TikTok under 30% leaves the number's allocation |
| T3 codes count TikTok, 14 days | 0 code orders with 3 or more direct orders on TikTok days: short-path brief | 1 or more code orders: codes on every buy row |
| T4 strangers buy (verdict Friday 27 November, as an interval) | 300 or more sessions with an upper bound below 1%: no volume ask | 3 or more orders in 300 sessions or fewer |
| T6 volume step (each step an ask) | median falls 50% or more for 3 days | within 25%: propose the next step |
| T7 panel against Krish's Yes, 20 items | agreement below 0.7 | 0.85 or more: spot checks 1 in 10 |
| T8 late gift | 0 orders on 300 or more visits by 8 December | 40% or more of the pre-cut-off rate |
| T9 phone songs | under 1.5x: winners only | 2x or more: up to 3 a day |
| T10 Pinterest | below Facebook's buy-lane rate | at or above it: keep to 24 December |

## The three U5 recovery plays

1. **Krish's warm post** linking heartside.io with an engine-tagged link (his call: it mixes his professional
   brand with a gift business).
2. **A zero-credit Pinterest gift-search lane** from approved buy stills (needs ruling 9).
3. **The Real Reveal:** the live store painting his own dog, after the likeness pass and A4.

## What we stop doing at U5

The day pack and three jobs (on L1); counting the viral lane or ranking money on views; "Link in bio" on
TikTok; crediting New York slots with US share; filling reserved slots ahead of evidence; treating judge
scores as results; writing asks in Krish's voice.
