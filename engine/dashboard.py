"""Build Control Center's report format from verified local evidence.

No credentials or provider calls. The existing post command handles delivery.
Reports remain evidence, with prepared recommendations linked to their owner.
"""
import datetime as dt
import json
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo

from . import ledger


MEASURES = ('net_sales', 'orders', 'sessions', 'sessions_with_cart_additions',
            'sessions_that_reached_checkout', 'sessions_that_completed_checkout')


def build(db, state, start, end, timezone, pack_date, engine_revision, recommendations):
    dt.date.fromisoformat(pack_date)
    if len(state.get('sha', '')) != 40 or not state.get('rules_ok'):
        raise ValueError('report needs a valid, approved product sync')
    summary = ledger.summary(db, start, end, timezone)
    common = {'pack_date': pack_date, 'venture': 'heartside', 'heartside_sha': state['sha'],
              'source_revision': state['sha']}
    rows = []
    for metric in MEASURES:
        evidence = summary['evidence'].get(metric, [])
        note = (f'{metric}: {start} inclusive to {end} exclusive, {timezone}, USD. '
                f'Coverage {summary["covered_days"].get(metric, 0)} of {summary["days"]} days. ')
        if evidence:
            note += 'Sources: ' + '; '.join(f'{e["source"]}, observed {e["observed_at"]}, [{e["start"]}, {e["end"]})' for e in evidence)
        else:
            note += 'Not shown. No matching aggregate report imported.'
        rows.append({'platform': 'shopify', metric: summary['totals'].get(metric), 'note': note})
    numbers = {**common, 'kind': 'numbers', 'headline': f'Heartside sales and funnel evidence: {start} to {end} (end exclusive)',
               'items': [], 'numbers': rows}

    latest = db.execute('''SELECT status, count(*) AS n FROM (
      SELECT status, row_number() OVER (PARTITION BY creative_id ORDER BY updated_at DESC, rowid DESC) AS rank
      FROM creatives) WHERE rank=1 GROUP BY status''').fetchall()
    statuses = ', '.join(f'{row["n"]} {row["status"]}' for row in latest) or 'no creative revisions recorded'
    report = {**common, 'kind': 'report', 'headline': 'Heartside growth: work completed, evidence and the next constraints', 'items': [
        {'platform': 'other', 'target_name': 'Growth engine implementation',
         'target_url': 'https://github.com/krishanraja/growth-heartside/pull/1',
         'why': 'Reviewable build evidence; a draft PR is not a deployed engine.',
         'text': f'Engine source {engine_revision}. Product source {state["sha"]}, synced {state.get("synced_at", "not shown")}. Latest recorded creative revisions: {statuses}. Media is still local to the runner; this dashboard cannot preview it yet.'},
        {'platform': 'other', 'target_name': 'Read the acquisition strategy',
         'target_url': 'https://github.com/krishanraja/growth-heartside/blob/codex/growth-engine-v3/STRATEGY.md',
         'text': 'Goal: $10,000 of Shopify net sales in one calendar month. Store totals do not prove which creative caused a sale. No channel, customer, margin or sharing result is inferred from missing data. Platform insights, cross-machine storage and confirmed social publication remain separate evidence.'},
    ]}
    for item in recommendations:
        if not all(isinstance(item.get(k), str) and item[k].strip() for k in ('title', 'why', 'next_action', 'closes_when', 'target_url')):
            raise ValueError('each recommendation needs title, why, next_action, closes_when and target_url')
        report['items'].append({'platform': 'other', 'target_name': item['title'], 'target_url': item['target_url'],
                                'why': item['why'], 'text': f'Next: {item["next_action"]}\nComplete when: {item["closes_when"]}'})
    return numbers, report


def write(root, db, state, start, end, timezone, pack_date=None):
    root = Path(root)
    day = pack_date or dt.datetime.now(ZoneInfo('America/New_York')).date().isoformat()
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True, check=True)
    revision = result.stdout.strip()
    dirty = subprocess.run(['git', 'diff', '--quiet'], cwd=root).returncode != 0
    revision += ' (working tree has changes)' if dirty else ''
    recommendations = json.loads((root / 'recommendations.json').read_text())
    packs = build(db, state, start, end, timezone, day, revision, recommendations)
    out = root / 'local/drafts/dashboard'
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for pack in packs:
        path = out / f'{day}-{pack["kind"]}.json'
        path.write_text(json.dumps(pack, indent=2, allow_nan=False) + '\n')
        paths.append(path)
    return paths
