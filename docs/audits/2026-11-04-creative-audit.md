# Creative audit: every motion and social asset (4 Nov 2026)

Krish asked on 4 Nov for an audit of every motion creative asset: Codex's builds, this session's clips, the previous session's clips, and every finished creative. The bar is "ready to be published and 10 out of 10 in every way", to delight people and convert them to Heartside, before any paid boost.

The short answer: **none of them is a 10 yet, and none should be boosted as it stands.**
- **Ready organically:** all 12 locked reels are now checked frame by frame. Eight score 8 or more and can keep going out unpaid: F01, F02, F04, F05, F06-frenchie and F12, plus F03 and F07 at 7 to 8. The best are F12 and F05 (9).
- **For boosting** (Krish, 4 Nov: boosts run the live organic post, so the organic score is what is boosted; the ad-version gaps below no longer apply): see `docs/PAID-BOOSTS.md`. Originally: **not ready for paid:** every asset fails at least one paid requirement. The failures are subtitles in Meta's no-text zone, no call-to-action end card, and Runway clips at 720p. (The music licence is settled: Krish, 4 Nov.)

## What was checked, and how

| Source | Assets | How they were checked |
|---|---|---|
| Drive `05_Social-Library/Posts/` (locked library) | 12 reels, 12 covers, 15 carousel slides, F13 photo | **6 reels in full:** F06-frenchie, F06-dachshund, F06-lab, F07, F10, F11. Each was downloaded and run through `factory/lock.py media` (size, sound, length, loudness), then read as a 16-frame contact sheet (0, 0.5, 1 and 1.5 s, then every ~1.5 to 3 s). **All 12 covers** were read. **The other 6 reels** (F01, F02, F03, F04, F05, F12) are over the Drive connector's size limit. They were read the same way, after downloading them from the engine library (`GET /api/library/file` on the engine key, the route content-engine built for cloud sessions). Each one's SHA-256 matched the library's record. |
| Codex motion candidates (private board) | F04, F05, F12 motion reels; F12 Facebook pair A (parcel first) and B (guard first) | Not reachable from this session: they are in Codex's private workspace. The record is `docs/HANDOFF.md` on `codex/nov-04-motion-production-record` (SHA-256s listed there). They need the same checks, run by Codex. |
| Runway clips (this session and the one before) | 18 Gen-4.5 clips, 5 s, 720x1280 | Every clip was compared with its Higgsfield source frame, then sampled at 6 points with closer looks. Verdicts are in `docs/history/2026-11-04-runway-motion-verdicts.md`: 15 pass, 8 of them only inside a cut window; 3 are held. |
| Captions and schedule | `02` and `02c` Schedule sheets, `01 Posting strategy` | Read live from Drive on 4 Nov. |

Live evidence used: Codex's 3 Nov early audit in the `02` Sheet. F10 had 26 TikTok views and 0 likes. Facebook showed 2 views, "largest drop at 0:01". There was no clickable Heartside website link on the TikTok profile, and no attributed shop session.

## The bar (what a 10 means here)

A 10 passes every line below. Each line comes from this repository's own doctrine: `factory/lock.py` STANDING, the `01 Posting strategy` humour bar, AGENTS.md rules 3 to 5, and `docs/CHANNEL-TASKS.md`. Platform safe zones come from Meta's ad guidance.

1. **Hook in the first second.** Motion and a legible situation on frame 1. No blank screen, no tiny subject, no static photo for 2 s.
2. **A laugh every 3 to 4 seconds**, funny with the sound off, in the dog's blunt voice. No swearing (AGENTS.md rule 5).
3. **The payoff is the real product, for the same dog.** The ending must be the live store's own render, of the breed and coat the viewer just watched. That is what makes "your dog loves you too" land.
4. **One cast and one setting, with no AI artifacts.** That covers STANDING: no added limbs, no warped text, no stray humans.
5. **Copy passes house rules.** US spelling, no exclamation marks, no em dashes or dash substitutes, grammatical lines, no slogans, URLs or prices on screen in organic posts.
6. **Platform fit:**
   - text clear of the interface: organic Reels and TikTok keep the bottom ~20% and the right ~12% clear; paid Reels keep the top 14%, the bottom 35% and the sides 6% clear;
   - the cover reads in the 3:4 grid crop;
   - 1080x1920, -18 to -13 LUFS;
   - 15 to 30 s for paid.
7. **Ready for paid** (only when boosting):
   - the music is the locked track (licence settled by Krish, 4 Nov);
   - there is a call-to-action end card for the product shown;
   - AI-generated content is labelled where the platform requires it;
   - the destination is the product shown, with paid UTMs.

## Scores: all 12 locked reels, checked frame by frame

Scores run 0 to 10. "Organic" is the post as it is today. "Paid" is the same file used as an ad.

