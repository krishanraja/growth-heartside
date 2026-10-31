# Codex card: mockups for C25 "The Seating Plan", in ChatGPT images

31 Oct 2026. Krish: "Higgsfield should be for actual production. Mockup should be done in ChatGPT images through
the Codex plugin." Run by Krish's WSL session (or Codex directly) in `~/growth-heartside`. It makes mockup stills
only. It posts, sends and spends nothing beyond the ChatGPT images it generates, and it never draws the product.

## The concept

**C25, The Seating Plan.** This is a new concept, not yet approved: these mockups are what Krish approves. It uses
the format of the Short Krish keeps seeing: one static wide shot in a real home, the dog as the actor, and a payoff
beat at about 7 seconds. Heartside's rules change the joke. It never lands on the person (no mocking the buyer), and
the product is never drawn: the film hard-cuts to the real gift.

| Beat | Seconds | What is on screen |
|---|---|---|
| 1 | 0 to 3 | Static wide shot of a lived-in US living room at Christmas. A person (seen from behind, no face) stands up from the couch to get a drink. The black lab from `assets/heartside-examples-2026-10-29/photos/lab.jpg`, red bandana, slides into the warm spot. |
| 2 | 3 to 5 | Same shot. The person returns, gives a look, and sits at the far end. The dog stretches its legs across the cushions. |
| 3 | 5 to 8 | Same shot. The person ends up sitting on the rug, laughing, with the dog's head now on the armrest like a king. |
| 4 | 8 to 12 | Hard cut to the real product: `assets/heartside-examples-2026-10-29/mockups/lab-sentimental-blanket/home-9x16.png`, unchanged, labelled "Example: shown with an example dog". The dog's line in Courier Prime: "I keep your seat warm, so this year you get your own blanket of me." Signed "Love, your dog". |

## What Codex makes

Three 9:16 stills, 1080 x 1920, photographic, warm late light, low and wide, shallow focus where it helps. These
are one per beat 1 to 3, the same room and camera position in all three, so they read as one static shot.

- Use `lab.jpg` as the reference for the dog in every still, so it matches the painted blanket.
- The person is seen from behind or below the shoulders only. No face and no brand.
- No text, logo or product in any still. No blanket printed with a dog: the couch throw is plain knit.
- Save them as `local/production/stills/c25-beat1.png`, `c25-beat2.png` and `c25-beat3.png`, plus a
  `c25-prompts.txt` with the exact prompts used.

Then run `python3 local/production/make_frames.py` only if the cloud session asks. The cloud session assembles the
board frames and shows Krish.

## Checks before reporting back

- `python3 -c "from PIL import Image; [print(f, Image.open(f).size) for f in ['local/production/stills/c25-beat1.png','local/production/stills/c25-beat2.png','local/production/stills/c25-beat3.png']]"`
  prints 1080x1920 (or 9:16) for all three.
- The dog has a red bandana and is a black lab in all three, and the room is the same room.
- Report to the cloud session (`session_01JRhKyrhj4rSrionhqLcWXH`) with the three file paths and the prompts.
  Nothing is committed: `local/` is ignored.
