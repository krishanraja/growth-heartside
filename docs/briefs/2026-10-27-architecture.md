# Plan: a bulletproof, sales-first architecture for the Heartside growth engine (Canva in)

Status: Proposed on 27 October 2026, awaiting Krish's approval. Nothing in it is built yet.
Brief: Krish's Claude Code brief of 27 Oct, the reference architecture and his growth corpus (Drive, Ventures/Temp).
The Cowork prompt for the Canva brand kit is [`2026-10-27-cowork-canva-brand-kit.md`](2026-10-27-cowork-canva-brand-kit.md).

## Context

Krish's brief of 27 Oct asks for an additive upgrade of `growth-heartside`. It follows the six rules of the reference architecture ("Growth engine reference architecture", Drive, 27 Oct), using his Perplexity growth corpus as best-practice reference. He also made Canva available to the engine at will with zero limits. His instruction this session: the engine is obsessed with as many sales as possible, as fast as possible, with as little paid media as possible. Lose nothing that has been built.

**Why now (live reads on 27 Oct)**
- The North Star number is not measured: U4, "attribution not wired" (`NOW.md`). The ladder asks for $200 this week, $2,431 by 16 Nov, $12,718 by 14 Dec and $25,000 by 28 Dec.
- Heartside's store made $24 in its trailing 28 days (Control Center, heartside `NOW.md`). There has been no real order through the V3 journey. PR #50's mug-proof guard is not deployed. The Christmas order-by date is unconfirmed.
- Code facts:
  - `cc` sends `schema_version: '1.0.0'` with no `stage`, so the plan, go-live and check-in loop of 19 Oct does not exist in code.
  - `organic_orders` is hard-coded as missing.
  - There is no discount-code registry and no order-level import.
  - Canva, Runway and Epidemic appear nowhere in the code.
  - Nothing can publish.
- Reading load: a daily-pack session reads about 135 KB of required reading, and about 300 KB when the canon changes. The target pack is 36 KB.
- Canva has a "Heartside" folder (`FAHXUgmLxDM`) holding the logo design and one draft, `DAHXUuWd95Y`. That draft carries the retired V2 "Annual Performance Review" direction and three misspellings ("Theat", "Biocuit", "maliman"). It is the first Canva failure on record. There is no Heartside brand kit and there are no brand templates.

**Krish's answers in this session** (to be recorded as rulings in `CHANGES.md` and the commit body)
1. The first signed run is **Creators + owned**: up to 20 gifted US creators with personal codes, plus send-first owned posts built in Canva for them to ride on.
2. Attribution uses a **read-only Shopify token** (custom app, `read_orders`) as a repo secret. The runner computes Tier 1 every day and stores aggregates only.
3. The engine drafts **all four tracking aids** (creator codes, post-family codes, a thank-you survey, per-post bio links). Krish switches each one on.
4. **The split:** Codex does content and social media management in the browser. Claude does orchestration, quality control and everything else. The Codex allowance has reset and is fully available, and the guard sits at 80%.
5. **Codex posts approved go-lives:** exactly the hash-matched payload, once, with the URL recorded. Approved comment-reply batches go out the same way. Codex never likes, follows or DMs. The engine code keeps no publish verb; only a go-live card can post.
6. **Knowing what works and what does not is critical, and it gets an owner.** That owner is the new `learn` specialist (section 3a). It owns the "what works" register, every verdict in it, and the input that register gives each next spec. Today nothing in the engine records a verdict, an amendment or a decline (register §D).

## What this moves on the North Star

- **It makes the number real.** Phase 1 turns "not measured" into a daily Tier 1 figure, so the U-rating stops being a guess.
- **It is the "one press" in the North Star.** The signed spec, plus a batched go-live, is the single approval that takes a winning format live.
- **It aims at the biggest lever before its window shuts.** Creator seeding has to happen before about 20 Nov.

## Corpus conflicts (canon wins, rule 2)

The corpus is used as reference; the canon overrides it in each of these places:
- The corpus lists V2 products (Annual Review, Body Double, Uniform set, Socks). V3 sells four gifts: mug $29, sherpa blanket $89, framed print $89, ornament $24 ($19 with another gift). Prices come from the sync, never from the corpus.
- The corpus proposes "draft order-by as 10 Dec". Heartside removed that promise on 23 Oct. A date appears only once Krish confirms it per product (rule 3).
- The corpus's "Your dog has notes" end card: the headline is retired in `RETIRED`, and the sign-off is undecided in heartside.
- The corpus names Biscuit. PR #21 renames the host to Buddy, so the host name is read from the canon and never hardcoded.

