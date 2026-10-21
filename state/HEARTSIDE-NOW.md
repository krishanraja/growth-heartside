# Heartside now

Read from `krishanraja/heartside` at commit `87c60af2c8` on 2026-10-21T10:26:55+00:00 UTC by `python3 growth.py sync`.
Rewritten when a sync finds heartside, its open pull requests or the store changed. Heartside's repository is the source of truth; this is a reading of it.

## Canon changed since the last sync

Read these again before drafting anything:

- changed: `README.md`
- changed: `docs/HANDOFF.md`
- changed: `docs/POSITIONING.md`
- changed: `docs/SYNC.md`

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

- `87c60af2c8` 2026-10-21 Merge pull request #35 from krishanraja/claude/festive-feynman-i7lvff
- `e822b23172` 2026-10-21 Rewrite POSITIONING and HANDOFF for v3 and the dog's own voice
- `0f345a77b2` 2026-10-21 Merge pull request #34 from krishanraja/claude/festive-feynman-i7lvff
- `8cf2ba06f6` 2026-10-21 Docs: the dog's own voice in V3 4.2, 5.2, 5.3, README and brand system

## Work in flight (open pull requests)

- none

## Latest decisions (`docs/V3-GIFTS-FROM-YOUR-DOG.md`, decision log)

- 2026-10-13: The Gemini key is in Krish's n8n as "Google Gemini(PaLM) - Heartside"; the AI runs through n8n webhooks. Sample order #1001 (the old HR-ring ornament) refunded by Krish; he reorders once the v3 page and products are live.
- 2026-10-13: Krish: "Build the two n8n webhooks and the site against section 11, switch everything on and merge everything to main." Built: the two webhooks are live in n8n (`n8n/README.md`), and the chat is in the theme as `hs3-chat` on hidden templates `?view=gifts` and `?view=landing` (`shopify/README.md`, v3). The live homepage is unchanged: the four gift products don't exist in Shopify yet, and section 7 keeps publishing for Sunday.
- 2026-10-14: Mug direction A chosen ("A"): the dog as a large cut-out on the outward face, the note on the drinker's face in Fraunces at 16pt or larger, and every preview on real product photos.
- 2026-10-15: Mug v3 approved; Shopify mug images replaced with two real-photo images ("yes to both").
- 2026-10-15: Cut-out and Fraunces redesign of the other three gifts judged "okay, pretty standard"; not built.
- 2026-10-15: Every-gift-as-a-letter rejected ("sounds shit").
- 2026-10-15: Krish asked for "10X personalized delight" from the first moment, using the AI edge and the breed corpus. Open.
- 2026-10-20: Krish, on a cart showing "Understands every word. Pretends he doesn't.": "It should be a message from your dog in their personality style... capture their demeanour, cross reference the corpus, and create literally a humanized warm message from the dog to the person with some humour and dog anthropomorphisms. Make sure all products create a warm message." So, on every gift: I, me and my are the dog, you is the person, never he, she or the dog's name, never the person's name, no exclamation marks, no "Dear" (the 15 Oct letter stays rejected; "Love, [dog]" is the only sign-off). Every scripted chip line was rewritten in that voice ("I took your side of the bed. Not sorry."). Compose now runs for every buyer, not only after a typed answer, so the AI writes all four lines as one message; the scripted lines show first and are the fallback. The chat has an optional "Breed, if you know it" field on step 1 (no new step); an exact corpus match sends its archetype to the AI as a light tone signal, never shown. This replaces the 13 Oct "no I" rule and the 15 Oct "no breed question yet".
