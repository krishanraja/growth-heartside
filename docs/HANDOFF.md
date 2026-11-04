# Heartside growth engine handoff

The engine is merged and active on main. Implementation and acquisition work live in this repository. Product and print
work was handed to heartside PR #13. Control Centre gets only
[its completed owner brief](CONTROL-CENTRE-BRIEF.md). Its existing draft was left
untouched during this completion; central delivery defaults off.

## Production handoff for F04, F05 and F12 (4 November 2026)

Three motion edits were made for existing posts. Each keeps its original audio, ends on its product and says “Make yours at Heartside.io”. The owner board played each complete export and served the SHA-256 listed below. No owner decision was present for these three exact files on 4 November. Review them under **Motion candidates** on the private Heartside board.

| Post and locked original in Drive | What changed in the motion edit | Board review ID | Reel SHA-256 |
|---|---|---|---|
| F04 · `Posts/F04/heartside_F04_me-vs-my-golden_reel.mp4` | The golden retriever takes the sofa seat. The reveal is the personalized golden blanket. 23.2 s, 696 frames. | `F04-MOTION-346c19bd14` | `346c19bd1440a1b95fd83fef5144901eb58d5517a6192f71bf9e7d11a4e754c4` |
| F05 · `Posts/F05/heartside_F05_court-of-the-couch_reel.mp4` | The Frenchie defendant and basset judge move. The jury remains illustrated. The film ends on the blanket. 30.1 s, 903 frames. | `F05-MOTION-980a3a9348` | `980a3a93482abf06e2697c96409576222ac8daeab09d5dec819cb39be0882e7f` |
| F12 · `Posts/F12/heartside_F12_head-of-security_reel.mp4` | The Frenchie spots the parcel, approaches and turns to sleeping backup before the personalized portrait reveal. 18.5 s, 555 frames. | `F12-MOTION-0b93e56eaf` | `0b93e56eaf927284956854aaec6130e9b76161bd7ceb4f1a44717a3c19748ac1` |

**Find the exact files.** In the private production workspace, the board reads `outputs/heartside-feedback-round/media/heartside_<id>_motion-review_reel.mp4` and the matching `heartside_<id>_motion-review_cover.jpg`. Substitute F04, F05 or F12. The reels are 720 × 1280 H.264/AAC at 30 fps. The three covers are 1080 × 1920 JPEGs. The private growth checkout has the source paths, shot selections and byte counts in `local/research/2026-11-03-pov/motion-review-manifest.json` and playback evidence in `motion-board-live-verification.json` beside it. The 1080 × 1920 working exports in `work/mobile-review/motion/<id>-motion-master1080.mp4` have different hashes. A release from one of those files needs its own exact-file check and owner sign-off.

**Separate F12 Facebook opening test.** Both files below are in the same private board media directory. They run 18.5 s at 1080 × 1920 and 30 fps. Only the first 60 frames differ visually. The audio and all decoded frames from 2.0 s onward match.

| Arm | File | SHA-256 | Creative decision |
|---|---|---|---|
| A · parcel first | `f12-parcel-first.mp4` | `5cf938e6df38259c4983b097999c576345ba527438f472ffd3dfd487317e32dd` | Byte-identical to the locked F12 Drive reel. Control. |
| B · guard first | `f12-guard-first.mp4` | `d7e6e06a1219757cc27df392b8fca6b236567d968f5da761e86d20c4aad245c7` | Krish approved this close-up opening on 4 November. It replaces the earlier portrait-first challenger. |

**Next action for Claude.** Read the three exact owner decisions from the private board before proposing any replacement. The [Drive map](DRIVE-MAP.md) reserves `Posts/<id>/` for locked media sent through the home-computer library lane. The three existing library reels and their covers remain the scheduling sources. Creative preparation owns candidate review. The scheduling desk alone operates the queue. The separate Facebook Feed test has an approved $90 lifetime budget ($45 per arm) and is held until Krish has seen the tracking checks and exact launch plan. Use `f12-paid-and-motion-review-plan.json` and `f12-guard-chat-approval.json` beside the private motion manifest for the exact experiment and decision.

**Earlier work in this chat.** In that same private evidence directory, `today-release-manifest.json` maps the ten earlier review items to source cards, files and checksums. `centered-caption-changes.json` records the POV text corrections. `weekly-gallery-release-manifest.json` maps 40 organic placements and two historical paid proposals to their media. Read those as placement history. The three motion edits above are the new films, and the F12 opening plan above supersedes those paid proposals.

## Delivered

- Current product canon/catalog sync, full source SHA binding and exact offer gates.
  Verified Morning Mug conversion editions activate only when the public gift
  and V3 homepage are ready; otherwise production remains audience-led.
- Seven campaign concepts with 28 hook experiments in three reusable families, with a newly generated,
  disclosed fictional Biscuit scene kept separate from real approved product photos.
- Native Instagram, Facebook and TikTok films with local neural narration,
  original score, restrained motion, cover, three Stories, three carousel slides,
  two Pins, subtitles, downloadable narration and platform captions/alt text. Downloadable HTML/media review ZIPs.
- Stable creative revisions, cache/tamper checks, human review/publication records
  and real URL evidence. Generation never approves or publishes.
- Serialized provider cost reservations, current quotes, recorded receipts,
  uncertain-submission recovery and role/provenance boundaries. Paid external
  generation remains disabled, with a zero default monthly budget.
- A validated hosted operator-evidence input for real human review/publication
  records and aggregate creative insights, with idempotent event receipts and
  partial-batch recovery. It never publishes on behalf of the human.
- Strict Shopify aggregate imports, corrections, overlap-safe reporting, private
  native/UTM insight imports and conservative exploratory replication decisions.
