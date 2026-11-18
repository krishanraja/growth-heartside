# Footage inventory, 18 Nov 2026: locked for compilation

Status: locked on 18 Nov. This is everything the 16 to 22 Nov sprint made that is usable, in one place, for the compile session. That session adds captions over the top and music, then the films are judged and go on the review board.

Krish, 18 Nov: "I am pretty confident that if your videos are already innate and they are realistic dogs doing real dog things ... then I'll be able to get them up to higher than that, with captions over the top and good music treatment". Footage is no longer gated on the model judge's 9 (floor `footage-not-gated-on-judge`).

## Where it is

On Krish's PC, under the repository (`local/` is never committed):

| Folder | Holds |
|---|---|
| `local/footage/clips/` | every usable clip, silent mp4, 9:16 |
| `local/footage/anchors/` | the approved anchor still for every clip (the first frame) |
| `local/footage/review/` | a 10-frame contact sheet per clip (`<clip>.jpg`) |
| `local/footage/prompts.tsv` | the exact motion prompt for every new clip |
| `local/footage/st-gy-09-terrier-blanket.png` | the painted end card (the store's own painter, this terrier on the blanket) |
| `local/media/studio/<id>/` | the six cut films of 17 to 18 Nov (`docs/briefs/2026-11-18-films/README.md`) |

Every clip can be fetched again from Higgsfield by its asset id: MCP `show_generation_by_ids` (a credit-free read), then curl its `rawUrl`.

## The cast

- **The terrier** (the hero): a gray and white scruffy terrier mix, orange collar. Called "Gary" in the bowl films.
- **The doodle** (sidekick C): a chocolate shaggy poodle and spaniel mix. Called "Doug" in the yoga film.
- The bedroom clip's dog is a lighter, tan-faced terrier from an earlier anchor. Use it alone, never cut next to the hero as the same dog.

## The clips

Quality: Kling 3.0 clips are 1080x1920 (1088x1904 from the website). Kling 2.5 Turbo clips are 716x1284 (720p, upscale at export).

### New on 18 Nov (one clip per anchor, all free on Unlimited)

| Clip | Asset | Model | What happens | Verdict | Usable | Known fault |
|---|---|---|---|---|---|---|
| `fg-parkpath_t1` | `12c00ac4` | Kling 2.5 Turbo | The terrier lies flat on a park path, leash taut from above; he will not move, only his eyes roll | pass, the most real clip of the round | 0 to 5 s | none seen |
| `fg-carwindow_t1` | `bcb14b85` | Kling 2.5 Turbo | The terrier rides in the passenger seat, ears blowing, grinning, the street passing; ends looking at the lens | pass | 0 to 5 s | none seen |
| `fg-leaveit_t1` | `89bcb826` | Kling 2.5 Turbo | The terrier lies down over a treat on the rug, the treat between his paws, squints and stares at the lens; the doodle looms behind | pass | 0 to 5 s | none seen |
| `fg-sleeprun_t1` | `35d0f45e` | Kling 2.5 Turbo | The terrier asleep on his side, paws twitching; the doodle behind him turns and stares at the lens | pass, a strong reaction shot | 0 to 5 s | none seen |
| `fg-furniture_t1` | `a413d11c` | Kling 2.5 Turbo | The doodle rests its chin on the terrier's back as a pillow; the terrier stares at the lens throughout | pass | 0 to 5 s | little motion: a hold shot |
| `fg-sofasprawl_t1` | `3412b458` | Kling 2.5 Turbo | The terrier belly-up against the sofa does a big stretch and goes limp; the doodle in the foreground turns to the lens | pass | 2.0 to 5 s (the stretch 1.2 to 2.2 s blurs) | motion blur on the stretch |
| `fg-kitchen_t1` | `1bd923bd` | Kling 2.5 Turbo | The terrier noses a treat around the kitchen tile, then steps back and stares at the lens | pass with a cut | 0 to 3.4 s; the stare 3.6 to 4.4 s | his collar vanishes 3.6 to 4.4 s |
| `fg-copycat_t1` | `b4e7bf61` | Kling 2.5 Turbo | Both dogs sniff the rug, then lie down side by side in the same pose and look at the lens | pass with a cut | 3.0 to 5 s for the matching pose | the terrier's collar drops out 2 to 4.5 s |
| `fg-onetoe_t1` | `bcdc9e9a` | Kling 2.5 Turbo | The doodle is draped off the sofa, one paw dangling; the terrier on the rug looks from the paw to the lens and back | pass with a cut | 0 to 2.3 s and 3.0 to 5 s | the dangling leg retracts and returns 2.3 to 3.0 s |
| `fg-lump_t1` | `b9d38010` | Kling 2.5 Turbo | The terrier digs at the throw on the sofa and flops into it head-first | pass | 0 to 5 s | a soft frame near 3.0 s; not a full burrow |
| `fg-sleepsit_t1` | `89202f83` | Kling 2.5 Turbo | The terrier sits dozing, head nodding lower, then gives up and slumps down onto the rug | pass | 0 to 5 s | motion blur at 2.5 s |
| `fg-bedroom_t1` | `f060dfd3` | Kling 3.0, 1080p | A tan-faced terrier curled on an unmade bed watches the lens, then lets his eyes close | pass | 0 to 5 s | a different dog from the hero; small in frame |
| `fg-livingroom_t1` | `0535c10e` | Kling 2.5 Turbo | The terrier yawns hugely and settles his chin on his paws; the doodle in the foreground stares into the lens throughout | pass | 0 to 5 s | none seen |

### From 17 to 18 Nov (Kling 3.0, 1080p)

| Clip | Asset | What happens | Verdict | Usable |
|---|---|---|---|---|
| `b2-ch-02` | `9ee3b737` | Wet patio: the terrier eats from the doodle's bowl; the doodle watches, then turns and stares at the lens at about 4.3 s | pass, the best clip made | 0 to 5 s |
| `b2-v2-c07` | `f18c691d` | Patio: the terrier sniffs the doodle's tail while the doodle eats from the bowl, then the doodle stares at the lens ("Customs") | pass | 0 to 5 s |
| `b2-v2-c02` and `b2-v2-c02b` | `16eaabad`, `8e493c2e` | Patio: the terrier belly-creeps until his nose is on the bowl's rim, then looks at the lens ("Adjacent") | pass | 0 to 5 s |
| `b2-ch-01e_t1` | `5735268e` | Patio: the doodle alone by its bowl; the terrier walks in and takes it | pass | 0 to 5 s |
| `b2-gy-03` | `9eceb8cc` | The terrier play-bows on a purple yoga mat; the doodle trots across the back | pass (the mat stages the dog) | 0 to 5 s |
| `b2-gy-05` | `df9c6de0` | The terrier lies down on the mat; the doodle lies down beside him | pass | 0 to 5 s |
| `b2-gy-04` | `aa06e76b` | The doodle trots past the terrier's stretch | the head morphs from 3.4 s | 0 to 3.2 s |

Not banked: `br-01` (the footbridge branch passes through the rails) and the three text-to-video clips with different-looking dogs.


## Suggested captions and music (for the compile session to test)

Captions go over the top, short and deadpan, in the dog's world. Run each through `python factory/jokelab.py check` before it goes on the board. None of these has been judged.

Angles to try, one or two lines each, the dog's world, never the buyer's body or life. The terrier is Gary and the doodle is Doug, as in the earlier films.

| Clip | Caption angles | Music idea |
|---|---|---|
| `fg-parkpath_t1` | "The walk is over when he says it is." / "Day three of negotiations." | slow, mournful strings, or a protest-march drum; stop it dead on the eye roll |
| `fg-carwindow_t1` | "He thinks we bought the car for him." / "Has never once asked where we are going." | a sunny driving song from the app's trending list, entering on the first ear flap |
| `fg-leaveit_t1` | "We said leave it. He left it. Under himself." | a heist theme that drops out when he squints |
| `fg-sleeprun_t1` | "Winning a race he has never won awake." / Doug's stare: "Every night." | a slow-motion victory theme; cut it on Doug's stare |
| `fg-furniture_t1` | "Doug found a pillow. The pillow has notes." | quiet lounge music, a single held note |
| `fg-sofasprawl_t1` | "Sat up once this morning. Still recovering." | a spa track; a record scratch as Doug turns |
| `fg-kitchen_t1` | "Burying it for later. On tile. In front of us." | tense documentary strings |
| `fg-copycat_t1` | "Doug does whatever Gary does. Gary does nothing." | a two-note copycat motif |
| `fg-onetoe_t1` | "Doug is technically still on the floor." | a game-show tick while Gary checks the paw |
| `fg-lump_t1` | "Gary has left the conversation." | a door-close sound, then silence |
| `fg-sleepsit_t1` | "Fought it bravely. For four seconds." | a lullaby that slows as he nods |
| `fg-bedroom_t1` | "He heard the word walk in a sentence that was not about him." | silence, then one low piano note on the stare |
| `fg-livingroom_t1` | "Gary has worked very hard today." (on the yawn) / Doug's stare: "He has not." | office ambience, a keyboard clacking, cut on the yawn |

Ways to combine them (each about 10 to 15 s, the same two dogs in the same room):
- **"A full day's work"**: `fg-sleepsit` → `fg-lump` → `fg-sofasprawl` → `fg-onetoe` → `fg-sleeprun`, a montage of doing nothing, with one deadpan time-stamp caption per beat.
- **"Gary and Doug"**: `fg-copycat` → `fg-furniture` → `fg-leaveit`, Doug imitating, using and hunting Gary.
- **"Outside"**: `fg-parkpath` → `fg-carwindow`, the same dog refusing a walk and loving a drive.
- **The patio pair**: `b2-v2-c07` and `b2-ch-02`, already proven at 8 by the film judge.
- **The product**: end any of these on the painted blanket (`local/footage/st-gy-09-terrier-blanket.png`), the store's own render of this terrier. The film judge marked a cold end card down every time, so give it a reason to be there (Gary asleep on it, or a caption that hands the joke to the gift).


## Credits

The 13 new clips cost nothing: 12 on Kling 2.5 Turbo Unlimited (720p std) and one on Kling 3.0 Unlimited, its last free job. The balance read 859.35 before and after. The 12 anchor stills came earlier through the MCP inside Krish's cap of 150: 82 credits spent in all for the sprint (941.35 to 859.35), 68 left in the cap.

## Rules for the compile session

- Krish adds captions and music; every caption is checked against `docs/HUMOUR.md` and the copy rules (US spelling, no em dashes, no exclamation marks).
- Cut inside the usable range in the table. Each clip's fault is named; never show it.
- The painted end card is the store's own render; never redraw the product.
- Judge the compiled films with the panel (tier 2 with the full live list) before the review board.
