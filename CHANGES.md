# Changes Krish made to the growth engine

Newest first. Record his words with the date, then change the job file and
`automations.json` together.

- 2026-10-21, later: Krish: "rewrite those two docs as well, we need
  consistency" (heartside's `POSITIONING.md` and `HANDOFF.md`, rewritten for
  v3 at heartside 87c60af). `RULES_BASIS` holds their sections as re-read.
  `check` also refuses the retired one-line offer ("posters, ornaments and
  pillows"). The 12 Oct social plan left heartside's POSITIONING section 6,
  so `PLAYBOOK.md` cites it as "the 12 Oct plan" and says where it went.

- 2026-10-21: Krish, on heartside's gift lines (20 Oct): "It should be a
  message from your dog in their personality style... a humanized warm
  message from the dog to the person with some humour and dog
  anthropomorphisms." Then, asked whether this repo knew: "yes, do both and
  merge to main". Heartside's V3 section 2 changed, which stopped every pack.
  `RULES_BASIS` now holds V3 2 as read at heartside 0f345a7. `check` refuses
  the retired third-person gift lines ("Steals your side of the bed.") in any
  public copy, with two new self-tests. AGENTS.md rule 5, the proposition in
  `knowledge/COPY-DOCTRINE.md` and the Biscuit's-interview script in
  `PLAYBOOK.md` now use the dog's own voice. Schedules, `automations.json`
  and the jobs are unchanged.

- 2026-10-19: Krish, giving "The Copywriting, Offers and Demand Corpus":
  "all of these growth engines need to be imbued with this knowledge". Both
  uploads are preserved byte for byte in `knowledge/` and in
  `corpus-manifest.json`, and the self-test now checks every manifest file's
  bytes and SHA-256. `knowledge/COPY-DOCTRINE.md` applies the corpus to
  Heartside, with the list of where the canon and Krish's rules change it.
  `PLAYBOOK.md` and the daily-pack, creators, store, report and radar jobs
  now diagnose awareness and choose a lead before drafting, run edit passes A
  to E and the rubric before `check`, and log tests in the corpus's test
  record shape. Schedules, `automations.json` prompts, `check` and the Control
  Center protocol are unchanged.

- 2026-10-19: Krish: "make each engine adopt its brief now". The engine
  reports through Control Center's growth engine protocol. A new workflow
  answers the daily `cc-growth-directive` dispatch with `growth.py cc`:
  attempt, directive, report with readback, decisions. It reads the latest
  checkpoint without writing one, renders nothing and never posts, sends or
  spends. The seven scheduled jobs and pack delivery are unchanged. The
  recommendation to pass the old brief to Control Center's owner is closed
  and removed.

- 2026-10-17, latest scope: Krish: "you are not to do any actual work in
  control-center, only pass me a brief once you have completed your work."
  Then: "Complete this all to 100% without coming back to me again. The next
  reply should be confirmation of completion and handoff." Implementation,
  checks, draft scheduling and the handoff stay in growth-heartside. Control
  Centre delivery is disabled by default. No further changes to its existing
  draft, code, database or deployments are authorized by this instruction.
  Seven declared jobs now have a persistent GitHub Actions fallback. New
  campaign layouts, native exports, original local sound, fictional AI scene,
  provider reservations, insight decisions and recovery checkpoints are here.
  Publishing, creator gifts and paid generation retain their existing limits.

- 2026-10-17: Krish: "Put everything that's not related to the marketing and
  customer acquisition in the heartside repository so that one can pick
  this up: your recommendation up next and then leave everything else in
  this repository and start building the engine for it." Product work is
  handed to heartside PR #13. This engine adds named-offer checks, real
  example-media rendering, creative revision history and aggregate report
  imports. Daily and reporting jobs use those commands; the seven schedules
  and publication restrictions remain in place.

- 2026-10-15: the canon also takes the newest dated handover in heartside's
  `docs/`. On 15 Oct a Cowork session wrote `docs/COWORK-HANDOVER-2026-10-15.md`
  (Krish's "10X personalized delight" direction, the approved mug redesign,
  the four gifts in Draft) without adding it to heartside's README, so the
  engine could not see it. This keeps Krish's 14 Oct instruction ("always
  across what the main heartside repository is doing") true when the README
  lags.

- 2026-10-14: the engine is built from the two documents in `knowledge/`.
  Krish: "see attached for reference material that should train this corpus
  on how it can become a dominant force in what it does globally".
- 2026-10-14: the engine always follows the heartside repository. Krish:
  "Ensure the growth engine is always across what the main heartside
  repository is doing at any point in time". Every job starts with
  `python3 growth.py sync`. `check` refuses a pack written before a canon
  change, and a GitHub Action rewrites `state/HEARTSIDE-NOW.md` every hour.
- 2026-10-14: a dedicated repository, run from Codex or Cowork. Krish: "I
  want to build an autonomous browser based growth engine that can be run
  from anywhere (codex or cowork), solely focused on getting this business
  to 10k a month with minimal paid CAC", and "I lean to the latter for
  focus" (a dedicated repository over the heartside repository).

## 2026-10-17: Control Center is the reporting destination

Krish: "Control Centre is ultimately where the unified dashboard is going to
be: where you report back on progress and recommendations to improve in the
format that it requires." He also asked for missing access and UI to be made
visible. The latest scope correction above supersedes the earlier interpretation of
implementation authorization. Only the reporting contract and final brief belong
to this task; no further work in Control Centre is authorized.

Added dashboard report generation from the aggregate ledger, with sources,
timezones, coverage and prepared recommendations. Central reads are scoped
to Heartside and keep dashboard marks. Every delivery retains a local retry
copy and production manifest. Control Center's live API is not yet ready for
Heartside and this runner has no reporting credential. The separate Control
Center change provides venture isolation, commerce measures and read-only
report cards, with migration and rollout checks. It is not deployed.

## 2026-10-17: verify the existing reporting secret in Actions

Krish clarified that Vercel access covers his projects and that
GROWTH_ENGINE_TOKEN is already in GitHub secrets. Verified all 18 Vercel team
projects and the Production binding by metadata only. A read-only Actions
probe used the existing repository secret and authenticated to live Control
Center with HTTP 200 (run 39020889464, 09:22:45 UTC). The remaining delivery
block is the deployed legacy API's missing venture isolation, not a missing
credential. No token was read out of GitHub, copied into this machine or
included in the probe artifact. Updated the runbook and recommendation to
use the proven Actions execution path. Secret-list API access is unnecessary.