---

## 1. The run spec: the one thing Krish signs

**Two layers.** The protocol caps `exact_payload` at 8,000 characters, so a signed spec cannot carry every creative.
- **The campaign spec**, `specs/runs/<run_id>.json`, is signed at G1 as `stage:"plan"`.
  - `exact_payload` is the canonical spec, and `payload_sha256` is its SHA-256.
  - The wall is `spend`, with `amount_usd` set to the gift cap. Ad spend is always 0.
- **The weekly go-live manifest** is compiled from the spec and signed at G2 as `stage:"go_live"`, with `parent_proposal_id` set to the plan.
  - It holds the exact words, the media SHA-256s, the channel and the time for every item.
  - An amendment produces `amended_sha256`, and the engine uses Krish's version.

**Campaign spec fields**
- **Typed:** `additionalProperties:false` everywhere, so free-text "do not" lists are impossible. Every rule is an invariant (section 2).
- **Identity:**
  - `spec_version`, `run_id` (e.g. `xmas26`), `kind` (campaign | week | creator_batch | answers_batch | experiment) and `venture`;
  - `heartside_sha` and `engine_fingerprint`, both pinned at compile.
- **Window:** `{start, end, tz}`. North Star `rungs` are copied by the compiler from the `north-star-metric` block in `docs/NORTH_STAR.md`, never typed by hand.
- **What runs:**
  - `plays[]`: an enum of corpus plays P1 to P10;
  - `offers[]`: `{gift_id, unit_price}`, bound to the live catalog at compile by `offers.validate_item`;
  - `audiences[]`: an enum, e.g. self_owner, partner_giver, family_giver, friend_same_breed.
- **Creators:** `{cohort_max: 20, gift_units_max, gift_spend_cap_usd, seed_by: "2026-11-20", code_value, ids: [CR01..CR20]}`. Real handles stay in `local/lists/` (rule 6).
- **Slots:** `slots[]` hold a platform, format (reel | story | carousel | pin | still | answers_page | creator_note | reply_batch), lane (render | canva | higgsfield | runway | codex_browser), play, `send_to` (an enum: who the viewer forwards it to, D2), intent, per-day count and code family.
- **Experiments:** `experiments[]` hold `{id, hypothesis, variable (one), metric, min_reach_per_arm, readout}`.
- **Budgets:**
  - `higgsfield_credits` and `runway_credits` sit inside Krish's approved allocation (PR #12);
  - `canva` is `"unlimited"`, but its use is counted;
  - `usd_ads` is 0, always;
  - `codex_cards_max`, `claude_tokens_max` and `engine_minutes_max` are also set here.
- **Gates and success:**
  - `gates`: the plan date, the go-live batch dates, and `check_in_every_days: 2`;
  - `crew[]`: the specialists in play;
  - `success`: leading indicators with read-out times, and the outcome `tier1_net_sales_28d` against each rung.

**What makes it hold**
- `growth.py spec check|sha|propose` validates the spec against `specs/schema/run-spec.schema.json` with a stdlib validator. It reuses the strict validator pattern in `tests/test_protocol.py:38-72`.
- The spec never holds `status`, `pass` or `done`. A lint refuses those keys anywhere in specs, card results or packs.

## 2. Repo structure (additive; nothing moved without a byte-equal copy)

```
specs/schema/run-spec.schema.json   go-live-manifest.schema.json   card.schema.json
specs/runs/<run_id>.json            # signed campaign specs (public-safe: no handles, no customers)
crew/<name>/card.md  (<=3 KB)       crew/<name>/lens.md (<=1 KB)    crew/<name>/bar.json (Krish's amendments/declines)
invariants/invariants.json          # every rule as data: hashtag max, host-name source, AI-label platforms,
                                    # organic utm_medium set, attribution timezone, order-by needs confirmation ...
engine/spec.py  engine/status.py  engine/session.py  engine/cards.py  engine/golive.py
engine/attribution.py  engine/codes.py  engine/canva.py
engine/crew/{truth,design,motion,social,pins,creators,answers,store,radar,measure,learn,golive}.py   # lint() + check()
engine/learn.py                     # the "what works" register: verdict rules, explore/exploit, feeds spec compile
docs/learnings/WHAT-WORKS.md        # weekly public-safe digest, committed by an interactive session only
tests/test_regressions.py           # one test per register entry, named test_R##_<slug>
tests/test_spec.py test_crew_*.py test_session_pack.py test_cards.py test_attribution.py test_golive.py test_canva.py
docs/briefs/2026-10-27-architecture.md   # this plan, filed where the repo keeps briefs
docs/baseline/2026-10-27.json            # measured baseline (aggregates only)
knowledge/heartside-growth-corpus-2026-10.md  # Krish's corpus, byte-for-byte, + manifest entry + canon-conflict banner
```

