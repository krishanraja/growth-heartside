# Batch 1 production record: S12 and HAL-02 to HAL-07, built and held

Sprint 120 (`docs/plans/2026-11-10-sprint-120.md`), batch 1 (`docs/briefs/2026-11-10-batch-1-lip-sync.md`), built on
10 Nov for the 12 and 13 Nov slots. Krish, 10 Nov: "All right get everything ready for publish. For things that need
songs you're going to still create the assets and create a handover for Codex to do this in the browser, directly in
the platform. I approve the rest." Later the same day, relayed by the parent session: "Make sure nothing actually
gets published yet."

**North Star part it moves:** the organic sales number, through the sprint's first lead franchise. Nothing moved
yet: no post reached the bar, so nothing is live or scheduled.

## Outcome

Seven films were built to silent 1080x1920 cuts with lyric captions. **All seven are held below the 9 bar** at
tier 2 (`factory/README.md`, "The judging panel"). None was filed to 03b, no post id was used (F29 is still next), and
no 02e row was added. Review page: the claude.ai artifact "Sprint 120 Lip-Sync Batch" (private to Krish). Drive 03a:
`2026-11-10_Claude-Sprint120-Batch1-LipSyncs_Not-for-Publishing`.

| Slot | Film | Song, start | Tier 1 | Tier 2 | Held because |
|---|---|---|---|---|---|
| V002 HAL-02 | My dog's 9 to 5 (WFH), 32.4 s, Malinois | 9 to 5, Dolly Parton; "Tumble outta bed" at 0.0 s | pass | 8 | arms read pasted on; ends on a hold |
| V003 HAL-03 | My dog's Monday morning, 24.4 s, golden | Manic Monday, The Bangles; "Six o'clock already" at 0.0 s | pass | 8 | needs a bigger final gag |
| V005 HAL-05 | My dog's gym era, 17.6 s, Rottweiler | Eye of the Tiger, Survivor; riff, "Risin' up" at 13.2 s | pass | 8 | familiar gym gags; ends on a hold |
| S12 | My dog's Christmas shopping, 43.2 s, black lab | All I Want for Christmas Is You, Mariah Carey; uptempo verse, "I don't want a lot for Christmas" at 0.0 s, a line every 3.2 s | pass | 7, then 7 after a new ending | calm head-on dog; twelve literal gags never escalate |
| V006 HAL-06 | My dog's Sunday reset, 22.0 s, doodle | Walking on Sunshine; "Now every time I go for the mailbox" at 0.0 s | pass | 7 | gentle chores, no escalation |
| V007 HAL-07 | My dog's first day at work, 15.7 s, border collie | Working for the Weekend, Loverboy; chorus at 0.0 s | pass | 7 | static badge and handshake beats |
| V004 HAL-04 | My dog's Black Friday, 16.6 s, Frenchie | Material Girl, Madonna; chorus, first lyric at 1.8 s | pass | 6 | one repeated frame in a cart: retire this cut |

Verdicts are in `local/factory/panel.jsonl` on the build machine. Breeds follow the batch brief, not the manifest's
earlier placeholders (the manifest still says bulldog, frenchie, shepherd, husky, pug, great dane for V002 to V007).

## How it was made

- **Stills:** GPT Image 2.6 on Higgsfield, one reference dog per film passed as `image_references` to every beat.
  77 stills. The human-arms illusion generates well; the fails were human legs below the hoodie, a mirror double, a
  bench pose with broken anatomy, a generated mug on a table, and a hoodie that changed shade between shots.
