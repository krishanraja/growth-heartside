"""Write docs/briefs/2026-11-18-footage/INVENTORY.md from manifest.json (run from the repository root)."""
import json

M = 'docs/briefs/2026-11-18-footage/manifest.json'
OUT = 'docs/briefs/2026-11-18-footage/INVENTORY.md'
m = json.load(open(M, encoding='utf-8'))

CAPS = {
    'FG01': ('"The walk is over when he says it is." / "Day three of negotiations."', 'slow, mournful strings or a protest-march drum; stop dead at 3.0 s'),
    'FG02': ('"He thinks we bought the car for him." / "Has never once asked where we are going."', "a sunny driving song from the app's trending list"),
    'FG03': ('"We said leave it. He left it. Under himself."', 'a heist theme that drops out at 3.0 s'),
    'FG04': ('"Winning a race he has never won awake." / on Doug: "Every night."', 'a slow-motion victory theme'),
    'FG05': ('"Doug found a pillow. The pillow has notes."', 'quiet lounge music, one held note'),
    'FG06': ('"Sat up once this morning. Still recovering."', 'a spa track; a record scratch at 2.5 s as Doug turns'),
    'FG07': ('"Burying it for later. On tile. In front of us."', 'tense documentary strings'),
    'FG08': ('"Doug does whatever Gary does. Gary does nothing."', 'a two-note copycat motif'),
    'FG09a': ('"Doug is technically still on the floor."', 'a game-show tick while Gary checks the paw'),
    'FG09b': ('(the end beat of FG09a)', 'as FG09a'),
    'FG10': ('"Gary has left the conversation."', 'a door-close sound at 3.0 s, then silence'),
    'FG11': ('"Fought it bravely. For four seconds."', 'a lullaby that slows as he nods'),
    'FG12': ('"He heard the word walk in a sentence that was not about him."', 'silence, then one low piano note'),
    'FG13': ('"Gary has worked very hard today." (on the yawn) / on Doug: "He has not."', 'office ambience, cut on the yawn at 1.0 s'),
    'FG14': ('Proven at 8 as "Best-trained dog" (`st-bowl-c18`); never reuse the judged caption "We are very proud of one of them."', 'a pompous brass march cut dead at 4.3 s'),
    'FG15': ('Proven at 8 as "Customs." (`st-v2-c07`)', 'customs-hall ambience, or silence on the stare'),
    'FG16': ('Judged 7 as "He is not near the bowl." / "He is adjacent." (`st-v2-c02`)', 'a creeping pizzicato'),
    'FG17': ('"Doug was saving that."', 'a lazy whistle'),
    'FG18': ('the yoga set: the film judge reads the mat as staged; use only if the caption owns that', 'a meditation bell'),
    'FG19': ('"Private class. Fully booked." then Doug joins', 'a meditation bell, then a thud'),
    'FG20': ('an opener for the yoga set', 'as FG18'),
}

rows = []
for c in m['clips']:
    beats = '<br>'.join(f"{t:.1f}s {b}" for t, b in c['beats'])
    dur = round(c['out'] - c['in'], 1)
    rows.append(f"| **{c['id']}** | `ready/{c['id']}_{c['slug']}.mp4` | {dur} s | {' + '.join(c['dogs'])} | {beats} | "
                f"{c['payoff']:.1f} s | {c['fault']} | {c['model']} |")
missing = [c['id'] for c in m['clips'] if c['id'] not in CAPS]
assert not missing, missing
captab = '\n'.join(f"| {k} | {v[0]} | {v[1]} |" for k, v in CAPS.items())
NL = '\n'

doc = f"""# Footage inventory, 18 Nov 2026: locked for compilation

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
{NL.join(rows)}

Kling 2.5 Turbo clips were 716x1284 and are upscaled to 1080x1920; Kling 3.0 clips were made at 1080p. Shots that match (same room and light): living room FG03 to FG06, FG08, FG09, FG11, FG13; sofa and throw FG10; patio FG14 to FG17; yard FG18 to FG20; on their own FG01, FG02, FG07, FG12.

Not used: `clips/b2-v2-c02.mp4` (Gary's eyes turn blue from 3.5 s; FG16 is the retake), the kitchen stare after 3.6 s (Gary's collar vanishes), `br-01` (the footbridge branch passes through the rails), and three early text-to-video clips with different-looking dogs.

## Caption angles and music (for the compile session to test)

Short, deadpan, in the dog's world, never the buyer's body or life. Run each line through `python factory/jokelab.py check` before it goes on the board. Only FG14 to FG16 have been judged, as the films named.

| ID | Caption angles | Music idea |
|---|---|---|
{captab}

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
"""
assert '—' not in doc and '!' not in doc
open(OUT, 'w', encoding='utf-8', newline='\n').write(doc)
print('wrote', OUT, len(doc))
