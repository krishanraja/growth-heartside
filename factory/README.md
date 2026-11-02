# The post factory

Builds finished posts from a JSON spec per concept, so one approved concept can be repurposed
across breeds and lines. Assets never enter git: this repository is public and the music is licensed.
Set `HEARTSIDE_ASSETS` to a folder with `renders/` (the live store's renders), `frames/` (generated
key frames), `audio/` (licensed music, SFX and voice reads) and `fonts/`. Output goes to
`HEARTSIDE_OUT` (default `local/media/factory`).

    python3 factory/film.py factory/specs/F07.json

- `common.py`: type, emoji, avatars, the product end card (real render, labelled Example), video assembly.
- `film.py`: key frames cut to a voice read and music, captions burned in, ending on the real render.
- `specs/`: F03, F05, F07 and F12 drafts. Not locked: each is shown to Krish finished once before locking.

Proposed next (awaiting Krish): lock files with fingerprints, variation slots, an approved joke bank
with breed tags, code gates and a trust ramp, so locked concepts cannot drift.
