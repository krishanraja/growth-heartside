"""Bind public prices and purchase links to the specific canonical, live gift."""
import datetime as dt
from decimal import Decimal, InvalidOperation
import re
from urllib.parse import urlparse, parse_qs


MONEY = re.compile(r'\$(\d+(?:\.\d{1,2})?)(?!\d|[.,]\d)')
BUY = re.compile(r'\b(?:buy|shop|order (?:now|yours|today)|add to cart)\b', re.I)


def cents(value):
    try:
        number = Decimal(str(value))
        if not number.is_finite() or number < 0 or number != number.quantize(Decimal('.01')):
            raise ValueError('price must be nonnegative with at most two decimal places')
        return int(number * 100)
    except (InvalidOperation, TypeError):
        raise ValueError('invalid price') from None


# The gifts heartside's canon prices, by the word its "configured baseline" uses.
# The order is the lead order for purchase drafts: the mug sits below the 30%
# net floor in every modeled case (heartside NOW.md, ECONOMICS), so it never leads.
GIFTS = ('blanket', 'portrait', 'mug')
LEAD_GIFTS = ('blanket', 'portrait')
ADD_ONS = {"artist's touch": 'artists-touch'}
BASELINE = re.compile(r'(?:\$|USD)\s?(\d+(?:\.\d{2})?)\s+(?:(?:un)?framed\s+)?(' + '|'.join(GIFTS) + r')\b', re.I)
ADD_ON = re.compile(r"(?:\$|USD)\s?(\d+(?:\.\d{2})?)\s+(artist'?s touch)", re.I)
BUNDLE = re.compile(r'(\d{1,2})% off two gifts, (\d{1,2})% off three or more', re.I)


def canonical_offers(texts):
    """Read gift prices from the canon's "configured baseline" sentences, never a hardcoded list.

    Every canon source that states a baseline must agree. A disagreement is a
    truth conflict, so the gift is marked and never offered for sale."""
    found, sources = {}, {}
    for path, text in texts.items():
        for sentence in re.split(r'(?<=[.;])\s+', text or ''):
            pairs = []
            if re.search(r'\bbaseline\b', sentence, re.I):
                pairs += [(m.group(2).lower(), m.group(1)) for m in BASELINE.finditer(sentence)]
            pairs += [(ADD_ONS[m.group(2).lower().replace("artists", "artist's")], m.group(1))
                      for m in ADD_ON.finditer(sentence)]
            per = {}
            for gift, price in pairs:
                per.setdefault(gift, set()).add(cents(price))
            for gift, prices in per.items():
                found.setdefault(gift, []).append((path, frozenset(prices)))
        bundle = BUNDLE.search(text or '')
        if bundle and 'bundle' not in sources:
            sources['bundle'] = {'2': int(bundle.group(1)), '3': int(bundle.group(2)), 'source': path}
    result = []
    for gift in list(GIFTS) + list(ADD_ONS.values()):
        if gift not in found:
            continue
        sets = {prices for _, prices in found[gift]}
        prices = sorted(set().union(*sets))
        result.append({'id': gift, 'name': gift.replace('-', ' ').replace('artists', "artist's"),
                       'kind': 'gift' if gift in GIFTS else 'add_on',
                       'price_cents': prices[0], 'prices_cents': prices,
                       'bundle_pct': ({k: v for k, v in sources['bundle'].items() if k != 'source'}
                                      if gift in GIFTS and 'bundle' in sources else None),
                       'conflict': len(sets) > 1,
                       'source': ', '.join(sorted({p for p, _ in found[gift]}))})
    return result


def _match(offer, products):
    word = re.compile(r'\b' + re.escape(offer['name']) + r'\b', re.I)
    matches = [p for p in products if word.search(p['title'])]
    return matches[0] if len(matches) == 1 else None


def catalog(state):
    products = state.get('store') or []
    result = []
    for offer in state.get('offers') or []:
        offer = {'prices_cents': [offer['price_cents']], **offer}
        product = _match(offer, products)
        live_prices = ([v['price'] for v in product['variants'] if v.get('available')]
                       if product and 'variants' in product else (product or {}).get('prices', []))
        live = {cents(p) for p in live_prices}
        price_matches = bool(product and set(offer['prices_cents']) <= live)
        reason = ('canon sources disagree on its price' if offer.get('conflict') else
                  'public catalog could not be checked' if state.get('store') is None else
                  'not in the public catalog' if not product else
                  'not available' if not product.get('available') else
                  'public price differs from the canon' if not price_matches else 'available at the approved price')
        result.append({**offer, 'title': product['title'] if product else None,
                       'ready': bool(product and product.get('available') and price_matches and not offer.get('conflict')),
                       'product': product, 'reason': reason})
    return result


