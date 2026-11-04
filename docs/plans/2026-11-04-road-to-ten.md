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

## The queue: swapped to the locked files (Krish, 4 Nov: "Swap them here")

Krish chose to swap the queued posts in this session, using permanent links and checking each one back. The swap Codex tried earlier failed because Buffer was pointed at a signed library link that expired after an hour. These links do not expire.

- **Hosting.** Each locked reel was uploaded to Higgsfield's CDN (`d2ol7oe51mr4n9.cloudfront.net`), then fetched publicly and hashed. All seven matched the locked sha256.
- **The swaps.** 20 Buffer posts now point at the locked files: F07, F06-dachshund, F12, F04, F03, F06-lab and F05, on TikTok, Instagram and Facebook. One post (F07 TikTok) was tested first.
- **The checks.** Every edit was read back: the post stays scheduled, the caption and time are unchanged, and Buffer read the new file's length and rendered its thumbnail.
- **F10.** The three 8 Nov posts of the old cut (the "WTF" version) are now drafts, so they do not publish. They come back when the new F10 is built and locked.
- **Already right.** F06-frenchie and F02 already carried their locked motion versions, and F11 its locked file. Those posts were not touched.
- **One risk left.** F06-frenchie (4 Nov) and F02 (5 Nov) are hosted on Codex's review server (`heartside-review.5-161-56-37.sslip.io`). If that server is down at publish time, those posts fail.

| Post | Permanent media URL |
|---|---|
| F03 | https://d2ol7oe51mr4n9.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/c842c532-7295-4d93-8fea-fbc4a03015ae.mp4 |
| F04 | https://d2ol7oe51mr4n9.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/bfbc4e48-4216-488b-af80-c58d6806ee20.mp4 |
| F05 | https://d2ol7oe51mr4n9.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/8829a1e6-2e9b-406d-8d71-c7db0bb7c5b7.mp4 |
| F06-dachshund | https://d2ol7oe51mr4n9.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/ba09c664-11b4-48a5-ad8f-e9e777ffcc27.mp4 |
| F06-lab | https://d2ol7oe51mr4n9.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/8cb7c62f-6f61-4c29-8464-5f27767c36cb.mp4 |
| F07 | https://d2ol7oe51mr4n9.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/cb4aebad-bc5a-4d25-abd0-e009d0b3ecfa.mp4 |
| F12 | https://d2ol7oe51mr4n9.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/41239328-d0c2-485b-86f3-64c5fe1ad1bc.mp4 |

## Still open after this session

- **F10**: Codex builds it from the card (the music and avatars are on the home machine), Krish locks it, and the three drafts get its file.
- **F11**: its new cut (opens on the first joke, last query whole) is in `Posts/F11/` as a `review-reel`, waiting for Krish's lock. The audit's blank-open check still flags the light canvas (pixel spread 26 against a threshold of 30). The queued F11 is the old locked cut.
- **F01, F02, F03, F05, F12 captions at 1300**: a Codex rebuild.

North Star check (2026-11-04): this moves "every winning format was found by this engine and approved by Krish in one press", because every asset gets to its best version before more reach is bought. The number has not moved.
