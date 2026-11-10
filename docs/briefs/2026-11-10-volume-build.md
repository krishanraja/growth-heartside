# Volume build: bulletproof image and video posts (Sprint 120)

Krish, 10 Nov: "we need a huge array of bulletproof posts here, image and video", then "file it as F29 and start
the volume build". The Heartside product posts in the style of the dog group chat (F10) come after this, as their own
build (Krish: "we will do that after").

## What 10 Nov proved

| Attempt | Score | Lesson |
|---|---|---|
| F28, dog 80s dance (Smalltown Boy) | passed, filed | Trend dances reskin well |
| Batch 1 lip-syncs (7 films) | 6 to 8, all held | Hands meeting objects and small facial reactions fail in generated video; lyric captions banned |
| HAL-02 remake | 6, held | Same failure: the coffee refusal never read |
| F29, Dame Hombro shoulder bounce | 7, then 8, then 9, filed | One simple movement per shot; cut on peaks; hard-cut over transitions; end on a sharp held frame |
| Corgi laundry inspector, backwards pug lineup (stills) | passed first time | Single-moment gags and group poses generate cleanly |

**Humour anchor** (Krish, 10 Nov): every build is written toward `docs/HUMOUR.md`: an intelligent observation, an utterly stupid premise and a slightly cruel payoff. A piece missing one of the three is not done.

## Build only these formats

1. **Trend dances.** A current trend sound read from dated sources this week, reskinned with dogs. Close-ups, a group
   shot, one rebel, a payoff peak and a held ending. The sound is added in the platform.
2. **Lineup gags with one rebel** (playbook "Perfect lineup, one rebel"), as stills or short motion.
3. **Single-image memes** in `factory/still.py`'s band layout: the line above the photo, never on it. Playbook grade A
   franchises: Tiny Employee, Side-Eye Tribunal, Bed-Space Economics, Crime Scene, Costume Reveal, Proud of the
   Underdog, Life in Five Clips.
4. **Carousels** of 3 to 5 stills telling one escalating joke.
5. **Short motion gags** with one physical payoff, one movement per shot and a locked camera.

Do not build lip-syncs, anything where hands handle objects, or story films longer than about 15 s.

## Rules (each is on the floor or a 10 Nov ruling)

- No lyric captions. No on-screen text in videos unless the proven original earned it. Memes carry their one line in
  the band. Every element must earn its place (the subtraction check).
- Real dogs: correct anatomy at full size on every still and on the final crop. The same dog stays the same across
  shots. Cut every clip on peaks and held frames, never on a blurred transition.
- No generated product, no mugs that could pass for ours, no chestnut or red dachshund.
- Proven posts may be reskinned and reused directly.
- A judged 9 or above at tier 2, on a 16-frame sheet for video, before anything is filed. Below 9: fix it or retire it.

## Batches

- **Size and mix:** about 12 posts a batch, roughly 8 image posts and 4 videos, best first.
- **Each passing post:**
  - filed through `factory/send_library.py` from F30 upward;
  - one new `02<letter> Schedule and captions (<ids>)` Sheet per batch, starting at `02g`, with the 16 columns as in `02f`;
  - `approved` left blank, and notes starting `SONG` for any in-platform sound.
- **After each batch:**
  - one review page for Krish: covers, scores, songs, held items;
  - the Drive audit and a `codex/INDEX.md` or `CHANGES.md` record;
  - commit and push.
- **Budget:**
  - Higgsfield: about 1,330 credits left. Stills cost about 0.25 credits each; a video post cost about 45 (5 Kling 3.0 pro clips).
  - Book every batch with `reserve_credit_spend` and settle it.
  - Stop when 1,100 credits are spent, keeping about 230 in reserve. Runway only after checking its per-clip cost.
- **Never:** post, schedule, queue, mark approved, message the publishing desk, or boost. Krish's hold stands: "Make
  Sure nothing actually gets published yet."
