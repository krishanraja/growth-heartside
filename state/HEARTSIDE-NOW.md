# Heartside now

Read from `krishanraja/heartside` at commit `1028556df9` on 2026-10-14T20:44:33+00:00 UTC by `python3 growth.py sync`.
Rewritten when a sync finds heartside, its open pull requests or the store changed. Heartside's repository is the source of truth; this is a reading of it.

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

- `1028556df9` 2026-10-14 v3: Cowork fixes, products wired, who-is-who AI rule, handover (#5)
- `998ac4c32d` 2026-10-14 Merge pull request #4 from krishanraja/claude/gracious-curie-ugu6b5
- `9fda51d628` 2026-10-14 v3 AI: replies before Done, and one call on the home question
- `dc0a2613db` 2026-10-14 Merge pull request #3 from krishanraja/claude/gracious-curie-ugu6b5
- `183255c7c9` 2026-10-14 v3 AI: warm-up ping, backup retry, call log, instant own-words ink
- `0490df90d7` 2026-10-13 docs: Cowork prompt for everything left before the v3 launch
- `cf2be90efe` 2026-10-13 Merge pull request #2 from krishanraja/claude/gracious-curie-ugu6b5
- `4a2a2e7b03` 2026-10-13 v3: webhook settings as text, so Shopify accepts the chat section
- `c03e41f1b8` 2026-10-13 Merge pull request #1 from krishanraja/claude/gracious-curie-ugu6b5
- `52caa44b45` 2026-10-13 v3: Biscuit's gift chat with live Gemini AI through n8n
- `a68f2a1f4c` 2026-10-13 docs: v3 AI runs through Krish's n8n Gemini credential; #1001 refunded
- `eb17a1c3fb` 2026-10-13 docs: v3 spec restores live AI in version one, as agreed
- `804fa6ebe4` 2026-10-13 docs: v3 spec records Krish's 13 Oct decisions; v1 ships with no AI server
- `2db064c8a5` 2026-10-13 design: add the approved v3 phone prototype source
- `da42070905` 2026-10-13 README: point to the v3 spec and prototype
- `5f25e34e03` 2026-10-13 docs: v3 gifts from your dog spec, pointers in HANDOFF and SYNC
- `b1932edbd5` 2026-10-12 README: point to SYNC.md (repo canonical, Drive mirrors)
- `fb562423ad` 2026-10-12 assets: add profile avatar and Facebook cover, index them
- `b24ae156a8` 2026-10-12 design: add BRAND-SYSTEM and CANVA-SOURCES (mirrored in Drive)
- `c3075e88ab` 2026-10-12 docs: sync with Drive, add SYNC.md, mark V2 positioning superseded
- `a88bcf502c` 2026-10-12 README: point new sessions to docs/POSITIONING.md first
- `35f00706ba` 2026-10-12 docs: add 12 Oct positioning and $10k social plan (Krish's decisions)

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
