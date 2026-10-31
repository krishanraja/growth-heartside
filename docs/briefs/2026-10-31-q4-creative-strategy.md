# Q4 creative and posting strategy, and what the engine was missing

31 Oct 2026. Krish, after seeing a TrendTrack ad (market data, then the Meta account, then Higgsfield,
then Claude Code): "I'm just wondering if you think we need any particular data to inform how our
content strategy and posting strategy are going to drive the North Star outcomes ... We don't have
time to test and learn ... I need you to help me figure out if we're missing anything critical in our
engine." He approved this plan the same day.

**North Star part it moves:** the number, organic net sales over the trailing 4 weeks with $0 of paid
ads behind them ($25,000 by 28 Dec). It also serves the second clause: every winning format is found by
the engine and approved by Krish in one press.

## Where it stands (read 31 Oct)

| Fact | Value | Source |
|---|---|---|
| Organic net sales, trailing 28 days | $0, U4 | `NOW.md`, `growth.py attribution` (29 Oct) |
| Heartside net sales, trailing 28 days | $24; the only orders are refunded tests | heartside `NOW.md`, read live 31 Oct |
| Heartside IG, FB and TikTok, October | 4 posts, 0 reactions, 0 comments, 0 shares | Buffer aggregate metrics, read 31 Oct |
| On sale | blanket $129, portrait $59 or $119, mug $45, Artist's touch $29, Christmas card from your dog $12 | `growth.py sync`, 31 Oct |
| What prints on the gift | The painting only. "Your note, in your dog's voice, comes in the box and on a free digital card." | heartside.io product pages, read 31 Oct |
| Card cutoff | "Order it by 3 December for Christmas." | heartside.io card page, read 31 Oct |
| Approved taste rules for Heartside | none yet | Control Center `get_approved_taste`, 31 Oct |

The accounts are effectively cold. Every number below that is not in this table is an assumption and says so.

## Do we need TrendTrack-style data?

We need the data, but not that tool. Three datasets change decisions:

1. **A library of proven winners.** The Meta Ad Library shows which custom pet-portrait and pet-gift
   ads in this category have run 30 days or more. An advertiser keeps paying only for an ad that pays
   back, so long-running ads are the closest public proof of which hooks, formats and offers sell this
   gift to this buyer. That replaces the test-and-learn phase with adaptation. It is pulled weekly
   through Apify (connected), so TrendTrack isn't needed.
2. **Organic outliers.** TikTok and Instagram posts in dog gifts and dog humour whose views far exceed
   the account's followers, from the last 60 days and from last Christmas (Nov to Dec 2025). These show
   what the platforms push to people who don't follow the account, which is the only reach a cold
   account gets.
3. **Our own feedback, automated.** Per-post reach, sends and saves at 24 and 72 hours, read from
   Buffer's API (today `growth.py insights` takes manual imports only), plus the store funnel: sessions
   to chat completion to checkout. Without this the engine can't find and repeat a winner on its own.

**The Meta account at $0 spend.** Its use is the pixel and Conversions API on the store, and the
catalog connected to Meta Commerce for product tags (already handed to heartside,
`2026-10-29-heartside-shopping-tags.md`). Boosting a post would put paid ads behind it and take it out
of the North Star number.

## What was missing, ranked

| # | Gap | Why it matters | Fix |
|---|---|---|---|
| 1 | The creative truth broke on 31 Oct | Two campaigns and `AGENTS.md` said the note is on the mug and portrait, which stopped being true that day | **Fixed in this change:** copy corrected, and `check` refuses any note-on-the-gift claim |
| 2 | No reach plan for a cold account | See the sensitivity below: volume from zero followers won't reach it | Borrowed reach first: creators seeded by about 10 Nov, Instagram Collab posts with dog and breed accounts, "comment your breed" reply loops |
| 3 | The calendar ignores Christmas shipping | The ladder peaks 14 to 28 Dec, when physical gifts stop arriving in time | A dated Q4 calendar (below), and a post-cutoff offer proposed to heartside |
| 4 | No go-live step (`GET-GOING.md` Step 1) | Concept approval exists, but posting stays with Krish until it does | The go-live step through Buffer, bound to the approved payload |
| 5 | No automated feedback loop | Winners can't be repeated without Krish | Buffer per-post metrics into `engine/insights.py`, kill or keep at 24 h, three variants of a winner at 72 h |
| 6 | No market intelligence | `jobs/radar.md` is a reactive, browser-only scan | The weekly Apify winners library (datasets 1 and 2) feeding concept choice |
| 7 | Breadth isn't packaged for one press | Concept approval needs Krish to see the breadth with real mocks | One concept board: 6 to 8 concepts, each with its mock, real product, hooks, evidence, gift and occasion |

