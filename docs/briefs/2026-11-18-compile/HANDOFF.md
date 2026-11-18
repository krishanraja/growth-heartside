# Compile round, 18 Nov 2026: handoff to the publishing session

Written at about 10:45 UTC on 18 Nov. A new session starts here and needs no earlier conversation. Read this whole file, then follow "The path to Buffer" step by step. Nothing below is approved for publishing yet.

## Krish's instructions this round (his words, in order)

1. "I am pretty confident that if your videos are already innate and they are realistic dogs doing real dog things ... then I'll be able to get them up to higher than that, with captions over the top and good music treatment". Floor `footage-not-gated-on-judge`: footage is not gated on the model judge's 9.
2. "Producing. Just make sure you file everything immaculately so that we can compile properly and caption properly later without needing to watch everything manually to figure out what's what."
3. "Okay keep producing until the end now. Just use the CLI or MCP for everything. Get it done fast. But do not compromise on quality."
4. On the music: "what music are you adding? this will define the humour score substantialy". **He has not answered yet.** The proposal he was shown is in `music.json` and in the film table below.
5. "can you commit all of this to the repository, with absolutely nothing left to assumption for a new session to pick this up precisely from where we are and go from there to aggressive social publishing scheduled in buffer?"

## Where everything is

The footage and films are on Krish's PC, under `local/`, which is never committed. Everything needed to rebuild them is committed.

