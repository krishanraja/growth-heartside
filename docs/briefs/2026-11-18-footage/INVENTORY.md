# Footage inventory, 18 Nov 2026: locked for compilation

Locked on 18 Nov. Every usable clip from the 16 to 22 Nov sprint is here, cut, normalized and described. You can pick shots and time captions without watching anything: each clip has a beat timeline, a payoff second and a poster frame. None of it is approved for publishing.

Krish, 18 Nov: "I am pretty confident that if your videos are already innate and they are realistic dogs doing real dog things ... then I'll be able to get them up to higher than that, with captions over the top and good music treatment". Footage is not gated on the model judge's 9 (floor `footage-not-gated-on-judge`).

## Where it is

On Krish's PC, in `local/footage/` under the repository (`local/` is never committed). Start with `START-HERE.md` and `INDEX.jpg` there.

| Path | Holds |
|---|---|
| `INDEX.jpg` | one page: every ready clip's poster frame with its id and name |
| `ready/FGxx_<setting>_<action>.mp4` | **use these**: 21 clips trimmed to their usable range, 1080x1920, 30 fps, silent |
| `ready/posters/` | one still per clip at its payoff moment (a thumbnail or cover candidate) |
| `ready/sheets/` | a frame every 0.5 s of each ready clip, timestamped, for timing captions |
| `ready/endcard/END_painted-blanket_gary.png` | the store's own painted blanket of Gary (never redraw the product) |
| `manifest.csv` | the table below as a spreadsheet: id, file, seconds, dogs, setting, beats, payoff, fault, model, source, Higgsfield asset |
| `clips/` and `clips-sheets/` | the raw 5 s generations and their sheets (sources only) |
| `anchors/` | the approved first frame of each new clip |
| `prompts.tsv` | the exact motion prompt of each new clip |
| `tools/` (committed, next to this file) | `sheet.py` (timestamped sheets), `build_ready.py` (rebuilds `ready/`, `INDEX.jpg` and `manifest.csv`), `write_inventory.py` (rewrites this file), `dl.sh` (downloads a take and sheets it) |

The source of truth is [`manifest.json`](manifest.json) in this folder. Change it, then from the repository root run `python -I docs/briefs/2026-11-18-footage/tools/build_ready.py` and `python -I docs/briefs/2026-11-18-footage/tools/write_inventory.py`. Every clip can be fetched again from Higgsfield by its asset id: MCP `show_generation_by_ids` (a credit-free read), then curl its `rawUrl`.

## The cast

- **Gary**: the hero. A gray and white scruffy terrier mix with an orange collar.
- **Doug**: the sidekick. A chocolate shaggy poodle and spaniel mix with an orange collar.
- FG12's dog is a lighter, tan-faced terrier. Use it alone, never next to Gary as the same dog.

## The clips

Times in "What happens" and "Payoff" are seconds in the ready file. The payoff is the moment a caption should land on.

