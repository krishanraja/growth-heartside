"""Acceptance for picture cards: duration matches the timeline, 1080x1920, and the last shot holds long enough."""
import json, subprocess, sys

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
if not last.get('product') or last['seconds'] < 3:
    problems.append('the last shot must be the real product render, held at least 3 seconds')
print('ok' if not problems else '\n'.join(problems))
sys.exit(1 if problems else 0)
