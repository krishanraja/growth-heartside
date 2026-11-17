---
name: heartside-assembly-panel-board
description: How a Heartside film goes from downloaded Kling takes to Krish's review board - cutting with the studio's cut.py, painting the end card on heartside.io's painter, judging with the panel (Haiku tier 1, Sonnet tier 2, words never excused), tracked links, and writing the board item. Use after the takes for a scored script are downloaded and checked.
---

# Assembly, the panel and the review board

Rules: `factory/README.md`, "The judging panel"; `docs/REVIEW-BOARD.md`; `codex/README.md`, "On-screen labels sit in
one place"; floor `fixed-label-position`, `text-clear-of-faces`, `real-product`, `endings-land`.

Only a script that scored 9 on its words (`heartside-joke-lab`) is cut.

## 1. Cut the film

Run it from the studio's `assembly/` folder. It reads `briefs/<id>.md` and `kling3/<id>_s<N>_t<N>.mp4`, and writes to
`local/media/studio/<id>/` in the growth repository (the mp4 and its contact sheet).

```bash
cd <STUDIO>/assembly
python cut.py parse <id>                                  # check what it read from the brief first
python cut.py build <id> --takes s1=t2,s2=t1 --end <render id or painted png> [--ground plain] [--frame s1=1.1:0.5:0.7] [--in s2=0.3]
python cut.py gate <id>                                   # re-run every gate on the last build
```

- Labels sit at a fixed place: text top y 360, centred x 140 to 820. The safe band is x 120 to 820, y 330 to 1180.
  If a label covers the dog's face, recrop the shot with `--frame` and leave the label where it is.
- A take can be a path to a bank clip (`s1=<STUDIO>/kling3/b2-rv-06.mp4`), so bank footage cuts without renaming.
- The end card is the store's own render or a painted product, pixels unaltered, held 3 to 4 seconds. Use
  `--ground plain` for a cream ground behind it.
- Fonts missing (Karla): `python factory/fetch_library.py local/assets/library` from the repository, then rebuild.

## 2. The painted end card (heartside.io painter, Claude in Chrome)

Use it only when the end card should show the film's own dog painted on the product. Use at most 2 paints per dog and
count every paint in `<STUDIO>/log-painter.md`.

1. Open a new tab at
   `https://heartside.io/products/your-dogs-personality-blanket?journey=1&utm_source=internal-paint&utm_medium=studio`.
2. For a dog not painted before in this browser:
   - remove the localStorage keys `teeinblue-photo-gen-state`, `teeinblue-customizations` and
     `hs2-handed-16158073880958`;
   - use a fresh tab, because sessionStorage is per tab.
   Otherwise the painter reuses the last dog (17 Nov).
3. Upload a dog frame at least 700 px tall. Under 700 px the painter hangs with no error. Recut the frame to
   1080x900 or larger.
4. Follow the painter's steps: Make one for my dog, the photo, Painterly, a tone, a spot, blanket only, Start painting,
   the questions, see it painted.
5. Copy the `customers/uploads` print URL. Never add to cart.
6. Composite it, from `local/paint`:
   `python <STUDIO>/tools/paint_composite.py <id> <dog> blanket <base layer url> <print url>`. Crop (150,85,905,970) and
   update the JSON record.

## 3. Judge it (the panel)

1. Contact sheet: `python factory/panel.py sheet local/media/studio/<id>/<id>.mp4 --out local/factory/panel-<date>/<id>.png`.
2. Tier 1, Haiku sub-agent: up to 4 sheets in one image
   (`python factory/panel.py batch <sheets...> --out <png>`), prompt from `python factory/panel.py brief tier1 <png>`.
   Any no sends it back with the failing frame.
3. Tier 2, Sonnet sub-agent, only on tier 1 survivors: `python factory/panel.py brief tier2 <sheet>`.
4. Give the judge the brief and the sheet only. Add no context that excuses anything: "fully human acts are allowed"
   moved a retread from 7 to 9 on 17 Nov, and Krish declined it.
5. Record both (three arguments: slot, tier, verdict):
   `python factory/panel.py record <id> tier1 tier1-pass` (or `tier1-fail`) and
   `python factory/panel.py record <id> tier2 tier2-<N> --score <N> --note "<best beat; floor risk>"`.
6. Before believing any judge's fault, open the frames it names at full size. Contact-sheet thumbnails produced false
   faults on 17 Nov (a "fake" painted blanket, a "second head") next to real ones.
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

Board: https://claude.ai/artifact/A3tFqoYZuYAEdUrziU5wnN. Steps: `docs/REVIEW-BOARD.md`.
1. Upload the cover and the mp4 to the board's asset store (`Artifact` publish with `asset: true` and the board's url).
2. Write the item with `ArtifactData` `set` into collection `items`, in the doc's format: the question, `on_yes`,
   `on_no`, the caption, the tracked link and the scores.
3. Only items, and only 9s. Never write to `verdicts`; only Krish writes those.
4. Read his answers with `ArtifactData` `list` on `verdicts`. Record each one (`panel.py record`, `jokelab.py verdict`,
   and the floor if he says no).

## Never

- Never cut a film whose words are below 9, and never re-cut pictures to raise a score when the words stay the same.
- Never alter the product's pixels, draw it with AI, or badge it (`real-product`, `no-badges`).
- Never move the label band per shot: recrop the shot.
- Never put an 8 on the board to fill a slot (`ten-out-of-ten`).
