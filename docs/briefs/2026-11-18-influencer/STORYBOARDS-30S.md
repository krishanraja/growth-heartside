# Influencer-parody storyboards at 30 seconds (18 Nov 2026)

Ruling (Krish, 2026-11-18): realistic dogs doing realistic dog things, cut to parody cringey human influencer
stereotypes, is the house series; every shot must look like a dog in its natural habitat doing a regular dog thing.
Each film is about 13 shots at 2 to 2.5 s, as F38 was, one stereotype each, and none reuses a stereotype a live post
owns (`TAKEN_STEREOTYPES` in `factory/jokelab.py`).

**What exists.** Codex's catalogue (`local/inventory/2026-11-18/clips.csv`, 81 rows) finds enough natural-looking
footage only of Gary (grey wire terrier, orange collar) and Doug (chocolate doodle, orange collar). Merging raw and
trimmed copies of the same take, and dropping what Krish rejected (FG01 "that dog wouldn't lay like that"; FG14 and FG17
"the food disappears like AI"), leaves about nine clean, active shots, roughly 22 s in all. So every film below needs
new shots. HAVE = an existing clip (catalogue score in brackets); NEED = a new clip to generate, of Gary or Doug from
the approved anchors, ordinary behaviour, owner's-phone framing.

## 1. A day in my life (Gary; Doug judges)

The influencer whose gruelling day is an iced coffee, one email and pilates, then "so drained".

| # | Label | Shot | |
|---|---|---|---|
| 1 | a day in my life | Gary wakes on an unmade bed, stretches front legs, yawns | NEED |
| 2 | iced coffee run | Gary in the passenger seat, ears blowing, grins at the lens (FG02) | HAVE (4) |
| 3 | grabbing my order | Gary noses into a takeaway paper bag on the kitchen floor | NEED |
| 4 | setting up my workspace | Gary nose-dives into the sofa throw and stays face-down (FG10, 0 to 3.0) | HAVE (4) |
| 5 | answered one email | Gary sitting on the rug nods off and slides flat (FG11) | HAVE (3, motion blur at 2.5 s) |
| 6 | meal prep | Gary buries a treat on bare tile; it stays in plain sight (FG07) | HAVE (4) |
| 7 | hydration | Gary drinks noisily from his water bowl, water slopping onto the floor | NEED |
| 8 | pilates | Gary creeps on his elbows to Doug's bowl (FG16, 1.0 to 3.6) | HAVE (4) |
| 9 | stretching it out | Gary belly-up against the sofa, one huge stretch, goes limp (FG06) | HAVE (4) |
| 10 | getting my steps in | Gary trots three laps of the rug chasing nothing, then flops | NEED |
| 11 | honestly so drained | Gary yawns hugely while Doug stares into the lens (FG13) | HAVE (4) |
| 12 | need a reset tbh | Gary paddles in his sleep while Doug stares (FG04) | HAVE (4) |

Caption: "Some days you just have to protect your energy." HAVE 8, NEED 4.

## 2. I am obsessed (Gary; ends on the real blanket; gift-led)

The sponsored product rave: months of use of a brand-new product, "literally life-changing", "run, don't walk".

| # | Label | Shot | |
|---|---|---|---|
| 1 | ok I am obsessed | Gary nose-dives into the throw (FG10) | HAVE (4) |
| 2 | unboxing | Gary tears at a delivery box on the hallway floor, cardboard flying | NEED |
| 3 | the texture | Gary circles three times and kneads a blanket before lying down | NEED |
| 4 | been using it for months | Gary belly-up, one huge stretch, limp (FG06) | HAVE (4) |
| 5 | obsessed with the fit | Gary rolls on his back on the blanket, legs wiggling | NEED |
| 6 | literally life-changing | Gary nods off sitting and slides flat (FG11) | HAVE (3) |
| 7 | my partner wants one | Doug tries to step onto the blanket; Gary lifts his lip without moving | NEED |
| 8 | not sharing | Gary lies over his treat, squinting at the lens (FG03) | HAVE (4) |
| 9 | run, don't walk | Gary yawns; Doug stares (FG13) | HAVE (4) |
| 10 | it is me | the store's own painted blanket of Gary, held 3 s | HAVE (product) |

Caption: "Not sponsored. He is the product." HAVE 6, NEED 4.

## 3. Yes, we're that couple (Gary and Doug)

The over-performed couple account: date nights, "communication is key", then the joint podcast.

| # | Label | Shot | |
|---|---|---|---|
| 1 | yes, we're that couple | Gary lies down; Doug copies a beat later (FG08) | HAVE (3, collar faint) |
| 2 | he's my safe space | Doug's chin on Gary's back; Gary stares flatly (FG05) | HAVE (3, static) |
| 3 | date night | Gary sniffs Doug's rear while he eats; Doug stares (FG15) | HAVE (4) |
| 4 | we share everything | Gary creeps on his elbows to Doug's bowl (FG16) | HAVE (4) |
| 5 | our first fight | Gary and Doug tug-of-war over a rope toy, growling | NEED |
| 6 | communication is key | Gary yawns in Doug's face; Doug stares (FG13) | HAVE (4) |
| 7 | space is healthy | both lie back to back on the rug, ignoring each other | NEED |
| 8 | he still surprises me | Doug sneaks Gary's chew while Gary sleeps | NEED |
| 9 | couples yoga | Gary lies on the mat; Doug lies half on him (FG19, 1.6 to 5.0) | HAVE (3) |
| 10 | our podcast drops Friday | both sit side by side on the sofa staring into the lens | NEED |

Caption: "Link to our couples merch is not in bio." HAVE 6, NEED 4.

## 4. Please respect the set (Gary; Doug walks into the shot)

The creator filming a wellness flow in public, annoyed by everyone in the background.

| # | Label | Shot | |
|---|---|---|---|
| 1 | filming my morning flow | Gary play-bows on the mat; Doug stands behind, looking at the lens (FG20, 0 to 3.1) | HAVE (3) |
| 2 | this is a closed set | Doug sniffs a hole behind the mat and trots off (FG18) | HAVE (3) |
| 3 | please respect the craft | Doug digs right behind the mat, dirt flying | NEED |
| 4 | back in flow | Gary alone on the mat again (FG19, 0 to 1.6) | HAVE (3) |
| 5 | take two | Doug shakes off water right beside the mat | NEED |
| 6 | take five | Doug zooms through the back of the shot | NEED |
| 7 | he is now in the content | Doug lies down half on Gary (FG19, 1.6 to 5.0) | HAVE (3) |
| 8 | collab I did not approve | Doug's chin on Gary's back; Gary stares (FG05) | HAVE (3) |

Caption: "Some people have no respect for the craft." HAVE 5, NEED 3. Weakest footage: the catalogue scores every yoga
shot 3 ("the mat reads staged"). Lowest priority.

## What it takes

16 new shots of Gary and Doug in total (4 + 4 + 4 + 3, one shared). Each would be image-to-video from their approved
anchor stills (`local/footage/anchors/`), on an Unlimited model in the Higgsfield website through Codex (no credits), and
each must pass the dog-realism checks and Krish's eye before it is cut. This lifts the generation freeze for these
16 shots only, so it waits on Krish's yes. The words of all four go through the humour engine before any shot is made.
