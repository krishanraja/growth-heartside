# The road to 10: every post (4 Nov 2026)

Krish, 4 Nov: "Yes, we need them all to be 10 out of 10. Where are your standards?" Then: "We need to get as close as we can without regenerating absolutely everything. We've run out of runway credits, but still have higgsfield and openai images."

The bar is the one in `docs/audits/2026-11-04-creative-audit.md`. Scores marked "now" are the audit's; "after" is what the fix in this table earns, judged against the same bar. Nothing here is locked until Krish says so.

## Done in session (4 Nov): locked and filed

Krish approved the lines and locked all four reels ("1. approved 2. approved"). The 11 files were filed through the library lane to `Posts/<id>/` under their plain names. Each sha256 was read back from the library and matched. `library/manifest.json` lists them as locked and the files they replace as superseded. Each one passes `factory/audit.py`.

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

## Lines approved by Krish on 4 Nov ("1. approved")

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

## F03, finished without a new voice read (waiting for Krish's lock)

F03 scored 7 because its laughs were thin. Three meme labels now land between the narrator's lines, in F04's "my golden:" format; no new voice is needed.

| When | Label | Why it is funny |
|---|---|---|
| 0 to 4.4 s | "Operation Stocking" | Frames the heist in the first second |
| 10.7 to 13.3 s | "The beagle:" | The narrator says nobody touches the cookies; the beagle is already holding one |
| 14.6 to 16.3 s | "The gift:" | Sets up the cut to the shepherd's portrait of itself |

The lines are proposed in the bank (F03.l1 to l3). The cut is `local/library/2026-11-04-ten/heartside_F03_operation-stocking_reel.mp4`, laid on the locked motion version (`factory/motion/F03-labels.json`). Score: 7 now, 9 after.

## What still keeps a post below 10

- **The Runway clips are 720p**, so the motion shots are softer than the stills. Higgsfield upscale_video can fix this. Price it per clip before spending.

## The queue (the engine's call, Krish: "you chose")

The engine leaves the Buffer queue as it is. Krish ruled out queue edits on 4 Nov, after a media swap broke a post. A pause or delete is still a queue edit, and both are harder to undo than letting an approved post run.

So F11 and F07 (5 Nov), F06-dachshund (6 Nov), and F03 and F06-lab (7 Nov) go out as they were locked. The new versions go out through new schedule rows: Codex adds them from the locked files, and Krish approves them in chat.

The one exception is Krish's to make. F06-dachshund's queued post ends on a dog of a different coat. If he wants it held, he can pause it in Buffer himself in one click.

North Star check (2026-11-04): this moves "every winning format was found by this engine and approved by Krish in one press", because every asset gets to its best version before more reach is bought. The number has not moved.
