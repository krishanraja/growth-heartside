# Paid boosts: the engine's ruling and the rules for any boost

Status: proposed by the growth engine on 4 Nov 2026. Krish's ruling is pending, and nothing is spent until he gives it. He asked: "Ideally I'll put some paid boosts behind these but need your ruling first."

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
- The music licence for ads is unconfirmed.
- F10 opens on a blank screen.

Boosting those would buy a measurement of the flaws.

Why not TikTok yet: the profile has no clickable website link (Codex audit, 3 Nov). Spark Ads also lock the post's music, and paid TikTok use needs a commercial licence for it.

## Hard gates before any money moves

Every gate must be true and written down in the boost manifest (`docs/BOOST-LIBRARY.md`).

1. **Music.** Krish confirms the Epidemic Sound plan covers paid social. Otherwise the paid cut uses music cleared for ads, such as Meta's Sound Collection on Meta. Epidemic's own pages tie paid TikTok use to Commercial or Enterprise plans.
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

- Epidemic Sound on TikTok ads and plans: <https://www.epidemicsound.com/tiktok>
- Meta Reels ad safe zone (14% top, 35% bottom, 6% sides, as widely cited; confirm with the Ads Manager guardrail): <https://adkit.so/tools/safe-zones/meta>
- TikTok Spark Ads: <https://ads.tiktok.com/help/article/spark-ads>
