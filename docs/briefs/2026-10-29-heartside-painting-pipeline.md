# For heartside: what the breed pilot taught us about the painting pipeline

29 Oct 2026, growth engine session. Krish: "The whole point here is to refine the technology that
generates the real-world customer generations as well ... feed back to the other repository how to
improve the data and AI pipeline permanently." This growth repository never changes heartside (rule
9); this is a brief for a heartside build session to act on.

Evidence (public review branch `review/heartside-examples-2026-10-29` in growth-heartside):
`review/golden-v1-v2-v3.jpg`, `review/golden-faces.jpg`, `review/golden-v3-v5.jpg`,
`review/golden-v5-face.jpg`, `review/golden-v5-v6.jpg`, `review/golden-v6-face.jpg`, and every prompt
sent under `review/prompts/`. Each run used the same
reference photo (a frontal, awake, sitting Golden, which is what a typical customer uploads), the same
image model through Codex as an edit with the photo as input, one generation each. Codex's own logs
confirm each prompt was sent byte for byte.

## What we asked for, and what came back

The job: Maple, Golden Retriever, Painterly, Sentimental, portrait. The buyer's taps: rests at her
person's feet, naps together, a stuffed toy, wears a collar.

| Run | Prompt | Asleep at her person's feet | Collar | Toy hugged | Re-staged | Face painted |
|---|---|---|---|---|---|---|
| v1 | the batch's prompt (5,531 characters) | no | no | beside her | no | no, photographic |
| v2 | the storefront's own facts (5,587) | no | **yes** | beside her | no | no |
| v3 | v2 plus two rule fixes (6,240) | no | yes | close | no | no |
| v5 | a short, scene-first prompt (628) | **yes** | **yes** | **yes** | **yes** | **yes** |
| v6 | v5 plus a detailed identity and framing brief (1,087) | yes | yes | yes | yes, but the photo's tiled floor returned | **no**, photographic hairs and a wet nose |

v5 is the master. v6 framed the dog better and matched the coat more closely, but its face went back
to the photo. A face-only second edit would have fixed it, but the customer route makes one
generation per order, and an example must be made the way a customer's painting is made.

## Finding 1: the breed batch does not send what the storefront sends

`tools/print-art/breed-batch.mjs` puts the whole tap brief into one fact with `source: "brief"`.
The storefront (`shopify/assets/hs-artwork-profile.js`, `fromChat`) sends separate facts with sources
`spot`, `together`, `toy` and `accessory`, and `serialize` would drop a `brief` source outright. The
grounding rule "When a toy or accessory fact is present, show that exact item" only fires on those
sources, so the batch's collar never appeared. Proven by v1 against v2: the only change was the facts,
and the collar arrived.

