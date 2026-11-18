---
name: heartside-codex-studio
description: How Claude sends orders to the Codex Desktop studio thread that drives Higgsfield in Krish's signed-in browser - opening the thread, queueing orders, writing orders that end at review points, confirming delivery, and what never to ask Codex to do. Use before writing or sending any message to Codex for Heartside production.
---

# Driving the Codex studio thread

Codex does the clicking in the Higgsfield website, inside Codex Desktop's in-app browser on Krish's PC. Claude writes the
orders, checks the results and records the lessons. Codex's report is never proof: check the log and the files.

## The thread

1. Talk to Codex only through `node scripts/codex_thread.mjs` (`open`, `send`, `read`). AGENTS.md, "Codex at any point".
2. Open the studio thread once a day: `node scripts/codex_thread.mjs open --cwd <STUDIO> "<title line>\n<message>"`.
   The first message says: do nothing until Krish attaches the browser, then read only and reply in one line: signed
   in yes or no, and which models show the Unlimited label.
3. Krish attaches his in-app browser to that thread and signs in to higgsfield.ai himself. Wait for him to say so.
4. Write the thread id at the top of `<STUDIO>/log.md`. 17 Nov's studio thread: `01a1e8e4-f7dd-7273-8ba5-fcf228bbe620`.
   Its session file: `~/.codex/sessions/2026/11/17/rollout-2026-11-17T09-44-42-01a1e8e4-f7dd-7273-8ba5-fcf228bbe620.jsonl`.
5. Every later order goes to that one thread. A thread opened from Claude cannot reach Desktop's browser (17 Nov, thread
   `01a1e920...`: Codex stopped, "cannot reach Desktop's in-app browser"). Never open a second thread to get round a lock.

## Sending an order

1. Write the order to a file first: `<STUDIO>/tools/order-<what>.txt`. Start it with a unique first line,
   `ORDER <date>-<slug>`, so delivery can be checked.
