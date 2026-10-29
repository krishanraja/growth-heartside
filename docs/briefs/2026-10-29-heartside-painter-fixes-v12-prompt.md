# Claude Code prompt: two painter fixes for heartside (recipes v12)

29 October 2026. Paste into a Claude Code session on `krishanraja/heartside`. Same rules as v11: no
theme publish, no Teeinblue change, no push to `main`; one pull request.

---

Read heartside's README and canon first. Then make recipes v11 (`claude/product-launch-readiness-mlh1bc`,
merge `1b9a775`) into v12 with two fixes. They come from painting the 24 breed examples from v11's own
prompt files: 22 passed, the two shepherd jobs did not. Krish asked for these fixes (29 October).

1. **A Hilarious joke must show something that makes it a joke.** `shepherd-hilarious-portrait`
   ("the dog leading the morning walk like the grand marshal of a parade") came out as a dog on a hiking
   trail: since v11 bans props and sets, nothing in the frame said "parade". Rewrite each
   `scene.joke` line in `tools/print-art/recipes-v1.json` so the joke is carried by a visible contrast
   built only from what the owner stated, the dog and their person. For `walk`: "marching far out in
   front with chest out and a high, proud stride like the leader of a parade, {pos} person (only their
   legs) hurrying to keep up far behind on the path". Check the other joke lines the same way (each must
   be readable with the caption covered) and add to `tones.hilarious`: "The joke must be readable at a
   glance with no caption: show the contrast, not just the dog."
2. **One place per scene, and no invented landscape on any product.** `shepherd-over_the_top-mug` got
   "curled at her person's feet" and "out on the morning walk" in the same scene line, and resolved the
   clash with an invented mountainside. In `tools/print-art/artwork-system.mjs`, when the spot answer
   and the together answer name different places, use one: Over the top and Sentimental take the spot,
   Warm and Hilarious take the together activity. Move v11's blanket-only line into every format: "The
   setting is the stated place only, with no invented landscape or scenery."

Then bump to `actual-dog-recipes-v12-directed-brief`, write `tools/print-art/teeinblue/PROMPT-SPEC-2026-10-30b.md`,
and add tests: the walk joke contains "keep up"; a feet-plus-walk Over the top prompt has one place; every
format's prompt contains "no invented landscape". Regenerate `design/examples-2026-10-29-breeds/prompts/`
and the browser bundle, run the tests and builds, report each result, and open one pull request.

Finish by listing which of the 24 prompt files changed beyond the shared lines, so the growth engine
knows which approved examples, if any, differ from the store's current output.