| Post | Hook | Laughs | Payoff | Craft | Copy | Fit | Organic | Paid | Must fix |
|---|---|---|---|---|---|---|---|---|---|
| F06-frenchie roast | 7 | 8 | 9 | 8 | 9 | 8 | **8** | 5 | The first 2 s are a still. Swap in the passing Runway frenchie opener (0 to 2.5 s). Check 5.8 s for a sliver of human arm at the right edge. Paid needs a CTA end card. |
| F06-dachshund roast | 7 | 8 | **4** | 8 | 9 | 8 | **7** | 3 | **The payoff is the wrong dog.** The roast stars a black-and-tan dachshund, but the end mug (`mug-real-dachshund.jpg`) is a chestnut dachshund in a green sweater. Use the passing Runway opener. Ask heartside for a black-and-tan dachshund store render, or recast the roast to match. Keep it organic only until then. |
| F06-lab roast | 7 | 6 | 8 | 8 | **5** | **6** | **6** | 3 | Two lines miss the bar. "I KNOW WHERE THE TREATS ARE FYI - TOP RIGHT CUPBOARD." uses a spaced hyphen as a dash. "YOU ARE MY FAVORITE HUMAN, THAT I SPEND TIME WITH EVERY DAY, AND ISN'T THE MAILMAN." does not parse. The cupboard caption sits in the bottom ~20%, under the platform interface. The fix needs new lines through the bank (Krish approves) and the caption moved up. |
| F07 art critic | **4** | 8 | 10 | 8 | 9 | 7 | **7** | 4 | **The weakest open in the set.** For 2 s the dog is small in a wide static shot, under "Hmm.", and the cover is the same frame. The passing Runway sniff clip can replace the 3.5 to 8 s still. The opener needs a new close-up hook (the Runway F07 hook was held). The payoff, the portrait on the wall, is the best in the library. |
| F10 group chat | **2** | 7 | 8 | 8 | **4** | 6 | **5** | 1 | **The first second is a blank screen.** Facebook's own retention shows its largest drop at 0:01. It says "WTF" four times, a swear acronym (rule 5), plus "mate" (not US voice). At 39 s it is long. The cover is almost blank. It is already live (3 Nov), so leave that post. The recut should open with three messages already on screen, replace the WTFs with an approved line, and trim to under 30 s. Never boost the current cut. |
| F11 search history | 6 | 8 | 8 | 8 | 9 | 7 | **7** | 4 | It opens on an empty search bar. Start mid-typing, with "how to say I love you without thumbs" already half typed. The cover is mostly blank, so use the "genius." and mug frame instead. The final search reads "n a mug: weird or genius" (cut off at the start), which looks like a typo. |
| F01 becoming the mug | 6 | 9 | 9 | 9 | 7 | 6 | **8** | 5 | The first 4.7 s are one still. The passing Runway hook clip (0 to 4.0 s) fits that exact shot. "Oh, [bleep] it. I'm going in." implies a swear (rule 5: "never a swear word"). Krish locked it, so flag it only for paid use. Subtitles sit at 78 to 90% of the height. |
| F02 project nothing | 6 | 9 | 9 | 8 | 9 | 6 | **8** | 5 | The first 4.7 s are one still; the passing Runway hook clip fits it. "It's me, on a mug. They have to look at me every single morning." is the best product line in the library. Subtitles sit in the bottom zone. |
| F03 operation stocking | 6 | 7 | 8 | 8 | 9 | 7 | **7** | 4 | The first 3.7 s are one still; the Runway hook clip passes for 0 to 3.5 s. It ends on the shepherd portrait. Funny, but fewer laughs per second than the best. |
| F04 me vs my golden | 6 | 8 | 9 | 8 | 8 | 5 | **8** | 4 | The first 3.9 s are one still. The meme captions at the top sit inside the paid no-text zone (top 14%), and "me: fine, I'll sit on the edge" sits at 90% of the height, under the interface. The golden blanket payoff matches the dog. |
| F05 court of the couch | 7 | 9 | 9 | 9 | 9 | 7 | **9** | 5 | The courtroom reads instantly, though the first 4.5 s are one still. Every shot is the same frenchie, and it ends on the frenchie blanket in the same blue bow tie. At 30 s it is at the paid limit. |
| F12 head of security | 7 | 9 | 10 | 9 | 9 | 7 | **9** | 6 | The best reveal in the library: "Oh. It's me." on its own portrait. At 18.5 s it suits paid. The first 2 s are one still (Krish has already approved the guard-first opening for paid). Subtitles sit in the bottom zone. |

All twelve pass `factory/audit.py` (except F10 and F11, flagged for a blank first frame) and `factory/lock.py media`: 1080x1920, sound, 6 to 60 s, loudness inside -18 to -13 LUFS. The end-card check could not run here, because the build's `end.png` lives on the build machine.

## Covers (all 12)

