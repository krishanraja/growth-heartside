# Paid boosts: the engine's ruling and the rules for any boost

Status: **plan approved** by Krish on 4 Nov 2026 ("Yes to all your 4 questions", answering "Do you approve the $250 Meta-only test, given it trades against the $0-paid North Star?"). He had asked: "Ideally I'll put some paid boosts behind these but need your ruling first."

What his yes covers, and what it does not:
- **It covers** the test as designed below: Meta only, a $250 cap including the $90 already approved for F12, the arms, the gates and the kill rule. Codex may build the paid cuts and the launch plan.
- **It does not** launch anything. Under AGENTS.md "Autonomy", an approved plan never authorises going live. The launch is a separate go-live: the exact files (by SHA-256), budget, dates and audience go to Krish with every gate below shown as true. He presses it, and Codex launches exactly that, once.

## The ruling

**Yes, a small, capped, Meta-only creative test. Not boosts of the organic posts as they stand, and not yet on TikTok.** Its only job is to tell us, within a week instead of a month, which concepts and hooks to make more of organically.

Why yes:
- The accounts are cold. On 3 Nov F10 drew 26 TikTok views and 2 on Facebook. At that reach, organic posting produces no usable signal on hooks or click-through for weeks.
- $150 to $250 on Meta buys a few thousand impressions per creative. That is enough to compare 3-second hold, thumbstop and outbound click rates between concepts. That information is what moves the North Star, because it shows the engine which formats to scale for free.

Why small, and why only as a test:
- **The North Star counts organic sales "with $0 of paid ads behind them", and its goal is that organic sells more than paid ads ever have.**
  - Any sale through a boosted post is excluded from the number.
  - Every paid sale raises the bar organic has to beat.
  - A big paid push therefore works against the target Krish set.
- At $10 a day per creative, purchases will be too few to judge. Treat any sale as a bonus, never as the test's verdict.

Why not now, as the posts stand: the creative audit (`docs/audits/2026-11-04-creative-audit.md`) found that no asset is paid-ready.
- Subtitles sit in Meta's no-text zone.
- There is no CTA end card.
- F10 opens on a blank screen.

Boosting those would buy a measurement of the flaws.

Why not TikTok yet: the profile has no clickable website link (Codex audit, 3 Nov).
## Hard gates before any money moves

Every gate must be true and written down in the boost manifest (`docs/BOOST-LIBRARY.md`).

1. **Music: closed, permanently.** Ruling (Krish, 2026-11-04): "Just use the music. I have the right license for the post type. Mark this as complete permanently." The locked track is used in paid cuts as it is. This gate is always `true` and is never raised again in an audit, plan or check.
2. **A paid cut that is a separate creative.** It is never the organic file. It must have:
   - subtitles at `cap_y` ≤ 1150 (out of Meta's bottom 35%), with the top 14% and the sides 6% clear;
   - a 3 s end card showing the real store render for the same dog and the product's name;
   - a running time of 15 to 30 s;
   - audit evidence from `factory/audit.py` and its own approval from Krish (organic approval never carries over, `docs/CHANNEL-TASKS.md`).
3. **The destination is the product shown,** for example the mug page for a mug ending. It is a heartside.io link with `utm_medium=paid_social` and `utm_campaign=hs_boost_<yyyymm>`, never the organic UTM.
4. **Attribution kept apart.** `growth.py attribution` and the Sunday report count paid sessions and orders separately. Those orders never enter the North Star number.
5. **AI labelling** is switched on wherever the platform requires it.
6. **A named spend.** Krish approves the exact campaign, budget, dates and creatives immediately before launch. The engine never spends (AGENTS.md rule 1), and Codex launches only with that approval in hand.

## The first test (proposed)

- **Total cap: $250 including the $90 already approved for F12.** Meta only (Facebook and Instagram Reels placements), US, adults 25 to 64. Advantage+ audience is off for the test so every arm sees the same audience.
- **Arms**, each at $10 a day for 5 days ($50 an arm), all ending on the real store render for their own dog:

| Arm | Creative | Why it is in the test |
|---|---|---|
| A | F12 guard-first (Krish approved the opening on 4 Nov) | Already approved, at $45 an arm in the $90 plan |
| B | F12 parcel-first (control) | Already approved, as part of the same $90 |
| C | F06-frenchie paid cut with the Runway opener | The best scoring roast; frenchie mug render for a frenchie |
| D | F02 or F01 paid cut | The strongest covers in the set; included only once Codex's full-rate check passes |

- **What is read, against its denominator:**
  - 3-second view rate (thumbstop);
  - ThruPlay rate;
  - outbound click-through;
  - cost per landing-page view;
  - add-to-cart.
- **Reading times:** after day 2 (delivery check only) and day 5. Purchases are reported but not used to judge.
- **Kill rule:** an arm is stopped on day 3 if its thumbstop is under half the best arm's after 1,000 impressions.
- **The decision:**
  - The winning hook and concept get 3 new organic breed variants through the factory.
  - The loser's opener is rebuilt.
  - Nothing is scaled until organic posts using the winning format have run for a week.

## What the engine will and will not do

- **It will:** prepare the paid cut specs, the manifest rows, the UTMs and the Codex card, and read the results in the Sunday report.
- **It will not:** create campaigns, change budgets, boost a post, or touch Ads Manager. No document, page or plan approval authorises spend. Only Krish's named yes does, immediately before the charge.

## Sources (read 4 Nov 2026)

- Meta Reels ad safe zone (14% top, 35% bottom, 6% sides, as widely cited; confirm with the Ads Manager guardrail): <https://adkit.so/tools/safe-zones/meta>
- TikTok Spark Ads: <https://ads.tiktok.com/help/article/spark-ads>
