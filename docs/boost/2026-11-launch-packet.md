# Launch packet: Heartside boost test, November 2026

This is the exact thing Krish says go on (`docs/PAID-BOOSTS.md`). Codex builds it as drafts, fills in the **To fill** column, and then waits. It publishes only after Krish's go on this packet with the blanks filled.

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
| Budget | $10.00 a day |
| Schedule | Starts within 24 hours of the post going live; ends 5 days later |
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

| Arm | Post | Live (UTC) | Website URL | To fill: Instagram permalink, ad ID |
|---|---|---|---|---|
| 1 | F12 head of security | 6 Nov 17:45 | `https://heartside.io/products/your-dogs-portrait?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_ENT_REEL_C112_H01_V1_20261103` | |
| 2 | F05 court of the couch | 8 Nov 14:20 | `https://heartside.io/products/your-dogs-personality-blanket?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_ENT_REEL_C105_H01_V1_20261103` | |
| 3 | F02 project nothing | 5 Nov 20:15 | `https://heartside.io/products/your-dogs-illustrated-mug?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_ENT_REEL_C102_H01_V1_20261103` | |
| 4 | F06-frenchie roast (carousel) | 4 Nov 17:45 | `https://heartside.io/products/your-dogs-illustrated-mug?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=IG_ENT_CAROUSEL_C106_H01_V1_20261103` | |

Total: 4 arms x $10 x 5 days = **$200**. The $50 reserve is not in this packet.

## Gates (every one true before go)

| Gate | Status |
|---|---|
| Music licence | True, permanently (Krish, 4 Nov) |
| Each post is live and is its locked file | Codex fills it in from each permalink |
| Each destination is the product shown, with `paid_social` tracking | True (URLs above, product pages live on 4 Nov) |
| Meta pixel live on heartside.io | True (checked 4 Nov) |
| Attribution keeps paid out of the North Star | True (`engine/attribution.py`) |
| Meta's AI label not hidden | Codex confirms at draft |
| Krish's go on this packet | Pending |

## Kill and readings

- **Day 2:** delivery check.
- **Day 3:** stop any arm whose cost per landing page view is more than twice the best arm's, after 1,000 impressions.
- **Day 5:** the verdict, in the next Sunday report. Purchases are reported but not used to judge.
