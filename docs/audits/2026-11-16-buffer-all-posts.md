# Every Heartside post sent through Buffer: what works, what doesn't, and why (16 Nov 2026)

DRAFT for Krish. Asked on 16 Nov 2026 for "a full Buffer analysis" to feed the 16 to 22 Nov production run (`CHANGES.md`,
16 Nov), keeping paid apart from organic because "some engagement came from paid boosts". This builds on
`docs/audits/2026-11-15-interest-vs-paid.md` and does not repeat it: that read covered 104 posts on three channels; this
one covers all 120 sent posts on four channels, tags every post, and turns the result into rules for the run. Read only:
nothing was posted, scheduled, edited or spent. A number Buffer does not show is "not shown", never zero. Every post is
cited by its Buffer id.

## Sources read

| Source | What | Window | Read |
|---|---|---|---|
| Buffer `list_posts` (status sent, metrics on, all pages) | 120 sent posts on the four Heartside channels: Instagram 32, TikTok 33, Facebook 42, Pinterest 13 | Facebook 12 Oct to 15 Nov; Instagram and TikTok 3 to 14 Nov; Pinterest 29 Oct to 15 Nov | 16 Nov 2026. Buffer's own refresh: Instagram 15 Nov 16:21 UTC, TikTok 15 Nov 16:41 UTC, Facebook up to 15 Nov 23:12 UTC, Pinterest 15 Nov 22:36 UTC |
| Buffer `get_aggregated_post_metrics`, per channel | Totals, 1 Oct to 16 Nov | same | 16 Nov 2026. **Cross-check passes:** the per-post sums equal the aggregates exactly on all four channels (for example TikTok 6,319 views, 264 reactions, 5 shares, 1 comment) |
| This repository | `docs/HUMOUR.md`, `factory/bank/anchors.json`, `factory/floor.json`, `knowledge/COPY-DOCTRINE.md` (skimmed), `docs/PAID-BOOSTS.md`, `docs/boost/`, `docs/social/`, `CHANGES.md` | to 16 Nov | 16 Nov 2026 |

Raw dataset: `buffer_heartside_posts.json` (scratchpad, not committed). The organization also holds 179 sent posts on
eight non-Heartside channels; they are excluded.

## The paid and organic situation

- **Paid on record: one post.** The F10 pilot ($25, Meta Ads Manager, 6 to 7 Nov) promoted the Instagram F10 Group Chat
  reel, Buffer id `6aeb87e5c6d064586b7bdf95` (`docs/boost/2026-11-05-sandbox.md`; `CHANGES.md` 13 Nov). Ads Manager read
  478 paid reach and 512 impressions on 6 Nov alone; Buffer shows that post at 9 reach and 24 views. So Buffer's
  Instagram numbers appear to exclude paid delivery (inference from one post). Its average watch of 502.6 s on a 27 s
  reel cannot be organic and is treated as corrupt.
