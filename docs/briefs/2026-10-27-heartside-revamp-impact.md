# Heartside's 27 October revamp: what changed and what it means for this engine

Read on 27 Oct 2026, 18:08 UTC. Sources:
- `python3 growth.py sync` at heartside `bea22ce182`;
- heartside's `README.md`, `docs/SCOPE.md`, `docs/ECONOMICS.md`, `docs/NORTH_STAR.md`, `docs/SYNC.md` and `NOW.md` at that commit;
- the Drive `00_Brand-Assets` folder;
- `Heartside-Brand-Book.pdf` (22 pages, compiled 27 Oct);
- `01_Identity/CANVA-BRAND-KIT-GUIDE.md`;
- live reads of heartside.io;
- Canva's brand-kit list.

Heartside's canon beats this repository (AGENTS.md, rule 2). Where anything below disagrees with heartside's current sources, those sources win.

## What changed

| Area | Before (what this engine assumes) | Now |
|---|---|---|
| Storefront | Password page, "Opening soon" | **Live.** The password was removed and the reviewed theme published on 27 Oct; the homepage and product pages return 200 |
| Range | Mug $29, sherpa blanket $89, framed print $89, ornament $24 ($19 with another gift) | **Three core gifts:** Your Dog's Illustrated Mug $45 (11 oz, five interior colors); Your Dog's Personality Blanket $129 (50 × 60, word-free); Your Dog's Portrait $59 unframed, $119 framed (black, white, red oak). The ornament is on hold, the pillow is a conditional pilot, and a book is planned for 2027 |
| Host | Biscuit | **Buddy**, a chestnut dachshund. He is never the customer's dog. Biscuit is retired |
| Canon files | `docs/V3-GIFTS-FROM-YOUR-DOG.md`, `docs/POSITIONING.md`, `docs/HANDOFF.md`, `design/BRAND-SYSTEM.md` | Moved to heartside's `docs/history/`. The current order is NORTH_STAR, NOW, SCOPE, ECONOMICS, SYNC; visual tokens live in `shopify/assets/hs3.css`; the Canva handoff is `design/CANVA-SOURCES.md` |
| Economics | none in this engine | **Maximize total net operating profit, with at least a 30% net margin after all attributable costs** (ruling of 26 Oct). Price and discount changes are gated. Do not add paid acquisition, percentage discounts or bundles without recalculating. A mug-heavy mix misses the floor; blanket and balanced mixes clear it |
| Brand | the old brand system | The **Brand Book** (Drive). Voice: plain US English, warm and direct, funny first then tender. Eight rules: no exclamation marks, no em dashes, plain words, no invented proof, **label every example**, **real mockups only**, **name the dog (never Buddy)**, one thing at a time. The palette adds body `#3E322D`, line `#E2D4C8`, pencil `#B9ADA4`, gold `#C9A048`, blanket-tan `#E3D3BF` and five mug interior colors. Fonts: Fraunces (headlines, signature), DM Sans (everything read and pressed), Courier Prime (words that print) |
| Assets | 15 Oct mug photos and a Biscuit headshot in heartside's repo | 16 current Printful renders, grouped by mug, blanket and portrait under `02_Imagery/Current-Shopify-Product-Mockups`. The example dog is a pug named Milo, and every image carries an Example label. `90-Source-Records-Not-for-Social` is not for posts |
| Canva | no Heartside brand kit | A brand kit named **Heartside** exists (`kAHZOWQoPQU`) but has **not** been updated yet. The Brand Book says no approved Buddy avatar and no finished social templates exist: **do not improvise them** |
| Heartside's North Star | n/a | $50,000 Shopify net sales over a trailing 4 weeks by 22 Feb 2027. Last measured: $0 (one $24 order, fully refunded, 24 Oct) |
| Proof | none | One fee-free blanket compatibility order passed through Teeinblue. Krish will place a real sample blanket order. Physical quality and paid fulfilment are not yet proven |

## What this means for the engine, right now

1. **The engine is on STOP, correctly.** The four rule sections it checks were moved into heartside's history, so `growth.py sync` refuses every pack. The rules basis has to be rebuilt on the current canon in an interactive session:
   - SCOPE's non-negotiables 5 and 10;
   - the Brand Book's voice rules, which live in Drive, not the repo;
   - `CANVA-SOURCES.md`.

   **One question for Krish:** the 20 Oct gift-line rule ("I is the dog, you is the person, signed Love, [dog]") now lives only in heartside's history. Does it still hold?
2. **The renderer would make retired creative,** so nothing it renders should go out. Specifically:
   - `engine/assets.py` pulls the 15 Oct mug photos and the Biscuit headshot;
   - `engine/media.py` has a `biscuit-desk` layout and an "EXAMPLE · Biscuit is an AI character" line;
   - `engine/offers.py` builds purchase copy around Biscuit and the old mug;
   - the 7 campaigns C90 to C96 use Biscuit scenes.

   The fix is to switch to the 16 current renders with an Example label, and to Buddy in canon form. PR #21 (Buddy rename) is now relevant and needs rebasing.
3. **The code checks old prices and products.** `offers.py` binds purchase copy to the "Morning Mug". `docs/GEO-AEO.md` lists entity facts at $29, $89, $89 and $24. The live Answers articles already show the new prices. One still uses "Love, Biscuit" as its example dog name; Milo matches the Brand Book.
4. **Codes and gifting fall under the economics rule.** The plan's creator gift codes, audience codes and post-family codes are discounts. Each must be modeled under heartside's ECONOMICS procedure, treated as acquisition cost against the 30% net floor, before Krish switches it on. The plan's "$19 ornament add-on" idea is void, because the ornament is on hold.
5. **The creative lean is product-led and blanket-forward.** The blanket ($129) carries the best modeled margin, and mug-heavy mixes miss the floor. Posts show the current mug, blanket and portrait exactly as they arrive, each image labelled as an example.
6. **The Canva design-system prompt needs a v4 before anyone runs it:**
   - update the **existing** Heartside kit rather than creating one;
   - use `01_Identity` and the three current-product folders only;
   - use the Brand Book palette and type scale;
   - make no Buddy avatar and no improvised template;
   - build any masters only as drafts for Krish's approval.
7. **Never-publish items already in this public repo.** Heartside now lists the Shopify store handle and the Drive folder link as never-publish. The store handle sits in `docs/ENGINE.md`, `engine/ledger.py`, `engine/insights.py` and `tests/test_ledger.py`, from before 27 Oct. Moving it into a secret or config is a phase 0 fix.
8. **Customer-facing email conflict.** The Brand Book's back page gives hello@krishraja.com. AGENTS.md and `growth.py` allow only krish@heartside.io. Krish to rule.
9. **The ladder reconciliation becomes concrete.** Heartside's whole-store target is $9,312 by 28 Dec; this repo's organic-only target is $25,000 for the same date (K03 in the architecture brief).

## Plan changes this triggers (architecture brief v3)

- **Gate 0, item 1 (unlock the store): done.** What remains is the real sample order.
- **Phase 0 gains:**
  - rebuilding the rules basis on the new canon;
  - the renderer and campaigns moving off Biscuit and onto the current renders;
  - PR #21 rebased;
  - prices and products updated in code and in `GEO-AEO.md`;
  - the store handle moved out of the repo.
- **G1 gains:** each code and gift line modeled under the 30% floor.
- **Appendix A** (the Cowork Canva prompt) is replaced by a v4 that follows the Brand Book and CANVA-BRAND-KIT-GUIDE.
