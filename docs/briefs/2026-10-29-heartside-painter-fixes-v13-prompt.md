# Claude Code prompt: painter v13 for heartside (no floating people, a walk joke that needs no person)

29 October 2026. Paste into a Claude Code session on `krishanraja/heartside`. Same rules as before: no
theme publish, no Teeinblue change, no push to `main`; one pull request.

---

Read heartside's README and canon first. Then make recipes v12 (`claude/product-launch-readiness-mlh1bc`,
merge `5710175`) into v13 with two fixes. Krish rejected two v12 paintings of `shepherd-hilarious-portrait`
(29 October): in both, the person's legs come in at the edge and end in the open sky, which looks broken,
and the "leader of a parade" walk joke still did not read as funny.

1. **People are never cut off against open space.** Add one rule to every prompt (beside the avoid
   line): "When part of the person shows, it enters from the edge of the frame on the same ground as the
   dog and is cut only by the frame edge, never ending in open space or sky; with a low or worm's-eye
   camera, leave the person out." Apply it in `tools/print-art/artwork-system.mjs` so a Hilarious prompt
   with a worm's-eye camera drops every "(only their legs …)" person phrase.
2. **The walk joke needs no person.** Replace `scene.joke.walk` in `tools/print-art/recipes-v1.json`
   with an exaggeration of what the owner stated, the walk and the toy: "the dog marching on the morning
   walk with a proud, high-stepping parade stride, chest out and tail up like a flag, carrying {pos} toy
   like a trophy". When a toy is named, exaggerate its importance in the dog's carriage, never its size
   or the dog's body. When no toy is named, keep the stride and drop the trophy. Check the other joke
   lines: any that needs a partial person to be funny gets the same treatment.

Bump to `actual-dog-recipes-v13-directed-brief`, write `tools/print-art/teeinblue/PROMPT-SPEC-2026-10-30c.md`,
and add tests: a worm's-eye Hilarious prompt has no "only their legs"; the cut-off rule is in every
prompt; the walk joke has no person. Regenerate `design/examples-2026-10-29-breeds/prompts/` and the
browser bundle, run the tests and builds, report each result, and open one pull request. Finish by
listing which of the 24 prompt files changed beyond the shared rule line.
