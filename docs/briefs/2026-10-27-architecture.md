# Plan v3: a bulletproof, sales-first architecture for the Heartside growth engine

**Status.** Proposed on 27 Oct 2026 for Krish's approval. Nothing in it is built.

**How it was checked:**
- **v1** went through a six-lens adversarial review: 82 agents. Of 91 findings, 84 survived a skeptic and 7 were refuted. A completeness critic added 21 (K00 to K20).
- **v2** answered all of them. A second pass over v2 (6 agents) then found 126 gaps, 9 of them blocking. Most came from mechanisms v2 itself had added:
  - Buffer posting from public Actions;
  - claims held in a checkpoint;
  - artifact uploads from the PC;
  - per-child commit pinning;
  - media hosted in a folder anyone with the link can edit.
- **v3 removes those mechanisms** instead of patching them, and is simpler for it.
- **A blocking-only third pass** (3 agents) found 22 more, B00 to B21. All are fixed here.
- **Krish's call on the public repo:** "leave it for now as is". So nothing private goes to GitHub, and the tactics that need private state run as PC-local drafts until he chooses a home for it (Gate 0, item 14).
- **Appendix B** maps every finding: C00 to C83, K00 to K20, G00 to G125 and B00 to B21.

## Context

Krish's brief of 27 Oct asks for an additive upgrade of `growth-heartside`. It follows the reference architecture's six rules (Drive, 27 Oct) and uses his growth corpus as reference. Canva is available to the engine at will. His standing instruction: as many sales as possible, as fast as possible, with as little paid media as possible. Lose nothing that has been built.

**Live state, read 27 Oct:**
- **The North Star number is not measured.** NOW.md rates it U4, "attribution not wired". The ladder: $728 (2 Nov), $1,417 (9 Nov), $2,431 (16 Nov), $12,718 (14 Dec), $25,000 (28 Dec).
- **The store has barely sold.** Heartside made $24 in the trailing 28 days (as of 23 Oct). No real order has gone through the V3 journey.
- **PR #50, the mug print-proof guard, is merged but not deployed.**
- **The storefront is locked, deliberately.** Every heartside.io path redirects (302) to `/password`, "Opening soon", and `/products.json` returns 401 (13:17 and 14:03 UTC). Krish, 27 Oct: "Deliberate, until PR #50". No post can sell until it reopens.
- **Code:**
  - `cc` sends `schema_version '1.0.0'` with no `stage`;
  - `organic_orders` is hard-coded as missing;
  - there is no code registry and no order-level import;
  - nothing publishes;
  - there is no Canva, Runway or Epidemic code;
  - a per-creative post-proposal loop exists (`protocol.post_proposals`).
- **Reading load.** A daily-pack session loads about 135 KB of required reading, and about 300 KB when the canon changes.
- **Canva:**
  - no Heartside brand kit and no brand templates;
  - a Heartside folder holding a logo design ("heartside 2022 est.") and one retired V2 draft with three misspellings.
- **Buffer** is connected to Instagram `yourdoghasnotes` (business), the Facebook page and TikTok `yourdoghasnotes` (account created 24 Oct). Buffer's API takes media by URL only.
- **Google Analytics.** GA4 `G-DTVJ5QESKX` is on the site. Control Center sees GA, but nothing it exposes to the engine carries GA data: not the directive, not decisions, not the MCP tools, not the API gateway.
- **Drive.** The Heartside folder `1QInHx…` and its parent "Active Ventures" are both shared "anyone with the link can edit". The folder id is also public through heartside's `docs/SYNC.md`. There is no Growth folder yet.
- **The repo is public.** Its Actions artifacts, including the engine checkpoint, can be downloaded by any signed-in GitHub user.
- **CI.** The last four `check.yml` runs took about 23.5 minutes each, against a 59-second median over 127 runs.

**Which part of the North Star this moves:**
- The number itself, which phase 1 makes measurable.
- "Every winning format found by this engine and approved by Krish in one press": a signed campaign plus a daily go-live batch is that press.
- The creator lever, before its window shuts: gifts must ship by about 20 Nov.

**One reconciliation for Krish (K03).** This proposes a decision, not a change to either number. This repo's organic-only ladder is higher than heartside's whole-store ladder every week:

| Date | This repo (organic only) | Heartside (whole store) |
|---|---|---|
| 16 Nov | $2,431 | $1,624 |
| 14 Dec | $12,718 | $5,612 |
| 28 Dec | $25,000 | $9,312 |

Organic sales are a subset of all sales, so one ladder is miscalibrated. NOW.md's check line becomes "recalibration proposed" until Krish rules.

## Krish's rulings (27 Oct)

Each is recorded in phase 0, before anything relies on it, in CHANGES.md and as a `Ruling` line in the commit body. The third column names the text it changes.

