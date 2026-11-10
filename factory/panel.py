"""The judging panel: code first, a cheap model for yes or no, a stronger model for taste, Krish last.

Krish, 2026-11-10: "what kind of straightforward simple judging panel can you implement that is going to
guarantee 10/10 outputs without destroying all of my Claude tokens or taking 20 hours to run?"

    python3 factory/panel.py sheet  MEDIA [--out PNG]         a contact sheet: an image as is, a video as 8 timed frames
    python3 factory/panel.py batch  SHEET... --out PNG          up to 4 sheets tiled into one image: a judge reads once per call
    python3 factory/panel.py tier0  MANIFEST SLOT [MEDIA]     code checks: the sprint slot, its spec, its media
    python3 factory/panel.py brief  tier1|tier2 SHEET...      the exact prompt for a judge sub-agent (Haiku for tier1, Sonnet for tier2)
    python3 factory/panel.py record SLOT TIER VERDICT [--score N] [--note ...]   tier1-pass|tier1-fail|tier2-N|krish-yes|krish-no
    python3 factory/panel.py agreement                        how often the panel's 9+ matched Krish's yes

Tier 0 is free and runs in seconds. Tier 1 asks six yes-or-no questions from Krish's floor of one contact sheet
per asset, four assets per call; any no sends the asset back with the failing frame. Tier 2 scores only Tier 1's
survivors against anchors (factory/bank/anchors.json plus the floor's own quotes); only 9 and above reach Krish's
one review page. No model watches a video: content-watcher or ffmpeg reads it locally into frames first.
Verdicts go to local/factory/panel.jsonl (rule 9: no tracked file changes in a scheduled run).
"""
import argparse, datetime as dt, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOG = os.environ.get('HEARTSIDE_PANEL_LOG', f'{ROOT}/local/factory/panel.jsonl')
ANCHORS = f'{HERE}/bank/anchors.json'
VIDEO = ('.mp4', '.mov', '.webm', '.m4v')


def sheet(media, out, frames=8, width=1024):
    """One image a judge can read cheaply: the picture itself, or a video's frames in time order with timestamps."""
    from PIL import Image, ImageDraw
    if not media.lower().endswith(VIDEO):
        im = Image.open(media).convert('RGB'); im.thumbnail((width, width)); im.save(out); return out
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', media],
                               capture_output=True, text=True).stdout or 0)
    if dur <= 0:
        raise SystemExit(f'{media}: no duration; not a readable video')
    shots = []
    for i in range(frames):
        t = dur * (i + 0.5) / frames
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', media, '-frames:v', '1', '-f', 'image2pipe',
                              '-vcodec', 'png', '-'], capture_output=True).stdout
        if raw:
            import io
            shots.append((t, Image.open(io.BytesIO(raw)).convert('RGB')))
    cols = 4; rows = (len(shots) + cols - 1) // cols
    tw = width // cols; th = round(tw * shots[0][1].height / shots[0][1].width)
    canvas = Image.new('RGB', (tw * cols, th * rows), (0, 0, 0)); d = ImageDraw.Draw(canvas)
    for n, (t, im) in enumerate(shots):
        x, y = (n % cols) * tw, (n // cols) * th
        canvas.paste(im.resize((tw, th)), (x, y)); d.rectangle((x, y, x + 64, y + 22), fill=(0, 0, 0))
        d.text((x + 4, y + 4), f'{t:4.1f}s', fill=(255, 220, 0))
    canvas.save(out); return out


def batch(sheets, out, width=1536):
    """Tile up to four contact sheets, labelled A to D, into one image. Each image a judge opens re-sends the whole
    context, so one read per call is what keeps a batch cheap (10 Nov test: three separate reads cost about 142k tokens)."""
    from PIL import Image, ImageDraw
    if not 1 <= len(sheets) <= 4:
        raise SystemExit('a batch holds 1 to 4 sheets')
    ims = [Image.open(p).convert('RGB') for p in sheets]
    cols = 2 if len(ims) > 1 else 1; rows = (len(ims) + cols - 1) // cols
    tw = width // cols; th = max(round(tw * im.height / im.width) for im in ims) + 30
    canvas = Image.new('RGB', (tw * cols, th * rows), (255, 255, 255)); d = ImageDraw.Draw(canvas)
    for n, im in enumerate(ims):
        x, y = (n % cols) * tw, (n // cols) * th
        d.text((x + 6, y + 6), f'{"ABCD"[n]}: {os.path.basename(sheets[n])}', fill=(0, 0, 0))
        canvas.paste(im.resize((tw, round(tw * im.height / im.width))), (x, y + 30))
    canvas.save(out); return out


def tier0(manifest, slot_id, media=None):
    """Every code check that applies to one slot. An empty list means it may go to Tier 1."""
    sys.path.insert(0, HERE)
    import sprint
    m = json.load(open(manifest, encoding='utf-8'))
    slot = next((s for s in m['slots'] if s['id'] == slot_id), None)
    if not slot:
        return [f'{slot_id}: no such slot']
    probs = [e for e in sprint.errors(m) if e.startswith(slot_id + ':')]
    if media and not os.path.exists(media):
        probs.append(f'{media}: missing')
    elif media and media.lower().endswith(VIDEO):
        j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height:format=duration',
                                       '-of', 'json', media], capture_output=True, text=True).stdout or '{}')
        v = [s for s in j.get('streams', []) if s.get('codec_type') == 'video']
        if not v:
            probs.append(f'{media}: no video stream')
        elif v[0]['height'] <= v[0]['width']:
            probs.append(f'{media}: {v[0]["width"]}x{v[0]["height"]} is not vertical')
        dur = float(j.get('format', {}).get('duration') or 0)
        if not 3 <= dur <= 90:
            probs.append(f'{media}: {dur:.1f}s long (3 to 90 allowed)')
    return probs


