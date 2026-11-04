# Brief for a heartside build session: a black-and-tan dachshund render

Written 4 Nov 2026 by the growth engine. Krish approved this on 4 Nov ("Yes to all your 4 questions", answering "Can heartside make a black-and-tan dachshund render for F06-dachshund?"). The growth engine never changes heartside (AGENTS.md rule 9), so this is a brief for Krish to paste into a heartside build session.

## The problem

- The locked roast F06-dachshund ("What your dachshund really thinks of you") stars a **black-and-tan** dachshund.
- It ends on `mug-real-dachshund.jpg`, the store's only dachshund mug render, which shows a **chestnut** dachshund in a green sweater.
- The viewer meets one dog and is sold a gift showing another. That breaks the post's payoff, so the post is held from paid use (`docs/audits/2026-11-04-creative-audit.md`).

## What is needed from heartside

1. **A black-and-tan dachshund mug render**, made the same way as the store's existing breed examples:
   - from heartside's own example brief, the painting generated in the house style;
   - composited unchanged onto the real mug product image;
   - with no badge or label (AGENTS.md rule 4).
   - Ideally the dog also matches the roast's dog: black and tan, smooth coat, smug grin.
2. **The same dog as a portrait render** as well, if that is cheap. The roast template can end on either product.
3. **Delivery to the growth engine:**
   - commit the renders to heartside with their sha256;
   - add them to the store's examples if Krish wants them shown there.
   - The growth engine then adds each render to `factory/bank/renders.json` with a new `coat: black-and-tan` tag, and rebuilds F06-dachshund's ending from it. The roast's lines and frames are unchanged, so its lock skeleton holds.

## Done means

- The render file exists in heartside at a known commit.
- `factory/bank/renders.json` lists it with its checksum and coat.
- The rebuilt F06-dachshund passes `factory/lock.py gate` and `factory/audit.py`.
- Its ending shows a black-and-tan dachshund on the real mug.
