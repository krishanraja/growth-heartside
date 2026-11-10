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
                                      [--three-s-rate R] [--avg-watch S] [--profile-visits N] [--link-clicks N]
    python3 factory/sprint.py ids     MANIFEST [SLOT]    each slot's creative id per platform and its 02e row fields
    python3 factory/sprint.py diagnose MANIFEST          the failing stage (stop, stay, click, convert) per franchise

Views are aggregate public post counts read on the platform or from Buffer's analytics, with where they
were read (AGENTS.md rule 8). They go to local/factory/sprint-views.jsonl, never to a tracked file, so a
scheduled run changes nothing tracked (rule 9). The optional funnel fields (3-second rate, average watch,
profile visits, link clicks) are written only when the platform showed them: an absent field is "not
shown", never zero and never guessed.
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


def errors(m, others=None):
    """Everything wrong with a manifest. An empty list means it may drive production.
    others: the other sprint manifests to check concept numbers against (default: every other file in factory/sprints/)."""
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
                errs.append(f'{sid}: {f["name"]} is excluded ({f["why"]})')
            if concepts.get(s.get('concept'), {}).get('name') != f['name']:
                errs.append(f'{sid}: concept {s.get("concept")} is not in {f["name"]}')
            used_concepts[s.get('concept')] += 1
        else:
            errs.append(f'{sid}: lane must be signature or viral')
        if s.get('franchise') == 'The Human-Arms Lip-Sync' and not (s.get('track') or {}).get('title'):
            errs.append(f'{sid}: a lip-sync names its song (track title, artist and cue)')
        if s.get('track') and not all((s['track'].get(k) or '').strip() for k in ('title', 'artist', 'cue')):
            errs.append(f'{sid}: a track needs its title, artist and cue')
        if s.get('breed') == 'dachshund' and not s.get('breed_ok'):
            errs.append(f'{sid}: no chestnut or red dachshund in a generated frame (it reads as Buddy); pick another breed')
    for c, n in used_concepts.items():
        if n > 1:
            errs.append(f'{c}: used by {n} concept slots; repeats belong in double-down slots')
    for (day, p), n in sorted(load_.items()):
        if n > caps.get(p, 0):
            errs.append(f'{day} {p}: {n} posts, the cap is {caps.get(p, 0)}')
    errs += concept_errors(m, others)
    return errs


def other_manifests(m):
    """Every other sprint manifest filed in factory/sprints/, by sprint id."""
    out = []
    folder = os.path.join(HERE, 'sprints')
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        if name.endswith('.json'):
            o = load(os.path.join(folder, name))
            if o.get('sprint') != m.get('sprint'):
                out.append(o)
    return out


def concept_numbers(m):
    """{concept number: slot id} for every slot, and the errors met deriving them."""
    nums, errs = {}, []
    for s in m.get('slots', []):
        try:
            c = int(creative_id(m, s, 'tiktok').split('_')[3][1:])
        except (ValueError, KeyError, TypeError) as e:
            errs.append(f'{s.get("id", "?")}: no concept number ({e})'); continue
        if c in nums:
            errs.append(f'C{c:02d}: given to both {nums[c]} and {s.get("id")} (the viral and signature blocks overlap; '
                        'set concept_base so they do not)')
        else:
            nums[c] = s.get('id')
    return nums, errs


def concept_errors(m, others=None):
    """Concept numbers run on through the whole engine (PLAYBOOK, "Creative ids"), so a sprint's derived numbers
    may not meet the engine's own C01 to C112, each other, or any other filed sprint's. Otherwise attribution
    families (PLATFORM_PILLAR_C###) and the code registry would merge sales across posts."""
    nums, errs = concept_numbers(m)
    for c, sid in sorted(nums.items()):
        if c in ENGINE_CONCEPTS:
            errs.append(f'{sid}: C{c:02d} is in the engine\'s used range C{ENGINE_CONCEPTS[0]:02d} to C{ENGINE_CONCEPTS[-1]}')
    for o in (other_manifests(m) if others is None else others):
        theirs, _ = concept_numbers(o)
        clash = sorted(set(nums) & set(theirs))
        if clash:
            errs.append(f'{m.get("sprint")}: concept numbers C{clash[0]} to C{clash[-1]} ({len(clash)}) are already used by '
                        f'{o.get("sprint")}; give this manifest its own concept_base')
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


