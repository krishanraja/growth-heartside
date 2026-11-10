"""The sprint ledger: many posts in a fixed window, every one tracked from idea to its 72-hour read.

Krish, 2026-11-10: "produce 20 signature Heartside organic posts, and 100 viral posts that generate
500000 views between them in the next 10 days". The plan is docs/plans/2026-11-10-sprint-120.md; the
manifest (factory/sprints/<id>.json) holds one slot per post. This tool keeps the manifest honest and
turns approved slots into factory specs, so a batch of 100 is built and checked like one post.

    python3 factory/sprint.py check   MANIFEST           structure, counts, grades, renders, platform caps
    python3 factory/sprint.py status  MANIFEST           where every slot is, views against the target, winners
    python3 factory/sprint.py specs   MANIFEST [--out D] a factory spec for every approved still slot
    python3 factory/sprint.py advance MANIFEST SLOT STAGE [--note ...]   move a slot (interactive sessions only)
    python3 factory/sprint.py views   MANIFEST SLOT PLATFORM VIEWS --at ISO --source WHERE

Views are aggregate public post counts read on the platform or from Buffer's analytics, with where they
were read (AGENTS.md rule 8). They go to local/factory/sprint-views.jsonl, never to a tracked file, so a
scheduled run changes nothing tracked (rule 9).
"""
import argparse, collections, datetime as dt, json, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VIEWS = os.environ.get('HEARTSIDE_SPRINT_VIEWS', f'{ROOT}/local/factory/sprint-views.jsonl')

# In order. A slot moves forward one gate at a time; `held` and `dropped` can happen at any gate.
STAGES = ['reserved', 'idea', 'script', 'script_approved', 'still', 'checked', 'shown', 'approved',
          'built', 'locked', 'filed', 'row_approved', 'live', 'read_72h']
SIDE = ['held', 'dropped']
PLATFORMS = ('tiktok', 'instagram', 'facebook')
TEMPLATES = ('still', 'film', 'chat', 'search', 'roast')
PRODUCTS = ('mug', 'portrait', 'blanket', 'card')


def load(path):
    return json.load(open(path, encoding='utf-8'))


def franchises():
    return {f['name']: f for f in load(f'{HERE}/bank/franchises.json')['franchises']}


def renders():
    return load(f'{HERE}/bank/renders.json')['renders']