def fresh_store(state, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    if not isinstance(state.get('store'), list):
        return False
    try:
        stamp = dt.datetime.fromisoformat(state['synced_at'])
        age = now - stamp
        return stamp.tzinfo is not None and dt.timedelta(0) <= age <= dt.timedelta(hours=26)
    except (KeyError, ValueError, TypeError):
        return False


def validate_item(item, public_text, state):
    errors = []
    declared = item.get('offers') or []
    if not isinstance(declared, list):
        return ['offers must be a list of named gift prices']
    quoted = [cents(v) for v in MONEY.findall(public_text)]
    purchase = item.get('intent') == 'buy' or bool(quoted) or bool(BUY.search(public_text))
    if item.get('intent', 'audience') not in ('audience', 'buy'):
        errors.append('intent must be audience or buy')
    if purchase and not declared:
        return errors + ['purchase copy or a public price needs offers with gift id, quantity and unit_price']
    if purchase and not fresh_store(state):
        errors.append('purchase copy needs a public catalog sync less than 26 hours old')
    known = {o['id']: o for o in catalog(state)}
    amounts, total, seen = set(), 0, set()
    for entry in declared:
        if not isinstance(entry, dict):
            errors.append('each offer must be an object'); continue
        oid, quantity = entry.get('id'), entry.get('quantity', 1)
        offer = known.get(oid)
        if not offer or oid in seen:
            errors.append(f'unknown or duplicate gift {oid}'); continue
        seen.add(oid)
        if isinstance(quantity, bool) or not isinstance(quantity, int) or not 1 <= quantity <= 20:
            errors.append(f'{oid}: quantity must be an integer from 1 to 20'); continue
        try:
            price = cents(entry['unit_price'])
        except (KeyError, ValueError):
            errors.append(f'{oid}: unit_price must be a valid dollar amount'); continue
        allowed = set(offer['prices_cents'])
        # A discount requires a second distinct gift and explicit, currently
        # confirmed bundle evidence. A canon sentence alone cannot prove activation.
        gifts = sum(1 for e in declared if isinstance(e, dict) and (known.get(e.get('id')) or {}).get('kind') == 'gift')
        pct = (offer.get('bundle_pct') or {}).get(str(min(gifts, 3)))
        if (pct and offer.get('kind') == 'gift' and state.get('bundle_verified_at') and
                state.get('bundle_verified_at') == state.get('synced_at')):
            allowed |= {round(p * (100 - pct) / 100) for p in offer['prices_cents']}
        if price not in allowed:
            errors.append(f'{oid}: price does not match this gift or a verified bundle')
        if purchase and not offer['ready']:
            errors.append(f'{oid}: {offer["reason"]}')
        amounts.add(price)
        total += price * quantity
    amounts.add(total)
    if any(price not in amounts for price in quoted):
        errors.append('a quoted price does not match the declared gift prices or basket total')
    for offer in known.values():
        names = [n for n in (offer['name'], offer.get('title')) if n]
        if purchase and offer['id'] not in seen and any(
                re.search(r'\b' + re.escape(n) + r'\b', public_text, re.I) for n in names):
            errors.append(f'copy names the {offer["name"]} without declaring that gift')
    if purchase:
        urls = re.findall(r'https?://[^\s)>\]"\']+', public_text)
        own = [u for u in urls if urlparse(u).hostname in ('heartside.io', 'www.heartside.io')]
        if not own:
            errors.append('purchase copy needs a tracked link to its active gift or a verified gifts landing page')
        for url in own:
            parsed = urlparse(url)
            direct = any(o.get('product') and urlparse(o['product']['url']).path == parsed.path
                         for oid, o in known.items() if oid in seen)
            landing = (parsed.path == '/' and
                       (parse_qs(parsed.query).get('view') == ['gifts'] or state.get('homepage_v3')) and
                       all(o['ready'] for o in known.values()) and bool(known))
            if not (direct or landing):
                errors.append('purchase link does not lead to its declared gift or a ready gifts landing page')
    return errors


def purchase_campaign(spec, state):
    """A ready single-gift conversion draft for the lead gift the film ends on (the blanket or the portrait).

    The mug is shown in audience films but never sold as the hero offer: it sits
    below the 30% net floor in every modeled case (heartside NOW.md, ECONOMICS)."""
    if not state or not state.get('homepage_v3') or not fresh_store(state):
        return None
    from .assets import PRODUCT_IMAGES
    last = spec['scenes'][-1]['asset']
    shown = PRODUCT_IMAGES.get(last[0] if isinstance(last, list) else last, (None,))[0]
    gift = next((o for o in catalog(state) if o['id'] == shown and o['id'] in LEAD_GIFTS
                 and o['kind'] == 'gift' and o['ready']), None)
    if not gift:
        return None
    import copy
    spec = copy.deepcopy(spec)
    name, price = gift['title'], f"{gift['price_cents'] / 100:.2f}"
    amount = ('from $' if len(gift['prices_cents']) > 1 else '$') + price
    spec['variation'] = spec.get('variation', 1) + 1
    spec.update(intent='buy', destination=gift['product']['url'],
                offers=[{'id': gift['id'], 'quantity': 1, 'unit_price': price}])
    opening = spec['scenes'][0]['headline']
    spec['scenes'][-1]['text'] = f'{name}, {amount}.'
    spec['captions'] = {
        'instagram': f'Personalized dog gifts for their person. {opening} {name}, {amount}. Explore the gift: {{link}} #PersonalizedDogGifts #GiftsFromTheDog',
        'facebook': f'{opening} A gift from the dog to its person. {name}, {amount}. Gift details: {{link}}',
        'tiktok': f'Personalized dog gifts. {opening} {name}, {amount}. Gift details: {{link}} #GiftsFromTheDog',
        'pinterest': [f'Personalized dog gifts: {name}\nA gift from the dog to its person. {amount}. {{link}}',
                      f'A gift from the dog\n{name}, {amount}. Shown with an example dog. {{link}}']}
    spec['mechanism'] += ' Conversion hypothesis: a verified single-gift price and tracked product link improve qualified visits. No discount or delivery deadline is claimed.'
    return spec
