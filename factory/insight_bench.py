"""The insight desk's offline calibration bench: no model call, no network, nothing written.

    python3 factory/insight_bench.py [--json]

It runs the desk's two deterministic checks (factory/insight_sheet.py: insight_format and specificity) over what
Krish has already turned down and what is already live, and reports each one:

  - every concept, joke, story and bar decline in factory/floor.json (the categories are in config/insight-desk.json),
    read as the thing that was made;
  - every post already live or locked, as the joke lab reads them (factory/jokelab.py live_posts).

What "calibrated" claims, and what it does not:
  - no bench item passes both checks (a bench item that does is a gap, printed with its id);
  - every floor decline fails specificity on its own: Krish turned these down, and none needs anything only Heartside
    sells. This is the one place a single check is shown to reject his declines by itself;
  - three synthetic controls: one in the insight form naming what only Heartside sells passes both; one in the insight
    form naming nothing Heartside sells fails specificity; one naming a Heartside gift but not in the insight form fails
    the format check. So each check is shown to reject something the other passes.

It does not claim that specificity alone rejects live posts. A live product post names the mug or the blanket, so it
passes specificity by design; those are counted and printed, never treated as a gap. The format check fails every bench
item almost by construction, since none was written as "X wants Y but Z because W", so its bench count shows little;
the controls are what show it works.

Exit 0 when calibrated as above, 1 otherwise.
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
# In the insight form, but a rival pet gift shop could run it unchanged: specificity must fail it.
GENERIC_CONTROL = ('people who live with a dog who steals their spot on the couch want to laugh about it with someone '
                   'but nobody else finds it funny because only they see it every night')
# Names a Heartside gift, but is not an insight: the format check must fail it.
PRODUCT_CONTROL = 'The mug with his painted portrait, now in the shop.'


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
    def checks(text):
        return {'format': insight_sheet.insight_format(text)[0], 'specificity': insight_sheet.specificity(text, adapter)[0]}

    control = checks(CONTROL)
    generic = checks(GENERIC_CONTROL)
    product = checks(PRODUCT_CONTROL)
    controls_hold = (control['format'] and control['specificity'] and generic['format'] and not generic['specificity']
                     and product['specificity'] and not product['format'])
    gaps = [r for r in rows if r['format'] and r['specificity']]
    floor_specific = [r['id'] for r in rows if r['kind'] == 'floor' and r['specificity']]
    live_specific = [r['id'] for r in rows if r['kind'] == 'live' and r['specificity']]
    return {
        'items': len(rows),
        'floor_items': sum(r['kind'] == 'floor' for r in rows),
        'live_items': sum(r['kind'] == 'live' for r in rows),
        'fail_format': sum(not r['format'] for r in rows),
        'fail_specificity': sum(not r['specificity'] for r in rows),
        'fail_both': sum(not r['format'] and not r['specificity'] for r in rows),
        'gaps': [r['id'] for r in gaps],
        'floor_pass_specificity': floor_specific,
        'live_pass_specificity': live_specific,
        'control': control,
        'generic_control': generic,
        'product_control': product,
        'calibrated': bool(not gaps and not floor_specific and controls_hold),
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
            'floor declines that pass specificity on its own (must be none): '
            + (', '.join(report['floor_pass_specificity']) or 'none'),
            f'live posts that pass specificity on its own (expected: a product post names the gift): '
            f'{len(report["live_pass_specificity"])} of {report["live_items"]}',
            'controls: ' + '; '.join(
                f'{name} format {"pass" if c["format"] else "fail"}, specificity {"pass" if c["specificity"] else "fail"}'
                for name, c in (('insight naming the gift', report['control']),
                                ('insight naming nothing only Heartside sells', report['generic_control']),
                                ('the gift named, no insight', report['product_control']))),
            'calibrated: no item passes both, no floor decline passes specificity, each control lands as expected'
            if report['calibrated'] else 'NOT calibrated: fix the checks before a sheet relies on them']
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
