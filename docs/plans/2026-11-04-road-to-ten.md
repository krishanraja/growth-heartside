# The road to 10: every post (4 Nov 2026)

Krish, 4 Nov: "Yes, we need them all to be 10 out of 10. Where are your standards?" Then: "We need to get as close as we can without regenerating absolutely everything. We've run out of runway credits, but still have higgsfield and openai images."

The bar is the one in `docs/audits/2026-11-04-creative-audit.md`. Scores marked "now" are the audit's; "after" is what the fix in this table earns, judged against the same bar. Nothing here is locked until Krish says so.

## Done in session (4 Nov), waiting for Krish's lock

The candidates are in `local/library/2026-11-04-ten/`. Each one passes `factory/audit.py`, which checks naming, 1080x1920, sound, length, loudness and the open.

| Post | Now | After | What changed |
|---|---|---|---|
| F06-dachshund | 7 | 9 | **The payoff is now the same dog.** The four roast frames were recast from black-and-tan to the chestnut red dachshund on `mug-real-dachshund.jpg`, keeping the pose, set, light and lines. The reel, slides 1 to 4 and the cover were rebuilt. This replaces the wait for a new heartside render. |
| F04 | 8 (motion held) | 9 | **One room, one light, start to end.** Krish's note was "chops a bit ... scene progression". The edge, push-off and floor shots were in a different, daylit room. They were redrawn in the opening's room and late sun, with the same golden and red collar. Captions sit at the top, and the narrator's line at 1300. Built on the organic finish, so it has no on-screen CTA. |
| F06-lab | 6 | 9 | **The two weak lines, fixed** (proposed lines; Krish approves): "I know where the treats are. Top right cupboard." and "Of everyone I see every day, you're my favorite. Sorry, mailman." The old text was removed from the frames, not covered over. The cupboard line now sits above the caption zone. The reel and slides 3 and 4 were rebuilt. |
| F07 | 7 | 9 | **The open is a hook.** Frame 1 is now tight on the doodle's face, then pulls back to the gallery over 2 s. Before, the open was a small dog in a wide static shot. The old caption box was removed from the frame first. The locked sniff clip and payoff are unchanged. |

Spend: 9 Higgsfield GPT Image 2.5 edits at high quality, 2k (24.75 credits; balance 2,402.85 to 2,378.10). No Runway.

## The factory now prevents these faults (merged on this branch)

- **Chat** (`open_with`): frame 1 already shows the first messages. No blank first second (F10).
- **Search** (`open_typed`): frame 1 is mid-typing. A finished query is shown whole, never cut off at the start (F11's "n a mug: weird or genius").
- **Film** (`pull`): a frame can open tight on its subject and pull back. The default caption moves from y 1440 to 1300, clear of the Reels and TikTok caption and username zone. `factory/splice.py` follows the same default.
- **Roast**: bottom text ends at 76% of the reel height, above the interface.

## Waiting on Krish's words (approve or kill)

| Line | Replaces | Post |
|---|---|---|
| F10.c15b "sorry, WHAT" | "WTF" | F10 |
| F10.c18b "somehow worse" | "still WTF" | F10 |
| F10.c28b "They threw it AWAY 😂😵" | "They threw it AWAY mate 😂😵" | F10 |
| F06.kla2b "I know where the treats are. Top right cupboard." | "I know where the treats are FYI - top right cupboard." | F06-lab |
| F06.kla3b "Of everyone I see every day, you're my favorite. Sorry, mailman." (or F06.kla3c "You're my favorite human. Don't tell the mailman.") | "You are my favorite human, that I spend time with every day, and isn't the mailman." | F06-lab |

## Built on the home machine by Codex (the music, voices and renders live there)

Card: `docs/briefs/codex/2026-11-04-road-to-ten-builds.md`.

| Post | Now | After | Build |
|---|---|---|---|
| F10 | 5 | 9 | The spec is ready: it opens with 3 messages on screen, has no WTF and no "mate", and runs 28.7 s (was 38.8). Needs the three F10 lines approved. |
| F11 | 7 | 9 | The spec is ready: it opens 60% into the first search, and the last query shows whole. All its lines are already approved; it needs only a relock. |
| F12, F05 | 9 | 10 | Rebuild the masters with captions at 1300, then lay the locked motion over them again (Codex's own plans, with `cap_y` 1300). |
| F01, F02, F03 | 8, 8, 7 | 9 | The same caption rebuild, then `factory/splice.py` with `factory/motion/F0x.json`. F01's "[bleep]" line is still flagged for paid only. |
| F06-frenchie | 8 | 9 | Check 5.8 s for the sliver of a human arm. If it is there, edit it out of that one frame. |

## What still keeps a post below 10

- **The Runway clips are 720p**, so the motion shots are softer than the stills. Higgsfield upscale_video can fix this. Price it per clip before spending.
- **F03's laughs per second.** It needs a new joke, which means new lines and a new voice read. That is a creative decision for Krish, so it is not in this pass.

## The queue

Posts already queued in Buffer go out as they were locked (Krish, 4 Nov: no queue edits). The next five below the bar:
- F11 and F07, 5 Nov;
- F06-dachshund, 6 Nov;
- F03 and F06-lab, 7 Nov.

Only Krish can pull or pause them. If he does, the 10/10 versions replace them through new schedule rows once locked.

North Star check (2026-11-04): this moves "every winning format was found by this engine and approved by Krish in one press", because every asset gets to its best version before more reach is bought. The number has not moved.
