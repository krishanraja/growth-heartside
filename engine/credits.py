"""Prepaid credits, protocol 1.16.0 (docs/CONTROL-CENTER-BRIEF.md, "Prepaid credits").

The directive's optional `credits` block names each prepaid pool placed on
Heartside, its share and what is left of it. Absent means unknown: nothing is
spent. The spending happens in the daily credits session (jobs/credits.md),
which reserves and settles each generation through Control Center. The
unattended runner spends nothing today; when it does, every spend goes through
`reserve` here, bounded by `remaining_for_you`, and is reported once in
`credits_spent`.
"""
from decimal import Decimal
import re

from . import providers

VERSION = '1.16.0'
MAX_SPENT = 40
POOL = re.compile(r'^[a-z0-9][a-z0-9_-]{0,63}$')
OBJECTIVE = re.compile(r'^[a-z][a-z0-9_]{0,63}$')


def read(directive):
    """The pools from a directive response or body, or None when the block is absent or unreadable."""
    body = (directive or {}).get('directive', directive) or {}
    block = body.get('credits') if isinstance(body, dict) else None
    if not isinstance(block, dict) or not isinstance(block.get('pools'), list):
        return None
    pools = []
    for p in block['pools']:
        if not isinstance(p, dict) or not isinstance(p.get('pool'), str) or not POOL.match(p['pool']):
            continue
        left = p.get('remaining_for_you')
        if isinstance(left, bool) or not isinstance(left, (int, float)) or left < 0:
            continue
        pools.append(p)
    return pools


def lines(pools):
    """One activity line per pool: what is left for Heartside and the last day to use it."""
    if pools is None:
        return ['No prepaid credits block in the directive: the share is unknown, so nothing was spent.']
    if not pools:
        return ['The directive places no prepaid credit pool on Heartside.']
    return [f'{p.get("tool") or p["pool"]}: {p["remaining_for_you"]:g} {p.get("unit") or "credits"} left for Heartside, '
            f'use by {p.get("use_by") or "an unknown day"}; spent by the daily credits session (jobs/credits.md).' for p in pools]


def allowance(pools, pool):
    """What this engine may still spend from one pool, or refuse when it is unknown."""
    if pools is None:
        raise ValueError('the credits block is unknown; nothing is spent')
    match = next((p for p in pools if p['pool'] == pool), None)
    if match is None:
        raise ValueError(f'no prepaid pool {pool} is placed on Heartside')
    return Decimal(str(match['remaining_for_you']))


def reserve(db, request, pools, pool, run_id):
    """Reserve one prepaid generation through the provider ledger, never past the share.

    Every reservation of this run counts against `remaining_for_you`, which Control
    Center already reduced by what earlier reports and the session spent.
    """
    request = dict(request, allocation=f'credits:{pool}:{run_id}')
    return providers.reserve(db, request, credit_allowance=allowance(pools, pool))


def spent(items):
    """The report's credits_spent: checked, at most 40, in the schema's shape."""
    out = []
    for item in items or ():
        if not isinstance(item, dict) or not POOL.match(str(item.get('pool', ''))):
            raise ValueError('a credits_spent entry names a pool')
        amount = item.get('amount')
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError('a credits_spent amount is positive')
        asset = str(item.get('asset') or '').strip()
        if not asset or len(asset) > 200 or '@' in asset:
            raise ValueError('a credits_spent asset is what was made, in words')
        key = item.get('objective_key')
        if key is not None and not (isinstance(key, str) and OBJECTIVE.match(key)):
            raise ValueError('a credits_spent objective_key is an objective key or null')
        out.append({'pool': item['pool'], 'amount': amount, 'asset': asset, 'objective_key': key})
    if len(out) > MAX_SPENT:
        raise ValueError('at most 40 credits_spent entries a report')
    return out
