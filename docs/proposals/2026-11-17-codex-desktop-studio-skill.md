# Proposal for ai-harness: a fleet skill for driving a Codex Desktop thread

Status: proposal, for Krish. Not applied to ai-harness: this repository never edits it (Claude is the only writer to
ai-harness, through its own session).
From: krishanraja/growth-heartside, 17 Nov 2026, the production-skills session.
Source in this repository: `.agents/skills/heartside-codex-studio/SKILL.md` and three floor entries:
`codex-orders-end-at-review-points`, `no-file-picker-for-codex` and `share-the-unlimited-slot`.

## Why it belongs to the fleet

Any repository whose Claude session drives a visible Codex Desktop thread with `scripts/codex_thread.mjs` meets the same
mechanics. That includes every growth engine doing browser legwork, under the canon's Codex line (Ruling, Krish,
2026-11-15). Heartside learned them on 17 Nov at the cost of hours of an expiring Unlimited window. The lessons are
about Codex Desktop, not about Heartside.

## What the skill would say (generic form)

1. **Delivery.** When Desktop holds the thread, `codex_thread.mjs send` queues the message (ai-harness#280). A queued
   message runs only when the current turn ends. Claude cannot put a message into a running turn: `turn/steer` exists
   only on Desktop's private app-server, and the daemon `codex app-server proxy` reaches does not load the thread. Only
   the person's "Send now" in Desktop forces it.
2. **Orders end their turn at review points.** Never write "do not stop", "no pauses" or "keep going until all N are
   done". Queue the next order as soon as the current one is delivered, never more than one ahead. On 17 Nov a
   "Don't stop to report between sequences" turn ran 3 hours 20 minutes and buried four later orders.
3. **Confirm delivery.** Give each order a unique first line and grep the thread's session file for it as a user
   message, within 2 minutes. Read turn ends from `task_complete` and `last_agent_message`, never from a log pattern
   alone.
4. **Stuck queue.** Ask the person in one line to press Send now. Give mechanics at most 5 minutes. Krish, 17 Nov,
   after a 15-minute steering detour: "what are you doing? you are fucking about now surely".
5. **The browser belongs to one thread.** Only the thread the person attached the in-app browser to can use it. A
   thread opened from Claude cannot. Never open a second thread to get round a lock.
6. **Never ask Codex to upload a local file through a website.** It opens the system file picker on the person's
   screen. Krish: "why would you make it do that". Reuse what the site already holds, or have Codex set the file input
   directly.
7. **Never ask the person to pause another session's work on a shared account.** Krish: "Other jobs must continue";
   "just get on with it, the other session is producing content too but I am sure you can be co operative".
8. **Codex's report is not proof.** Check the log lines, the files and the site's own history.

## Proposed change in ai-harness

- Add `skills/codex-desktop-thread/SKILL.md` with points 1 to 8, written as a checklist.
- Link it from the canon's Codex line, next to `codex_thread.mjs`.
- Optional, for the script: a `send --confirm` flag that waits up to 2 minutes for the message to appear as a user
  message in the session file, and exits non-zero with "queued behind a running turn" if it has not. That makes point 3
  a command instead of a habit.

## What stays in Heartside

The Higgsfield, anchor-still, dog-realism, joke-lab and assembly skills are Heartside's own, and they stay in
`.agents/skills/`.
