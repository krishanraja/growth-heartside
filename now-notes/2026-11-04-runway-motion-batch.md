# Runway motion batch for the locked posts (4 Nov)

Status: 16 Runway Gen-4.5 motion clips are made: 5 seconds, 9:16, 720p, 60 credits each. Each one animates a locked post's own Higgsfield key frame and is reserved and settled in Control Center. Krish's ask was "Use the locked frames", and later: "as much coverage in-market as possible". The aim is that every locked story post opens on motion.

All 16 clips have now been checked against their frames: 13 pass, 7 of them with a cut, and 3 are held (see "Verdicts"). Nothing is posted, and the Drive originals are untouched. Runway has 138 credits left, which are wiped on 7 Nov.

Codex's earlier motion reviews of F04, F05 and F12 are on the owner board and are not part of this batch.

| Post | Shot | Runway task | Source frame (Higgsfield) |
|---|---|---|---|
| F01 | hook: watching the person scroll | 4c40db4f-3cc6-4290-81e3-c3730ae284c9 | 8d64a03f |
| F01 | PLAN C grin | 619adae2-53b8-40c0-8266-06c7f6358b8b | 3775d7f4 |
| F01 | leap into the steam | 530b6cd1-365c-428f-aabc-f7746dc81744 | c7b06196 |
| F01 | wink (checked) | 70c9d3b7-cdb0-4430-93e2-97bca205d816 | 58030530 |
| F02 | hook: 3 am at the laptop | a7917d0e-5bf2-4b3a-985d-c821e9aa972c | 3ee78066 |
| F02 | jolts awake | ec79a000-a3f7-4f4a-bd08-b2ce13b2f501 | ff162e1c |
| F02 | end grin | b258c062-b38a-4983-bad0-bb76de514250 | 77eb86f6 |
| F03 | hook: shepherd over the floor plan | e164f8a2-c3d2-4518-b1f2-24bbf79b805b | 795e8f29 |
| F03 | beagle caught with a cookie | b0aef47a-5dac-4a3f-be39-006edd32e71b | 7c78a174 |
| F03 | gift under the tree | 4346ebc6-8181-4103-b9f3-b30a4b30617f | be715f57 |
| F04 | asleep in the spot (spare) | 7ae3cef0-95a4-48f6-8d36-12ed8150d359 | 57cb256c |
| F06-frenchie | opener | e957b2e5-5802-4c5d-b820-7d09d4fa0f3c | b2fc01b7 |
| F06-dachshund | opener | dc90e0e7-887e-4cce-b6b9-2cbd2b586ca0 | 2864f113 |
| F06-lab | opener | e24c6b21-fb3a-4ca2-9893-f70bd3fc6946 | a7fd8925 |
| F07 | hook: doodle in the turtleneck | 43efbb93-a331-4a2a-8007-5522850602a5 | 25e48897 |
| F07 | sniffs the frame | b91acfda-ccbe-41fe-b9b2-699fdb4b494c | 23fd74cb |

Each clip's Runway URL comes from `get_task` with its task id. Each frame's URL comes from Higgsfield `show_generations`.

## Verdicts (4 Nov, checked against the source frames)

How it was checked:
- **The source frame.** Each clip's first frame was compared with its Higgsfield frame, both scaled to 90x160, by mean absolute pixel difference.
  - Thirteen clips scored 2.0 to 3.0 out of 255, so they start on the stated frame.
  - The three F06 openers scored 27 to 33, because their sources are 4:5 (1792x2240) and the clips are 9:16 crops of them. Side by side, the dog, wardrobe and room are the same. The lamps and cushions that come into view later are already in the 4:5 source.
- **The motion.** Each clip was read at 0, 1, 2, 3, 4 and 4.9 seconds, with closer looks at the doubtful moments.
  - A one-frame flicker between those samples could be missed.
  - Codex's full-rate review is the final check.

"Use" is the window to cut. Everything outside it is dropped.

