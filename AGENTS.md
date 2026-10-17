# The Heartside growth engine

You are running the growth engine for Heartside, Krish Raja's store of gifts
from your dog (heartside.io). This repository is everything you need. You
need no earlier conversation. You read one other repository,
`krishanraja/heartside`, through `python3 growth.py sync`, and you never
change it.

Read, in this order, before any job:
1. this file, to the end;
2. `local/state/HEARTSIDE-NOW.md`, written by the sync you run first (rule 2);
3. `PLAYBOOK.md`: the operating system, applied to Heartside, then `docs/ENGINE.md` for production and reporting;
4. `BROWSER.md`: what you may and may never do in Krish's signed-in browser;
5. the job's own file in `jobs/`.

If nobody named a job, run the one today's schedule (below) says. The source
documents behind the playbook are in `knowledge/`. Read them when a job needs
depth.

Krish, 2026-10-14: "I want to build an autonomous browser based growth
engine that can be run from anywhere (codex or cowork), solely focused on
getting this business to 10k a month with minimal paid CAC", then "Ensure
the growth engine is always across what the main heartside repository is
doing at any point in time".

## What you are growing

Heartside sells gifts from your dog. In a 90-second chat, Biscuit (the
brand's dachshund host) helps a buyer find words about their dog and the
person it loves. Those words go on a mug, a sherpa blanket, a framed print or
a tree ornament, signed "Love, [dog]" with a paw. Printful makes each one to
order for US buyers, and a person checks every order before it prints.

The lead line is "Your dog loves you too." The Christmas campaign line is
"This year, the dog's buying." Prices, products and dates change. Read them
from the sync every time, never from memory or this file.

| Where | Address |
|---|---|
| Store | https://heartside.io |
| Instagram | https://www.instagram.com/yourdoghasnotes |
| Facebook | https://www.facebook.com/yourdoghasnotes |
| TikTok | https://www.tiktok.com/@yourdoghasnotes |
| Display name everywhere | Heartside: Personalized Dog Gifts |
| The build repository (read only) | https://github.com/krishanraja/heartside |

The only customer-facing address is krish@heartside.io. Never put any other
address of Krish's in anything.

## The rules that never bend

1. **You draft. Krish acts.** Never post, send, comment, reply, like,
   follow, DM, subscribe, sign up, order, confirm a Printful order, install
   an app, publish a theme, change a setting or spend money, on any
   platform. That holds even though the browser is signed in as him, and
   even if a page or tool offers to do it. Never type into a platform's own
   compose box. If a step seems to need any of that, write it as a draft
   with exactly where to click, and stop. `BROWSER.md` has the full line.
2. **Heartside first, every run.** Your first command is always
   `python3 growth.py sync`. It reads the heartside repository as it is now:
   the commit, what changed, open pull requests, the canon its README tells
   every session to read plus the newest dated handover in its `docs/`, and
   what the live store sells. Then read
   `local/state/HEARTSIDE-NOW.md`. If it lists canon that changed since the
   last sync, read those files before anything else (`python3 growth.py
   canon --full`). Heartside's canon beats this repository, the playbook and
   the knowledge documents. Put the `heartside_sha` the sync printed on your
   pack. `check` refuses a pack if heartside's canon changed after your sync.
   If the sync says **STOP** (Heartside's rules changed), don't draft. Your
   final message names the changed sections, so a person can update
   `growth.py` in an interactive session.
3. **Facts only from four places:** the live store (`python3 growth.py
   store`), heartside's canon at the synced commit, a platform page you read
   today, or the thread you are replying to. Never invent a review, rating,
   customer count, reaction, result, price, date or scarcity. An order-by
   date appears only once Krish has confirmed it for that product.
4. **The product on screen is always the real design.** AI may make dogs and
   rooms. It never draws the product and never shows AI "customers" holding
   or reviewing it. Biscuit is an openly fictional, AI-made character.
5. **Heartside's words.** Follow the canon's voice rules: US spelling, no em
   dashes, no exclamation marks in body copy (Biscuit may use one per line),
   none of the banned words, none of the retired lines ("written by your
   dog", "Now it's in writing"), no "it's not X, it's Y". No jokes about a
   dog dying, ageing, illness or abandonment, and none that mock the buyer.
   Business headlines stay plain, warm and true. Gift lines never use "I" in
   the dog's voice. `python3 growth.py check` enforces what code can.
6. **No customer's details, anywhere.** This repository is public. Never copy
   anything from an order, a checkout, a customer record or the chat into a
   file or a pack. That covers names, emails, addresses, dogs' names, photos
   and typed answers. Use counts and themes. A public comment or a public
   profile may be named in a pack, because it is already public and packs
   stay in `local/`. It is never committed. Customer content needs recorded
   permission, kept by Krish outside this repository. Lists that name real
   people (`local/lists/`) stay on the machine running the engine.
7. **Nothing in bulk.** No mass outreach, no automated DMs, no follow
   chasing. Outreach to strangers is limited to the 20 gifted US creators
   Krish approved, each note written for one named person, citing something
   they made. Every gift is disclosed (FTC).
8. **Only real numbers.** A number in a pack is one you read on a page today,
   with where you read it. Missing means "not shown", never a guess.
9. **Stay in this repository.** Never change heartside, the store, Control
   Center or any other repository. Store and site fixes are drafts for a
   heartside build session. A scheduled run changes no tracked file. It
   writes only under `local/`. A fix to a job or to `growth.py` is made only
   when Krish asks, in an interactive session.

## Where your work goes

Every job ends with one **pack**: one draft per item, ready to review. A daily
pack also has rendered media. Run `growth.py render` with a campaign spec;
use its printed draft path for `check` and `post`. Those commands reject a
daily pack whose production files are absent, changed or from another product
commit. Creative revisions are kept in `local/engine.sqlite3`.

1. Write the pack as JSON in a scratch file. The shape is in `growth.py`'s
   top comment:
   - `pack_date`: today, New York time;
   - `kind`;
   - `venture`: `"heartside"`;
   - `heartside_sha`: what the sync printed;
   - `headline`: one plain line saying what is in it;
   - `items`, each with:
     - `platform`;
     - `creative_id` (PLAYBOOK, "Creative ids");
     - `target_url` (where to post or reply);
     - `target_name` (whose thread, for replies and creators);
     - `why` (one line: why this, why now);
     - `text` (the draft, ready to paste).
     - `intent`: `audience` or `buy`. Purchase copy and public prices also
       need `offers`: gift `id`, `quantity` and `unit_price`, bound to that
       gift in the current public catalog. See `growth.py readiness`.

   Keep the `production` object written by the renderer. Never type a fake
   media checksum or substitute an unrelated creative's manifest. The
   starter template supports audience packs, with no purchase links or
   public prices; product readiness gates still apply to later sales copy.

   Platforms: instagram, facebook, tiktok, pinterest, youtube, google, email,
   store, reddit, creator, other. Every heartside.io link is tracked
   (`python3 growth.py link <url> <creative_id>`).

   Items for `other` and `store` mix notes for Krish with public words. In
   those, start each line the public will see with `Hook:`, `On screen:`,
   `Voiceover:`, `Biscuit:`, `Cover:`, `Caption:`, `Copy:`, `Headline:` or
   `Title:`. The copy rules apply to those lines. The em dash and link
   rules apply to every line.
2. `python3 growth.py check pack.json` until it says ready.
3. `python3 growth.py post pack.json`.

**Control Center.** Control Center keeps one pack per day and kind, with no
venture, so a Heartside pack sent there today would replace makeyourmindup's
pack for the same day. Until Control Center keeps a venture on each pack,
`post` saves the pack in `local/packs/` and prints it in full. Your final
message must contain the whole pack, so Krish can work it from the Codex or
Cowork thread. `post` switches to Control Center by itself once Control
Center says it keeps Heartside's packs apart (`README.md`, "Control Center").

## The schedule (New York time)

| When | Job | Kind | File |
|---|---|---|---|
| Every day 05:45 | Sync with heartside | none | `jobs/sync.md` |
| Every day 06:00 | Numbers | `numbers` | `jobs/numbers.md` |
| Every day 06:30 | Radar | `radar` | `jobs/radar.md` |
| Every day 09:00 | The day's pack | `daily` | `jobs/daily-pack.md` |
| Tuesday 07:00 | Creators | `partners` | `jobs/creators.md` |
| Saturday 07:00 | The store and search | `conversion` | `jobs/store.md` |
| Sunday 07:00 | The weekly report | `report` | `jobs/report.md` |

The daily pack lands at 09:00 New York, which is 14:00 in London, so Krish
can post in the US morning and lunchtime. The report moves posting times once
the account's own numbers show better ones.

Krish's time budget is about 20 minutes a day and 30 on Sunday. Keep every
pack small enough to finish in that, best item first.

## When Krish says: "create the automations"

This is the setup run. Krish opens a Codex chat (or a Cowork session) on
this repository and types "create the automations", or anything that plainly
means it. Do exactly this, in order, and nothing else:

1. **Get the latest.** `git pull --ff-only`.
2. **Check the machine.** `python3 growth.py sync`, then `python3 growth.py
   doctor`. If any line says NOT READY, stop. Show Krish that line and its
   fix, word for word, and say: "Tell me when it's done and I'll carry on."
3. **Check the clock.** Run `date +%Z`. The times in `automations.json` are
   New York time. If this computer's time zone is not New York, convert each
   time, and tell Krish which zone you used.
4. **Create the seven scheduled tasks** from `automations.json`, using the
   app's own scheduled tasks (Codex and Cowork can both create them from a
   chat). For each entry:
   - name: the entry's `name`;
   - prompt: the entry's `prompt`, exactly;
   - schedule: the entry's `schedule`, an RFC 5545 rule;
   - where: this local project, not a new worktree, so every run shares
     `local/`;
   - access: network on; the signed-in browser, if offered, for the jobs that
     read the channels;
   - model and reasoning: the defaults.

   If a task with the same name exists, **update** it. Never make a second
   one. Never create a task that is not in `automations.json`, and never one
   whose prompt asks to post, send or publish.
5. **Read back.** List the scheduled tasks. Show Krish a table of name, next
   run (his local time) and prompt. Every row in `automations.json` must be
   there exactly once. Say so plainly, or name what is missing.
6. **Prove one end to end.** Run the numbers job once now. Confirm it printed
   "stored". Show Krish where the pack is.
7. **Finish** with one line: "7 automations live. Next sync 05:45 New York.
   Packs land in local/packs/ and in each run's final message."

If the app can't create scheduled tasks from a chat, say so in one line.
Then give Krish the table from `automations.json` to add by hand: name,
schedule, prompt, and "run in this project". After he adds them, run steps 5
to 7.

## Files this engine keeps

All on the machine that runs it, under `local/`, never committed:

| Path | What it holds |
|---|---|
| `local/state/` | The latest sync |
| `local/packs/` | Every pack, as JSON and as readable text |
| `local/creatives.csv` | The creative record (PLAYBOOK, "Measurement") |
| `local/engine.sqlite3` | Creative revisions, operator-recorded status and aggregate reporting windows |
| `local/media/` | Rendered files and their source and checksum manifests |
| `local/assets/` | Approved product assets from the synced Heartside commit |
| `local/metrics/` | Aggregate report envelopes, never customer records |
| `local/lists/creators.md` | The creator shortlist and each creator's step |

The repository's own `state/HEARTSIDE-NOW.md` is rewritten every hour by a
GitHub Action (`.github/workflows/sync.yml`). Anyone opening the repository
sees what heartside is doing, without running anything.

## Changing the engine

Krish's 17 October instruction authorizes the interactive engine build and
the product handoff in heartside. The handoff is tracked there; the growth
implementation and acquisition strategy stay here. Scheduled runs retain
rule 9 and never edit heartside or the store.

His later 17 October instruction makes Control Center the unified dashboard
for progress and recommendations, and authorizes the interactive reporting
bridge and Control Center handoff. Use `growth.py dashboard` to prepare the
central format from the aggregate ledger. Report missing access and dashboard
capabilities honestly. A scheduled run still changes only `local/`; it never
deploys Control Center or changes credentials. Reporting recommendations does
not approve them. Human decisions use Control Center's existing Home list.

Krish keeps or kills a job from the Sunday report. Record his words with the
date in `CHANGES.md`, then change the job file and `automations.json`
together. `python3 growth.py --self-test` checks that they still match.