### The sensitivity (assumptions, not a forecast)

$25,000 at an assumed $80 basket is about 310 orders in four weeks. At an assumed 2% conversion that
is about 15,600 sessions. At an assumed one session per 100 to 300 views, that's roughly 1.5 to 5
million views in four weeks. The basket, conversion and click rates are unmeasured. The first real
orders replace them.

## The creative strategy

The spine: **"Your dog loves you too", sold as a Christmas gift from the dog.** Since 31 Oct the
painting is the gift, and the dog's note arrives in the box, on a free digital card, and as a $12
printed card. The note is the reveal. It is never shown printed on the product.

| Pillar | What it is | Sells | Evidence it rests on |
|---|---|---|---|
| Translate your dog | Daily carousels and stills: one breed, its comic character, four lines, the real gift last | All three gifts | The 24 approved breed examples; heartside's ten comic breed characters (below) |
| The card from the dog | What the dog would say this Christmas, ending on the $12 card and the gift | Card plus a gift, before 3 Dec | The live card page |
| Hero films | Higgsfield stills first, then Runway motion on the winner only: The Wait, Every Dog Says It Differently, Becoming the Painting | Portrait, blanket | `2026-10-29-creative-direction.md` |
| Proven formats | Hooks and formats from the winners library, rebuilt in Heartside's voice with the real product, never copied | Whichever gift the format fits | Dataset 1 |
| Creators and collabs | Gifted creators and Collab posts, FTC disclosure on every gift | Portrait, blanket | `jobs/creators.md` |

Heartside's comic characters (DOG_VOICE at `bfdb531`, for the hilarious and over_the_top tones):

- Herding, the household's exhausted operations director;
- Retriever, an overjoyed sweetheart who takes everything literally;
- Doodle, a snobbish style critic;
- Companion, a melodramatic soap star;
- Terrier, a smug little crime boss;
- Scent hound, a food critic and private investigator;
- Spitz, an unimpressed narrator of sighs;
- Sighthound, a languid sofa diva;
- Guardian, a deadly serious head of security;
- Working breeds, lovable chaos with no idea of their own size.

These give "Translate your dog" a format that sounds like each breed and can be tagged to a friend.

Lead with the blanket, the portrait and the sets. The $45 mug sits below heartside's 30% floor (heartside
`NOW.md`, 31 Oct), so it's an entry hook, not the lead.

## The Q4 calendar

| Date | What happens | Source |
|---|---|---|
| 26 Nov | Thanksgiving | calendar |
| 27 Nov | Black Friday | calendar |
| 30 Nov | Cyber Monday | calendar |
| 3 Dec | Last day to order the printed card for Christmas | heartside.io card page |
| mid-December, exact date not read yet | Printful's holiday cutoffs for the mug, portrait and blanket | read live from Printful before it is used; never assumed |
| 25 Dec | Christmas (a Friday) | calendar |

After the shipping cutoff, propose to heartside: "the card from the dog arrives on Christmas morning,
the painting follows". The free digital card already exists. Without this, the last two weeks of the
ladder have nothing to sell.

## Winners library, first read (31 Oct, Krish approved the Apify spend)

Three Apify runs on 31 Oct cost **$1.37** in total:

