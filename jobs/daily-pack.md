# Job: the day's pack (every day)

Kind `daily`. Parts 3 and 6 in `PLAYBOOK.md`. Deliver finished media for
Krish to review and post. Read `docs/ENGINE.md` for the template and limits.

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
   - the one signal it should move (sends, link taps, orders);
   - the copy diagnosis (`knowledge/COPY-DOCTRINE.md`, section 9, "Before
     drafting"): each edition's awareness level and lead type, the one
     promise and scene, and the proof with its fact source.
   Then run **reel-script** (docs/CHANNEL-TASKS.md): write 5 hook options
   for the concept (first frame, works muted), pick the strongest, and note
   why it beats the other four for the one signal. Put them in the brief as
   note lines `Alternative hook 1:` to `Alternative hook 5:` and
   `Picked hook: <n>, because <reason>`. The picked one becomes the brief's
   `Hook:` line and passes the copy rules.
3. Draft, one item each, each with its own creative id (PLAYBOOK, "Creative
   ids"). Every heartside.io link is tracked (`python3 growth.py link`). Keep
   the idea the same in every edition. Change the opening frame, hook
   wording, caption, cover and call to action to suit the platform. Never
   paste the same text twice.
   - **The brief** (`platform: other`). It includes:
     - the hook (first frame, works muted);
     - a beat sheet with times, and a shot list;
     - on-screen text and any voiceover;
     - the source assets from heartside's library;
     - how the real print files appear;
     - what must not appear: AI customers, the product drawn by AI,
       invented reactions.

     9:16, with text inside the safe zone. Start every line the public will
     see or hear with `Hook:`, `On screen:`, `Voiceover:`, `Buddy:`,
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
     "Comment your dog's name", with the reply pattern for the radar.
4. State the test in the brief's `why`, in the test record shape
   (`knowledge/COPY-DOCTRINE.md`, section 8): question, mechanism, control,
   the one changed variable and the signal. Test current recognition stories
   and gift proof. V3 rejected the HR builder, so the older roast-versus-
   love-letter instruction must not revive it. Judge sends per reach
   alongside useful visits and purchases when observed.
5. Write the production spec under `local/specs/`, using
   `campaigns/waits-at-the-door.json` as the schema. A scheduled run never
   edits that tracked file. Keep the visible detail true to its approved
   example product. A verified buy spec can declare the current single-unit
   offer of a gift the film shows and its exact product destination; use
   {link} in captions for per-creative tracking. Run `python3 growth.py render <spec>`. It produces native audience films with restrained motion, an original local
   score, cover, carousel, Stories, Pins and subtitles. Approved narration can
   be attached with verified provenance. Connected provider jobs use the budget
   and receipt contract in docs/PROVIDERS.md; no paid generation is automatic.
6. **caption-set** for each edition (docs/CHANNEL-TASKS.md): before choosing
   its caption, write it five ways (story, practical, a plain opinion, the
   buyer's problem, step by step), pick one for that platform's signal, and
   record the other four in the brief as note lines `Alternative caption
   (<platform>, <way>):` with `Picked caption (<platform>): <way>, because
   <reason>`. These hooks and captions are the alternatives the creative
   review cites before any go-live.
   Before `check`, run edit passes A to E and score the rubric
   (`knowledge/COPY-DOCTRINE.md`, section 9). Rewrite or drop any edition
   under 28 of 48. Add `Rubric: total/48, weakest link: <link>` as a note
   line in the brief.
   Keep the renderer's production manifest and native creative IDs. Use
   its printed draft path for `growth.py check` and `post`. Incorporate
   additional checked briefs or comment items if needed. Missing or
   changed media makes the daily pack incomplete; report the exact
   failure rather than calling a text brief ready. Revisions are saved
   in `local/engine.sqlite3` automatically.
7. Headline: the day, the concept and its test, for example "Monday, C04
   'My dog got me a gift' (partner): Reel, Story, FB, TikTok, 2 Pins". Check,
   then store with `growth.py post <printed-draft-path>`. Include the media
   paths and whole pack in the final message. Record actual publication
   afterward with `growth.py creatives mark`. A generated file is not
   published. `local/creatives.csv` is legacy history, not evidence that
   these new files were posted.