# ---------------------------------------------------------------------------
# Creative ids: so a sprint post can carry a tracked link and its sales land in the engine tier.
# ---------------------------------------------------------------------------
PLATFORM_CODE = {'tiktok': 'TT', 'instagram': 'IG', 'facebook': 'FB'}
# Concept numbers run on through the whole engine (PLAYBOOK, "Creative ids"). Before this sprint the engine used
# C01 to C112; a sprint reserves its own block so no two posts share a family. Overridable per manifest.
CONCEPT_BASE = {'viral': 200, 'signature': 300}
ENGINE_CONCEPTS = range(1, 113)   # C01 to C112, used before the first sprint


def slot_number(slot):
    """The number in a slot id: S01 -> 1, V100 -> 100."""
    digits = ''.join(ch for ch in str(slot.get('id', '')) if ch.isdigit())
    if not digits:
        raise ValueError(f'{slot.get("id")}: a slot id needs a number to give it a concept number')
    return int(digits)


def creative_id(m, slot, platform):
    """The creative id for one sprint slot on one platform. Deterministic: the same slot always gets the same id.

    {PLATFORM}_{PILLAR}_{FORMAT}_C{concept}_H{hook}_V{version}_{YYYYMMDD}, mapped from the slot's own fields:
      platform  tiktok TT, instagram IG, facebook FB (the slot's platforms; one id per platform)
      pillar    signature is EMO (it ends on a real gift from the dog); viral is ENT (made to travel, no product)
      format    template film, chat, search or roast is REEL; still is POST
      concept   the manifest's concept_base for the lane (default viral 200, signature 300) plus the slot number,
                so V001 is C201, V100 is C300 and S01 is C301. One slot, one concept number, so attribution's
                family (PLATFORM_PILLAR_C###) names exactly one post
      hook      H01: a sprint slot has one hook; a re-cut keeps its slot and moves the version
      version   V1, or the slot's own `version` when a re-cut is filed
      date      the slot's day
    The franchise concept (DVC-021, HAL-02) stays on the slot; it is not a number this format can carry.
    """
    if platform not in PLATFORM_CODE:
        raise ValueError(f'{platform}: a sprint posts to {", ".join(PLATFORMS)} only')
    base = {**CONCEPT_BASE, **(m.get('concept_base') or {})}
    lane = slot.get('lane')
    if lane not in base:
        raise ValueError(f'{slot.get("id")}: lane must be signature or viral')
    concept = base[lane] + slot_number(slot)
    if not 10 <= concept <= 999:
        raise ValueError(f'{slot.get("id")}: concept number {concept} does not fit C## to C###')
    pillar = 'EMO' if lane == 'signature' else 'ENT'
    fmt = 'POST' if slot.get('template') == 'still' else 'REEL'
    version = int(slot.get('version') or 1)
    day = dt.date.fromisoformat(slot['day']).strftime('%Y%m%d')
    return f'{PLATFORM_CODE[platform]}_{pillar}_{fmt}_C{concept:02d}_H01_V{version}_{day}'


def find_slot(m, slot_id):
    s = next((x for x in m['slots'] if x.get('id') == slot_id), None)
    if not s:
        raise ValueError(f'{slot_id}: no such slot in {m.get("sprint")}')
    return s


def schedule_row(m, slot, platform):
    """The engine's fields for a slot's row in its 02e Schedule Sheet, creative id included.
    Captions, media and approval are filled at filing; `approved` is always left for Krish (AGENTS.md)."""
    return {'post_id': slot['id'], 'sprint': m['sprint'], 'platform': platform, 'date': slot['day'],
            'creative_id': creative_id(m, slot, platform), 'intent': slot.get('intent', 'audience'),
            'approved': ''}