**Existing pieces this plan reuses rather than rebuilds**
- Copy and pack lints: `growth.py:problems()` (547-622), `check_pack()` (625-696) and `freshness()` (699-729).
- Offers and assets: `engine/offers.py:validate_item` and `fresh_store`; `engine/assets.py:prepare()` as the single admission point for sources.
- Media: `engine/media.py:render()` and `verify()`.
- Providers: `engine/providers.py:reserve/transition/import_asset`.
- Ledger and insights: `engine/ledger.py` (`mark()` already requires HTTPS on the platform host) and `engine/insights.py:import_observation`.
- Protocol: `engine/protocol.py:run/build_report/bind_decisions`, `control_center.canonical` and `report_digest`.
- Tracking: `growth.py:tracked()` (205-217).

## 3. The crew: 12 specialists, each with code plus a small card

Lints run before acting and measured checks run after acting, both in code at zero tokens. Cards load only when that specialist is in the run's `crew[]`.

| Specialist | Owns | Lint before acting (blocks) | Measured check after acting | Lens: one question for the reviewer |
|---|---|---|---|---|
| truth | sync, catalog, canon, host name, order-by | sha fresh; catalog verified (a 429 means unverified); prices bound; host name from canon; any date needs a canon confirmation | canon or catalog drift since signing holds the run | "Is every fact on screen traceable to today's sync?" |
| design (Canva lane + renderer) | stills, carousels, Pins, covers, Stories, end cards | dimensions per format; product pixels only from approved assets (asset-id chain); Canva read-back text passes `problems()` plus a spellcheck; AI imagery flagged and labeled; brand fonts and colors | export manifest equals the go-live hash; amendment rate per lane | "Would Krish post this unchanged?" |
| motion | Higgsfield, Runway, Epidemic, Kokoro | motion only from a still Krish picked; reservation inside the allocation; Epidemic recording id and own-channel only | credits spent vs allocation (`providers` ledger) | "Does motion add send-worthiness the still lacks?" |
| social | IG, FB, TikTok Reels, Stories, carousels, reply batches | hook of 3 to 7 words in under 2 s; `send_to` set; at most 5 hashtags; gift phrase in the first sentence; AI-label flag; 1 CTA; UTM | sends per reach, watch time, profile taps and UTM sessions at 24 h, 72 h and 7 d | "Who exactly forwards this, and why?" |
| pins | Pinterest | "gift ideas" phrasing; title of 100 characters or fewer; 1000x1500; UTM | outbound clicks, saves | "Would a November gift-searcher save it?" |
| creators | 20 gifted US creators | cohort of 20 or fewer; one note per person citing their work; FTC line; code and UTM issued; inside the gift cap; before `seed_by`; product-verified flag | post rate (pass mark 8/20), disclosure within 48 h, Tier 1 orders per gifted unit, code-leak flag | "Is this note unmistakably for one person?" |
| answers | Answers/GEO, the Christmas dates page | short answer of 40 to 60 words; checked-on date; sources; facts equal the store | page sessions, AI referrals, Search Console clicks | "Could an answer engine quote line one?" |
| store | conversion recommendations | recommendation only; names the weak link in the persuasion chain | gift-query and zero-result signals ("not shown" when absent) | "Which link in the chain does this fix?" |
| radar | trends, comments | `SAD` and mockery regexes; no repost without written rights; escalations | Trial Reel outcome of radar hooks | "Does this fit the affectionate voice?" |
| measure | facts: attribution, observations, ladder | every link and code registered; observation JSON carries source URL, `observed_at` and screenshot path | Tier 1, 2 and 3; trailing 28 d vs rung; leak flags; observation coverage per live post | "Is the number derived, or asserted?" |
| **learn (owner of what works)** | verdicts: the "what works" register, scale/iterate/hold/kill, explore vs exploit, feeding the next spec | every spec slot cites the register as `exploit:<entry>` or `explore:<entry>` with a pre-registered single-variable experiment; the mix stays near 70/20/10; repeating a `doesnt` pattern is refused unless the slot names what changed | verdicts recomputed at every read-out (24 h, 72 h, 7 d); exploit hit rate vs explore hit rate; hours from first signal to a scale proposal (target 24 or fewer) | "What would have to be true for this verdict to be wrong, and is that measured?" |
| golive (Codex browser) | posting approved items | decision approved; `payload_sha256` or `amended_sha256` matches; once-only ledger; channel matches | published URL recorded; live caption read back and hash-compared | "Is what went live byte-identical to what was approved?" |

