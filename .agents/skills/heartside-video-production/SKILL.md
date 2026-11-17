---
name: heartside-video-production
description: Start here for any Heartside film or footage work (planning, generating in Higgsfield through Codex, judging, cutting, putting on the review board). Sets up the machine, gives the order of the other heartside-* skills, plans an Unlimited window, and says how to record every correction. Built from the 17 Nov 2026 sprint session's failures so a cheaper model can run production.
---

# Heartside video production: the entry checklist

Follow the steps in order. Each step names the skill that holds the detail. Do not skip a step because it seems obvious:
every step here exists because a session on 17 Nov 2026 skipped it and Krish paid for it.

## 1. Before anything (5 minutes, no more)

1. Read `AGENTS.md` to the end, then `docs/NORTH_STAR.md` and the first line under "Where it is right now" in `NOW.md`.
2. Say in one line which part of the North Star the work moves.
3. Set up the shell. On Krish's Windows PCs:
   - use `python`, never `python3` (`python3` opens the Microsoft Store);
   - run `export PYTHONIOENCODING=utf-8` first in every Bash call that runs `jokelab.py`, `growth.py` or `panel.py`
     (without it they crash on cp1252 with UnicodeEncodeError).
4. Read the rules that apply, in this order:
   - `python growth.py floor --format reel` (or `still`): Krish's corrections, with his words;
   - `docs/HUMOUR.md` before writing any word on screen;
   - `codex/INDEX.md` before any Codex work;
   - the studio log tail: `tail -40 <STUDIO>/log.md`.
