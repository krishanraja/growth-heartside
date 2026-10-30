# Proposal for heartside: a short, directed painter prompt

29 October 2026. From the growth engine to a heartside build session. Heartside's canon beats this
repository, so this is a proposal only: nothing here changes heartside or the store.

## What we found

The painter today sends a rulebook of about 5,500 characters (`tools/print-art/native-candidate.mjs`
with `artwork-system` recipes v6). With a customer's photo as the edit input, that prompt returns the
photo's own pose, angle and face, with photographic eyes and fur, whatever the tone or style says. The
golden example made that way (v1 to v3) was awake when the buyer said "mid-nap", had no collar or
person, and had a photographic face. A plain prompt of about 1,200 characters fixed all of that in one
generation (the golden master, v7).

A control test then ran the short-prompt method on two photos: an easy stock golden and a hard case
(a black rescue dog, small in the frame, in dim, busy light). It covered 3 tones, 6 styles, 4 kinds of
chat answer and 3 products: 47 generations, each checked byte for byte against what was sent.

- **Without a stated pose and camera, the model reuses the photo's pose** and one safe layout ("dog by
  the feet, looking at you"). Tone changed only the light, so Warm and Hilarious were near-identical,
  and every style of the hard dog was the photo's pose (evidence 1 and 4).
- **When each tone owns the pose, camera and staging, tone reads at a glance** for both dogs
  (evidence 2): Sentimental asleep, Warm caught mid-moment, Hilarious a visual joke.
- **Hilarious needs a visual joke, not an attitude.** "Deadpan" in oil reads as solemn. A stated toy
  on a velvet cushion under a spotlight, or the dog perched on the couch back like a film critic, reads
  as funny (evidence 3).
- **Each style needs its medium described as material behaviour, with the dog made of it.** Cinematic,
  comic and ink pass. Collage passes once the dog itself is "20 to 30 hand-cut paper pieces"; screenprint
  is right on the hard dog but a long coat still shows fur strands (evidence 5 and 6).
- **Chat answers come through:** a typed answer appears (ball and laptop, the TV), and "no toy" is
  respected. With no answers at all, the photo's pose returns unless the tone names one (evidence 7).
- **Products:** the mug keeps the dog left with the note area plain; the blanket repeats varied poses
  (evidence 8).
- **Words the model takes literally:** "wink" closes one eye (lab v1, golden collage). Patterned
  clothing grows fake lettering (lab v2). Percentages for framing are ignored; scene words work.

## What to change

Replace the rulebook with a brief built from the chat's own fields: photo, breed, pronoun, the home,
spot and together answers (chip or typed), toy, accessory, tone, style and product. The reference
builder is `brief_builder.py` beside this file. Its order:

1. Medium and product shape, then "of the dog in this photo".
2. Identity in one line: this breed's face shape, ears, eyes, muzzle, coat colours and markings. Then
   "Change everything else; never reuse the photo's pose, angle, light or background."
3. Staging owned by the tone, always with an explicit pose and camera:
   - Sentimental: asleep or resting, eyes closed, close and low, soft window light.
   - Warm: caught mid-moment (from the together or home answer), three-quarter view, candid, daylight,
     both eyes open.
   - Hilarious: one visual joke built on the stated thing (its scale or importance, never the dog's
     anatomy), worm's-eye wide-angle, theatrical light.
4. Composition owned by the style, then the product's framing in scene words.
5. The medium, as how the material behaves, with the face made the same way.
6. An avoid list that also bans what a theme invites: food and snacks, visible screens, patterned
   clothing, lettering, any object not named.

## Rulings and decisions

- Ruling (Krish, 2026-10-29): Hilarious may use theatrical staging (a cushion, a spotlight, the
  buyer's own couch cushions piled high); it never invents the dog's toys, food, clothes, habits or
  places.
- Every worn item is described as plain and solid-coloured.

## Open for heartside

- **Identity has no anchors in production.** The test used only breed and "this dog's face, ears…".
  Likeness held on both dogs, but a hand-written anchor line (coat shades, markings) made the golden
  master closer. A vision step that writes that one line from the photo would help, kept to one
  sentence: more detail pulls the photo's face back in.
- **"Over the top" is used in an example (the doodle) but is not a tone the store offers** (it has
  sentimental, warm and hilarious). Either drop that example or add the tone.
- **Screenprint on long coats** still shows fur strands; one more wording pass or accepting it.
- **One generation per order** stays true: every image here is a single generation from the photo.

## Fixes after painting stage 1 and 2 from recipes v10 (29 October)

Heartside adopted the directed brief as recipes v10 (`ef76390`). The 24 example paintings made
from its own prompt files show six gaps that a real customer would hit too. Krish approved
sending them (29 October). Of the 18 stage 2 paintings, 9 were approved and 9 held for these.

1. **Hilarious and Over the top use the same gag.** Seven of ten put the stated toy on a red velvet
   cushion under a spotlight with red curtains, so the two tones look the same and repeat. The
   example in this proposal ("a toy on a velvet cushion under a spotlight") was copied into the
   recipe and became the default. Fix: Hilarious builds its joke from the buyer's own answer (the
   couch as a film critic's balcony, the coffee guarded like treasure, the feet pinned like a
   paperweight) and does not use velvet, spotlights or curtains. Over the top keeps the grand,
   symmetrical royal-portrait staging.
2. **The joke can overwrite where the owner said the dog is.** The stage 1 frenchie lost its couch and
   film to a theatre stage. Keep the stated place and activity, with the joke built on them.
3. **Held items lose their verb.** "A tennis ball in his mouth" became "with his tennis ball", and the
   ball ended up on the seat. Keep the owner's verb (in the mouth, hugged, at the paws).
4. **Settings invite unnamed accessories.** A walk added a leash. Add "leash" to the avoid list
   unless the owner named one.
5. **Blankets invent scenery** (mountains and a lake for "out on a walk"). Keep a blanket's ground to
   the stated place.
6. **Collage paints the dog.** All three shepherd collages are painted fur. Use the wording proven in
   the control test: "the dog itself built from 20 to 30 hand-cut paper pieces, each one flat colour
   with scissor-cut or torn edges, no brushwork or fur strands anywhere".

The approvals ledger beside the examples folder
(`assets/heartside-examples-2026-10-29.approvals.json`) records which painting of each job is
approved, with its hash and prompt; only those may be copied to Drive, GitHub or the store.

## Evidence

The before-and-after grids were removed on 29 October 2026 with the other rejected artwork; the
approvals ledger records every candidate and why it was not used. The stage 1 examples built with this method are on branch
`codex/heartside-examples-2026-10-29` under `assets/heartside-examples-2026-10-29/`.
