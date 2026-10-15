# Heartside now

Read from `krishanraja/heartside` at commit `1faf8e82b5` on 2026-10-15T10:08:35+00:00 UTC by `python3 growth.py sync`.
Rewritten when a sync finds heartside, its open pull requests or the store changed. Heartside's repository is the source of truth; this is a reading of it.

## Canon changed since the last sync

Read these again before drafting anything:

- changed: `README.md`

## The canon, in heartside's order

1. `docs/V3-GIFTS-FROM-YOUR-DOG.md`
2. `docs/POSITIONING.md`
3. `docs/HANDOFF.md`
4. `docs/SYNC.md`
5. `README.md`
6. `design/BRAND-SYSTEM.md`
7. `shopify/README.md`

## On sale at heartside.io now

| Product | Price | Available |
|---|---|---|
| [Tiny Me, For The Tree](https://heartside.io/products/tiny-me-for-the-tree) | $24 | yes |
| [The Body Double](https://heartside.io/products/the-body-double) | $59 | yes |
| [The Annual Review, Framed](https://heartside.io/products/the-annual-review-framed) | $89 | yes |
| [The Annual Review](https://heartside.io/products/the-annual-review) | $39 | yes |

## Recent commits on main

- `1faf8e82b5` 2026-10-15 Merge pull request #7 from krishanraja/claude/gracious-turing-kbsuss
- `4b1165a1db` 2026-10-15 README: point to the growth engine and the canon line it reads
- `c233185891` 2026-10-15 Merge pull request #6 from krishanraja/cowork-handover-2026-10-15
- `34b3ec133b` 2026-10-15 Explored, not approved: mug directions, three-gift redesign, rejected letter direction
- `bff5220396` 2026-10-15 Real-photo mug tools: cylinder wrap, mockup builder, print masks, Teeinblue simulator, Shopify image renders
- `79a8d6e1e7` 2026-10-15 Fraunces fonts used by the mug v3 artwork and preview renders, with OFL license
- `f248066be3` 2026-10-15 Mug v3 Teeinblue source assets: background, photo mask, sample, mockup bases, shades, print masks, geometry
- `4f75310dce` 2026-10-15 Breed corpus audit, US lookup additions and US display names
- `5bbeac50ea` 2026-10-15 Mug v3 evidence: real-photo renders, print files, Teeinblue previews, Shopify images
- `328e9abd4a` 2026-10-15 Cowork handover for the next session (15 Oct)
- `29aafaaa8c` 2026-10-15 Cowork evidence 14-15 Oct: round reports and the mug v3 spec

## Work in flight (open pull requests)

- none

## Latest decisions (`docs/V3-GIFTS-FROM-YOUR-DOG.md`, decision log)

- 2026-10-13: Launch moved to Sunday 18 October ("aim for 5 days from now").
- 2026-10-13: Product direction: words in the owner's voice about their dog (Krish's pick), then reframed by Krish the same day to gifts given on behalf of the dog to someone it loves, everyday functional gifts.
- 2026-10-13: Concept process: three independent concepts (conversation, recognition deck, print-as-interface), two blind judges; the conversation with Biscuit won, with grafts from the other two. Trace in the Cowork session.
- 2026-10-13: Prototype approved ("I love it"), with two changes: make the choice of gifts obvious, and make Biscuit talk a bit like a dog. Both made in version 7; approved ("love it").
- 2026-10-13: AI drawings from answers deferred to phase two, as illustrations, gated by a five-dog likeness test.
- 2026-10-13: Krish approved the prices, hiding the HR poster, framed poster and pillow, and the twice-daily order check. Live AI stays in version one, as agreed, using Gemini with Krish's key. Krish: "This is a Shopify business": no new outside project. Where the key sits is his call (5.4).
- 2026-10-13: The Gemini key is in Krish's n8n as "Google Gemini(PaLM) - Heartside"; the AI runs through n8n webhooks. Sample order #1001 (the old HR-ring ornament) refunded by Krish; he reorders once the v3 page and products are live.
- 2026-10-13: Krish: "Build the two n8n webhooks and the site against section 11, switch everything on and merge everything to main." Built: the two webhooks are live in n8n (`n8n/README.md`), and the chat is in the theme as `hs3-chat` on hidden templates `?view=gifts` and `?view=landing` (`shopify/README.md`, v3). The live homepage is unchanged: the four gift products don't exist in Shopify yet, and section 7 keeps publishing for Sunday.