def errors(m):
    """Everything wrong with a manifest. An empty list means it may drive production."""
    errs, fr = [], franchises()
    concepts = {c['id']: f for f in fr.values() for c in f['concepts']}
    rs = renders()
    slots = m.get('slots', [])
    ids = [s.get('id') for s in slots]
    for d in sorted({i for i in ids if ids.count(i) > 1}):
        errs.append(f'{d}: slot id used twice')
    start, end = dt.date.fromisoformat(m['window']['start']), dt.date.fromisoformat(m['window']['end'])
    lanes = collections.Counter(s.get('lane') for s in slots)
    for lane, want in m['targets']['posts'].items():
        if lanes[lane] != want:
            errs.append(f'{lane}: {lanes[lane]} slots, the target is {want}')
    caps = m['caps']['per_platform_per_day']
    load_ = collections.Counter()
    used_concepts = collections.Counter()
    for s in slots:
        sid = s.get('id', '?')
        if s.get('stage') not in STAGES + SIDE:
            errs.append(f'{sid}: unknown stage {s.get("stage")}')
        if s.get('template') not in TEMPLATES:
            errs.append(f'{sid}: unknown template {s.get("template")}')
        try:
            day = dt.date.fromisoformat(s['day'])
            if not start <= day <= end:
                errs.append(f'{sid}: {day} is outside the sprint window')
        except (KeyError, ValueError):
            errs.append(f'{sid}: no valid day'); day = None
        plats = s.get('platforms') or []
        if not plats or any(p not in PLATFORMS for p in plats):
            errs.append(f'{sid}: platforms must be from {", ".join(PLATFORMS)}')
        for p in plats:
            if day: load_[(day, p)] += 1
        if s.get('lane') == 'signature':
            if s.get('product') not in PRODUCTS:
                errs.append(f'{sid}: a signature post ends on a real product ({", ".join(PRODUCTS)})')
            elif not any(r['product'] == s['product'] and r['breed'] in (s.get('breed'), 'any') for r in rs):
                errs.append(f'{sid}: no approved {s["product"]} render for a {s.get("breed")}')
            if not s.get('premise') or not s.get('payoff'):
                errs.append(f'{sid}: a signature slot states its premise and its payoff without the caption (floor dumb-stopping)')
        elif s.get('lane') == 'viral':
            if s.get('double_down'):
                if day and day < start + dt.timedelta(days=m['rules']['double_down_from_day'] - 1):
                    errs.append(f'{sid}: a double-down slot cannot fall before the first 72-hour read')
                continue
            f = fr.get(s.get('franchise'))
            if not f:
                errs.append(f'{sid}: franchise {s.get("franchise")} is not in bank/franchises.json'); continue
            if f['grade'] == 'C':
                errs.append(f'{sid}: {f["name"]} is excluded for generated media ({f["why"]})')
            if concepts.get(s.get('concept'), {}).get('name') != f['name']:
                errs.append(f'{sid}: concept {s.get("concept")} is not in {f["name"]}')
            used_concepts[s.get('concept')] += 1
        else:
            errs.append(f'{sid}: lane must be signature or viral')
        if s.get('breed') == 'dachshund' and not s.get('breed_ok'):
            errs.append(f'{sid}: no chestnut or red dachshund in a generated frame (it reads as Buddy); pick another breed')
    for c, n in used_concepts.items():
        if n > 1:
            errs.append(f'{c}: used by {n} concept slots; repeats belong in double-down slots')
    for (day, p), n in sorted(load_.items()):
        if n > caps.get(p, 0):
            errs.append(f'{day} {p}: {n} posts, the cap is {caps.get(p, 0)}')
    return errs


def views_log():
    if not os.path.exists(VIEWS):
        return []
    return [json.loads(l) for l in open(VIEWS, encoding='utf-8') if l.strip()]


def latest_views(m):
    """The latest reading per (slot, platform), summed per slot."""
    last = {}
    for r in views_log():
        if r.get('sprint') == m['sprint']:
            k = (r['slot'], r['platform'])
            if k not in last or r['at'] >= last[k]['at']:
                last[k] = r
    per = collections.Counter()
    for (slot, _), r in last.items():
        per[slot] += int(r['views'])
    return per


def status(m, today=None):
    today = today or dt.date.today()
    out, slots = [], m['slots']
    by = collections.defaultdict(collections.Counter)
    for s in slots:
        by[s['lane']][s['stage']] += 1
    out.append(f"Sprint {m['sprint']}: {m['window']['start']} to {m['window']['end']}")
    for lane in ('signature', 'viral'):
        parts = [f'{st} {by[lane][st]}' for st in STAGES + SIDE if by[lane][st]]
        out.append(f'  {lane:9} {sum(by[lane].values()):3}: ' + ', '.join(parts))
    per = latest_views(m); total = sum(per.values()); target = m['targets']['views']
    end = dt.date.fromisoformat(m['window']['end'])
    days_left = max((end - today).days + 1, 0)
    live = [s for s in slots if s['id'] in per]
    out.append(f'  views {total:,} of {target:,} ({total / target:.1%}); {len(live)} posts measured; '
               f'{days_left} day(s) left' + (f', need {max(target - total, 0) // max(days_left, 1):,} a day' if days_left else ''))
    if len(live) >= 5:
        med = statistics.median(per[s['id']] for s in live)
        win = [s['id'] for s in live if per[s['id']] >= m['rules']['winner_multiple'] * med]
        lose = [s['id'] for s in live if per[s['id']] < m['rules']['retire_below_multiple'] * med]
        out.append(f'  median {med:,.0f}; winners (>= {m["rules"]["winner_multiple"]}x): {", ".join(win) or "none"}; '
                   f'below {m["rules"]["retire_below_multiple"]}x: {len(lose)}')
    due = [s['id'] for s in slots if s.get('day') == today.isoformat() and s['stage'] not in ('live', 'read_72h', 'dropped')]
    if due:
        out.append(f'  due today and not live: {", ".join(due)}')
    return '\n'.join(out)


