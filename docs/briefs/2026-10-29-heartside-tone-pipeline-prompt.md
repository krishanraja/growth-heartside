# Claude Code prompt: the tone pipeline upgrade for heartside (breed character, every answer, real parody)

29 October 2026. A standalone data and AI pipeline session. Paste into Claude Code on
`krishanraja/heartside`. No theme publish, no Teeinblue change, no push to `main`; one pull request.
Generating test images spends credits, so the test board waits for Krish's yes.

---

Read heartside's README, canon and `NOW.md` first. This session upgrades how the painter turns everything
Heartside knows about a dog into the scene, so each tone (Sentimental, Warm, Hilarious, Over the top) feels
written for that particular dog. Krish (29 October): "with what we know about each breed in the corpus plus
all the data inputs by then, we should be able to draw on some stereotypes and exaggerations and parodies".

**What the growth engine found** painting the 24 breed examples (evidence in `krishanraja/growth-heartside`,
`assets/heartside-examples-2026-10-29.approvals.json` and `docs/briefs/painter-prompt/PROPOSAL.md`):

1. **The scene comes from one answer.** In `shopify/assets/hs-brief.js` the Hilarious joke is
   `JOKE[o.together]` and Over the top is `ROYAL[o.together]`: one fixed line per "Best thing you do
   together" chip. Two buyers who both tap Walks get the same joke whatever their dog. Five versions of
   the walk joke never landed; the jokes that did (car rides as driving, coffee as the chairman) were the
   ones where the answer happened to imply a human situation.
2. **Half the chat never reaches the painting.** "When you get home…" (door, brings something, spins,
   plays it cool) and "What [dog] is to them" (a shadow, a best friend, there on hard days, the boss of
   the house) are collected in `shopify/assets/hs-journey.js` but barely shape the image. "The boss of the
   house" and "spins in circles" are ready-made comedy that is thrown away.
3. **The breed corpus is flattened to a whisper.** `breeds-corpus/dog_corpus_completed.csv` (370 breeds
   and crosses) gives every dog a vivid archetype: Terrier Menace, Spitz Commentator, Sighthound Sofa
   Missile, Scent Detective, Herding Manager, Working Goofball, Companion Velcro, Doodle Wildcard,
   Guardian, Retriever. The recipe (`energy` in `tools/print-art/recipes-v1.json`) reduces each to a
   bland pose code ("elegant-languid", "curious-unhurried") and calls it "a light signal, never a prop
   or habit". So a beagle and a greyhound get the same joke, though "Scent Detective" and "Sighthound
   Sofa Missile" are themselves jokes.

**Build this:**
- **A comedy and character layer, per archetype and per tone.** For each corpus archetype, write the
  well-known, affectionate breed stereotype it carries (the herding dog who herds the family, the
  sighthound folded onto the sofa like a dropped coat, the scent hound led everywhere by its nose, the
  spitz with opinions, the terrier who thinks it is a lion) and how each tone treats it: Sentimental
  softens it, Warm smiles at it, Hilarious exaggerates it into a visible situation, Over the top crowns it.
  Stereotypes are affectionate and about breed behaviour only, never about a buyer, a person, a culture
  or a dog's health, age or death (heartside's voice rules apply).
- **A composer that combines everything** for one picture: breed archetype + home + spot + together +
  meaning + toys + clothing + tone. Rank the candidate scenes by how strongly they fit this dog, and pick
  one clear visual situation. The buyer's stated facts always win; the archetype colours how they play
  out (a Herding Manager on Walks herds the walk; a Sighthound on Naps is a sofa missile; "the boss of the
  house" plus Terrier Menace is a tiny dictator). Mixed or unknown breeds use the buyer's answers only,
  as today.
- **Revisit the rulings that block this, and put the trade-offs to Krish rather than deciding alone:**
  the 27 October ruling keeps breed energy to "mood, pose, expression" and bars it from adding props or
  habits; v13 bans theatrical props for Hilarious. Propose exactly what changes (for example: archetype
  behaviour may shape the situation; Hilarious may add one small prop a joke needs, never the dog's own
  toys, food, clothes or habits) and what never changes.
- **Make it deterministic and testable.** Same inputs, same brief. Unit tests for every archetype × tone ×
  together combination (no empty, contradictory or duplicated scene lines; facts always present).

**Prove it before customers see it.** Propose a test board: the same photo-real inputs a buyer would tap,
across several archetypes (at least Retriever, Terrier Menace, Sighthound Sofa Missile, Scent Detective,
Herding Manager, Spitz Commentator) × the four tones, painted with the store's own path. State the count
and wait for Krish's yes. He judges it at a $119 standard: each picture must read as that tone at a
glance and feel like that dog. Keep only what he approves.

Bump the recipe version, write the next `PROMPT-SPEC`, regenerate the breed example prompts and the
browser bundle, run the tests and builds, report each result, and open one pull request with the test
board linked.
