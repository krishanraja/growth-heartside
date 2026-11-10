# F34 chat variants: three built, on Krish's board (10 Nov)

Krish, 10 Nov: "Yes, build the F34 variants from existing photos". Then "yes go for it".

**North Star part it moves:** organic sales, through more of the one chat format Krish scored 9.

## What was built

The asset library was rebuilt here with `factory/fetch_library.py` (18 renders, 3 photos, fonts, audio; every sha256
checked). F34's lock freezes the product type and the photo beat, so every variant uses a blanket and reuses the one
existing photo: Dog B is the brindle frenchie, sending `p04-frenchie-bark.jpg`, with a new gift line that photo proves.
That leaves three plotters with a blanket render: golden, dachshund and doodle (shepherd is F34 itself).

| Post | Cast (A, B, C) | Running gag | Closer | Panel |
|---|---|---|---|---|
| F34-golden | golden, frenchie, dachshund | the stolen sock and the tulips | "bro shes crying cos this one doesnt shed 💀" | 9, then 8 after the closer was tightened |
| F34-dachshund | dachshund, frenchie, doodle | barking at the mirror at 3am | "bro she can finally fold u 💀" | 8, 8 |
| F34-doodle | doodle, frenchie, golden | the eaten couch cushion | "bro she already has a blanket of u. its called the couch 💀" | 8, 8 |

All three keep F34's fingerprint `dabe3d3b9b180cba`; `lock.py check` reports only their 25 proposed lines each, and
`lock.py media` passes. Each is on the review board (`post-F34-<breed>`) with its reel and cover. A Yes approves its
lines and files it as `F34-<breed>` with its own 02 Sheet; nothing files before that.

## Filed (Krish, 10 Nov: "i approve them all")

The 75 lines are approved in `factory/bank/lines.json` and `lock.py` records `krish-approve` and an independent
`reviewer-pass` for each post. A first reviewer held F34-golden because the dachshund avatar looked chestnut; it is a
crop of the store's own dachshund mug render (the F01 exception), and the same check found the golden avatar showed a
window, not a face: `factory/bank/renders.json` now centres it on the dog (726, 640). After the rebuild, both
reviewers passed. The release gate's per-platform placement review stays for posting time, as F34's own rows say.
Files went through the library lane (`Posts/F34-golden/`, `F34-dachshund/`, `F34-doodle/`, reel and cover each) and
the rows are in `02n` for 17 Nov, 26 Nov and 1 Dec, `approved` blank for Krish.

## Lessons (observations, not Krish's rulings)

1. **Judges score the closer hardest.** Every read compared the last line with F34's "thats a hostage situation": a
   short verdict on the blanket itself beats an explained joke.
2. **The middle beats that boast about the speaker's own gift roast the plotter only sideways**, which judges call
   plot lines. Write those beats so they still land on the plotter.
3. **Variants are cheap.** The library fetch and three builds cost no credits; the only cost is about 130k tokens a
   judge read.
