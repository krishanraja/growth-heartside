# Changes Krish made to the growth engine

Newest first. Record his words with the date, then change the job file and
`automations.json` together.

- 2026-10-29: Prepaid credits are spent by a daily scheduled session ("Scheduled sessions", Krish's answer on
  who spends them). `docs/CREDITS-SESSION.md` is its playbook; it is not one of the seven jobs, so
  `automations.json` is unchanged.

- 2026-10-29: Concept-level approval, cadence and platforms (answers in this session to a ruling his
  "Growth engines alignment" session relayed).
  - "As long as I get enough of a look at the breadth of concepts, then yes, concept-level approval
    is fine." Recorded in AGENTS.md, "Concept-level approval".
  - Cadence: 5 a day per platform (not the 3 to 4 relayed).
  - Platforms: Instagram, TikTok and Facebook. Not YouTube or X for Heartside.
  - "Right now, just get this codex artwork produced to a high standard because this is going to set
    the tone for everything." The Codex card gained a pilot gate (one job, then review) and a
    compositing recipe.

- 2026-10-29: Krish's creative answers.
  - Breed examples: "go and get codex to build out all the assets, make sure you micromanage codex
    properly", with heartside's breed batch README. Stage 1 (6 paintings) is approved; stage 2 waits
    for review and his yes. Card: `docs/briefs/codex/2026-10-29-breed-examples-stage-1.md`; checker:
    `python3 growth.py examples check --stage 1`.
  - The morph: "a video of a realistic AI dog suddenly becoming the artwork could be cool, but
    that's just one creative idea." One hero concept may morph, ending on the real render.
  - Cadence: 5 posts a day per platform once the daily layer runs.
  - Shoppable product tags: handed to a heartside build session
    (`docs/briefs/2026-10-29-heartside-shopping-tags.md`).
  - Direction: `docs/briefs/2026-10-29-creative-direction.md`.

- 2026-10-29: Krish: "ok get going", approving the mandate heartside's session
  relayed: rebuild the rule checks on heartside's current NORTH_STAR, NOW, SCOPE
  and ECONOMICS; move image-making onto the current renders and Buddy; take the
  store handle and other never-publish items out of this public repository.
  - `growth.py` reads its rules from those files and `n8n/build.mjs`; Biscuit,
    exclamation marks, the worn lines and stacked fragments are refused.
  - Krish, the same day, asked whether purchase posts may sell the mug (the
    store recommends it; heartside's economics show it below the 30% floor),
    and chose "Allow equally": every gift may be sold, the mug included. The
    one-day block on mug purchase posts is removed.
  - No job file or `automations.json` entry changed.

- 2026-10-22: Ruling (Krish, 2026-10-22): each venture's own repository is
  the only reference for its status and plan; nowhere else holds a copy.
  - The engine no longer keeps a copy of heartside's state. `growth.py sync`
    stops writing `state/HEARTSIDE-NOW.md`, `state/heartside.json` and
    `local/state/HEARTSIDE-NOW.md` (and removes a leftover local one). It
    prints its reading and reads heartside's own `NOW.md` live; `growth.py
    now` reads it on its own. `NOW.md` is fresh when no commit other than a
    `docs(steward):` one landed on heartside's `main` after the latest
    commit that touched it. Unreadable or stale is unknown.
  - `local/state/heartside.json` keeps only the engine's input data: the
    commit, canon and rules fingerprints, the store and offers, which
    `check`, `readiness`, `render` and the Control Center report need. It no
    longer stores commits or pull requests.
  - The hourly `sync.yml` reads and fails on a rules change, as before, but
    commits nothing and needs only read access. The last copy is archived in
    `docs/history/2026-10-22-HEARTSIDE-NOW.md`.

- 2026-10-22: Krish approved the first weekly tool allocation and "approve"
  to letting the engine record prepaid credits as no new money (Ruling, Krish,
  2026-10-22: generation within prepaid credits, inside a weekly allocation he
  approved, counts as authorized).
  - `growth.py provider reserve` takes a prepaid request (`prepaid_credits`,
    `allocation`, `maximum_usd` 0) with `--credit-allowance`, bounded by that
    allocation's credits. `docs/PROVIDERS.md` shows the shape. The USD budget
    and its zero default are unchanged.

- 2026-10-21: Krish: "add a nice site favicon, social media cards, 11/10 GEO
  and AEO strategy, allow AI crawlers", then "create a recurring AEO blog
  strategy that is invisible to humans but very visible to Google and AI.
  These need to be discoverable."
  - `docs/GEO-AEO.md` is the strategy. Its blog is the Answers library:
    unlisted from the store's menu and gift journey, but public, the same for
    people and crawlers, and in the sitemap and `/llms.txt`. Hidden text and
    cloaking break Google's spam policies, so they're out.
  - A new eighth job, `jobs/answers.md` (Wednesday 07:30, kind `answers`),
    drafts two answers a week from `knowledge/aeo-question-bank.json`. The
    hosted runner builds the brief; publishing stays Krish's approval.
  - Batch 1 is in `docs/answers/2026-10-21-batch-1.md`.

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
  change, and a GitHub Action rewrote `state/HEARTSIDE-NOW.md` every hour
  (retired 2026-10-22: heartside's `NOW.md` is read live instead).
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
