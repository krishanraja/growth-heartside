# growth-heartside

The growth engine for [Heartside](https://heartside.io), gifts from your dog.
It produces media and drafts that bring US buyers to the store with as little paid spend as
possible: the day's Reel and its native editions, replies to comments,
creator notes, store and search fixes, the numbers and a weekly decision. It
runs as scheduled Codex or Cowork sessions. Krish reads each pack, posts and
sends by hand, and keeps or kills jobs from the Sunday report.

**Goal:** $10,000 of net sales a month, starting with the Christmas window
(about $10,000 by the 10 December order-by date). Then the category,
worldwide. See `PLAYBOOK.md`.

Nothing here posts, sends, comments, orders, confirms a Printful order,
installs an app or spends. Nothing here changes the heartside repository or
the store.

- How it works and the rules: `AGENTS.md` (every run reads it first).
- The operating system, adapted to Heartside: `PLAYBOOK.md`.
- Krish's source documents, and where Heartside changes them: `knowledge/`.
- The jobs: `jobs/`. The entrypoint: `growth.py` (standard-library core;
  Pillow and FFmpeg for media).
- What heartside is doing right now: `state/HEARTSIDE-NOW.md`.
- Krish's changes: `CHANGES.md`.
- The build, commands, aggregate reporting format and current limits: [`docs/ENGINE.md`](docs/ENGINE.md).
- Acquisition strategy and the 30-day experiment: [`STRATEGY.md`](STRATEGY.md).
- Product, purchase-flow and fulfillment work now belongs in [heartside's product handover](https://github.com/krishanraja/heartside/blob/codex/product-handoff-2026-10-17/docs/HANDOVER-2026-10-17.md) ([PR #13](https://github.com/krishanraja/heartside/pull/13)).

## Produce the first media pack

```sh
python3 -m pip install -r requirements-media.txt
# Install FFmpeg using your operating system's package manager.
python3 growth.py sync
python3 growth.py readiness
python3 growth.py render campaigns/waits-at-the-door.json
```

The render command prints the exact draft pack path. `growth.py check <path>`
verifies its copy, product commit and media checksums. `growth.py post <path>`
stores it for review; it does not publish to any social platform. The starter
produces a ten-second 1080x1920 example film, cover, three Story frames, two
Pins and subtitles from the approved real mug images. It has silent audio.
No paid AI generation runs. Use `--heartside-dir /path/to/heartside` to read
the pinned assets from a local checkout instead of downloading them.

The local SQLite ledger keeps creative revisions and aggregate reports across
runs. A machine move needs a consistent backup (`growth.py ledger backup
local/backups/engine.sqlite3`) or a future shared-state adapter. It is not
automatically replicated to n8n or Control Center.

## How it stays across heartside

The heartside repository (`krishanraja/heartside`) is the source of truth for
the product, the prices, the words and the launch. This engine never keeps
its own copy of any of that.

| When | What happens |
|---|---|
| Every run, first | `python3 growth.py sync` reads heartside's main branch: the commit, the commits since the last sync, open pull requests, the canon its README names, and the live store's products and prices. It writes `local/state/HEARTSIDE-NOW.md`, and the job reads any canon that changed before drafting. |
| Every pack | `check` refuses a pack whose `heartside_sha` is older than a canon change on heartside, or written while Heartside's rules differ from what the checker was written for. Prices in a draft must be prices in the live store or heartside's gift table. |
| Every hour | A GitHub Action (`.github/workflows/sync.yml`) rewrites `state/HEARTSIDE-NOW.md` here when heartside, its open pull requests or the store changed. If Heartside's rules changed, it commits a STOP notice and fails the run, so GitHub emails the owner. |

**The contract with heartside:** the canon is whatever the "Picking this
up?" line of heartside's `README.md` links, in its order. Then comes the
newest dated handover in heartside's `docs/` (a file named like
`COWORK-HANDOVER-2026-10-15.md`), because sessions write those before the
README catches up. Then `README.md`, `design/BRAND-SYSTEM.md` and
`shopify/README.md`. Change that line, or write a newer handover, and this
engine follows it on its next sync.

## Setting it up (Krish, once)

1. **Connect this repository** in Codex (cloud or the desktop app) or Cowork,
   with network access on. Runs need to reach github.com,
   raw.githubusercontent.com, heartside.io and the channels. Use the desktop
   app and "run in this project" so every run shares `local/`.
2. **Optional, for the dashboards:** a browser signed in to Shopify admin,
   Meta Business Suite, TikTok and later Pinterest and Google Merchant
   Center. The engine only reads (`BROWSER.md`).
3. **Create the schedule.** Open a chat on this repository and type "create
   the automations". It checks the machine, creates the seven tasks below and
   runs one to prove it. To add them by hand instead, use these (New York
   time):

   | Name | When | Prompt |
   |---|---|---|
   | Heartside growth: sync | daily 05:45 | `Run jobs/sync.md as AGENTS.md says.` |
   | Heartside growth: numbers | daily 06:00 | `Run jobs/numbers.md as AGENTS.md says.` |
   | Heartside growth: radar | daily 06:30 | `Run jobs/radar.md as AGENTS.md says.` |
   | Heartside growth: day pack | daily 09:00 | `Run jobs/daily-pack.md as AGENTS.md says.` |
   | Heartside growth: creators | Tue 07:00 | `Run jobs/creators.md as AGENTS.md says.` |
   | Heartside growth: store and search | Sat 07:00 | `Run jobs/store.md as AGENTS.md says.` |
   | Heartside growth: report | Sun 07:00 | `Run jobs/report.md as AGENTS.md says.` |

To run one job by hand from anywhere, open a chat on this repository and
type, for example, "Run jobs/daily-pack.md as AGENTS.md says."

Check the machine at any time with `python3 growth.py doctor`.

## Control Center

Control Center is the unified dashboard for progress and recommendations.
The live table still lacks venture isolation, so Heartside packs currently
stay under `local/packs/`. The compatible change is prepared in Control
Center's `codex/heartside-growth-reporting` branch; its migration and app
must be deployed together. The existing GitHub Actions secret is available
and authenticated to the live reporting API with HTTP 200 on 17 October.
The interactive shell does not receive Actions secrets automatically.

`.github/workflows/reporting-access.yml` uses that secret inside GitHub and
records only a read-only capability result. The verified run is
[39020889464](https://github.com/krishanraja/growth-heartside/actions/runs/39020889464).
It confirmed authentication and correctly detected the live API's missing
venture support. `python3 growth.py reporting-access` runs the same check
where the credential is bound. Never export the secret to logs or artifacts.

`growth.py dashboard --start <date> --end <exclusive-date> --timezone <store-zone>`
prepares numbers and progress packs with sources, coverage and prepared links.
Check and post each printed draft. `post` checks for Heartside in the API's
`ventures` capability, scopes every write to Heartside, and keeps a local
retry copy and media provenance. `read` uses Heartside's central report when
available and merges dashboard marks with local evidence. Existing publication
callers remain isolated. See `docs/ENGINE.md` for commands and current limits.

Control Center's media review, private downloads, shared runner state and
Home-list routing of prepared decisions still need work. The detailed UI and
access handoff lives in that repository at
`docs/handoff/heartside-growth/README.md`. No second dashboard is built here.

## Layout

```
AGENTS.md         the brief every run reads first
PLAYBOOK.md       the operating system, applied to Heartside
BROWSER.md        read-only rules for the signed-in browser
jobs/             one file per job; automations.json schedules them
growth.py         sync, canon, store, link, check, post, read, doctor, self-test
engine/           offer checks, pinned asset cache, media renderer and local ledger
campaigns/        editable production templates; scheduled copies go under local/
docs/ENGINE.md    runtime commands, report format and implementation limits
STRATEGY.md       acquisition experiment and revenue scenarios
knowledge/        Krish's two source documents, and where Heartside changes them
state/            the hourly reading of heartside (written by the Action)
local/            on the running machine only, never committed: sync, packs, lists
```
