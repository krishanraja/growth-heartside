# Volume build, batch 1: built, judged and held (10 Nov)

Brief: `docs/briefs/2026-11-10-volume-build.md`. Krish, 10 Nov: "we need a huge array of bulletproof posts here, image
and video". Hold in force: "Make Sure nothing actually gets published yet."

**North Star part it moves:** organic sales, through volume of shareable posts. Nothing moved yet: no post reached the
9 bar, so nothing was filed, no post id was used (F30 is still next) and no 02g Sheet was made.

## Trends read (dated sources)

NewEngen, "TikTok Trends: November 2026" (updated 4 to 5 Nov); SocialBee trending songs (5 Nov); Revid viral sounds
(8 Nov). Used: Kylie's runway hip pop ("Angel of My Dreams", JADE), "Pray For Me" slow-mo group entrance (The Weeknd,
Kendrick Lamar), Mariah Carey "It's Time" holiday kickoff, "Why Would I Deceive You?" audio meme. Not used yet:
"Housewife" (Tate McRae), "Self Aware" (Temper City).

## Outcome: 0 of 12 at 9

| Post | Format | Tier 2 (each read) | Held because |
|---|---|---|---|
| Toilet-paper crime scene | carousel, 4 | 7, 7, 8 | the mummified golden lands; suspects two and three stay mild |
| Proud of the underdog (her dog / my dog) | carousel, 3 | 7, 8, 7 | familiar format; hose tangle is the only surprise |
| Kitchen inspector (schnauzer) | carousel, 3 | 8, 7 | the inspector role rests on the caption |
| Bed-space economics (Bernese) | carousel, 3 | 8, 7 | familiar arc; the content filter refuses any visible person in the bed |
| Pray For Me slow-mo entrance | video, 12.1 s | 7, 7 | four entrances treated the same; no escalation |
| Mariah "It's Time" | video, 7.8 s | 8, 6 | nothing happens after the cut |
| Why would I deceive you (beagle) | meme | 6, 6 | familiar guilty-dog picture; the stare is not a troll |
| Runway hip pop | video, 8.3 s | 6, 6 | dalmatian trots, the corgi's swing is too small to sync |
| Bedtime burrito | meme | 6 | retired: stock burrito |
| Bedtime row, one awake | meme | 5 | retired: the cheese drawer exists only in the caption |
| Lineup, one rebel (motion) | video, 6.5 s | 5 | retired: dogs tiny, the turn invisible |
| Called another dog cute | meme | tier 1 fail | retired: payoff in the caption only |

Verdicts: `local/factory/panel.jsonl` on the build machine. Contact sheets and judge sheets: Drive 03a
`2026-11-10_Claude-VolumeBuild_Not-for-Publishing`.

## Lessons for batch 2 (observations, not Krish's rulings)

1. **Familiar meme formats score 6 to 8 however clean.** Every judge asked for a surprising visual consequence. The
   best-scoring frame of the batch was the golden mummified in toilet paper with a roll in its mouth: the evidence is
   absurd and the dog is deadpan. Design every post around one picture like that; the line only names it.
2. **The dog must be visibly in on the joke in the payoff frame** (flat stare at the lens, paw on the evidence). A
   calm neutral dog scored 6 every time (floor troll-not-mild).
3. **Tier 2 drifts about one point between reads of the same work** (It's Time 8 then 6, kitchen 8 then 7, underdog
   8 then 7). A single 9 from one read is weak evidence; batch 2 asks for the same score from two fresh judges before
   filing.
4. **Trend reskins need the trend's signature move to be big.** A strut must be a strut and a hip pop a big rump
   swing; Kling 3.0 underplays both from a static start frame. Prompt the exaggeration and pick the clip where the
   motion is largest.
5. **Escalate repeated beats.** Four entrances shot the same way read as one; each must be more over the top, with
   the smallest dog getting the biggest treatment.
6. **Higgsfield's filter refuses a person in a bed** (twice, unbilled). Keep people out of bed scenes.
7. **Stills are cheap (0.25) and motion is not (8.75 a clip).** Batch 1 spent 7.50 on 39 stills and 113.75 on 13
   clips. Judge the start frame and the concept at tier 2 before any motion is generated.

## Spend

Higgsfield 123.50 credits, booked and settled in Control Center in two reservations (stills 7.50; motion 116.00, which
also carries 9 still remakes at 2.25). Balance after: 1,206.1. Runway 0.

## Code

`factory/still.py`: a newline in a meme line is a deliberate break, so two-speaker memes lay out as two lines.