**The creative bar.** Every amendment or decline Krish makes in Control Center appends to `crew/<name>/bar.json` (committed; no customer data). `learn` also reads each one as evidence. This closes register #7 and §D: no amendment or decline is recorded today.

### 3a. `learn`: the owner of knowing what works

**Division of labour.**
- `measure` produces facts.
- `learn` turns facts into verdicts and decides what the next spec does with them.
- Claude, as orchestrator, is accountable for the register in every session.
- Codex supplies the platform readings through social cards. Claude spot-checks those readings against their screenshots before they count.

**Register entries.** Each lives in a `learnings` table in `local/engine.sqlite3` and is checkpointed by `state_store`. Fields:
- `subject`: the kind is one of hook, format, play, lane, channel, `send_to`, audience, offer, creator cohort, copy pattern or time slot, plus a ref;
- `verdict`: works, doesnt, inconclusive or untested;
- `evidence[]`: each item is `{metric, value, baseline, n, window, source}`;
- `rule_id`, which names the rule that produced the verdict;
- `since` and `revisit_when`.

Verdicts are computed and never hand-written: a schema lint refuses any `verdict` without a `rule_id` and evidence. The rules come from the existing `jobs/report.md` and `engine/insights.py` and the corpus §5 and §8 decision tables:
- **Works:**
  - sessions per 1,000 reach at least 1.5 times the 14-day rolling median;
  - or Tier 1 orders at a worthwhile margin;
  - or, as an early signal, sends per reach in Heartside's own top quartile, once it has 20 posts.
- **Doesnt:** three clearly different hooks fail. A Krish decline records "doesnt for Krish", with his reason.
- **Inconclusive:** below the minimum sample (1,000 reach per arm), or a week-on-week Tier 1 change under about 10 orders.
- **Never:** conversion-rate comparisons at these volumes.
- **Carried over:** `insights` refuses to name a winner from one post and requires two comparable peers.

**What it drives.**
- The `spec compile` step reads the register. Exploit slots multiply the `works` entries: within 24 hours of a winner, 5 hooks, 3 audience versions, a carousel, a Pin and a proof block (`jobs/report.md`). Explore slots test `untested` entries.
- Every G3 check-in packet opens with "What works / what does not since the last check-in", taken from the register.
- The Sunday report becomes `learn`'s weekly output. An interactive session then commits a public-safe digest, `docs/learnings/WHAT-WORKS.md`, with aggregates only and creators by anonymous id. Scheduled runs never commit (rule 9).
- The session pack carries the top `works` and `doesnt` entries, at 3 KB or less.

**Its own scorecard.** Did the spec's exploit slots beat its explore slots? How many hours passed from signal to proposal? How much of what is live is measured (posts with all three read-outs)? A post that is never measured counts against `learn`, not as neutral.

## 4. Checks mapped to this repo's failure history

The register holds 60 entries from git, `CHANGES.md`, `docs/` and the PRs. Each becomes `test_R##`.

**Phase 0 first closes the seven that are written rules only:**