| # | Ruling | Texts it changes |
|---|---|---|
| R-1 | **Creators plus owned:** "up to 20 gifted US creators with personal codes, plus daily send-first Reels, carousels and Pins built in Canva" (Krish's words). The engine's proposal to cut Reels with the renderer or motion tools, with Canva covers, cards and end cards, appears **only as a G1 departure**, for Krish to approve or amend. If he declines it, Reels are built in Canva (B20). Pins need Pinterest business connected to Buffer (Gate 0) | none |
| R-2 | **Attribution through a read-only Shopify token.** Shopify no longer allows new admin-created custom apps, so this is a Dev Dashboard app with `read_orders` only and client credentials (a 24-hour token). The runner computes Tier 1 daily on Actions. Aggregates only | none |
| R-3 | The engine **drafts creator codes, post-family codes, a thank-you survey and per-post bio links**, and Krish switches each one on | none |
| R-4 | **Codex does content and social management in the browser. Claude does orchestration, quality control and everything else, engine code included.** The Codex allowance is "reset, fully available" | none |
| R-5 | **Codex posts approved go-lives:** exactly the hash-matched payload, once, recording the URL. Approved reply and comment batches go out the same way. Never likes, follows or DMs | Rule 1 exception: AGENTS.md (Autonomy, rule 1), BROWSER.md |
| R-6 | **Knowing what works** is owned by `learn` | none |
| R-7 | **Everything the engine produces is filed in Drive `Heartside/Growth`**, easy to find, with no sprawl, owned by `librarian` | Rule 9: one sanctioned writer outside `local/` |
| R-8 | **H: is Google Drive for desktop:** `H:\…\Active Ventures\Heartside` is folder `1QInHx…` | fact, not a rule change |
| R-9 | **Creator names may live in `Growth/04_Creators/_private`**: the shortlist and the name-to-id key only, owner-only | Rule 6 exception, `docs/CREATORS.md`, `jobs/creators.md` |
| R-10 | **GA is part of `measure`, read from Control Center** | none (brief to Control Center) |
| R-11 | **An `audience` specialist grows Heartside's accounts relentlessly.** After approved batches it may: edit profiles, comment on others' posts (at most 10 a day, each written for that post), make collab posts on any platform that offers them, and reshare with rights. Until the state home is chosen, everything except profile edits runs PC-local, with Krish acting by hand | Rules 1 and 7; **BROWSER.md lines 13-24**; and AGENTS.md Autonomy's "Nothing else widens", amended to name exactly these verbs, only as items of an approved, hash-matched batch: edit the profile, bio, link, highlights and pinned posts; comment on others' posts (10 a day or fewer, each written for that post); start a collab on Heartside's own post, or accept one from a creator at "agreed"; reshare with a rights record. Follow, like, DM, accepting terms and signing in stay barred. The automations rule names "Heartside cards" as the one automation that may take approved go-lives live (B19) |
| R-12 | **Buffer first.** The Codex go-live card posts the exact approved words through Buffer. The browser is used only where Buffer cannot post the format | BROWSER.md |
| R-13 | **"Deliberate, until PR #50"** (Krish's words). Heartside's own next action, check a fresh mug chat and cart, is attributed to heartside's NOW.md | none |
| R-14 | **Growth inherits the Heartside folder's link sharing.** Only `_private` is locked down | none |
| R-15 | **Creators order their own gift** with a one-time code worth one gift, through the chat. Those orders never count as organic sales | `docs/CREATORS.md` |

**Also recorded:**
- **Canva is available to the engine "at will with zero limits".** No placement decision is asked of Krish, because an unplaced tool stays usable (G84).
- **Texts that the rulings make false are amended in phase 0:**
  - README.md:10;
  - PLAYBOOK.md:414;
  - `jobs/creators.md`:46-47;
  - `automations.json` `_about` and `run_in`;
  - `engine.yml`'s "No social publishing" strings;
  - AGENTS.md's "create the automations", "Files this engine keeps" and "Changing the engine": "seven" becomes eight, and the Codex and PC automations are added (G35, G76, G113, G125).

**Corpus vs canon (the canon wins, rule 2).** These corpus items are out:
- the V2 products;
- the "10 Dec order-by";
- the "Your dog has notes" end card.

The host's name is read from the canon. PR #21 is not touched, but Gate 0 tells Krish it conflicts with R11 and would reintroduce hardcoded host checks (G23).

## 0. Lose nothing: what stays

- **Jobs:** the 8 jobs in `automations.json` and their `jobs/*.md` files.
- **Workflows:** 8, namely engine (every 15 min), sync (hourly), control-center, check, docs-steward, harness-repository-context, handoff and reporting-access.
- **Code and tests:** `growth.py` and the 18 `engine/` modules; 86 unit tests and 134 self-test checks.
- **Creative:** campaigns C90–C96, 28 hooks, the fictional Biscuit asset.
- **Knowledge and published work:** `knowledge/`, and Answers batch 1.
- **Control Center:** the loop, and the per-creative post-proposal loop.
- **Open PRs:** #21 and #22.
- **Receipts:** the 17 Oct verification JSON and HANDOFF.

**The register.** The 60-entry failure register is filed at `docs/REGISTER.md` (27 Oct). Its numbers 1 to 60 are R01 to R60, and new entries take R61 onward (G08, G107).

**AGENTS.md stays whole**, with the amendments above. Nothing moves out of it (G17, G26, G27, G38, G67, G97, G125).

The current daily-pack route keeps running until two weekly runs prove the new one. Nothing is deleted.

## 1. Runs, specs and gates

### G1: the campaign, signed once

- **Proposal:** `heartside:plan:xmas26`, `kind: prepared`, `stage: "plan"`, wall `spend`. `amount_usd` is the gift cap. `channel` is "creators+owned". `close_condition` is `campaign_closed` (G112).
- **`exact_payload`** is readable text (8,000 characters or fewer): the plan in plain lines, the departures Krish must know about, and a final `Binding: <sha256>` line naming the canonical JSON spec, `specs/runs/xmas26.json`.
  - `payload_sha256` is the SHA-256 of that text.
  - An interactive session commits the JSON spec once its digest equals the approved binding.
- **What the spec holds:** `window`; `plays[]` (P1 to P10); `audiences[]`; `offers[]` as **gift ids and canon prices at the synced sha**; creator caps; budgets; `success`.
  - Offers are bound to the live catalog only per go-live item, so G1 can be signed while the store is locked (G86).
  - `success` holds the North Star rungs (copied from `docs/NORTH_STAR.md`) and **heartside's canon checkpoints, read live**. Each series is measured only against its own targets, with a test (C27, G21).
  - The spec is typed (`additionalProperties:false`), with no free-text "do not" lists.
- **Departures stated in G1:**
  - W44 and W45 run on the current route;
  - Reels come from the renderer, with Canva cards;
  - about 50 go-live asks instead of the reference's "two or three gates";
  - Pins wait on Pinterest business.

**Budgets:**
- `paid_ads_usd` is 0. Anything non-zero needs Krish's separate spend approval, and those creatives are excluded from organic (K04).
- `higgsfield_credits` and `runway_credits`: this spec **proposes** the allocation, stills before motion (GET-GOING Step 0.5 folds in; PR #12 covered one week only) (C09).
- `canva`: unlimited, counted.
- `codex_cards_max`, `claude_tokens_max`, `engine_minutes_max`.
- `krish_minutes`: at most 20 a day and 30 on Sunday, **with the daily pack counted** (C50, G45, G104).
- `backlog_threshold`: Teeinblue orders waiting for his check (K12).

**Creators:**
- `gift_code`: per creator, opaque and random, single use, once per customer, a **fixed amount equal to one eligible gift's price, applied once per order**, expiring at `seed_by` (G42).
- The audience-code value comes from a synced heartside canon decision, never from this spec (K10, G105).
- `seed_by` is 2026-11-20 and `cohort_max` is 20.

**audience:** follower targets per platform, `tactics_enabled[]`, and `comment_daily_max` (5 in week 1, then up to 10 while Account Status stays clean).

### Weekly runs (`kind: week`, one per ISO week, America/New_York)

ISO weeks come from `isocalendar()`. 2026 has 53 weeks, and W53 runs 28 Dec–3 Jan (G108).

- **Compiling.** At the start of a run's production window, `spec compile` runs in `engine.yml` on main. It writes a `child_runs` row (engine state): the spec JSON, its digest, and the main commit it was compiled at. Child specs are not tracked files, because rule 9 forbids scheduled writers from writing them (G04).
- **Immutability, not commit pinning** (reference rule 5; C00, C55, G49, G94, G121):
  - Every compiled item (render, export, caption, payload text, binding) is stored by SHA-256 when compiled.
  - Later engine changes on main cannot alter it, because `cc` relays the stored payload text and recomputes nothing from code (with a test).
  - New capability applies from the next compile.
  - CI refuses a PR that changes `engine/` or `growth.py` together with `specs/runs/` or run outputs.
  - Production cards cannot write `engine/`.
  - No worktrees and no `HEARTSIDE_LOCAL_DIR`: the PC runs in the main checkout, as AGENTS.md says (C21, G125).
- **W44** (26 Oct–1 Nov) precedes G1, so it is not a run. It is the current daily pack (G94).
- **W45** (2–8 Nov) is the first week run if G1 is approved by 2 Nov, on the current route (renderer, daily pack, Krish hand-posts).
- **W46** (9–15 Nov) is the first run with the Canva lane, Codex and Buffer go-lives, and card read-outs.

### G2: one go-live ask, kept current (C02, C19, C36, C47, C59, G05, G33, G34, G55, G89, G90, G100, G112, G117, G122, G123)

- **Ids and the one-ask rule.** `heartside:golive:xmas26-<seq>`, `kind: prepared`, `stage: go_live`, `parent_proposal_id` `heartside:plan:xmas26`, wall `post`, `channel` "buffer+browser".
  - **Only one is ever unanswered.** New items join the unanswered batch, and its text and digest are recomputed: "keep the one waiting current".
  - Expired items drop out.
  - Overflow over 8,000 characters waits **in the engine**, never as a second ask.
  - After Krish answers, the next batch takes the next `seq`.
  - `expires_at` is the **latest** item's `not_after`. Each item's own window is enforced by `arm`, and late items record `missed_window` (B07).
  - `protocol.post_proposals` skips every creative bound into a G2 batch, so no item reaches Krish twice (B03).
  - `close_condition` is `golive_batch_done` with the batch id.
- **`exact_payload`, readable by Krish on his list, per item:**
  - `[n/N] <Platform> <Format> · <date> <window ET> · <creative_id>`;
  - `On screen:` lines (words burned into the media);
  - `Caption:` lines (verbatim);
  - `Settings:` (Instagram type, share to feed, AI label, first comment or none);
  - `Media:` the SHA-256 and size of each file;
  - `Item: <sha256>`, over the item's revision, route, review SHA-256 and the lines above.
  - The last line is `Binding: <sha256>`, for the whole batch.
  - The PC verifies against these lines, read from Control Center (B01).
  - While the repo stays public, there is no `Target:` line: comments and replies run PC-local (section 2).
- **Evidence,** up to 12 entries: a preview link to each item's media in Growth (view only), and its review summary (doctrine checked, 2 or more alternatives, why it wins) (G11, G33, G100).
- **Amendments.**
  - Krish may change `Caption:` lines only.
  - The engine parses his version back strictly.
  - A caption change runs the copy lints again and proceeds under `amended_sha256`.
  - A change to any other line (on-screen words, settings, target, window, item digest) holds that item, with "amend outside caption".
  - Unparseable text holds the batch and re-proposes it.
- **Purge** stops every unposted item: they go to `Held/`, marked "purged", and the decline is recorded. Re-proposing the same item digest is refused (C01).

### G3 check-in

- **When:** at least every other day, and after the first results of every go-live (AGENTS.md Autonomy).
- **Proposal:** `heartside:checkin:xmas26-<date>`, `kind: prepared`, wall `strategy`.
- **It never blocks a go-live.**
- **Order of the packet:**
  1. incidents (lock, drift, account status, filing backlog, decisions gap);
  2. `learn`'s "what works / what does not";
  3. numbers against both ladders;
  4. what comes next.

### Creative evidence (C07, C23)

Each item carries a `review.json`, checked against `creative-review.schema.json`. It holds:
- `doctrine_refs[]` (at least 1);
- `alternatives[]` (at least 2, kept in `Held/`);
- `why_this_wins`;
- a rubric score of 38/48 or more;
- the edit passes A to E;
- `producer` and `reviewer`, which must differ.

A lint refuses an item without it.

## 2. State, decisions and the go-live step

**Two homes for state, each with one writer** (C17, C35, C53, C72, G01, G03, G47, G51, G52, G93, G119, G120):

1. **The engine ledger** (`local/engine.sqlite3` on Actions).
   - **Writer:** `engine.yml` on **main only**. Concurrency is per ref, so the golive and admission paths refuse any other ref.
   - **Holds:** attribution, insights and read-outs, learn, bar, decisions, child runs, and hash-only records of PC-made items.
   - **Checkpoint.** It travels in the existing public checkpoint artifact, **unchanged and unencrypted**. Krish, 27 Oct: "leave it for now as is".
   - **Privacy by exclusion instead.** A **checkpoint privacy lint** (R82) refuses any export, or any `operator_events` payload, that contains:
     - an @handle or a third-party profile or post URL;
     - a Drive file or folder id;
     - a plain discount code;
     - a creator name from `local/lists/`;
     - any customer field.
     Only Heartside's own published permalinks, SHA-256s, relative paths, CR ids and aggregates pass (B00, G103).
2. **The PC store** (`local/pc.sqlite` on Krish's PC; never checkpointed and never engine state).
   - **Holds:** go-live claims, filings, card results, the outbox, and everything the lint keeps off GitHub: creator handles, comment targets, the code-to-creator key, Drive ids.

**State home: Krish's decision, deferred** ("leave it for now as is", 27 Oct). While the repo stays public, these **R-11 and R-9 tactics run PC-local**:
- comments on others' posts;
- reply batches;
- collab invites;
- reshares;
- creator shortlist and notes.

How they run:
- Codex drafts them, Claude QCs them, and the librarian files them in `Growth/04_Creators/_private` or `local/`. Krish acts on them by hand under rule 1, and the time counts in his minutes.
- They become G2 go-live items as soon as Krish picks one of three private homes for that data:
  1. make the repo private, with the engine moving to hourly to fit Actions minutes;
  2. encrypt state, with keys on both sides;
  3. a private Supabase store.

  Each is costed in Gate 0, item 14.
- Owned posts, profile edits from canon text, and audience read-outs carry nothing private, so they run as planned.

**From the PC to the ledger.**
- `card verify` writes typed, idempotent events with deterministic `event_id`s:
  - `admitted_external`: manifest, per-file SHA-256 and size, and the Drive file id;
  - `published`;
  - `readout`;
  - `audience_snapshot`;
  - `filed`;
  - `halt`.
- They are delivered through `engine.yml`'s existing `operator_events` dispatch, which prints in public run logs. So every event passes the privacy lint first, carries no Drive ids, and uses SHA-256s for anything third-party.
- **One chunk at a time** (100 events or fewer, 64,000 characters or fewer). The outbox polls that run to completion and confirms its `event_id`s in the next checkpoint before sending the next chunk. A cancelled run counts as undelivered (B06).
- **Hash only: no media bytes ever travel.** `operations.validate_creative` accepts `origin: pc` items on manifest plus hashes, so PC-made items can be approved and proposed.
- An outbox event is cleared only when a later ledger read-back shows its `event_id`. The read-back is the PC's read-only mirror of the latest checkpoint, downloaded with the fine-grained token and restored into `local/mirror/`, never over the PC's own files. Until then the event is re-dispatched.
- One bad event is quarantined with a reason and does not block the rest.

**Decisions** (G03).
- Each `engine.yml` run on main reads `GET decisions?since=<latest stored>` with **the engine bearer (the protocol token ENGINE.md names)**, the protocol bearer (ENGINE.md:272), extended from the cc steps to `engine.yml`.
- It upserts a `decisions` table: `proposal_id`, `decided_at`, decision, stage, `payload_sha256`, `amended_sha256`, with no payload text.
- Plan stops, Purge refusals, the one-ask rule and `bar` rows derive from that table, never from the 7-day window.
- If the last good read is more than 6 days old, every compile and go-live holds with "decisions gap".
- the old pack-delivery token (the disabled pack delivery) is untouched (G02, G30, G75, G91, G124).

**The go-live step: Codex, through Buffer, on Krish's PC, as he ruled** (R-5, R-12; G00, G16, G29, G31, G48, G50, G53, G54, G69, G73, G74, G87, G88, G99, G115, G116, G118). A Codex go-live card handles one item at a time, inside its window:

1. **`growth.py golive arm <batch> <item>`**, the only gate. **What it reads:**
   - **Control Center decisions, live,** with the engine bearer from the Windows Credential Manager. There is never a second token: a reissue replaces the first (G92, B08, B18).
   - **The approved text comes from Control Center,** not from the ledger. Each item's `Item:` block in `exact_payload` carries its media SHA-256s and settings, so the PC verifies against what Krish approved, with no ledger needed (B01).

   **What it requires:**
   - the batch's latest decision approved, with `stage: go_live`, and no later Purge;
   - **the parent plan still open:** its latest decision approved, and no declined `heartside:checkin:xmas26-*` or plan decision at any time since approval. If the decisions read cannot cover that span, it fails closed (B02);
   - a matching `payload_sha256` or recomputed `amended_sha256`;
   - now inside the item's window;
   - no `halt:<platform>`;
   - the store not locked when the item links to it;
   - no truth drift incident;
   - the item's preview in Growth still at the `headRevisionId` and SHA-256 recorded at filing (B15);
   - no `heartside:post:<cid>` approval and no `published` record for the creative (B03).

   **What it checks in Buffer.** Buffer itself, read-only through a **query-only client** that refuses any `mutation` (B09), on:
   - the channel's settings: link shortening off, reminders off, scheduling automatic, else it refuses;
   - an existing post on the channel matching (normalised text, asset file size or duration or image size, `createdAt` at or after any earlier claim), so an empty-caption Story never matches another Story (B04);
   - the `pc.sqlite` claims and the ledger mirror.

   **Then** it writes a **one-way** claim to `pc.sqlite` and exits 0. A claim unconfirmed after 10 minutes becomes `press_unknown`, and it blocks that item permanently until a confirm pass reads the target and finds no matching post (B05).
2. **Upload and share.** In Buffer's web composer, Codex uploads the **local file** after `growth.py golive verify-file` has checked its SHA-256 against the approved `Item:` block, pastes the caption, applies the bound settings, and presses **Share now**.
   - Renderer-made media come from the public checkpoint artifact, as today.
   - Canva and Codex media come from `local/`.
   - **Nothing is queued in Buffer ahead of time,** so a later Purge, halt, drift or lock never meets a queued post.
   - **No public media URL is needed,** so the link-editable Drive is never a media source.
3. **`growth.py golive confirm`** finds the post in Buffer by the same composite key, stores its Buffer post id, waits for `sent`, reads `externalLink`, compares the normalised caption with the approved text, records `published` with the permalink in `pc.sqlite`, and queues the outbox event.
   - A mismatch, or an unknown result, sets `press_unknown`, holds that platform, and leads the next G3.
4. **Unarmed actions are caught** (B16). Before and after every write card, the kill switch reads per-platform counts of posts, comments and reshares, from Buffer's sent posts and the profile read. It requires after = before + armed and confirmed claims; anything else sets `halt:<platform>`. The daily audience read also checks every live post against an approved `published` record (R83).

**Browser-only items** follow the same arm, act, confirm sequence in the platform's own page: comments on others, profile edits, collab posts, reshares, and formats Buffer lacks.

- **Allowlist.** Go-live acts only on wall `post` and channels {instagram, facebook, tiktok, pinterest}. It never executes a `send` or `spend` (C42).
- **Edits and archives are not go-lives.** Truth incidents draft corrections that Krish makes by hand (G111).
- **Clocks.** If the PC is asleep through an item's window, the item records `missed_window`, re-enters the next batch, and G3 reports it. That is the cost of "Share now", stated plainly (K13).

## 3. Repo structure (additive)

```
specs/schema/{run-spec,golive-batch,card,creative-review,observation,baseline}.schema.json
specs/runs/xmas26.json            # the only tracked spec; committed by an interactive session once approved
crew/<name>/card.md (≤3 KB)  crew/<name>/lens.md (≤0.5 KB)  crew/<name>/bar.json (sanitized; interactive sessions only)
invariants/{invariants,drive-contract,capabilities,known-exceptions}.json
engine/{spec,status,session,cards,allowance,golive,attribution,codes,canva,learn,librarian,audience}.py
engine/crew/{truth,design,motion,social,audience,pins,creators,answers,store,radar,measure,learn,librarian,golive}.py
jobs/cards.md (Codex)  jobs/verify-file.md (Claude on the PC)
tests/test_regressions.py (test_R##_*) and one test file per new module
docs/REGISTER.md  docs/SYNC.md  docs/baseline/2026-10-27.json
docs/briefs/2026-10-27-architecture.md (this plan)  docs/briefs/2026-10-27-cowork-canva-design-system.md (Appendix A)
knowledge/heartside-growth-corpus-2026-10.md (byte-for-byte, manifest, .gitattributes -text) + ...CONFLICTS.md (C29)
```

**Reused:**
- From `growth.py`: `problems()`, `check_pack()`, `freshness()` and `tracked()`.
- From `engine/`:
  - `offers.validate_item` and `fresh_store`;
  - `assets.prepare`;
  - `media.render` and `verify`;
  - `providers`;
  - `ledger.mark` and `normalize_report`;
  - `insights`;
  - `operations.apply`;
  - `protocol.post_proposals` and `bind_decisions`;
  - `control_center.canonical`;
  - `retention.prune`;
  - `state_store`.

**Code changes:**
- **New ledger tables:** `attribution` (keyed by start, end, timezone and tier), `insight_readouts` (append-only, read-out derived from `observed_at − published_at` in bands), `decisions`, `child_runs`, `bar`, `learnings` and `external_items`, each added to `state_store`.
- **`media.verify` reads roles by manifest `kind`:**
  - an existing manifest with no `kind` keeps today's 14 roles;
  - `canva_still`, `canva_carousel` and `canva_pin` must agree with the creative id's format token (STILL, CAROUSEL, PIN), and the id must end `_YYYYMMDD` (C58, G63).
- **`retention.prune` never evicts unfiled or open-go-live media** (B13).
  - **Trigger:** "filing backlog" fires, leads G3, and **holds new renders** when either:
    - those media pass about 40 MB; or
    - they are more than 7 days old.
  - **Proof:** a test uses measured render sizes and proves the checkpoint stays under 100 MB, or the engine holds, through a 21-day PC stall.
  - **Dropped:** there is no 90-day unfiled artifact (C20, C79, G14, G60).
- **Purchase specs generalised.** `media.render`'s buy branch, `offers.purchase_campaign`, the scene allowlist and `assets.SOURCES` stop hard-coding the mug. Any gift whose approved photography exists at the synced sha qualifies (G41).
- **Automations:**
  - `automations.json` gains `pc_automations[]`, which the runner never reads: "Heartside cards" (Codex, runs `jobs/cards.md`) and "Heartside verify and file" (Claude, through Cowork or Claude Code on the PC, runs `jobs/verify-file.md`) (C05, C16, C71, G09, G102).
  - The self-test is extended: every `jobs/*.md` file matches an `automations[].job` or a `pc_automations[].job`, `cards` and `verify-file` join KINDS, and no automation prompt says post, publish or send. The posting gate lives in `golive arm` code, never in a prompt.
- **Job counts:** a self-test refuses any job count in docs that differs from the automations (new R78; C33, G27).

## 4. The crew: 14 specialists, each with code plus a small card

Lints run before acting, and measured checks after acting, both in code. A lens (0.5 KB or less) loads for every specialist in `crew[]`. A full card (3 KB or less) loads only where that specialist acts.

| Specialist | Owns | Lint before acting (blocks) | Measured check after acting |
|---|---|---|---|
| truth | sync, catalog, canon, host name, order-by, fulfilment region, storefront state | sha fresh; `storefront_locked` (password redirect or 401) kept distinct from a 429 or a network error (R69); no store link while the store is locked; prices bound per item; a date only with canon confirmation; a date-bound item gets a hard `not_after` at its cutoff (G44) | daily drift between live posts and the sync; a mismatch opens an incident and drafts a correction for Krish; watches Printful's 2026 page and each product's region, reporting with evidence (C49) |
| design | the Canva lane (Codex fills masters in the browser) plus the renderer | QC by Claude: a transaction `read-design`, text linted element by element through `problems()` and a spellcheck, then the transaction cancelled; **every image element maps to a receipt-recorded asset id** (approved product photos, host stills, approved scenes), otherwise refused, stock photos included (G57); AI imagery labelled; size per format | the export's SHA-256 equals the binding; amendment rate per lane |
| motion | Higgsfield, Runway, Epidemic, Kokoro | a named reservation, `count` 1, no top-up or plan change; stills before motion; Runway joins `providers.PROVIDERS` | Claude matches each card's provider transactions (job ids and costs from the provider's history) to its reservations; the balance is only a cross-check, because credits are shared with Full Time (G39) |
| social | Reels, Stories and carousels on IG, FB and TikTok | hook of 3–7 words in under 2 s; `send_to`; ≤5 hashtags; gift phrase first; AI label; one CTA; the link mechanism per platform (K09) | read-outs at 24 h, 72 h and 7 d |
| audience | profiles, discoverability, comments on others, collabs, reshares | the name is frozen to the AGENTS.md display name; the bio uses canon text only (POSITIONING §1/§5 at the synced sha, K11); comments within the cap, each citing its post, with no link, no pitch and no near-duplicates; collab only with a creator at "agreed"; reshare only with a rights record; refused: follow, like, DM, engagement bait, pods, bought reach | daily: followers, follow rate, profile visits, visit-to-follow rate, bio clicks, non-follower and US share, Account Status. Milestones: TikTok 1,000 (bio link), Instagram about 1,000 (Trial Reels) |
| pins | Pinterest, once business is connected (Gate 0) | "gift ideas" phrasing; title ≤100 characters; 1000×1500; per-pin UTM | outbound clicks, saves |
| creators | 20 gifted US creators | cohort ≤20; one note per person citing their work; FTC line; codes issued; within cap; before `seed_by`; **store unlocked and the product verified** before any note is sent (G114) | post rate (PLAYBOOK assumption A2), disclosure within 48 h, Tier 1 per gifted unit at family level, code-leak flag |
| answers | Answers/GEO and the Christmas dates page (drafted in phase 1, placeholders) | 40–60-word short answer; checked-on date; sources; facts equal the store | page sessions and AI referrals, from GA via Control Center |
| store | conversion recommendations, in run 1 (checkout recovery, the $19 ornament add-on) | recommendation only; names the weak link in the persuasion chain | STRATEGY.md's diagnostic: 200 relevant US sessions through a verified journey with no purchase (G46); gift-query and zero-result signals |
| radar | trends, comments | `SAD` and mockery regexes; no repost without rights; escalations | Trial Reel outcomes |
| measure | Shopify attribution, GA from Control Center, observations, paid spend, the order-check backlog | links and codes registered; field allowlists; screenshots kept in `local/screens/`, cropped to the metric, never of orders, customers or inboxes, and never filed (K15, G68) | Tier 1, 2 and 3; trailing 28 days against both ladders; organic ≤ store total (a test); leak flags; coverage; lifetime paid-ads gifts recorded once as the comparator (G66) |
| learn | the what-works register (section 4a) | every slot labelled and citing an entry; experiments single-variable and pre-registered | verdicts recomputed **only at pre-registered read-outs**; exploit vs explore; hours from signal to proposal |
| librarian | Drive Growth and the Canva tree (section 4b) | contract path, naming, dedupe, admitted-only, `_private` by id only | an audit after each filing and weekly; every count must be 0 |
| golive | Codex, through Buffer and the browser (section 2) | `golive arm` | `golive confirm` |

**Kill switch (K06, G53).** Before and after every write card, Codex reads the following count, the sent-DM count and Account Status for each platform. A change, "Action blocked", a login challenge or a status warning does three things:
- sets `halt:<platform>` in `pc.sqlite`, which `golive arm` refuses on;
- emits a `halt` event;
- leads G3.

**The creative bar (C08, C18, C39).**
- Each amendment or decline becomes a `bar` row derived from the `decisions` table: `proposal_id`, crew, decision, `reason_code`, digests, and no free text.
- The amended text and his verbatim reasons stay in `local/bar/` on the PC, never checkpointed.
- Only an interactive session commits a sanitized `crew/<name>/bar.json`, linted against handles, profile URLs, note bodies and listed names.
- Bar rows are **taste**, kept separate from market verdicts.

### 4a. `learn`: the owner of knowing what works

**Seeded from what exists (C22, G15, G59):**
- the 28 campaign-bank pairs (C90–C96 × H01–H04, with each `mechanism` as the hypothesis);
- corpus plays P1 to P10;
- the COPY-DOCTRINE test record.

**One home per fact.** PLAYBOOK's assumption ledger (A1 to A6) stays the home of those beliefs. learn's `assumption` entries *point* to PLAYBOOK rows, and the Sunday report updates PLAYBOOK as today. The decision vocabulary stays SCALE, ITERATE, HOLD and KILL.

**The floor is ported unchanged from `insights.decisions`:**
- reach of 2,000 or more;
- age of 48 h or more;
- sends observed;
- 10 or more sends per 1,000 reach;
- at least 2× the median of 2 or more same-platform peers in the same 48-hour band.

Lowering any of these is Krish's ruling.

**Verdicts:**
- **works:** the floor, plus one of these:
  - (a) sessions per 1,000 reached at least 1.5× the platform's 14-day median, **only where the link is per-creative** (Story link stickers, Pins, a per-post bio landing page; G43, G58);
  - (b) Tier 1 orders at **family level** (code family or campaign), at least 5 orders in the window.
- **US-share gate.** Reach-based verdicts need US share shown and at least 50% where the platform reports it (G59).
- **candidate:** the bootstrap rule (`knowledge/organic-pet-commerce-engine.md`: "Before the account has a winner, 'proven' means evidence from the first seven days"). Meets the replicate test in its first 7 days.
- **doesnt:** three clearly different hooks fail on one subject.
- **inconclusive:** below the floor.
- **unavailable:** the data source is missing (GA not served, store locked) (G43).
- **untested.**

**Slots and evidence:**
- **Labels:** `exploit:<works>` (SCALE), `iterate:<works|candidate|inconclusive>` (ITERATE) and `explore:<untested>`. The mix is 70/20/10, except **until the register holds its first `works` entry**: then explore and iterate may fill every slot (G64).
- **Credit:** only from arms of a pre-registered experiment whose single variable is that subject. Slots join creatives through the signed `slot_id`, `experiment_id` and arm.
- **Capacity guard:** a scale-up holds when the Teeinblue backlog passes `backlog_threshold`, or when the oldest wait passes 24 hours.
- **Its scorecard:** exploit vs explore, hours from signal to proposal, read-out coverage. Exploring is never penalised.
- **Weekly digest:** `docs/learnings/WHAT-WORKS.md`, aggregates only, committed by an interactive session.

### 4b. `librarian`: the owner of findability, with no sprawl

**Where it writes.** Under Drive `Heartside/Growth` only.
- It never touches heartside's `00_Brand-Assets`, `_Archive` or the mirrors.
- `invariants/known-exceptions.json` lists what the engine does not manage: the older `growth-*` Drive folders, the Canva logo design and the retired V2 Canva draft (flagged in place).

**Access.** Growth is link-editable by Krish's choice (R-14). So:
- Drive is never a media source for posting.
- Drive is never canonical for an approval.
- The audit re-hashes every filed binary and flags edits.
- Folder ids live in local config only.

**`_private`:**
- created with inherited permissions off;
- **written only by id** through the Drive MCP from a Claude session, never by path through H:, because a look-alike `_private` could be planted by path (G28);
- holds the **shortlist and the name-to-id key only** (R-9). Named notes stay local (G82);
- its access read-back (`get_file_metadata` and `get_file_permissions`) is refreshed by `jobs/verify-file.md` and gates every `_private` write.

**Gift codes are never filed in Growth** (G36, B21).
- Codes are opaque.
- The plaintext code-to-CR key lives only in `local/` on the PC.
- The checkpoint holds only SHA-256s of the codes, which is enough for attribution.
- `_private` holds the shortlist and the name-to-id key only (R-9).

**Superseding inside `_private` stays inside it** (B14).
- Old `_private` files go to `_private/_superseded/<YYYY-MM-DD>/`.
- The filer and the MCP writer refuse any move into or out of `_private`.
- The audit asserts four things:
  - no `99_Archive` path contains `_private`;
  - every `_private` file has only Krish's permission;
  - `inheritedPermissionsDisabled` is still true;
  - every filed preview's `headRevisionId` is unchanged (B15).

**The contract** (depth 8 or less, covering archived paths; G62):

```
Growth/
  START-HERE.txt  INDEX.csv     derived views; rewritten in place by the PC filer (stable file ids); never superseded
  00_Inbox/                     drop point for non-librarian writers; the filer drains it each run; >24 h is an audit finding
  01_Strategy/LINKS.txt         links to the repo's briefs and specs and to the originals in Ventures/Temp; no copies (G25, G65)
  02_Campaigns/<run_id>/00_Spec/                     approval record (digests, links)
  02_Campaigns/<run_id>/<YYYY-Www>/Live/<creative_id>/   final media, caption.txt, manifest.json, live-url.txt
  02_Campaigns/<run_id>/<YYYY-Www>/Held/<creative_id>/   alternatives, unapproved, purged, with reason
  02_Campaigns/<run_id>/Results/                     check-ins, read-outs, weekly reports (aggregates)
  03_Library/                   Canva master exports, approved host stills and scenes, cue sheets, hook snapshots
  04_Creators/                  briefs, templates, results by CR01–CR20 (no codes, no names)
  04_Creators/_private/         shortlist, name-to-id key (owner-only; INDEX lists counts only)
  05_Learnings/  06_Reports/
  99_Archive/Superseded-<YYYY-MM-DD>/<original relative path>   never deleted; collisions get -2, -3
```

**Naming.** Media are `<creative_id>_<rev16>_<role>.<ext>`. Documents are `<YYYY-MM-DD>_<slug>`. Canva titles are the `creative_id`. Dedupe means skip the copy and point the INDEX row at the existing path.

**One writer.**
- `growth.py file` on the PC, under an exclusive `local/drive.lock`, run by `jobs/verify-file.md` after `card verify`, and by `file --pending`.
- **Bootstrap exception:** phase 0 creates the tree and the first START-HERE and INDEX (as plain files, with `disableConversionToGoogleType`) through the Drive MCP, once, after Krish's yes given at that moment (G12, G61, G77, G110).
- Cowork writes only to `00_Inbox`, and never creates folders (G18, G26).

**START-HERE, line 1:** "As of <UTC>, filing <id>, heartside <sha>". It then gives folder links and a link to the repo's `NOW.md`, and **never restates status** (C31).

**Canva tree.**
- `Heartside/Engine masters` corresponds to `03_Library`.
- `Heartside/Runs/<run_id>/<YYYY-Www>` corresponds to the matching campaign folder.
- Every design Codex creates is recorded, moved and titled in its card. `card verify` refuses a card that leaves a stray design (C81).

**Repo and Drive (heartside's `SYNC.md`, adapted):**
- hand-written text is canonical in the repo, and Drive holds links, not copies;
- engine binaries are canonical in Drive, with their SHA-256s in the ledger;
- generated views are canonical as their generator's output;
- superseded files are moved, never deleted.

`docs/SYNC.md` records this.

### 4c. `audience`: the owner of visibility and followers

**Daily**, as Codex read cards, which hold no write verbs:
- read each profile and its insights;
- emit `audience_snapshot`.

**Daily batch candidates.** While the state home is undecided, these are PC-local drafts that Krish acts on by hand. Once it is decided, they join the waiting G2:
- comments on others (cap 5 in W46, then up to 10 while status stays clean);
- reply batches;
- reshares with rights.

**Weekly, through G2:**
- a profile refresh: bio from canon text only, highlights, three pinned posts, covers;
- cross-links between platforms;
- collab invites on the platforms that offer them (G83). These stay PC-local drafts until the state home is chosen.

**Known leaks:**
- The TikTok account is registered in London and reaches mostly the UK. `audience` reports the US share and proposes options.
- Pinterest business and YouTube are not live. Setup is drafted, and Gate 0 asks for Pinterest (G79).
- Keyword ideas go to a heartside build-session draft, never into a go-live.

## 5. Checks mapped to the failure history

**Before any go-live, in phases 0 and 1** (G07). These come first because they are held only in writing, or live today:

| Entry | What it pins |
|---|---|
| R07 | the stacked-fragment detector; replaces "Not sorry." as the model |
| R11 | host name from canon |
| R14 | the gift-line rules: no "!", no "Dear", no he, she or names, signed only "Love, [dog]" |
| R16 | `SLOP` |
| R17 | PLAYBOOK and COPY-DOCTRINE examples pass `problems()` |
| R18 | doctrine checked against `invariants.json` |
| R34 | sends `schema_version '1.1.0'` with stage fields, and reads `amended` and `amended_sha256`; 1.2.0 only when `subject_ref` is used (C70) |
| R35 | the dispatch run id includes `GITHUB_RUN_ID`, after a test reproduces the 23 Oct 409 |
| R37 | checkpoint chosen by creation time |
| R43 | a missing checkpoint fails closed |
| R52 | an approved plan never goes live; amended text is used; a declined check-in stops the plan; Purge stops unposted items; one ask at a time; G3 never blocks G2; an 8-day-old Purge still holds |

**New this session:**

| Entry | What it pins |
|---|---|
| R61 | Canva read-back lint |
| R62 | prices and dates traced to `truth` |
| R63 | each ladder against its own targets |
| R64 | Reddit is listen-only by default |
| R65 | explicit timezones: London ledger, New York scheduler, GMT store, GA zone as Control Center reports it |
| R66 | CI time (fixed first) |
| R67 | `learn` lints |
| R68 | librarian contract and never-delete |
| R69 | `storefront_locked` |
| R70 | `audience` caps and refusals |
| R71 | GA rows with `?dog=…&person=…` refused (K00) |
| R72 | kill-switch triggers |
| R73 | an injected-comment fixture changes no card action (K07) |
| R74 | seed, gift and test orders excluded |
| R75 | live-post drift incident |
| R76 | Shopify query fields equal the allowlist |
| R77 | net-sales arithmetic |
| R78 | job counts match the automations |
| R79 | a run on a non-main ref takes nothing live and admits nothing |
| R80 | a Buffer post already present means arm refuses |
| R81 | an amendment outside a caption holds the item |
| R82 | the checkpoint privacy lint: a planted handle, third-party URL, Drive id, plain code or customer field in an export or an `operator_events` payload is refused, and nothing in a step's env header carries plaintext from the outbox (B00) |
| R83 | every live post and comment reconciles to an approved `published` record; an unarmed action sets a halt (B16) |
| R44 | Windows self-test, **in phase 1**, before PC commands run (G22) |

**Architecture tests:**
- No `POST` to a posting endpoint of instagram, facebook, tiktok, pinterest or youtube from `engine/`. Existing hosts (Control Center, Shopify auth and GraphQL, the Buffer API read) are allowlisted by name (C30, G24).
- A `status`, `pass` or `done` key is refused in specs, card returns and batches.
- `cc` relays stored payload text unchanged.
- No `.py` file under `specs/` or `local/`.

## 6. Session protocol

**The session pack:** 36,864 bytes or less, on top of the auto-loaded CLAUDE.md and AGENTS.md (C03, C66).

| Part | Size |
|---|---|
| core | 4 KB |
| spec | 8 KB |
| open lints | 3 KB |
| gate status and measurements | 2 KB |
| truth digest, with the North Star line and the lock | 3 KB |
| bar | 1.5 KB |
| learn | 2.5 KB |
| librarian | 0.5 KB |
| audience | 0.5 KB |
| lenses (0.5 KB × crew in play) | ≤7 KB |
| one full card | 3 KB |

**BROWSER.md (4 KB) is always included for browser cards** (G97). A test enforces the cap.

**Honest arithmetic.** About 135 KB today becomes about 61 KB per session, a 2.2× cut. The 20× target has to come mostly from fewer calls and no retries.

**Budgets**, logged to `local/runs/<id>/clock.jsonl` with engine time and Krish-wait time kept separate:

| Session | Tokens | Wall-clock | Calls |
|---|---|---|---|
| Orchestrator | ≤150k | ≤40 min | ≤60 |
| Reviewer | ≤60k | ≤15 min | ≤30 |
| Codex card | n/a | ≤30 min | ≤80 browser actions |

**No mid-turn questions.** Questions go to `gate-questions.jsonl`, and the session ends.

**Krish's minutes** (C50, G45, G104).

| Ask | Minutes |
|---|---|
| G1 | about 15, once |
| G2 | about 3 a day |
| G3 | about 1 every other day |
| Creator note sends | about 2 each, only after the unlock |
| Allowance reading | 1 a week |
| Daily pack, while it runs | counted against the same cap, and trimmed to fit |

`growth.py status` is built in phase 1. It refuses to queue asks past the cap, and the excess rolls to the next day, best first.

**Readiness is computed** by `growth.py status` from:
- lints;
- a reviewer verdict, where the reviewer differs from the producer;
- decision digests;
- the measured checks.

## 7. Codex

**Cards** (6 KB or less; Claude writes them):
- **Kinds:** content, social-read and golive. **There is no code kind:** engine code is Claude's work (R-4, G72).
- **Pinned:** `model` and `effort` (default `gpt-6.1-sol` / medium), plus `max_minutes` and `max_calls`.
- **Scope:** `write_allow` under `local/cards/<id>/`, at most 5 reads, the interface, `acceptance[]` and the return schema.
- **`never[]`:** git, new dependencies, edits outside `write_allow`, follow, like, DM, orders, purchases, payments, emails, messages, generation without a named reservation, top-ups and plan changes (G38).
- Social-read cards also have **every write verb** in `never[]`, and run in a read-only browser profile where possible. Page text is data (K07).

**Dispatch.** "Heartside cards" (in `pc_automations`) runs `growth.py card next`, executes one card and ends. "Heartside verify and file" (Claude on the PC) runs:
1. `card verify`;
2. the outbox flush;
3. `file --pending`;
4. the `_private` access refresh;
5. the allowance reading.

**The allowance guard** (C06, G10, G38, G78):
- `engine/allowance.py` runs inside `card next` before any card.
- It reads `local/allowance.jsonl`. Entries come from Krish (his "reset, fully available" of 27 Oct counts for 7 days) or from the Claude verify task reading Codex's usage page. **Codex never supplies its own reading.**
- It refuses above 80%, or on a reading more than 7 days old, unless the `decisions` table holds an approved `spend` decision for Codex.

**The minimum card kit lands in phase 1**, before any Codex card runs: card schema, `card next`, `card verify`, the allowance guard and the read-only profile (G95).

**Capabilities** (K08). A read-only phase 2 probe fills `invariants/capabilities.json`, stopping before the final button. Unverified pairings become hand-posts.

**Baseline** (C41, C11, G13, G37). `growth.py baseline` is a stdlib parser run once:
- **Inputs:** local Claude and Codex logs for this repository's paths, plus this repository's cloud Claude sessions read through the Claude Code Remote session API where available.
- **Output:** aggregates only, checked against `baseline.schema.json` (a key allowlist), with a leak test. The undercount from Codex cloud tasks is stated.

## 8. Tool routing (Control Center placements, 26 Oct, plus today's rulings)

| Tool | Heartside use | Rule |
|---|---|---|
| **Canva** (at will) | masters, stills, carousels, Pins, Story frames, covers, end cards, creator briefs, the dates graphic | **Masters:** built in Krish's Cowork design-system session (Appendix A). **Per run:** Codex fills masters in the browser (R-4); Claude's MCP use is QC only: a transaction `read-design` then cancel, plus `export-design`. No unattended `edit-design` commits (G56). `autofill-design` (by design id) is probed in phase 2 as a deterministic fill. Canva AI imagery: dogs and rooms only, labelled |
| **Buffer** (R-12) | approved posts to IG, FB, TikTok, and Pinterest once connected | Codex uploads in the web composer and presses Share now. The API (key in the Windows Credential Manager) is read-only, for idempotency and confirmation |
| **Codex browser** (R-4) | content building; reading profiles, insights, comments and Ads Manager spend; browser-only go-live items | cards only; kill switch; read cards separate from write cards |
| **Google Drive** (R-7) | Growth filing; `_private` by id | the PC filer is the only writer; MCP for the `_private` and bootstrap writes |
| **Google Analytics** (R-10) | sessions, engaged sessions, add-to-carts, checkouts and purchases by `utm_content`, landing **path** (never query strings, K00), and AI-referral source | **From Control Center**, requested in `docs/CONTROL-CENTRE-BRIEF.md`, the file AGENTS.md has the engine hand Krish (G85). The brief also asks for an objective key, `organic_net_sales_28d_usd`, with its target (G20, G101). Until served: GA "unavailable" |
| Shopify | attribution (R-2): Dev Dashboard app, client credentials, scope exactly `read_orders`, protected data level 1 | allowlisted fields; raw responses never logged; reconciliation with ShopifyQL `net_sales` runs **once, in an interactive session**, through the Shopify MCP (read-only), because the runner's scope excludes `read_reports` (G98) |
| Higgsfield, Runway | stills, then motion; reframe and upscale | named reservations; transaction matching |
| Epidemic Sound | music and effects | own channels only; recording id stored |
| Kokoro | narration drafts | unchanged |
| HeyGen, ElevenLabs | not for Heartside | they hold Krish's clones |
| ChatGPT Images | not routed | its ruling covers publication stills (K18) |
| Retired | Instantly, Apollo, Fireflies, Descript | never |

**Heartside privacy flag (K00).** `hs2.js` writes buyers' chat answers (dog and person names) into URL query strings, which GA likely stores, against GA's policy. The engine reads paths only, and drafts a heartside build-session brief to strip or hash them.

## 9. Phased build: sales first, never building inside a run

### Phase 0, 27–29 Oct (Claude)

1. `docs/REGISTER.md` is already filed; add its R61 onward entries.
2. Fix CI time (R66).
3. Record R-1 to R-15 and amend every text listed under the rulings (G35, G76). Mark `docs/briefs/2026-10-27-cowork-canva-brand-kit.md` superseded, with a banner and a NOW.md line (G67).
4. File `docs/SYNC.md`, this brief, Appendix A, and the corpus plus its CONFLICTS file.
5. Rewrite `docs/GET-GOING.md`'s build onto these phases (C24):
   - Step 0.5 goes into G1;
   - Steps 1 to 3 go into phase 1;
   - Step 4 goes into G2;
   - Step 5 goes into `truth`.
6. Add the R07, R11, R14, R16, R17, R18, R34, R35, R37, R43 and R78 tests.
7. Ship `baseline` and the checkpoint privacy lint (R82).
8. **After Krish's yes, given at that moment:** create the Growth tree and `_private` through the MCP, read back access, and write START-HERE and INDEX as plain files. This step comes before the Cowork session.

**Accept:** suites green; CI under 5 minutes; the Drive read-back equals the contract; `_private` owner-only.

### Phase 1, 28 Oct–2 Nov (Claude). Items marked * are needed before G1.

- **Measurement:**
  - `attribution.py`: client-credentials exchange with an exact scope check; the allowlisted GraphQL query (R76);
  - net sales: `subtotalPriceSet` per order, minus refund-line `subtotalSet` dated by `processedAt`, with test orders skipped and `taxesIncluded` asserted false (R77);
  - `customerJourneySummary.ready` false means pending (72 h);
  - exclusions: test, `hs-internal`, gift codes, paid-spend creatives;
  - store total and organic subset, in the `attribution` table *.
- **Control Center:**
  - the `decisions` table;
  - protocol 1.1.0 stages and amend handling;
  - one ask at a time *;
  - `spec` validate, compile and propose *;
  - `status` and minutes;
  - the GA and objective requests in `docs/CONTROL-CENTRE-BRIEF.md`.
- **learn:** seed and slot lints *.
- **Drafting:**
  - `codes.py`: gift codes (fixed amount, once per order), audience and post-family codes, combination settings, and a checkout test per gift;
  - the thank-you survey: app options and the one-question config, with Tier 2 counts only and never typed text (C15, G19, G71);
  - the bio-link landing page brief for heartside (K09);
  - the Christmas dates Answers page and post, with placeholders.
- **The minimum card kit,** then the first Codex cards: audience daily reads (the follower baseline) and creator shortlist research.
- **Truth:** lock, drift, Printful and region watches.
- **Product photography** for the blanket, framed print and ornament: a heartside build-session brief (heartside owns product media; Codex does not generate in Printful, G96).
- **The Windows self-test job** (R44).
- **Accept:** the * items pass on the stand-in, and **one interactive reconciliation of attribution against ShopifyQL** passes. G1 then goes on Krish's list (target Fri 30 Oct).

### W45 (2–8 Nov), if G1 is approved: the current route

- Renderer and daily pack, with audience posts that carry no store link while the store is locked, hand-posted by Krish.
- The creator batch: shortlist and notes drafted by Codex and QC'd by Claude. **Sends and gift codes only after the unlock and a verified mug cart.**

### Phase 2, 2–8 Nov (Claude builds; Codex proves), alongside W45 (whose compiled items are immutable)

- Crew lints, cards and lenses for run 1.
- `session` with its byte cap.
- `canva.admit`, with manifest kinds and `origin: pc`.
- The kill switch and the capabilities probe.
- `golive arm`, `verify-file` and `confirm`, with Buffer readback.
- The outbox and hash-only admission.
- `librarian` file and audit.
- The retention change.
- `insight_readouts`.
- The purchase-spec generalisation.
- **Accept:**
  - one Canva master filled by Codex, QC'd, admitted, filed and exported;
  - one synthetic batch end to end on the stand-in: amend inside and outside a caption, Purge, a missed window, a duplicate Buffer post refused;
  - audit all zeros.

### Phase 3, W46 onward (from 9 Nov)

The first Canva-lane slots, Codex and Buffer go-lives, and card read-outs. G2 runs daily and G3 every other day.

**Accept, dated from the unlock:**
- the first batch is live, with permalinks, and the caption read-back matches;
- every post from W46 has its three read-outs;
- W47's slots are compiled from the register, or it states plainly that none were eligible;
- every approved item is in `Live/`;
- Tier 1 is measured against the 16 Nov rung.

### Phase 4, between runs, in Nov

- answers, store and radar cards in full;
- all register entries tested;
- job files become thin wrappers;
- the daily pack is retired from the default route after two weekly runs prove the new one. It is never deleted.

### The 20× target (C11)

- **Unit:** a Krish-approved, go-live-ready creative. If the baseline count is zero, the unit becomes "proposed to Krish", and the report says so.
- **Cost:** tokens per unit, from the baseline (17 to 27 Oct, with n). Target: baseline ÷ 20 over W46 and W47.
- **Time:** engine wall-clock from compile to batch-ready, with Krish's wait reported separately. Target: baseline ÷ 20.

## Gate 0: only Krish can do these, ordered by revenue

| # | What | Minutes |
|---|---|---|
| 1 | **Heartside:** deploy PR #50, then reopen the store (R-13). Heartside's own NOW.md also asks for a fresh mug chat and cart check first. Every sale waits on this | about 20 |
| 2 | **Shopify read access:** a Dev Dashboard app with `read_orders` and protected data level 1, installed, with its client id and secret added as repository secrets | about 10 |
| 3 | **Codex on the PC:** the "Heartside cards" automation (network plus signed-in browser); a read-only browser profile; `HEARTSIDE_DRIVE_DIR` set to `H:\…\Active Ventures\Heartside\Growth` | about 15 |
| 4 | **Claude on the PC:** the "Heartside verify and file" scheduled task (Cowork or Claude Code). Store in the Windows Credential Manager, approved by name: the existing the engine bearer (the protocol token ENGINE.md names) value, a Buffer API key, and a fine-grained GitHub token (`actions:write` on this repository) | about 15 |
| 5 | **Bearer check:** if the plaintext of the engine bearer (the protocol token ENGINE.md names) is not in your own password manager (GitHub secrets cannot be read back), reissue it once through Control Center's script. In the same sitting, set it as the repository secret **and** in the Windows Credential Manager. Then one synthetic `cc` run on Actions and one `golive arm --dry` on the PC prove both (B08, B18) | about 10 |
| 6 | **Pinterest business:** create the account and connect it to Buffer, or drop Pins from R-1 | about 10 |
| 7 | **The Cowork design-system session** (Appendix A), after phase 0 step 8 | about 30, mostly unattended |
| 8 | **At G1:** gift cap and eligible gifts, `paid_ads_usd` 0, backlog threshold, follower targets, weekly credit allocation. The audience-code value is a heartside canon decision | included in G1 |
| 9 | **Heartside:** the order-by date and fulfilment region for each product, from the evidence `truth` gathers. A date is needed before 16 Nov for the dates post to run in its peak window | about 10 |
| 10 | **Switch on what the engine drafted:** codes, the survey app, the bio-link page (heartside session) and checkout recovery | about 20 |
| 11 | **Pass `docs/CONTROL-CENTRE-BRIEF.md` to Control Center:** GA aggregates, the organic objective key | about 5 |
| 12 | **Decisions:** the ladder reconciliation (K03); PR #21, which conflicts with R11's host-from-canon change, so rebase or close it after phase 0 | about 5 |
| 13 | **Run `growth.py baseline`** once on the PC | about 5 |
| 14 | **State home (deferred, "leave it for now as is"):** when ready, choose one, to turn the PC-local tactics (comments on others, replies, collabs, reshares, creator lists) into go-live items. (a) Make the repo private: the engine moves to hourly to fit about 1,700 Actions minutes a month. (b) Encrypt state, with keys on both sides. (c) A private Supabase store, as new infrastructure | about 5 |

## Verification (verification-loop after each phase)

**Deterministic:**
- `--self-test` and `unittest` on Linux and Windows;
- `spec check`;
- `session` is 36,864 bytes or less;
- `card verify`;
- CI under 5 minutes.

**Live:**
- an attribution read, with window, source and tiers;
- one interactive reconciliation against ShopifyQL;
- a Control Center synthetic run: plan, then go-live (amend inside and outside a caption, Purge), then check-in, read back by digest;
- Buffer API read-only checks (channels, post lookup) only. The first real approved batch is the live proof, and nothing is published to test (G111);
- `canva admit` on a real export;
- `audit` all zeros, with the Drive read-back matching INDEX and START-HERE's links resolving;
- the `_private` access read-back;
- GA either served by Control Center as path-only rows, or reported "unavailable";
- the checkpoint privacy lint on a real export and a real outbox chunk.

**Waits on the unlock:** anything that needs an open store.

## The call

**The call.** Approve v3, and build phases 0 and 1 now. That makes the number real, and puts G1 on Krish's list by Fri 30 Oct. Creator research and audience posts keep moving while the store is locked.

**Sharper alternative.** Hold phase 2 (Canva, Codex go-lives and Buffer) until the store unlocks, and pour every hour into the creator cohort, codes and the follower base.

**Next 24 to 72 hours:**
1. the phase 0 PR;
2. Gate 0 items 1, 2, 4 and 5;
3. the phase 1 PR;
4. G1.

**Counterpoints:**
- Every sale waits on PR #50 and the unlock. If that slips past about 6 Nov, creator seeding misses Christmas.
- "Share now" posting needs Krish's PC awake in each window. Missed windows are reported, not hidden, but they will happen.

---

## Appendix A: Cowork prompt, "Build the Heartside design system in Canva"

**Canonical.** Filed as `docs/briefs/2026-10-27-cowork-canva-design-system.md`.

It is the text Krish received in chat on 27 Oct, with the review's corrections marked **[v3]**:
- the receipt goes to `Growth/00_Inbox`, and is never a new folder;
- Canva asset ids are recorded, with product-frame element ids;
- the kit is not "in" a folder;
- where the prompt and the canon disagree, the canon wins, and the canon commit is recorded.

Run it after phase 0 step 8 has created Growth. If Krish already ran the earlier text, a short follow-up records the asset ids and product-frame ids, and moves the receipt into `00_Inbox`.

```
Build the Heartside design system in Canva, using computer use on this PC.

Krish has opened H:\...\Active Ventures\Heartside\00_Brand-Assets (Google Drive for desktop) in File Explorer and is signed in to Canva in the browser.

Goal: the Heartside design system in Canva. That is one Brand Kit named "Heartside", plus one master template for every format the growth engine produces (github.com/krishanraja/growth-heartside). Nothing is published to any social platform, shared, posted or bought.

STEP 1: READ THE CANON, THEN SHOW KRISH THE PLAN
1. Read the canon live:
   - https://raw.githubusercontent.com/krishanraja/heartside/main/design/BRAND-SYSTEM.md (colors, type, imagery)
   - https://raw.githubusercontent.com/krishanraja/heartside/main/docs/V3-GIFTS-FROM-YOUR-DOG.md (the four gifts, the voice, the host's current name)
   Where they disagree, V3 wins.
   [v3] Where anything in this prompt disagrees with the canon, the canon wins. Follow it, and list the difference in the receipt with the heartside commit you read (git ls-remote https://github.com/krishanraja/heartside main).
2. The host's name: if V3 says Buddy, use Buddy. If that is unclear, ask Krish once. Every mention of the host below uses that name.
3. List the folder's contents. Show Krish a table: file, what it is, keep or skip, and why. Wait for his yes before uploading anything.
   - 01_Identity holds the logo, heart mark, favicon and fonts.
   - 02_Imagery holds photos, product scenes and the host.
   - 03_Social-and-Ads holds product mockups, Profiles and the ornament artwork.
   - Skip Poster-template and Annual-Review. Both are retired V2.
   - This folder mirrors heartside's repo. Never edit, move or delete anything in it.

STEP 2: THE BRAND KIT ("Heartside")
[v3] A brand kit is not stored in a folder.
- Logos: the Heartside logo (the watercolor heart), in every version present.
  Skip any logo or design that shows "est." with a year, unless Krish confirms the year.
- Colors. Name each one exactly:
  ink #121010, cream #FBF6F1, blush #F0C0C0, stamp-red #A8284E, chestnut #8A4A2B,
  night #1E1714, paper #FFFDF9, white #FFFFFF, muted #5A4A44, rule #E8DCD3, focus #E49CB4.
- Fonts:
  - Fraunces for headings (SemiBold); Fraunces italic 400 for the one emotional phrase.
  - DM Sans for body and UI.
  - Courier Prime for paperwork details.
  Prefer Canva's library versions. Upload .ttf files only if Canva lacks the font and the folder holds its OFL licence.
- Text styles:
  - Heading: Fraunces SemiBold, ink.
  - Subheading: DM Sans, ink.
  - Body: DM Sans, muted.
  - Accent: Fraunces italic, stamp-red.
- Images:
  - the host character's approved images (openly AI-made; never presented as a real customer);
  - the paw signature;
  - real product photos and Printful mockups of the four V3 gifts only: mug, sherpa blanket, framed print, ornament.
- Brand voice field, if Canva offers one:
  "Your dog loves you too. Warm first, funny second. US spelling. No exclamation marks in body copy.
  Gift lines are the dog talking: I is the dog, you is the person, signed Love, [dog]."

STEP 3: THE MASTER TEMPLATES
Make them in the Canva folder "Heartside", subfolder "Engine masters". Create that subfolder and an empty "Runs" subfolder if they are missing, and never create a second folder with the same name.

Name each master exactly as listed. Use only the kit's colors, fonts and text styles.

Placeholder text must be obviously a placeholder, in square brackets, for example [HOOK: 3 to 7 words]. Never write real marketing copy into a master.

Every product area is a labeled frame: [PRODUCT: real photo or Printful mockup only]. Never fill a product frame with AI imagery or a drawn product.

Every frame showing the host carries this small line, in muted DM Sans: "[Host name] is an AI character".

The masters:
1. MASTER_REEL-COVER_recognition_v1. 1080x1920. Hook headline, dog scene area, product frame.
   Keep text out of the top 250 px and the bottom 420 px.
2. MASTER_REEL-COVER_two-sides_v1. 1080x1920. Split layout: dog side and person side, one headline.
3. MASTER_REEL-COVER_host-desk_v1. 1080x1920. The host at a desk, one line, product frame.
4. MASTER_STORY_v1. 1080x1920, 3 pages:
   - frame 1: hook;
   - frame 2: product frame and gift line;
   - frame 3: CTA with [heartside.io link sticker area].
5. MASTER_CAROUSEL_v1. 1080x1350, 3 pages:
   - slide 1: hook;
   - slide 2: recognition beat with product frame;
   - slide 3: tender turn and "heartside.io".
6. MASTER_PIN_gift-ideas_v1. 1000x1500. Title area reading [TITLE: ... gift ideas ...], product frame, "heartside.io".
7. MASTER_END-CARD_v1. 1080x1920. Logo, "Your dog loves you too.", "heartside.io". Nothing else.
8. MASTER_DATES_post_v1. 1080x1350 and a 1080x1920 Story page.
   - "Christmas order dates", plus one row per gift: [GIFT] [ORDER BY: confirmed date only].
   - Leave every date as a placeholder.
9. MASTER_CREATOR-BRIEF_v1. US Letter, 2 pages:
   - what the gift is;
   - the 2-second ritual;
   - the real product reveal;
   - [the creator's own words];
   - "#ad or gifted in the first line, plus the platform's paid-partnership label";
   - [CODE] and [LINK] placeholders.
10. MASTER_FB-TT-OPENING_v1. 1080x1920. A single native opening card: [OPENING LINE], and nothing else.

Copy rules in every master:
- US spelling.
- No exclamation marks.
- No em dashes.
- No "Your dog has notes" headline.
- Nothing from the retired annual or performance review.
- No stars, ratings, review counts, countdowns or "was" prices.

If Canva offers "Publish as Brand Template" (or "Make a template") on this plan, publish each master as a Brand Template under the Heartside kit. If it does not, leave them as designs and say so in the receipt.

NEVER UPLOAD
- The retired V2 range: The Annual Review poster, Body Double, Company Uniform, Surveillance Socks, or any performance-review design.
- Any image of an AI "customer" with a product.
- Any customer's photo, name, order or typed answer.
- Anything from outside the folder Krish opened.

NEVER
- Publish, share, post, invite anyone, or change plan, billing or team settings.
- Delete or rename any existing design, brand kit or folder.
  The existing "Conversion drafts - needs QA" folder is a retired V2 draft. Leave it untouched.
- Edit any other brand kit.
- [v3] Create any folder on the H: drive.

RECEIPT
[v3] Return this as your final message, and save it as H:\...\Active Ventures\Heartside\Growth\00_Inbox\2026-10-27_design-system-receipt.json. If 00_Inbox does not exist, do not create it: give the receipt in chat only and say so.

It must contain:
- the brand kit's name, id and URL;
- [v3] for every uploaded file: filename, SHA-256 (from PowerShell Get-FileHash), its Canva asset id and Canva name, and its kit section;
- the colors, fonts and text styles as set, read back from the kit page;
- for every master: name, design id, URL, size, page count, and brand template id (or "not available on this plan");
- [v3] for every master: the element id of each product frame and each text placeholder;
- the URLs of the "Engine masters" and "Runs" folders;
- every file skipped, and why;
- [v3] every difference between this prompt and the canon, and which one you followed, with the heartside commit read;
- one screenshot of the kit page and one of each master.
```

## Appendix B: every finding and where it is resolved

**Pass 1.** Run `wf_6bbbfa5e-2b0`: C00 to C83 (84 confirmed, 7 refuted) and K00 to K20. **Pass 2.** Run `wf_fb072b9a-2c3`: G00 to G125. Full texts are in those runs' journals, and phase 0 files the summaries in `docs/REGISTER.md`.

**Pass 1:**

| Section | Findings resolved there |
|---|---|
| §0 | C04, C25 |
| §1 | C00, C01, C02, C07, C09, C19, C23, C27, C36, C46, C47, C50, C55, C59, K10, K13, K16 |
| §2 | C17, C35, C42, C53, C72, K05 |
| §3 | C05, C16, C20, C21, C29, C33, C57, C58, C71, C79 |
| §4 | C08, C18, C39, C43, C45, C49, C52, C60, C64, K02, K04, K06, K11, K12, K14, K15 |
| §4a | C22, C48, C61, C62, C73, C74, C75, C76 |
| §4b | C13, C31, C32, C34, C65, C68, C69, C77, C78, C80, C81, C82, C83 |
| §5 | C14, C28, C30, C51, C70 |
| §6 | C03, C26, C38, C66, C67, K19 |
| §7 | C06, C11, C41, K07, K08 |
| §8 | C12, C15, C40, C54, C56, C63, K00, K18, K20 (moot: GA comes from Control Center) |
| §9 and Gate 0 | C10, C24, C37, C44, K01, K03, K09, K17 |

**Pass 2:**

| Section | Gaps resolved there |
|---|---|
| Rulings | G23, G35, G69, G70, G71, G76, G79, G80, G81, G82, G83, G84, G113, G125 |
| §0 | G08, G17, G26, G27, G38, G67, G97, G107 |
| §1 | G04, G05, G11, G21, G33, G34, G42, G44, G45, G49, G55, G86, G89, G90, G94, G100, G104, G105, G108, G112, G117, G121, G122, G123 |
| §2 | G00, G01, G02, G03, G16, G29, G30, G31, G32, G47, G48, G50, G51, G52, G53, G54, G73, G74, G75, G87, G88, G91, G92, G93, G99, G103 (privacy lint; comment targets and handles stay PC-local while the repo is public), G111, G115, G116, G118, G119, G120, G124 |
| §3 | G09, G14, G41, G60, G63, G102 |
| §4 | G39, G43, G46, G57, G58, G59, G64, G66, G68, G114 |
| §4b | G12, G18, G25, G28, G36, G61, G62, G65, G77, G110 |
| §5 | G07, G22, G24 |
| §6 | G06, G106 |
| §7 | G10, G13, G37, G72, G78, G95 |
| §8 | G19, G20, G56, G85, G96, G98, G101, G109 |
| §9 and Gate 0 | G15 (§4a), G40 (Appendix A) |

**Pass 3** (run `wf_e706ecd3-dce`, blocking only). It found B00 to B21. After it, Krish ruled "leave it for now as is" on the repo's visibility:

| Finding | Resolved by |
|---|---|
| B00 | privacy lint on events and exports |
| B01, B12, B17 | no encryption; the PC verifies against Control Center's `Item:` blocks; mirror in `local/mirror/` |
| B02 | `arm` checks that the parent plan is open and no check-in was declined |
| B03 | `post_proposals` skips batch items; `arm` refuses double routes |
| B04 | Buffer composite key and channel settings |
| B05 | one-way claims |
| B06 | serial outbox chunks |
| B07 | batch expires at the latest window |
| B08, B18 | Gate 0 #5: reissue the bearer in one sitting if needed |
| B09 | query-only Buffer client |
| B10, B11 | no encryption, so no empty-key or restore-site failure |
| B13 | backlog hold at 40 MB or 7 days; never evict |
| B14 | `_private` supersedes stay inside it |
| B15 | preview `headRevisionId` checked at proposal and at arm |
| B16 | unarmed-action reconciliation (R83) |
| B19 | R-11 amends BROWSER.md 13-24, the Autonomy line and the automations rule |
| B20 | R-1 recorded in Krish's words; Reels departure in G1 only |
| B21 | the code key stays in `local/` only |