2. Send it: `node scripts/codex_thread.mjs send --prompt-file <STUDIO>/tools/order-<what>.txt <thread>`.
   - When Desktop holds the thread (Krish has it open), `send` queues the message for Desktop and says so. That is
     normal, and it is the route that works (ai-harness#280).
   - Fallback only if the script itself fails: `codex queue --thread <thread> --message "$(cat <file>)"`.
   - Run it as this session's own command (foreground or `run_in_background`), never `--detach` from a throwaway
     shell: on 17 Nov a detached `open` died with its shell and no thread appeared.
   - If the script fails, report it in one line. Never edit MCP, Claude or Codex settings to work round it (canon).
3. Confirm delivery within 2 minutes. Look for your first line as a user message in the session file:
   ```bash
   grep -c "ORDER <date>-<slug>" <session file>
   ```
   0 means it is still queued behind a running turn. Go to "When an order is stuck".

## How a queued message is delivered (the rule that cost 17 Nov the most)

Floor: `codex-orders-end-at-review-points`, `orchestrate-without-babysitting`, `no-file-picker-for-codex`,
`share-the-unlimited-slot`.

- A message queued while Codex is between turns runs at once. A message queued during a running turn waits until that
  turn ends. Nothing Claude can run puts a message into a running turn: `turn/steer` exists only on Desktop's own
  app-server, and the daemon `codex app-server proxy` reaches does not load the thread. Only Krish's "Send now" forces
  it.
- So:
  1. Every order ends its turn at a natural review point: at most one set, or about 6 jobs (about 90 minutes of
     Kling). End every order with "Then end the turn and tell me in one line."
  2. Never write "do not stop to report between sets", "no pauses" or "keep going until all N are done". On 17 Nov a
     42-job order with "Don't stop to report between sequences" ran one turn for 3 hours 20 minutes. Four later orders
     sat behind it, and Codex kept generating a bank Claude had already replaced.
  3. Never leave Codex idle. Queue the next order the moment a turn ends, never more than one order ahead.
  4. A change of plan goes in the next order, written to make sense after the current turn ends ("This replaces X.
     Do not run X.").
- **Codex reads a prompt file when its turn starts.** An edit made after that runs only on later turns. On 17 Nov it
  pasted the old text for `anc-gr` t1b and `anc-rv` t2. Finish every prompt file before you queue the order, or paste
  the exact prompt inside the order.

## When a turn stops: read the exact error first

Krish, 18 Nov: "its stopped jut waiting for you because you are doing a fucking poor job of orchestrating codex", and
"ok its back - get going to full autonomous completion, i have babysat you way too much".

1. Read the tool output, not Codex's summary. Codex's summary of an error is not the error. The last few tool outputs:
   `grep -o '"output":"[^"]\{0,300\}' <session file> | tail -5`
2. Find the string in this table and do its fix in one step. Never re-send an unchanged order into the same error.
3. Ask Krish only for a physical action that only he can take. Name exactly what to click, once.

| Exact error, or what Codex reports | What it means | Fix |
|---|---|---|
| "Computer Use was stopped by the user with the physical Escape key" (or "stopped with Escape") | An Escape key press on the PC sets a flag that sticks: every later turn fails on its first `cua.getState()` in 0.03 s. Re-queuing, or unlocking the PC, does not clear it (17 to 18 Nov). | One line to Krish: "Quit Codex Desktop completely, tray included, reopen it and reattach Higgsfield." Then send one order, not the backlog, and check its first submission lands. |
| "Timed out waiting for the Browser webview to attach for this browser-use page." | After a Desktop restart, the tab attached before the restart is stale. | Order a new in-app tab at the model URL (`heartside-higgsfield-ui`, section 2). If it fails twice, use another route: Krish's Chrome (floor `chrome-or-machine-for-higgsfield`), or the MCP inside a cap (floor `mcp-credit-route-with-cap`). |
| A fresh tab Codex opened "disconnected" | A new tab opened mid-session drops (17 Nov 23:06). | Use the tab Krish attached; never `createBrowserTab` while that tab works. |
| No Nano Banana Unlimited control; the page looks like a phone | A narrow tab gets Higgsfield's mobile layout. | Navigate the same tab to the model URL; if needed, set the viewport to at least 1440x900 and reload. |
| Generate shows a number ("8.75", "30") | Unlimited has closed for that model. | Submit nothing. Read the model list for Krish's fallback; if there is none, use the MCP credit route inside a cap he names. |
| Generate clicked, but nothing new in History | The job may or may not exist. | Read History through the MCP before any retry. |
| "Higgsfield tab is disconnected" or "unresponsive" | The browser lost Higgsfield. | One line to Krish: "Higgsfield dropped in Codex's browser; please reattach it." Then send the order again at once. |
| Codex says "cannot reach Desktop's in-app browser" | The thread is not the one Krish attached. | Send to the attached studio thread only. |

Overnight runs need the PC awake and unlocked, and nobody pressing keys on it. Check this with Krish before he leaves
the PC, never after the first stop. Any other Codex mechanics problem gets 5 minutes, then one line to Krish
("what are you doing? you are fucking about now surely", 17 Nov).

## Every order contains

Copy this block and fill it in. Leave nothing out: Codex follows the words literally.

```
ORDER <date>-<slug>
Claude, <date>: <one line of what and why>.
First read C:\Users\krish\dev\growth-heartside\.agents\skills\heartside-higgsfield-ui\SKILL.md (sections 2 and 5).
Use the Higgsfield tab Krish attached, at <model URL>. Higgsfield website only, <model> showing the Unlimited label.
Settings: <1080p>, 9:16, <N> s, audio off, enhance off, <text-to-video|image-to-video|image-to-image>.
Prompt: paste the whole text of each file untouched (the files are final).
Inputs: <for image jobs: which existing Higgsfield upload or History card to reuse, by asset id>.
Jobs, one at a time, submit the next as soon as History shows the last one done:
1. <prompt file> -> log as "<id> | s<N> | t<N> | DONE asset <uuid> | <model> Unlimited", save to <path>.
Check the Unlimited label at the Generate button before every click. If it shows a number (credits), or the tab is
disconnected, submit nothing and tell me in one line. Never credits, never buy a pass, never the Higgsfield connected
tool. If a click's acceptance is unverified, say so; do not click again. If a tool call fails, quote its exact error.
Then end the turn and tell me in one line.
```

## Never ask Codex to

- **Upload a file from this computer through the website.** It opens the system file picker on Krish's screen.
  Krish, 17 Nov: "why would you make it do that". Name an image already in Higgsfield (an upload, or a History card's
  reuse option, by asset id). If none exists, have Codex set the page's file input directly. Never the dialog.
- **Generate through Higgsfield's connected tool or the API.** On 17 Nov Codex tried "Higgsfield's connected tool".
  Credit generation is Claude's, through the MCP inside Krish's cap (`mcp-credit-route-with-cap`).
- **Ask Krish to pause other jobs on the account.** Krish: "Other jobs must continue".
- **Pick a model, a take or a dog.** Claude picks from the files, at full size.
- **Run a Codex card for Higgsfield.** A card's Codex cannot reach Krish's signed-in browser.

## After each turn

1. Read the turn end: `last_agent_message` of the newest `task_complete` in the session file. On a stop, read the
   exact error (the section above).
2. Check it against `<STUDIO>/log.md`. Every claimed job needs its DONE line and asset id.
3. Queue the next order now. Update `codex/INDEX.md` if the order was a card.
