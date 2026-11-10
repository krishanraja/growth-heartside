# North Star

Status: Current
Owner: Krish Raja
Last verified: 2026-11-10

> By 31 December 2026, organic posts sell more Heartside gifts than paid ads ever have, and every winning format was found by this engine and approved by Krish in one press.

Set by Krish on 18 October 2026. It is not reached yet. It is what every session in this repository works toward.

This repository serves [Heartside's North Star](https://github.com/krishanraja/heartside/blob/main/docs/NORTH_STAR.md). The lines above are this repository's part of it.

## The number

**Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them**: $50,000 by 28 December 2026, on a front-loaded weekly ladder. Checkpoints: 16 Nov 2026: $4,862; 14 Dec 2026: $25,436; 28 Dec 2026: $50,000.

Raised from $25,000 by Krish on 10 Nov 2026, on his review board (`decision-north-star-50k`, Yes), to match the Sprint 120 plan's $50,000 by Christmas (`docs/plans/2026-11-10-sprint-120.md`). The weeks already past keep their original targets.

```yaml north-star-metric
metric: "Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them"
unit: USD
direction: up
target: 50000
deadline: 2026-12-28
ladder_shape: front-loaded
source: "Shopify orders with organic attribution (UTM and discount codes from this engine)"
status: active
ladder:
  - [2026-10-26, 200]
  - [2026-11-02, 728]
  - [2026-11-09, 1417]
  - [2026-11-16, 4862]
  - [2026-11-23, 7782]
  - [2026-11-30, 11906]
  - [2026-12-07, 17626]
  - [2026-12-14, 25436]
  - [2026-12-21, 35966]
  - [2026-12-28, 50000]
```

Urgency (U1 to U5) is worked out every week from where the number stands against that week's target, by [the harness contract](https://github.com/krishanraja/ai-harness/blob/main/contract/north-star-metric.md). Set by Krish on 23 October 2026.

## How to use it

- Read it before any work, every session.
- Before you start, say which part of it the task moves. If the task moves nothing toward it, say so first and let Krish decide.
- Prefer the work that moves it furthest, and close each session by noting what moved.
- Only Krish changes this file. Record his ruling in the commit body as `Ruling (Krish, YYYY-MM-DD): ...`.
- When it is reached, say so and ask Krish for the next one.
