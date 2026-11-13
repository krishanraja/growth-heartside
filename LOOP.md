# The Order Loop

The plan Krish approved as the build on 13 Nov 2026: find out which factor of the number is zero (the till,
US reach, the click, a stranger's purchase), then run one daily loop that reads, ranks and asks. Only the
**buy lane** carries the North Star number: posts that end on the real product and carry a counted path,
led by the blanket, the portrait and bundles. The viral lane builds audience and is never ranked for money.

## What is built

- `factory/loop.py`, the decision core. Rules are constants there, and only Krish's ruling changes them:
  - like with like (platform and lane, trailing 14 days, baseline below 5 measured);
  - a buy-lane signal per platform from the fields Buffer shows (Instagram follows, shares and saves per
    1,000 reach; TikTok shares per 1,000 views; Facebook clicks per 1,000 reach), never zero when not shown;
  - candidate at 24 hours (buy 2x, viral 3x on 72-hour views), winner after two matched variants at 1.5x,
    kill after three below 0.5x;
  - orders gate and never rank; an `unverified` order (engine/attribution.py) never graduates a concept;
  - the reader is never the maker, a Krish approval comes only from the board's verdicts, and a prediction
    counts only when saved before the post.
  It writes nothing, so a scheduled session may call it (AGENTS.md rule 9). Tests: `tests/test_loop.py`.
- `engine/attribution.py`: the `unverified` Meta tier and the month window that measures `net_sales_usd`.
- `growth.py` claims gate: no words on a gift, no handmade, no uninspected quality, no delivery promise, no
  deal wording without a live offer.

## What is not built yet

- The readers that feed it: Buffer per-post readings inside `engine.yml` wait on Krish's ruling 5 (a
  read-only Buffer key in the runner's secrets); the weekly browser read stays in a session he starts.
- The private ledger page and the placement registry over the 02 Sheets.
- The batch Sheet builder (one board item per batch) and the freeze of the day pack, radar, creators and
  store jobs, which wait on the L1 ruling.

Every widening of authority is its own Yes or No on the board. Nothing here posts, sends or spends.
