# Codex card: concept mockups for C20 to C25, in ChatGPT images

31 Oct 2026. Krish: "Higgsfield should be for actual production. Mockup should be done in ChatGPT images through
the Codex plugin." Run by Krish's WSL session (or Codex directly) in `~/growth-heartside`. It makes mockup stills
only. It posts, sends and spends nothing beyond the ChatGPT images it generates, and it never draws the product.

## The order (Krish, 31 Oct)

"I want concept design done in codex chatgpt images first, so I can see we are on the right track, only then we use
runway and higgsfield." So Codex makes every concept's opening stills in ChatGPT images. Krish reviews them on the
concept board, and only then does any Runway or Higgsfield motion run.

## C20 to C24: the opening stills

These are one 9:16 still per concept, plus one per breed for C23. The same rules apply to every still: photographic, a
lived-in US home at Christmas, a low camera at the dog's eye level, warm light, shallow focus, and no text, logo or
product. The dog matches its reference photo in `assets/heartside-examples-2026-10-29/photos/` exactly, so the real
painting at the end is visibly the same dog. People appear only as hands, feet or from behind.

| File (`local/production/stills/codex-…png`) | Reference photo | Scene |
|---|---|---|
| `c20` | `lab.jpg` (red bandana) | asleep across a woman's feet in cream wool socks on a rug, Christmas morning, tree lights out of focus |
| `c21` | `golden.jpg` | chin resting on an older woman's knitted slippers by a fireplace, her hand on its head, stockings behind |
| `c22` | `frenchie.jpg` (small blue bow tie) | sitting in torn red and gold wrapping paper under a lit tree at night, guilty face, ribbon on its head |
| `c23-golden` | `golden.jpg` | trotting toward the camera down a hallway carrying one fuzzy slipper |
| `c23-shepherd` | `shepherd.jpg` | sitting upright by the front door at 7 am like a supervisor, wreath on the door |
| `c23-dachshund` | `dachshund.jpg` | head and front half inside a paper grocery bag on a kitchen floor, tail up |
| `c23-doodle` | `doodle.jpg` | on a sofa giving an unimpressed side-eye to a pile of loud Christmas sweaters |
| `c24` | `lab.jpg` (red bandana) | at a front window at dusk, from behind, headlights in the snow outside |

## C25: the new concept

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
