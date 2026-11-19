# Instagram conversion: from views to followers to sales (19 Nov 2026)

Status: decisions 1 to 3 approved and applied 19 Nov; decision 4 drafted (4 comments) and on the review board.
North Star part it moves: organic net sales (trailing 4 weeks, $0 now, U5). Views are not the problem; the path from a view to the store is.

## What was checked, and against what

| Claim (audit Krish pasted, 19 Nov) | Checked against | Result |
|---|---|---|
| 5,283 views, all non-followers; 4,462 reached; 6 profile visits; 3 follows (28 days) | Instagram professional dashboard, read by Codex | **Verified 19 Nov** (30-day view): 5,319 views, 100% non-followers, 4,424 viewers, 6 profile visits, 1 link tap, 3 followers (`docs/social/2026-11-19-ig-dashboard.json`). The Codex read failed (no Chrome access); Claude read it in the browser pane. |
| Reels drove 4,402 views; feed 5, carousels 1; single images 0 likes | Same | **Verified:** reels 99.9% of views. Top reel 1,620 views (guest room). |
| Heartside sells posters, ornaments and pillows | `growth.py store`, 19 Nov | **False.** Live catalog: Illustrated Mug $45, Personality Blanket $129, Portrait $59 / $119, Christmas card from your dog $12, Artist's touch add-on $29. Ornament is on hold. The current bio (mugs, blankets, portraits) is right; it misses the $12 card. |
| A free preview is the hook | heartside.io home page text and heartside canon at `ffc69c1` | **Not found.** The store promises free US shipping, a person checking every order, and a free digital card with the note. No "see it before you pay" claim. The bio must not promise a preview until heartside confirms one exists. |
| Post in US evenings, 22:00 to 01:00 UK | Buffer plan `docs/social/2026-11-18-buffer-week.json` | UK is on UTC in November. 2 of our 5 daily slots (22:00 and 01:00 UTC = 17:00 and 20:00 ET) are already in that window; 13:00, 16:30 and 19:00 UTC (08:00, 11:30, 14:00 ET) are not. |

## The funnel we are building

View (reel, non-follower) -> hook holds 3 s -> product in the last 3 to 4 s -> profile visit -> bio says what it is and the price of entry -> link tap -> store -> order.

Targets for the 28 days to 17 Dec, measured in the dashboard:

| Step | Now (audit) | Target |
|---|---|---|
| Views / 28 d | 5.3k | 100k |
| Profile visits / views | 0.11% | 1% |
| Follows / profile visit | 50% (3 of 6) | 30% |
| Link taps / profile visit | not shown | 10% |
| Organic orders | 0 | first 10, then the North Star ladder |

The weak step is view -> profile visit (0.1%). That is a creative problem (no product, no reason to look further), not a reach problem, so it is fixed in the reel's last seconds and in the bio, not by posting more images.

## Posting mix

- **Instagram: reels only for growth.** Single images stop on Instagram after this week's Buffer queue. They can stay on Facebook, where the cost is nil.
- **Every reel ends on the real product** (store render, untouched, rule 4) with the end card from `docs/briefs/2026-11-18-influencer/endcard.py`: product, price from the store, "Link in bio".
- **Breed-specific jokes** from the joke lab (`factory/jokelab.py`), one breed per reel, named in the first line on screen and in the caption, so the right owners self-select.
- **Volume:** keep 5 a day per platform inside the ceiling, but on Instagram 2 to 3 of the 5 are reels; the rest are Stories (link sticker to heartside.io) rather than feed images.
- **Slots:** two US evening slots a day (22:00 and 01:00 UTC) carry the strongest reels; the US lunchtime slot (16:30 UTC) carries the rest. The 13:00 UTC slot (08:00 ET) moves to 23:30 UTC.

## Measurement

- Codex reads the dashboard at 24 h, 72 h and 7 days for every post (`post_check` and numbers into a dated `docs/social/` event file; Claude imports with `growth.py events import`).
- Per reel: views, 3 s hold, average watch time, profile visits, follows, link taps. Per week: the funnel table above.
- Decision rule after 7 days: a format with profile visits / views under 0.3% across 3 posts is dropped; one over 1% gets three more in the next week.
- Organic sales come only from tracked links (`growth.py link`) and Shopify, never from the dashboard.

## Distribution (within rule 7)

- No bulk, no DMs to strangers, no follow chasing.
- **Comments:** up to 3 per target account, each written for one specific public post with the `heartside-audience-comments` skill, in batches Krish approves ("Approve batches, Codex posts"). Targets: large breed-specific dog accounts posting in the last 24 h, where our comment is the joke, never a pitch and never a link.
- **Collabs:** the Instagram Collab invite to a named dog account is a message to a stranger, so it is a draft for Krish only, one at a time, citing their post.
- **Cross-posting:** every reel goes to TikTok and Facebook Reels the same day (already in Buffer); YouTube Shorts is not set up and is not proposed here.

## Decisions for Krish (yes or no each)

1. **Convert the remaining Instagram single-image memes in this week's Buffer queue into reels** (meme still + slow push-in + an Epidemic track + the premium end card with the real product, about 8 s). About 20 Instagram posts from 20 to 25 Nov. Facebook and TikTok images stay as they are. Each converted reel is replaced in Buffer through the connector.
2. **Move the 13:00 UTC slot to 23:30 UTC** for the rest of the week on all three platforms (about 21 posts).
3. **Profile:** the bio, pinned posts and highlights below.
4. **Comment batches** as above, first batch of 10 drafted for his yes.

## Profile draft (decision 3)

Name field: `Heartside: Personalized Dog Gifts` (unchanged).

Bio:
```
Gifts from your dog, painted from their photo
Mug $45 · Portrait from $59 · Blanket $129
A note from your dog in every box
Free US shipping 👇
```
(Prices read from the live store on 19 Nov; recheck on the day it is set. No "free preview" line until heartside confirms one.)

Link: heartside.io with a tracked link (`growth.py link https://heartside.io ig-bio`).

Pinned (3):
1. The best-performing influencer-parody reel with the product end card (the hook).
2. A product reel: a real dog photo, then the painted mug and portrait (store renders), "What your dog would give you".
3. "How it works" reel: photo -> chat with Buddy -> the painting -> the note in the box.
Items 2 and 3 do not exist yet; they are built through the joke lab and the panel before they are pinned.

Highlights: `Gifts` (each product, store renders), `How it works`, `Notes` (dog notes, no customer details), `Reviews` only once real public reviews exist.
