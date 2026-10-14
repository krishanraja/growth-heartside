# growth-heartside

The growth engine for [Heartside](https://heartside.io), gifts from your dog.
It drafts what brings US buyers to the store with as little paid spend as
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
- The jobs: `jobs/`. The one tool: `growth.py` (Python standard library,
  plus git).
- What heartside is doing right now: `state/HEARTSIDE-NOW.md`.
- Krish's changes: `CHANGES.md`.

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
up?" line of heartside's `README.md` links, in its order, plus
`design/BRAND-SYSTEM.md` and `shopify/README.md`. Change that line in
heartside, and this engine follows it on its next sync.

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

Packs don't go to Control Center yet. Control Center's `growth_packs` table
keeps one pack per `(pack_date, kind)`, with no venture. So a Heartside
`daily` pack would replace makeyourmindup's `daily` pack for the same day.
Until that changes, `post` saves each pack in `local/packs/` and prints it
in full in the run's final message.

The change that lets Heartside in, for a Control Center session:
- add `venture text not null default 'makeyourmindup'` to `growth_packs`;
- make the unique key `(pack_date, venture, kind)`;
- accept `venture` on POST and filter on it on GET (`?venture=`);
- answer GET with `"ventures": ["makeyourmindup", "heartside"]`;
- show the venture on Growth > Packs.

`post` checks for that `ventures` list before every send, and switches to
Control Center by itself once it includes `heartside`. It uses the same
`GROWTH_ENGINE_TOKEN` as the makeyourmindup engine.

## Layout

```
AGENTS.md         the brief every run reads first
PLAYBOOK.md       the operating system, applied to Heartside
BROWSER.md        read-only rules for the signed-in browser
jobs/             one file per job; automations.json schedules them
growth.py         sync, canon, store, link, check, post, read, doctor, self-test
knowledge/        Krish's two source documents, and where Heartside changes them
state/            the hourly reading of heartside (written by the Action)
local/            on the running machine only, never committed: sync, packs, lists
```