- **Every other post: paid status unknown.** The repository records no other boost (`CHANGES.md`, 13 Nov: "no boost has
  run since"), but Krish says boosts ran on several platforms, and the 15 Nov audit found 379 Facebook-referred visits on
  11 to 13 Nov with no boost on record. No post here is called organic. Rankings below use the posts with no boost on
  record and set aside the posts whose numbers look boost-inflated; those are listed for Ads Manager at the end.
- Buffer shows **0 follows on every post** on every channel, and no profile visits or sends at all. Leading signals
  across all 120 posts total 13: Instagram 2 shares and 2 saves, TikTok 5 shares and 1 comment, Facebook 1 share,
  1 click and 1 comment. That is too few to rank posts on; reactions per 1,000 is the working proxy, with leading
  signals breaking ties.

## What the numbers say

**1. Part of the library cannot be judged from Buffer at all.** 9 of Instagram's 11 stills and carousels show 0 reach
(the F06 breed roasts, the holiday stills, the product still) and all 7 TikTok photo posts show 0 on every metric,
watch time included. These are live posts (each has a public link), so the numbers are not shown, not zero. Nothing
here says stills or carousels fail on Instagram or TikTok; they are simply unmeasured. On Facebook the stills are
measured and dead: 13 stills reached 0 to 2 people each.

**2. Each channel's distribution is set by something other than the post, so rates, not reach, carry the creative
signal.**
- Instagram: every readable reel reached 92 to 138 people (bar three early posts at 9 to 39), whatever the concept.
- TikTok: every Buffer-published video from 3 to 8 Nov but one drew 52 to 143 views; every natively published post from 12 to
  14 Nov drew 252 to 298, including the one non-alibi post in that window (Pug dance night `6af8bf2c170193d0ac9dbf40`,
  275). A step that uniform is a distribution change (native publishing, account age, or both), not a creative one.
- Facebook: median reach 13 across 37 posts at least a day old (videos 46, stills 1). Median reaction rate 7.8 per
  1,000 reach on the 17 posts that reached 20 or more.

**3. The alibi family beats the gift-led genre films on every channel, by 3 to 5 times.** Median reactions, comments,
shares, saves and clicks per 1,000 (index = against the channel's median):

| Family | Instagram | TikTok | Facebook |
|---|---|---|---|
| Alibi deadpan (12 to 15 Nov) | 49.1, index 1.69, n 10, 2 shares + 1 save | 66.9, index 1.67, n 9, 2 shares | 13.2, index 1.71, n 9, 1 share + 1 comment |
| Gift-led genre films F01 to F12 (3 to 8 Nov) | 9.1, index 0.31, n 8, 1 save | 13.6, index 0.34, n 10, 2 shares | 0.0, n 7 |
| F06 breed roasts (TikTok slideshows only) | not shown | 37.0, index 0.93, n 3 | reach 1 each |
| F38 dog-does-dog-things | 43.9, n 1, 9.7 s watch (longest on Instagram) | 17.3, n 1, boost suspect | 44.4, n 1 (probable copy, low confidence) |

The caveat is real: the two families never ran in the same week, and the alibi week was also the native-publishing
week. Two within-week checks point the same way, each with n of 1 to 3: on TikTok on 3 to 8 Nov the breed roasts (37.0)
beat the genre films (13.6) on the same route; on TikTok on 12 to 14 Nov the Pug dance reel (40.0) trailed the alibi
films (66.9) on the same route.

**4. Why, judged against HUMOUR's three parts.** The alibi posts carry all three in eight seconds: an observation every
owner has made (the dog was alone with the thing), a stupid premise played straight (he issues a statement, a memo, a
denial), and a slightly cruel payoff (the evidence contradicts him, or the cat has his job). The genre films put the
premise first and the payoff, the product reveal, at 18 to 39 s, while average watch is 2 to 6 s on every channel. Their
captions are setups or cute lines, which HUMOUR rules out by name: "The defendant pleads very cute" (`6aeb887fc6d064586b7c0f30`,
0 reactions on Instagram), "the most relatable thing we have read all year" (`6aeb88f4c6d064586b7c2f75`, 0 on TikTok),
"The dogs are scheming." (`6aea251b02521ecbfd8f0095`, 0 on TikTok).

**5. Length is the clearest format lever.** The TikTok alibi films are 8 s, the Pug reel 11 s, the genre films 16 to
39 s. Average watch barely moves (alibi 3.4 s, genre films 3.0 s), so an 8 s film is watched about 40% of the way and a
30 s film about 10%. Short films reach their payoff; long ones don't.

**6. Inside the alibi family, the visible crime scene wins and the complaint loses.** Ranked by index across channels:
Snowman, Gingerbread roof, Cat runs department, Clean sheets and Toilet roll lead; "He was told it is the same amount
as yesterday. He has requested the minutes." is last on Instagram (14.9, `6af995b12c7226f87e700a4d`) and last of the
alibi films on TikTok (51.6, `6af8bf2c170193d0ac9dbf56`). It is the only one with no damage in frame and no denial: the
dog complains instead of getting caught, so the observation is generic and the payoff isn't cruel. The corporate memo
works when it lands on a demotion (Cat runs department, `6af8442798a38b14f9e06e29`, 82.7 and 1 share), not on a
grievance.

**7. Re-airing the same film inside two days earned nothing.** F01 Coffee mug went out twice on Instagram (4 Nov 1 save,
then 6 Nov 8.5 per 1,000) and twice on TikTok (4 Nov with a plain brand-line caption, 46.7 and 2 shares,
`6aeae9022b43f8ba7d7c7417`; 6 Nov with the joke caption, 10.3, `6aeb8839f67f30658c549b14`). F10 Group Chat went out on
3 and 4 Nov on every channel and drew 0 reactions everywhere. The second airing always did worse; with n of 2 the cause
(the repeat, or the caption) cannot be split.

**8. Slots and days: no conclusion.** Within the alibi family no hour has more than 3 posts per channel. Instagram reach
is flat across slots (92 to 138), so the slot is not the lever there. Directional only: Instagram 08:00 and 16:00 ET
(rates 55.8 and 75.8, n 2 each), TikTok 08:00 and 14:45 ET (88.9 and 89.0, n 2 each). Friday and Saturday lead only
because the alibi posts ran then. Facebook's two largest reaches were 08:10 and 18:25 ET, and both are boost suspects.

**9. Captions and CTAs: confounded, one pattern holds.** CTA style (link, link in bio, typed domain) tracks the week, so
it cannot be judged. The pattern that holds across the winners is two short lines: the scene, then the dog's
third-person statement ("He has an alibi." "He has no idea what happened." "He has been asked to support the
transition."), then the brand line. Every caption from 12 Nov carries "Painted lovingly in your style of choice using
our next-generation AI artists"; whether that line sits within the floor's `no-ai-label` ("none in the caption") is
Krish's call, not a performance finding.

**10. Pinterest: nothing to read yet.** 12 of 13 Pins are video Pins under four days old with 0 impressions; the one
older Pin (product, `6ae3750d488970a7d10ce910`, 29 Oct) has 117 impressions and no saves or clicks. `docs/CHANNEL-TASKS.md`
reads Pins at 7 and 28 days; the first read is due 19 Nov.

## Top 5 and bottom 5 per channel

Posts with no boost on record, boost suspects set aside, ranked by leading signals, then comments, then rate.
"Rate" is per 1,000 views (Instagram, TikTok) or reach (Facebook).

### Instagram (19 posts; median 25.9 per 1,000 views)

| | Buffer id | Post | Rate (index) | Leading | Why, against HUMOUR |
|---|---|---|---|---|---|
| Top 1 | `6af8442798a38b14f9e06e29` | Cat runs department | 82.7 (3.2) | 1 share | All three: the household pecking order, a corporate memo, and the dog demoted in his own house |
| Top 2 | `6af995b12c7226f87e700a61` | Clean sheets | 72.0 (2.8) | 1 save | All three: a statement for the record that the picture contradicts |
| Top 3 | `6af995b12c7226f87e700a78` | Sofa rule | 29.0 (1.1) | 1 share | Intellectual stupidity: the loophole lawyer. Shared on Instagram and Facebook, but the lowest reaction rate of the five |
| Top 4 | `6aeae902d59713e43431851d` | F01 Coffee mug (first airing) | 22.7 (0.9) | 1 save | One save on 44 views; n too small to read anything into |
| Top 5 | `6af8442798a38b14f9e06e1c` | Gingerbread roof | 79.4 (3.1) | none | All three: the crime scene, then "He says it came without a roof" |
| Bottom 1 | `6aeb887fc6d064586b7c0f30` | F05 Court of the couch | 0.0 | none | Strong format, but the caption's payoff is "pleads very cute": a cute line, not a cruel one |
| Bottom 2 | `6aeb883b23e3db949c151e08` | F03 Christmas heist | 0.0 | none | Heist setup, cookie payoff; 1.4 s watch, so the 20 s film's payoff is never seen |
| Bottom 3 | `6aeb88f623e3db949c1552d8` | F12 Head of security | 8.2 (0.3) | none | Good premise, payoff (the product) at 18 s; watched 5.8 s |
| Bottom 4 | `6aeb8839f67f30658c549b8e` | F01 Coffee mug (second airing) | 8.5 (0.3) | none | Repeat two days after the first |
| Bottom 5 | `6aeb8837f67f30658c549aad` | F02 Project nothing | 9.7 (0.4) | none | Gift-led premise; the joke is the purchase intent, not the dog getting caught |

### TikTok (24 posts; median 40.0 per 1,000 views)

| | Buffer id | Post | Rate (index) | Leading | Why, against HUMOUR |
|---|---|---|---|---|---|
| Top 1 | `6af8bf2c170193d0ac9dbf42` | Gingerbread roof | 68.1 (1.7) | 2 shares | All three, and the only alibi film shared on TikTok |
| Top 2 | `6aeae9022b43f8ba7d7c7417` | F01 Coffee mug, brand-line caption | 46.7 (1.2) | 2 shares | First airing; caption was only the brand line and hashtags (concept matched by length and slot, medium confidence) |
| Top 3 | `6af8bf2c170193d0ac9dbf3a` | Snowman | 126.4 (3.2) | none | All three; the best rate on Instagram or TikTok |
| Top 4 | `6af8bf2c170193d0ac9dbf52` | Toilet roll alibi | 115.4 (2.9) | none | Two beats: the evidence, then "He has an alibi" |
| Top 5 | `6af8bf2c170193d0ac9dbf4a` | Sofa rule | 67.1 (1.7) | none | Loophole lawyer; the longest watch on TikTok (4.9 s of 8) |
| Bottom 1 | `6aea251b02521ecbfd8f0095` | F10 Group chat v1, "The dogs are scheming." | 0.0 | none | No observation and no payoff in the caption; 39 s film |
| Bottom 2 | `6aeb88f4c6d064586b7c2f75` | F11 Search history | 0.0 | none | Tells the viewer it is relatable instead of showing it |
| Bottom 3 | `6aeb88f76cbba97f5cbfb999` | F07 Art critic | 9.5 (0.2) | none | The verdict serves the product, so there is no cruelty in the payoff |
| Bottom 4 | `6aeb8839f67f30658c549b14` | F01 Coffee mug, second airing | 10.3 (0.3) | none | Repeat |
| Bottom 5 | `6aeb887fc6d064586b7c0ed4` | F05 Court of the couch | 13.2 (0.3) | none | As on Instagram |

### Facebook (13 posts reaching 20 or more; median 7.8 per 1,000 reach)

| | Buffer id | Post | Rate (index) | Leading | Why |
|---|---|---|---|---|---|
| Top 1 | `6af3a7bb7b17f0bb1eb225cf` | No caption; posted the same minute as Instagram's F38, so probably F38 (low confidence) | 44.4 | 1 click | The only click on Facebook |
| Top 2 | `6af85e3bd6dfe42dc90dcb76` | Clean sheets | 20.4 (2.6) | 1 comment | Same read as Instagram |
| Top 3 | `6af780bf1093e7552bb0da94` | Cat runs department | 148.1 | none | 4 reactions on reach 27: too small to rank on |
| Top 4 | `6af728d1712c517e58e808b5` | Gingerbread roof | 34.5 | none | 1 reaction on reach 29 |
| Top 5 | `6af87dd59ccf6c8303e3d071` | Fridge witness | 16.7 (2.2) | none | 1 reaction on reach 60 |
| Bottom | `6aeb883a8ee551b5aa780fcd`, `6aeb8880f67f30658c54b0f6`, `6aeb88f88ee551b5aa784532`, `6af76b7402c85d7e14c7feb3`, `6af8d22e8bf56d99caf8217b` | F01, F05, F07, Snowman, Vacuum coward | 0 to 5.6 | none | Facebook gives almost no reactions to anything; Snowman, the best post on TikTok, got 0 here |

Facebook's ranking is noise around single reactions. It confirms the 15 Nov proposal: a paired cross-post only.

### Pinterest

One readable Pin, so no top or bottom five. See finding 10.

## Rules for the 16 to 22 Nov run

Each rule is a proposal for Krish's Yes, and none changes approved strategy or spend.

1. **Make the alibi family most of the run.** Frame 1 is the crime scene (the destroyed snowman, the roofless
   gingerbread house, the unrolled roll); the payoff is the dog's denial or demotion. Evidence: `6af8bf2c170193d0ac9dbf3a`,
   `6af8bf2c170193d0ac9dbf52`, `6af8442798a38b14f9e06e1c`, `6af8442798a38b14f9e06e29`, `6af995b12c7226f87e700a61`.
2. **No crime, no post.** A complaint, a mood or a cute behavior is not an alibi. Retire the "grievance" variant.
   Evidence: `6af995b12c7226f87e700a4d` and `6af8bf2c170193d0ac9dbf56` (same amount), last in the family on two channels.
3. **8 to 12 seconds, payoff by second 4.** Average watch is 3 to 4 s everywhere; the product end card (held 3 s, floor
   `endings-land`) follows the payoff, never replaces it. Evidence: the 8 s alibi films (TikTok median 66.9) against the
   16 to 39 s genre films (13.6), with the same 3 s watch.
4. **Stop the 18 to 39 s gift-led genre films and setup captions.** Keep their premises only if they can be rebuilt as
   an 8 s caught-in-the-act. Evidence: `6aeb887fc6d064586b7c0f30`, `6aeb883b23e3db949c151e08`, `6aeb88f4c6d064586b7c2f75`,
   `6aeb88f76cbba97f5cbfb999`, `6aea251b02521ecbfd8f0095`.
5. **Caption pattern.** Line 1: the scene in under ten words. Line 2: the dog's third-person statement, plain and flat
   ("He has an alibi." "He has read the rule very carefully."). Then the brand line. Never "cute", "relatable" or a
   teaser. Evidence: the winners above against the three zero-reaction captions in rule 4.
6. **Corporate language only on a demotion or a ruling.** The memo works when the dog loses status or a loophole wins.
   Evidence: `6af8442798a38b14f9e06e29` (memo plus demotion, 82.7 and a share) and `6af995b12c7226f87e700a78` (loophole, shared on
   two channels) against `6af995b12c7226f87e700a4d` (memo plus grievance, 14.9).
7. **Never re-air a film within seven days on the same channel.** Evidence: F01 `6aeae902d59713e43431851d` then
   `6aeb8839f67f30658c549b8e`; `6aeae9022b43f8ba7d7c7417` then `6aeb8839f67f30658c549b14`; F10 on 3 and 4 Nov.
8. **One or two dog-does-dog-things reels in the week, judged on rate.** F38 earned Instagram's longest watch (9.7 s,
   `6af44f892ac365bb29971f73`), but its TikTok views are unverified (see the list below), so do not build the week on them.
9. **Slots: keep the house slots.** The data cannot pick one. If a choice is forced, lead with Instagram 08:00 and
   16:00 ET and TikTok 08:00 and 14:45 ET (n 2 each, direction only). Facebook and Pinterest follow their paired posts.
10. **Measure what Buffer can't.** Any still or carousel on Instagram or TikTok is read natively (Instagram Insights,
    TikTok analytics) at 24 h, or it counts as unmeasured, not failed. Facebook stills stop: 13 reached 0 to 2 people.
11. **Pinterest: no new creative until the 19 Nov read.** Then judge by saves and outbound clicks per impression.
12. **The boost bar from 15 Nov stands.** By rate and leading signals the current organic candidates are Cat runs
    department and Clean sheets on Instagram, and Gingerbread roof and Snowman on TikTok, subject to their 72 h reads
    and to the verification below.

## Posts needing Ads Manager or TikTok Promote verification

For the browser session (read only). In priority order:

| # | Buffer id | Channel, post, ET | Why it looks boost-inflated | Where to read |
|---|---|---|---|---|
| 1 | `6af41759b5558cbc3c34e37b` | TikTok, F38 4 AM routine, 10 Nov 19:24 | 2,314 views, 17 times the median; rate 0.43 of median; 1.7 s watch, the lowest on TikTok | TikTok Promote and TikTok Ads Manager |
| 2 | `6af8ee4e34921e8252adba8c` | Facebook, Sofa rule, 14 Nov 18:25 | 831 reach and 1,057 impressions, 8.5 times the median | Meta Ads Manager; Page Boost history |
| 3 | `6af70cbbbbc744c14cd04deb` | Facebook, Toilet roll alibi, 13 Nov 08:10 | 233 reach with 0 reactions, inside the 11 to 13 Nov burst of 379 homepage visits | Ads Manager; also Shopify sessions by `utm_content` for 11 to 13 Nov, which would name the post the burst came through |
| 4 | `6af5d74f63cc33009a548cad`, `6af3a7bb7b17f0bb1eb225cf`, `6af38eae5645445a053428e1`, `6af3901ce04e630ba5b238b3` | Facebook, Pie (12 Nov), the uncaptioned 10 Nov post, and two F38 copies (10 Nov) | Live during the burst. The two F38 copies show 0 reach with metrics last refreshed 10 Nov, so their numbers are stale, not zero | Ads Manager; Page post insights |
| 5 | `6aeb887e23e3db949c15329a`, `6aeb883c6cbba97f5cbf77f1` | Facebook, F04 The spot (7 Nov) and F03 Christmas heist (8 Nov) | 217 and 182 reach with 0 reactions each, during and just after the F10 pilot | Ads Manager; Page Boost history |
| 6 | `6af8d22e8bf56d99caf8217b`, `6af85e3bd6dfe42dc90dcb76`, `6af8bcec135e51aa93dbac5e` | Facebook, Vacuum coward, Clean sheets, Same amount (14 Nov) | 128 to 180 reach, 1.3 to 1.8 times the median | Ads Manager |
| 7 | `6aeb87e5c6d064586b7bdf95`, `6aea252124384d401855c00b` | Instagram, F10 Group chat (4 Nov, paid on record) and its 3 Nov copy | Final pilot numbers by placement. The 3 Nov copy shows 0 views but a 308 s average watch, which needs explaining | Ads Manager; Instagram Insights |
| 8 | All 11 TikTok posts of 12 to 14 Nov (for example `6af8bf2c170193d0ac9dbf3a`) | TikTok | A uniform step to 252 to 298 views. Probably organic distribution, but nothing rules out a promotion | TikTok Promote |

Each reading becomes a `boost` record in a dated `docs/social/` event file (`docs/PAID-BOOSTS.md`, "Reading a boost's
results"). Until then, every ranking above is "paid status unknown".

## Limits

- Sample sizes are small: 20 readable Instagram posts, 25 TikTok, 17 Facebook, 1 Pinterest. Family comparisons rest on
  8 to 10 posts per side per channel; hook, slot, day and CTA cells mostly hold 1 to 3 posts and are direction only.
- The families are confounded with the week and the publishing route (Buffer 3 to 8 Nov, native from 10 Nov). Rates,
  not reach, are used for that reason, but the confound is not removed.
- The newest posts are one to two days old at reading (TikTok 14 Nov reach not yet shown; Facebook 15 Nov posts under
  24 hours old); their numbers will move.
- Tags come from captions, Buffer's video length and posting slot, not from watching the films. Low-confidence tags
  are marked in Appendix A.

## Appendix A: every readable post, tagged

Rate is reactions, comments, shares, saves and clicks per 1,000 views (Instagram, TikTok) or per 1,000 reach (Facebook). Index is the post's rate over its channel's median rate. Leading is shares + saves + clicks + follows. Watch is Buffer's average watch time in seconds. Slot is US Eastern. A dash means Buffer did not show the number. Paid: "unknown" means no boost is on record and none can be ruled out.

### Instagram (20 readable; median rate 25.9 per 1,000)

| Buffer id | Slot (ET) | Concept | Family | Format, length | Hook | CTA | Paid | Base | Rate | Index | Leading | Watch | Tag confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6aeae902d59713e43431851d | 11-04 Wed 09:21 | F01 coffee mug Plan C | gift-led genre film | video, 31 s | serial diary | link in bio | unknown | 44 views | 22.7 | 0.88 | 1 save | 1.89 | high |
| 6aeb87e5c6d064586b7bdf95 | 11-04 Wed 15:15 | F10 group chat | gift-led genre film | video, 27 s | second-person reveal + tag a friend | link in bio | on record (F10 pilot) | 24 views | 0.0 | 0.0 | none | 502.64 | high |
| 6aeb88f41310dbd9d43f33de | 11-05 Thu 09:23 | F11 search history | gift-led genre film | video, 27 s | we found your dog's X | link in bio | unknown | 124 views | 16.1 | 0.62 | none | 6.11 | high |
| 6aeb8837f67f30658c549aad | 11-05 Thu 12:46 | F02 project nothing | gift-led genre film | video, 32 s | human claim, dog hears a challenge | link in bio | unknown | 103 views | 9.7 | 0.38 | none | 2.86 | high |
| 6aeb88f623e3db949c1552d8 | 11-06 Fri 09:20 | F12 head of security | gift-led genre film | video, 18 s | genre setup, then undercut | link in bio | unknown | 122 views | 8.2 | 0.32 | none | 5.82 | high |
| 6aeb8839f67f30658c549b8e | 11-06 Fri 15:15 | F01 coffee mug Plan C | gift-led genre film | video, 31 s | serial diary | link in bio | unknown | 118 views | 8.5 | 0.33 | none | 5.12 | high |
| 6aeb887ec6d064586b7c0e90 | 11-07 Sat 09:20 | F04 the spot | gift-led genre film | video, 23 s | relatable rule | link in bio | unknown | 148 views | 20.3 | 0.78 | none | 4.14 | high |
| 6aeb887fc6d064586b7c0f30 | 11-08 Sun 09:21 | F05 court of the couch | gift-led genre film | video, 30 s | genre setup, then undercut | link in bio | unknown | 40 views | 0.0 | 0.0 | none | 3.41 | high |
| 6aeb883b23e3db949c151e08 | 11-08 Sun 12:46 | F03 Christmas heist | gift-led genre film | video, 20 s | genre setup, then undercut | link in bio | unknown | 96 views | 0.0 | 0.0 | none | 1.43 | high |
| 6af44f892ac365bb29971f73 | 11-10 Tue 18:23 | F38 4 AM routine | dog-does-dog-things | video, length not shown | time-stamped routine labels | link in bio | unknown | 114 views | 43.9 | 1.7 | none | 9.74 | high |
| 6af6f29ee7d5baf3e38fa8c5 | 11-12 Thu 10:06 | Pie investigation | alibi deadpan | video, length not shown | evidence, then inflated explanation | link in bio | unknown | 134 views | 44.8 | 1.73 | none | 4.96 | high |
| 6af8442798a38b14f9e06e2f | 11-13 Fri 08:06 | Toilet roll alibi | alibi deadpan | video, length not shown | evidence, then inflated explanation | link in bio | unknown | 126 views | 39.7 | 1.53 | none | 2.1 | high |
| 6af8442798a38b14f9e06e1c | 11-13 Fri 10:06 | Gingerbread roof | alibi deadpan | video, length not shown | evidence, then inflated explanation | link in bio | unknown | 126 views | 79.4 | 3.07 | none | 3.27 | high |
| 6af8442798a38b14f9e06e1a | 11-13 Fri 14:50 | Snowman | alibi deadpan | video, length not shown | evidence, then inflated explanation | link in bio | unknown | 131 views | 53.4 | 2.07 | none | 3.3 | high |
| 6af8442798a38b14f9e06e29 | 11-13 Fri 16:21 | Cat runs department | alibi deadpan | video, length not shown | corporate memo | link in bio | unknown | 133 views | 82.7 | 3.2 | 1 share | 4.2 | high |
| 6af995b12c7226f87e700a61 | 11-14 Sat 08:06 | Clean sheets | alibi deadpan | video, length not shown | evidence, then inflated explanation | link in bio | unknown | 125 views | 72.0 | 2.78 | 1 save | 3.94 | high |
| 6af995b12c7226f87e700a5e | 11-14 Sat 10:21 | Fridge witness | alibi deadpan | video, length not shown | time stamp + scene | link in bio | unknown | 131 views | 38.2 | 1.48 | none | 3.85 | high |
| 6af995b12c7226f87e700a4d | 11-14 Sat 14:50 | Same amount, minutes | alibi deadpan | video, length not shown | corporate memo | link in bio | unknown | 134 views | 14.9 | 0.58 | none | 3.39 | high |
| 6af995b12c7226f87e700a5c | 11-14 Sat 16:21 | Vacuum coward | alibi deadpan | video, length not shown | claim, then puncture | link in bio | unknown | 116 views | 69.0 | 2.67 | none | 4.08 | high |
| 6af995b12c7226f87e700a78 | 11-14 Sat 18:21 | Sofa rule | alibi deadpan | video, length not shown | rule, then loophole | link in bio | unknown | 138 views | 29.0 | 1.12 | 1 share | 4.46 | high |

### TikTok (25 readable; median rate 40.0 per 1,000)

| Buffer id | Slot (ET) | Concept | Family | Format, length | Hook | CTA | Paid | Base | Rate | Index | Leading | Watch | Tag confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6aea251b02521ecbfd8f0095 | 11-03 Tue 13:18 | F10 group chat v1 (teaser caption) | gift-led genre film | video, 39 s | three-word teaser | none | unknown | 73 views | 0.0 | 0.0 | none | 3.29 | medium |
| 6aeae9022b43f8ba7d7c7417 | 11-04 Wed 09:16 | F01 coffee mug (brand-line caption) | gift-led genre film | video, 31 s | brand line as hook | typed domain | unknown | 107 views | 46.7 | 1.17 | 2 share | 4.14 | medium |
| 6aeb88f4c6d064586b7c2f75 | 11-05 Thu 09:16 | F11 search history | gift-led genre film | video, 27 s | we found your dog's X | typed domain | unknown | 52 views | 0.0 | 0.0 | none | 2.72 | high |
| 6aec690320e5812fe94518a0 | 11-05 Thu 11:03 | Untitled still (no caption) | holiday still | carousel, length not shown | none | none | unknown | 101 views | 19.8 | 0.5 | none | 3.13 | low |
| 6aeb88358ee551b5aa780e03 | 11-05 Thu 12:40 | F02 project nothing | gift-led genre film | video, 32 s | human claim, dog hears a challenge | typed domain | unknown | 60 views | 33.3 | 0.83 | none | 4.03 | high |
| 6aeb88f58ee551b5aa7844c3 | 11-05 Thu 15:10 | F06 frenchie roast | breed roast carousel | video, 16 s | what your BREED thinks of you | typed domain | unknown | 60 views | 33.3 | 0.83 | none | 3.48 | high |
| 6aeb88f6f67f30658c54e1c8 | 11-06 Fri 09:15 | F12 head of security | gift-led genre film | video, 18 s | genre setup, then undercut | typed domain | unknown | 108 views | 55.6 | 1.39 | none | 2.07 | high |
| 6aeb887d23e3db949c153222 | 11-06 Fri 12:40 | F06 dachshund roast | breed roast carousel | video, 16 s | what your BREED thinks of you | typed domain | unknown | 120 views | 66.7 | 1.67 | none | 2.21 | high |
| 6aeb8839f67f30658c549b14 | 11-06 Fri 15:10 | F01 coffee mug Plan C | gift-led genre film | video, 31 s | serial diary | typed domain | unknown | 97 views | 10.3 | 0.26 | none | 2.56 | high |
| 6aeb887ec6d064586b7c0e41 | 11-07 Sat 09:16 | F04 the spot | gift-led genre film | video, 23 s | relatable rule | typed domain | unknown | 143 views | 14.0 | 0.35 | none | 3.52 | high |
| 6aeb88f76cbba97f5cbfb999 | 11-07 Sat 12:40 | F07 art critic | gift-led genre film | video, 19 s | genre setup, then undercut | typed domain | unknown | 105 views | 9.5 | 0.24 | none | 2.43 | high |
| 6aeb88f823e3db949c155390 | 11-07 Sat 15:11 | F06 lab roast | breed roast carousel | video, 16 s | what your BREED thinks of you | typed domain | unknown | 135 views | 37.0 | 0.93 | none | 4.08 | high |
| 6aeb887fc6d064586b7c0ed4 | 11-08 Sun 09:15 | F05 court of the couch | gift-led genre film | video, 30 s | genre setup, then undercut | typed domain | unknown | 76 views | 13.2 | 0.33 | none | 3.45 | high |
| 6aeb883bf67f30658c549e42 | 11-08 Sun 12:40 | F03 Christmas heist | gift-led genre film | video, 20 s | genre setup, then undercut | typed domain | unknown | 90 views | 33.3 | 0.83 | none | 2.78 | high |
| 6af41759b5558cbc3c34e37b | 11-10 Tue 19:24 | F38 4 AM routine | dog-does-dog-things | video, 22 s | time-stamped routine labels | none | unknown; boost suspect | 2314 views | 17.3 | 0.43 | 1 share, 1 comment | 1.71 | high |
| 6af8bf2c170193d0ac9dbf40 | 11-12 Thu 08:00 | Pug dance night | trend/dance reel | video, 11 s | scene + deadpan aside | link in bio | unknown | 275 views | 40.0 | 1.0 | none | 2.83 | low |
| 6af8bf2c170193d0ac9dbf3c | 11-12 Thu 10:00 | Pie investigation | alibi deadpan | video, 8 s | evidence, then inflated explanation | link in bio | unknown | 281 views | 56.9 | 1.42 | none | 4.49 | high |
| 6af8bf2c170193d0ac9dbf52 | 11-13 Fri 08:00 | Toilet roll alibi | alibi deadpan | video, 8 s | evidence, then inflated explanation | link in bio | unknown | 260 views | 115.4 | 2.88 | none | 3.47 | high |
| 6af8bf2c170193d0ac9dbf42 | 11-13 Fri 10:00 | Gingerbread roof | alibi deadpan | video, 8 s | evidence, then inflated explanation | link in bio | unknown | 279 views | 68.1 | 1.7 | 2 share | 2.76 | high |
| 6af8bf2c170193d0ac9dbf3a | 11-13 Fri 14:45 | Snowman | alibi deadpan | video, 8 s | evidence, then inflated explanation | link in bio | unknown | 261 views | 126.4 | 3.16 | none | 3.55 | high |
| 6af8bf2c170193d0ac9dbf44 | 11-13 Fri 16:15 | Cat runs department | alibi deadpan | video, 8 s | corporate memo | link in bio | unknown | 254 views | 66.9 | 1.67 | none | 2.93 | high |
| 6af8bf2c170193d0ac9dbf4a | 11-14 Sat 06:15 | Sofa rule | alibi deadpan | video, 8 s | rule, then loophole | link in bio | unknown | 298 views | 67.1 | 1.68 | none | 4.88 | high |
| 6af8bf2c170193d0ac9dbfaa | 11-14 Sat 08:00 | Clean sheets | alibi deadpan | video, 8 s | evidence, then inflated explanation | link in bio | unknown | 256 views | 62.5 | 1.56 | none | 3.38 | high |
| 6af8bf2c170193d0ac9dbf4c | 11-14 Sat 10:15 | Fridge witness | alibi deadpan | video, 8 s | time stamp + scene | link in bio | unknown | 254 views | 66.9 | 1.67 | none | 3.06 | high |
| 6af8bf2c170193d0ac9dbf56 | 11-14 Sat 14:45 | Same amount, minutes | alibi deadpan | video, 8 s | corporate memo | link in bio | unknown | 252 views | 51.6 | 1.29 | none | 2.77 | high |

### Facebook (17 readable; median rate 7.8 per 1,000)

| Buffer id | Slot (ET) | Concept | Family | Format, length | Hook | CTA | Paid | Base | Rate | Index | Leading | Watch | Tag confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6aeb8838c6d064586b7bf3a1 | 11-05 Thu 12:50 | F02 project nothing | gift-led genre film | video, 32 s | human claim, dog hears a challenge | link | unknown | 76 reach | 13.2 | 1.7 | none | - | high |
| 6aeb88f66cbba97f5cbfb967 | 11-06 Fri 09:25 | F12 head of security | gift-led genre film | video, 18 s | genre setup, then undercut | link | unknown | 129 reach | 7.8 | 1.0 | none | - | high |
| 6aeb883a8ee551b5aa780fcd | 11-06 Fri 15:20 | F01 coffee mug Plan C | gift-led genre film | video, 31 s | serial diary | link | unknown | 98 reach | 0.0 | 0.0 | none | - | high |
| 6aeb887e23e3db949c15329a | 11-07 Sat 09:25 | F04 the spot | gift-led genre film | video, 23 s | relatable rule | link | unknown; boost suspect | 217 reach | 0.0 | 0.0 | none | - | high |
| 6aeb88f88ee551b5aa784532 | 11-07 Sat 12:50 | F07 art critic | gift-led genre film | video, 19 s | genre setup, then undercut | link | unknown | 24 reach | 0.0 | 0.0 | none | - | high |
| 6aeb8880f67f30658c54b0f6 | 11-08 Sun 09:25 | F05 court of the couch | gift-led genre film | video, 30 s | genre setup, then undercut | link | unknown | 47 reach | 0.0 | 0.0 | none | - | high |
| 6aeb883c6cbba97f5cbf77f1 | 11-08 Sun 12:50 | F03 Christmas heist | gift-led genre film | video, 20 s | genre setup, then undercut | link | unknown; boost suspect | 182 reach | 0.0 | 0.0 | none | - | high |
| 6af3a7bb7b17f0bb1eb225cf | 11-10 Tue 18:23 | F38 4 AM routine (probable FB copy, no caption) | dog-does-dog-things | video, length not shown | time-stamped routine labels | none | unknown; watch | 45 reach | 44.4 | 5.73 | 1 click | - | low |
| 6af70cbbbbc744c14cd04deb | 11-13 Fri 08:10 | Toilet roll alibi | alibi deadpan | video, length not shown | evidence, then inflated explanation | link | unknown; boost suspect | 233 reach | 0.0 | 0.0 | none | - | high |
| 6af728d1712c517e58e808b5 | 11-13 Fri 10:10 | Gingerbread roof | alibi deadpan | video, length not shown | evidence, then inflated explanation | link | unknown | 29 reach | 34.5 | 4.45 | none | - | high |
| 6af76b7402c85d7e14c7feb3 | 11-13 Fri 14:55 | Snowman | alibi deadpan | video, length not shown | evidence, then inflated explanation | link | unknown | 35 reach | 0.0 | 0.0 | none | - | high |
| 6af780bf1093e7552bb0da94 | 11-13 Fri 16:26 | Cat runs department | alibi deadpan | video, length not shown | corporate memo | link | unknown | 27 reach | 148.1 | 19.11 | none | - | high |
| 6af85e3bd6dfe42dc90dcb76 | 11-14 Sat 08:10 | Clean sheets | alibi deadpan | video, length not shown | evidence, then inflated explanation | link | unknown; watch | 147 reach | 20.4 | 2.63 | 1 comment | - | high |
| 6af87dd59ccf6c8303e3d071 | 11-14 Sat 10:25 | Fridge witness | alibi deadpan | video, length not shown | time stamp + scene | link | unknown | 60 reach | 16.7 | 2.15 | none | - | high |
| 6af8bcec135e51aa93dbac5e | 11-14 Sat 14:55 | Same amount, minutes | alibi deadpan | video, length not shown | corporate memo | link | unknown; watch | 128 reach | 7.8 | 1.01 | none | - | high |
| 6af8d22e8bf56d99caf8217b | 11-14 Sat 16:25 | Vacuum coward | alibi deadpan | video, length not shown | claim, then puncture | link | unknown; watch | 180 reach | 5.6 | 0.72 | none | - | high |
| 6af8ee4e34921e8252adba8c | 11-14 Sat 18:25 | Sofa rule | alibi deadpan | video, length not shown | rule, then loophole | link | unknown; boost suspect | 831 reach | 13.2 | 1.71 | 1 share | - | high |

### Pinterest (1 readable; median rate 0.0 per 1,000)

| Buffer id | Slot (ET) | Concept | Family | Format, length | Hook | CTA | Paid | Base | Rate | Index | Leading | Watch | Tag confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6ae3750d488970a7d10ce910 | 10-29 Thu 11:36 | Product Pin | gift-led product | image, length not shown | product description | none | unknown | 117 impressions | 0.0 | - | none | - | high |

## Appendix B: posts with no usable reading

| Channel | Why | Buffer ids |
|---|---|---|
| Facebook | reach under 20: a real reading, too small for a rate | 6af5d74f63cc33009a548cad, 6aeb891b6cbba97f5cbfc61c, 6aec66e38477444d9dbc8279, 6aec66e31381c3b3047651cf, 6aeb891a1310dbd9d43f4bd3, 6aec66e28ed5e05aeda3379c, 6aeb891923e3db949c155e01, 6aec66e1f5b4b5564cb35499, 6aeb88f5c6d064586b7c30c7, 6aeb87e6f67f30658c5482b4, 6aeae903d59713e43431868a, 6aea1fdd4132b75c1ec9a669, 6aea26231f06859f7ba52f04, 6aea17d52ea34807059c7911, 6ae096d5ad63bebc814552c4 |
| Facebook | no delivery shown (0 reach) | 6af3901ce04e630ba5b238b3, 6af38eae5645445a053428e1, 6ae096d5ad63bebc814552c6, 6ae096d5ad63bebc814552c0, 6ae096d5ad63bebc814552c2 |
| Facebook | under 24 h old at reading | 6afa3c57623618d060e91970, 6afa120180bb7829774b8cf4, 6af9eef3d0ffd3d942a6f317, 6af9afb7e2c271fa702eca64, 6af9971d10d2a2ca57ada297 |
| Instagram | still or carousel: Buffer shows 0 reach (not shown, the post is live) | 6aeb891a8ee551b5aa7855b0, 6aec66e38ed5e05aeda337ff, 6aec66e2096bdb6b0ff3bd34, 6aeb891923e3db949c155e2e, 6aec66e28477444d9dbc81f0, 6aeb8918f67f30658c54f3c1, 6aec66e11381c3b3047650a3, 6aea1fcca29d5d9e76cf8030, 6aea1754be501cd7c1ba4749 |
| Instagram | views under 20: too small for a rate | 6aeb88f76cbba97f5cbfb9c7 |
| Instagram | no delivery shown (0 reach) | 6af3c8b5b2f530c024ee808b, 6aea252124384d401855c00b |
| Pinterest | Pin under 4 days old | 6af9dd093a7e0136563cf4eb, 6af9dd093a7e0136563cf4e6, 6af9dd093a7e0136563cf4e9, 6af9dd093a7e0136563cf4e3, 6af88b7a320d8a8b8a0c0f3b, 6af88b7a320d8a8b8a0c0f35, 6af88b7a320d8a8b8a0c0f37, 6af88b7a320d8a8b8a0c0f3e, 6af88b7a320d8a8b8a0c0f33, 6af739eb88ce4e599aa66a5d, 6af739eb88ce4e599aa66a60, 6af5e85c450bd1826c18a874 |
| TikTok | photo post: every metric 0, watch time included (not shown, the post is live) | 6af43a50bf43cde557a26529, 6af43a50bf43cde557a26512, 6af43a50bf43cde557a26514, 6af43a50bf43cde557a26510, 6af43a50bf43cde557a2652c, 6af43a50bf43cde557a26517, 6af43a50bf43cde557a2651c |
| TikTok | views under 20: too small for a rate | 6aeb87e51310dbd9d43ee144 |