| Post | Shot | Verdict | Use | Why |
|---|---|---|---|---|
| F01 | hook: watching the person scroll | pass | 0.0-4.0 s | Same dog, sweater, person, mug and kitchen. From about 4.5 s the dog walks into the lens and fills the frame. |
| F01 | PLAN C grin | pass | 0.0-5.0 s | The dog licks the chart edge at about 1 s, and the drawing and "PLAN C" stay unchanged. Its tail coming into view is natural. |
| F01 | leap into the steam | pass | 0.0-3.0 s | After about 3.5 s the dog is gone into the steam, and the table turns into a dark counter slab. |
| F01 | wink | pass | 0.0-3.5 s | Rechecked. After about 4 s the camera swings into a blurred close-up of the sweater. |
| F02 | hook: 3 am at the laptop | pass | 0.0-5.0 s | Same golden, glasses, red collar, clock and room. No text appears. |
| F02 | jolts awake | **hold** | none | The ears flare into wing shapes at 1-2 s, and the red collar is gone from about 3 s (a wardrobe change). |
| F02 | end grin | **hold** | none | The on-screen text mutates within 1 s, from "Consultant has left the meeting" to "Coneultant hes left the meeting". |
| F03 | hook: shepherd over the floor plan | pass | 0.0-3.5 s | Same shepherd, beanie, pointer, plan and "DO NOT TOUCH" card. After 3.5 s it walks onto the plan and the close-up crops it. |
| F03 | beagle caught with a cookie | pass | 0.0-5.0 s | Both dogs, the goggles, the beanie, the "For Santa" glass and the room all hold. |
| F03 | gift under the tree | pass | 0.0-2.5 s | At about 3 s it jumps to a different shot: the dog stands front-on, the beanie loses its paw patch and the present moves. |
| F04 | asleep in the spot (spare) | pass | 0.0-2.0 s | After 2 s the dog sits up (off brief) and jumps to a close-up on the armrest. It is a spare only. |
| F06-frenchie | opener | pass | 0.0-2.5 s | At about 3 s the bow tie nearly vanishes under the chin before it comes back. |
| F06-dachshund | opener | pass | 0.0-5.0 s | Same dog and couch. The lamp glow on the right is in the 4:5 source. |
| F06-lab | opener | pass | 0.0-5.0 s | Same dog and red bandana. The lamp and the plaid cushion are in the 4:5 source, and the expression changes at 3 s. |
| F07 | hook: doodle in the turtleneck | **hold** | none | At about 1 s it cuts to a close-up with pink mirrored lenses (a wardrobe change). It ends on a wide shot with new artworks on the wall. |
| F07 | sniffs the frame | pass | 0.0-5.0 s | The glasses, turtleneck, glass and "UNTITLED (VERY GOOD BOY)" label all hold. |

None of the 16 clips adds a product, a hand or a limb.

Result:
- **13 pass.** Seven of those pass only with a cut.
- **3 are held:** F02 jolt, F02 end grin and F07 hook.

Coverage after this check:
- F01: 4 shots.
- F02: 1 shot (hook).
- F03: 3 shots.
- F06: all 3 openers.
- F07: 1 shot (sniff).

That is why the two clips still to make are F02's whiteboard and F03's tiptoe.

## The last two clips (not made yet)

The source frames are confirmed in Higgsfield, both 1520x2688:
- **F02 whiteboard (`c9bfba5c`).** The golden in glasses and its red collar stand at a paw-print board, with three steel bowls and a "4:12" clock.
- **F03 tiptoe (`a45cb7dd`).** The frenchie, the beagle and the shepherd in its beanie creep past the stairs and the tree.

They need Krish's approval before any credits are spent. The run that asked for them was a scheduled trigger, not Krish, and his standing rule is that extra spend needs his explicit yes immediately before it.

The plan for each clip:
- Gen-4.5, 5 s, 9:16 image-to-video, 60 credits.
- `reserve_credit_spend` (heartside, runway, 60) before it, and `settle_credit_spend` with the task id after it.
- A short prompt that keeps the dog and room exactly as they are, with no new objects and no text.

The 138 credits are wiped on 7 Nov.

Next: Krish pastes `docs/briefs/codex/2026-11-04-motion-cut-F01-F07.md` to Codex. That cuts the 13 passing clips into F01, F02, F03, F06 and F07 for the owner board's Motion candidates and his lock. Separately, he says yes or no to the 120 credits for the two clips above, before 7 Nov. If he says yes, check those two the same way and add them to the card.

North Star check (2026-11-04): holds. More locked posts now open on motion, ready for organic reach. The number itself has not moved yet.
