# Failure and fix register

Filed 27 Oct 2026 from the architecture review (`docs/briefs/2026-10-27-architecture.md`). Entries 1 to 60 are R01 to R60; new entries take R61 onward.


Everything below comes from `/home/user/growth-heartside`. That is the full git history (62 commits, 17 to 23 Oct 2026; the current branch matches `main`), `CHANGES.md`, `NOW.md`, everything under `docs/`, `recommendations.json`, `tests/` and the `growth.py` self-test. I also made read-only GitHub REST calls for the bodies of PRs #1 to #22 and the Actions run history; findings from those are labelled as from outside the repo.

In the Test column, "self-test" means `/home/user/growth-heartside/growth.py` `self_test()` (130 checks). "Rule only" means the rule is written down but no test enforces it.

## A. Register

| # | Date | What went wrong / what Krish corrected | Fix sha | Where the fix lives | Test or marker |
|---|---|---|---|---|---|
| **Product truth drift** ||||||
| 1 | 15 Oct | Heartside's `COWORK-HANDOVER-2026-10-15.md` was not listed in its README, so the engine could not see it (it held Krish's "10X personalized delight" direction) | 5c31853 (CHANGES 15 Oct) | `growth.py:newest_handover`, `canon_paths`, `freshness` | self-test 'the newest dated handover wins', 'stale when a newer handover appears' |
| 2 | 17 Oct | Wrong-price draft: "The Morning Mug is $89." got past the live-price check, because $89 is a real store price (blanket, print) | 5c31853/a99c093 | `engine/offers.py:validate_item` | `test_offers::test_original_wrong_price_probe_is_rejected_even_with_sentence_period`, `::test_price_for_another_gift_and_wrong_link_are_rejected` |
| 3 | 17 Oct | The retired v2 public range does not prove the V3 gifts are ready; purchase copy must name exact `offers` | a99c093 | `offers.catalog`, `purchase_campaign`; `protocol.product_holds` | `test_offers::test_conversion_drafts_require_current_live_mug_and_homepage`, `::test_draft_gift_and_unavailable_cheap_variant_do_not_pass`; `test_protocol::test_product_hold_follows_current_product_truth` |
| 4 | 17 Oct | Catalog snapshots that are too old or future-dated were being treated as fresh | 5c31853 | `offers.fresh_store` | `test_offers::test_old_and_future_catalogs_are_not_fresh` |
| 5 | 20–21 Oct | Heartside's V3 §2 dog-voice ruling ("I" is the dog, "you" is the person) changed `RULES_BASIS`, so sync said STOP and every pack stopped. Krish: "yes, do both and merge to main". Actions (outside repo): 11 failed runs (6 engine, 5 sync), 20 Oct 13:03 to 21 Oct 09:37 UTC | ca52b75 (PR #7) | `growth.py` `RULES_BASIS`, `RETIRED` third-person regex; AGENTS rule 5 | self-test 'a retired third-person gift line is refused', "the dog's own voice passes", 'stopped when rules changed' |
| 6 | 21 Oct | Heartside POSITIONING and HANDOFF were rewritten (Krish: "we need consistency"), causing a second `RULES_BASIS` change. The one-line offer "posters, ornaments and pillows" was retired | 400d62b (PR #8) | `RULES_BASIS`, `RETIRED` | self-test 'the retired one-line offer is refused' |
| 7 | 22 Oct | Krish: AI gift lines "all sound like Claude… stacked two-word sentences are a clear tell". The Answers articles were rewritten live. The rule "never quote the old stacked lines" ("Weekends too. Obviously.", "Not sorry.") lived only in `state/HEARTSIDE-NOW.md`, which was deleted hours later | 68940b1 (PR #13), lost in 89e1ec9 | Docs only. The checker still uses the retired line as its model: `growth.py:161` message and the self-test at `:926` ("I took your side of the bed. Not sorry.") | **None** |
| 8 | 23 Oct | A local HTTP 429 on `/products.json` stored `store: null`. Readiness then said all 4 gifts were "not in the public catalog" and called the snapshot fresh | 398d15d (PR #19, e373717) | `offers.catalog` reason, `offers.fresh_store` | `test_offers::test_unreachable_catalog_is_not_a_fresh_empty_catalog`. No test of how `sync` itself handles a 429 |
| 9 | 23 Oct | NOW.md blamed the 429 on "this runner" (production), then narrowed it to local Windows, then confirmed the scheduled runner saw all 4 gifts. Three corrections in 5 minutes | 07e12f9 → 11d09dc → 74a2939 | NOW.md only | None |
| 10 | 19 Oct onward, open | The catalog matched the canon by 19 Oct (PR #3 body) and the V3 homepage went public 19 Oct (heartside 9ea7e34). `docs/HANDOFF.md`, README, STRATEGY, ENGINE, the `protocol.product_holds` detail text and `recommendations.json` `heartside:rec:product-readiness` still cite PR #13 or a catalog mismatch | Not fixed | NOW "Do not trust" list only | `test_protocol::test_empty_ledger_is_schema_valid_and_unknown_objectives_stay_null_with_reasons` asserts the stale 'heartside PR 13' text |
| 11 | 23 Oct, open | Heartside's host was renamed Biscuit → Buddy. PR #21 is open and unmerged; the checker's `Biscuit:` line logic and all docs still say Biscuit | None | `growth.py:problems` | None |
| 12 | Open | The order-by date (10 Dec) is unconfirmed. The brief's "$12 product… free with any order until 1 November" has not been checked against the canon | n/a | AGENTS rule 3 | Partly: self-test 'invented urgency is refused' |
| **Voice and copy** ||||||
| 13 | 14–17 Oct | House rules: no em dash anywhere (briefs and COPY-DOCTRINE too), banned words, "it's not X, it's Y", US spelling, grief, invented proof or urgency, was-prices, any email other than krish@heartside.io, hashtag walls | 5c31853 | `growth.py:problems`, `check_pack` | self-test (an em dash is refused; a brief's em dash is still refused; COPY-DOCTRINE has no em dash; banned word; UK spelling; grief; invented urgency; invented proof; was-price; another email; hashtag wall) |
| 14 | 14 Oct / 20 Oct | Exclamation marks: none in body copy; Biscuit gets at most one per line and no emoji. Gift lines: no "!", no "Dear", never he/she/dog's name/person's name, "Love, [dog]" is the only sign-off | 5c31853, ca52b75 | `problems` (body copy and Biscuit lines only) | self-test 'an exclamation in body copy is refused', 'Biscuit may have one / not two / no emoji'. The gift-line rules are rule only |
| 15 | 14 Oct | Retired lines: "written by your dog", "Now it's in writing", "Your dog has notes" (headline retired; sign-off undecided, ask Krish; the handle is fine), annual/performance review, body double | 5c31853 | `RETIRED` | self-test for each. "performance review" itself is not tested directly |
| 16 | 14 Oct | Krish's slop kill list (`SLOP`: delve, seamless, leverage…) | 5c31853 | `growth.py:148` | **None** |
| 17 | 21 Oct onward | The PLAYBOOK hook "If your dog waits at the door for you, this is for you." (`PLAYBOOK.md:194`) and the matching example in `COPY-DOCTRINE.md:26` match the retired regex at `growth.py:160`. The doctrine's own hook fails `check` (I confirmed the regex matches) | Not fixed | Docs | None |
| 18 | 19 Oct onward | `COPY-DOCTRINE.md:230` §10.8 still says 'no "I" in the dog's voice on a gift'. That is the 13 Oct rule that the 20 Oct ruling replaced | Not fixed (from c5654b4) | Doc | None |
| 19 | 19 Oct | Krish: "imbue [engines] with this knowledge". The corpus is kept byte for byte, with `.gitattributes -text` | c5654b4 | `knowledge/corpus-manifest.json` | self-test '<path> matches its manifest bytes and SHA-256' |
| 20 | 21 Oct | Krish asked for AEO content "invisible to humans". The agent pushed back (that would be cloaking) and built it unlisted but public; Krish: "yes to all four" | 70fa624, d664d54 | `docs/GEO-AEO.md` §3, §10 | None |
| **Provenance and media** ||||||
| 21 | 14–17 Oct | AI never draws the product and never shows AI customers | 5c31853 | assets, media | `test_engine_runtime::test_generated_media_cannot_replace_a_product_photo` |
| 22 | 17 Oct | Render integrity: checksums, tamper detection, a failed build keeps the previous output, paths stay inside `local/` | 5c31853 | `engine/media.py` | `test_media::test_render_cache_checksums_and_failed_build_preserve_previous_output`, `::test_generated_paths_cannot_escape_local` |
| 23 | 19 Oct | A caption edited after approval must be held, not proposed | a87b932 | `protocol.post_proposals` | `test_protocol::test_a_tampered_caption_is_held_not_proposed`; `test_operations::test_tampered_files_and_extra_customer_fields_cannot_be_recorded` |
| 24 | 17 Oct | Voice model supply chain: unpinned downloads are refused | 5c31853 | `engine/voice.py` | `test_voice::test_unpinned_download_sources_are_refused`, `::test_scripts_are_bounded_before_loading_any_model` |
| 25 | 22 Oct | The media brief asks for V2 "performance review" stills and a "dog reads your review" product. V3 retired the HR builder and the poster range | Flagged in 634d789 | NOW.md "Next action" (doc only) | Partly: the `RETIRED` regex would refuse that pack copy. Nothing checks the brief itself |
| 26 | 17 Oct | Paid generation budget defaults to zero; an uncertain submission is never retried automatically | 5c31853 | `engine/providers.py` | `test_engine_runtime::test_budget_default_blocks_paid_and_idempotency_survives_a_new_quote`, `::test_uncertain_generation_cannot_auto_retry_and_honest_overrun_blocks_budget` |
| 27 | 22 Oct | Ruling: generation within prepaid credits, inside a weekly allocation Krish approved, counts as authorized. Drift: `PLAYBOOK.md:254` still says any credit spend needs his yes, and the Higgsfield balance is 1,303 in the brief but 1,413 in the PR #12 body | 0303ffb (PR #12) | `providers.py` | `test_engine_runtime::test_prepaid_credits_spend_no_new_money_and_stop_at_the_allocation` |
| **Attribution** ||||||
| 28 | Open | `organic_orders` is hard-coded missing. The North Star number is "not measured (attribution not wired)", urgency U4 (`NOW.md:36`) | GET-GOING Step 3 open | `protocol.organic_orders` | Asserted missing in `test_protocol::test_empty_ledger…` |
| 29 | 17 Oct | Store totals are never credited to a creative; no winner is declared from one post; replication needs two comparable peers | 5c31853 | `engine/insights.py` | `test_engine_runtime::test_observations_replace_snapshots_and_never_allocate_native_revenue`, `::test_no_decision_without_publication_and_no_winner_from_one_post`, `::test_replication_requires_two_comparable_peers_and_stale_evidence_is_held` |
| 30 | 14 Oct | Every heartside.io link must carry tracking built from its creative id | 5c31853 | `growth.tracked`, `problems` | self-test 'an untracked store link is refused', 'a mismatched creative id…', "a brief's link is still tracked" |
| **Protocol and reporting** ||||||
| 31 | 19 Oct | The live report was **held**: `net_sales_usd` read 0 and stale because Shopify imports stop at 16 Oct | Labelling fixed in a87b932; the daily import (Step 2) is not built | `protocol.net_sales` | `test_protocol::test_overlapping_windows_are_never_added_and_old_coverage_is_stale`, `::test_partial_coverage_is_missing`, `::test_no_ledger_is_degraded_not_zero` |
| 32 | 19 Oct | Never send a zero that was not measured; JavaScript writes 1 where Python writes 1.0, which breaks the digest (caught by mutation testing in PR #3) | a87b932 | `control_center._wire_safe`, `canonical` | `test_protocol::test_measured_zero_is_zero_and_never_a_float_one_point_oh`, `::test_canonical_json_matches_javascript_and_refuses_python_only_numbers`, `::test_worked_example_digest_is_reproduced`; self-test 'a guessed number is refused' |
| 33 | 19 Oct | A 409 or timeout is read back, never retried blindly; the token never appears in output; redirects are refused | a87b932 | `protocol.deliver`, `Client` | `test_protocol::test_conflict_is_read_back_never_retried_blindly`, `::test_unauthorized_…`, `::test_missing_secret_…`, `::test_redirects_are_refused…` |
| 34 | 21 Oct | Protocol version: Legibility and Mindmake demanded exactly 1.0.0 and stopped reporting for 2 days. The rule now is "accept any 1.x". This engine accepts any version only because it never checks. It still **sends `schema_version: '1.0.0'`** (`protocol.py:279`), while GET-GOING says send 1.1.0 and NOW says it "speaks 1.2.0" | b1a14af (protocol doc copy only) | No code | **None**: the directive fixture is 1.0.0 only (`tests/test_protocol.py:31`) |
| 35 | 23 Oct | Outside repo: a second same-day `repository_dispatch` reused run id `heartside:2026-10-23:directive`, so the attempt start returned 409 `conflict` (run 39984403394, 16:09 UTC) | Not fixed, not recorded in the repo | `protocol.run_identity` | `test_run_ids_are_stable_per_day…` asserts the id that collides |
| 36 | 17 Oct | Dashboard and ledger: one sourced Shopify row, the right store, overlapping windows never added, corrections replace, customer fields rejected | 5c31853 | ledger, dashboard | `test_ledger::test_tool_result_has_one_row_and_the_right_store`, `::test_overlapping_aggregate_and_daily_windows_are_not_added`, `::test_raw_customer_fields_and_invalid_numbers_are_rejected`; `test_dashboard::test_remote_read_is_scoped_…`, `::test_zero_sales_and_partial_coverage_…` |
| **Scheduling and runtime** ||||||
| 37 | 17 Oct | The recovery checkpoint was chosen by artifact ID instead of creation time | 5c31853 | `engine.yml` JS sort | None |
| 38 | 17 Oct | Artifact storage was not bounded when a job failed | 5c31853 | `engine.yml` `if: always()` cleanup | Hosted run 39024993241 (intended failure); `test_engine_runtime::test_hot_media_retention_preserves_ledger_metadata` |
| 39 | 17 Oct | Completed jobs were not refreshed when product inputs changed | 5c31853 | runner fingerprints | `test_engine_runtime::test_changed_product_input_refreshes_completed_work` |
| 40 | 17 Oct | Exported campaigns were outside the authoritative ledger | 2963648 | engine and handoff workflow allowlist | None |
| 41 | 17 Oct | Duplicate checkpoint bytes; library export failed at "Bind the handoff receipt" (run 39026601463) | 9c74731, 6ebdbab | `state_store` v2 | `test_checkpoint_versions::test_identical_content_is_stored_once…`, `::test_original_version_one_checkpoint_still_restores` |
| 42 | 17 Oct | Non-portable and case-colliding checkpoint paths | d5c515d | `state_store.permitted`, `export` | `test_checkpoint_versions::test_external_hardlink_is_rejected…`; collision assert inside `test_identical_content…` |
| 43 | 17 Oct | A missing or expired checkpoint must fail closed, never silently reset | 5c31853 | `engine.yml:62` | None |
| 44 | 23 Oct, open | Windows (PR #19/#20/#21 bodies): DejaVuSans.ttf missing; the corpus DOCX filename contains an em dash and cannot be resolved, so the self-test fails; the case-collision test fails on a case-insensitive filesystem | None | n/a | CI runs Linux only |
| 45 | 22 Oct | Docs steward failed: no the steward's Claude token (runs 39833107521, 39873371234) | Krish added the secret; 11 successes since | n/a | None |
| 46 | 17–22 Oct | The hourly sync bot committed copies of Heartside's state (13 "sync: heartside" commits) and the copy went stale | 89e1ec9 | `sync.yml` `contents: read`, no commit | `test_heartside_now::test_the_repository_holds_no_copy`, `::test_sync_writes_no_copy_of_heartside_status`; self-test 'sync stores no copy' |
| 47 | 22 Oct | NOW.md freshness: steward, heartbeat, harness and merge commits must not make it stale; unreadable means unknown | 89e1ec9 | `growth.now_verdict`, `heartside_now` | 11 tests in `tests/test_heartside_now.py`; self-test 'Automation and merges never make NOW.md stale' |
| 48 | 21 Oct | Seven jobs became eight; New York DST; every job has an automation; no automation asks to post | 70fa624 | runner, `automations.json` | `test_engine_runtime::test_scheduling_uses_new_york_dst_and_eight_declared_jobs`; self-test 'every job file has an automation', '…never asks to post' |
| **Approvals and authority** ||||||
| 49 | 17 Oct | The agent worked toward Control Centre (draft PR #472). Krish: "you are not to do any actual work in control-center, only pass me a brief" | 5c31853 | `HEARTSIDE_ENABLE_CC_DELIVERY` defaults off; AGENTS boundary | `test_control_center::test_reporting_token_does_not_enable_central_requests`, `::test_missing_secret_never_makes_a_request` |
| 50 | 17 Oct | The agent thought the credential was missing. Krish: the old pack-delivery token was already in secrets; the real blocker was venture isolation (a Heartside pack would overwrite makeyourmindup's) | 5c31853 | `growth.control_center_takes_heartside` (its docstring still says PR 472 is pending, though it merged 18 Oct) | `test_control_center::test_legacy_api_authentication_is_separate_from_venture_readiness` |
| 51 | 17 Oct | Scope: product work goes to the heartside repo (PR #13); "Complete this all to 100% without coming back to me again" | 5c31853 | CHANGES only | None |
| 52 | 19 Oct | Rulings: plan → go-live → live; "autonomy is given where it's deserved"; Krish approves or amends; the creative bar. **None of it is built (Step 1):** `protocol.py` still says "he still acts by hand" and ignores `stage`, `amended` and `amended_sha256` | 8ba5523 (docs only) | AGENTS "Autonomy" | **None**: nothing tests that an approved plan never goes live, that his amended text is used, or that a declined check-in stops the plan |
| 53 | 19 Oct | A declined payload is never proposed again; a changed payload goes back to Krish | a87b932 | `protocol.build_report` | `test_protocol::test_declined_payload_is_not_proposed_again_…`, `::test_approved_creative_is_a_post_proposal_bound…` |
| 54 | 21 Oct | Ruling: one ask per engine at a time (go-live, then check-in, then plan); `subject_ref` gives way to Control Center's copy | b1a14af (doc only) | Not implemented: a report can carry up to 10 proposals | None |
| 55 | 18–23 Oct | Process rulings: a North Star per repo (bf8b536); human-speed dates moved to agent speed (c51ed5b); next action chosen by rule (ENGINE-PROTOCOL:151); every engine adopts the protocol (PR #3 body); "Get going", no pasted prompts (70d9236); one home per fact and merge the five PRs (89e1ec9); a number, weekly ladder and urgency (72e301f) | n/a | Docs; machine-readable `north-star-state` block in NOW | None |
| **Docs drift** ||||||
| 56 | 23 Oct | The CONTROL-CENTER-BRIEF status line still said synthetic-only after the loop went live | 634d789 (PR #20) | Doc | None |
| 57 | Open | "Seven" jobs in README, HANDOFF and AGENTS (setup steps 4 and 7); AGENTS Autonomy and GET-GOING still say protocol 1.1.0 | Not fixed | NOW flags only README/HANDOFF jobs and GET-GOING | Only file parity is checked (#48) |
| 58 | 19 Oct | The copied protocol doc linked ADR-038 by a relative path that does not exist here; the link check refused it | 8ba5523 (second commit) | Doc | The link check is not in `check.yml` |
| 59 | 18–21 Oct | CONTROL-CENTRE-BRIEF superseded (9790ed7, banner); the 12 Oct social plan left heartside POSITIONING §6 (400d62b; PLAYBOOK now cites "the 12 Oct plan") | as listed | Docs | None |
| 60 | 23 Oct | Harness closeout failed on PR #19 until NOW.md was updated (run 39953878696). Test counts disagree: HANDOFF says 52, the PR #1 body says 45 | 07e12f9–74a2939 | `.claude/hooks/harness-closeout.mjs` | The hook itself |

## B. Themes

- **Product truth drift:** 1–12, 25.
- **Voice and copy:** 5–7, 13–20.
- **Provenance and media:** 21–27.
- **Attribution:** 28–30.
- **Protocol and reporting:** 31–36, 53.
- **Scheduling and runtime:** 37–48.
- **Approvals and authority:** 49–55.
- **Docs drift:** 9, 10, 17, 18, 27, 34, 56–60.

Seven corrections are recorded only in writing, with nothing enforcing them or pinning the right behaviour: 7, 11, 17, 18, 34, 35, 52.

## C. Baseline evidence

**In the repo**
- **17 Oct verification** (`docs/VERIFICATION-2026-10-17.json`):
  - 7 campaign packs, 28 hook experiments, 105 native media files.
  - 110 self-checks, 52 tests.
  - `purchase_ready_gifts: 0` of `canonical_gifts: 4`.
  - 14 hosted runs recorded (13 success, 1 intended failure), verified 11:31:37 UTC.
  - Replay `operator_events_counts: ["0"]`.
- **Shopify, 1–16 Oct** (`docs/HANDOFF.md:98`): 1 order, $0 net sales, 380 sessions, 40 cart sessions, 21 checkout sessions, 1 completed checkout. No post, paid AI job, order or store change was performed. Images came from the native authoring tool "whose output did not include a monetary charge".
- **19 Oct live report** (`docs/GET-GOING.md:45`): held; `net_sales_usd` 0 and stale; `organic_orders` missing; 2 proposals.
- **North Star** (`NOW.md:36`): current `null`, week target $200, U4.
- **Credits:** provider balances are kept out of this public file (NOW.md never_publish); see the 22 Oct brief.

- **Answers:** 3 published 21 Oct, updated 22 Oct; question bank of 28.
- **Test counts over time:** 110/52 (17 Oct), 112/73 (PR #3), 123/73 (PR #7), 124 (PR #8), 130 (PR #13), 74 tests (PR #12). Today there are 86 test methods in `tests/`.
- **Krish's time budget:** a target of about 20 minutes a day and 30 on Sunday (`AGENTS.md:234`); per-job estimates of 5 to 15 minutes in `jobs/*.md`. None of it is measured.
- **Sessions:** 6 distinct `Claude-Session` ids in commit trailers. Model trailers: Opus 5.5 ×14, Sonnet 5.5 ×2 (steward), Opus 5 ×1. Codex sessions (PRs #1, #19, #20, #21) carry no ids.
- **Not recorded anywhere in the repo:**
  - token usage;
  - per-session wall-clock time;
  - packs approved or declined by Krish (the ledger lives in uncommitted `local/` and in Actions artifacts);
  - plans or go-lives proposed or approved (zero, since Steps 0.5 and 1 are unticked);
  - publications (zero);
  - creatives rendered after 17 Oct.

**Outside the repo (GitHub API, read 27 Oct)**
- **PRs:** 20 merged. Seven merged within 10 seconds of opening (#7, #8, #9, #10, #13, and others); #1 took 2 h 08 m; #15 took 1 h 35 m.
- **Allocation:** PR #12 records a one-week Higgsfield allocation across Heartside and Full Time (balances omitted).
- **Actions** (325 runs in total):

| Workflow | Runs (ok/fail) | Median duration | Other |
|---|---|---|---|
| Engine | 79 (72/7) | 59 s | max 993 s, about 113 min in total |
| Control Center directive | 10 (9/1) | 19 s | |
| Sync | 72 (67/5) | 13 s | |
| Check | 127 (all ok) | 59 s | about 409 min in total |
| Docs steward | 13 (11/2) | n/a | |
| Handoff | 4 (3/1) | n/a | |

## D. The creative bar (Krish's recorded amendments and declines)

**Where it is written:**
- `AGENTS.md:33` "The creative bar" (8ba5523): "Krish has a low tolerance for poor creative output… His amendments and declines are the bar: record each one where the next draft reads it."
- `docs/control-center/ENGINE-PROTOCOL.md:180`.
- `docs/GET-GOING.md:33` and Step 1: the doctrine checked against, at least two alternatives, and why this one wins.
- The brief's "Counterpoint to carry": idle credits are no reason to generate.

**What is actually recorded for this engine's creative work: nothing.**
- No file or ledger table stores amendments or declines.
- `protocol.py` keeps a decline only as a payload hash so it is not proposed again. It stores no reason.
- No go-live has ever been proposed.
- PLAYBOOK asks for a "Rubric: total/48" note line, but none is committed.

**Krish's recorded creative judgments.** These are all on Heartside's product copy. They survive only in the archive `docs/history/2026-10-22-HEARTSIDE-NOW.md:78-85`, marked "not current guidance":
- 14 Oct: mug direction A.
- 15 Oct: mug v3 approved ("yes to both").
- 15 Oct: cut-out and Fraunces redesign "okay, pretty standard", not built.
- 15 Oct: every gift as a letter rejected ("sounds shit").
- 15 Oct: "10X personalized delight", still open.
- 20 Oct: the dog-voice ruling.
- 21 Oct: "re-render the product images in the dog's voice".
- 22 Oct: "They all sound like Claude… stacked fragments are a clear tell", which led to 60-character lines and Sonnet writing the note.

**On growth work:**
- "yes to all four, put them live" (`docs/GEO-AEO.md` §10).
- "update the Answers article" (68940b1).
- The kill list in `growth.py` `SLOP`, the 12 overrides in `COPY-DOCTRINE.md` §10 (one of them stale, see #18), and `jobs/daily-pack.md:63` "V3 rejected the HR builder".