def manifest_for_slot(slot_id, sprints_dir=None):
    """The newest sprint manifest that holds a slot id, so `growth.py link URL S01` needs no path."""
    d = sprints_dir or f'{HERE}/sprints'
    for name in sorted(os.listdir(d), reverse=True):
        if name.endswith('.json'):
            m = load(os.path.join(d, name))
            if any(s.get('id') == slot_id for s in m.get('slots', [])):
                return m
    raise ValueError(f'{slot_id}: no sprint manifest in {d} has this slot')


# ---------------------------------------------------------------------------
# Diagnosis: which stage of the funnel fails, per franchise.
# ---------------------------------------------------------------------------
FUNNEL = ('three_s_rate', 'avg_watch_s', 'profile_visits', 'link_clicks')
# The next test for each failing stage, from docs/CHANNEL-TASKS.md, "Publish once; learn from the result", step 4,
# and its TikTok row; the stay fix is the hook system's on-ramp rule.
NEXT_TEST = {
    'stop': 'test a new first shot and keep everything else (CHANNEL-TASKS: early abandonment suggests testing the first shot)',
    'stay': 'keep the first shot and rework what follows it, the on-ramp (hook system: hold rate is the on-ramp\'s metric)',
    'click': 'keep the joke and test an adjacent gift-led post as its own creative (CHANNEL-TASKS: good sends but no profile visits)',
    'convert': 'check the destination first, then the offer and checkout (CHANNEL-TASKS: clicks without visits, visits without orders)',
}
MIN_MEASURED = 5  # the same floor status() uses before it computes a median; below it, build the baseline


def view_record(m, slot, platform, views, at, source, **funnel):
    """One views-log line. Funnel fields the platform did not show are left out, never written as zero."""
    rec = {'sprint': m['sprint'], 'slot': slot, 'platform': platform, 'views': int(views), 'at': at, 'source': source}
    for k in FUNNEL:
        v = funnel.get(k)
        if v is None:
            continue
        if isinstance(v, bool) or v < 0 or (k == 'three_s_rate' and v > 1):
            raise ValueError(f'{k} {v}: a count or a seconds figure is 0 or more; a 3-second rate is 0 to 1')
        rec[k] = v
    return rec


def latest_readings(m):
    """The latest reading per (slot, platform), with every field it carried."""
    last = {}
    for r in views_log():
        if r.get('sprint') == m['sprint']:
            k = (r['slot'], r['platform'])
            if k not in last or r['at'] >= last[k]['at']:
                last[k] = r
    return last


