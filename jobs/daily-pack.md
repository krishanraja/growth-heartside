# Job: the day's pack (every day)

Kind `daily`. Parts 3 and 6 in `PLAYBOOK.md`. Time for Krish: about 10
minutes to read, then the time to make and post one Reel.

1. `python3 growth.py sync`. Use the `heartside_sha` it prints. Run `python3
   growth.py store`. If the v3 gifts are not on sale yet, today's pack builds
   the audience and the comment loop, with no "buy" call to action, and the
   headline says so.
2. Choose **one concept**. In order of preference:
   - a winner to multiply (the latest `report` or `numbers` pack names it);
   - the strongest opportunity in today's or yesterday's radar
     (`python3 growth.py read --days 2 --kind radar`);
   - the next format in the PLAYBOOK bank not used in the last 7 days.

   Keep the mix in PLAYBOOK, "Pillars". Before drafting, write down:
   - the concept number;
   - the pillar;
   - the one-sentence mechanism ("a partner reading the lines aloud makes
     people send it to their own partner");
   - the buyer (partner, mom, dad, friend);
   - the one signal it should move (sends, link taps, orders).
3. Draft, one item each, each with its own creative id (PLAYBOOK, "Creative
   ids"). Every heartside.io link is tracked (`python3 growth.py link`). Keep
   the idea the same in every edition. Change the opening frame, hook
   wording, caption, cover and call to action to suit the platform. Never
   paste the same text twice.
   - **The brief** (`platform: other`). It includes:
     - the hook (first frame, works muted);
     - a beat sheet with times, and a shot list;
     - on-screen text, any voiceover and any Biscuit lines;
     - the source assets from heartside's library;
     - how the real print files appear;
     - what must not appear: AI customers, the product drawn by AI,
       invented reactions.

     9:16, with text inside the safe zone. Start every line the public will
     see or hear with `Hook:`, `On screen:`, `Voiceover:`, `Biscuit:`,
     `Cover:` or `Caption:`. `check` holds those lines to the copy rules and
     reads the rest as notes for Krish.
   - **Instagram Reel** (`instagram`, REEL): the caption, with the search
     phrase in the first sentence and 2 to 5 specific hashtags; the cover
     (3 to 6 words); one call to action.
   - **Instagram Story** (`instagram`, STORY): 3 to 5 frames as text lines,
     for example a poll on a chat question, the chat on a phone, the words
     inking in, the order-by date if confirmed, and the link sticker's words
     and tracked link.
   - **Facebook Reel** (`facebook`, REEL): a plainer caption for the gift
     buyer, inviting their own dog's story.
   - **TikTok** (`tiktok`, REEL): the caption with the search phrase first,
     and an on-screen hook of 3 to 7 words.
   - **Pinterest** (`pinterest`, PIN), two Pins from the Reel's stills: a
     title under 100 characters, a description under 500 with the search
     phrase, and the tracked link to the most specific page.
   - **Comment prompt** (`instagram`, POST), if the format invites it:
     "Comment your dog's name", with Biscuit's reply pattern for the radar.
4. For the A/B test the canon runs (judged by sends per reach), say which
   angle today's concept tests in the brief's `why`.
5. Headline: the day, the concept and its test, for example "Monday, C04
   'My dog got me a gift' (partner): Reel, Story, FB, TikTok, 2 Pins". Check,
   then post. Add the new creative ids to `local/creatives.csv`, one row
   each, with approval left blank for Krish.