| ID | Ready file | Length | Dogs | What happens | Payoff | Known fault | Model |
|---|---|---|---|---|---|---|---|
| **FG01** | `ready/FG01_park_refuses-walk.mp4` | 5.0 s | Gary | 0.0s Gary lies flat on the asphalt path, chin down, leash taut up out of frame<br>1.0s the leash pulls; he does not move<br>3.0s eyes on the lens, completely unmoved, to the end | 3.0 s | none seen | Kling 2.5 Turbo 720p |
| **FG02** | `ready/FG02_car_window-joyride.mp4` | 5.0 s | Gary | 0.0s Gary sits in the passenger seat looking out, ears blowing back, grinning<br>2.5s the street and houses slide past, ears up<br>4.0s he turns his grin to the lens | 4.0 s | none seen | Kling 2.5 Turbo 720p |
| **FG03** | `ready/FG03_rug_lies-on-treat.mp4` | 5.0 s | Gary + Doug | 0.0s Gary sniffs a bone treat on the rug, Doug standing beside him<br>1.0s Gary lowers himself down over the treat<br>2.0s lying with the treat between his front paws, looking up<br>3.0s squints at the lens, guarding it; Doug looms behind looking down | 3.0 s | none seen | Kling 2.5 Turbo 720p |
| **FG04** | `ready/FG04_floor_sleep-running_doug-stares.mp4` | 5.0 s | Gary + Doug | 0.0s Gary asleep on his side, tongue out; Doug lying behind him<br>1.0s Gary's paws twitch and paddle in a dream<br>1.0s Doug stares straight into the lens, to the end | 1.0 s | none seen | Kling 2.5 Turbo 720p |
| **FG05** | `ready/FG05_rug_doug-uses-gary-as-pillow.mp4` | 5.0 s | Gary + Doug | 0.0s Doug rests his chin on Gary's back; Gary stares at the lens<br>2.5s Doug settles heavier; Gary does not react<br>4.0s the same deadpan stare from Gary to the end | 0.0 s | little motion: a hold shot | Kling 2.5 Turbo 720p |
| **FG06** | `ready/FG06_sofa_belly-up-stretch_doug-turns.mp4` | 5.0 s | Gary + Doug | 0.0s Gary belly-up against the sofa, legs splayed; Doug in the foreground watching him<br>1.2s a huge stretch, front legs straight up<br>2.2s he goes limp again<br>2.5s Doug turns and looks into the lens, to the end | 2.5 s | motion blur on the stretch 1.2 to 2.2 s (reads as speed) | Kling 2.5 Turbo 720p |
| **FG07** | `ready/FG07_kitchen_buries-treat-on-tile.mp4` | 3.4 s | Gary | 0.0s Gary noses a bone treat on the kitchen tile<br>1.0s he nudges the bare tile around it, burying it in nothing<br>2.5s the treat still in plain sight; he lifts his head | 2.5 s | the raw clip's stare at 3.6 to 4.4 s loses the collar, so it is cut | Kling 2.5 Turbo 720p |
| **FG08** | `ready/FG08_rug_doug-copies-gary.mp4` | 5.0 s | Gary + Doug | 0.0s Gary and Doug sniff the rug side by side<br>2.0s Gary lies down; Doug lies down next to him a beat later<br>3.0s both lying in the same pose, looking at the lens | 3.0 s | Gary's collar is faint 2 to 4.5 s | Kling 2.5 Turbo 720p |
| **FG09a** | `ready/FG09a_sofa_doug-one-paw-on-floor.mp4` | 2.3 s | Gary + Doug | 0.0s Doug sprawled over the sofa, one front paw dangling to the floor; Gary on the rug looks up at him<br>1.0s Gary looks from Doug to the lens | 1.0 s | cut at 2.3 s, where Doug's leg retracts | Kling 2.5 Turbo 720p |
| **FG09b** | `ready/FG09b_sofa_doug-one-paw-on-floor_end.mp4` | 2.0 s | Gary + Doug | 0.0s Doug's paw back on the floor; Gary looks at the lens, then away | 0.0 s | starts after the leg glitch | Kling 2.5 Turbo 720p |
| **FG10** | `ready/FG10_sofa_digs-into-throw.mp4` | 5.0 s | Gary | 0.0s Gary stands on the sofa nosing the throw<br>1.5s digs at it, head going under<br>3.0s flops into the throw head-first and stays there | 3.0 s | a soft frame near 3.0 s; not a full burrow | Kling 2.5 Turbo 720p |
| **FG11** | `ready/FG11_rug_dozes-off-sitting.mp4` | 5.0 s | Gary | 0.0s Gary sits on the rug, head drooping<br>1.5s nods lower and lower, then slides down<br>3.0s lying flat, chin on the rug, eyes heavy | 3.0 s | motion blur at 2.5 s as he slides down | Kling 2.5 Turbo 720p |
| **FG12** | `ready/FG12_bed_watches-then-sleeps_tan-dog.mp4` | 5.0 s | tan terrier (not Gary) | 0.0s a tan-faced terrier curled on an unmade bed, eyes on the lens<br>3.5s his eyes slowly close | 3.5 s | a different dog from Gary; small in frame | Kling 3.0 1080p |
| **FG13** | `ready/FG13_rug_gary-yawns_doug-stares.mp4` | 5.0 s | Gary + Doug | 0.0s Doug in the foreground stares into the lens; Gary on the rug behind<br>1.0s Gary yawns hugely<br>2.5s Gary settles his chin on his paws; Doug never stops staring | 1.0 s | none seen | Kling 2.5 Turbo 720p |
| **FG14** | `ready/FG14_patio_gary-eats-dougs-dinner_doug-stares.mp4` | 5.0 s | Gary + Doug | 0.0s Gary lies eating from a steel bowl; Doug lies beside him, watching<br>3.5s Doug turns his head<br>4.3s Doug stares straight into the lens | 4.3 s | none seen | Kling 3.0 1080p |
| **FG15** | `ready/FG15_patio_customs-sniff_doug-stares.mp4` | 5.0 s | Gary + Doug | 0.0s Doug eats from the bowl; Gary sniffs Doug's rear, absorbed<br>2.5s Doug lifts his head from the bowl<br>3.5s Doug stares into the lens while Gary keeps sniffing | 3.5 s | none seen | Kling 3.0 1080p |
| **FG16** | `ready/FG16_patio_belly-creeps-to-bowl.mp4` | 5.0 s | Gary + Doug | 0.0s Doug eats from the bowl; Gary flat on his belly beside it<br>1.5s Gary creeps forward on his elbows until his nose is at the rim<br>3.5s Gary looks into the lens; Doug pulls back out of frame | 3.5 s | none seen | Kling 3.0 1080p |
| **FG17** | `ready/FG17_patio_gary-takes-the-bowl.mp4` | 5.0 s | Gary + Doug | 0.0s Doug lies beside a full bowl<br>1.0s Gary walks in from the left<br>2.0s Gary eats from it standing<br>3.0s Gary lies down and keeps eating; Doug watches | 2.0 s | none seen | Kling 3.0 1080p |
| **FG18** | `ready/FG18_yard_yoga-mat_play-bow.mp4` | 5.0 s | Gary + Doug | 0.0s Gary holds a play-bow on the purple mat; Doug sniffs a hole behind<br>2.5s Doug trots off behind him | 0.0 s | the mat reads as a staged pose (film judge) | Kling 3.0 1080p |
| **FG19** | `ready/FG19_yard_yoga-mat_both-lie-down.mp4` | 5.0 s | Gary + Doug | 0.0s Gary in a play-bow on the mat<br>1.0s Gary lies down on the mat, panting<br>2.5s Doug walks over onto the mat<br>4.0s Doug lies down beside Gary, half on him | 4.0 s | none seen | Kling 3.0 1080p |
| **FG20** | `ready/FG20_yard_yoga-mat_doug-walks-past.mp4` | 3.2 s | Gary + Doug | 0.0s Gary holds a play-bow on the mat; Doug stands behind, looking at the lens<br>2.5s Doug starts walking behind Gary | 0.0 s | cut at 3.2 s; Doug's head morphs after 3.4 s | Kling 3.0 1080p |

