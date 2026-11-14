"""Does each scheduled post have a counted path to an order? Read only; drafts only.

The North Star counts organic net sales that engine/attribution.py can see. A post sells into that number only
through a path the attribution read counts:

  tracked_link   the row's own link carries this engine's tags (growth.tracked): engine tier, the post's family.
  code           the caption carries a code Krish registered in config/codes.json: engine tier, its family.
  profile_link   the caption sends people to the profile link, and Krish has set that profile's link to the
                 tracked profile URL below (config/profile-links.json says so): engine tier, family <P>_OFFER_C900.
  none           anything else, including "Link in bio" on a profile whose link is not set, and every TikTok
                 "Link in bio" while TikTok's profile shows no clickable website (docs/briefs/2026-11-10-codes-biolink-survey.md).

A row whose path is `none` can sell, but no order it causes is counted. Nothing here writes to a Sheet, a store, a profile or config: Krish sets a profile link and creates a code
himself, then records it (rule 1).
"""
import csv
import json
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_LINKS = os.path.join(HERE, 'config', 'profile-links.json')
PREFIX = {'instagram': 'IG', 'tiktok': 'TT', 'facebook': 'FB', 'pinterest': 'PIN', 'youtube': 'YT'}
PROFILE_CONCEPT = 'C900'  # reserved: the profile link of each platform, never a post (PLAYBOOK.md, "Creative ids")
PROFILE_DAY = '20261114'
BIO = re.compile(r'link\s+in\s+(?:bio|profile)', re.I)
TAG = re.compile(r'utm_campaign=hs_growth_\d{6}&utm_content=([A-Z_0-9]+)')
PATHS = ('tracked_link', 'code', 'profile_link', 'none')


def profile_creative_id(platform):
    """The reserved creative id of a platform's profile link, for example IG_OFFER_BIO_C900_H01_V1_20261114."""
    return f'{PREFIX[platform]}_OFFER_BIO_{PROFILE_CONCEPT}_H01_V1_{PROFILE_DAY}'


def profile_url(platform, url='https://heartside.io'):
    """The tracked URL Krish would set as the profile's website. Its visits count in the engine tier."""
    import growth
    return growth.tracked(url, profile_creative_id(platform))


def set_profiles(path=None):
    """Platforms whose profile link Krish has confirmed is the tracked profile URL, {platform: date set}."""
    try:
        with open(path or PROFILE_LINKS, encoding='utf-8') as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return {}
    links = data.get('set') or {}
    if not isinstance(links, dict) or any(p not in PREFIX for p in links):
        raise ValueError('config/profile-links.json: "set" maps a platform (' + ', '.join(PREFIX) + ') to the date Krish set it')
    return {p: d for p, d in links.items() if d}


def counted_path(row, registry, profiles):
    """(path, family or reason) for one Schedule row: a dict with platform, caption, link and creative_id."""
    platform = (row.get('platform') or '').strip().lower()
    text = ' '.join([row.get('caption') or '', row.get('link') or ''])
    for m in TAG.finditer(text):
        cid = m.group(1)
        if cid == (row.get('creative_id') or '').strip():
            parts = cid.split('_')
            return 'tracked_link', f'{parts[0]}_{parts[1]}_{parts[3]}'
    words = {w.upper() for w in re.findall(r'[A-Za-z]{3,8}\d{2,3}[A-Za-z]', row.get('caption') or '')}
    for code in sorted(words):
        hits = [p for p in registry if code.startswith(p)]
        if hits:
            return 'code', registry[max(hits, key=len)]
    if BIO.search(text):
        if platform in profiles:
            return 'profile_link', f'{PREFIX[platform]}_OFFER_{PROFILE_CONCEPT}'
        if platform == 'tiktok':
            return 'none', 'TikTok "Link in bio" with no clickable website on the profile'
        return 'none', f'"Link in bio" but the {platform or "?"} profile link is not the tracked profile URL'
    return 'none', 'no tracked link, registered code or profile link'


def read_rows(path):
    with open(path, encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def audit(rows, registry=None, profiles=None):
    """Each row with its path; registry and profiles default to config/codes.json and config/profile-links.json."""
    from . import attribution
    registry = attribution.load_codes() if registry is None else registry
    profiles = set_profiles() if profiles is None else profiles
    out = []
    for row in rows:
        path, why = counted_path(row, registry, profiles)
        out.append({'slot': row.get('slot') or row.get('post_id') or '', 'platform': row.get('platform') or '',
                    'post_id': row.get('post_id') or '', 'creative_id': row.get('creative_id') or '',
                    'path': path, 'detail': why})
    return out


def render(audited):
    counts = {p: sum(1 for r in audited if r['path'] == p) for p in PATHS}
    lines = [f'{len(audited)} row(s): ' + ', '.join(f'{counts[p]} {p}' for p in PATHS), '']
    for r in audited:
        lines.append(f"{r['slot'][:24]:24} {r['platform']:10} {r['path']:13} {r['detail']}")
    lines += ['', 'Profile links Krish can set (counted in the engine tier once set and recorded in config/profile-links.json):']
    for p in ('instagram', 'tiktok', 'facebook', 'pinterest'):
        lines.append(f'  {p:10} {profile_url(p)}')
    return '\n'.join(lines)
