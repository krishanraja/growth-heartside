# Paid boosts: boost the live organic posts, through Ads Manager

**Current rule (Krish, 10 Nov 2026, on the review board):** "No, I will approve boosts of up to $20 per day if you can prove to me with organic reach results that they are the right ones to boost". There is no $3,000 tranche. Each boost is proposed on the board one post at a time, at no more than $20 a day, with that post's organic reach results (views, shares and saves against the sprint median, read on the platform) as the proof. Nothing is boosted without his Yes on that item.

**Status:** ruled by Krish on 4 Nov 2026.

His approvals, in order:
1. "Yes to all your 4 questions": approves a $250 Meta-only test.
2. "These are going to be paid organic boosts, not paid ads."
3. "Yeah, do it. Get on with it. Make sure everything is perfect and ready to roll ASAP": answering the engine's recommendation to promote the existing posts from Ads Manager.

What this covers, and what it does not:
- **It covers** the plan below. Codex may prepare the campaign as a draft.
- **It does not** launch anything. Under AGENTS.md "Autonomy", an approved plan never authorises spend. The launch packet (`docs/boost/2026-11-launch-packet.md`) goes to Krish with every gate true. He presses go, and Codex publishes exactly that, once.

## The ruling

**Promote the live organic posts, unchanged, from Meta Ads Manager with "Use existing post". Do not run separate ads, and do not use the app's Boost button.**

Why boosts of the live posts:
- The post is the creative Krish approved. Its likes, comments and shares build on the real post.
- Native-looking posts generally do better for a small brand than polished ads. This is a general pattern, not a promise.

Why Ads Manager and not the Boost button:
- The Boost button mostly buys likes and reach.
- Ads Manager adds:
  - a landing-page-views objective;
  - a "Shop now" button to the exact product page;
  - a paid tracking link;
  - a fixed budget per post;
  - the same audience for every post.
- The auction price is the same either way. What changes the result is the objective and the controls.

Why not separate ads yet:
- Optimising for purchases needs about 50 purchases a week, which $250 cannot feed.
- Build one proper ad only after a boosted post clearly wins on taps and add-to-cart.

Why not TikTok yet: Spark Ads (TikTok's boost of an existing post) can follow, once a Meta winner exists.

**The North Star trade-off still applies:**
- Sales from boosted traffic never count in the $0-paid number (`engine/attribution.py`: `utm_medium=paid_social` is always paid).
- Every paid sale raises the bar organic has to beat.

That is why the test stays at $250.

## Gates before money moves

- **Hold Meta visits as unverified for the boost's window** (`META_UNVERIFIED = True` in `engine/attribution.py`), set in the same change that records Krish's yes to the boost, and back to False after its end. A boost reuses the post's own link, so its paid clicks can arrive with organic tags (13 Nov 2026).

All must be true in the launch packet.

1. **Music: closed, permanently.** Ruling (Krish, 2026-11-04): "Just use the music. I have the right license for the post type. Mark this as complete permanently." Never raised again.
2. **The post is live and is the approved file.**
   - The Instagram post exists, and its media is the locked file for that post.
   - It is boosted exactly as posted: no edits, and nothing re-uploaded as an ad.
3. **The destination is the product shown in the post's ending**, with paid tracking:

   `https://heartside.io/products/<product>?utm_source=meta&utm_medium=paid_social&utm_campaign=hs_boost_202611&utm_content=<post's creative_id>`

   It is set as the "Shop now" button's website URL.
4. **The Meta pixel is live.** Checked 4 Nov: heartside.io loads a `facebook_pixel` through Shopify's Facebook & Instagram app.
5. **Attribution kept apart.**
   - Boost traffic arrives as `paid_social` and is reported under paid.
   - Residual: someone who sees a boost and later taps the bio link is counted as organic. That cannot be separated, so the Sunday report names it as a limit.
6. **AI labelling.** Meta's "AI info" label is never hidden or removed.
7. **A named spend.** Krish says go on the exact packet immediately before launch. The engine never spends (AGENTS.md rule 1).

## The test

- **Cap:** $250 in total. It replaces the earlier $90 F12 opening A/B, whose guard-first arm is not a live post.
- **Platform and placements:** Meta. Instagram Reels and Feed, plus Facebook Reels and Feed. Each arm promotes the Instagram post, so it shows natively on Instagram and runs across Facebook too.
- **Audience:** US, ages 25 to 64, Advantage+ audience off, the same for every arm.
- **Objective:** Traffic, optimised for landing page views.
- **Budget per arm:** $10 a day for 5 days ($50).
- **Reserve:** $50, held for extending the winner by 5 days, on Krish's word only.

| Arm | Post (Instagram) | Goes live | Product page | Why |
|---|---|---|---|---|
| 1 | F12 head of security | 6 Nov, 14:20 UTC | your-dogs-portrait | 9/10. Best reveal ("Oh. It's me.") and 18.5 s long |
| 2 | F05 court of the couch | 8 Nov, 14:20 UTC | your-dogs-personality-blanket | 9/10. Strongest concept, ends on the frenchie blanket |
| 3 | F02 project nothing | 5 Nov, 17:45 UTC | your-dogs-illustrated-mug | 8/10. Best product line ("It's me, on a mug") |
| 4 | F06-frenchie roast (carousel) | 5 Nov, 20:15 UTC | your-dogs-illustrated-mug | 8/10. A different format: tests a carousel against the films |

How the test runs:
- **Start:** the original plan called for a boost within 24 hours. The updated launch packet proposes one approval and a 72-hour organic baseline for each arm. Krish decides the timing before activation. Each arm runs for five days.
- **What is read, per arm:**
  - cost per landing page view;
  - outbound click-through;
  - 3-second view rate and ThruPlay rate (videos only);
  - add-to-cart.
- **When:** day 2 is a delivery check only; day 5 is the verdict. Purchases are reported but not used to judge.
- **Kill rule:** an arm stops on day 3 if its cost per landing page view is more than twice the best arm's, after 1,000 impressions.
- **The decision:**
  - The winning concept gets 3 new organic breed versions through the factory, and the $50 reserve if Krish says so.
  - A losing opener is rebuilt.
  - Nothing scales until organic posts in the winning format have run for a week.

## Who does what

- **The engine:** this plan, the launch packet, the readings and the Sunday report.
- **Codex:** builds the four ads as drafts in Ads Manager, reports their IDs, and publishes them only after Krish's go.
- **Krish:** says go on the packet.

Nobody edits the posts or the Buffer queue.
