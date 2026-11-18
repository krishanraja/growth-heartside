---
name: heartside-dog-realism
description: How a Heartside dog must look (a real, slightly scruffy pet on the owner's phone, never a perfect AI dog), the cast Krish has passed, and the frame-by-frame checklist for judging a still or a clip. Use before approving any generated dog, anchor or Kling take.
---

# The dog must pass for someone's real pet

Floor rules: `real-scruffy-dogs`, `real-dogs`, `one-register-never-blurred`, `real-behavior-in-motion`,
`dog-does-dog-things`. Read their words with `python growth.py floor --format reel`. Krish has said this four times,
the last on 17 Nov: "he still looks a bit too perfect in terms of fur, and I cant figure otu what else". Then, going
to sleep: "I need you to have incredibly high standards and keep reworking until you're happy with the realism".

## The cast (17 Nov sprint)

Use these dogs. Never roll a new dog during a timed Unlimited window.

| Role | Dog | Source frame | Roll |
|---|---|---|---|
| Hero, in every set | gray and white scruffy terrier mix, wiry coat, reflective orange collar | `<STUDIO>/anchors/ref-hero.png` (d1-li-01) | `local/factory/roll-li01.json` (dog-d93f8241db38) |
| Sidekick C, sets with two dogs | chocolate shaggy poodle and spaniel mix, curly coat, orange collar | `<STUDIO>/anchors/ref-c.png` (d1-li-04) | `local/factory/roll-li04.json` (dog-817e43b02fa6) |

Krish, 17 Nov: "Hero is good, sidekick should be C". He offered the beagle only "if you can get the beagle to look
good". It failed the 17 Nov test, so C stays. `local/` lives on Krish's main checkout (`C:\Users\krish\dev\growth-heartside`).

A new dog, outside a timed window only: `python growth.py floor --format still` first (the roller refuses until the
floor is read), then `python growth.py still roll --count 1 --breed <key> --setting <key> --frame video --json >
local/factory/roll-<name>.json`. Write long `--action` and `--expression` values into a script file and run that:
inline shell quoting broke on 17 Nov.

## Judge the frames, never the prompt

A prompt that lists flaws proves nothing. The 17 Nov beagle prompt asked for a patchy coat, tear stains, a dirt crust,
a nicked ear, drool and burrs, and Kling 3.0 rendered none of them.

1. Make a contact sheet: `python factory/panel.py sheet <clip or still> --out <png>` (8 timed frames for a clip).
2. Also pull 3 frames at full size:
   `ffmpeg -v error -ss <t> -i <clip> -frames:v 1 <png>` at 20%, 50% and 90% of the clip.
3. Open each with the Read tool at full size. Thumbnails mislead: on 17 Nov a judge called the painted blanket fake
   and saw a "second head" that was not there. Another frame really did have a merged extra head.
4. Go through the checklist below for each frame. One fail rejects the take.

## The checklist

Anatomy (`real-dogs`):
- [ ] four legs, one tail, two eyes, two ears, paws with toes; no merged, extra or missing parts;
- [ ] no second dog head or body growing out of the dog or the furniture;
- [ ] the dog is on four legs (photoreal register: never standing on hind legs, never human arm moves).

The tells of an AI dog (17 Nov beagle test). Fail the take if any is true:
- [ ] the fur is even, glossy, shampooed or blow-dried, with every hair lying the same way;
- [ ] the face markings are mirror-symmetric;
- [ ] the whites (paws, muzzle, chest) are spotless while it walks on grass or dirt;
- [ ] the light is a golden backlight, rich even colour, an advert lawn: it looks like a dog-food advert;
- [ ] the eyes are glossy with neat studio catchlights;
- [ ] it hits its mark: walks straight to the lens, stops in the centre and looks up on cue.

What a real pet shows. Pass only if most are true:
- [ ] uneven fur: a bed-head tuft, a flat patch where it lay, a clump, wet or dusty paws;
- [ ] ordinary light: a window, a lamp, a blown-out sky;
- [ ] a lived-in room or yard with clutter;
- [ ] imperfect framing: off-centre, horizon a little off;
- [ ] real dog timing: it wanders off-line, ignores the camera, turns away, sniffs, scratches, flops.

Motion (video takes, frame by frame):
- [ ] no head morphs as the dog turns toward the lens, above all while another dog passes behind (`b2-gy-04`, 3.4 s);
- [ ] a real behaviour stays a dog's behaviour: no prop that names a human activity (yoga mat, desk, podium) under it.

Consistency (`generation-continuity`):
- [ ] the same dog as the reference: coat colour, markings, build, collar;
- [ ] no collar, ear or coat change between frames.

Register (`one-register-never-blurred`):
- [ ] photoreal pieces: the dog does only what a real dog does, and the words do the human thinking;
- [ ] absurd pieces: unmistakably staged. A near-real dog doing a slightly human thing is the blur, and it fails.

## What to do with a fail

1. Log it: `<id> rejected: <the failed line from the checklist>`.
2. If the dog itself fails, do not re-prompt it with more listed flaws: Kling ignores them. Go back to a passed
   reference frame and an anchor still (`heartside-anchor-stills`).
3. If two takes fail on the same tell, change the scene: light, viewpoint or action. Not the adjective list.
4. When Krish asks "Do the two dogs look like real-life dogs or AI dogs?", answer dog by dog, honestly, from the
   frames. On 17 Nov the terrier passed and C did not, because C was posed: centred, square-on, staring, groomed.
   The fixes for a posed dog are in `heartside-anchor-stills`, step 2.
5. Show Krish a frame strip only for a casting decision: a new dog, or a swap. Ask one question, "beagle or C?"
   style, with the deadline it must be answered by.

## Never

- Never approve a dog from its prompt, its roll or Codex's report.
- Never show Krish a dog you would not bet passes for a real pet. Krish: "make all dogs look realistic and not just
  perfect AI dogs, they need to ALL look photorealistic and have real world dog mannerisms and slight scruffiness about
  them".
- Never dress a photoreal dog (vests, glasses, props on its head) to make a joke. The words carry the parody
  (`no-retread-of-live-post`, `dog-does-dog-things`).
