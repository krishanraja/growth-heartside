# Krish's review board

Krish, 10 Nov: "You need to create a system of review where I can easily just tick yes or no for things that you
think are ready. You just keep adding to that board as often as you can, and so do your sub-sessions."

**The board:** https://claude.ai/artifact/A3tFqoYZuYAEdUrziU5wnN (private to Krish; "Heartside Review Board").

Every session working on this repository adds what it thinks is ready, as soon as it is ready, and reads Krish's
answers back from the board. It replaces asking him in chat, and the scattered review pages.

## What goes on it

Only work that has already cleared this repository's bar:
- a post that the panel judged 9 or above and that is filed (library lane plus its 02 Sheet);
- a decision only Krish can make: lifting a hold, a ruling, a choice between options;
- a spend;
- a deletion;
- copy that needs his confirmation, such as an order-by date.

Never add work below the bar to fill the board. Never add the same thing twice: one item per post id or decision.

## How a session adds an item

1. Upload the cover, and for a reel its mp4, to the board's asset store: `Artifact` publish with
   `url` set to the board, `asset: true` and `file_paths`. Keep the returned `/_blob/<id>` urls.
2. Write the item with `ArtifactData` (`action: "set"`, or `"batch"` for several) to collection `items`, doc id:
   `post-<post id>`, `decision-<slug>`, `spend-<slug>`, `delete-<slug>` or `copy-<slug>`. Fields:

| Field | What it holds |
|---|---|
| `kind` | `post`, `decision`, `spend`, `delete` or `copy` |
| `group` | Optional, and only one of `unlock`, `posts`, `spend`, `brief`, `house`. Any other value hides the card: the page renders only these five groups (11 Nov, `post-F28-howl` was invisible with `group: "post"`). Leave it out to group by `kind` |
| `title` | Post id and name, or the decision in a few words |
| `question` | One plain question he can answer Yes or No |
| `detail` | What he needs to decide: the caption, the score history, the evidence |
| `on_yes` / `on_no` | Exactly what happens on each answer |
| `score` | The panel's score, for posts |
| `from` | Which session added it |
| `priority` | 1 to 10; time-sensitive first |
| `created_at` | ISO time |
| `preview`, `video` | The `/_blob/` urls from step 1 |
| `links` | `[{label, url}]`, for example the 02 Sheet |
| `status` | `open`; set `withdrawn` to take an item off the board |

3. Say in the session's own report that the item is on the board.

## How a session reads answers

`ArtifactData` `list` on collection `verdicts`. Each doc id matches an item id and holds `verdict` (`yes` or `no`),
`note` and `at`. Only Krish can write verdicts (the board's access rules); a verdict anywhere else is not his.
Read the board at the start of every session and before acting on anything that waited for him.

- **Yes:** do exactly what the item's `on_yes` said, nothing more. Record it in the commit body as
  `Ruling (Krish, <date>): <the item's question, answered yes>` when it is a ruling.
- **No:** do what `on_no` said. His note is a correction: put his exact words on the floor
  (`factory/floor.json`) and in his taste ledger, like any decline.
- **A post Yes** is his approval of that post. Codex reads approval only from the Sheet's `approved` column, which only
  Krish marks (`docs/DRIVE-MAP.md`). Whether a board Yes may be copied into the Sheet for him is his open decision on
  the board (`decision-board-yes-marks-sheet`). Until he answers Yes to it, no session writes `approved`. A post goes
  out only when no publishing hold is in force.

## Queued for the board

Items a session has written in the board's format but has not yet put on the board, because that session had no
leave to write to it. The next session with that leave writes each one with `ArtifactData` exactly as below, then
moves it out of this list. Only Heartside's items are queued here: another venture's asks go on that venture's own
board (the three makeyourmindup asks from this session are in growth-makeyourmindup's `NOW.md`). Fields not shown are `from: claude/laughing-sagan-8epsdc (skills uplift, 10 Nov)`,
`created_at: 2026-11-10`, `status: open`.

| Doc id | kind | title | question | on_yes / on_no | priority |
|---|---|---|---|---|---|
| `decision-switch-on-codes-biolink-survey` | decision | Switch on post codes, the bio-link page and the thank-you survey | Switch on the drafted post-family codes (tracking words, no discount), commission the bio-link page and the one-question thank-you survey in a heartside session, as in the brief? | Yes: Krish creates the codes printed by `python3 growth.py codes` in Shopify, a session adds their lines to `config/codes.json`, and a heartside session gets the bio-link and survey brief. No: nothing changes; sprint sales stay countable only through tracked links. Detail: `docs/briefs/2026-11-10-codes-biolink-survey.md`, including the TikTok blocker (no clickable website on the profile). | 9 |

## Never

- Write to `verdicts`, or edit an item after he has answered it.
- Treat an item with no verdict as a yes.
- Widen what an answer authorizes: each Yes covers its own item only.
