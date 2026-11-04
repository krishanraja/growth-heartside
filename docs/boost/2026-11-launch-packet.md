# Launch packet: Heartside boost test, November 2026

This is the exact thing Krish says go on (`docs/PAID-BOOSTS.md`). Codex builds it as drafts, fills in the **To fill** column, and then waits. It publishes only after Krish's go on this packet with the blanks filled.

## Decision for this test

Krish approved 36 organic placements on 4 November. Paid activation is pending. Allocate $50 to each of four existing Instagram posts, $200 total. Keep the remaining $50 out of every ad set. Its use requires a separate decision after the results.

**Proposed timing for one approval.** Review all four eligible live posts and unpublished drafts together on 8 November, after the last Instagram post is live at its approved 14:20 UTC slot. Start each boost approximately 72 hours after its actual organic publication. This changes the original within-24-hours plan and gives each post the same organic observation window. If any post is delayed, blocked or ineligible, revise the dates or omit that arm explicitly before sign-off. The table gives proposed paid starts only; no paid start has been scheduled.

| Instagram post | Approved organic slot (UTC) | Proposed paid start (UTC) | End after five days (UTC) | Maximum spend |
|---|---|---|---|---:|
| F02 Project Nothing · reel | 5 Nov 17:45 | 8 Nov 17:45 | 13 Nov 17:45 | $50 |
| F06-frenchie · carousel | 5 Nov 20:15 | 8 Nov 20:15 | 13 Nov 20:15 | $50 |
| F12 Head of Security · reel | 6 Nov 14:20 | 9 Nov 14:20 | 14 Nov 14:20 | $50 |
| F05 Court of the Couch · reel | 8 Nov 14:20 | 11 Nov 14:20 | 16 Nov 14:20 | $50 |

Record a pre-boost organic baseline immediately before each start. Capture the post ID, reach, saves, shares, profile visits and attributable store visits where available. Keep paid-social traffic and sales separate from the organic North Star.

## The campaign

| Setting | Value |
|---|---|
| Ad account | Heartside's Meta ad account, the one linked to the Heartside Facebook Page and @yourdoghasnotes |
| Campaign name | `hs_boost_202611_test` |
| Objective | Traffic |
| Budget | Set on each ad set, not on the campaign |
| Special ad category | None |

## Ad sets (one per arm, identical except budget timing)

| Setting | Value |
|---|---|
| Name | `hs_boost_202611_<post id>` |
| Performance goal | Maximise landing page views |
| Pixel | The Heartside pixel installed by Shopify's Facebook & Instagram app |
| Proposed hard limit | $50 lifetime per ad set over five days, equivalent to $10/day on average. Read back all four lifetime limits and end times before activation. |
| Schedule | Use the equal-age dates above, subject to approval of this timing change |
| Audience | United States, ages 25 to 64, all genders. Advantage+ audience off. No interests |
| Placements | Manual: Instagram Reels, Instagram Feed, Facebook Reels, Facebook Feed |
| Bid strategy | Highest volume |

## Ads (one per ad set)

| Setting | Value |
|---|---|
| Ad setup | Use existing post |
| Post | The arm's live Instagram post, from @yourdoghasnotes |
| Call to action | Shop now |
| Website URL | Below, exactly |
| Facebook Page | Heartside: Personalized Dog Gifts |
| Labels | Leave Meta's "AI info" label as Meta sets it |

| Arm | Post | Organic slot (UTC) | Website URL | To fill: Instagram permalink, ad ID |
|---|---|---|---|---|
| 1 | F12 head of security | 6 Nov 14:20 | `https://heartside.io/products/your-dogs-portrait?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_ENT_REEL_C112_H01_V1_20261103` | |
| 2 | F05 court of the couch | 8 Nov 14:20 | `https://heartside.io/products/your-dogs-personality-blanket?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_ENT_REEL_C105_H01_V1_20261103` | |
| 3 | F02 project nothing | 5 Nov 17:45 | `https://heartside.io/products/your-dogs-illustrated-mug?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_ENT_REEL_C102_H01_V1_20261103` | |
| 4 | F06-frenchie roast (carousel) | 5 Nov 20:15 | `https://heartside.io/products/your-dogs-illustrated-mug?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_ENT_CAROUSEL_C106_H01_V1_20261103` | |

Total: 4 arms x $10 x 5 days = **$200**. The $50 reserve is not in this packet.

## Gates (every one true before go)

| Gate | Status |
|---|---|
| Music licence | True, permanently (Krish, 4 Nov) |
| Each post is live and is its locked file | Codex fills it in from each permalink |
| Each destination is the product shown, with `paid_social` tracking | Checked 4 Nov. All four tracked links returned HTTP 200 and the expected product title, retaining their paid query parameters. |
| Meta pixel live on heartside.io | Storefront pixel configuration found on all four URLs on 4 Nov. Confirm the selected pixel receives a landing-page event in Meta before launch. |
| Attribution keeps paid out of the North Star | True (`engine/attribution.py`) |
| Meta's AI label not hidden | Codex confirms at draft |
| Account, actual placements and limits | Confirm the Heartside account and currency, existing-post eligibility on each surface, destination, delivery dates, and the $50 lifetime limit in every unpublished draft. |
| Krish's go on this packet | Pending. Present the actual four permalinks, draft IDs, budgets and times together. |

## Kill and readings

- **Day 2:** delivery check.
- **Day 3:** stop any arm whose cost per landing page view is more than twice the best arm's, after 1,000 impressions.
- **Day 5 for each arm:** rank by cost per landing-page view. Report spend, impressions, landing-page views, outbound CTR and add-to-carts alongside the ranking. Include three-second views and ThruPlay for reels only. Record purchases descriptively. If the comparison is too small or there are no meaningful downstream actions, keep the reserve unallocated. Compare all completed five-day windows after the last arm ends.