| # | Failure | New test or invariant |
|---|---|---|
| R07 | The "stacked two-word lines" correction was lost when the copy was deleted; the checker still models "Not sorry." | Stacked-fragment detector; the self-test example replaced |
| R11 | Biscuit → Buddy (PR #21) | Host name read from synced canon; `Biscuit:` prefix logic follows the canon |
| R17 | The PLAYBOOK hook matches the retired regex | A test runs every PLAYBOOK and COPY-DOCTRINE example through `problems()` |
| R18 | COPY-DOCTRINE §10.8 contradicts rule 5 | Doctrine statements are checked against `invariants.json` |
| R34 | Sends 1.0.0 while the docs claim 1.2.0 | The constant and the doc claim are checked to agree; a 1.x directive fixture |
| R35 | A second same-day dispatch collides on run id (409) | Run id includes the attempt; test for the collision |
| R52 | Autonomy is not built | Tests: an approved plan never goes live; amended text is used; a declined check-in stops the plan; one ask at a time (R54) |

**It then adds coverage for gates that exist in code but have no test:**
- `SLOP`, platform `LIMITS`, venture, real date, headline em dash, the 40-item cap, id/platform and id/date mismatch;
- the layout and asset allowlists, scene timing, narration provenance, stale quotes, purchase gating and the `sync` 429 path.

**New entries from this session:**
- **R61:** the Canva V2 draft with typos. Read-back lint and quarantine.
- **R62:** the corpus's V2 products and order-by date. A price or date may be drafted only if it traces to truth.
- **R63:** the numbers job's own checkpoints (15 orders by 1 Nov…) versus the North Star ladder. Rungs come only from `NORTH_STAR.md`.
- **R64:** the Reddit conflict between PLAYBOOK and GEO. Default to listening only.
- **R65:** timezones (London ledger, New York scheduler, Shopify in GMT). Attribution windows are explicit UTC boundaries, and the zone is printed.
- **R66:** the last four `check.yml` runs (24 to 27 Oct) took about 23.5 minutes each, against a 59-second median over all 127 runs. Find the cause and fix it.
- **R44:** Windows portability. Add a `windows-latest` self-test job.
- **R67:** nothing records what works. There are no verdicts, no amendments and no declines (register §D), and the Sunday report's calls live only in packs. Tests:
  - a verdict without `rule_id` and evidence is refused;
  - a decline becomes a `doesnt` entry;
  - a spec slot without an `exploit:` or `explore:` citation is refused;
  - a live post missing a read-out lowers `learn`'s coverage score.

**Architecture tests**
- A run executes only at its pinned `engine_fingerprint`, a hash of `growth.py` and `engine/`. New capability lands between runs and is used by the next run.
- No `.py` file under `specs/` or `local/cards/`; no engine module mentions a `run_id` literal; content and social cards cannot write to `engine/` or `growth.py`.
- No HTTP to any platform host anywhere in `engine/`. Only `golive.py` emits a posting card.
- A `status`, `pass` or `done` key is refused everywhere.
- The self-test rule "automations never ask to post" allows exactly one named go-live automation, whose prompt calls `growth.py golive next`.

## 5. Session protocol

**The session pack.** `growth.py session <run_id> --role orchestrator|reviewer|codex` prints a pack of 36,864 bytes or less. A test enforces the cap. Contents:

| Part | Size |
|---|---|
| Engine core card (rules that never bend, authority, roles) | ≤4 KB |
| Spec | ≤8 KB |
| In-play crew cards | ≤3 KB each |
| Open lint findings | ≤4 KB |
| Gate status and last measurements | ≤4 KB |
| Truth digest (sha, catalog table, changed-canon list, heartside NOW freshness verdict) | ≤4 KB |
| Latest creative-bar entries | ≤2 KB |
| `learn` register: top works and doesnt entries, plus open read-outs | ≤3 KB |

- A canon change ends the session at a gate packet, which keeps the existing STOP path.
- `AGENTS.md` (25 KB, auto-loaded) is slimmed to 10 KB or less. Its long sections move byte-for-byte to `docs/OPERATING-BRIEF.md`. A test checks that every moved heading exists there, so nothing is lost. The harness canon block is untouched.

**Budgets**, logged to `local/runs/<id>/clock.jsonl` with engine time and Krish-wait time kept separate:

| Session | Tokens | Wall-clock | Calls |
|---|---|---|---|
| Orchestrator | ≤150k | ≤40 min | ≤60 |
| Reviewer | ≤60k | ≤15 min | n/a |
| Codex card | n/a | ≤30 min | ≤80 browser actions |

**No mid-turn questions.** Questions append to `local/runs/<id>/gate-questions.jsonl`, and the session ends. Each run has three gate types only:
- **G1 plan:** the spec, behind `spend` (the gift cap);
- **G2 go-live:** a weekly batch, behind `post`;
- **G3 check-in:** every other day and after the first results, behind `strategy`. It opens with `learn`'s "what works / what does not".

Control Center already shows one walled ask at a time.

**Readiness is computed, never written.** `growth.py status <run_id>` combines:
- lint results;
- a reviewer verdict, where `reviewer` must differ from `producer` (Codex produces and Claude reviews; for Claude-built code, a fresh reviewer gets only the lens and the diff);
- the Control Center decision digest;
- the measured checks.

## 6. Codex task cards

**Kinds:**
- **content:** a Canva build, a Higgsfield or Runway generation inside the allocation, or creative assembly;
- **social:** read insights and comments, then write aggregate observation JSON for `insights import`;
- **golive:** post an approved payload;
- **baseline:** a one-off, read-only aggregate of local Codex and Claude logs;
- **code:** rare. Claude builds the engine by default.

**Card fields** (`specs/schema/card.schema.json`, 6 KB or less, Claude writes it):
- pinned `model` and `effort` (default `gpt-6.1-sol` / medium; never the account default);
- `max_minutes`, `max_calls`, `cwd`, and `write_allow` globs (e.g. `local/cards/<id>/**`);
- at most 5 read files;
- `never[]`: no git, no new dependencies, no edits outside `write_allow`, no likes, follows or DMs, and no posting unless `kind: golive` with a verified decision;
- the interface verbatim, `acceptance[]` commands that must exit 0, and the JSON return shape.

**Dispatch:**
- Content, social and go-live cards run in a Codex app automation, "Heartside cards", which needs network and the signed-in browser. It calls `growth.py card next`, executes one card and ends.
- Code cards use the reference route: `codex-companion.mjs task --background --fresh --write --model --effort --cwd <worktree>`, with a worktree per card.
- A run executes from a worktree at its pinned engine commit, with `local/` shared through `HEARTSIDE_LOCAL_DIR`.

**Allowance guard.** Each card's first step reads the Codex usage page and records the percentage with a screenshot path. `growth.py card next` refuses at more than 80% unless a Control Center spend decision id is attached.

**Verification.** `growth.py card verify <id>`, run by Claude outside the sandbox:
- re-runs `acceptance[]`;
- refuses any file outside `write_allow`;
- validates the return JSON;
- admits media only through `canva admit`, `provider import` or `render`.

Codex's own report is never evidence.

## 7. Tool routing (Control Center placements, 26 Oct, plus today's Canva ruling)

| Tool | Heartside use | Rule |
|---|---|---|
| Canva (at will, unlimited; Krish 27 Oct) | Main lane for stills, carousels, Pins, Stories, covers, end cards, creator brief one-pagers, the Christmas dates graphic | Claude builds masters between runs (MCP: `create-design`, `create-brand-template-draft`, `copy-design`, `edit-design`, `resize-design`, `export-design`) in `Heartside/Engine masters`. Codex fills them per run. Claude QCs with `read-design` text read-back plus element asset ids, and exports. Canva AI images are for dogs and rooms only, labeled, never the product. Autofill is unverified (no templates; the help lookup lacked scope), so phase 2 probes it, with copy-and-edit as the fallback. The placement lists no Heartside yet: Krish adds it in Control Center (this engine never works there) |
| Higgsfield (main) | Fictional dog and room stills, then motion | Stills before motion; 2.75 credits per still, 210 per Seedance clip; inside the approved allocation (PR #12) |
| Runway (main) | Reframe, upscale, one costed prototype | As in the 22 Oct brief, with the V2 direction replaced by V3 |
| Epidemic Sound (main) | Music and effects | Own channels only, never ads; recording id stored with the asset |
| Kokoro (local) | Narration drafts | Unchanged |
| Shopify | Attribution via the read-only token (runner) and MCP (spot checks) | Aggregates only; never order ids, names or emails |
| Control Center | Gates, decisions, venture state | Protocol only |
| HeyGen, ElevenLabs | Not for Heartside | They hold Krish's clones (Mindmake/publication) |
| Buffer, Apify | Not used | Posting is by Codex in the browser; Apify is unplaced for Heartside |

## 8. Phased build: sales first, never building mid-run

Today is Tue 27 Oct. Each phase lands as its own PR on `claude/canva-integration-plan-cpy1p2` (then the PRs Krish names), green on `--self-test` and `unittest`.

**Phase 0, 27–28 Oct (Claude). Lose nothing, plus the baseline.**
- Steps:
  - file this plan and the corpus (byte-for-byte, with a manifest entry and a conflict banner);
  - add `test_R##` for R07, R11, R17, R18, R34, R35 and R52, fixing the drift each one exposes;
  - bring PR #21 up to date on the synced canon (Krish merges);
  - write `docs/baseline/2026-10-27.json` from Actions (325 runs), git and PR cycle times, and reading bytes;
  - issue Codex card C0 for the local token and time aggregates;
  - **build the Canva brand kit (Krish 27 Oct):** a Cowork session on Krish's PC uses computer use to build the "Heartside" Brand Kit in Canva from the assets in his H: drive Ventures folder. The ready-to-paste prompt is filed at `docs/briefs/2026-10-27-cowork-canva-brand-kit.md`. Krish opens the folder and signs in to Canva. Claude then verifies the kit (`list-brand-kits`, the receipt's SHA-256s matched against heartside's approved assets) before any master uses it.
- Accept: suites green; the baseline file names its sources; PRs #21 and #22 are untouched or brought current, never closed.

**Phase 1, 28–30 Oct (Claude). Attribution, spec and stages.**
- `engine/attribution.py`:
  - pages Shopify `orders` in UTC windows;
  - reads `customerJourneySummary.{first,last}Visit.utmParameters` and `discountCodes`, with net sales = subtotal − discounts − refunds;
  - assigns Tier 1 (registered `utm_content` or a registered code, de-duplicated by order), Tier 2 (survey) and Tier 3 (the rest);
  - computes trailing 28 days against each rung.
- It emits the aggregate envelope only, extending `ledger.normalize_report` with an `organic` scope. It feeds `protocol.organic_orders` and a new `organic_net_sales_28d`.
- `engine.yml` runs it daily with the read-only Shopify token from repository secrets.
- `engine/codes.py` drafts the creator codes (CR01–CR20), the post-family codes, the survey and the bio-link packet for Krish.
- The spec validator and `spec propose`.
- `engine/learn.py` with the register schema and verdict rules (porting `insights.decisions` and the `jobs/report.md` thresholds), plus the slot-citation lint. The first spec therefore declares every slot as explore or exploit. With no data yet, every slot is `explore` with a pre-registered experiment.
- Protocol 1.2.0: `stage`, `parent_proposal_id`, `amended_sha256` and one ask at a time, proved on the local stand-in (GET-GOING Step 1).
- Accept: fixture tests; one live read printing a real Tier 1 figure (even $0) with its window and source; `NOW.md` north-star-state set to the measured value.

**Phase 2, 29 Oct–5 Nov (Claude builds; Codex proves). Crew, pack, Canva lane, cards, go-live.**
- Crew lints and checks, with cards and lenses for the run-1 crew: truth, design, social, pins, creators, measure, learn, golive.
- Codex social cards read insights at 24 h, 72 h and 7 d after each go-live, then run `insights import`. `learn` recomputes verdicts, and Claude spot-checks the readings against their screenshots.
- `growth.py session` with the 36 KB cap.
- `engine/canva.py`, through `canva admit <card>`:
  - takes the export file, `design_id`, read-back text and element asset ids;
  - admits them through an extended `assets.prepare` and a `canva` provider entry;
  - adds a `render()` branch for finished stills, carousels and Pins.
- `engine/cards.py` with the allowance guard.
- `engine/golive.py`: `golive next` builds a posting card only for an approved, hash-matched decision; `golive confirm` uses `ledger.mark` and the live-caption read-back.
- `BROWSER.md` and `AGENTS.md` record today's ruling.
- Accept: one Canva master filled by Codex, admitted, QC'd and exported; one synthetic go-live end to end on the stand-in.

**Phase 3, from 29 Oct: run `xmas26`, creators + owned.**
- **G1** spec (target Thu 29 Oct).
- **Creators:** Codex builds the shortlist; Codex drafts the notes and Claude QCs them; Krish sends the notes and orders the gifts inside the cap. Gifts go to creators **only after heartside's first verified order**, with seeding by 20 Nov.
- **Owned posts:**
  - week 1 uses the current renderer route, so the fallback keeps running;
  - from week 2, the Canva lane: send-first Reels and Pins, P3 Trial Reels where eligible, and the Christmas dates post once dates are confirmed.
- **G2** go-live batches weekly; Codex posts them.
- **G3** every other day.
- Accept:
  - the first go-live posted byte-identical to the approval;
  - Tier 1 measured against the 2 Nov ($728) and 9 Nov ($1,417) rungs;
  - every live post has its 24 h, 72 h and 7 d read-outs in the register;
  - the week-2 spec's exploit slots are compiled from week-1 verdicts.

**Phase 4, between weekly runs in Nov.**
- The remaining crew (answers, store, radar, motion).
- All 67 register entries mapped to tests.
- The Windows CI job and the CI-time fix.
- Job files turned into thin wrappers over specs.
- `AGENTS.md` slimmed.
- The current daily pack is retired from the default route only after two weekly runs prove the new one. It is never deleted.

**The 20x target, measured against the phase 0 baseline**
- **The unit:** a Krish-approved, go-live-ready creative.
- **Cost:** tokens per unit. Context falls from about 135 KB to 36 KB or less (about 3.75x). Calls per unit must fall by at least 5.3x, through code lints, no mid-run building and no retries.
- **Time:** engine wall-clock from the signed spec to the go-live packet, reported separately from Krish's wait.
- **Honesty:** if the baseline denominator is zero (no approved creative to date), the plan says so and uses "creative proposed to Krish" from the 17 Oct library and the packs since.

## Gate 0: only Krish can do these (batched)

1. Add a Shopify custom-app token with `read_orders` only as a repository secret.
2. Set up the Codex app automation "Heartside cards": network and signed-in browser, with Canva reachable in the browser or through its MCP. Allow card C0 to read local Codex and Claude logs for aggregates.
3. Heartside dependencies that gate creator gifts and buy-intent posts:
   - deploy PR #50;
   - make the first verified order;
   - confirm the Christmas order-by per product.
4. At G1: the gift cap and code value (amendable in Control Center).
5. Add Heartside to Canva's placement in Control Center.
5a. For the brand kit Cowork session (`2026-10-27-cowork-canva-brand-kit.md`): open the Heartside assets folder on H:, sign in to Canva, paste the prompt, and give its one-word yes on the keep/skip table.
6. Merge PR #21 once the synced canon names Buddy.
7. Switch on the drafted codes, survey and bio links.

## Verification (verification-loop after each phase)

**Deterministic**
- `python3 growth.py --self-test`
- `python3 -m unittest discover -s tests -v`
- `python3 growth.py spec check specs/runs/xmas26.json`
- `python3 growth.py session xmas26 | wc -c` must be 36,864 or less
- `growth.py card verify <id>`
- `check.yml` green on Linux and Windows

**Live**
- An attribution read with its window, source and Tier counts (no customer fields).
- A Control Center synthetic run with `plan`, then `go_live`, then `check_in`, read back by digest.
- `canva admit` on a real export, checking the read-back text, the asset-id chain and the SHA-256.
- The first go-live live caption hash-compared to the approval.
- A `learn` register read-back: every live post carries evidence and a rule id, and the G3 packet's "what works" lines trace to register entries.

**Reporting.** Verified results are reported separately from inferred ones. The close-out updates `NOW.md`, with a North Star check line.

## The call

Build phases 0 and 1 now. They make the number real and give Krish one press to sign `xmas26` by Thursday. Then run creators and owned posts while phase 2 lands between weekly runs.

- **Sharper alternative:** skip the Canva masters in week 1 and put every hour into the creator cohort and codes. That trades owned-post polish for the biggest lever's deadline.
- **Owner of what works:** `learn` from the first spec onward. Every slot is explore or exploit, and every live post is measured or counted against it.
- **Next 24 to 72 hours:**
  - Phase 0 PR (Wed);
  - Phase 1 PR plus the token (Thu);
  - the G1 spec on Krish's list (Thu or Fri).
- **Counterpoints:**
  - Creator gifts depend on heartside's first verified order. If that slips past about 6 Nov, seeding misses Christmas, and the week-2 owned posts carry the ladder alone.
  - Codex posting widens what the engine can do. One wrong post costs more than a week of hand-posting, which is why posting stays hash-bound and read back.
