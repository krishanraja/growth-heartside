# Platform UI implementation verification

Date: 6 November 2026. Source baseline: `392c0af`, from the asset-prep branch.
Scope: implement the supplied social creative UI standard in the existing
production and release paths. No live post, queue, account or spend mutation.

Route: krish-principles -> strategy-brief -> document extraction and bounded
layout repair through krish-design -> krish-build -> verification-loop.
The supplied standard controls the repair; no new creative direction or channel
is introduced. Rollback is a revert of this implementation commit, preserving
the existing locks and media library. No provider generation or original-asset
recovery was needed to test the implementation.

Verified:

- 152 repository self-checks pass with Python UTF-8 mode on Windows.
- Final focused suite: 46 tests pass, including matching/mismatching metadata,
  missing/stale/future evidence, exact media/copy binding, required devices and
  states, separate paid previews, factory release holds, automated proposal
  holds, preservation of approved geometry, and receipt checkpoint/restore.
- Media and layout suite: 15 tests pass, including actual FFmpeg render, cache,
  file checksums, copy tampering, failed-build preservation and caption pixels.
- Broad suite: 150 tests ran; 148 pass, one voice integration test skipped, one
  existing Windows case-collision fixture fails. The same failure reproduced
  with `engine/state_store.py` loaded from the unchanged `392c0af` baseline:
  writing `A.bin` overwrites `a.bin` on this filesystem, so the fixture cannot
  create the simultaneous duplicate names it expects. No passing claim for
  that test. The new creative-ui checkpoint roundtrip passes separately.
- Synthetic chat/caption frames were rendered and visually inspected. The
  caption is readable in its narrowed middle-lower panel; latest chat blocks
  stay within the working region. These use test fonts/shapes and prove helper
  layout behaviour, not final branded creative or platform acceptance.
- Locked specifications, locks and `library/manifest.json` have no diff.

Not verified / retained holds:

- Actual new F10/mug exports, final descriptions, native overlays, Android/iOS
  viewing and live published UI have not been reviewed in this implementation.
  Their evidence stubs must stay unverified; do not infer clearance from tests.
- Current sync at heartside `602813d605` reports changed DOG_VOICE rules and
  keeps production STOP. Store returned 429. Neither issue is bypassed here.
- Source document's official platform claims were not independently refreshed;
  only house defaults are encoded. Inspect current native upload paths at release.
- New code is a repository change, not proof that a scheduled runner has been
  updated or that a currently queued post has been replaced.
