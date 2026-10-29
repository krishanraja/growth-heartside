# Claude Code prompt: painter v14 for heartside (the note area, and a Hilarious walk worth $119)

29 October 2026. Paste into a Claude Code session on `krishanraja/heartside`. Same rules as before: no
theme publish, no Teeinblue change, no push to `main`; one pull request.

---

Read heartside's README and canon first. Then make recipes v13 (`claude/product-launch-readiness-mlh1bc`,
merge `1bb9243`) into v14 with two fixes. Krish rejected the v13 painting of `shepherd-hilarious-portrait`
(29 October): "if I was paying $119 I would not accept that".

1. **The note area is a quiet part of the scene, never a blank patch.** The v13 portrait prompt asks for
   the lower-right quarter to be left plain twice, once in the scene line and once in the framing, and
   the collage style rendered it literally as a bare, torn sheet of paper filling a quarter of the
   portrait. A customer choosing collage would get the same. Say it once, in the framing only, and say
   what it is: "The lower-right quarter is a calm, low-detail continuation of the scene (soft ground,
   plain wall or sky in the same medium), where a small note will be added later; never a blank sheet,
   card, label, frame or empty patch." Apply the same wording to the mug's note area. Add a test that
   no prompt mentions the note area twice and none asks for anything "plain" or "blank" on its own.
2. **The walk joke has to be funny, not just proud.** After four tries the "parade" walk reads as a
   dog walking proudly. Rewrite `scene.joke.walk` so the joke lands from the owner's own words alone,
   with no person and no props: "the dog leading the morning walk like a five-star general inspecting
   the troops: bolt upright, chest puffed out, one front paw raised mid-march, chin high, an utterly
   serious expression, the rope toy clamped like a field marshal's baton". Keep the same structure
   for a stated toy and drop the baton when no toy is named.

Bump to `actual-dog-recipes-v14-directed-brief`, write the next `PROMPT-SPEC` file, regenerate
`design/examples-2026-10-29-breeds/prompts/` and the browser bundle, run the tests and builds, report
each result, and open one pull request. List which of the 24 prompt files changed beyond the shared
note line, so the growth engine knows whether any approved example differs from the store's output.