Kling 2.5 Turbo clips were 716x1284 and are upscaled to 1080x1920; Kling 3.0 clips were made at 1080p. Shots that match (same room and light): living room FG03 to FG06, FG08, FG09, FG11, FG13; sofa and throw FG10; patio FG14 to FG17; yard FG18 to FG20; on their own FG01, FG02, FG07, FG12.

Not used: `clips/b2-v2-c02.mp4` (Gary's eyes turn blue from 3.5 s; FG16 is the retake), the kitchen stare after 3.6 s (Gary's collar vanishes), `br-01` (the footbridge branch passes through the rails), and three early text-to-video clips with different-looking dogs.

## Caption angles and music (for the compile session to test)

Short, deadpan, in the dog's world, never the buyer's body or life. Run each line through `python factory/jokelab.py check` before it goes on the board. Only FG14 to FG16 have been judged, as the films named.

| ID | Caption angles | Music idea |
|---|---|---|
| FG01 | "The walk is over when he says it is." / "Day three of negotiations." | slow, mournful strings or a protest-march drum; stop dead at 3.0 s |
| FG02 | "He thinks we bought the car for him." / "Has never once asked where we are going." | a sunny driving song from the app's trending list |
| FG03 | "We said leave it. He left it. Under himself." | a heist theme that drops out at 3.0 s |
| FG04 | "Winning a race he has never won awake." / on Doug: "Every night." | a slow-motion victory theme |
| FG05 | "Doug found a pillow. The pillow has notes." | quiet lounge music, one held note |
| FG06 | "Sat up once this morning. Still recovering." | a spa track; a record scratch at 2.5 s as Doug turns |
| FG07 | "Burying it for later. On tile. In front of us." | tense documentary strings |
| FG08 | "Doug does whatever Gary does. Gary does nothing." | a two-note copycat motif |
| FG09a | "Doug is technically still on the floor." | a game-show tick while Gary checks the paw |
| FG09b | (the end beat of FG09a) | as FG09a |
| FG10 | "Gary has left the conversation." | a door-close sound at 3.0 s, then silence |
| FG11 | "Fought it bravely. For four seconds." | a lullaby that slows as he nods |
| FG12 | "He heard the word walk in a sentence that was not about him." | silence, then one low piano note |
| FG13 | "Gary has worked very hard today." (on the yawn) / on Doug: "He has not." | office ambience, cut on the yawn at 1.0 s |
| FG14 | Proven at 8 as "Best-trained dog" (`st-bowl-c18`); never reuse the judged caption "We are very proud of one of them." | a pompous brass march cut dead at 4.3 s |
| FG15 | Proven at 8 as "Customs." (`st-v2-c07`) | customs-hall ambience, or silence on the stare |
| FG16 | Judged 7 as "He is not near the bowl." / "He is adjacent." (`st-v2-c02`) | a creeping pizzicato |
| FG17 | "Doug was saving that." | a lazy whistle |
| FG18 | the yoga set: the film judge reads the mat as staged; use only if the caption owns that | a meditation bell |
| FG19 | "Private class. Fully booked." then Doug joins | a meditation bell, then a thud |
| FG20 | an opener for the yoga set | as FG18 |

