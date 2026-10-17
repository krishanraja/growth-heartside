# Changes Krish made to the growth engine

Newest first. Record his words with the date, then change the job file and
`automations.json` together.

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
