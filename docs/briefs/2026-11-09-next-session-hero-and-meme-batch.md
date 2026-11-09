# Next session: 3 to 5 hero assets, then 50+ meme and video posts

Krish, 2026-11-09: "After this session, I'm going to kick off a new session to create 3-5 hero assets and then 50+
hilarious meme and generated video assets based on approved hilarious scripts that we agree on."

This is the route for that session. Everything it needs is in this repository and in Drive by ID; it needs no earlier
conversation. It moves the North Star directly: organic posts that travel are the only lever on organic sales.

## Step 0: start state (about 10 minutes, before any idea)

1. `python3 growth.py sync`, then read what it printed (AGENTS.md rule 2).
2. The 4 to 9 Nov production branch is on `main` ([krishanraja/growth-heartside#42](https://github.com/krishanraja/growth-heartside/pull/42),
   merged 9 Nov): the platform-UI gate in `factory/lock.py`, `factory/review_board.py`, `factory/audit.py`, the
   anatomy section of `factory/README.md` and `docs/briefs/2026-11-08-organic-anatomy-correction.md`. Read them.
3. `python3 growth.py events import docs/social/2026-11-09-engagement-history.json` (safe to replay), then
   `python3 growth.py social status`. Production does not own those tests; note them and move on.
4. `python3 growth.py floor`, the whole floor, then `--format` for each format you will make. Every entry is a check.
5. Open a 03a session folder `YYYY-MM-DD_Claude-Hero-and-Meme-Batch` with its `START-HERE.md`, and run the Drive audit
   (`docs/DRIVE-MAP.md`, "Auditing").
6. Read "Decided by Krish on 9 Nov" below; those questions are closed.

## The loop, one stage at a time

Each stage has its gate. Nothing moves to the next stage on a promise.

1. **Ideas (Claude).** For the heroes: 8 to 10 genuinely different premises, each in one sentence with its payoff
   stated without the caption (floor `dumb-stopping`). For the memes: 70 or more one-line scripts across the comic modes
   in `docs/briefs/2026-11-02-funny-bar.md`, grouped by premise family. Strike anything that repeats a retired premise:
   the rain scene, F03 Operation Stocking's reuse, the F06 frenchie roast lines and the OG-01 to OG-05 executions.
   Gate: Krish picks on **one** review page (floor `one-status-page`), with the scripts' exact words. His picks and his
   words go into `factory/bank/lines.json` (approved, with `text_sha256`) and `CHANGES.md`. Concept-level approval
   (AGENTS.md, Krish 29 Oct) then covers every post derived from an approved concept and its exact mock.
2. **Stills before motion (Claude through Higgsfield, inside the venture's Control Center share).** One still per
   approved script. Before Krish sees any: an anatomy and realism record for the source and the final crop (floor
   `real-dogs`); the caption covered and the joke still readable (`stage-the-joke`); no text over eyes or action
   (`text-clear-of-faces`); the real product render only (`real-product`). If generated dogs keep failing, switch to real
   dog photography rather than repairing. Gate: Krish approves stills on the review page, scored out of 10
   (`ten-out-of-ten`).
3. **Motion, only for approved hero stills.** Write the shot list as set-up, turn, payoff (`scene-progression`). Check
   every movement has a cause and every dog behaves like a dog (`real-behavior-in-motion`). A still's approval never
   carries over to its motion. Gate: Krish approves the motion.
4. **Builds by Codex, by card (`codex/README.md`, "Claude runs Codex end to end").** One card per hero, and one card per
   batch of memes with a manifest of the posts. Each card has its `## Floor` and `## Drive` sections. Claude checks
   every output at full size against each floor line; a fail goes back as a new card. Record every card in
   `codex/INDEX.md`.
5. **Lock and file.** `factory/lock.py` (check, media, brief, record, lock, gate) for each post; then
   `factory/send_library.py` files the locked media into 03b `Posts/<id>/` (next id `F28`). The rows go in a new
   `02e Schedule and captions (<ids>)` Sheet, with `approved` left for Krish, and the README for Codex is updated in
   the same step.

## Volume: what the factory lacks for 50+, to build first in that session

- **A still/meme template.** `factory/build.py` builds chat, search, roast and film; the 7 to 9 Nov stills were made
  outside the factory and never passed `lock.py`. Add a `still` template (one image, real render composited
  unchanged, text placed clear of faces) before making memes.
- **Batch specs.** One spec per post by hand will not scale. Generate the specs from the approved-lines manifest, then
  check and build them in one pass.
- **The trust ramp.** `lock.py` sends the first 5 variants of every lock to Krish. With concept-level approval, group
  the memes under a handful of approved concepts so the ramp is about 5 reviews per concept, not per post. Krish's
  budget is about 20 minutes a day.

## Decided by Krish on 9 Nov ("Go with your recommendations")

1. **Trolling dogs look like real dogs.** Real dog expressions that read as trolling (the stare, the head tilt, the
   paw on the thing), never a human smile (floor `troll-not-mild`).
2. **Approval lives in the Sheet.** Krish marks `approved = yes` in the `02e` Sheet; the publishing desk posts
   nothing else. A chat approval no longer counts.
3. **The `ui-v1`/`ui-v2` editions are retired** (`library/CURRENT.md`). They stay in Drive; nothing new posts from
   them.

## Done when

3 to 5 heroes and 50+ meme or video posts are locked in `factory/locks/`, filed in 03b with their `02e` rows, each
with a floor record that passed and Krish's approval on record; `codex/INDEX.md`, `factory/floor.json` (any new
declines), `CHANGES.md` and the Drive audit are current; nothing has been posted by the engine.
