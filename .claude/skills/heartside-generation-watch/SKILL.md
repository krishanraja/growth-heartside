---
name: heartside-generation-watch
description: How to monitor a long Higgsfield generation run driven by Codex - background watchers with deadlines, the 15-minute check-in, reading Codex's session file, inventory counts, tab drops and stuck queues, and what to tell Krish. Use while any studio order is running.
---

# Watching a long generation run

Floor: `check-in-every-15-minutes`. Krish, 17 Nov: "ok, keep checking in on this every 15 min to ensure everything is
ok". A run is watched, never assumed.
Three things are watched: `<STUDIO>/log.md` (Codex's DONE lines), the Codex session file (turns and messages), and
Higgsfield History (through the MCP's read calls).

Set these once per session:
```bash
S=~/.scratch/heartside-studio-2026-11-16          # <STUDIO>
F=~/.codex/sessions/2026/11/17/rollout-2026-11-17T09-44-42-01a1e8e4-f7dd-7273-8ba5-fcf228bbe620.jsonl   # the studio thread's file
```
Find a new day's file with `ls -t ~/.codex/sessions/*/*/*/rollout-*<thread id>*.jsonl | head -1`.

## Watchers: always background, always a deadline

Foreground `sleep` is blocked in Claude Code. A plain `sleep` chain does not work. Use an `until` loop with
`run_in_background: true`, and give every loop a deadline, so a missed pattern can never hang forever.

1. Wait for a job's DONE line, or 15 minutes:
   ```bash
   n=$(grep -c " | DONE" $S/log.md); end=$(( $(date +%s)+900 )); until [ "$(grep -c ' | DONE' $S/log.md)" -gt $n ] || [ $(date +%s) -ge $end ]; do sleep 20; done; date -u +%H:%M:%SZ; tail -3 $S/log.md
   ```
2. Wait for Codex's turn to end. Count `task_complete`, not DONE lines. On 17 Nov a watcher keyed only on DONE lines
   missed Codex stopping on a dropped tab.
   ```bash
   n=$(grep -c '"task_complete"' $F); end=$(( $(date +%s)+900 )); until [ "$(grep -c '"task_complete"' $F)" -gt $n ] || [ $(date +%s) -ge $end ]; do sleep 20; done; date -u +%H:%M:%SZ
   ```
3. The 15-minute check-in timer. Restart it after every check:
   ```bash
   end=$(( $(date +%s)+900 )); until [ $(date +%s) -ge $end ]; do sleep 20; done; echo "15-min check due"
   ```
4. Key every pattern on the exact log format your order asked for (`b2-xx-NN | DONE asset`). Test the grep on an
   existing line before you start the watcher: a wrong pattern waits silently until its deadline.

## The 15-minute check (under 2 minutes, every time)

1. `date -u +%H:%M:%SZ; tail -5 $S/log.md`: what landed since the last check.
2. What Codex is doing now, from the last 40 events of the session file:
   ```bash
   python - "$F" <<'EOF'
   import json,sys
   for l in open(sys.argv[1],encoding='utf-8').read().splitlines()[-40:]:
       try: d=json.loads(l)
       except Exception: continue
       p=d.get('payload') or {}
       if p.get('type')=='task_complete': print('TURN END:', (p.get('last_agent_message') or '')[:300])
       elif p.get('type')=='message' and p.get('role') in ('user','assistant'):
           print(p['role'], ' '.join(b.get('text','') for b in p.get('content',[]) if isinstance(b,dict))[:200])
   EOF
   ```
3. Is the right order running? Compare the job ids in the newest DONE lines with your latest order. If Codex is running
   a superseded order, follow `heartside-codex-studio`, "When an order is stuck".
4. Credits: MCP `balance`. It must equal the session's opening reading.
5. Download what landed (`heartside-higgsfield-ui`, section 3) and check it (`heartside-dog-realism`).
6. Restart the 15-minute timer.
7. Tell Krish only what needs him, or a one-line all clear if he asked for check-ins:
   "Checked at HH:MMZ: <n> of <planned> done, <job> generating, credits unchanged."

## Inventory (when Krish asks "how many out of how many")

```bash
grep -c "^b2-.* | DONE" $S/log.md        # done in the current bank
ls $S/bank2/prompts | wc -l               # planned
ls $S/kling3 | grep -c "^b2-"             # downloaded
```
Report the three counts, the shots still owed to scripts scoring 9, and the clips the window can still hold (4 an hour).

## Known failures and the one response to each

| Signal | Meaning | Do |
|---|---|---|
| Codex: "tab disconnected", "unresponsive", "browser access was lost" | the in-app browser lost Higgsfield | Tell Krish in one line: "Higgsfield dropped in Codex's browser; please reattach it." Then wait. Floor: `higgsfield-browser-ui-only`, "if you lose access, tell me and I reinstate it". |
| Generate shows a number ("8.75") instead of Unlimited | Unlimited dropped or lapsed | Codex stops correctly. Ask Codex to read the model list, then follow Krish's fallback order (`heartside-higgsfield-ui`). |
| A click with no History entry | the job may or may not exist | Check History with the MCP read. Never retry blind. |
| No new DONE line in 30 minutes, Codex turn still open | a stall inside the turn | Read the session file; if Codex is stuck on the page, tell Krish in one line. |
| Old order still running, new order not in the session file | the queue is behind a long turn | One line to Krish: press Send now. No investigating. |
| Sub-agent file missing at its deadline | the sub-agent is dead | Do its work yourself now (`heartside-joke-lab`, step 3). |

Krish's "I don't see anything running anywhere - here, codex or higgsfield?" came after 30 minutes when the only work
was invisible sub-agents. If nothing is generating in an Unlimited window, that is the problem to fix first.

## Never

- Never leave a watcher without a deadline, or a run with no watcher.
- Never report "on track" from Codex's last message alone: check the log and History.
- Never spend more than 5 minutes on a tooling problem before one line to Krish.
