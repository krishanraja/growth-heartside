# Job: the weekly report (Sunday 07:00)

Kind `report`. Part 7 in `PLAYBOOK.md`. Time for Krish: about 15 minutes.

1. `python3 growth.py sync`. Use the `heartside_sha` it prints. Note every
   canon change this week, from the commits list in
   `local/state/HEARTSIDE-NOW.md`.
2. Read `python3 growth.py read --days 8`, `growth.py creatives list`,
   and `growth.py metrics report` with explicit dates and timezone.
   Check coverage before calling anything a full-period total. The ledger
   distinguishes rendered, approved and actually published. Reconcile any
   legacy `local/creatives.csv` evidence without counting it twice.
3. Work out, from real numbers only:
   - orders, net sales, the average order value and the multi-gift share,
     against last week, the month's $10,000 and the canon's checkpoints;
   - contribution, from the canon's per-gift figures (V3 section 3);
   - orders and sessions per 1,000 reached, per channel and per creative
     family;
   - sends per reach for the A/B angles;
   - where buyers drop in the journey (PLAYBOOK, "Funnel diagnosis");
   - the share loop, if it can be counted yet.
4. Write the report as items (`platform: other`), one short section each,
   answering the documents' ten questions:
   1. Which buyer (partner, mom, dad, friend) brought the most contribution?
   2. Which promise brought the most sessions per 1,000 reached?
   3. Which proof removed the biggest objection?
   4. Which format earned the most sends or saves?
   5. Which step in the journey loses the most buyers?
   6. Which channel helped sales that last-click hides?
   7. Which creative family deserves ten derivatives?
   8. Which work took time and moved nothing?
   9. Can the human check keep up with next week's target?
   10. What single constraint limits growth now: attention, traffic, offer,
       conversion, trust, economics or fulfillment?
5. Then:
   - **Scale, iterate, hold or kill**, for each creative family, channel and
     job, with the evidence.
   - **The assumption ledger** (PLAYBOOK): update each row's confidence and
     say which one moved.
   - **Next week**: the targets, the one concept family to lead with, and any
     job to change, for Krish to keep or kill.
   - **Once a month**:
     - what the engine is not doing (paid retargeting, more platforms, a new
       market), with the evidence for each in a sentence, and that it is
       Krish's call;
     - the stage in PLAYBOOK, "Becoming the category leader", and what the
       next gate needs.
6. The current Shopify adapter supplies store totals, not per-creative
   revenue. Keep attribution unavailable until a real source links it.
   A shared bio link cannot identify which Reel caused a visit. Keep
   low-volume results inconclusive. First-party event and purchase-flow
   fixes go back to the Heartside product handoff as evidence and a brief.
7. End with one call and one counterpoint. Headline: the week in one plain
   line, for example "Week 2: 11 orders ($604), behind 15 by 1 Nov by 4; the
   partner reveal is the winner". Check, then post.
