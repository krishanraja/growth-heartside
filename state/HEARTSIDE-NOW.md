# Heartside now

Read from `krishanraja/heartside` at commit `5618a99829` on 2026-10-15T19:12:54+00:00 UTC by `python3 growth.py sync`.
Rewritten when a sync finds heartside, its open pull requests or the store changed. Heartside's repository is the source of truth; this is a reading of it.

## Canon changed since the last sync

Read these again before drafting anything:

- changed: `docs/COWORK-HANDOVER-2026-10-15.md`
- changed: `shopify/README.md`

## The canon, in heartside's order

1. `docs/V3-GIFTS-FROM-YOUR-DOG.md`
2. `docs/POSITIONING.md`
3. `docs/HANDOFF.md`
4. `docs/SYNC.md`
5. `docs/COWORK-HANDOVER-2026-10-15.md`
6. `README.md`
7. `design/BRAND-SYSTEM.md`
8. `shopify/README.md`

## On sale at heartside.io now

| Product | Price | Available |
|---|---|---|
| [Tiny Me, For The Tree](https://heartside.io/products/tiny-me-for-the-tree) | $24 | yes |
| [The Body Double](https://heartside.io/products/the-body-double) | $59 | yes |
| [The Annual Review, Framed](https://heartside.io/products/the-annual-review-framed) | $89 | yes |
| [The Annual Review](https://heartside.io/products/the-annual-review) | $39 | yes |

## Recent commits on main

- `5618a99829` 2026-10-15 Merge pull request #12 from krishanraja/claude/keen-albattani-bijgeg
- `b3d5c23c2d` 2026-10-15 First screen: the real-photo mug replaces the drawn one; Cowork's next prompt
- `25830340b8` 2026-10-15 Mug text curves as the photo does: more toward the base
- `fdd656e297` 2026-10-15 Merge pull request #11 from krishanraja/claude/keen-albattani-bijgeg
- `bda2340a8c` 2026-10-15 Order QC is scheduled: twice daily, waiting on Shopify being connected
- `f045a2bfb8` 2026-10-15 Merge pull request #10 from krishanraja/claude/keen-albattani-bijgeg
- `ffe773f4d0` 2026-10-15 Order QC for the mug: check each order's real print file before it prints
- `77124f79bd` 2026-10-15 Chat mug drawn as the approved images are, held to Teeinblue's print files
- `17d5d34cac` 2026-10-15 Merge pull request #9 from krishanraja/claude/keen-albattani-bijgeg
- `a7aa67ac16` 2026-10-15 Handover: the 15 Oct work is merged and live on the theme
- `80f7fd946b` 2026-10-15 Merge pull request #8 from krishanraja/claude/keen-albattani-bijgeg
- `f4a5bc003b` 2026-10-15 Handover: next session prompt on main, Krish's evening ask, the one idea
- `9b85b23ecb` 2026-10-15 Handover section 5: items 3, 4 and 7 marked done, with commit links
- `d81697569a` 2026-10-15 US spelling in a comment and a test label (centered)
- `5cc02fed14` 2026-10-15 V3: five dated decisions in section 13; the mug's lines are in Fraunces
- `7f51d5329b` 2026-10-15 Mug reveal on the real mug, even line breaks, paws, chip-style typed lines
- `68c67d3786` 2026-10-15 Breed lookup the chat can call later
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

- 2026-10-13: Krish approved the prices, hiding the HR poster, framed poster and pillow, and the twice-daily order check. Live AI stays in version one, as agreed, using Gemini with Krish's key. Krish: "This is a Shopify business": no new outside project. Where the key sits is his call (5.4).
- 2026-10-13: The Gemini key is in Krish's n8n as "Google Gemini(PaLM) - Heartside"; the AI runs through n8n webhooks. Sample order #1001 (the old HR-ring ornament) refunded by Krish; he reorders once the v3 page and products are live.
- 2026-10-13: Krish: "Build the two n8n webhooks and the site against section 11, switch everything on and merge everything to main." Built: the two webhooks are live in n8n (`n8n/README.md`), and the chat is in the theme as `hs3-chat` on hidden templates `?view=gifts` and `?view=landing` (`shopify/README.md`, v3). The live homepage is unchanged: the four gift products don't exist in Shopify yet, and section 7 keeps publishing for Sunday.
- 2026-10-14: Mug direction A chosen ("A"): the dog as a large cut-out on the outward face, the note on the drinker's face in Fraunces at 16pt or larger, and every preview on real product photos.
- 2026-10-15: Mug v3 approved; Shopify mug images replaced with two real-photo images ("yes to both").
- 2026-10-15: Cut-out and Fraunces redesign of the other three gifts judged "okay, pretty standard"; not built.
- 2026-10-15: Every-gift-as-a-letter rejected ("sounds shit").
- 2026-10-15: Krish asked for "10X personalized delight" from the first moment, using the AI edge and the breed corpus. Open.
