> **Live since 2026-10-19.** The first Control Center loop completed its directive, report readback and decision read on 19 October. The scheduled workflow still ran successfully on 23 October ([run 39904322191](https://github.com/krishanraja/growth-heartside/actions/runs/39904322191)). This is the original setup brief; use `docs/control-center/ENGINE-PROTOCOL.md` for the current protocol.

# Control Center brief: growth-heartside

Written 2026-10-18 by Control Center. This brief **supersedes `docs/CONTROL-CENTRE-BRIEF.md`** as the reporting contract. Krish ruled that every growth engine reports through one protocol (ADR-038 in Control Center). Packs stay for media and copy review, now kept apart per venture (PR 472, merged 2026-10-18), so `HEARTSIDE_ENABLE_CC_DELIVERY` and the `ventures` probe gate your media delivery only. Progress goes through the protocol.

## What Control Center now does for you

- **Pushes you one next action every day, chosen by rule.**
- **Puts every post and every spend that only Krish can approve on his one list on Home.** It returns his decision bound to the exact payload, which here means the `(creative_id, revision)` you hash into `payload_sha256`.
- **Shows your health, objectives, today's push and what you did** on Growth > Engines.

## Your registry row

| | |
|---|---|
| Slug in the path | `heartside` |
| `engine_id` | `growth-heartside` |
| `product_slug` | `heartside` |
| Aim | Organic posts sell more Heartside gifts than paid ads ever have, and every winning format was found by this engine and approved by Krish in one press. By 2026-12-31 |
| Objectives | `net_sales_usd`: target 10,000 USD per month (Europe/London, Shopify net sales); `organic_orders`: no target set yet |
| Cadence | daily |
| State | Live loop enabled. The first run completed on 2026-10-19; the scheduled 2026-10-23 run succeeded. Use the current protocol and repository workflow for operating details |

## The protocol, in short

The full spec is `docs/control-center/ENGINE-PROTOCOL.md`, with the report and directive schemas and a worked example beside it. In short:

**Base URL and auth.**
- Base: `CONTROL_CENTER_URL`, which is `https://controlcenter.krishraja.com`.
- Bearer: `Authorization: Bearer $CONTROL_CENTER_ENGINE_TOKEN`. This is a `gen1_` token issued for this engine alone. Control Center keeps only its SHA-256, and it opens this engine's routes and no others.
- Transport: HTTPS only. Follow no redirects, use bounded timeouts, and read back before retrying any write.

**Every run, in this order:**
1. `POST {base}/api/growth/engines/heartside/attempts` with `status: started`, before reading any source.
2. `GET {base}/api/growth/engines/heartside/directive` returns today's `next_action`, your objectives with their targets and latest values, his decisions of the last seven days, and the walls.
3. Do the work, inside the walls. The rule, word for word: "Nothing sends, posts, spends, deletes or changes a permission without a decision from Krish whose payload_sha256 matches what you are about to do."
4. `POST {base}/api/growth/engines/heartside/reports` with header `Idempotency-Key: {run_id}`. The body is the report envelope:
   - `schema_version: "1.0.0"`, `engine_id`, `product_slug`, `run_id`, `mode`, `observed_at`, `source`, `status`
   - `objectives[]`, `activity[]`, `proposals[]`, `events[]`, `holds[]`
   - `payload_sha256`: the SHA-256 of the canonical JSON without that field, with keys sorted at every depth and no whitespace

   An unknown field is refused, never dropped. Then `GET .../reports/{run_id}` and compare the digest.
5. `POST .../attempts` again with the terminal state (`succeeded`, `failed` with a lower_snake `error_code`, or `unknown`) and `finished_at`. A terminal record never changes.
6. `GET {base}/api/growth/engines/heartside/decisions?since={last run}` returns his yes and no, each with the `payload_sha256` it was made on. Act on a yes only when that digest equals the payload you are about to use. A changed payload is a new ask, and it goes back to him by itself when you report it.

**How proposals and readings are judged.**
- A proposal behind a wall (`spend` with its `amount_usd`, `send` or `post` with its `exact_payload`, or `strategy`) goes on Krish's one list on Home, where Clear approves it, Purge declines it and Bump defers it a day.
- A proposal inside the walls is yours to do. Control Center may pick it as your next push.
- Unknown is `value: null` with a `reason`, never zero. A measured zero is `0`.
- `mode: synthetic` is stored and read back but never touches his numbers or his list. Use it to prove your client before Krish switches you on. A live report is refused (409 `engine_inactive`) until he does.

**The wake-up.** Control Center wakes you once a day around 06:10 London with `repository_dispatch` of type `cc-growth-directive`, whose `client_payload` is `{ directive_id, engine_id }` and nothing else. Add that trigger to your workflow. If you do not run on GitHub Actions, pull the directive at the start of your own run instead; it is the same directive.

## How your old brief maps

| Your contract | In the protocol |
|---|---|
| `numbers` pack rows (one platform per row, null means missing, 0 means measured) | `objectives[]`, with the same rule. Net sales go in `net_sales_usd`, with `window_start`, `window_end` and `timezone: Europe/London`. Do not add overlapping windows together |
| `recommendations.json` (`title`, `why`, `next_action`, `closes_when`) | A proposal: `title`, `why`, and `close_condition.event` for `closes_when`. Give each a stable `proposal_id`, the id the brief asked Control Center to show |
| `creative_status` approved and published | A post proposal: `wall: post`, `channel`, `exact_payload` (the caption), and `payload_sha256` over `creative_id`, `revision` and the caption. Krish's Clear is the approval. Report `events[]` `creative_published` with the permalink once he has posted |
| `operator_events` into your workflow | `GET decisions`. Nothing needs to call your workflow input any more |
| The product constraint (heartside PR 13) | A `holds[]` entry with the reason. Control Center shows it without turning it into a task |
| `production.manifest` | Stays local. Name the creative and revision in `activity[]` |

## What you build now

1. The client for the six calls, behind a flag that defaults off.
2. The `cc-growth-directive` trigger on the growth workflow.
3. Proposals for posts and paid boosts. A paid boost is `wall: spend` with `amount_usd`. Your default budget stays $0, so propose a spend only when you would recommend Krish to approve it.
4. A synthetic report, read back by digest.

## What you stop

- Using packs for progress. Packs are now kept apart per venture (PR 472, merged 2026-10-18), so `venture=heartside` works for media and copy review. Progress, proposals and holds go through this protocol.
- Expecting a Posted action on report cards.

## Acceptance

- A measured zero and a missing value show differently on Growth > Engines.
- A post proposal reaches Krish's list. Clear appears in `GET decisions` with your digest. A changed caption asks him again.
- A stale run (no report for 36 hours) shows as stale, never green.