| What | Where |
|---|---|
| The 21 ready clips (FG01 to FG20), their beats, payoffs and faults | `docs/briefs/2026-11-18-footage/INVENTORY.md` and `manifest.json`; files in `local/footage/ready/` |
| The 7 new films: definition (shots, in-points, labels, caption, music) | `films.json` in this folder |
| Each film's cut brief (what `cut.py` reads) | `briefs/cp-*.md` in this folder |
| The cut tool | `assembly/cut.py` in this folder (a copy of the studio's, runnable from the repository root) |
| The exact cut commands | `cut_cmds.json` in this folder (regenerate with `python -I docs/briefs/2026-11-18-compile/tools/make_briefs.py`) |
| The built silent masters and contact sheets | `local/media/studio/<film>/<film>.mp4` and `sheet.png`; lengths and sha256 in `built.json` in this folder |
| The music beds (generated, not mixed) | `local/footage/music/*.mp3`; job ids, prompts and the stop points in `music.json` |
| The music mixer | `tools/mix_music.py` in this folder; it writes `<film>_music.mp4` beside each silent master |
| The painted end card (the store's painter, Gary on the blanket) | `local/paint/out/st-gy-09-terrier-blanket.png` with its painter record `.json` beside it |

If a `local/` file is missing, rebuild in this order (all from the repository root):
1. Clips: `python -I docs/briefs/2026-11-18-footage/tools/build_ready.py` (needs `local/footage/clips/`; every raw clip can be fetched again by its Higgsfield asset id in the footage `manifest.json`, with the MCP `show_generation_by_ids`, a credit-free read, then curl its `rawUrl`).
2. Briefs and held clips: `python -I docs/briefs/2026-11-18-compile/tools/make_briefs.py`.
3. Films: run each command in `cut_cmds.json` from the repository root.
4. Music: download each `job` in `music.json` the same way into `local/footage/music/<file>`, then run `tools/mix_music.py`.

## The films

All are 1080x1920, 30 fps, silent masters. Labels are burned in at the house's fixed top band (Karla, text top y 360). Each ends on the painted blanket, held about 3 s: `codex/check_picture.py` holds any film whose last shot is not the real product. All 7 pass every code gate in `cut.py` (gates, lock media, check_picture, timing, placeholder guard). I checked each contact sheet at full size.

| Film | Length | Shots (ready clips) | Labels (seconds: words) | Post caption | Music bed (proposed, not approved) |
|---|---|---|---|---|---|
| `cp-workday` "Gary's workday" | 17.5 s | FG11, FG10, FG06, FG04, end card | 0 to 3.5 "9:00 am. Gary starts work." / 3.5 to 7 "10:30. Deep in the files." / 7 to 10.5 "1:00 pm. A short break." / 10.5 to 12.5 "3:00. Overtime." / 12.5 to 14.5 "Doug has seen his timesheet." | He says it was a long day. | smug office lounge; stops at 12.5 s |
| `cp-copycat` "Doug copies Gary" | 18.0 s | FG08, FG05, FG03, FG13, end card | 0 to 3 "Doug copies everything Gary does." / 3 to 6.5 "Gary now sleeps under supervision." / 6.5 to 10.5 "Gary has started hiding things." / 10.5 to 15 "Doug has started taking notes." | Gary would like some privacy. | spy surveillance theme; stops at 10.5 s |
| `cp-walk` "The walk he begged for" | 13.0 s | FG01, FG02, end card | 0 to 2.5 "The walk he begged for." / 2.5 to 5 "Minute two." / 5 to 7.5 "The car, going who knows where." / 7.5 to 10 "He has never once asked." | He has strong opinions about walking. | mournful cello 0 to 5 s, then a sunny road-trip guitar |
| `cp-leaveit` "Leave it" | 12.4 s | FG07, FG03 (held 1 s), end card | 0 to 3.4 "We taught him leave it." / 3.4 to 6.4 "He left it." / 6.4 to 9.4 "He is keeping it company." | Technically a good boy. | jazzy heist theme; stops at 6.4 s |
| `cp-besttrained` "Best-trained dog" (recut of `st-bowl-c18`, which judged 8) | 12.5 s | FG17, FG14 from 1.5 s (held 1 s), end card | 0 to 2.4 "We trained him to wait before he eats." / 2.4 to 5 "Gary was not trained." / 5 to 7.8 "He's still waiting." / 7.8 to 9.5 "Our best-trained dog." | Patience is a virtue. Gary disagrees. | pompous brass march; stops at 7.8 s on Doug's stare |
| `cp-technically` "Technically on the floor" | 8.3 s | FG09a, FG09b (held 1 s), end card | 0 to 2 "House rule: no dogs on the sofa." / 2 to 5.3 "Doug is technically on the floor." | The rule did not say how much of the dog. | game-show thinking music, ticking |
| `cp-alarm` "Your alarm" | 9.0 s | FG12 (held 1 s), end card | 0 to 2.2 "Your alarm went off." / 2.2 to 6 "He has decided it was for you." | Five more minutes, for him. | music-box lullaby |
| `st-v2-c07` "Customs" (built 18 Nov, judged 8) | 9.0 s | patio clip, end card | its own (`docs/briefs/2026-11-18-films/st-v2-c07.md`) | its own | customs-inspection drone; stops at 3.5 s |

Known weak points, for the judge and for Krish:
- `cp-alarm`'s dog is a tan-faced terrier, but the end card is the painting of Gary. Only Gary's painting exists (painter limit, 2 paints a dog).
- The end card is the same painted blanket on cream for every film; the 18 Nov judges called it bolted on every time.
- `cp-workday` and `cp-copycat` run 14.5 s and 15 s before the end card; `cut.py`'s timing rule prefers 8 to 12 s (a review note, not a hold).
- In Leave it, "Under himself." was replaced by "He is keeping it company." because the treat sits between his paws, not under him.

What has **not** been done:
- No tier 1 or tier 2 panel judging of these 7 films.
- No humour-engine check: `python factory/jokelab.py doctor` reports the token is not set (CONTROL_CENTER_ENGINE_TOKEN), so `check` returns unavailable, never a pass.
- No music mixed: waiting for Krish's answer.
- Nothing on the review board, nothing locked, nothing in Drive, no Schedule rows, nothing in Buffer.

## Credits

Krish's cap for the sprint's MCP credit route is 150. Spent: 104.01 (941.35 to 837.34). That is 82.00 on anchor stills and earlier clips, then 22.01 on the music beds; the 13 footage clips were free on Unlimited. **45.99 left.** Read `balance` before any paid job and log it.

## The path to Buffer (do these in order)

The rules are in `AGENTS.md` ("Autonomy", rule 1 with the 16 to 22 Nov scoped exceptions), `docs/CHANNEL-TASKS.md`, `docs/DRIVE-MAP.md` and `docs/REVIEW-BOARD.md`. Read them first.

1. **Ask Krish two questions in one message:**
   - the music (keep the proposed beds, change some, or post silent with an in-app trending sound);
   - whether these films go on the review board whatever their judge score. His 18 Nov ruling lifts the 9 gate for footage; `docs/REVIEW-BOARD.md` and the floor (`ten-out-of-ten`) still say only 9s go on the board.
   Do not decide either for him.
2. **Music.** On his answer, run `python -I docs/briefs/2026-11-18-compile/tools/mix_music.py` (or edit `music.json` first). Keep the silent masters too: a TikTok or Reel posted natively with an in-app trending sound uses the silent master (rule 1's scoped exception, "Native posting").
3. **Judge.** Follow `.claude/skills/heartside-assembly-panel-board/SKILL.md`, section 3:
   - `python factory/panel.py sheet <mp4> --out local/factory/panel-2026-11-18/<id>.png`;
   - a tier 1 Haiku sub-agent, then a tier 2 Sonnet sub-agent with `python factory/panel.py brief tier2 <sheet>`;
   - confirm the tier 2 brief lists `V005` and the full live list;
   - record each score with `panel.py record`;
   - check every named fault at full size before believing it.
4. **Board.** Put the films Krish allowed (step 1) on the review board, https://claude.ai/artifact/6kGmidNyYAnRwiSdzAtcr4, as `docs/REVIEW-BOARD.md` says:
   - upload the mp4 and a cover to the board's asset store;
   - `ArtifactData set` an item in `items` with the question, the caption, the tracked link (`python growth.py link "<landing url>&hook=<hook>" <CREATIVE_ID>`; find the next free creative id in `local/creatives.csv` and the Schedule) and the scores.
   - Read his verdicts from `verdicts`; never write there.
5. **Lock and file.** For each film Krish says yes to:
   - **Post id.** Take the next free id: F60 onward. F52 to F59 are in `02t`, and F46 to F51 are taken. Confirm against Drive `Posts/` (folder `1boYZjB7ma-1YIcKzSl51usdYuNk6faHO`) and `factory/specs` first.
   - **Files.** Build the library folder as `heartside_<id>_<slug>_reel.mp4` and `_cover.jpg`, with `manifest.json` (post, file, bytes, sha256).
   - **Send.** Run `python3 factory/send_library.py <folder>` on Krish's home computer. Then check `03b_Social-Schedule/Posts/<id>/` within about 20 minutes.
6. **Schedule rows.**
   - Make a new Sheet `02u Schedule and captions (<ids>)` in `03b_Social-Schedule` with the same 16 columns as `02`. `02s` is reserved for the volume session; `02t` is the latest.
   - Rows go to Instagram, Facebook and TikTok, in the existing US Eastern slots and inside the sprint cadence: 20 posts a day in total, 5 per platform, through 22 Nov (`AGENTS.md`). Alternate send-led and gift-led rows, and keep every locked slot.
   - A row whose sound is added in the app has the silent reel and a `notes` field starting `SONG`.
   - Write a new "00 README for Codex" version that names `02u`, and rename the old one "(superseded …)".
   - Run the Drive audit (`docs/DRIVE-MAP.md`, "Auditing").
7. **Approval.** Krish marks `approved = yes` in `02u`. Alternatively, for the sprint, he says "Approve daily batch" for an exact day's batch. Nothing is scheduled without one of the two.
8. **Buffer.**
   - **Who sends it.** Only a Claude session on Krish's own computer sends the approved batch to the Publishing desk: Codex thread `01a1a23e-de37-74f1-95a8-4a9bed2e756d`, through `node scripts/codex_thread.mjs send 01a1a23e-de37-74f1-95a8-4a9bed2e756d "<exact rows>"`.
   - **What Codex does.** It schedules them in Buffer, the only writer there. Then it reads each one back live and records a `post_check`.
   - **Claude's part.** Import its `docs/social/` event file (`growth.py events import`) and write `status`, `live_url`, `notes` and `Results` in the Sheet.
   - **Buffer MCP.** This session has a Buffer MCP connected (`create_post` and others). The 15 Nov ruling makes the Publishing desk the only writer to Buffer, so do not use it unless Krish rules otherwise in his own words.
9. **Learn.** Read each post at 24 hours, 72 hours and 7 days (`docs/CHANNEL-TASKS.md`, "Publish once; learn from the result"). Record every verdict of Krish's on the floor and in his taste ledger.

## Progress, 18 Nov afternoon (publishing session)

- Step 1 answered. Music: Krish, "I want to hear the audio with the video to make sure its good first". Review board: "Yes, all 8 regardless" of the judge score.
- Step 2: `mix_music.py` run for all 8 (beds as proposed in `music.json`); `<film>_music.mp4` sit beside the silent masters, which are kept. Sent to Krish to hear. Music is still not approved.
- Step 3: judged. Tier 1 (Haiku) faults checked at full size: "AI-drawn blanket" false on all 8 (the painter's real blanket); Customs' first frame and copycat's "frozen frames" false. Tier 2 (Sonnet; every brief listed V005): cp-besttrained 8; cp-workday, cp-walk, cp-leaveit, cp-technically, cp-alarm, st-v2-c07 7; cp-copycat 6. Recorded in `local/factory/panel.jsonl`. Workday's retread of the live 9 to 5 posts (V002, F43; V003) is real. On Windows, `panel.py brief` needs `PYTHONIOENCODING=utf-8` (an emoji in the live list).
- Tracked links: concepts C209 to C216 in film order, one creative id per platform, in `local/factory/panel-2026-11-18/links-compile.txt`. Confirm the concept numbers against the 02t Schedule before filing.
- Step 4: all 8 are on the review board (doc ids `post-<film>`), each playing its music mix, with caption, scores, best beat, faults and links. The humour engine is unavailable (no `CONTROL_CENTER_ENGINE_TOKEN`), said on each card.
- Next: read `verdicts` on the board; for each Yes, step 5 (post id F60 onward). A post Krish adds a recognisable track to in the app also goes on his phone posts page (`docs/REVIEW-BOARD.md`).
