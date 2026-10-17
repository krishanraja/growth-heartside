# Heartside growth: brief for the Control Centre owner

This is a handoff, not authorization for this task to implement anything in
Control Centre. Krish explicitly restricted implementation to growth-heartside.
The earlier Control Centre draft PR #472 was not changed, merged, migrated or
deployed during this completion. Its owner should reassess it against this
contract, rather than assuming it is the final required implementation.

## Outcome to support

On a phone, Krish opens Heartside's latest growth pack, watches the exact
creative revision, downloads native files, reads the caption, records what he
actually published, and sees sourced sales/progress plus a small actionable
recommendation. All ventures share the existing unified dashboard. There must
be no separate approval app or competing recommendation queue.

The engine is independently operational. Its current review surface is a
standalone downloadable HTML/media ZIP, and its state travels between runners
in checked GitHub artifacts. There is no central delivery while this brief is
unimplemented. `HEARTSIDE_ENABLE_CC_DELIVERY` defaults off. The automatic growth
workflow does not receive the central token or contact the dashboard.

## Existing contract and required isolation

The established internal reporting path is `/api/growth/packs`, authenticated
with the existing `GROWTH_ENGINE_TOKEN`. GitHub Actions proved that identity
against the live legacy API on 17 October, HTTP 200:
[verified run](https://github.com/krishanraja/growth-heartside/actions/runs/39020889464).
The problem was venture isolation, not a missing token. Secret values need not
be readable through GitHub's secrets-list API and must never be copied into a
brief, repository, browser link, artifact or generated media.

Before enabling delivery, the API must advertise `heartside` in a `ventures`
capability list, accept/read `venture=heartside`, preserve the full product
`source_revision`, and key upserts by `(venture, pack_date, kind)`. Existing
Make Your Mind Up callers must retain their historical venture semantics.
Store the raw production evidence in an appropriate private backend rather
than silently dropping it. A successful acknowledgement must echo the expected
venture, date, kind and full source revision. The engine retains its local retry
copy even after a successful delivery. Ambiguous acknowledgements are failures.

The engine already produces this reporting envelope:

```json
{
  "pack_date": "2026-10-17",
  "kind": "numbers",
  "venture": "heartside",
  "heartside_sha": "5618a99829a0c9ef1291b73c20cda3d837c262de",
  "source_revision": "5618a99829a0c9ef1291b73c20cda3d837c262de",
  "headline": "Source-backed sales and funnel evidence",
  "items": [],
  "numbers": [{
    "platform": "shopify",
    "net_sales": null,
    "orders": null,
    "sessions": null,
    "sessions_with_cart_additions": null,
    "sessions_that_reached_checkout": null,
    "sessions_that_completed_checkout": null,
    "note": "Reporting window, IANA timezone, covered days, source and actual observation timestamp."
  }]
}
```

This is a schema example, not an observation. Keep one platform's measures in
one row. Missing means not shown; zero is a measured zero. Never add rates,
overlapping windows or partial coverage into a fabricated full-period result.
Currency is USD; store reporting timezone is Europe/London independently of
New York job scheduling. Shopify net sales include discounts/reversals and
exclude shipping/tax. Actual store totals are not per-creative attribution.

Daily packs also contain `production.manifest` and `production.sha256`. The
manifest identifies `version`, `creative_id`, full `revision`, product SHA,
copy digests, provenance, duration, audio disclosure, review requirement and
files with `path`/SHA-256. Paths are local runner references, not usable remote
URLs. Do not render them as if the user could open them from another machine.

## Media and review UI gap

The earlier UI audit showed that text packs alone do not provide usable media
review. The required surface must add:

- A clear Heartside venture filter and product/engine source evidence.
- A playable vertical master and the Facebook/TikTok native editions.
- Cover, Story, Pin and carousel previews with direct downloads.
- Captions, alt-text guidance, subtitles, synthetic voice/character disclosure
  and rights/provenance alongside the exact revision.
- Human review/publication status bound to `(creative_id, revision)`, with a
  real platform URL and timestamp when the user records publication.
- Failure, stale-source, missing-file and unavailable-metric states that remain
  visible rather than looking like successful generation or zero performance.

Use private durable media storage with explicit access control and bounded
signed URLs resolved at viewing time. Local paths and expiring authoring-tool
URLs are not storage. Public-repository Actions artifacts are a bounded
operational fallback, not confidential customer/creator storage or a permanent
media library. The engine retains seven days of hot media and all creative
metadata; a central archive should define its own retention and storage budget.

Current statuses are `rendered`, `reviewed`, `approved`, `published`, `skipped`.
They describe evidence, not automatic social publishing. Central statuses must
reconcile with the engine ledger instead of approving a changed or older file.
Generated assets always require human review. Do not give progress/report cards
a misleading Posted action intended for a social creative.

## Available operator evidence transport

The growth workflow now accepts `operator_events`, a bounded JSON array of
`creative_status` and aggregate `insight` events. It writes only the engine's
hosted ledger, with stable event IDs, exact revision/file validation and replay
receipts. It never publishes a post. Local `growth.py events import` uses the
same contract. The owner may connect the existing central UI to this transport
or implement an equivalent authenticated outbox; neither is implemented here.
Unknown fields/customer data fail, and failed partial batches are checkpointed.
Progress reports refresh when statuses or observations change. See ENGINE.md
and `examples/operator-events.json` for the concrete current schema.

## Recommendations in the existing Home list

The engine's `recommendations.json` provides title, why, next action, completion
condition and evidence URL. Progress packs carry those fields in readable form.
In the existing Home surface, present a stable recommendation ID, venture,
owner, priority, the concrete prepared action, evidence and completion check.
Deduplicate refreshed reports. Recording a recommendation must not execute it.
One decision should have one canonical status and completion-evidence location.

The immediate product dependency is already in
[heartside PR #13](https://github.com/krishanraja/heartside/pull/13): the canonical
four gifts still differ from the public catalog. Growth keeps purchase claims
gated while making audience materials. The central UI should surface this
constraint without turning it into an implementation task in growth-heartside.

Fresh private analytics collection and paid provider credentials/budgets are
separate runtime capabilities. Connected tools in an authoring session and
healthy provider checks elsewhere do not establish those capabilities on a
GitHub runner. Show the actual source-access state, not a universal green light.

## Acceptance checks for the owner

1. Store and read Heartside and Make Your Mind Up packs with the same date/kind;
   neither is replaced, leaked or selected by the wrong venture filter.
2. Retry one Heartside delivery; it updates the same pack, preserving creative
   revision evidence and local recovery state. Verify the acknowledgement fields.
3. At 360px and desktop width, watch/download native media, read captions and
   evidence without horizontal overflow or expired source links.
4. Change one output file or its copy; the old review/approval cannot authorize
   the changed revision. Record an actual publication once and reconcile it.
5. Display a measured zero and a missing value differently, with reporting
   window, timezone, coverage and retrieval time visible. Keep attribution limits.
6. Surface one prepared recommendation in Home, act once, and retain its
   completion evidence without creating another queue.
7. Keep secrets, customer content and named creator research out of public
   repositories, public artifacts, signed URL logs and client bundle code.

No Vercel deployment, database migration or Control Centre merge was performed
as part of this growth completion. Its owner controls the implementation and
rollout sequence separately.
