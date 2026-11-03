# 2026-11-03: Heartside's media goes into Drive through the home-computer lane

Status:
- content-engine's library lane carries a second library, `heartside` ([krishanraja/content-engine#356](https://github.com/krishanraja/content-engine/pull/356), merged and deployed).
- The migration was applied to production and read back.
- `factory/send_library.py` sent all 39 library files.
- Krish's home computer wrote all 39 into `Heartside/05_Social-Library/Posts/<post id>/` by 11:29 UTC. Drive shows the 12 post folders, and spot-checked sizes match the manifest byte for byte.
- The Codex README now says the media is already in `Posts/`, with the zip only a backup. The older READMEs are kept and marked superseded.
- Nothing is run by hand at home: the recordings pass keeps the sync's copy current.

Next: Krish locks F01, F02 and F04 on the lock page (and says whether F01's red dachshund stays, or "recast").

North Star check (2026-11-03): holds. Every post now reaches the Drive library Codex posts from, with no manual step for Krish.
