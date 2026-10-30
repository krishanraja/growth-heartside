# Running the Heartside growth engine

Implementation lives here. Product, purchase and print work is already handed
to [heartside PR #13](https://github.com/krishanraja/heartside/pull/13).
Progress reaches Control Center through the growth engine protocol
([brief](CONTROL-CENTER-BRIEF.md), [loop](#control-center-protocol-loop)); packs stay
for media and copy review.
No social publisher, customer-record reader or paid-generation scheduler exists.

## Channel tasks and the weekly loop

Which specialist runs which of the seven channel tasks, and the loop from this week's gap to the North Star: docs/CHANNEL-TASKS.md.

## Production

```sh
python3 -m pip install -r requirements-media.txt
# Install FFmpeg and ffprobe through the system package manager.
python3 growth.py sync
python3 growth.py readiness
python3 growth.py render campaigns/waits-at-the-door.json
```

Use the printed draft path with `growth.py check` and `growth.py post`. `post`
means internal pack storage. Central delivery is disabled unless a later
integration session explicitly sets `HEARTSIDE_ENABLE_CC_DELIVERY=1`.
`growth.py library` builds the complete seven-concept library; the manual
`handoff.yml` workflow attaches its verified output to the owner-only draft
completion release. It uses the GitHub runner identity for binary uploads and
does not change any autonomous schedule.

`growth.py bundle <pack-path> local/review/campaign.zip` creates a portable review
artifact. Unzip and open `review.html`. No web account or second dashboard is needed.

The seven checked concepts with 28 prewritten hook experiments cover three reusable families: recognition, product
proof and a question to the audience. Since 29 Oct they show only the live store's current renders, blanket and
portrait in most concepts and the mug in one; any of them may be sold. Each has native captions, hook
metadata, a declared mechanism and an audience intent. Selection falls back to a
stable seven-day rotation, never an invented trend. An eligible observed
replication candidate gets a changed opening and hook ID, holding its mechanism
constant. It is an exploratory test, not an automatically established winner.

Every pack has a 1080x1920 Instagram film, distinct Facebook/TikTok opening
editions, a cover, three Story frames, two 1000x1500 Pins, three 1080x1350 carousel
slides, SRT subtitles, checked alt text, downloadable narration and an original locally synthesized score. Restrained
push-ins preserve the actual approved product imagery. Narration imports are
supported with an approved transcript, exact source SHA, checksum and duration.
See [the AI provider contract](PROVIDERS.md). The default films combine local Kokoro neural narration with the original
score and captions. All narration remains a draft requiring human listening
review; it uses no metered provider API. See [voice provenance](VOICE-LICENSES.md). Nothing is approved or published by rendering.

The logo and typefaces come from the full synced Heartside commit
(`--heartside-dir /path/to/heartside` reads via `git show SHA:path` without
executing its code). Product images are the live store's own gallery renders,
named role by role in `engine/assets.py` (`PRODUCT_IMAGES`), each recorded with
its source URL and checksum; a blank template or checkout tile is refused, and
every frame carries an Example label. The retired fictional Biscuit entryway
scene was removed on 29 October 2026 (Biscuit is retired). Each output has file checksums, native copy digests,
product SHA and a content-addressed revision. Modified copy/files fail checking;
failed renders preserve previous output. Renderer source and FFmpeg/Pillow/zlib versions also participate in revision
identity, so different production runtimes cannot silently share an approval.
A new revision needs fresh human review.

## Autonomous draft scheduling

The `Heartside draft engine` GitHub Actions workflow checks the seven canonical
schedules in `automations.json` every 15 minutes. It is a single serialized writer
per branch. All scheduling uses `America/New_York`, including daylight saving;
GitHub can start late. The independent public product sync remains hourly.

```sh
python3 growth.py run                 # only due jobs, idempotent per day/job
python3 growth.py run --job all       # prove all declared job types now
python3 growth.py run --job numbers   # a declared job, still idempotent
```

Every job syncs current product canon first. Failed jobs remain retryable, with
at least 15 minutes between attempts. Independent jobs continue. A two-hour local
writer lease recovers after a crash; the GitHub job timeout is one hour. Completed
jobs do not regenerate the same day's creative. Run results and failure types
are under `local/automation/`, with checked packs and review ZIPs under
`local/automation/runs/YYYY-MM-DD/`. The runner never contacts Control Centre. A changed product/catalog fingerprint
or corrected metrics refreshes affected completed jobs; unchanged inputs do not
repeat production. `run --job NAME --force` is an explicit operator rebuild.
Previous pack revisions remain in per-job history. The checkpoint excludes
duplicate review ZIP bytes; the latest review is rebuilt from verified media
after restore.

The GitHub workflow restores a validated checkpoint from its own previous
trusted same-branch run. It checks the workflow path, source repository, regular
file paths, size bounds, checksums and SQLite integrity before replacing state.
Checkpoint version two stores identical bytes once, including assets reused
across product commits; restore creates independent files after verifying every
internal duplicate. Original version-one checkpoints remain readable. Both the
engine and manual library export share one writer group and one authoritative
ledger, so any exported campaign can receive a later publication/insight record.
A missing/expired checkpoint after a previous successful run fails closed rather
than silently starting a second campaign history. The latest three checkpoints
and standalone review artifacts are kept with 90-day expiration. Hot media
and per-run files retain seven days; permanent creative/evidence ledger
metadata remains. Compressed checkpoints are capped at 100 MB. Save publication
masters separately for longer retention; this is not unlimited storage. A workflow run after restore proves idempotency.

Download `heartside-state`, extract `state.tgz`, then restore to another checkout:

```sh
python3 growth.py snapshot restore /path/to/state.tgz --replace
```

Close engine processes first. Existing state is retained in a local recovery
folder. `snapshot export local/backups/new-state.tgz` produces a consistent SQLite
backup including committed WAL records. Lists, raw customer files, tokens and
arbitrary local directories are excluded. Public-repository Actions artifacts are
not confidential storage: they contain only approved marketing/example material
and allowlisted aggregates. Never put customer or creator identities in them.
Raw creator research stays under `local/lists/` and is not checkpointed.

The runner has no private social browser or inherited connected-Shopify token.
Its numbers job uses imported aggregate evidence and names its actual windows;
its radar reads public search suggestions and labels them as suggestions, not
volume or trends. Its creator job reports the research boundary and operating
brief, without pretending it has sent gifts or verified profiles it cannot read.
Connected authoring sessions can carry out the richer research in `jobs/`.
This fallback runs unattended; fresh multi-provider generation and private
analytics collection are not silently claimed as deployed capabilities.

## Offer readiness

`readiness` binds canonical gift IDs, approved prices, available public variants
and landing-page readiness to a current catalog snapshot. The retired public
range does not establish readiness for the new range. Initial campaigns are
price-free audience materials. Purchase copy must name exact structured `offers`
and match that gift's actual live price and destination. A bundle discount needs
current confirmation that the store applies it, not merely a canon price table.
No Christmas order-by deadline is promised without current confirmation.

## Aggregate measurement

Use connected Shopify analytics after verifying Heartside and its IANA timezone.
Read reports, never order/customer records. Schema: `platform: shopify`,
`scope: store`, `currency: USD`, `source`, offset `observed_at`, `period` with
inclusive `start`, exclusive `end`, verified `timezone`, and the tool's `result`
(`shopDomain`, `columns`, one ungrouped `rows` entry), or explicit allowlisted
aggregate `values`. The verified store's Shopify handle is never published: it is the
`HEARTSIDE_SHOP_DOMAIN` repository variable, and `heartside.io` is always accepted. The shop's
IANA timezone was verified as `Europe/London`; a display abbreviation such as
BST must not replace that zone. Source reporting days are independent of New
York job times.

```sh
python3 growth.py metrics import local/metrics/report.json
python3 growth.py metrics report --start 2026-10-01 --end 2026-10-17 --timezone Europe/London
python3 growth.py dashboard --start 2026-10-01 --end 2026-10-17 --timezone Europe/London
```

Only finite allowlisted totals/rates are imported. Customer fields, grouped
rows, wrong stores and invalid counts fail. Null stays missing. Corrected windows
replace prior observations; rates and overlapping windows are never summed.
Partial coverage remains explicit. Refunds can make net sales negative.
Month-to-date corrections are needed even when daily imports already exist.

`dashboard` prepares numbers and progress packs in the existing central format,
with source observations, timezone, coverage and prepared recommendations. It
works without central credentials. Store totals are never allocated to the
latest creative. The actual October 1–16 audit showed one order and zero net
sales; it is not proof of current V3 conversion or organic attribution.

## Publication and creative insights

```sh
python3 growth.py creatives mark CREATIVE_ID FULL_REVISION approved
python3 growth.py creatives mark CREATIVE_ID FULL_REVISION published --url REAL_PLATFORM_URL
python3 growth.py insights import local/metrics/creative-observation.json
python3 growth.py insights decisions
```

Only an operator may record a real publication after it happens. An insight
requires that exact published revision, matching platform, an allowlisted HTTPS
report surface, offset publication/retrieval timestamps, an attribution field
and allowlisted aggregate values. See `examples/creative-observation.json` for
the schema; it is illustrative data, never imported as evidence. Native attention
cannot carry orders/net sales. Shopify attribution requires an explicit filter
to the exact `utm_content` creative ID. Observations replace lifetime snapshots;
they are not additive and do not change the whole-store revenue ledger.

A pilot replication candidate needs current native evidence, at least 2,000
reach, 48 hours, observed sends, two same-platform peers in the same 48-hour
age band, at least 10 sends/1,000 reach and twice their median rate. These are
experimental thresholds, not validated benchmarks or statistical significance.
Sparse, stale or absent metrics stay inconclusive. No command scales spend or
publishes. Unattributed sales and unknown costs remain unknown.

## Recovery and verification

```sh
python3 growth.py --self-test
python3 -m unittest discover -s tests -v
python3 growth.py ledger backup local/backups/new-ledger.sqlite3
```

Checks cover copy/offer gates, current source binding, real FFmpeg exports,
cache/tamper/failure behavior, publication evidence, aggregate corrections,
overlap, provider budgets and uncertain submissions, conservative insights,
DST schedules, idempotent/retryable jobs, archive traversal and checkpoint
recovery. CI installs the media runtime. No test calls a paid provider, social
publisher or production database.

## Feed human records back into hosted state

The hosted ledger can accept bounded operator evidence without publishing
anything or using Control Centre. Use the engine workflow's `operator_events`
input with a JSON array, and choose the declared `report` job to refresh the
progress/decision pack. The same array works locally with:

```sh
python3 growth.py events import local/operator-events.json
```

Local imports stay local. To update scheduled runs, supply the evidence to the
GitHub workflow; do not assume another checkout automatically syncs its SQLite
file. An eventual central UI can use this same typed contract.

`creative_status` events contain exactly `event_id`, `type`, `creative_id`, full
`revision`, `status` and `url` (null except a real publication permalink).
`insight` events contain exactly `event_id`, `type`, `observation`, using the
creative aggregate schema above. See `examples/operator-events.json`. Its
placeholders are deliberately invalid; never import illustrative observations
as real evidence. Approval/publication validates the exact stored media first.

Event IDs are stable. A replay is a no-op; reusing an ID for changed evidence
fails. Partial batches retain per-event receipts, so a retry skips the applied
prefix. The workflow checkpoints even when a later event fails. Unknown fields,
customer records, unsupported statuses and ambiguous or modified media fail.
A status record asserts what the human actually did; it never posts, sends,
orders or generates media on their behalf. Report fingerprints include creative
status and insight observations, so importing evidence refreshes the learning
report without replacing a completed day's creative.

## Control Center protocol loop

Control Center wakes this repository once a day, at about 06:10 London, with a
`repository_dispatch` of type `cc-growth-directive`. The
[Control Center directive](../.github/workflows/control-center.yml) workflow
then runs the protocol in
[docs/control-center/ENGINE-PROTOCOL.md](control-center/ENGINE-PROTOCOL.md).
A manual run from the Actions tab does the same, as `live` or `synthetic`.

1. `growth.py cc start` records the attempt as `started` before any source is read.
2. The workflow restores the engine's latest trusted checkpoint, read only. This
   loop never writes a checkpoint, so `engine.yml` stays the only writer of engine state.
3. `growth.py cc run` reads today's directive, syncs product truth, reads the
   ledger, builds the report, sends it with `Idempotency-Key: <run_id>`, reads it
   back and compares `payload_sha256`, reads Krish's decisions from the last
   seven days and closes the attempt as `succeeded`, `failed` with a lower_snake
   code, or `unknown` when a write's outcome cannot be read back.
4. If a step between them fails, `growth.py cc finish` closes the attempt as
   failed with `checkpoint_restore_failed`.

It renders no media and calls no paid provider. It never posts, sends,
publishes or spends.

| Part of the report | What the engine sends |
|---|---|
| `net_sales_usd` | Imported Shopify net sales for the London month to date (on the 1st, the month that closed). `measured` only when imported windows cover every day, `stale` when they stop earlier (the window says where), `missing` with a reason otherwise. Overlapping windows are never added together |
| `organic_orders` | Always `missing` for now, with the reason: store totals do not show which post caused an order, and creative UTM observations are lifetime snapshots, not weekly windows |
| `proposals` | Each recommendation in `recommendations.json` (its `id` is the stable `proposal_id`, `close_event` its close), and each approved creative whose media and caption still match its render manifest as `wall: post`. The caption is `exact_payload`, the platform is `channel`, and `payload_sha256` is the SHA-256 of canonical `{caption, channel, creative_id, revision}`. It expires when the hot media is pruned. No `spend` proposal: the budget is $0 and the engine recommends no boost |
| `events` | `creative_published` with the permalink, for each publication recorded in the last 14 days |
| `holds` | The product constraint from heartside PR 13, read from current product truth: purchase claims while the catalog differs from the canon, then conversion editions until the V3 homepage is public. Also approved creatives that could not be verified |
| `status` | `degraded` when product sync failed or no checkpoint was available, otherwise `held` when anything is held, otherwise `ready` |

The run id is `heartside:<London date>:directive` for the daily dispatch,
`manual-<run id>` for a manual run, with `-a<n>` on a rerun and `synthetic-`
in front in synthetic mode, so a rerun never collides with the day's report.
A 409 is read back, never retried. A decision binds to its `payload_sha256`:
a declined payload is not proposed again, a changed payload goes back to Krish,
and an approved post still waits for him to post it by hand and record the
permalink through the engine workflow's `operator_events`, after which the next
report carries the `creative_published` event.

The bearer is the `CONTROL_CENTER_ENGINE_TOKEN` secret, given only to the
three `growth.py cc` steps; `CONTROL_CENTER_URL` is a repository variable. The
client uses HTTPS only, follows no redirect and times out after 20 seconds. It
never prints, logs or stores the token; failures are codes. With no secret the
step fails with "CONTROL_CENTER_ENGINE_TOKEN is not set" and makes no request.
`python3 -m unittest tests.test_protocol` proves the loop against an in-process
stand-in; the CLI's default `--mode synthetic` never touches Krish's numbers or list.

## Verified conversion media

The renderer also accepts `intent: buy` with one declared unit of a live gift,
the exact live product `destination`, and current gift `offers`, when the film
shows that gift. Every gift qualifies, the mug included (Ruling, Krish,
2026-10-29). The same copy, price, availability, source, subtitle, narration and
media checks apply. Put `{link}` in native captions; rendering supplies a separate
tracked destination for every creative ID. Structured offers are included in
purchase-copy digests. A different gift, wrong price, unavailable product or
missing link fails before production. No discount, delivery deadline or checkout
result is invented.

When the gifts and the homepage are public and the catalog is current, the
scheduled fallback tests a conversion edition every third day for the gift the
film ends on. It reads the canon's configured price and the live destination;
the remaining days keep recognition and sharing hypotheses. An authoring session can prepare its own verified purchase spec using
these same boundaries. For Instagram/TikTok, place the prepared URL in the
appropriate link surface by hand; a shared bio link does not establish which
Reel caused an order. Direct Story/Pin links provide more specific evidence.

## Organic attribution

`python3 growth.py attribution` reads which store orders came from organic posts
and stores aggregates only (`engine/attribution.py`). It runs in `engine.yml`
before the draft jobs, at most every six hours.

- **Tags.** Every tracked link carries `utm_source` (the platform),
  `utm_medium` (`organic_video`, `organic_social`, `organic_search`,
  `product_listing` or `email`), `utm_campaign` (`hs_growth_YYYYMM`) and the
  creative id in `utm_content`. The post family is the creative id's platform,
  pillar and concept, for example `IG_EMO_C90`.
- **Tiers.** `engine` (this engine's tags), `organic_social` (a social
  referrer or organic tags), `organic_search`, `paid` (a paid medium or an ad
  click id, never counted even when tagged), `pending` (Shopify's journey not
  ready, up to 72 hours) and `direct`. Organic posts are `engine` plus
  `organic_social`. Test, cancelled and `hs-internal` orders never count.
- **Windows.** The trailing 28 days and the last full Monday-to-Monday week,
  by the London day each order was created. Net sales are each order's
  current subtotal after discounts and refunds, before shipping and tax.
- **Privacy.** The query reads an exact field list (a test holds it). No
  order id, customer field, line item or note is read. Landing pages and
  referrers are used only to classify an order and are never stored; their
  query strings can hold a buyer's dog and person names.
- **Access.** A Shopify Dev Dashboard app with exactly `read_orders`, whose
  client id and secret are repository secrets (names in `engine.yml`), plus
  the store handle variable. A token with any other scope is refused. Without
  them the step prints a hold naming what is missing, and the Control Center
  report keeps `organic_orders` missing, never zero.

