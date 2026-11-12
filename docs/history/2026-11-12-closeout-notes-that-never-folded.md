# Closeout notes that never folded (4 to 10 Nov 2026)

Nine closeout notes sat in `now-notes/` from 4 to 12 Nov. The closeout fold
(`.claude/hooks/harness-closeout.mjs --fold`, run by "Repository operating context"
on every push to main) takes only `Status:`, `Changed:`, `Next:` and one bare
"North Star check (YYYY-MM-DD): holds." line with no em dash. Each of these broke
that shape (a `#` heading, narrative lines, text after "holds.", an em dash, or
no `Status:` or `Next:`), so the fold refused them and its job failed on every
push to main from 4 Nov. The docs steward left them for a person on 12 Nov.

They were moved here on 12 Nov rather than rewritten and folded: by then every
one of them was superseded by later work already in NOW.md (02r was approved,
02t replaced 02q and 02r's photo rows, F38 and F28 were remade and posted, the
F10 paid pilot was published on 6 Nov, and the skills uplift was merged), so
folding them would have put stale statuses on top of current ones. They are the
record, word for word, except one em dash in a heading, replaced by a colon.
Nothing here is current guidance.

## `now-notes/2026-11-04-group-chat-paid-pilot.md`

Status: The 5 November pilot (docs/boost/2026-11-05-sandbox.md) is ready for a plan decision. F10 has publication receipts on all three channels and its tracked mobile mug path passed. Meta draft and receiving dataset confirmation remain open. Authorized spend is $0.
Next: Verify the unpublished Meta draft and bring its ID, previews, dataset and $25 lifetime cap to Krish for a separate activation decision.
North Star check (2026-11-04): holds. Paid traffic is reported separately from organic net sales.

## `now-notes/2026-11-07-organic-execution-correction.md`

# Organic comedy execution correction

Krish's exact feedback at 2026-11-07T16:26:35Z: "I actually find 3 and 5 the funniest, but none of them are really hilarious in their execution."

Reprioritized OG-03 Cheese radar and OG-05 One stick. The earlier selection of OG-01, OG-02 and OG-04 was a subjective producer judgment, not demonstrated audience performance. Sent a superseding F25–F27 quality hold to Scheduling; its current chat and saved 16:31 UTC receipt acknowledge the hold. Earlier approved posts remain outside this hold.

Two unapproved execution tests were generated and visually inspected:

- `local/organic-comedy-revision-20261107/03-cheese-r2.png`: same wording, exaggerated floppy sleep versus a wide-angle cheese-seeking face.
- `local/organic-comedy-revision-20261107/05-stick-r3.png`: same wording, close crop followed by a huge fallen limb and owner holding the door. The intermediate r2 had a visibly detached upper branch; r3 fixes that continuity error. Preserve r2 as provenance, exclude it from the review selection.

Original generations remain in the Codex generated-images folder; copies and SHA-256 manifest are in the local revision folder. Review candidates have not been uploaded to the release library, scheduled, or approved. A stronger visual does not establish hilarity or organic performance. Next decision is whether either exact execution makes Krish laugh before final platform production.

Taste evidence recorded verbatim as report c94df009-5c5a-4cf3-a800-be20537856ef. Harness observation inbox262 records the execution/ranking correction without asserting an approved taste rule.

## `now-notes/2026-11-08-organic-anatomy-correction.md`

# Organic anatomy correction

Status: Four scenes replaced after Krish's realism/anatomy rejection. Fourteen
exports support fifteen review placements. Stick r3 and social copy unchanged.
No publication, queue mutation, Drive release or paid action.

Next: Krish reviews corrected realism; scheduling retains the hold. Exact
artifacts and remaining native checks are in
`docs/briefs/2026-11-08-organic-anatomy-correction.md` and its JSON receipt.

Changed: Natural sleeping pose, ordinary sofa proportions, threshold hesitation,
natural dog greeting, and source/final-crop anatomy review in `factory/README.md`.
Old brief marked superseded for current artwork.

North Star check (2026-11-08): This improves plausibility of Heartside's organic
creative supply. No engagement or sales effect is established by the correction.
Release remains held pending the actual creative decision.

## `now-notes/2026-11-09-creative-session-archive.md`

# Session closed into Drive : 9 November 2026

Krish requested a complete creative-session archive and shutdown. The isolated destination is Heartside/_Archive/2026-11-09_Codex-Creative-Session_Not-for-Publishing:
https://drive.google.com/drive/folders/1gwVjIYoDAJSEshJ4dBFJ5Sq_XL-rG1GW

START-HERE.md contains the closeout and restart instructions. LATEST-REVIEW.html is self-contained. The archive inventory covers 1,115 files in 29 independently extractable ZIPs, including generated originals, production sources, historical exports, rejected iterations, captions/prompts and repository context. Checksums are in the accompanying inventory and archive manifest. Transfer verification is recorded separately in VERIFICATION.json after the completed Drive readback.

The latest anatomy-corrected five-post batch remains unapproved and held. Stick r3 is unchanged. No live library, queue or paid setting was changed by this closeout. Other sessions' motion work and working-tree edits were left alone. The port-8769 Python review server was already not running at closeout inspection.

Next: reopen START-HERE.md only when Krish resumes this work; resolve creative acceptance before scheduling. No follow-up automation is created.

North Star check (2026-11-09): Preserve recoverable creative work and stop session sprawl. No new reach or sales outcome is claimed.

## `now-notes/2026-11-10-photo-music.md`

