# Codex card: finish the audit, fill the library, plan the boost test

Written on 4 Nov 2026 by the growth engine's Claude session, for Codex. Krish asked for every motion asset to be audited to a 10/10 bar and gathered into one uniform library with one manifest, "so codex can begin planning the paid boost tests".

Read these first:
- `docs/audits/2026-11-04-creative-audit.md` (the bar, the scores and the fix list);
- `docs/PAID-BOOSTS.md` (the ruling and its gates);
- `docs/PUBLISHING.md`;
- `docs/BOOST-LIBRARY.md`;
- `docs/DRIVE-MAP.md`.

## Hard lines

- Spend nothing, launch nothing, boost nothing. Planning only. A campaign goes live only with Krish's named approval of the exact campaign, budget, dates and files, given immediately before launch.
- Post nothing that is not already an approved schedule row, and change no locked post's words, captions or renders.
- No new Drive folders. Library files go only through the home-computer lane: `factory/send_library.py` with a `manifest.json`.
- Review renders and contact sheets stay under `local/`: never in git or Drive.

## 1. Finish the audit: the files this session could not reach

This session could not download F01, F02, F03, F04, F05 or F12, because they are over the Drive connector's size limit. It also could not reach your private board.

1. Run `python3 factory/audit.py <folder> --json local/audit/2026-11-04.json --sheets local/audit/sheets` on:
   - the 12 library reels and their covers and slides;
   - the 3 motion candidates (F04, F05, F12);
   - the F12 A and B pair.
2. Review each reel at full frame rate against the bar in the audit doc (sections "The bar" and "Systemic findings"). Score hook, laughs, payoff, craft, copy and fit out of 10, organic and paid, the same way the six scored reels were done.
3. Copy `bytes`, `sha256`, the machine verdict and your scores into `library/manifest.json`. Add the carousel slides and the F13 photo as their own entries.

## 2. Fix what the audit found

These fixes are creative work only, with no generation spend. Each fixed file is a candidate until Krish locks it.

| Post | Fix |
|---|---|
| F06 x3 | Cut the passing Runway openers into the first 2 to 2.5 s (`docs/briefs/codex/2026-11-04-motion-cut-F01-F07.md`). Upscale them to 1080 first. |
| F07 | The Runway sniff clip replaces the 3.5 to 8 s still. Propose a new cover: a frame with the dog close to the painting. |
| F10 | Proposed recut: open with three messages already on screen, under 30 s, and a new cover. **Do not** replace the "WTF" lines yourself. The engine proposes new lines through `factory/bank/lines.json`, and Krish approves them. |
| F11 | Start the typing mid-word on frame 1. Use the "genius." and mug frame as the cover. |
| F04 | Move the "my golden:" cover caption above y=1440 so it survives the 3:4 grid crop. |

Leave these alone:
- **F06-dachshund product mismatch:** it needs a black-and-tan dachshund store render from heartside. Keep the post organic only and flag it in the manifest.
- **F06-lab lines:** these go to the engine and then to Krish.

## 3. Build the paid cuts (candidates, not launches)

For each test arm in `docs/PAID-BOOSTS.md` ("The first test"), build a `paid-reel` to the paid spec:
- 15 to 30 s;
- subtitles at `cap_y` ≤ 1150, with the top 14% and the sides 6% clear;
- a 3 s end card with the real store render for the same dog, the product's name and "heartside.io" (allowed on paid cuts only);
- music cleared for ads, recorded in the manifest's `paid_gates.music_ads`.

The F12 A and B pair keep their approved openings. Rebuild only their subtitles and end card to the paid spec, and say so in the manifest.

Run `factory/audit.py --paid` on each cut.

## 4. Plan the test (a document, not a campaign)

Write `local/boost/2026-11-plan.json` and a one-page summary for Krish. Cover:
- the arms;
- the exact files (by SHA-256);
- the placements;
- the audience;
- the budget per arm and the total (cap $250, including the approved $90 for F12);
- the paid UTMs (`utm_medium=paid_social`, `utm_campaign=hs_boost_202611`, `utm_content=<asset>`);
- the destination page for each arm;
- the reading schedule and the kill rule from `docs/PAID-BOOSTS.md`.

Mark each `paid_gates` value true or false with its evidence. Any false gate is listed at the top as a blocker.

## Report back

Report back with:
- the scores table for every reel (organic and paid);
- the updated `library/manifest.json`, as a pull request on a `codex/` branch;
- the list of candidates waiting for Krish's lock;
- the plan summary with its blockers.
