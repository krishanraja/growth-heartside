# Dog does dog things, wave 3 (F46 onward): scripts

Krish, 10 Nov, on his review board: Yes to "Next dog-does-dog-things wave on Runway (F46 onward)", with "added
higgsfield credits, use them wisely"; No to keeping production outside the Codex lane, so this wave goes through
Codex as one card. The schedule needs about 20 more posts before the 4 Dec Christmas order-by.

Written to `docs/HUMOUR.md` (an intelligent observation, an utterly stupid premise, a slightly cruel payoff) and the
format's formula (`docs/briefs/2026-11-10-dog-does-dog-things-scripts.md`): a human video format played completely
straight, every beat a real dog behavior, labelled on every shot like F38 and F40, judged against F38 to F40.

**Budget, read from Control Center 10 Nov:**
- Higgsfield: 37.1 credits left in Heartside's share; stills at 0.25.
- Runway: 540 credits left; Gen-4 Turbo about 25 a clip.

So: stills for every beat (about 50, about 12.5 credits), and motion only where the motion is the joke, 3 clips a
reel at most (15 clips, about 375 credits). Every other beat is a still with a push-in, as in F38 to F40.

**Rules carried:**
- No human arms; people appear only as feet, an off-screen hand or a blurred figure.
- One dog per reel, the same dog in every shot.
- No chestnut or red dachshund.
- The product only as the store's own render.
- No lyric text; the song is added in the app.
- Labels sit in the safe band (y 220 to 1450) and never cover a face.

## 1. What I eat in a day · beagle · about 17 s · audience

The wellness creator's food diary, sincerely labelled; the dog eats exactly what dogs eat.

| Beat | Label | Picture |
|---|---|---|
| 1 | 7:00 AM · Breakfast | Nose deep in its own full bowl, then walks away from it (still, push-in) |
| 2 | 7:02 AM · Second breakfast | Face in the cat's bowl, eye contact with camera (clip) |
| 3 | 10:00 AM · Fiber | A sock hanging out of its mouth, dead serious (still) |
| 4 | 1:00 PM · Greens | Chewing grass in the garden (still, push-in) |
| 5 | 3:30 PM · Supplements | Carrying one entire tree branch through a doorway sideways, stuck (clip) |
| 6 | 6:00 PM · Dinner | Under the dinner table, chin on someone's knee, eyes up (still) |
| 7 | Button | Flat on its back, belly up, asleep; label "Calories: confidential" (clip, slow breathing) |

Song: "Ooh La La", Goldfrapp, from 0:00 (the stomp).

## 2. Get ready with me: Christmas photo day · goldendoodle · about 20 s · signature, ends on the real portrait

GRWM, played straight. Everything goes wrong, and then the portrait shows how good it looks anyway.

| Beat | Label | Picture |
|---|---|---|
| 1 | GRWM · Christmas photo day | Freshly groomed doodle, fluffy, posing (still) |
| 2 | Step 1 · Skincare | Rolling in a pile of wet leaves (clip) |
| 3 | Step 2 · Hydration | Standing in a puddle, drinking from it (still) |
| 4 | Step 3 · Setting spray | The full-body shake, water flying (clip) |
| 5 | Step 4 · Hair | Ears inside out, leaf on head, flat stare (still, push-in) |
| 6 | The final look | Hard cut to the real doodle portrait render, held 3.5 s |

Song: "Vogue", Madonna, from the chorus (platform default). The portrait is shown only as the store's own render.

## 3. Day in the life of a CEO · French bulldog in a tiny knitted jumper · about 18 s · audience

Corporate self-importance, punctured by every beat (the profile's "puncturing pretension").

| Beat | Label | Picture |
|---|---|---|
| 1 | 6:00 AM · Up before the market | Asleep, tongue out, on a pillow (still) |
| 2 | 9:00 AM · Board meeting | Lying on the actual bed, eyes half open (still, push-in) |
| 3 | 11:00 AM · Delegating | Drops a ball at off-screen feet, stares (clip) |
| 4 | 1:00 PM · Due diligence | Head inside the kitchen bin (still) |
| 5 | 3:00 PM · Networking | Nose to nose with another dog through a fence (clip) |
| 6 | 5:00 PM · Golden parachute | Upside down on the sofa, legs in the air (clip) |

Song: "Money", Pink Floyd, from 0:00 (the till).

## 4. What's in my carry-on · golden retriever · about 15 s · audience

The travel vlogger's packing video. The dog packs only itself.

| Beat | Label | Picture |
|---|---|---|
| 1 | Packing for a trip | Open suitcase on a bed, folded clothes (still) |
| 2 | Essentials | The golden is lying in the suitcase on the clothes (still, push-in) |
| 3 | Snacks | A tennis ball placed in the suitcase pocket by the dog's mouth (clip) |
| 4 | Comfort item | A stuffed toy dropped onto the clothes (still) |
| 5 | Button | Lying across the closed case in the doorway, flat stare: "Nobody's going" (clip) |

Song: "Leaving on a Jet Plane", John Denver, from 0:00.

## 5. Christmas card, take 47 · corgi · about 16 s · signature, ends on the real Christmas card

Behind the scenes of the family Christmas card, in numbered takes.

| Beat | Label | Picture |
|---|---|---|
| 1 | Take 1 | Corgi in front of a tree, antlers on, mid-blink (still) |
| 2 | Take 9 | Chewing one antler off (clip) |
| 3 | Take 22 | Walking out of frame, butt to camera (still) |
| 4 | Take 38 | Asleep under the tree (still, push-in) |
| 5 | Take 47 | A perfect pose, then a sneeze (clip) |
| 6 | The card | Hard cut to the real Heartside Christmas card render, held 3.5 s |

Song: "It's the Most Wonderful Time of the Year", Andy Williams, from 0:00.

## Production through the Codex lane

1. **Claude makes the inputs.** Stills on Higgsfield, booked in Control Center and checked on a contact sheet for
   anatomy and identity before any motion. Then Runway clips for the clip beats only.
2. **Codex assembles each reel** from one card, `codex/queue/dog-things-wave-3.md`. Its inputs are the stills, the
   clips, the label text and timings, and the store renders. It returns silent 1080x1920 reels and covers.
3. **Claude checks the result.** At full size, frame by frame, against every floor line; then the tier 2 judges.
   Only 9s go on the review board.
