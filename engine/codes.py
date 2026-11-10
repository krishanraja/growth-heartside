"""Post-family discount code names, drafted for Krish to switch on. Drafts only.

R-3 (docs/briefs/2026-10-27-architecture.md) approved drafting post-family codes. A code is a tracking
word a buyer types at checkout; it carries no discount by default, because every dollar off comes out of
the profit goal. Krish creates each code in Shopify himself and then registers its family in
config/codes.json, which is when engine/attribution.py starts counting it. Nothing here writes to the store,
to config/codes.json or to any tracked file.

Only slots that sell get a code: intent buy, or the signature lane. A standalone joke never carries a code
line (docs/CHANNEL-TASKS.md: no product slide, hashtag or shop link on an approved standalone joke).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORM_LETTER = {'tiktok': 'T', 'instagram': 'I', 'facebook': 'F'}
STOP = {'the', 'a', 'an', 'my', 'your', 'our', 'of', 'and', 'to', 'in', 'on', 'for', 'with', 'from', 'at', 'is', 'it',
        # Words that say nothing to a buyer typing them, or read as an internal label.
        'who', 'one', 'dog', 'dogs', 'draft', 'what', 'when', 'this', 'that', 'not', 'but', 'all', 'you', 'are', 'was',
        'has', 'have', 'got', 'get', 'each', 'every', 'some', 'his', 'her', 'its', 'out', 'off', 'day', 'new', 'test', 'slot', 'post', 'reel'}


def _banned():
    """Heartside's banned and slop words (growth.py), so a public code never says one."""
    try:
        sys.path.insert(0, HERE)
        import growth
        return {w.lower() for w in list(growth.BANNED) + list(growth.SLOP)}
    except (ImportError, AttributeError):
        return set()


def _sprint():
    sys.path.insert(0, os.path.join(HERE, 'factory'))
    import sprint
    return sprint


def selling(slot):
    """True for a slot that may carry a code line: intent buy or a signature post."""
    return slot.get('intent') == 'buy' or slot.get('lane') == 'signature'


def word(slot, banned=None):
    """The tracking word: the first whole word of the slot's title worth saying out loud, 3 to 8 letters, never
    cut off, never a stop word and never a word Heartside bans. HEART when the title has none."""
    banned = _banned() if banned is None else banned
    for w in re.findall(r"[A-Za-z]+", slot.get('title') or ''):
        lw = w.lower()
        if 3 <= len(w) <= 8 and lw not in STOP and lw not in banned:
            return w.upper()
    return 'HEART'


def draft(m):
    """One draft per selling slot and platform: the code name, its family and no discount."""
    sprint = _sprint()
    banned = _banned()
    out = []
    for slot in m['slots']:
        if not selling(slot):
            continue
        for platform in slot.get('platforms') or []:
            cid = sprint.creative_id(m, slot, platform)
            plat, pillar, _fmt, concept = cid.split('_')[:4]
            out.append({'slot': slot['id'], 'platform': platform, 'creative_id': cid,
                        'family': f'{plat}_{pillar}_{concept}',
                        'code': f'{word(slot, banned)}{concept[1:]}{PLATFORM_LETTER[platform]}',
                        'discount': None, 'status': 'draft: Krish creates it in Shopify, then registers it'})
    codes = [d['code'] for d in out]
    clash = sorted({c for c in codes if codes.count(c) > 1})
    if clash:
        raise ValueError('two drafts share a code: ' + ', '.join(clash))
    prefixes = sorted(codes)
    for a, b in zip(prefixes, prefixes[1:]):
        if b.startswith(a):
            raise ValueError(f'{a} is a prefix of {b}: the registry could not tell them apart')
    return out


def registry(drafts):
    """The families block these drafts would add to config/codes.json, once each code exists in Shopify."""
    return {d['code']: d['family'] for d in drafts}


def render(drafts):
    lines = [f'{len(drafts)} draft code(s), tracking words with no discount. Nothing is switched on: Krish creates each '
             'code in Shopify, then adds its line to config/codes.json.', '']
    for d in drafts:
        lines.append(f"{d['slot']:5} {d['platform']:10} {d['code']:14} {d['family']:12} {d['creative_id']}")
    return '\n'.join(lines)
