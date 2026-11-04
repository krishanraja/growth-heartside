# The road to posting: every asset, from candidate to live (4 Nov 2026)

This plan covers what remains between today's library and everything going out at its best, organically and in the $250 paid test.

Who does what:
- **"Engine"** is the growth engine in an interactive session. It audits, builds and files through the library lane.
- **"Codex"** schedules, posts and launches.
- **"Krish"** locks, approves and presses go-live.

Nothing goes out without the approval named in its step.

## Where things stand

| Group | Posts | State |
|---|---|---|
| Live | F10 (3 Nov, all three platforms) | Old cut. Leave the post up; fix the next cut |
| Scheduled in Buffer with the locked media | F06-frenchie (4 Nov), F11 and F07 (5 Nov), F06-dachshund and F12 (6 Nov), F03 and F06-lab (7 Nov), F05 (8 Nov), F01, F02 and F04 (moved earlier) | Going out as locked, with still openers |
| Engine's motion versions | F01, F02, F03, F06 x3, F07 reels; F07, F10, F11 covers | **Locked by Krish on 4 Nov and filed** to `Posts/<id>/` under their plain names; hashes read back from the library |
| Codex's motion candidates | F04, F05, F12; the F12 A/B pair | On Codex's board. Coming to the library as `review-` files (`docs/briefs/codex/2026-11-04-drop-for-review.md`) |
| Needs new lines (Krish approves lines) | F10 (the four "WTF"s), F06-lab (two lines) | The engine proposes the lines |
| Needs heartside | F06-dachshund's ending: a black-and-tan dachshund render | Brief: `docs/briefs/2026-11-04-heartside-dachshund-render.md` |
| Boost test | F12, F05, F02 and the F06-frenchie carousel, boosted as live organic posts | Plan ruled; launch packet ready (`docs/boost/2026-11-launch-packet.md`); Codex drafts the ads, then Krish says go |

## The steps

1. **Done (4 Nov): Krish locked today's engine candidates.**
   - Watch the 10 files and reply "lock" (all), or name which.
   - Any he declines stays as it is. His words go in `CHANGES.md` and the commit.
2. **Codex sends its candidates for review** (the Codex card, 15 minutes). Then the engine audits them, scores them, and puts motion-or-still for F04, F05 and F12 to Krish with the evidence.
3. **The engine files every locked version.**
   - It sends each one through the library lane under its plain name (`heartside_<id>_<slug>_reel.mp4` / `_cover.jpg`), replacing the locked file in place (Drive map rule 4).
   - It writes `factory/locks` evidence and updates `library/manifest.json` with the new SHA-256s.
   - The schedule rows need no change: the file names stay the same.
4. **No edits to the live queue** (Krish, 4 Nov, after a Buffer media swap failed).
   - Posts already queued in Buffer publish as queued, with their approved locked media.
   - The locked motion versions go out from the next schedule batch onward, through new rows that name the Drive files.
   - Nobody re-attaches media in the queue.
   - The one queued item a failed swap had broken (F03 Instagram, 7 Nov) was put back on its approved Buffer-hosted reel on 4 Nov and read back.
5. **New lines.**
   - The engine proposes replacement lines for F10's "WTF"s and F06-lab's two weak lines in `factory/bank/lines.json` (status `proposed`, checked by `growth.py check`). Krish approves or kills them.
   - Then the engine rebuilds F10 so it opens on a full chat with no blank second, under 30 s, and F11 so it opens mid-search. It re-cuts F06-lab with the new lines.
   - Each one goes to Krish to lock, then repeats steps 3 and 4.
6. **The F06-dachshund ending.** When heartside delivers the black-and-tan render, the engine rebuilds the ending, Krish locks it, and steps 3 and 4 repeat. Until then the post stays organic only.
7. **Boost drafts** (Codex, `docs/briefs/codex/2026-11-04-boost-drafts.md`).
   - As each arm's Instagram post goes live, Codex builds its ad in Ads Manager as a draft, exactly as the launch packet says: use the existing post, Shop now, the packet's URL.
   - It fills in the permalink and ad ID, and confirms the post's media matches its locked file.
   - Nothing is published.
8. **Boost go.**
   - Krish says go on the filled packet. Codex publishes each draft, once.
   - The engine reads day 2, day 3 (kill rule) and day 5, with paid traffic kept out of the North Star number.
9. **Every post, ongoing.** Codex posts each approved row as built and writes back status and permalink. The engine reads the results at 24 hours, 72 hours and 7 days, and the Sunday report decides what gets more breed versions.

## What could still stop a post

- **Rows already in Buffer keep their original locked media** and publish that way: still openers, but approved.
- **The TikTok captions say "Link in bio".** Codex's 3 Nov audit found no clickable website on the profile, so a TikTok viewer who wants the gift has nowhere to tap. It is not a blocker for posting: drop "Link in bio" from TikTok captions or add the link, either is fine.

North Star check (2026-11-04): this plan moves the North Star part "every winning format was found by this engine and approved by Krish in one press": every asset gets to its best version, and the paid test finds which format to scale for free. The number has not moved.
