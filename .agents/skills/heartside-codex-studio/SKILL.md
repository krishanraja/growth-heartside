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

Floor: `codex-orders-end-at-review-points`, `no-file-picker-for-codex`, `share-the-unlimited-slot`.

A queued message runs only when Codex's current turn ends. Nothing Claude can run puts a message into a running turn:
- `turn/steer` exists, but only on Desktop's own app-server, behind a private pipe;
- the daemon that `codex app-server proxy` reaches does not load the thread.

Only Krish can force a queued message in, by pressing "Send now" on it in Codex Desktop. So:

1. Every order ends its turn at a natural review point: at most one set, or about 6 jobs (about 90 minutes of Kling).
   End every order with: "Then end the turn and tell me in one line."
2. Never write "do not stop to report between sets", "no pauses" or "keep going until all N are done". On 17 Nov a
   42-job order with "Don't stop to report between sequences" ran one turn for 3 hours 20 minutes. Four later orders
   sat in the queue behind it, and Codex kept generating a bank Claude had already replaced.
3. Keep the line moving by queueing the next order straight after the current one is delivered, never more than one
   order ahead. Two or more queued orders mean a correction waits behind all of them.
4. A change of plan goes in the next order, not as an interruption: write it so it still makes sense after the current
   turn ends ("This replaces X. Do not run X.").

## When an order is stuck

- If the order has not landed after 10 minutes and a wrong job is running, tell Krish in one line:
  "In the Codex studio thread, press Send now on my queued message '<first line>'."
- Do not investigate steering, app-server, sqlite queues or process trees. On 17 Nov a 15-minute detour into steering
  produced nothing usable. Krish: "what are you doing? you are fucking about now surely". Krish expects messages to be
  forced through ("you should be able to steer comments (force them through) when you need to otherwise each new
  message you try just gets backed up in a queue"). Today the only way is his Send now, so ask him for it in one line.
- Any Codex mechanics problem gets 5 minutes, then one line to Krish, then back to the work.

## Every order contains

Copy this block and fill it in. Leave nothing out: Codex follows the words literally.

```
ORDER <date>-<slug>
Claude, <date>: <one line of what and why>.
First read C:\Users\krish\dev\growth-heartside\.agents\skills\heartside-higgsfield-ui\SKILL.md (sections 2 and 4).
Higgsfield website only, <image|video> page, <model> showing the Unlimited label.
Settings: <1080p>, 9:16, <N> s, audio off, enhance off, <text-to-video|image-to-video|image-to-image>.
Prompt: paste the whole text of each file untouched.
Inputs: <for image jobs: which existing Higgsfield upload or History card to reuse, by asset id>.
Jobs, one at a time, submit the next as soon as History shows the last one done:
1. <prompt file> -> log as "<id> | s<N> | t<N> | DONE asset <uuid> | <model> Unlimited", save to <path>.
Check the Unlimited label at the Generate button before every click. If it shows a number (credits), or the tab is
disconnected, submit nothing and tell me in one line. Never credits, never buy a pass, never the Higgsfield connected
tool. If a click's acceptance is unverified, say so; do not click again.
Then end the turn and tell me in one line.
```

## Never ask Codex to

- **Upload a file from this computer through the website.** It opens the system file picker on Krish's screen. Krish,
  17 Nov: "codex opened file upload, expecting an anchor image to be uploaded", then "why would you make it do that".
  Instead, name an image already in Higgsfield: an earlier upload, or a History card's reuse option, by asset id. If
  none exists, have Codex set the page's file input directly ("storage upload only", the way the 17 Nov shot 2 start
  stills went in). Never the dialog.
- **Generate through Higgsfield's connected tool or the API.** On 17 Nov at 12:29 Codex tried "Higgsfield's connected
  tool", which rejected an Unlimited Kling job. Unlimited exists only in the website (`higgsfield-browser-ui-only`).
- **Ask Krish to pause other jobs on the account.** The Unlimited slot is shared with his other ventures. Krish, to
  Codex on 17 Nov: "Other jobs must continue", then "just get on with it, the other session is producing content too
  but I am sure you can be co operative". Codex waits for the slot to free, then submits.
- **Pick a model, a take or a dog.** Claude picks from the files, at full size.
- **Run a Codex card for Higgsfield.** A card's Codex cannot reach Krish's signed-in browser; only the Desktop thread
  can. Cards are for builds (`codex/README.md`).

## After each turn

1. Read the turn end: `last_agent_message` of the newest `task_complete` in the session file.
2. Check it against `<STUDIO>/log.md`. Every claimed job needs its DONE line and asset id.
3. Update `codex/INDEX.md` if the order was a card.
