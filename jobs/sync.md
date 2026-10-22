# Job: sync with heartside (every day, and first in every other job)

No pack. This job keeps the engine across what the heartside repository is
doing. Every other job starts with the same command.

1. `git pull --ff-only` (this repository).
2. `python3 growth.py sync`. It reads `krishanraja/heartside` on `main` and
   prints what it read. It keeps only the engine's input data (the commit,
   canon and rules fingerprints, the store and offers) in
   `local/state/heartside.json`, and never a copy of heartside's status:
   - the commit it read (`heartside_sha`);
   - commits since the last sync, and open pull requests (work in flight);
   - heartside's own `NOW.md`, read live, printed when it is fresh (no
     product commit, automation and merges aside, after the latest commit
     that touched it). Unreadable or stale prints "status: unknown" with the
     reason;
   - the canon, in the order heartside's README tells every session to read
     it, plus the newest dated handover in heartside's `docs/`, and which
     canon files changed or became canon since the last sync;
   - the latest lines of the top canon document's decision log;
   - what the live store sells right now, at what price;
   - whether the rules sections the checker was written from are unchanged.
3. Read what the sync printed. If canon changed, read the changed
   files (`python3 growth.py canon --full`). If heartside's status is
   unknown, say so in your final message and assume nothing about its plan
   beyond the canon, the commits and the store. In your final message, say in
   one or two plain lines what changed and what it means for growth, for
   example:
   - "V3 section 3 changed the blanket to $79: the gift guide items need the
     new price";
   - "a new open pull request adds the share card link: tracked share
     visits become possible".
4. If the sync printed **STOP**, Heartside's rules changed. Name the changed
   sections and say a person must update `RULES` and `RULES_BASIS` in
   `growth.py` before any pack can pass. Don't change `growth.py` yourself in
   a scheduled run.

Final message: the heartside commit, what changed, and anything a later job
today must do differently.
