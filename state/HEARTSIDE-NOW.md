# Heartside now

Read from `krishanraja/heartside` at commit `218e20f4ba` on 2026-10-20T01:52:26+00:00 UTC by `python3 growth.py sync`.
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

## Recent commits on main

- `218e20f4ba` 2026-10-19 Merge pull request #30 from krishanraja/claude/adoring-cerf-ybph82
- `5cb47240d8` 2026-10-19 Mug page: chosen color's photos only, whole mug in the cart, Your Words says when the headshot is in
- `0ddd2289c5` 2026-10-19 Merge pull request #29 from krishanraja/claude/adoring-cerf-ybph82
- `da52861684` 2026-10-19 Mug colors live: variants, images and checks
- `a5a76c2515` 2026-10-19 Cowork prompt for the mug colors in Teeinblue
- `0a75c79140` 2026-10-19 Merge pull request #28 from krishanraja/claude/adoring-cerf-ybph82
- `c886af9084` 2026-10-19 Mug colors: recolored bases, per-color images, swatches in the chat and on the product page
- `90232f4739` 2026-10-19 Merge pull request #27 from krishanraja/claude/adoring-cerf-ybph82
- `6b205f3207` 2026-10-19 Mug colors: a first-look board of the five proposed colors on the approved render
- `b191fd3938` 2026-10-19 Order QC checks the mug color; plan for the mug in five colors
- `9a89140655` 2026-10-19 Merge pull request #26 from krishanraja/claude/adoring-cerf-ybph82
- `b2c28b95f9` 2026-10-19 Desktop: reveal and choose in two columns; phone top bar on two clean lines
- `a1b371ef4a` 2026-10-19 Merge pull request #25 from krishanraja/claude/adoring-cerf-ybph82
- `4fb50d33bd` 2026-10-19 Desktop: one page, not a window in a window
- `e66a67689a` 2026-10-19 Merge pull request #24 from krishanraja/cowork/2026-10-19-desktop-check
- `15153ce015` 2026-10-19 Cowork 19 Oct: desktop check on the live site, Order QC task paused
- `ca02b1f262` 2026-10-19 Merge pull request #23 from krishanraja/claude/adoring-cerf-ybph82
- `8abfa7df33` 2026-10-19 Desktop layout for the homepage chat; header padding capped
- `8c3c288640` 2026-10-19 Merge pull request #22 from krishanraja/claude/adoring-cerf-ybph82
- `56fc7c3ac1` 2026-10-19 Report: dry run 3 and real run 4 green; schedule on
- `5075902bb8` 2026-10-19 Order QC: switch the schedule on (07:56 and 16:56 London)
- `f75f7f08a8` 2026-10-19 Merge pull request #21 from krishanraja/claude/adoring-cerf-ybph82
- `ad8b5e6607` 2026-10-19 Report: second dry run green
- `399dd88840` 2026-10-19 Order QC: find mugs by line item title, not product (read_orders only)
- `34a56af502` 2026-10-19 Merge pull request #20 from krishanraja/claude/adoring-cerf-ybph82
- `306a626a15` 2026-10-19 Order QC signs in with the Dev Dashboard app's client credentials
- `c5a15bdf5f` 2026-10-19 Merge pull request #19 from krishanraja/cowork/2026-10-19-launch-checks
- `df9de3cde5` 2026-10-19 Cowork 19 Oct: Part A checks on what went live, order QC status
- `be54fe7098` 2026-10-19 Merge pull request #18 from krishanraja/claude/adoring-cerf-ybph82
- `00073c2573` 2026-10-19 Report: theme deploy run 50 and the mug image swap, with live checks

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
