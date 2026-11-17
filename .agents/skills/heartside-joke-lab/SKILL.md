---
name: heartside-joke-lab
description: Where Heartside's humour comes from and the exact joke lab run (brief, writers, screen, words-only judge, Krish) that every film's words go through before any frame is made. Covers the sub-agent watchdog, the shortlist fix and the formats already capped by live posts. Use before writing any concept, label, caption or script.
---

# The joke lab: words first, judged alone

Full method: `factory/README.md`, "The joke lab". The joke itself: `docs/HUMOUR.md`. This skill is the run order and the
traps that cost 17 Nov about 5 hours.

## Where the humour comes from (read in this order)

1. `docs/HUMOUR.md`: every piece needs an intelligent observation, an utterly stupid premise and a slightly cruel payoff.
2. Krish's formula, 17 Nov: "that prior video worked because it was a parody of shameless LinkedIn influencers, but real
   dog behavior". The parody is in the words. The dog does real dog things, photoreal and scruffy, never dressed up.
3. The floor's joke and concept entries: `python growth.py floor --format reel`.
4. What he has said yes and no to: `python factory/jokelab.py taste`.
5. The families that earn: alibi leads (`docs/audits/2026-11-15-interest-vs-paid.md`).
6. The live posts. A new piece must not retread one (`no-retread-of-live-post`). F38 "My dog's 4 AM routine" owns
   "LinkedIn parody over a real dog". On 17 Nov 121 LinkedIn scripts all capped at 8 against it. Do not brief that
   format again unless the brief names how it beats F38.
7. Fresh territory Krish named on 17 Nov, one stereotype per set:
   - the fake candid routine;
   - the "OMG I'm obsessed" reviewer;
   - overused hooks;
   - out-of-touch privilege;
   - staged charity;
   - main character in public;
   - disruptive gym filming;
   - the copy-paste caption fail;
   - filtered body positivity.

## The run

Set up first: `export PYTHONIOENCODING=utf-8` (without it, `jokelab.py` crashes on Windows).

1. **Brief.** `python factory/jokelab.py brief "<concept or set>" --n 30 > local/jokelab/briefs/<slug>.txt`.
   For footage that already exists, name the clip ids the words must sit on (`b2-rv-06` and so on) in the topic.
2. **Writers.** Give each brief to one sub-agent (Sonnet). Tell it to write the JSON list to
   `local/jokelab/cand-<slug>.json`, then reply with its own top pick and why.
3. **Watchdog (never skip).** Start a background watcher with a 15-minute deadline the moment the writers start:
   ```bash
   end=$(( $(date +%s) + 900 )); until ls local/jokelab/cand-<slug>.json >/dev/null 2>&1 || [ $(date +%s) -ge $end ]; do sleep 20; done; ls -la local/jokelab/cand-*.json
   ```
   If the file is missing at the deadline, the writer is dead. A user interrupt kills sub-agents silently. Write the
   candidates yourself in the main session; 30 short scripts is a few minutes' work.
   - On 17 Nov the writers died and nobody checked for about 2 hours. Krish: "what takes jokes 2 hours to write
     exactly?"
4. **Screen.** `python factory/jokelab.py screen --run <slug>-r1 local/jokelab/cand-<slug>.json` (add `--live` only if
   `CONTROL_CENTER_ENGINE_TOKEN` is set on this machine).
   - Always pass `--run` with a unique name. Without it, runs are named by the second, and two screens in the same
     second overwrite each other (17 Nov).
   - No token: the screen runs its code gates and says so. Report that in one line and go on. Never fake a live read.
5. **Shortlist.** `python factory/jokelab.py show <run>`. The ranker takes the top 4 by family weight and over-weights
   the alibi family. Add each writer's own top pick to the judge set if the ranker left it out. On 17 Nov
   "Didn't see you there" scored 9 only because it was added this way.
6. **Judge the words alone.** Write each shortlisted script to `local/jokelab/words-<cand>.md`: the lines, the shot
   list and the closest live post. Nothing else.
   - `python factory/panel.py brief tier2 local/jokelab/words-<cand>.md` gives the Sonnet judge's prompt; run it as a
     sub-agent.
   - Add no session notes, no excuses, no "fully human acts are allowed". On 17 Nov notes like that talked the judge
     from 7 to 9 on a retread, and Krish declined it.
7. **Gate.** Only a 9 on the words goes forward. Below 9: write a new round with a different mechanism. Do not polish
   the same lines. After two rounds capped at 8 for one structural reason, shelve the concept and say why in one line.
8. **Check the line, if the tool exists.** Run `python factory/jokelab.py --help`. If it lists `check`, run
   `python factory/jokelab.py check "<line>" --surface caption --on-screen "<what the dog does>"` before a caption goes
   on the board.
9. **Krish.** Put the 9s to him with the footage plan. Record each verdict, his words exact:
   `python factory/jokelab.py verdict <run> <cand> yes|no "<his words>"`.
10. **Build cuts.** For every cut of a built film, log
    `python factory/jokelab.py cut <run> <cand> --score N --words <file>`. If it exits 1 (the score moved but the words
    did not, or three cuts with the same words), stop building and go back to step 1.

## Writing rules the screen will not catch

- One script, one stereotype, one register (`one-register-never-blurred`).
- Every label states plainly what the dog is supposedly doing (`deadpan-labels`), and the footage shows the dog doing
  it (`stage-the-joke`).
- The cruel payoff lands on the owner's habits, never their body, looks, age, money, job or family (AGENTS.md rule 5).
- US spelling, no em dashes, no exclamation marks, no swearing on screen.

## Never

- Never build an inherited idea without running it through the lab. Krish, 17 Nov: "No, it's not funny - the post that
  is already live on this topic is 10x better".
- Never hold Unlimited footage generation while the words are being written (`heartside-video-production`, section 3).
  The lab gates credits and builds, not real-dog footage on Unlimited.
- Never send Krish a piece you would not bet he laughs at.