Ways to combine them (each about 10 to 15 s, the same two dogs in the same room):
- **"A full day's work"**: FG11, FG10, FG06, FG09a, FG04. A montage of doing nothing, with one deadpan time-stamp caption per beat.
- **"Gary and Doug"**: FG08, FG05, FG03, FG13. Doug imitates Gary, uses him as a pillow and hunts his treat.
- **"Outside"**: FG01 then FG02. The same dog refusing a walk and loving a drive.
- **The patio pair**: FG15 and FG14, each already 8 with the film judge.
- **The product**: end any of these on `ready/endcard/END_painted-blanket_gary.png`. The film judge marked a cold end card down every time, so give it a reason to be there: a caption that hands the joke to the gift.

## Credits

The 13 new clips cost nothing: 12 on Kling 2.5 Turbo Unlimited (720p std) and one on Kling 3.0 Unlimited, its last free job. The balance read 859.35 before and after. The anchor stills came earlier through the MCP inside Krish's cap of 150: 82 credits spent in all for the sprint (941.35 to 859.35), 68 left in the cap.

## Rules for the compile session

- Captions and music are added at compile. Every caption is checked against `docs/HUMOUR.md` and the copy rules: US spelling, no em dashes, no exclamation marks.
- Use `ready/` files only; their faults are already cut out.
- The painted end card is the store's own render; never redraw the product.
- Judge the compiled films with the panel (tier 2, with the full live list) before the review board.