def diagnose(m, readings=None, orders=None):
    """The failing stage per franchise, with the next test. Stop, Stay, Click, Convert.

    Adapted from coreyhaines31/marketingskills, skills/ad-creative/references/hook-system.md, "The Diagnostic
    Funnel" (MIT, commit 9d6d7ce8): each stage isolates one part of a post, so read the funnel to find which part
    to fix instead of scrapping the post. Here, organic and per franchise:
      stop     3-second view rate          (three_s_rate)
      stay     average watch in seconds    (avg_watch_s)
      click    profile visits and link clicks per 1,000 views
      convert  orders per link click, when attributed orders per franchise are given (else not shown)
    No outside benchmark is used (AGENTS.md rule 8). A franchise fails a stage when it sits below the median of
    the measured franchises for that stage, read in funnel order; the first stage it fails is its diagnosis.
    A field the platform did not show is skipped, never counted as zero. Until MIN_MEASURED posts are measured
    the answer is "baseline" (CHANNEL-TASKS: a cold account has no useful median at first).

    readings: {(slot, platform): record}, default the local views log. orders: {franchise: attributed orders}.
    Returns {franchise: {'stage', 'next_test', 'posts', 'measures'}}.
    """
    readings = latest_readings(m) if readings is None else readings
    by_slot = {s['id']: s for s in m['slots']}
    groups = collections.defaultdict(lambda: {'posts': set(), 'views': 0, 'three': [], 'watch': [], 'visits': 0,
                                               'visit_views': 0, 'clicks': 0, 'click_views': 0})
    for (slot, _platform), r in readings.items():
        s = by_slot.get(slot)
        if not s:
            continue
        name = s.get('franchise') or ('double-down' if s.get('double_down') else s['lane'])
        g = groups[name]; g['posts'].add(slot); v = int(r.get('views') or 0); g['views'] += v
        if r.get('three_s_rate') is not None: g['three'].append(float(r['three_s_rate']))
        if r.get('avg_watch_s') is not None: g['watch'].append(float(r['avg_watch_s']))
        if r.get('profile_visits') is not None: g['visits'] += int(r['profile_visits']); g['visit_views'] += v
        if r.get('link_clicks') is not None: g['clicks'] += int(r['link_clicks']); g['click_views'] += v
    measures = {}
    for name, g in groups.items():
        # Each rate over the views of the posts that showed it, then added: posts that showed only one field
        # must not dilute the other's rate.
        rates = [1000 * n / v for n, v in ((g['visits'], g['visit_views']), (g['clicks'], g['click_views'])) if v]
        click = sum(rates) if rates else None
        conv = None
        if orders is not None and name in orders and g['clicks']:
            conv = orders[name] / g['clicks']
        measures[name] = {'stop': statistics.mean(g['three']) if g['three'] else None,
                          'stay': statistics.mean(g['watch']) if g['watch'] else None,
                          'click': click, 'convert': conv}
    measured_posts = len({slot for (slot, _p) in readings if slot in by_slot})
    medians = {}
    for stage in ('stop', 'stay', 'click', 'convert'):
        vals = [x[stage] for x in measures.values() if x[stage] is not None]
        medians[stage] = statistics.median(vals) if len(vals) >= 2 else None
    out = {}
    for name, x in sorted(measures.items()):
        row = {'posts': len(groups[name]['posts']), 'views': groups[name]['views'], 'measures': x}
        if measured_posts < MIN_MEASURED:
            row.update(stage='baseline', next_test=f'build the baseline: {measured_posts} of {MIN_MEASURED} posts measured; show counts')
        else:
            failing = next((st for st in ('stop', 'stay', 'click', 'convert')
                            if x[st] is not None and medians[st] is not None and x[st] < medians[st]), None)
            if failing:
                row.update(stage=failing, next_test=NEXT_TEST[failing])
            elif all(x[st] is None for st in ('stop', 'stay', 'click')):
                row.update(stage='not shown', next_test='record the funnel fields the platform shows (3-second rate, average watch, profile visits, link clicks)')
            else:
                row.update(stage='holding', next_test='at or above the sprint median on every stage shown: a double-down candidate')
        out[name] = row
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('manifest'); ap.add_argument('rest', nargs='*')
    ap.add_argument('--out'); ap.add_argument('--note', default=''); ap.add_argument('--at'); ap.add_argument('--source')
    ap.add_argument('--three-s-rate', type=float); ap.add_argument('--avg-watch', type=float)
    ap.add_argument('--profile-visits', type=int); ap.add_argument('--link-clicks', type=int)
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
        try:
            rec = view_record(m, slot, platform, views, a.at, a.source, three_s_rate=a.three_s_rate,
                              avg_watch_s=a.avg_watch, profile_visits=a.profile_visits, link_clicks=a.link_clicks)
        except ValueError as e:
            sys.exit(str(e))
        with open(VIEWS, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec) + '\n')
        print('recorded'); return
    if a.cmd == 'ids':
        try:
            slots = [find_slot(m, a.rest[0])] if a.rest else m['slots']
            for s in slots:
                for p in s['platforms']:
                    print(json.dumps(schedule_row(m, s, p)))
        except ValueError as e:
            sys.exit(str(e))
        return
    if a.cmd == 'diagnose':
        for name, row in diagnose(m).items():
            print(f"{name}: {row['stage']} ({row['posts']} posts, {row['views']:,} views); next: {row['next_test']}")
        return
    sys.exit(f'unknown command {a.cmd}')


if __name__ == '__main__':
    main()