| Run | Cost |
|---|---|
| Meta Ad Library, 401 active US ads (`curious_coder/facebook-ads-library-scraper`) | $0.30 |
| TikTok keyword search, 28 videos (5 of 6 queries "not found"; don't use that route again) | $0.11 |
| TikTok hashtags, 240 videos (`clockworks/tiktok-scraper`) | $0.96 |

Control Center has no Apify pool for Heartside (`reserve_credit_spend`: `no_pool`), so the spend is recorded here. Raw data stays in `local/research/`, which is not committed. No creator is named here.

### Paid: what this category keeps paying for (Meta Ad Library, US, active)

The sample covered four searches: "custom dog portrait", "personalized dog gift", "dog mom gift" and "pet portrait blanket". It returned 401 ads from 140 advertisers, 299 of them pet-related, and 276 of all 401 had run 30 days or more.

| Message | Pet ads | Running 30 days or more | Advertisers |
|---|---:|---:|---:|
| Painted portrait or painting style | 177 (59%) | 130 | 51 |
| Blanket or throw | 114 (38%) | 89 | 23 |
| Memorial or loss | 81 (27%) | 73 | 32 |
| Christmas or holiday | 67 (22%) | 46 | 19 |
| For mom or a dog mom | 53 (17%) | 37 | 25 |
| Humour | 33 (11%) | 21 | 14 |
| Preview before you buy | 18 (6%) | 10 | 10 |
| A gift from the dog, in its own voice | 0 | 0 | 0 |

What it means:

1. **The painted pet blanket is the category's most-scaled paid product.** The leading advertiser alone runs 36 pet ads. Leading with the $129 blanket sells what the category already proves people buy.
2. **Video carries the long-runners.** Of the ads that ran 30 days or more, 125 are video, 80 are image and 41 are catalog ads.
3. **The category talks about loss; Heartside can't and doesn't need to.** A quarter of pet ads are memorial. Heartside's rules keep death and loss out, so it's the living, funny, warm option in a crowded, sad aisle.
4. **No one sells the gift as coming from the dog, in the dog's own voice.** Every competitor sells "your pet's photo, painted". Heartside's idea is unclaimed in this sample.
5. **Proven hooks to adapt, never copy:**
   - "Her grandkids have four legs", a story-led monologue running 172 days;
   - "That is so your dog", humour with a Christmas setting, 6 variants;
   - "Your pet, stitched into Christmas", 15 variants: Christmas-specific creative scales;
   - "Give mom the perfect gift: her dog on ...", running for years;
   - "See it free" or preview-first, which Heartside already does with "check the design before you order".

### Organic: what TikTok shows to people who don't follow the account

The sample was 6 hashtags, giving 201 unique posts.

1. **A cold account isn't a ceiling on TikTok.** 84 posts passed 100,000 plays. The median account behind them has about 14,600 followers, and 38 of the 84 have under 10,000. Several accounts with under 5,000 followers reached 2 to 6 million plays with gift videos.
2. **They are short videos.** The median length of a 100,000-play post is 14 seconds, and there was no slideshow among them. "Translate your dog" runs as a carousel on Instagram and as a 8 to 12 second video on TikTok.
3. **Shares come from the recipient and the season, not the painting:**

   | Post type | Median shares per 1,000 plays |
   |---|---:|
   | "Send this to / tag a dog owner" | 11.0 |
   | Christmas | 10.6 |
   | "Comment [word] if you want one" | 9.2 |
   | No social call to action | 4.0 |
   | Painted portrait or painting | 2.2 |
   | Memorial | 2.3 |

   Painting-process videos win views but not sends. **The rule for every Heartside post: open on the dog and the person it loves, name the recipient ("send this to the dog mom who ..."), set it at Christmas, and reveal the real painted gift last.**
4. **"Comment DOG" is usually wired to automated DMs.** Rule 7 bans those. Heartside uses "comment your dog's breed", answered by the radar's drafted replies in that breed's voice, which Krish posts.

### Concepts this points to (for the concept board)

| Concept | Built from | Sells |
|---|---|---|
| Send this to the dog mom: a dog's line to its person, Christmas morning, the real blanket last | Send/tag share rate, the blanket's paid scale, the for-mom message | Blanket |
| Her grandkids have four legs: the dog's note to grandma, as a gift from the dog | The 172-day story hook, rebuilt as the dog talking | Portrait and card |
| That is so your dog, Christmas edition: a breed's comic character ruins Christmas, then signs the card | The humour and Christmas hooks, and heartside's comic characters | Card plus a gift, before 3 Dec |
| Translate your dog, comment your breed: 12-second breed videos with a reply loop in that breed's voice | Comment-word share rate, without automated DMs | All three |
| See it before you buy: the chat shows the painting before you order | The preview-first ads | Any gift (conversion) |

## Order of work (each is its own pull request; nothing posts without an approved go-live)

1. **Done here:** the truth fix and this brief.
2. **Done 31 Oct:** the first winners library read ($1.37 of Apify, above). Rerun weekly on Mondays with the same two actors and hashtags.
3. The concept board with real-product mocks, proposed as one `stage: "plan"` behind `strategy`.
4. The go-live step through Buffer (`GET-GOING.md` Step 1), proved against the protocol stand-in.
5. Buffer metrics into `engine/insights.py`.
6. Creator seeding brought forward so gifts land by about 10 Nov.

## Assumption ledger

| Belief | Confidence | Flips when |
|---|---|---|
| Long-running competitor ads show what sells this category | medium | Adapted formats underperform our own originals on sends per reach over two weeks |
| Borrowed reach beats volume from a cold account | high | Any own-account post reaches 50,000 views without a collab |
| Basket about $80 | low | The first 10 real orders |
| $0 paid holds the ladder | low | No format reaches `replicate_candidate` by 16 Nov; then propose a capped dark-post hook lab, kept out of the organic number |

## For heartside (a finding, not a change: rule 9)

`n8n/build.mjs` DOG_VOICE at `bfdb531` still says "the meaning line is printed on the mug and the
portrait". The live product pages and heartside's own `NOW.md` say the gifts print the painting only.
A heartside session should reconcile the prompt with the release.
