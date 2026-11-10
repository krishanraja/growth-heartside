# F34: the locked dog group chat structure

Krish, 10 Nov, on P04 v12: "9, file it and lock the structure". Lock: `factory/locks/F34.json`, fingerprint
`dabe3d3b9b180cba`; master `factory/specs/F34.json`; filed in 03b `Posts/F34/` and `02k` for 13 Nov.

A chat variant must keep the master's fingerprint (`python3 factory/lock.py check`). Only these slots may change:
- the cast, from the breeds the store has renders for;
- the line in each role, from approved lines tagged for the dog that says it;
- the link-preview render and the end render, for the same product type;
- the photos the dogs send (generated dogs, never a product).

Everything else is frozen: the beats, their order, timings, typing bubbles, title, sounds and layout. The first five
variants go to Krish; after that, one in ten (the trust ramp in `factory/lock.py`).

**Humour anchor** (Krish, 10 Nov): every build is written toward `docs/HUMOUR.md`: an intelligent observation, an utterly stupid premise and a slightly cruel payoff. A piece missing one of the three is not done.

## The beats

| # | Who | Role | F34's line |
|---|---|---|---|
| 1 to 4 | B, C | Cold open mid-chat on a running gag (all four on screen in frame 1) | "who ate the remote 😤" / "not me" / "doodle its in ur bed" / "the remote came to me 🥺" |
| 5 | A | The plotter announces the gift | "ok boys. moms gift lands today. act normal" |
| 6 | B | First roast of the plotter | "bro u have never once acted normal" |
| 7 | A | Link preview: the real store render (the gift) | the shepherd blanket |
| 8 to 11 | B, C | Pile-on about the gift (typing before the first) | "bro 💀" / "thats ur FACE" / "its so many of ur face 😍" / "u got her a blanket of urself 😭😭" |
| 12 | A | The plotter defends | "so she thinks of me when im not there" |
| 13 to 14 | B | Roast from shared history | "u have literally never not been there" / "u follow her to the bathroom" |
| 15 | A | Doubles down in character | "someone has to guard her in there 🫡" |
| 16 | A | Turns it on the others | "wat did U get her" |
| 17 to 18 | B | Dog B's gift, with a photo as proof | "barked at the mailman for her" + photo |
| 19 to 20 | A, B | The plotter roasts back; B defends | "u bark at him every day and take credit for it" / "and every day she lives 💪" |
| 21 to 23 | A, C | Dog C's dumb gift; the plotter calls it | "doodle?" / "i sat on her foot so she cant leave 🥰" / "doodle thats kidnapping" |
| 24 to 25 | A, C | The running gag pays off; C denies it | "also ur sitting on the remote rn" / "no im not 🥺" |
| 26 | C | The human reacts (C changes the subject) | "shes crying 😭" |
| 27 | B | Closer: a roast that turns the product into the punchline | "bro theres like 12 of ur face staring at her. thats a hostage situation 💀" |
| end | | The real product, held 4 s | the shepherd blanket |

## What makes it work (Krish's words are on the floor)

- **Lads banter** (`chat-lads-banter`): best mates with fixed personalities. Every line roasts, defends, calls back or
  escalates; nothing only moves the plot.
- **They type like mates**: a few "bro"s, emojis, lowercase, dropped apostrophes and misspellings.
- **Builds like WhatsApp** (`chat-builds-like-whatsapp`): the screen is full from frame 1, and old messages slide up
  under the header.
- **No novelty sound** (`no-novelty-sfx`): message pops and typing only; the music is added in the platform.
- **The product is the joke**: the gift is shown early, and the closer lands on it.

## A new variant, step by step

0. Build the asset library: `python3 factory/fetch_library.py <dir> --shimmer-url <url>`, with the url from the Epidemic connector's `DownloadSoundEffect` for `bf81899c-45a9-4b6f-a006-11c32d2040fd` (MP3), and set `HEARTSIDE_ASSETS=<dir>`. Variants stay blankets, because the lock freezes the product type.
1. Pick the cast, the gift (a product with a store render for the plotter's breed) and the running gag.
2. Write one line per role, true to each dog's personality, and pass `lock.copy_problems` on every line.
3. Add the lines to `factory/bank/lines.json` as proposed, tagged for the breed that says them.
4. Build with `--preview`; `lock.py check` must report only the proposed lines.
5. Judge at tier 2 against F34. The panel runs about a point below Krish on chat posts.
6. Send the variant to Krish. His yes approves its lines, and it is filed as `F34-<breed>` (DRIVE-MAP, "Post id").