- One persistent GitHub Actions runner executing the seven declared schedules,
  with timezone/DST handling, idempotency, retries, writer lease, verified portable
  checkpoints, bounded artifact storage and a standalone review download.
- A 30-day acquisition strategy, creator operating brief and central integration
  brief with concrete UI gaps and acceptance checks.

## Download the complete library

The [draft completion release](https://github.com/krishanraja/growth-heartside/releases) holds the full seven-campaign
library and handoff documents. It requires the repository owner or an authorized
collaborator to sign in. Download `heartside-campaign-library.zip`, unzip it, and
open `index.html`. Nothing in that draft release publishes a social post.

The manual library export shares the authoritative hosted ledger and writer
lock with scheduled jobs. Every exported creative revision is persisted before
the download is attached, so the same validated operator-evidence input works
for all seven campaign packs. Duplicate asset bytes are stored once per
checkpoint; restored files remain independent.

## Where to operate

Use [the engine workflow](https://github.com/krishanraja/growth-heartside/actions/workflows/engine.yml).
The latest successful run provides `heartside-review` and `heartside-state`.
Unzip the review artifact, then its inner ZIP, and open `review.html`. For local
work, run `python3 growth.py sync`, then the commands in [the runbook](ENGINE.md).
The seven schedules remain in [automations.json](../automations.json), all in
America/New_York. Connected Codex/Cowork sessions can use the richer job prompts;
the hosted fallback needs no private browser or central dashboard.

Private creator research is never included in checkpoint artifacts. Publication
masters need separate long-term storage beyond the seven-day hot workspace.
The latest three checkpoints/review artifacts are retained with 90-day expiry;
compressed checkpoint size is capped at 100 MB. Missing recovery state fails
closed. Public-repository artifacts are not confidential media storage.

## Verified production and recovery

- [Production bootstrap](https://github.com/krishanraja/growth-heartside/actions/runs/39024960655): all seven jobs completed; two verified Shopify aggregate envelopes imported.
- [Production replay](https://github.com/krishanraja/growth-heartside/actions/runs/39025075980): restored that checkpoint and skipped all seven completed jobs.
- [Controlled invalid-job test](https://github.com/krishanraja/growth-heartside/actions/runs/39024993241): failed as intended on the test branch; checkpoint upload and storage cleanup succeeded.
- [Recovery replay](https://github.com/krishanraja/growth-heartside/actions/runs/39025077762): restored the failed run's valid checkpoint and skipped all seven completed jobs.
- [Hosted operator evidence deployment](https://github.com/krishanraja/growth-heartside/actions/runs/39025502013): validated evidence input and all production steps succeeded without recording any fictional publication.
- [Final hosted replay](https://github.com/krishanraja/growth-heartside/actions/runs/39025604815): validated the evidence-input step, restored the current production checkpoint and skipped all seven completed jobs.
- [Implementation CI](https://github.com/krishanraja/growth-heartside/actions/runs/39028701800): 110 self-checks and 52 tests passed, including actual neural voice synthesis.

- [Full library export](https://github.com/krishanraja/growth-heartside/actions/runs/39027003626): all seven campaign packs were restored, verified, persisted in the hosted ledger and attached to the owner handoff.
- [Expanded checkpoint restore](https://github.com/krishanraja/growth-heartside/actions/runs/39027175642): the scheduled engine restored the deduplicated library checkpoint, reused completed production and refreshed the progress report for the expanded ledger.

- [Final expanded-state replay](https://github.com/krishanraja/growth-heartside/actions/runs/39027495460): all seven jobs were already complete after the portable-path and archive validation checks; no duplicate production occurred.

- [Final conversion-capable production](https://github.com/krishanraja/growth-heartside/actions/runs/39028701698) and [unchanged-input replay](https://github.com/krishanraja/growth-heartside/actions/runs/39028901853): the final implementation ran successfully, then reused all seven completed jobs. Conversion rendering passed with a synthetic ready-catalog fixture; no real order was placed. The real store remained gated.

The machine-readable [verification receipt](VERIFICATION-2026-10-17.json) records
source revisions, actual run conclusions, campaign/library checksums and explicit
capability limits. The invalid-job test is expected failure evidence, not an
unresolved production incident.

## Evidence and limits

Verification records are in `local/handoff/verification.json` and workflow runs.
The checks exercise real FFmpeg exports and local neural synthesis, recovery to
another workspace, failure preservation, retry/idempotency, provider budgets,
source/copy/media binding, strict aggregate reporting and sparse/stale insights.
All seven job types were run locally. The first hosted execution also
completed all seven job types successfully in
[run 39023911551](https://github.com/krishanraja/growth-heartside/actions/runs/39023911551).
The test suite passes 110 self-checks and 52 unit/integration tests, including
actual neural synthesis. Hosted runs verified checkpoint restore, failure recovery and idempotency
against the final implementation source revision.

Shopify's verified October 1–16 aggregate showed one order and zero net sales,
380 sessions, 40 cart sessions, 21 checkout sessions and one completed-checkout
session. Those are whole-store observations, not new-range conversion or organic
attribution. The public catalog still does not offer the four canonical V3 gifts.
Purchase campaigns remain gated to actual public readiness.

Fresh private social insights and automatic private Shopify collection are not
available to the hosted runner. It uses imported observations without inventing
missing values. No social post, message, creator gift, paid AI API job, product
order, store change or Printful confirmation was performed. The local neural
voice needs no metered API; image generation used the native authoring tool,
whose output did not include a monetary charge.

No performance winner, viral outcome or $10,000 revenue result is claimed. The
engine and operational verification are delivered; product readiness, source
access and real human publication are visible operating dependencies, not tasks
hidden behind a completion claim. The Control Centre owner has the brief and
acceptance checks, without any new implementation in that repository.
