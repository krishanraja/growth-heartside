---
name: heartside-assembly-panel-board
description: How a Heartside film goes from downloaded Kling takes to Krish's review board - cutting with the studio's cut.py, painting the end card on heartside.io's painter, judging with the panel (Haiku tier 1, Sonnet tier 2, words never excused), tracked links, and writing the board item. Use after the takes for a scored script are downloaded and checked.
---

# Assembly, the panel and the review board

Rules: `factory/README.md`, "The judging panel"; `docs/REVIEW-BOARD.md`; `codex/README.md`, "On-screen labels sit in
one place"; floor `fixed-label-position`, `text-clear-of-faces`, `real-product`, `endings-land`.

Only a script that scored 9 on its words (`heartside-joke-lab`) is cut.

## 1. Cut the film

A runnable copy of `cut.py` is committed at `docs/briefs/2026-11-18-compile/assembly/cut.py`. Run it from the
repository root, with take paths relative to the repository. Briefs go in `docs/briefs/<round>/briefs/<id>.md`;
`films.json`, `tools/make_briefs.py` and `cut_cmds.json` in `docs/briefs/2026-11-18-compile/` are the pattern for a
round. It writes `local/media/studio/<id>/` (the mp4 and its contact sheet).

```bash
python docs/briefs/<round>/assembly/cut.py parse <id>     # check what it read from the brief first
python docs/briefs/<round>/assembly/cut.py build <id> --takes s1=<repo-relative clip>,s2=<clip> --end <render id or painted png> [--ground plain] [--frame s1=1.1:0.5:0.7] [--in s2=0.3]
python docs/briefs/<round>/assembly/cut.py gate <id>      # re-run every gate on the last build
```

- Every film ends on the real product render, held 3 to 4 s. `codex/check_picture.py` holds a film whose last shot is
  anything else, so a film with no end card cannot pass. Every 18 Nov compile film ended on the painted blanket.
- The timing gate prefers 8 to 12 s of film before the end card.

- Labels sit at a fixed place: text top y 360, centred x 140 to 820. The safe band is x 120 to 820, y 330 to 1180.
  If a label covers the dog's face, recrop the shot with `--frame` and leave the label where it is.
- A take can be a path to a bank clip (`s1=<STUDIO>/kling3/b2-rv-06.mp4`), so bank footage cuts without renaming.
- The end card is the store's own render or a painted product, pixels unaltered, held 3 to 4 seconds. Use
  `--ground plain` for a cream ground behind it. On 18 Nov both tiers flagged every film's end card (the painted
  blanket on plain cream) as bolted on. Give the product a reason to be there: the blanket shows the film's own dog,
  or the product sits in the dog's world in the last shot. Never add a line that only sells: "Gary also got the
  blanket." scored 7 against 8 without it.
- Two visual rounds on 18 Nov proved the end card is structural, not polish. Five built films whose scripts scored 9
  as described films came out at 7 or 8, and every film judge named the same two gaps: the product card is cold and
  disconnected from the joke, and a single beat with no escalation is thin. The live posts that land with a product
  (F34, S01) make the dog's own face on the gift part of the story. Before cutting, the script must say why the gift is
  in the film; if it cannot, shelve the script rather than cut it.
- When a look lands at the very end of a clip, hold the last frame for 1 s before the cut. Put `-ss` and `-t` before
  `-i`: with `-t` after `-vf`, the hold is cut off and `cut.py` refuses the shot as too short.
  `ffmpeg -v error -ss <in> -t <len> -i <clip> -vf tpad=stop_mode=clone:stop_duration=1 <clip-held>.mp4`, then pass the
  held clip as the take (`s2=<path>`). Time each label against the frame where the look actually lands (read it on the contact sheet),
  never against the prompt.
- A label says only what the picture literally shows. "Under himself." was wrong: the treat sat between the paws, not
  under the dog. It became "He is keeping it company." Check each label against its frame at full size.
- A label longer than two lines fails the gate. Split it across two beats with the words unchanged, never reword it
  at the cut. The caption comes from the joke lab with the labels; never write one at assembly.
- Fonts missing (Karla): `python factory/fetch_library.py local/assets/library` from the repository, then rebuild.

### Music (after Krish's yes on it)

1. Keep every film's silent master (`local/media/studio/<film>/<film>.mp4`), so the platforms' in-app trending sound
   can go on instead (floor `music-defines-humour`).
2. Show Krish each film's music in one line and wait for his answer. Record it in the round's `music.json` (`status`).
   The beds come from `heartside-higgsfield-ui`, "Music beds".
3. Check each bed's length with `ffprobe`: it must cover the whole film, end card included.
4. Mix: `python -I docs/briefs/2026-11-18-compile/tools/mix_music.py [film ...]` from the repository root. It
   normalises each bed to -16 LUFS and writes `<film>_music.mp4`. Set `stop_at` in `music.json` to cut the music to
   silence on the reaction shot, so the payoff lands in silence.

## 2. The painted end card (heartside.io painter, Claude in Chrome)

Use it only when the end card should show the film's own dog painted on the product. By 18 Nov the only painted card
is the hero Gary's blanket, so a film with a different dog (the tan terrier in FG12) still ends on Gary's painting.
That is a known weak point: paint the film's own dog when a round is built around it. Use at most 2 paints per dog and
count every paint in `<STUDIO>/log-painter.md`.

