# Claude Code prompt: six painter fixes for heartside (recipes v11)

29 October 2026. Paste the prompt below into a Claude Code session on the `krishanraja/heartside`
repository. It changes the painter's recipe and regenerates the example prompts. It does not publish
the theme, change Teeinblue or touch the live store.

---

Read heartside's README and canon first, as every session does. Then make one change: recipes v10
(the directed brief, commit `ef76390` on `claude/product-launch-readiness-mlh1bc`) becomes v11 with the
six fixes below. They come from the growth engine painting all 24 breed examples from v10's own prompt
files; the evidence and reasoning are in `krishanraja/growth-heartside`, branch
`codex/heartside-examples-2026-10-29`, file `docs/briefs/painter-prompt/PROPOSAL.md`, section "Fixes
after painting stage 1 and 2". Krish approved sending them (29 October).

Work on a new branch from `claude/product-launch-readiness-mlh1bc`. The recipe is
`tools/print-art/recipes-v1.json` (version `actual-dog-recipes-v10-directed-brief`) and the code that
assembles it is `tools/print-art/artwork-system.mjs`.

1. **Hilarious stops using the velvet cushion.** Seven of the ten Hilarious and Over the top paintings
   put the toy on a red velvet cushion under a spotlight, so the two tones look the same.
   - `tones.hilarious.items`: drop the velvet cushion and spotlight examples. Say the joke's staging
     comes from the owner's stated place and activity, and that velvet, spotlights, curtains and stages
     are not used for Hilarious.
   - `tones.hilarious.light`: "bright, punchy light and bold diagonals." (no spotlight).
   - `scene.joke.toy`: replace the velvet cushion with a joke about the toy in the stated scene, for
     example "{pos} {toy} guarded like a priceless treasure, the dog standing watch over it".
   - Over the top keeps its royal-portrait staging, velvet included; it is the one tone that may use it.
2. **The joke keeps where the owner said the dog is.** Today the toy joke wins over the stated place,
   and the frenchie lost its couch and film to a theatre stage. In `artwork-system.mjs`, choose the
   Hilarious joke from the stated together or spot answer first, then home, and use the toy joke only
   when no place or activity was given. When a toy was named, add it into the chosen joke's scene
   rather than replacing the scene. Over the top: always keep the stated place in the scene line.
3. **Held items keep the owner's verb.** "A tennis ball in his mouth" became "with his tennis ball"
   and the ball ended up on the seat. Pass the owner's toy wording through unchanged (including "in his
   mouth", "hugged", "at her paws"), and only add "with" when the wording has no verb of its own. In
   the breed jobs, put the brief's verb into the toy field where the brief has one.
4. **No unnamed leash.** A walk added a leash and an implied person. Add "a leash or lead, unless the
   owner named one" to `avoid`.
5. **Blankets stay in the stated place.** A walk became mountains and a lake. Add to
   `formats.blanket.framing`: "The ground is the stated place only, with no invented landscape or
   scenery."
6. **Collage builds the dog from paper.** All three shepherd collages painted the dog's fur. Add to the
   collage style's grammar: "The dog itself is built from 20 to 30 hand-cut paper pieces, each one flat
   colour with scissor-cut or torn edges, with no brushwork or fur strands anywhere."

Then:
- Bump the version to `actual-dog-recipes-v11-directed-brief`, and write
  `tools/print-art/teeinblue/PROMPT-SPEC-2026-10-30.md` with the new exact text (keep the 10-29 spec as
  the record of v10).
- Add tests in `tools/print-art/artwork-system.test.mjs`: no "velvet" or "spotlight" in any Hilarious
  prompt; a stated couch or film survives a named toy in Hilarious; "in his mouth" survives; "leash" is
  in the avoid line; the collage prompt contains "hand-cut paper pieces".
- Regenerate `design/examples-2026-10-29-breeds/prompts/` with `tools/print-art/breed-batch.mjs` and the
  browser bundle with `tools/print-art/build-browser.mjs`. Run the repository's tests and builds and
  report each result.
- Do not publish the theme, change Teeinblue, deploy or push to `main`. Open one pull request and
  give Krish its link.

Finish with the list of regenerated prompt files for these 9 held jobs, which the growth engine will
repaint once the pull request is merged: golden-hilarious-blanket, lab-hilarious-mug,
lab-over_the_top-blanket, doodle-hilarious-blanket, dachshund-hilarious-mug,
dachshund-over_the_top-blanket, shepherd-hilarious-portrait, shepherd-over_the_top-mug,
shepherd-sentimental-mug. Also list which stage 1 prompts changed (lab-warm-portrait,
frenchie-hilarious-portrait, doodle-over_the_top-portrait, shepherd-warm-blanket), because their
current examples were held back for these same gaps.