| Cover | Verdict | Why |
|---|---|---|
| F01, F02, F03, F05, F06 x3, F12 | Pass | Each reads as a story in one glance: PLAN C, GIFT IDEAS with "the neighbor's cat", the heist plan, the courtroom, the roast faces, the security vest. |
| F04 | Fix | "my golden:" sits at 92% of the height, which the 3:4 profile-grid crop cuts off, so the joke vanishes on the grid. |
| F07 | **Fail** | A small dog and "Hmm." There is no reason to tap. |
| F10 | **Fail** | 90% blank chat window. |
| F11 | **Fail** | 85% blank search page. |

## Systemic findings (they affect every post, not one)

1. **Subtitles sit in the bottom zone.** The film template puts subtitles at y=1440 of 1920 by default (`factory/build.py` line 289), and F01 and F04 put some at 1500 to 1720.
   - Organically, 1500 and below collides with the username and caption overlay.
   - For any ad, everything under y=1248 is in Meta's no-text zone (the bottom 35%).
   - **Fix:** paid cuts use `cap_y` ≤ 1150. The organic default should move to ~1300.
2. **No first-second motion on the roasts and the chat.** The roasts open on a still, the chat and the search on an empty interface. The Runway openers exist to fix this (F06 x3 pass).
3. **The product payoff must match the dog.** F06-dachshund breaks it. F11 and F10 are fine, because their ends show the dogs of the story. The factory checks breed but not coat: add a `coat` tag to `factory/bank/renders.json` and to specs.
4. **The paid-readiness gaps are the same for every asset:**
   - **Music licence: closed.** Ruling (Krish, 2026-11-04): "Just use the music. I have the right license for the post type. Mark this as complete permanently." It is never raised again.
   - **No CTA end card:** organic posts end on the product with no words, by Krish's rule. An ad needs the product name and a reason to tap (Codex's motion cuts already add "Make yours at Heartside.io"). That makes paid cuts separate creatives that need their own approval.
   - **AI labelling:** the dogs are photorealistic AI. TikTok requires its AI-generated-content label on realistic AI media, and Meta applies "AI info" labels. Set the label at upload; never hide it.
   - **720p clips:** the Runway clips are 720x1280. Cutting them into 1080 masters softens them, so upscale before cutting (Runway `upscale_video` or Topaz). The 18 remaining Runway credits will not cover that.
5. **Resolved 4 Nov: chat approval counts** (Krish: "Yes to all your 4 questions"; AGENTS.md now says so). The original finding was **the approval column is empty.** Every row in `02c` has a blank `approved` column while the notes say "Approved in chat", and posts are going out through Buffer. The Drive map says Codex posts only rows Krish marked `approved = yes`. Either the README rule changed, or rows are going out unapproved. **Krish should rule on which.**
6. **The TikTok profile has no clickable website link** (Codex audit, 3 Nov). Any TikTok spend before that is fixed is wasted.

## What has not been verified (open, not passed)

- **Codex's motion candidates are unchecked:** F04, F05 and F12, and the F12 A and B pair.
- **The 15 passing Runway clips have not been checked at full frame rate.**

Codex runs `python3 factory/audit.py <folder>` on every master (see `docs/briefs/codex/2026-11-04-boost-library.md`) and records full-rate verdicts against the bar above. Until it does, none of these is "ready".

## Fix list, in order of value

| # | Fix | Owner | Needs |
|---|---|---|---|
| 1 | ~~Music licence for paid~~ Done: Krish, 4 Nov, "I have the right license for the post type". Closed permanently | Krish | None |
| 2 | Recut the F10 opener (no blank first second, no "WTF"), keeping it under 30 s; same for F11's empty search bar | Factory rebuild of the chat and search templates, with new lines from the bank | Krish approves the replacement lines. A 0.4 to 0.6 s trim was tried and still fails the dead-open check, because the templates start on an empty screen |
| 3 | Fix the F07, F10 and F11 covers (a frame with a story in it) | **Built 4 Nov in session**, awaiting Krish's lock | `local/library/2026-11-04-motion/`. F04's caption falls outside the 3:4 crop in every frame, so its cover is unchanged |
| 4 | Motion into F01 (4 shots), F02 (opener), F03 (4 shots), F06 x3 (openers), F07 (sniff) | **Built 4 Nov in session** with `factory/splice.py` and `factory/motion/<id>.json`, awaiting Krish's lock | Words and caption layout redrawn with the factory's own code; the audio is the master's, unchanged; all pass `factory/audit.py` |
| 5 | Paid cut spec: captions ≤ y 1150, a 3 s CTA end card ("Personalized [product] from your dog's photo" plus the product render), 15 to 30 s | Codex | Krish approves each paid cut |
| 6 | F06-dachshund product match | heartside build session (a black-and-tan dachshund render) | heartside |
| 7 | F06-lab line replacements | Engine proposes, Krish approves | `factory/bank/lines.json` |
| 8 | TikTok profile link | Krish | His account |

North Star check (2026-11-04): this audit moves "every winning format found by this engine and approved by Krish in one press". The number has not moved.