Status: All 15 photo posts are now 8 s videos with licensed Epidemic music built in: the seven in 02r plus eight new ones, F52 to F59. They are filed through the library lane (30 files) and listed in Drive Sheet 02t (45 rows; read back 736 of 736 cells). README v5.4 has Codex post every 02t row on all three platforms and replace the 02r photo rows for those seven posts. The new posts run 18 to 28 Nov, with the guest-room and grace posts around Thanksgiving. The F28 howl clip (10 Higgsfield credits; Heartside's share has 8.1 left) waits for Krish. Its song is the joke, so it would go to his phone list.
Changed: photo posts go out as music videos that Codex posts everywhere.
Next: Krish types yes in 02t's approved column; then Codex schedules them.
North Star check (2026-11-10): holds. About 27 posts are ready of the brief's 120.

## `now-notes/2026-11-10-skills-uplift.md`

# Skills uplift: sprint sales made countable (10 November 2026)

Status: built in the working tree on branch `claude/laughing-sagan-8epsdc`, not committed. Every sprint slot now has a deterministic creative id per platform (`factory/sprint.py` `creative_id`, `python3 factory/sprint.py ids`), so `python3 growth.py link <url> S01` gives a tracked link that `check` accepts. `engine/attribution.py` counts an order with a registered discount code in the engine tier under its post family, after the paid checks; the registry `config/codes.json` starts empty. `python3 growth.py codes` drafts 60 post-family codes (tracking words, no discount) for the 20 signature slots, and `docs/briefs/2026-11-10-codes-biolink-survey.md` asks Krish to switch them on with a bio-link page and a one-question thank-you survey. The sprint views log takes optional 3-second rate, average watch, profile visits and link clicks, and `python3 factory/sprint.py diagnose` names the failing stage per franchise with its next test. `growth.py check` refuses five unsourced statistics. The sources digest is `knowledge/corpus/external-growth-skills.md`. Four decisions are queued on `docs/REVIEW-BOARD.md` for a session with leave to write to the board.

Next: Krish answers `decision-switch-on-codes-biolink-survey`; until codes are live, sprint captions that link use `python3 growth.py link <url> <slot>`.

North Star check (2026-11-10): holds. The number (organic net sales, trailing 4 weeks) was not measured in this session and is unchanged; this work makes sprint sales countable once posts go live and codes are switched on, and moves nothing on its own.

## `now-notes/2026-11-10-sprint-wrap.md`

Status: everything filed is ready for Codex. All 21 Sprint posts are in one Sheet, 02q (63 rows, verified cell for cell against the source Sheets), three a day from Wed 11 Nov, with F42 on 27 Nov. Each row's notes give the exact song, start, volume and the stop rule. The new README for Codex adds the evening-before song check, and the old Sheets and README are superseded. All 35 media files are confirmed in Posts/. The hold is lifted and the North Star raised to $50,000, both on Krish's board answers.
Next: Krish types yes in 02q's approved column (63 cells) and runs Codex; wave 3 (F46 onward, 5 reels, stills done) goes through the Codex lane.
North Star check (2026-11-10): holds. Raised by Krish to $50,000 today.

## `now-notes/2026-11-10-state-of-play.md`

Status: Krish approved every row in 02r (M2:M58 = yes) and posted F38 himself. README v5.3 holds F28 (to be redone: two dance trends in two rooms, glitchy) and F34 (Krish posts it later), and has Codex record F38. Codex schedules TikTok song rows in TikTok Studio and every NO SONG row. The 24 Instagram and Facebook song reels are Krish's, from his phone (Sheet 04 and Doc 04a). Credits: Runway account 5; Heartside's Higgsfield share about 16. Of the brief's 120 posts, about 19 are ready. Scripts for the F28 replacement (a beagle howling the falsetto) and a 12-photo batch (F52 onward) are written and go to the judge before any spend.
Changed: holds on F28 and F34; F38 live; floor rule one-trend-one-scene.
Next: judge the 13 scripts; make only the 9s (F28-howl about 9 Higgsfield, photos 0.25 each); file them and give Codex a new Sheet and README.
North Star check (2026-11-10): holds. 19 of 120 posts ready; the credit pools, not the scripts, now limit the volume.

## `now-notes/2026-11-10-wave-3-judged.md`

# Wave 3 judged: two 9s on the board, three held

Status: Codex built F46 to F50 (card dog-things-wave-3), and fix card dog-things-wave-3-fix1 rescaled F50's
Christmas card so it reads on a phone. The tier 2 judges (docs/HUMOUR.md, against F38 to F40) scored F48 "Day in the
life of a CEO" 9, F49 "What's in my carry-on" 9, F46 "What I eat in a day" 8, F47 "GRWM: Christmas photo day" 8
and F50 "Christmas card, take 47" 7. F48 and F49 are on the review board (post-F48, post-F49), proposed for
18 and 19 Nov at 12:30 ET. The three below 9 are held. Board item held-wave-3 asks whether to rework them: F47
re-cut free, and F46 and F50 with one new Runway clip each. The Codex spend 1cfc68d6 is settled at 1. Media stays
in the session scratchpad until Krish says yes.

Judge lessons for the next wave:
- end on the cruel payoff, with the dog in on it (a flat stare);
- a product ending must not steal the last laugh;
- the product render's dog should match the reel's breed, or the story breaks;
- every beat needs a laugh; drop filler beats.

Next: on Krish's Yes to F48 and F49, file them through factory/send_library.py, create Sheet 02r with song notes
("Money", Pink Floyd, from 0:00; "Leaving on a Jet Plane", John Denver, from 0:00; both song 100 / reel 0), and
update DRIVE-MAP and the sprint manifest.

North Star check (10 Nov): holds. Two more viral posts ready for approval toward the 100.
