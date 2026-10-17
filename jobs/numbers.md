# Job: numbers (every day)

Kind `numbers`. Part 7 in `PLAYBOOK.md`. No drafts: one row per place in
`numbers`. Time for Krish: one minute to read the headline.

1. `python3 growth.py sync`. Use the `heartside_sha` it prints.
2. Prefer connected Shopify aggregate reporting after verifying Heartside
   and its IANA reporting timezone. Follow `docs/ENGINE.md` to save actual
   structured results under `local/metrics/` and run `growth.py metrics
   import <file>`. Never read customer records. End dates in imports are
   exclusive. Reimports replace a window rather than counting it again.

   New York job times do not change a source's reporting timezone. Name
   the actual date window and zone; never relabel a store day as New York.
   For other sources, use the signed-in browser (`BROWSER.md`; reports
   only), reading yesterday in the source's reported timezone. Record it.
   Write down only what each
   page shows:

   | `platform` | Fields to fill, when shown |
   |---|---|
   | `shopify` | `orders`, `net_sales`, `aov`, `sessions`, `add_to_cart`, `checkouts`, `multi_gift_orders`, `waiting_check` |
   | `instagram` | `followers`, `reach`, `sends`, `saves`, `profile_visits`, `link_taps` |
   | `facebook` | `followers`, `reach`, `shares`, `link_clicks` |
   | `tiktok` | `followers`, `views`, `profile_views` |
   | `pinterest` | `impressions`, `saves`, `outbound_clicks` |
   | `google` | `clicks`, `disapproved` |
   | `chat` | `calls`, `fallbacks` (the n8n table "Heartside AI calls") |

   Each row's `note` says where you read it, plus the top source or the top
   creative id. Shopify's note gives the top three utm_content values with
   orders or sessions. Leave a field out, or set it to `null`, when the page
   doesn't show it. Never estimate.

   With neither connected reports nor signed-in analytics, read these public pages and say so in each
   `note`:
   - https://www.instagram.com/yourdoghasnotes
   - https://www.facebook.com/yourdoghasnotes
   - https://www.tiktok.com/@yourdoghasnotes

   Shopify has no public numbers. If its connector and dashboard are both
   unavailable, write nulls and name the missing source. Missing data must
   not erase previous observations in the ledger.
3. Also retrieve a current month-to-date aggregate to capture late refunds
   and corrections within earlier days. Import that complete window.
   Read Shopify totals with `growth.py metrics report` using explicit
   start, exclusive end and timezone. Check covered days and provenance;
   never add overlapping windows or raw daily packs to those totals.
   Other source observations remain in the earlier numbers packs
   (`python3 growth.py read --days 31 --kind numbers`). Compare with the
   canon's checkpoints (`docs/POSITIONING.md` section 6, read in the sync):
   orders against 15 by 1 Nov, 80 by 22 Nov and 220 by 10 Dec, and the month
   against $10,000.
4. Headline: the one change that matters, in plain words, for example "3
   orders yesterday ($131), 9 so far against 15 by 1 Nov; top creative
   IG_EMO_REEL_C02". Check, then post.
