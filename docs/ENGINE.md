# Running the growth engine

The engine produces reviewable marketing media and keeps a record of what was
made, posted and measured. Product, checkout, personalization and fulfillment
work is handed to [heartside PR #13](https://github.com/krishanraja/heartside/pull/13).
This repository reads product truth and never deploys the store. `STRATEGY.md`
holds the acquisition experiment; `AGENTS.md` holds the operating permissions.

## What works now

- Canon and live catalog sync, with product-specific readiness.
- Checked audience media from approved real product photos, read at the
  synced product commit: Reel, cover, three Stories, two Pins and subtitles.
- Content-addressed media caching, file checksums and human review status.
- Transactional SQLite creative revisions and publication evidence entered
  by an operator. Recording a URL does not publish anything.
- Importing aggregate connected-Shopify reports, including corrected reports,
  without adding duplicate or overlapping windows.
- Consistent portable ledger backups. Storage is local, not automatically
  replicated to a cloud service.

The first renderer makes an example audience pack with simple cuts and a
silent audio track. It does not generate new AI scenes, voice, music or
customer-specific artwork. Its manifests say which approved assets it used.
Paid provider adapters, shared n8n state, platform-insight imports and automatic
experiment selection are subsequent work. No social publisher is installed.

## Start a run

```sh
python3 -m pip install -r requirements-media.txt
# Install FFmpeg (including ffprobe) with the system package manager.
python3 growth.py sync
python3 growth.py readiness
python3 growth.py render campaigns/waits-at-the-door.json
```

Use `--heartside-dir /path/to/heartside` on `assets` or `render` for an
existing checkout. Assets are read using `git show <synced-sha>:<path>`, so
uncommitted edits and a different checkout branch cannot replace them.
Without that option, the same paths are downloaded from raw GitHub at the
full synced SHA. They are cached under `local/assets/` with source paths and
SHA-256 checksums. Rendering never executes code from the other repository.

The campaign file is an editable production spec. It gives the concept,
hook, pillar, variation, three scenes and native captions. `C90` is the
starter example. Use a new concept number for a different mechanism, a new
hook number for a different opening, and a new variation for a derivative.
Review changed product canon before reusing any template or example photo.

The renderer prints a draft path under `local/drafts/`. Then run:

```sh
python3 growth.py check <printed-draft-path>
python3 growth.py post <printed-draft-path>
python3 growth.py creatives list
```

Replace the angle-bracket placeholder with the printed path. The media lives
under `local/media/<creative-id>/<revision>/`. A daily pack needs a verified
production manifest; a text-only brief cannot pass `check` or `post` as a
finished daily pack. Every file is verified before storing. A media manifest
must match the pack's creative, native copy and product commit. Changed files invalidate
the check. Failed encodes build in a temporary directory and leave prior
outputs intact. Repaired output returns to the rendered state for review.

`post` means store the internal pack, not publish a social post. Previous
versions of a stored pack are retained in `local/packs/history/`. Scratch
drafts are outside the packs directory so weekly reads do not count them
twice.

## Offer checks

`readiness` lists the canonical gifts, approved prices, current public
products and the reason each gift is ready or blocked. It distinguishes a
machine ready to work from a gift ready to sell. A public catalog containing
four retired products does not make the new range ready.

Public prices or purchase copy must name their offers in structured metadata:

```json
{"intent":"buy","offers":[{"id":"the-morning-mug","quantity":1,"unit_price":"29.00"}]}
```

This is a schema example; re-read current readiness before using a price.
Gift IDs and prices come from the synced gift table. The amount must belong
to that particular gift and an available live variant, and the tracked link
must lead to that gift or a ready gifts landing page. A discounted bundle
also needs current confirmation that the store applies it; the price table
alone is not evidence of an active discount. The initial renderer emits
audience packs without public prices or purchase links.

## Aggregate Shopify reporting

Use the connected Shopify reporting tool when available, after verifying
that it is Heartside. Read reports, not orders or customer records. Discover
current ShopifyQL metrics and syntax before constructing queries.

The tested sales query selects `orders, net_sales` from `sales`. The tested
funnel query selects `sessions, sessions_with_cart_additions,
sessions_that_reached_checkout, sessions_that_completed_checkout,
conversion_rate` from `sessions`. Use one ungrouped row per import.

Write a local JSON envelope with these fields:

| Field | Meaning |
|---|---|
| `platform` | `shopify` |
| `scope` | `store`, meaning an unfiltered whole-store aggregate |
| `currency` | `USD` |
| `source` | The report/query and reporting surface |
| `observed_at` | Actual retrieval time, ISO 8601 with UTC offset |
| `period.start` | Inclusive calendar date |
| `period.end` | Exclusive calendar date |
| `period.timezone` | Store's verified IANA timezone, not a fixed abbreviation |
| `result` | The tool's structured result containing `shopDomain`, `columns` and one `rows` entry |

An inclusive ShopifyQL `UNTIL October 16` is recorded with exclusive end
`October 17`. The API confirmed Heartside's timezone as `Europe/London` on
17 October; read it again if configuration changes. New York job times do
not turn store reporting days into New York days. Never relabel a London
day as New York to make the numbers fit.

```sh
python3 growth.py metrics import local/metrics/<report>.json
python3 growth.py metrics report --start 2026-10-01 --end 2026-11-01 --timezone Europe/London
```

Only allowlisted aggregates are accepted. Customer fields, grouped rows,
wrong-store results, nonfinite numbers and invalid counts fail. Null means
missing, not zero. A corrected observation replaces that source's window;
an older observation cannot overwrite a newer one. A conflicting correction
needs a later actual observation time.

Reporting chooses nonoverlapping complete windows separately for each
additive metric. It prefers a broader complete aggregate to overlapping
daily fragments, never sums rates, and shows covered days and source
evidence. It does not prorate a broad window into smaller days. Partial
coverage must be described as partial. Different timezone windows never mix.
Orders can remain nonzero when a sale was refunded; net sales are the
revenue ledger. There is no per-creative revenue attribution in this adapter
yet, so an account total must not be credited to the latest Reel.

## Review and record publication

```sh
python3 growth.py creatives mark <creative-id> <full-revision> approved
python3 growth.py creatives mark <creative-id> <full-revision> published --url <real-platform-url>
```

Run the second command only after Krish actually posts the approved asset.
The URL must belong to the creative's platform. Revision history keeps the
publication evidence; editing or repairing the same render requires review
again. These commands only write the local ledger.

```sh
python3 growth.py ledger backup local/backups/engine-20261017.sqlite3
```

Choose a new filename each time. Backups include committed WAL records.
When changing machines, copy the backup and the referenced `local/media/`
and `local/assets/` directories. Close running jobs before restoring a copy
to `local/engine.sqlite3`. A fresh cloud workspace has no previous local
history unless those files are restored. A shared storage adapter is still
required for unattended execution across different machines.

## Next engineering work

1. Add a cost and capability contract for connected image, motion and voice
   providers. Require a configured budget before a paid request, use
   idempotent request IDs and bounded retries, and keep the deterministic
   template usable when providers fail.
2. Add native media templates and reusable approved motion. Maintain product
   truth, exact typography, source provenance and platform safe zones.
3. Add a shared-state adapter to existing n8n infrastructure if its limits
   suit the workload; keep imports and backups portable.
4. Import native platform insights and known attribution before implementing
   automatic scale/hold/kill decisions. Keep low-volume results inconclusive.
5. Feed the first-party sharing event contract back from the product repo.
   `hs3_share_card` currently means a card render, and `hs3_add_to_cart`
   means a handoff to product pages. Confirmed purchases come from Shopify.

Social publishing permissions and human print confirmation remain as stated
in `AGENTS.md`. This implementation does not change them.

## Verification

```sh
python3 growth.py --self-test
python3 -m unittest discover -s tests -v
```

The tests cover price binding, unavailable variants, missing daily work,
correction and overlap behavior, publication status, backups, real FFmpeg
encoding, cache reuse, file tampering and failure preservation. CI installs
the optional media dependencies. The core sync and copy checker remain
standard-library Python.

## Control Center reporting

Control Center is the unified dashboard. The reviewed server change is in its
`codex/heartside-growth-reporting` branch. Until its migration and application
are deployed and the runner can authenticate, reports remain local retry
copies. A repository checkout does not supply runtime credentials.

Build the dashboard's two packs from aggregate evidence:

```sh
python3 growth.py dashboard --start 2026-10-01 --end 2026-10-17 --timezone Europe/London
python3 growth.py check local/drafts/dashboard/2026-10-17-numbers.json
python3 growth.py post local/drafts/dashboard/2026-10-17-numbers.json
python3 growth.py check local/drafts/dashboard/2026-10-17-report.json
python3 growth.py post local/drafts/dashboard/2026-10-17-report.json
```

Use the date printed by the command and the reporting period actually imported.
The examples above describe an exclusive end, not a forecast. Each measure
keeps its source, actual observation time, timezone and coverage. Missing data
stays null, including missing revenue. The progress pack links prepared work
from `recommendations.json` with a next action and a completion condition.
These are recommendations, not automatic changes or another decision queue.

The API must advertise Heartside in `ventures`; every engine write and report
read names `venture=heartside`. Old publication callers remain scoped to
makeyourmindup. Local copies and media provenance survive remote delivery and
outages. Reads merge Control Center's marks with local production evidence;
a failed central read explicitly says it is showing local evidence only.
The renderer's paths do not make media remotely accessible. A private media
adapter and reconciliation of dashboard marks with the creative ledger are
still needed for a shared production review workflow.

The 17 October access audit verified repository access, connected Shopify
reports, Control Center's live database and Vercel project. Control Center's
06:00 UTC provider sweep reported its AI and n8n connections healthy. That
is evidence of the server's checks, not proof this runner can call those
providers or read private social insights. This runner has no authenticated
Control Center API session, signed-in social analytics or proven persistent
scheduler. Keep those gaps visible; never present missing access as zero
performance. Detailed integration and UI work belongs to Control Center's
`docs/handoff/heartside-growth/README.md`, not a second dashboard here.
