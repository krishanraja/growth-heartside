"""Acceptance for picture cards against the 12 Nov corpus profile (engine/creative_ui.py).

    python3 codex/check_picture.py VIDEO TIMELINE

Checks: 1080x1920; duration matches the timeline; the export preset (H.264 yuv420p BT.709, constant
frame rate, AAC 48 kHz stereo, true peak at or under -1 dBTP); the last shot is the real product render,
held 3 to 4 s (Krish's floor endings-land, never a dead outro); and every on-screen label sits at one
fixed `label_box` inside the critical box (x 120 to 820, y 330 to 1180), at most 12 words, never moving
between shots (floor fixed-label-position). A timeline with labels must record `label_box`: the
position the card drew them at, in 1080x1920 pixels.
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.creative_ui import CRITICAL, END_HOLD, HOOK_WORDS, inside, media_errors, words

video, timeline = sys.argv[1], sys.argv[2]
t = json.load(open(timeline))
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                            'stream=width,height:format=duration', '-of', 'json', video]))
w, h = probe['streams'][0]['width'], probe['streams'][0]['height']
dur = float(probe['format']['duration'])
want = sum(s['seconds'] for s in t['shots'])
problems = []
if (w, h) != (1080, 1920):
    problems.append(f'size is {w}x{h}, want 1080x1920')
if abs(dur - want) > 0.25:
    problems.append(f'duration {dur:.2f}s, timeline says {want:.2f}s')
last = t['shots'][-1]
if not last.get('product') or not END_HOLD[0] <= last['seconds'] <= END_HOLD[1]:
    problems.append('the last shot must be the real product render, held 3 to 4 seconds')
labelled = [s for s in t['shots'] if s.get('label')]
boxes = {tuple(s.get('label_box') or t.get('label_box') or ()) for s in labelled}
if labelled:
    if boxes == {()}:
        problems.append('labels carry no label_box: record where the card drew them')
    elif len(boxes) > 1:
        problems.append('labels move between shots: one fixed label_box for the whole reel')
    for box in boxes - {()}:
        if not inside(list(box), CRITICAL):
            problems.append(f'label_box {list(box)} leaves the critical box {CRITICAL}')
    for s in labelled:
        if words(s['label']) > HOOK_WORDS:
            problems.append(f"label {s['label']!r}: more than {HOOK_WORDS} words")
problems += ['export: ' + x for x in media_errors(video)[0]]
print('ok' if not problems else '\n'.join(problems))
sys.exit(1 if problems else 0)