5. Find the studio folder (`<STUDIO>`). For the 16 to 22 Nov sprint it is `~/.scratch/heartside-studio-2026-11-16/`.
   Its Drive copy is `H:\My Drive\Ventures\Active Ventures\Heartside\03a_Social-Production\2026-11-16_Claude-Velocity-Sprint-Studio_Not-for-Publishing\`.
   Start only from a complete copy: if Drive is still syncing, say so and wait.
6. Work on the day's branch, never on `main`. A sub-session you start must be cut from that same branch
   (`start_session` with `source_branch: <day branch>`). On 17 Nov one was cut from `main`, missed the day's floor
   entries, and failed to start.

## 2. The order of work

| Step | Skill | Stop when |
|---|---|---|
| Words | `heartside-joke-lab` | a script scores 9 on its words alone, or the concept is shelved |
| Footage plan | this skill, section 3 | the set list, the dogs and the priority order are written |
| Unlimited check | `heartside-higgsfield-ui` | Codex has read today's Unlimited models, with the time |
| Anchor stills | `heartside-anchor-stills` | one approved anchor per set, checked at full size |
| Dog check | `heartside-dog-realism` | every anchor and take passes the realism list |
| Orders to Codex | `heartside-codex-studio` | each order is confirmed delivered in the session file |
| Watching the run | `heartside-generation-watch` | every job is logged DONE and downloaded |
| Cut, judge, board | `heartside-assembly-panel-board` | every 9 is on the board with tracked links |

Words and footage run in parallel, never one after the other (section 3).

## 3. Plan an Unlimited window

Krish's Unlimited plans expire (Kling 3.0 Unlimited ran 16 to 17 Nov only). An idle window is lost output.
Floor: `generate-while-the-words-are-written`, `share-the-unlimited-slot`.

1. Throughput: Higgsfield runs one Unlimited job at a time for the whole account, shared with Krish's other ventures.
   A Kling 3.0 job takes 12 to 15 minutes; a Nano Banana still about 5 minutes. So plan about 4 video clips an hour.
   Write the number of clips the window can hold before writing the order.
2. Start generation in the first 15 minutes. Footage of a real dog doing an ordinary dog thing does not depend on which
   words win, so queue it while the words are still being written.
   - Krish, 17 Nov, after 30 minutes with nothing in Codex or Higgsfield: "I don't see anything running anywhere -
     here, codex or higgsfield?"; then "ok, we need to get moving with kling generations now we have 6 hours remaining
     of use!"
   - `spend-means-nine` (no credit spent before a 9 on the words) governs credits. Unlimited jobs spend no credits.
3. Plan footage as a bank by set: one influencer stereotype per set, real dogs doing ordinary things, captions added
   later. Krish, 17 Nov: "generate loads of good videos of dogs behaving regularly but cut in to sequences that look like
   typical female influencer videos, that we can add hilarious captions over later on".
4. One hero dog across all sets, so scenes mix across films. A sidekick only where the set needs two dogs. Use the dogs
   Krish has already passed (`heartside-dog-realism`, "The cast"), never a new roll in a timed window.
5. Priority order: the shots that serve scripts already scoring 9 run first, then the rest of the bank.
6. Write the plan to `<STUDIO>/log.md` as one `Claude |` line: the window's end time, the clip count, the order.

## 4. Every correction is recorded in the same commit

When Krish corrects, declines or swears at something:

1. Quote his exact words. Never paraphrase them in a record.
2. Add them to `factory/floor.json` with a targeted text edit, never `json.load` then `json.dump` of the whole file
   (on 17 Nov that reformatted all of it twice and had to be reverted with `git checkout factory/floor.json`):
   ```python
   import json
   p = 'factory/floor.json'; s = open(p, encoding='utf-8', newline='').read()
   e = {"id": "...", "date": "YYYY-MM-DD", "made": "...", "words": ["his exact words"], "category": "process",
        "rule": "...", "check": "review: ...", "applies_to": ["reel", "still"]}
   block = '\n'.join('  ' + l for l in json.dumps(e, indent=1, ensure_ascii=True).split('\n'))
   i = s.index('\n ],\n "open_conflicts"'); s = s[:i] + ',\n' + block + s[i:]
   open(p, 'w', encoding='utf-8', newline='').write(s); json.load(open(p, encoding='utf-8'))
   ```
   Then `git diff --stat factory/floor.json` must show insertions only. If the rule already exists, add his words to
   that entry's `words` list with a one-line string replace instead.
3. Send the same words to his taste ledger with `report_to_taste_engine` (repository `krishanraja/growth-heartside`,
   venture `heartside`, where and when he typed them).
4. Commit the floor change with a body line `Ruling (Krish, YYYY-MM-DD): <the ruling, in one line>`.
5. Check: `python growth.py --self-test`. A failure on a knowledge `.docx` hash was already there before 17 Nov.
   Report it as pre-existing and do not touch that file. Any other failure is yours to fix.

Reporting to the taste ledger is not enough on its own. Krish, 17 Nov: "You're reporting everything to the taste engine
like some sort of teacher's pet, but are you actually enhancing the fucking brain of this fucking repository where we
fucking produce the fucking videos?" A lesson becomes a floor entry, a fix to a tool, or a line in one of these skills.

## 5. Talking to Krish

- Message him only when he must act or decide, or when a clip lands that he asked to see. Give him one line for a
  blocked tab or a stuck order (`heartside-generation-watch`).
- When he asks "going ok?", answer with counts, from the log: done of planned, failed, the next job, and credits unchanged.
- Never claim a step is done from a report: Codex's report is not proof. Check the log line, the session file or the
  downloaded file.

## 6. Close-out

1. Update `codex/INDEX.md` with every card or studio order's state.
2. Write `now-notes/YYYY-MM-DD-<slug>.md`: `Status:`, `Next:` the single next step, and one North Star check line.
3. Commit, push the day branch, and open or update its pull request.

## Never

- Never retread a post that is already live: see `no-retread-of-live-post` on the floor. Krish: "No, it's not funny -
  the post that is already live on this topic is 10x better".
- Never polish pictures when the words are not funny: see `jokelab.py cut`. It took 5 hours and seven cuts on one idea on
  17 Nov. Krish: "Is this what you've spent the last 5 hours on that one video?"
- Never drive Krish's screen with computer use, and never post, schedule or spend (AGENTS.md rule 1).