**Fix:** build each job's Personality with `HSArtworkProfile.serialize(HSArtworkProfile.fromChat({spot,
together, toy, accessory}))`, so examples are painted from exactly what a buyer's taps produce.

## Finding 2: the long prompt makes the model copy the photo

The live template (`nativePrompt` with `recipes-v1.json`) is a rulebook of about 5,500 characters. It
opens with "Use the supplied photo as the only identity authority. Preserve ...", the scene arrives
only as quoted JSON near the end, and each tone fixes an expression (Sentimental: "a gentle gaze
toward the viewer") that contradicts facts such as napping. Faced with dozens of competing rules in an
image edit, the model kept the safest one: the photo. v1 to v3 all reproduce the photo's frontal head,
open eyes, fine hairs, glossy eyes and wet nose, despite the Painterly grammar forbidding exactly
that. Adding clarifying sentences (v3) changed nothing. A typical customer photo is frontal and
awake, so customers very likely get the same: their dog's photo, lightly painted, in the photo's pose,
whatever tone and scene they chose.

v5 used one short paragraph in this order, and every check passed:

1. **What to make:** "Create a new hand-painted oil painting of the dog in this photo."
2. **What to keep, in one sentence:** "Keep exactly who she is: the same face shape, ears, eyes, muzzle
   and coat colour."
3. **The scene, built from the facts:** "Change everything else: she is asleep with her eyes closed,
   curled up at her person's feet, with a stuffed toy hugged close and her collar on. Only her
   person's feet and ankles show, never a face."
4. **The tone's light and mood:** "Warm, low golden side light; quiet and tender."
5. **The medium, including the face:** "Thick, visible brushstrokes and impasto across the whole
   picture, the face included: no photographic fur, eyes or nose."
6. **The format:** "Plenty of calm space around her, and the lower right corner left plain."
7. **Short negatives:** "No text, no other animals, no other objects."

**Fix: move the safeguards out of the prompt and into the code.** The composer, not the model,
decides what is allowed in the picture: it turns only tagged, tidied facts into a scene sentence (the
way `hs-brief.js` already does on the phone), so the prompt never needs to explain the rules about
untrusted data, invented props or breed stereotypes. The template becomes about seven short slots:

| Slot | Built from | Length |
|---|---|---|
| Make | the style's medium noun ("oil painting", "comic-book illustration", ...) | 1 sentence |
| Keep | fixed identity sentence, pronoun from the chat | 1 sentence |
| Scene | `spot`, `together`, `toy`, `accessory` facts; asleep when `together` is naps; the tone's premise (hilarious and over the top) | 1 to 2 sentences |
| Mood | the tone's light, expression and composition, condensed | 1 sentence |
| Medium | the style grammar, condensed, always naming the face | 1 to 2 sentences |
| Format | portrait: quiet lower right; mug: left two thirds; blanket: repeated motifs, no panel | 1 sentence |
| Never | no text, no other animals, no other objects, no people's faces | 1 sentence |

Teeinblue's `gpt:image_filter` takes one static prompt with `{{field}}` slots, so this maps directly:
the storefront fills `{{Make}}`, `{{Scene}}`, `{{Mood}}` and `{{Medium}}` the way it already fills
`{{Style direction}}` and `{{Tone direction}}` today.

**Before switching the live template:** one test order on manual review through the real Teeinblue
route, because Codex's image tool (used here) and Teeinblue's filter may weigh a prompt differently,
and because Codex's tool accepts no quality setting while Teeinblue renders at 3840.

## Finding 3: the tones need to yield to the facts

Each tone's fixed expression must give way to a stated habit: a napping dog sleeps, eyes closed, in
any tone. `hs-brief.js` already knows this ("a dog mid-nap can't gaze or keep watch"); the image
recipe does not. In the composed template, the Scene slot comes before Mood, and Mood never states an
expression that contradicts the scene.

## Finding 4: spelling out identity copies the photo's face

v6 described the dog in detail (coat shades, ear colour, nose colour, ear shape, muzzle) and got the
photo's face back: fine hairs, a wet, pored nose. Each trait the prompt names is something the model
checks against the photo, and the cheapest way to pass is to copy those pixels. Keep the identity
slot to one generic sentence ("the same face shape, ears, eyes, muzzle and coat colour") and let the
photo carry the specifics. The `Keep` slot in the table above is fixed text for this reason; it is
never filled from the buyer's answers about appearance.

## The short prompts for the rest of stage 1

Composed by hand in the shape above, from each dog's taps in `breed-batch.mjs` as the storefront
would send them (one toy per dog, as `fromChat` takes one). These are what the growth engine will
paint the remaining stage-1 examples with; heartside's composer should be able to produce prompts
like them.

**lab-warm-portrait (Bear, Cinematic, Warm):**
> Create a new cinematic portrait of the dog in this photo. Keep exactly who he is: the same face shape, ears, eyes, muzzle, coat colour and markings. Change everything else: he rides in the back seat of a car on a sunny day, wearing his bandana, with a tennis ball on the seat beside him that he gives a knowing sideways glance, one ear up and a small happy smile. Clear, warm daylight through the window and lively natural colour, the dog slightly off center on an easy diagonal. Natural photographic proportions, composed cinematic light and believable depth, never blurring his face or markings. Leave the lower right corner quiet and plain. No text, no people, no other animals, no other objects.

**frenchie-hilarious-portrait (Bao, Comic book, Hilarious):**
> Create a new comic-book illustration of the dog in this photo. Keep exactly who he is: the same face shape, ears, eyes, muzzle, coat colour and markings. Change everything else: it is movie night, and he sits in his person's spot on the couch as if it were a matter of enormous importance, wearing his bow, with his squeaky toy placed beside him like a precious trophy. A dramatically low, close camera looks up at him; chin lifted, mouth closed, one solemn sideways glance. Bright theatrical light and bold diagonals. Strong ink contours, selective halftone shading and energetic graphic staging, his anatomy and proportions exact. Leave the lower right corner quiet and plain. No words, lettering or speech bubbles, no people, no other animals, no other objects.

**doodle-over_the_top-portrait (Clover, Vintage screenprint, Over the top):**
> Create a new vintage screenprint poster of the dog in this photo. Keep exactly who she is: the same face shape, ears, eyes, muzzle, coat colour and markings. Change everything else: out on a walk, she marches like royalty at the head of a victory parade of one, wearing her bandana like regalia and carrying her frisbee like a prize, chin high, eyes half closed, utterly smug. Grand and symmetrical, centered, seen from a low camera, with bold rays of light behind her. A limited three-to-five-colour ink palette, bold cut silhouettes, purposeful negative space and visible paper and ink grain. Leave the lower right corner quiet and plain. No crowns, capes or costumes, no text, no people, no other animals, no other objects.

**dachshund-sentimental-blanket (Frank, Fine ink drawing, Sentimental):**
> Create a new fine ink drawing of the dog in this photo, as an all-over blanket pattern. Keep exactly who he is in every repetition: the same face shape, ears, eyes, muzzle, coat colours and markings. Repeat him five to seven times across the whole square in quiet, tender moments: curled asleep on the bed, resting beside a morning coffee cup, with his bone tucked under his chin, always in his sweater. Soft, peaceful expressions and generous, even spacing, with soft irregular edges and no rectangular panel. Precise contours, deliberate hatching and a restrained warm wash on a light paper ground, in printable line weights. No text, no people, no other animals, no other objects.

**shepherd-warm-blanket (Juno, Cut-paper collage, Warm):**
> Create a new cut-paper collage of the dog in this photo, as an all-over blanket pattern. Keep exactly who she is in every repetition: the same face shape, ears, eyes, muzzle, coat colours and markings. Repeat her five to seven times across the whole square in bright, everyday moments: trotting on a walk in her harness, resting at her person's feet (only the feet show, never a face), and with her rope toy, giving it a knowing sideways glance. Bright eyes, a slight head tilt or a small knowing smile, varied angles with comfortable, even spacing, soft irregular edges and no rectangular panel. Distinct layered cut-paper shapes with visible paper fibres and subtle layer shadows, in warm, lively daylight colours. No photographic fur or painted impasto, no text, no other animals, no other objects.

## What the growth engine does next

Paints the remaining five stage-1 examples with these prompts, one generation each, judged against
the same checklist, with the results and prompts added to the review branch so heartside can see how
the short template behaves across styles, tones and formats before adopting it.