def floor_quotes():
    d = json.load(open(f'{HERE}/floor.json', encoding='utf-8'))
    return [(e['id'], e['words'][0] if e['words'] else e.get('said', ''), e['rule']) for e in d['entries']]


def brief(tier, sheets):
    a = json.load(open(ANCHORS, encoding='utf-8'))
    out = []
    if tier == 'tier1':
        out.append('You are a strict checker for Heartside social posts. Open the batch image once; it holds up to four contact sheets labelled A to D. For each sheet, answer every question '
                   'yes or no. A no needs the frame time and one short reason. Do not judge taste or humour. '
                   'Reply as JSON only: {"<sheet>": {"<question id>": {"ok": true|false, "frame": "...", "why": "..."}}}.')
        out += [f'- {q["id"]} (floor {q["floor"]}): {q["ask"]}' for q in a['questions_tier1']]
    else:
        out.append("You score Heartside social posts against Krish's own bar. " + a['tier2_rubric'])
        out.append('The tens:')
        out += [f'- {t["id"]}: {t["what"]} ({t["why"]})' for t in a['tens']]
        out.append("What Krish rejected, in his words (a post that earns one of these scores 6 or below):")
        out += [f'- {i}: "{w}" -> {r}' for i, w, r in floor_quotes() if w]
        out.append('Reply as JSON only: {"<sheet>": {"score": N, "compared_to": "...", "best_beat": "...", "floor_risk": "..."}}.')
    out.append('Sheets: ' + ', '.join(sheets))
    return '\n'.join(out)


def record(slot, tier, verdict, score=None, note=''):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    row = {'slot': slot, 'tier': tier, 'verdict': verdict, 'score': score, 'note': note,
           'at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(row) + '\n')
    return row


def agreement(rows=None):
    """Of the slots the panel scored and Krish judged, how often 9+ meant yes and under 9 meant no."""
    if rows is None:
        rows = [json.loads(l) for l in open(LOG, encoding='utf-8')] if os.path.exists(LOG) else []
    panel, krish = {}, {}
    for r in rows:
        if r['tier'] == 'tier2' and r.get('score') is not None:
            panel[r['slot']] = r['score'] >= 9
        if r['tier'] == 'krish':
            krish[r['slot']] = r['verdict'] == 'krish-yes'
    both = [s for s in panel if s in krish]
    if not both:
        return None, 0
    return sum(panel[s] == krish[s] for s in both) / len(both), len(both)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('args', nargs='*')
    ap.add_argument('--out'); ap.add_argument('--score', type=float); ap.add_argument('--note', default='')
    a = ap.parse_args()
    if a.cmd == 'sheet':
        print(sheet(a.args[0], a.out or os.path.splitext(a.args[0])[0] + '.sheet.png'))
    elif a.cmd == 'batch':
        print(batch(a.args, a.out or 'batch.png'))
    elif a.cmd == 'tier0':
        p = tier0(*a.args[:3]); [print('HOLD:', x) for x in p]; print('tier0', 'pass' if not p else 'held'); sys.exit(1 if p else 0)
    elif a.cmd == 'brief':
        print(brief(a.args[0], a.args[1:]))
    elif a.cmd == 'record':
        slot, tier, verdict = a.args; print(record(slot, tier, verdict, a.score, a.note))
    elif a.cmd == 'agreement':
        rate, n = agreement()
        print('no slot judged by both the panel and Krish yet' if rate is None else
              f'panel and Krish agree on {rate:.0%} of {n}; under 80% rebuild the anchors before the next batch')
    else:
        sys.exit(f'unknown command {a.cmd}')


if __name__ == '__main__':
    main()