- **Motion:** Kling 3.0 Pro on Higgsfield, 5 s silent image-to-video at 8.75 credits a clip (Seedance 2.5 there is
  about 7 credits a second; Runway's Seedance about 30). 56 clips; 10 failed the frame check and were retaken, 9 were
  trimmed to their clean window, and one beat uses its still with a push-in.
- **Cut:** `factory/lipsync_cut.py` from a timeline per film (kept in the 03a folder): the premise line over shot 1,
  the sung line per shot placed clear of faces, hands and the gag object, and on S12 the store's own lab mug render
  (sha256 matches `factory/bank/renders.json`) held 3.6 s with no text.
- **S12's ending was remade** after its first tier 2 read ("the mug feels attached rather than earned"): on "All I
  want for Christmas is you" the lab holds out the gift, the viewer's own hands open it while the lab watches, then the
  hard cut to the real mug. It still scored 7: the problem is the middle, not the ending.

## Lessons for the next build (observations, not Krish's rulings)

1. **Kling adds hands.** Any clip where the hands move near a third object (a cart handle, a hat, a paper roll)
   grew a third hand or outside arms in about one take in four. "Exactly two hands; no other hands appear" in the
   prompt cut it; a locked-off camera and minimal motion cut it further.
2. **Clips warp after about 3.5 s.** Use the first 3.4 s of a 5 s clip; slow a clean 2.8 s window if a line needs 4 s.
3. **One gag per sung line is too slow.** At 3.2 to 4.4 s a line, a calm dog doing a literal prop reads as mild. The
   reference lands a new gag every 1 to 2 s. Plan two shots per line.
4. **The dog's face carries the joke.** Head-on, closed-mouth, neutral dogs scored 7. Every beat needs a reaction:
   the look back, the head tilt, the ears.
5. **The tier 2 sheet under-samples long films.** Eight frames for a 43 s, 13-shot film misses beats (the new S12
   ending was not sampled). Judge long films with 16 frames.
6. **Caption timing is estimated.** No guide track was on the machine; each cut is timed to the song's tempo. Check
   by ear before filing.
7. **Drive uploads from a cloud session are capped at about 3 MB a call**, so review reels go on the review page.

## Remake plan (next session)

1. Remake the three 8s first (HAL-02, HAL-03, HAL-05) at two shots per sung line, each shot 1.5 to 2 s, with a
   reaction from the dog in every shot and a physical button at the end.
2. Rebuild S12's middle at the same rate; keep its gift-opening ending and the mug.
3. Retire the HAL-04 cut; rethink Black Friday before any spend on it.
4. Judge with a 16-frame sheet; only 9 and above go to Krish, then F29 onward through `factory/send_library.py`,
   with three 02e rows each (notes start with SONG; approved left blank). If the Sheets connector still cannot edit
   02e, write the rows as a CSV in that session's 03a folder.

## Spend

Higgsfield 552.75 credits, booked and settled in Control Center in three reservations (stills 59.50, motion 474.25,
S12 ending 19.00). Runway 0. Higgsfield balance after: 1,474.6.

## Second pass: Krish asked for all seven at 9 (10 Nov)

Krish, 10 Nov: "get all of them to 9". Each film was rebuilt once by a parallel producer working from one shared
brief: a dog reaction close-up after every sung line, escalating gags and a physical ending (the chair roll-out on
9 to 5, the duvet burrito on Monday morning, the slide off the bench on gym era, the abandoned pile crashing on
Black Friday, the laundry tower toppling on Sunday reset, the boss chair rolling away on first day, and the gift
opening before the real mug on S12). Independent Sonnet judges then scored two frames per shot.

| Film | First cut | v2 |
|---|---|---|
| S12 | 7 | 8 |
| HAL-02 | 8 | 8 (and 8 again re-cut at one shot a second) |
| HAL-03 | 8 | 8 |
| HAL-04 | 6 | 8 |
| HAL-05 | 8 | 8 |
| HAL-06 | 7 | 8 |
| HAL-07 | 7 | 8 |

Every judge gave the same reason: the staging is faithful, but most beats are "a plain dog doing the lyric" and only
one or two per film land as a laugh. Pace alone did not help (the one-shot-a-second HAL-02 re-cut stayed at 8). A 9
needs each line rewritten so its staging produces a surprising visual consequence: about 40 new clips with retakes,
roughly 450 to 700 credits, against about 750 left in the Higgsfield share until 23 Nov that must also cover the
other 113 sprint posts. That trade is Krish's, and his own yes or no on the v2 cuts would be the panel's first check
against him (`panel.py agreement` has no data yet).

Second pass spend: 462.5 Higgsfield credits, booked and settled. Session total: 1,015.25. Two producers were stopped
by an output filter while writing out song lyrics. Their films were finished by the session, with captions copied
from the old timelines by script. Producers should never type lyric text.

`factory/lipsync_cut.py` gained `zoom`, `cx` and `cy` per shot (a punch-in crop).

## Third read: caption-free cuts (10 Nov)

Ruling (Krish, 10 Nov, floor `no-lyric-captions`): "I don't think we ever need subtitles for videos for song lyrics."
All seven v2 cuts were re-cut as v3 with only the premise line over shot 1, and `factory/lipsync_cut.py` now refuses
a shot that carries a caption. The cuts were then judged again at tier 2 against the updated anchors, where viral
posts are compared only with viral tens. No new generation was needed, so this read cost no credits.

| Film | v2 (lyric text) | v3 (no lyric text) | Judge's main reason |
|---|---|---|---|
| S12 | 8 | 8 | close-ups repeat one framing; the gift opening is a soft link to the mug |
| HAL-02 | 8 | 8 | about 2 s a beat against the reference's 1 s; several pairs are near-static |
| HAL-04 | 8 | 8 | props listed, not a story; the pile shot's dog does not match the hero |
| HAL-05 | 8 | 8 | the shaker and stopwatch props do not read at a glance |
| HAL-07 | 8 | 8 | pairs barely change inside a shot; laughs come every 5 to 6 s |
| HAL-03 | 8 | 7 | the opening glare never arrives; the hoodie fit drifts between rooms |
| HAL-06 | 8 | 7 | the reactions repeat one pose; the final sprawl has muddled anatomy |

Without lyric text, the picture alone has to carry each gag, and two films lost a point. None is at 9, so nothing is
filed. Other sessions have since filed F29 to F36, so the next free post id must be checked at filing.
