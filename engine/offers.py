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


def canonical_offers(texts):
    """Read facts from the gift table, never a second hardcoded price list."""
    for path, text in texts.items():
        match = re.search(r'^## 3\. The gift range.*?(?=^## |\Z)', text or '', re.M | re.S)
        if not match:
            continue
        result = []
        for line in match.group(0).splitlines():
            cells = [c.strip() for c in line.split('|')]
            if len(cells) < 5 or not cells[1].startswith('**'):
                continue
            name = cells[1].replace('**', '')
            prices = MONEY.findall(cells[3])
            if prices:
                result.append({'id': re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-'),
                               'name': name, 'price_cents': cents(prices[0]),
                               'bundle_price_cents': cents(prices[1]) if len(prices) > 1 else None,
                               'source': path + '#3-the-gift-range-launch'})
        return result
    return []


def catalog(state):
    products = state.get('store') or []
    result = []
    for offer in state.get('offers') or []:
        matches = [p for p in products if p['title'].strip().casefold() == offer['name'].casefold()]
        product = matches[0] if len(matches) == 1 else None
        live_prices = ([v['price'] for v in product['variants'] if v.get('available')]
                       if product and 'variants' in product else (product or {}).get('prices', []))
        price_matches = bool(product and offer['price_cents'] in {cents(p) for p in live_prices})
        reason = ('public catalog could not be checked' if state.get('store') is None else
                  'not in the public catalog' if not product else
                  'not available' if not product.get('available') else
                  'public price differs from the canon' if not price_matches else 'available at the approved price')
        result.append({**offer, 'ready': bool(product and product.get('available') and price_matches),
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
        allowed = {offer['price_cents']}
        # A discount requires a second distinct gift and explicit, currently
        # confirmed bundle evidence. A price table alone cannot prove activation.
        if (len(declared) > 1 and state.get('bundle_verified_at') and
                state.get('bundle_verified_at') == state.get('synced_at')):
            allowed.add(offer.get('bundle_price_cents'))
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
        if purchase and offer['name'].casefold() in public_text.casefold() and offer['id'] not in seen:
            errors.append(f'copy names {offer["name"]} without declaring that gift')
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
    """A ready single-mug conversion draft; other gifts await approved photos."""
    if not state or not state.get('homepage_v3') or not fresh_store(state):
        return None
    mug = next((o for o in catalog(state) if o['id'] == 'the-morning-mug' and o['ready']), None)
    if not mug:
        return None
    import copy
    spec = copy.deepcopy(spec)
    name, price = mug['name'], f"{mug['price_cents'] / 100:.2f}"
    spec['variation'] = spec.get('variation', 1) + 1
    spec.update(intent='buy', destination=mug['product']['url'],
                offers=[{'id':mug['id'], 'quantity':1, 'unit_price':price}])
    opening = spec['scenes'][0]['headline']
    spec['scenes'][-1]['text'] = 'Meet ' + name + '.'
    spec['captions'] = {
        'instagram': f'Personalized dog gifts for their person. {opening} {name}, ${price}. Explore the gift: {{link}} #PersonalizedDogGifts #GiftsFromTheDog',
        'facebook': f'{opening} A little gift from the dog to their person. {name}, ${price}. Gift details: {{link}}',
        'tiktok': f'Personalized dog gifts. {opening} {name}, ${price}. Gift details: {{link}} #GiftsFromTheDog',
        'pinterest': [f'Personalized dog gifts: {name}\nA gift from the dog to their person. ${price}. {{link}}',
                      f'A gift from the dog\n{name}, ${price}. Shown with Biscuit, our fictional AI dog. {{link}}']}
    spec['mechanism'] += ' Conversion hypothesis: a verified single-gift price and tracked product link improve qualified visits. No discount or delivery deadline is claimed.'
    return spec