1. Open a new tab at
   `https://heartside.io/products/your-dogs-personality-blanket?journey=1&utm_source=internal-paint&utm_medium=studio`.
2. For a dog not painted before in this browser:
   - remove the localStorage keys `teeinblue-photo-gen-state`, `teeinblue-customizations` and
     `hs2-handed-16158073880958`;
   - use a fresh tab, because sessionStorage is per tab.
   Otherwise the painter reuses the last dog (17 Nov).
3. Upload a dog frame at least 700 px tall. Under 700 px the painter hangs with no error. Recut the frame to
   1080x900 or larger, with only this dog in it: the painter asks for "just your dog, no other dogs", so crop out any
   second dog.
4. Follow the painter's steps: Make one for my dog, the photo, Painterly, a tone, a spot, blanket only, Start painting,
   the questions, see it painted.
5. Copy the `customers/uploads` print URL. Never add to cart.
6. Composite it, from `local/paint`:
   `python <STUDIO>/tools/paint_composite.py <id> <dog> blanket <base layer url> <print url>`. Crop (150,85,905,970) and
   update the JSON record beside the image: `cut.py gate` checks for that painter record.

## 3. Judge it (the panel)

1. Contact sheet: `python factory/panel.py sheet local/media/studio/<id>/<id>.mp4 --out local/factory/panel-<date>/<id>.png`.
2. Tier 1, Haiku sub-agent: up to 4 sheets in one image
   (`python factory/panel.py batch <sheets...> --out <png>`), prompt from `python factory/panel.py brief tier1 <png>`.
   Any no sends it back with the failing frame.
3. Tier 2, Sonnet sub-agent, only on tier 1 survivors: `python factory/panel.py brief tier2 <sheet>`. The brief
   carries every live post; confirm it lists `V005` before you trust the score. Judge the film as a film even when
   its words scored 9: on 18 Nov the gym film fell to 7 (it retread the live V005 "gym era"), the waitlist film to 6
   (the yoga mat made a real play-bow read as a staged pose), and three more to 6, 6 and 8 because the joke lived only
   in the labels. The film judge wants a visible consequence, or a reaction shot from the dog the joke lands on.
4. Give the judge the brief and the sheet only. Add no context that excuses anything: "fully human acts are allowed"
   moved a retread from 7 to 9 on 17 Nov, and Krish declined it.
5. Record both (three arguments: slot, tier, verdict):
   `python factory/panel.py record <id> tier1 tier1-pass` (or `tier1-fail`) and
   `python factory/panel.py record <id> tier2 tier2-<N> --score <N> --note "<best beat; floor risk>"`.
6. Before believing any judge's fault, open the frames it names at full size. Tier 1 (Haiku) is often wrong from
   thumbnails: on 18 Nov, 6 of 7 faults it named on the gym film were false. Its usual false faults:
   - one dog occluding another, read as "merged bodies";
   - a play-bow read as "a human pose";
   - the store painter's real blanket read as "generated art";
   - a payoff called "only in the captions" when the dog visibly does it.
   A fault that holds at full size is real. On 17 Nov there was a real merged extra head beside the false ones.
7. The tier 2 judge varies by about 1 point. A 9 that rests on one beat, or that the judge's own `floor_risk` says Krish
   would reject, is an 8: hold it.
8. Every cut gets `python factory/jokelab.py cut <run> <cand> --score N --words <file>`. When it exits 1, stop cutting.
9. After Krish answers, record `python factory/panel.py record <id> krish krish-yes` (or `krish-no`). Check `python factory/panel.py agreement`. Below 80%, rebuild
   the anchors in `factory/bank/anchors.json` before the next batch.

## 4. Tracked links

One per film, on its gift's social landing page:
```bash
python growth.py link "<landing url>&hook=<hook>" <CREATIVE_ID>
```
Concept ids are numbered in order. C201 to C208 were used by 17 Nov, so find the next free one in the Schedule and
`local/creatives.csv` before you assign it. Keep the links in `local/factory/panel-<date>/links-<batch>.txt`.

## 5. The review board

Board: https://claude.ai/artifact/6kGmidNyYAnRwiSdzAtcr4. Steps: `docs/REVIEW-BOARD.md`.
1. Upload the cover and the mp4 to the board's asset store (`Artifact` publish with `asset: true` and the board's url).
2. Write the item with `ArtifactData` `set` into collection `items`, in the doc's format: the question, `on_yes`,
   `on_no`, the caption, the tracked link and the scores.
3. The board's player shows a 9:16 film at its own size (`aspect-ratio: 9/16; object-fit: contain`, fixed 17 Nov after
   Krish: "can you make the video player the same size as the videos"). Keep that CSS when republishing the board.
4. Only items, and only 9s. Never write to `verdicts`; only Krish writes those.
5. Read his answers with `ArtifactData` `list` on `verdicts`. Record each one (`panel.py record`, `jokelab.py verdict`,
   and the floor if he says no).

## Never

- Never cut a film whose words are below 9, and never re-cut pictures to raise a score when the words stay the same.
- Never alter the product's pixels, draw it with AI, or badge it (`real-product`, `no-badges`).
- Never move the label band per shot: recrop the shot.
- Never put an 8 on the board to fill a slot (`ten-out-of-ten`).
