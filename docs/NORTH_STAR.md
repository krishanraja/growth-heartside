# North Star

Status: Current
Owner: Krish Raja
Last verified: 2026-10-18

> By 31 December 2026, organic posts sell more Heartside gifts than paid ads ever have, and every winning format was found by this engine and approved by Krish in one press.

Set by Krish on 18 October 2026. It is not reached yet. It is what every session in this repository works toward.

This repository serves [Heartside's North Star](https://github.com/krishanraja/heartside/blob/main/docs/NORTH_STAR.md). The lines above are this repository's part of it.

## The number

**Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them**: $25,000 by 28 December 2026, on a front-loaded weekly ladder. Checkpoints: 16 Nov 2026: $2,431; 14 Dec 2026: $12,718; 28 Dec 2026: $25,000.

```yaml north-star-metric
metric: "Heartside net sales attributed to organic posts, trailing 4 weeks, with $0 of paid ads behind them"
unit: USD
direction: up
target: 25000
deadline: 2026-12-28
ladder_shape: front-loaded
source: "Shopify orders with organic attribution (UTM and discount codes from this engine)"
status: active
ladder:
  - [2026-10-26, 200]
  - [2026-11-02, 728]
  - [2026-11-09, 1417]
  - [2026-11-16, 2431]
  - [2026-11-23, 3891]
  - [2026-11-30, 5953]
  - [2026-12-07, 8813]
  - [2026-12-14, 12718]
  - [2026-12-21, 17983]
  - [2026-12-28, 25000]
```

Urgency (U1 to U5) is worked out every week from where the number stands against that week's target, by [the harness contract](https://github.com/krishanraja/ai-harness/blob/main/contract/north-star-metric.md). Set by Krish on 23 October 2026.

## How to use it

- Read it before any work, every session.
- Before you start, say which part of it the task moves. If the task moves nothing toward it, say so first and let Krish decide.
- Prefer the work that moves it furthest, and close each session by noting what moved.
- Only Krish changes this file. Record his ruling in the commit body as `Ruling (Krish, YYYY-MM-DD): ...`.
- When it is reached, say so and ask Krish for the next one.
