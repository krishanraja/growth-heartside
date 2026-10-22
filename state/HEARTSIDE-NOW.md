# Heartside now

Read from `krishanraja/heartside` at commit `64cc3f5a5d` on 2026-10-21T18:41:59+00:00 UTC by `python3 growth.py sync`.
Rewritten when a sync finds heartside, its open pull requests or the store changed. Heartside's repository is the source of truth; this is a reading of it.

## Canon changed since the last sync

Read these again before drafting anything:

- changed: `docs/HANDOFF.md`
- changed: `shopify/README.md`

## The canon, in heartside's order

1. `docs/V3-GIFTS-FROM-YOUR-DOG.md`
2. `docs/POSITIONING.md`
3. `docs/HANDOFF.md`
4. `docs/COWORK-HANDOVER-2026-10-15.md`
5. `docs/HANDOVER-2026-10-17.md`
6. `docs/SYNC.md`
7. `README.md`
8. `design/BRAND-SYSTEM.md`
9. `shopify/README.md`

## On sale at heartside.io now

| Product | Price | Available |
|---|---|---|
| [The Tree Ornament](https://heartside.io/products/the-tree-ornament) | $24 | yes |
| [The Framed Print](https://heartside.io/products/the-framed-print) | $89 | yes |
| [The Couch Blanket](https://heartside.io/products/the-couch-blanket) | $89 | yes |
| [The Morning Mug](https://heartside.io/products/the-morning-mug) | $29 | yes |

## Recent commits on main

- `64cc3f5a5d` 2026-10-21 Merge pull request #43 from krishanraja/claude/jolly-planck-5mf1bi
- `39698070d7` 2026-10-21 Cowork prompt for the first mock order; HANDOFF points to it
- `3add64a2bd` 2026-10-21 Merge pull request #42 from krishanraja/claude/jolly-planck-5mf1bi
- `b343580e55` 2026-10-21 HANDOFF: one-screen homepage and gift page, hidden answers on orders, deploy from main
- `ba42117031` 2026-10-21 Merge pull request #41 from krishanraja/claude/jolly-planck-5mf1bi
- `dee0513833` 2026-10-21 Merge remote-tracking branch 'origin/main' into claude/jolly-planck-5mf1bi
- `5440649eb9` 2026-10-21 Hidden chat answers reach the order again
- `895bcdf343` 2026-10-21 Gift product page: one screen, no scroll, radical simplicity
- `74f8e90f1b` 2026-10-21 Homepage fits one screen with no scroll on every device; footer signup can be switched off
- `eda5b2accf` 2026-10-21 Merge pull request #40 from krishanraja/claude/festive-feynman-i7lvff
- `99f1c8cc7d` 2026-10-21 Cowork launch prompt: today's live site work, share-card cache refresh, search listings in the job and report
- `b9787b664f` 2026-10-21 Merge pull request #39 from krishanraja/claude/festive-feynman-i7lvff
- `b96c44d212` 2026-10-21 Footer Answers link in the company-note row; Cowork search-listing steps
- `a814b1b5eb` 2026-10-21 Merge pull request #38 from krishanraja/claude/festive-feynman-i7lvff
- `e5a0af212d` 2026-10-21 Favicon and v3 share card go live: theme push gains a favicon option
- `3c3f346dbf` 2026-10-21 Merge pull request #37 from krishanraja/claude/festive-feynman-i7lvff
- `126c6ce352` 2026-10-21 Answers button uses the growth engine's tracking params
- `89519a8a36` 2026-10-21 Search and answer engines: structured data, brand-first llms.txt, Answers template; favicon and share-card drafts
- `684a74835b` 2026-10-21 Merge pull request #36 from krishanraja/claude/festive-feynman-i7lvff
- `745adfff36` 2026-10-21 HANDOFF: renumber work left and open questions
- `1333330b7b` 2026-10-21 Cowork launch-and-test-order handoff; docs record the new product images
- `cef09ae41c` 2026-10-21 Product images in the dog's own voice: mug note faces and the other three gifts
- `87c60af2c8` 2026-10-21 Merge pull request #35 from krishanraja/claude/festive-feynman-i7lvff
- `e822b23172` 2026-10-21 Rewrite POSITIONING and HANDOFF for v3 and the dog's own voice
- `0f345a77b2` 2026-10-21 Merge pull request #34 from krishanraja/claude/festive-feynman-i7lvff
- `8cf2ba06f6` 2026-10-21 Docs: the dog's own voice in V3 4.2, 5.2, 5.3, README and brand system

## Work in flight (open pull requests)

- none

## Latest decisions (`docs/V3-GIFTS-FROM-YOUR-DOG.md`, decision log)

- 2026-10-13: Krish: "Build the two n8n webhooks and the site against section 11, switch everything on and merge everything to main." Built: the two webhooks are live in n8n (`n8n/README.md`), and the chat is in the theme as `hs3-chat` on hidden templates `?view=gifts` and `?view=landing` (`shopify/README.md`, v3). The live homepage is unchanged: the four gift products don't exist in Shopify yet, and section 7 keeps publishing for Sunday.
- 2026-10-14: Mug direction A chosen ("A"): the dog as a large cut-out on the outward face, the note on the drinker's face in Fraunces at 16pt or larger, and every preview on real product photos.
- 2026-10-15: Mug v3 approved; Shopify mug images replaced with two real-photo images ("yes to both").
- 2026-10-15: Cut-out and Fraunces redesign of the other three gifts judged "okay, pretty standard"; not built.
- 2026-10-15: Every-gift-as-a-letter rejected ("sounds shit").
- 2026-10-15: Krish asked for "10X personalized delight" from the first moment, using the AI edge and the breed corpus. Open.
- 2026-10-20: Krish, on a cart showing "Understands every word. Pretends he doesn't.": "It should be a message from your dog in their personality style... capture their demeanour, cross reference the corpus, and create literally a humanized warm message from the dog to the person with some humour and dog anthropomorphisms. Make sure all products create a warm message." So, on every gift: I, me and my are the dog, you is the person, never he, she or the dog's name, never the person's name, no exclamation marks, no "Dear" (the 15 Oct letter stays rejected; "Love, [dog]" is the only sign-off). Every scripted chip line was rewritten in that voice ("I took your side of the bed. Not sorry."). Compose now runs for every buyer, not only after a typed answer, so the AI writes all four lines as one message; the scripted lines show first and are the fallback. The chat has an optional "Breed, if you know it" field on step 1 (no new step); an exact corpus match sends its archetype to the AI as a light tone signal, never shown. This replaces the 13 Oct "no I" rule and the 15 Oct "no breed question yet".
- 2026-10-21: Krish: "yes, re-render the product images in the dog's voice". Done the same day:
- 2026-10-22: Krish on the AI's gift lines: "They all sound like Claude... Two-word sentences stacked against two- or three-word sentences are just a clear tell... A border collie would sound different to a poodle if they were human." Live the same day (heartside PR #44): each dog writes in its breed-corpus archetype's voice, one natural sentence per line, lines up to 60 characters (meaning 44 for the ornament), Claude Sonnet writes the note, the mug prints at 58 px. The three published Answers articles now quote the new voice. Growth copy must never quote the old stacked lines ("Weekends too. Obviously.", "Not sorry.").
