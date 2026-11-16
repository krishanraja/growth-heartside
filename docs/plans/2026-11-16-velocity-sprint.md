# Velocity sprint, 16 to 22 Nov 2026

Krish, 16 Nov: "the main priority as you know is getting more, better posts out with more velocity and using all strategies possible to have them gain massive exposure and get traffic to heartside.io - commenting on posts can happen in the background".

North Star part this moves: organic posts that reach new US dog owners and send them to heartside.io (link taps and sessions by `utm_content`), the leading signals before `organic_net_sales_usd`.

## Re-weighted, 16 Nov afternoon: reach, click path and landing come before volume

Live Shopify readings for the last 30 days, taken on 16 Nov:
- Organic posts sent about 10 visits.
- Social sent 541 sessions, which arrived in two bursts that look paid: 116 on 6 to 7 Nov and 414 on 11 to 13 Nov.
- Those 541 sessions produced 1 cart add (Instagram). Facebook's 470 sessions produced none.

Krish asked "what do we need to be doing 10x better", then "Do the rest, anything is on the table". The order of work is now:

1. **Landing.** The heartside site gets a social landing route that continues the post the visitor came from. In the same work, testimonials that can't be verified and the EXAMPLE badges come off. This is built in the heartside repository and needs Krish's approval before it goes live. Until it lands, every link points to the product page the post shows, never to the homepage.
2. **A click path on every channel.**
   - Daily Stories with link stickers.
   - Pins that link straight to product pages.
   - An Instagram bio link to the page for the latest post.
   - TikTok business verification for a website link. It waits on Krish: which legal entity, and the documents.
3. **Product first.** Gift-led posts show the real product in frame 1 or by second 2, with a reason to tap (wave 4). The alibi films stay as the reach play.
4. **Borrowed reach.** Paid shoutouts and collab posts on large US dog accounts, Trial Reels, and boosts only for posts that have already proved themselves organically. The costed options are in `docs/audits/2026-11-16-borrowed-reach.md`. Every spend needs Krish's yes. Paid reach breaks the North Star's "$0 of paid ads" condition, so any order it brings is reported apart from organic.
5. **Volume.** Volume stays at 20 a day, but only once items 1 to 3 are in place for those posts.

## Output target

- **Daily volume:** 20 posts a day, 5 per platform.
  - About 5 unique films each day, each going to TikTok, Instagram and Facebook: 15 posts.
  - 5 Pins.
- **Over 7 days:** about 35 films and 35 Pins.
- **Judged and ready so far:** 20 films and 4 stills have cleared the independent tier-2 judge at 9 or above. The remaining roughly 15 films come from waves 3 and up, which are written and judged continuously.
- **The bar is unchanged:** a script reaches generation only at 9 or above, and a finished piece reaches Krish only at 9 or above.

## Production line

1. **Generation (Codex studio thread).** Higgsfield web, unlimited only. The Generate control must read "Unlimited" before anything is pressed.
   - Kling 3 runs until it expires on 17 Nov. For speed, it runs the most parallel jobs it can and uses text-to-video wherever a start frame slows a shot down.
   - Clips at 1088x1904 are conformed to 1080x1920 in assembly. They are not a reason to pause generation.
   - After 17 Nov, Kling 2.5 Turbo Unlimited takes over.
   - Stills run on Nano Banana and Seedream Unlimited.
2. **Writing and judging.** A writer agent drafts each wave. A separate judge agent scores it without seeing the writer's scores. Only 9s are queued.
3. **Assembly (Claude, heavy renders on the worker).**
   - Labels in the fixed band.
   - The store render as the end card.
   - Captions in the audit's pattern.
   - A tracked link per creative.
   - `growth.py check` and a panel pass at full size.
4. **Review.** Each day's 20 go on the review board by 07:00 London. One yes from Krish covers the batch.
5. **Publishing desk.** It schedules exactly the approved batch into Buffer at the US Eastern slots (08:00, 12:30 and 18:00), TikTok first, Instagram 5 minutes later, Facebook 10 minutes later. It then records a `post_check` for each post and reads results at 24 hours, 72 hours and 7 days.

## Exposure levers, in order of expected traffic

| # | Lever | Status |
|---|---|---|
| 1 | IG and FB Stories every day, with a link sticker to the matching product on heartside.io. Every film's product end card also becomes a Story | Approved, Krish 16 Nov ("Yes, all three") |
| 2 | Instagram Trial Reels for every alibi film (shown to non-followers first) | Approved, Krish 16 Nov ("Yes, all three") |
| 3 | Trending in-app sounds on TikTok and Reels, added by the Publishing desk when it posts natively, since Buffer can't attach sounds | Approved, Krish 16 Nov ("Yes, all three") |
| 4 | 5 Pins a day, each linking straight to its product page with UTMs | Inside the daily batch |
| 5 | Double down: a post above 3x its channel median at 24 hours gets 2 new variants the next day (Sprint 120's rule, brought forward from 72 hours) | Engine rule |
| 6 | Link-click boosts to heartside.io, only on posts that beat 3x the median organically | Needs Krish's yes for each boost (`docs/PAID-BOOSTS.md`) |
| 7 | Comments on high-reach dog posts, run in the background | Comments desk drafts in Krish's voice, from the 11 Nov calibration and the Comment Intelligence tab. Each batch is posted only after his yes |
| 8 | Christmas urgency: signature films end on the product and the order-by date, wherever the date is confirmed for that product | Inside the daily batch |

## Measurement

- Every post carries a creative id and a tracked heartside.io link.
- Each morning, the board leads with yesterday's link taps and sessions by `utm_content`, and the 3x-median winners.
- A number Buffer does not show is "not shown", never zero.

## Known blocker

Claude drives the Codex Desktop window with computer use. The window must be on screen and the PC unlocked. While the PC is locked, threads finish the turn they are on but cannot be steered.
