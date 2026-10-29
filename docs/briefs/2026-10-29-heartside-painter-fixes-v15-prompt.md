# Claude Code prompt: painter v15 for heartside (blankets as a scattered pattern)

29 October 2026. Paste into a Claude Code session on `krishanraja/heartside`. Same rules as before: no
theme publish, no Teeinblue change, no push to `main`; one pull request.

---

Read heartside's README and canon first. Then make recipes v14 (`claude/product-launch-readiness-mlh1bc`,
merge `7ed61c3`) into v15 with one change, to the blanket. Krish reviewed the blanket examples (29 October):
the dogs overlap, crop and grow out of each other, so Maple's blanket "looks like he is surrounded by lots
of other disembodied versions of himself... a bit creepy", a "dog centipede". Most of the eight blankets
show it. He wants the look of a printed fleece pattern, like an Oodie: small, separate, whole motifs
scattered on a plain fabric ground.

The cause is `formats.blanket.framing` in `tools/print-art/recipes-v1.json`: "five or six different poses
of the dog drawn from this scene, edge to edge ... motifs may run off the edges", with each pose drawn as
part of a full scene, so the poses and their scenery pile into one another.

Replace the blanket layout with a scattered pattern:
- "An all-over scattered pattern for a sherpa blanket, like a printed fleece throw: eight to twelve small,
  complete figures of the same dog, each one whole and separate, evenly spaced with clear plain ground
  around every figure. Dogs never overlap, touch, merge or share a body, and none is cut off except where
  it meets the blanket's outer edge. The ground is one soft, plain colour that suits the style, with at
  most a few tiny scattered motifs from the owner's own answers (a toy, a paw print). No scene, horizon,
  furniture or landscape behind the dogs."
- Vary the poses across the figures: the tone's moment (asleep for Sentimental, mid-moment for Warm, the
  joke for Hilarious, smug for Over the top), plus sitting, lying and playing with the named toy. Every
  figure shows the same dog with the same markings and the same named clothing.
- The style still applies to every figure (oil, ink, collage, comic, screenprint, cinematic), and figures
  must be large enough to read the dog's face across a room.
- In `tools/print-art/artwork-system.mjs`, for the blanket drop the scene lines (setting, place, camera)
  that only make sense for a single picture, keeping the tone, toys and clothing.

Bump to `actual-dog-recipes-v15-directed-brief`, write the next `PROMPT-SPEC`, add tests (every blanket
prompt says figures never overlap; no blanket prompt asks for a scene or "edge to edge"), regenerate
`design/examples-2026-10-29-breeds/prompts/` and the browser bundle, run the tests and builds, report each
result, and open one pull request. List the eight blanket prompt files and say whether any non-blanket
prompt changed.
