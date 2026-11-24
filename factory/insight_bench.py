"""The insight desk's offline calibration bench: no model call, no network, nothing written.

    python3 factory/insight_bench.py [--json]

It runs the desk's two deterministic checks (factory/insight_sheet.py: insight_format and specificity) over what
Krish has already turned down and what is already live, and reports each one:

  - every concept, joke, story and bar decline in factory/floor.json (the categories are in config/insight-desk.json),
    read as the thing that was made;
  - every post already live or locked, as the joke lab reads them (factory/jokelab.py live_posts).

None of these was written from an insight, so none should pass both checks: a bench item that passes both is a gap in
the checks, printed with its id. One synthetic control, written here in the insight form and naming what only Heartside
sells, must pass both, or the checks reject everything and prove nothing.

Exit 0 when the checks are calibrated (no bench item passes both, the control passes both), 1 otherwise.
It measures the checks, never an idea's worth; a pass here is never shown to Krish as a score.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import insight_sheet  # noqa: E402

# Synthetic, written for this bench only; no customer, post or verdict.
CONTROL = ('people who live with a dog who steals their spot on the couch want to laugh about it with someone '
           'but nobody else finds it funny because only they see it every night, so a painted portrait with a note '
           'from the dog owns up to it for them')


def bench_items(adapter):
    """(kind, id, text) for every bench item, in a fixed order."""
    import jokelab
    cats = set(adapter['bench']['floor_categories'])
    floor = jokelab._load(jokelab.FLOOR, {'entries': []})
    items = [('floor', e['id'], e.get('made', '')) for e in floor.get('entries', []) if e.get('category') in cats]
    if adapter['bench'].get('include_live_posts', True):
        items += [('live', pid, text) for pid, text in jokelab.live_posts()]
    return items


def run(adapter=None):
    adapter = adapter if adapter is not None else insight_sheet.load_adapter()
    rows = []
    for kind, item_id, text in bench_items(adapter):
        fmt, fmt_why = insight_sheet.insight_format(text)
        spec, spec_why = insight_sheet.specificity(text, adapter)
        rows.append({'kind': kind, 'id': item_id, 'format': fmt, 'format_reason': fmt_why,
                     'specificity': spec, 'specificity_reason': spec_why})
    control = {'format': insight_sheet.insight_format(CONTROL)[0], 'specificity': insight_sheet.specificity(CONTROL, adapter)[0]}
    gaps = [r for r in rows if r['format'] and r['specificity']]
    return {
        'items': len(rows),
        'floor_items': sum(r['kind'] == 'floor' for r in rows),
        'live_items': sum(r['kind'] == 'live' for r in rows),
        'fail_format': sum(not r['format'] for r in rows),
        'fail_specificity': sum(not r['specificity'] for r in rows),
        'fail_both': sum(not r['format'] and not r['specificity'] for r in rows),
        'gaps': [r['id'] for r in gaps],
        'control': control,
        'calibrated': not gaps and control['format'] and control['specificity'],
        'rows': rows,
    }


def render(report):
    out = [f'insight desk bench: {report["items"]} items ({report["floor_items"]} floor declines, '
           f'{report["live_items"]} live or locked posts), offline, no model call', '']
    for r in report['rows']:
        out.append(f'  {r["kind"]:5} {r["id"]:34} format {"pass" if r["format"] else "fail"}, '
                   f'specificity {"pass" if r["specificity"] else "fail"} ({r["specificity_reason"]})')
    out += ['',
            f'fail the insight format: {report["fail_format"]} of {report["items"]}',
            f'fail specificity: {report["fail_specificity"]} of {report["items"]}',
            f'fail both: {report["fail_both"]} of {report["items"]}',
            'pass both (a gap in the checks): ' + (', '.join(report['gaps']) or 'none'),
            f'synthetic control: format {"pass" if report["control"]["format"] else "fail"}, '
            f'specificity {"pass" if report["control"]["specificity"] else "fail"}',
            'calibrated' if report['calibrated'] else 'NOT calibrated: fix the checks before a sheet relies on them']
    return '\n'.join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--json', action='store_true')
    a = p.parse_args(argv)
    report = run()
    print(json.dumps(report, ensure_ascii=False, indent=2) if a.json else render(report))
    return 0 if report['calibrated'] else 1


if __name__ == '__main__':
    sys.exit(main())
