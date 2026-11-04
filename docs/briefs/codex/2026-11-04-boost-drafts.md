# Codex card: build the four boost drafts in Ads Manager

Written on 4 Nov 2026 by the growth engine.

Krish ruled that boosts run the live organic posts: "paid organic boosts, not paid ads", then "Yeah, do it. Get on with it. Make sure everything is perfect and ready to roll ASAP."

Read first:
- `docs/PAID-BOOSTS.md`;
- `docs/boost/2026-11-launch-packet.md`. The packet is the spec: copy every setting exactly.

## Hard lines

- **Drafts only.** Publish nothing, and spend nothing, until Krish says go on the filled packet.
- **Never edit a post, a caption or the Buffer queue.** The boost uses the post exactly as it is live.
- **Ads Manager only**, with "Use existing post". Never the app's Boost button, and never a re-uploaded video.
- **If Ads Manager is unreachable from your tools, stop and say so.** Do not try another route, and do not use the browser on Krish's signed-in accounts. Krish builds the drafts himself from the packet.

## Steps

1. **Check access.** Confirm you can reach Heartside's Meta ad account in Ads Manager, and that the Shopify-installed pixel shows there. If either fails, stop and report it (see the last hard line).
2. **Build each arm's draft when its post is live.** For each arm in the packet, once its Instagram post is live on @yourdoghasnotes:
   - find the post;
   - confirm its media is the locked file (the reel or carousel listed for that post id in `library/manifest.json`);
   - build its campaign, ad set and ad as **drafts**, exactly as the packet says.

   | Arm | Post | Live |
   |---|---|---|
   | 4 | F06-frenchie carousel | today, 17:45 UTC |
   | 3 | F02 | 5 Nov, 20:15 UTC |
   | 1 | F12 | 6 Nov, 17:45 UTC |
   | 2 | F05 | 8 Nov, 14:20 UTC |
3. **Fill the packet.** In the "To fill" column of `docs/boost/2026-11-launch-packet.md`, write each arm's Instagram permalink and draft ad ID. Mark the "post is live and is its locked file" gate and the AI-label gate. Commit it on `claude/runway-motion-batch`.
4. **Report** each arm as it is drafted: its permalink, draft ad ID, and anything that did not match the packet.

## After Krish says go

- Publish exactly the drafts in the packet, once each.
- Report each ad ID and its first delivery status.
- Run the day-3 kill rule only on Krish's word or the engine's reading. Never change a budget on your own.
