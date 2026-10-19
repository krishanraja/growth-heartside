# Heartside now

Read from `krishanraja/heartside` at commit `32cc8fa584` on 2026-10-19T04:48:33+00:00 UTC by `python3 growth.py sync`.
Rewritten when a sync finds heartside, its open pull requests or the store changed. Heartside's repository is the source of truth; this is a reading of it.

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
| [Tiny Me, For The Tree](https://heartside.io/products/tiny-me-for-the-tree) | $24 | yes |
| [The Body Double](https://heartside.io/products/the-body-double) | $59 | yes |
| [The Annual Review, Framed](https://heartside.io/products/the-annual-review-framed) | $89 | yes |
| [The Annual Review](https://heartside.io/products/the-annual-review) | $39 | yes |

## Recent commits on main

- `32cc8fa584` 2026-10-18 Merge pull request #13 from krishanraja/codex/product-handoff-2026-10-17
- `5ecbbe3f0a` 2026-10-18 docs: set North Star dates to agent speed
- `dfafcf0190` 2026-10-18 docs: add the North Star and anchor every session to it

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