def specs(m, out_dir):
    """A still spec for every approved slot that names its photos and lines. Returns what it wrote."""
    from engine.creative_ui import REVISION
    os.makedirs(out_dir, exist_ok=True); wrote = []
    ready = STAGES[STAGES.index('approved'):]
    for s in m['slots']:
        if s['template'] != 'still' or s['stage'] not in ready or not s.get('slides'):
            continue
        spec = {'id': s['id'], 'template': 'still', 'ui_profile': REVISION, 'breed': s['breed'],
                'aspect': s['aspect'], 'slides': s['slides'], 'sprint': m['sprint']}
        if s.get('concept'): spec['concept'] = s['concept']
        if s.get('variant_of'): spec['variant_of'] = s['variant_of']
        if s.get('end_renders'): spec['end'] = {'renders': s['end_renders']}
        p = os.path.join(out_dir, f"{s['id']}.json")
        json.dump(spec, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); wrote.append(p)
    return wrote


def advance(m, slot, stage, note=''):
    s = next((x for x in m['slots'] if x['id'] == slot), None)
    if not s:
        raise SystemExit(f'{slot}: no such slot')
    if stage not in STAGES + SIDE:
        raise SystemExit(f'{stage}: not a stage')
    if stage in STAGES and s['stage'] in STAGES and STAGES.index(stage) != STAGES.index(s['stage']) + 1:
        raise SystemExit(f'{slot}: {s["stage"]} moves to {STAGES[STAGES.index(s["stage"]) + 1]} next, not {stage}')
    s.setdefault('history', []).append({'from': s['stage'], 'to': stage, 'note': note,
                                        'at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')})
    s['stage'] = stage


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('manifest'); ap.add_argument('rest', nargs='*')
    ap.add_argument('--out'); ap.add_argument('--note', default=''); ap.add_argument('--at'); ap.add_argument('--source')
    a = ap.parse_args(); m = load(a.manifest)
    if a.cmd == 'check':
        e = errors(m); [print('PROBLEM:', x) for x in e]
        print(f"{m['sprint']}: {'ready' if not e else str(len(e)) + ' problem(s)'} ({len(m['slots'])} slots)"); sys.exit(1 if e else 0)
    if a.cmd == 'status':
        print(status(m)); return
    if a.cmd == 'specs':
        sys.path.insert(0, ROOT)
        w = specs(m, a.out or f'{ROOT}/local/factory/specs/{m["sprint"]}'); print(f'{len(w)} spec(s) written'); [print(' ', p) for p in w]; return
    if a.cmd == 'advance':
        slot, stage = a.rest; advance(m, slot, stage, a.note)
        json.dump(m, open(a.manifest, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); print(slot, '->', stage); return
    if a.cmd == 'views':
        slot, platform, views = a.rest
        if not a.at or not a.source:
            sys.exit('views needs --at (when it was read) and --source (where it was read)')
        if platform not in PLATFORMS or slot not in {s['id'] for s in m['slots']}:
            sys.exit('unknown slot or platform')
        os.makedirs(os.path.dirname(VIEWS), exist_ok=True)
        with open(VIEWS, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'sprint': m['sprint'], 'slot': slot, 'platform': platform, 'views': int(views), 'at': a.at, 'source': a.source}) + '\n')
        print('recorded'); return
    sys.exit(f'unknown command {a.cmd}')


if __name__ == '__main__':
    main()
