# Every post now built and gated against the 12 Nov creative corpus

Status: Krish supplied a creative production corpus on 12 Nov: "Ensure all social media posts adhere to these best
practices." It is kept in `knowledge/social-media-creative-production-corpus-2026-11-12.md` and runs as profile
`social-corpus-2026-11-12-v2` (`engine/creative_ui.py`, `docs/CREATIVE-UI.md`). It sets the critical box at
x 120 to 820, y 330 to 1180; subtitles of 1 or 2 lines and at most 7 words a segment; hooks of at most 12 words;
no logo or empty opening; a moving 3 to 4 s product end; and the export preset. Every renderer writes a layout
manifest bound to its file. `lock.py media` and `gate`, the release check, `factory/audit.py` and
`codex/check_picture.py` hold anything outside the corpus.

Placement left the lock fingerprint, so all 16 factory specs moved onto the profile and keep their locks. Proof
renders from the rebuilt public library: F34 and its three variants pass, and all seven campaigns pass. F11's
searches are too long for the box (it now refuses to build). F10 breaks `no-novelty-sfx`. Filed 03b media
(F01 to F59) predates the corpus and was not measured or edited. Codex labels move from text top y 300 to y 360.
Tests: 256 pass (baseline 248), self-test 170. Detail: `docs/audits/2026-11-12-corpus-audit.md`.

The review board (claude.ai/artifact/A3tFqoYZuYAEdUrziU5wnN) was not reachable from this cloud session (not found
for this account), so this decision is not on it yet: `decision-corpus-hold-queue`, "Hold the pre-corpus posts
not yet live until Codex recuts them to the corpus?" Recommendation: No. Their labels sit 30 px above the box,
inside the 10 Nov TikTok-checked band, and the 16 Nov checkpoint needs them out. Apply the corpus to every new
build and to any rebuilt edition.

Next: add `decision-corpus-hold-queue` to the review board from a session that can open it, then run
`python3 factory/audit.py` on the 03b `Posts/` folder on the home computer to measure the filed media.

North Star check (12 Nov): holds. Posts readable in the platform UI protect watch time and taps toward the
$4,862 checkpoint on 16 Nov; no number moved today.
