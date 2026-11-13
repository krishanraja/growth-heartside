"""heartside's claims rules (growth.claim_problems), read against what copy really says (adversarial review, 13 Nov
2026). heartside's docs/SELLING.md wins on what may be claimed: its promises must pass, its forbidden claims must not."""
import glob
import json
import os
import re
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, ROOT)
import growth  # noqa: E402
from engine import media  # noqa: E402

EN_DASH, NB_HYPHEN, LQ, RQ = chr(0x2013), chr(0x2011), chr(0x201c), chr(0x201d)

# heartside docs/SELLING.md (10 Nov 2026), its copy-like lines: the offer, the bundle, "Promises we can make", the
# angles and the example notes. Each must pass every claims rule.
CANON = [
    "Heartside paints your dog from one photo onto a mug, a blanket or a portrait, as a gift from the dog to the person it loves. A short note in the dog's own voice comes in the box and as a free digital card. Free US shipping. Order by December 4 for Christmas.",
    "Your dog loves you too.",
    "This year, the dog's buying.",
    "Bundle: two gifts save 15%, and three or more save 20%. It applies automatically, to gifts only.",
    "Artist's touch: an optional add-on. Our artist also paints the dog's toy or collar from the buyer's photos. It adds about 5 days, and its price is on each product page.",
    "Printed Christmas card from the dog: $12, offered with each gift until 11:59 pm Eastern on December 3, 2026.",
    "Every gift is artwork only. No words are printed on any gift. The note travels in the box, on the packing slip, and as the free digital card.",
    "Not on sale: the ornament (on hold), the pillow (a conditional pilot) and the book (planned for 2027).",
    "Free standard shipping on every US order, to US addresses only.",
    "Timing: printing usually takes 2 to 5 business days, then delivery takes 3 to 7. These are typical times, not guarantees.",
    "Christmas: order by December 4 for delivery by Christmas to a US address. At the slowest times, an order placed on December 4 arrives by December 22.",
    "Something wrong: if a gift arrives misprinted, damaged or wrong, tell us within 30 days of delivery with a photo. We refund in full, shipping included, or remake it free. Nothing needs to be sent back.",
    "Cancellation: a full refund until the order goes to print. Personalized pieces can't be returned for a change of mind after printing.",
    "Tracking by email: each parcel's tracking goes out when it ships. Since 10 November, every Printful shipment marks the Shopify order fulfilled and sends Shopify's shipping email with tracking.",
    "Their own dog everywhere: every order email shows the buyer's own painting, not a stock dog. The order status page adds \"Your painting\" once the order-painting app is installed.",
    "Help from a real person: the help chat in the corner of every page answers questions at once. Anyone can ask for a person, and someone from the team replies by email within 6 hours.",
    "It sounds like their dog. The note is written from the owner's own answers and the breed's personality, so a Border Collie and a Poodle don't sound alike.",
    "Roast. A tone where the dog teases the person it loves, with affection: who throws the ball badly, who steals the couch. It is shareable and funny, and it is never cruel.",
    "The gift from the dog. People already sign cards \"from the dog\", and Heartside makes that real for partners, parents, best friends and dog moms and dads.",
    "Fast and easy on a phone. One photo, a few taps, and the painting is ready in about a minute. You see it before you pay.",
    "A person checks every order. The AI never has the last word: a human reviews each design before it prints.",
    "Christmas is sorted if they order by December 4, with free shipping.",
    "Printed and shipped by Printful.",
    "I hear your car long before anyone else.",
    "I took your side of the bed to keep it warm.",
    "Our walks are the best part of my day.",
    "I'm your shadow, and I like it that way.",
]

# True lines the rules must keep passing: the canon said other ways, word-free lines and dog jokes.
TRUE = [
    'Order by Dec 4 for Christmas. Link in bio.',
    'Order by December 4 and it arrives under the tree by Christmas.',
    'For delivery by Christmas, order by December 4.',
    'Arrives by Christmas if you order by December 4.',
    'An order placed on December 4 arrives by December 22 at the latest.',
    'Santa arrives on Christmas Eve. I have been at the window since Tuesday.',
    'Two gifts save 15%, three or more save 20%.',
    '15% off two gifts, 20% off three or more.',
    'Bundle two gifts and save 15%. Bundle three or more and save 20%.',
    'Bundle and save: 15% on two gifts, 20% on three or more.',
    'Save 15% on any two gifts.',
    'Three or more gifts? Save 20%.',
    'Two gifts? 15% off, automatically.',
    'Add a second gift and save 15%.',
    'The note from your dog comes in the box.',
    'The note printed on the packing slip comes in the box.',
    'The note comes in the box, signed with a paw.',
    'In the box: a short note from the dog.',
    'No words on the mug, just your dog.',
    'Every gift is artwork only, with no words printed on it.',
    'Print, mug or blanket, there are no words on them.',
    'Your mug says nothing. Your dog says everything.',
    'I put my face on your mug so you think of me at work.',
    "Our artist also paints the dog's toy or collar from your photos.",
    "Your Dog's Illustrated Mug is painted all the way around.",
    'The card goes on sale December 1.',
    "The ornament isn't on sale yet.",
    'Black Friday? Your dog already picked the gift.',
    'Add a printed Christmas card from the dog for $12 until December 3.',
    'Free standard shipping, US addresses only.',
]

FORBIDDEN = {
    'words on a gift': [
        'A short note from the dog goes on it too.',
        "Your dog's note, printed right on the mug.",
        'The note is printed on the mug.',
        "We print your dog's message on the portrait.",
        'The mug reads ' + LQ + 'Love, Kuku' + RQ + ' under the painting.',
        "Each blanket is embroidered with your dog's name.",
        'A custom mug featuring a quote from your dog.',
        'Her mug: ' + LQ + 'I hear your car first.' + RQ,
        'On her mug: ' + LQ + 'I hear your car first.' + RQ,
        'On the coffee mug: ' + LQ + 'I hear your car first.' + RQ,
        "On the mug: 'I hear your car first.'",
        "Personalized mug with your dog's name on it.",
        'Printed with a little note from your dog.',
        'A mug with a love note from the dog.',
        'Each mug is printed with a sweet message from your dog.',
        'Words from your dog, printed on the blanket.',
        'A mug with a note on it, plus a card in the box.',
        "The print has a caption in your dog's voice.",
        "Your dog's name and a short note go on the front of the mug.",
        "The portrait comes with your dog's words across the bottom.",
        "A blanket covered in your dog's words.",
        "Your dog's message, right there on the blanket.",
        "Text on the mug: your dog's line, in their voice.",
        'A mug that says "I hear your car first." The note also comes in the box.',
        'On the mug: "I hear your car first." A copy comes in the box too.',
        'The portrait carries a short note from the dog, and the same note comes in the box.',
        "Mug with your dog's note printed on it, plus the digital card.",
    ],
    'promises a delivery date': [
        'Christmas delivery guaranteed.',
        'Order by Dec 4. Christmas delivery is guaranteed.',
        'Order by December 10 for Christmas.',
        'Last order date for Christmas: December 18.',
        "Order by December 15 and it's under the tree in time.",
        'Ships in 24 hours.',
        'Free 2-day shipping on every gift.',
        'Arrives in 3 days.',
        'Delivered before the 25th.',
        'Gets there before Christmas.',
        'Delivered to your door by Christmas Eve.',
        'Order today, delivered tomorrow.',
        'Order by December 4, guaranteed to arrive by December 15.',
        "Even if you didn't order by December 4, it still arrives by Christmas.",
        'Order by December 4 or later, and it still arrives by Christmas.',
        'Order by December 4th, guaranteed delivery to Canada by Christmas.',
        'Ordered on December 4 or December 20, it arrives by Christmas.',
        'It arrives by Christmas.',
    ],
    'outside the US': [
        'We ship worldwide.',
        'Free international shipping.',
        'Order by December 4th, guaranteed delivery to Canada by Christmas.',
    ],
    'a percentage other': [
        '20% off sitewide for the next 2 hours.',
        '15% off everything, 3 days only.',
        'Save 15% on your first mug, then 2 more ship free.',
        'Two gifts save 20%.',
        'Three or more gifts save 15%.',
        '50 percent off portraits.',
        'Fifteen percent off a single mug.',
        '25 per cent off two gifts.',
        '25% off two gifts.',
        'Save 20% sitewide.',
        'Black Friday: 30% off two gifts.',
    ],
    'deal or sale': [
        'Save big this Black Friday.',
        'Special offer for Black Friday.',
        'Cyber Week deals are live.',
        'Sitewide sale: two gifts save 15%.',
        'Deal of the day: two gifts save 15%.',
        'Big sale this weekend.',
        'Buy one, get one free.',
        'BOGO on every mug.',
        'Half off the blanket.',
        'Price drop on the portrait.',
        'A free gift with every order.',
        'Limited-time offer: two gifts save 15%.',
        'Two gifts save 15% through Cyber Monday only.',
    ],
    'handmade': [
        "Hand-drawn from your dog's photo.",
        'Hand-illustrated portraits of your dog.',
        "Hand-sketched from your dog's photo.",
        'Every portrait is painted by real artists, one dog at a time.',
        'Each portrait is painted by a human artist.',
        'Lovingly hand-finished in our studio.',
        'Artisan-made dog mugs.',
        'Every brushstroke on the canvas is by our illustrators.',
        'A hand' + EN_DASH + 'painted portrait of your dog.',
        'A hand' + NB_HYPHEN + 'painted portrait of your dog.',
    ],
    'physical quality': [
        'Premium-quality ceramic that lasts.',
        'Archival inks on fine-art paper.',
        'The softest sherpa blanket you will ever own.',
        'Made to last for decades.',
        'Vibrant colors that stay bright wash after wash.',
        'Dishwasher-friendly and chip-resistant.',
        'A luxury sherpa blanket for the couch.',
        'A gallery-worthy portrait of your dog.',
        'Thick, heavyweight ceramic you can feel.',
        "Machine washable and it won't pill.",
        'Superior quality you can feel.',
        'A portrait to treasure for generations.',
        "It won't fade, ever.",
        'Scratch-resistant print.',
        'A gallery' + NB_HYPHEN + 'quality portrait.',
    ],
}


class ClaimsTests(unittest.TestCase):
    def test_heartside_canon_passes_every_claims_rule(self):
        for line in CANON:
            self.assertEqual(growth.claim_problems(line), [], line)

    def test_true_lines_pass(self):
        for line in TRUE:
            self.assertEqual(growth.claim_problems(line), [], line)

    def test_each_forbidden_claim_is_refused_by_its_rule(self):
        for rule, lines in FORBIDDEN.items():
            for line in lines:
                self.assertTrue(any(rule in p for p in growth.claim_problems(line)), (rule, line))

    def test_the_whole_pack_gate_refuses_them_too(self):
        cid = 'IG_EMO_REEL_C01_H03_V1_20261019'
        pack = {'pack_date': '2026-10-19', 'kind': 'daily', 'venture': 'heartside', 'heartside_sha': '1028556df9',
                'headline': 'Monday pack'}
        for rule, lines in FORBIDDEN.items():
            for line in lines[:3]:
                errors = growth.check_pack({**pack, 'items': [{'platform': 'instagram', 'creative_id': cid, 'text': line}]},
                                           [12.0, 29.0, 45.0, 59.0, 119.0, 129.0])
                self.assertTrue(any(rule in e for e in errors), (rule, line))

    def test_an_invented_rating_or_customer_count_is_refused(self):
        for line in ('Rated 4.9 stars by dog moms.', 'Over 500 dog parents have ordered.'):
            self.assertTrue(any('proof' in p for p in growth.problems({'platform': 'instagram', 'text': line})), line)


# ---------------------------------------------------------------------------------------------------------------
# Round 2 (fresh reverifier, 13 Nov 2026), the lead's rulings: the lines HEAD passed that round 1 refused must pass
# again, and the promises and deals the reverifier found passing must refuse. heartside's SELLING.md still wins.
# ---------------------------------------------------------------------------------------------------------------
# docs/GEO-AEO.md, the proof points: the canon line about the note, pinned word for word.
GEO_NOTE_LINE = ('every gift is artwork only, with no words printed on it; the short note from the dog, signed "Love, '
                 '[dog]" with a paw, comes in the box and on a free digital card (heartside, Ruling, Krish, 2026-10-31);')

# heartside docs/SELLING.md, "Promises we can make", word for word (10 Nov 2026).
SELLING_PROMISES = [
    'Free standard shipping on every US order, to US addresses only.',
    'Timing: printing usually takes 2 to 5 business days, then delivery takes 3 to 7. These are typical times, not guarantees.',
    'Christmas: order by December 4 for delivery by Christmas to a US address. At the slowest times, an order placed on December 4 arrives by December 22.',
    'Something wrong: if a gift arrives misprinted, damaged or wrong, tell us within 30 days of delivery with a photo. We refund in full, shipping included, or remake it free. Nothing needs to be sent back.',
    "Cancellation: a full refund until the order goes to print. Personalized pieces can't be returned for a change of mind after printing.",
    "Tracking by email: each parcel's tracking goes out when it ships. Since 10 November, every Printful shipment marks the Shopify order fulfilled and sends Shopify's shipping email with tracking.",
    "Their own dog everywhere: every order email shows the buyer's own painting, not a stock dog.",
    'Help from a real person: the help chat in the corner of every page answers questions at once. Anyone can ask for a person, and someone from the team replies by email within 6 hours.',
    'Bundle: two gifts save 15%, and three or more save 20%. It applies automatically, to gifts only.',
    'Order by December 4 for Christmas.',
]

MUST_PASS = {
    # 1. Words on a gift: the note's own signature in a box sentence (a), a figurative "says" (b), an art line and a
    # dog's name "on it" (c), and FAQ questions (d).
    'words on a gift': [
        GEO_NOTE_LINE,
        'The note from your dog comes in the box, signed "Love, Kuku" with a paw.',
        'A short note from the dog, signed "Love, Kuku", comes in the box.',
        "The note comes in the box, signed with your dog's name and a paw.",
        'Every note is signed "Love, [dog]" and comes in the box.',
        'The mug says it all.',
        'The portrait says more than words.',
        'Every line on the portrait is painted from your photo.',
        "The fine lines on the mug follow your dog's ears.",
        'The blanket? My name is on it now.',
        'Is there text on the mug? No, the note comes in the box.',
        "Does the portrait have my dog's name on it? No. The name goes on the note in the box.",
        "Is my dog's name printed on the blanket? No, it goes on the card in the box.",
    ],
    # 2. Delivery: the canon Christmas line inside one sentence.
    'promises a delivery date': [
        'Order by December 4 and it arrives under the tree by Christmas.',
        'Arrives by Christmas if you order by December 4.',
        'Order by December 4 to have it in time for Christmas.',
        'Order by December 4 and we deliver by Christmas.',
        'Read 10 Nov at about 17:10 UTC, superseded by the 20:10 UTC section below.',
    ],
    # 3. Deal: the event and the cue never across a full stop, "?" or "!"; "only" is never a cue.
    'deal or sale': [
        'Black Friday. He got the only thing he wanted.',
        'Black Friday haul. Everything was free. Most of it was yours.',
        'Black Friday. The only thing I want is you.',
        'Cyber Monday. I save my best naps for you.',
        'Black Friday crowds? I only go to the park.',
        'Your dog loves you. Only you. Black Friday is just a Friday.',
    ],
    # 4. Percentages: none without a sale in the sentence; in a sale, the two tiers in any common order.
    'a percentage other': [
        'A dog meteorologist calls the winter: a front of lap-sitting moving in, 100 percent chance through March.',
        "I'm 100% sure it was the cat.",
        '99% of my job is watching the door.',
        '15% off two gifts, 20% off three.',
        'Two gifts: 15% off. Three or more: 20% off.',
        '15% off when you buy two gifts.',
        'Bundle two gifts for 15% off.',
        'Two gifts save 15% and three save 20%.',
        'Three gifts save 20%, two save 15%.',
        'Bundles save 15 to 20%.',
        'Save 15% on two gifts, or save 20% when you add a third.',
        'Two gifts save fifteen percent.',
    ],
    # 5. The broader quality and handmade words, with no product in the sentence: the dog talking.
    'physical quality': [
        'The softest spot on the couch is mine.',
        'I take the softest pillow. Every time.',
        'A luxury I allow myself: your side of the bed.',
        'I will love you for generations.',
        'Your sweaters are heavy-duty dog beds now.',
    ],
    'handmade': [
        'I am the real artist in this house. Look at the couch.',
        'My breakfast is artisanal kibble, apparently.',
    ],
}

MUST_REFUSE = {
    'words on a gift': [
        'On the mug: "I hear your car first." The note comes in the box.',  # the closing quote still ends its sentence
        'The mug says "I hear your car first."',
        'The mug says, "I hear your car first."',
        'A mug that says it all.',
        'Each mug is signed "Love, Kuku" and the note comes in the box.',  # the gift is the one signed
        'The portrait carries a short note from the dog, and the same note comes in the box.',
        "Your dog's name and a short note go on the front of the mug, and the note comes in the box.",
        "Your dog's name on the mug.",
        'A short note goes on it.',
    ],
    'promises a delivery date': [
        # An anchor in the next sentence never excuses a promise (the lead's ruling; HEAD refused these too).
        'Want it under the tree by Christmas? Order by December 4.',
        'Order by December 4. It arrives by Christmas.',
        'Ordered on December 4? It arrives by December 22.',
        # The reverifier's lines: later orders promised Christmas, or a date before canon.
        'Order by December 4 for Christmas. Order later and it arrives by Christmas.',
        'Order by December 4. Orders after that arrive by Christmas too.',
        'Order by December 4. Order next week and it arrives by Christmas.',
        'Order by December 4. Late orders arrive by Christmas too.',
        'Order by December 4. Any order arrives by Christmas.',
        'Order by December 4. Every order arrives by Christmas, no matter when.',
        'Order by December 4 at noon. It arrives by Christmas, at the latest by the 20th.',
        # The same excusal inside one sentence.
        'Order by December 4, and orders after that arrive by Christmas too.',
        'Order by December 4 and any order arrives by Christmas.',
        'Order by December 4; late orders arrive by Christmas too.',
        'Order by December 4 and it arrives by Christmas, wherever you live.',
        'Order by December 4 for Christmas, even the blanket ordered next week.',
        # Open at HEAD too.
        'We deliver by Christmas.',
        'In time for Christmas.',
        'Your gift will make it in time for Christmas.',
        'Under the tree by the 23rd.',
    ],
    'deal or sale': [
        'Black Friday: two gifts save 15%.',
        'Cyber Monday deals on every mug.',
        'Black Friday, save on the blanket.',
        'A Cyber Monday discount on portraits.',
    ],
    'a percentage other': [
        'Save 15% on any two gifts this weekend only.',
        '15% off two gifts, today only.',
        '15% off two gifts for the next 2 hours.',
        'Two gifts save 20% and three save 15%.',
        'Up to 20% off.',
        'Save 15 to 20% on everything.',
        'Two or three gifts save 15%.',
        'Save 15% on two gifts until December 3.',
    ],
    'physical quality': [
        'The softest blanket on the couch.',
        'A luxurious sherpa for the couch.',
        'A mug your family will love for generations.',
        'A heavy-duty ceramic mug.',
        'Durable enough for the dog.',             # the core words need no product
        'Dishwasher-safe, of course.',
        'Gallery-quality, every time.',
        'Long-lasting color.',
        'Fade-resistant ink.',
    ],
    'handmade': [
        'A portrait by a real artist.',
        'Artisanal mugs from your dog.',
        'Our illustrators paint every portrait.',
        'Handmade, every time.',                   # the core words need no product
        'Hand' + EN_DASH + 'painted from your photo.',
        'Hand' + NB_HYPHEN + 'painted from your photo.',
        'Painted by hand from your photo.',
    ],
}

# Invented time limits are the scarcity rule (FAKE_PROOF), read on every line through problems() and the film gate.
INVENTED_LIMITS = [
    'Save 15% on two gifts. Black Friday only.',
    'Two gifts save 15%. Today only.',
    'This weekend only: two gifts save 15%.',
    'Two gifts save 15% for the next 2 hours.',
    'A limited-time gift from your dog.',
]


def _lock():
    import importlib.util
    spec = importlib.util.spec_from_file_location('factory_lock_claims', os.path.join(ROOT, 'factory', 'lock.py'))
    module = importlib.util.module_from_spec(spec)
    argv = sys.argv
    sys.argv = ['lock.py']
    try:
        spec.loader.exec_module(module)
    finally:
        sys.argv = argv
    return module


class RoundTwoTests(unittest.TestCase):
    def test_heartside_promises_pass(self):
        for line in SELLING_PROMISES:
            self.assertEqual(growth.claim_problems(line), [], line)

    def test_the_canon_note_line_is_pinned_from_geo_aeo(self):
        with open(os.path.join(ROOT, 'docs', 'GEO-AEO.md'), encoding='utf-8') as handle:
            self.assertIn(GEO_NOTE_LINE, handle.read())

    def test_must_pass_lines_pass_every_claims_rule(self):
        for rule, lines in MUST_PASS.items():
            for line in lines:
                self.assertEqual(growth.claim_problems(line), [], (rule, line))

    def test_must_refuse_lines_are_refused_by_their_rule(self):
        for rule, lines in MUST_REFUSE.items():
            for line in lines:
                self.assertTrue(any(rule in p for p in growth.claim_problems(line)), (rule, line))

    def test_dog_jokes_pass_the_film_gate(self):
        # lock.copy_problems runs claim_problems on every on-screen line (round 1, finding 14).
        lock = _lock()
        g = lock._growth()
        claims = {p for lines in list(MUST_REFUSE.values()) + list(FORBIDDEN.values()) for line in lines
                  for p in g.claim_problems(line)}
        self.assertEqual(len(claims), 7)  # every claims rule's message, from its refusals
        for rule in ('deal or sale', 'a percentage other', 'physical quality', 'handmade', 'words on a gift'):
            for line in MUST_PASS[rule]:
                self.assertEqual(claims & set(lock.copy_problems(g, line, 'headline')), set(), line)

    def test_invented_time_limits_are_refused(self):
        lock = _lock()
        g = lock._growth()
        for line in INVENTED_LIMITS:
            self.assertTrue(any('urgency' in p for p in growth.problems({'platform': 'instagram', 'text': line})), line)
            self.assertTrue(any('urgency' in p for p in lock.copy_problems(g, line, 'headline')), line)
        for line in ('I will be at the window all weekend.', 'Black Friday. The only thing I want is you.'):
            self.assertFalse(any('urgency' in p for p in growth.problems({'platform': 'instagram', 'text': line})), line)


class ApprovedCopySweepTests(unittest.TestCase):
    """No approved line is refused by the claims rules: campaign scenes and captions, config, the schedule builders,
    the joke bank and Sprint 120's slots (item 7 of the round-2 rulings)."""

    def _strings(self):
        import ast
        import importlib.util
        out = []

        def walk(value, where):
            if isinstance(value, str):
                out.append((where, value))
            elif isinstance(value, dict):
                for key, item in value.items():
                    walk(item, f'{where}.{key}')
            elif isinstance(value, list):
                for n, item in enumerate(value):
                    walk(item, f'{where}[{n}]')

        for path in sorted(glob.glob(os.path.join(ROOT, 'campaigns', '*.json')) + glob.glob(os.path.join(ROOT, 'config', '*.json'))):
            with open(path, encoding='utf-8') as handle:
                walk(json.load(handle), os.path.basename(path))
        for path in sorted(glob.glob(os.path.join(ROOT, 'factory', 'schedule', 'build_*.py'))):
            with open(path, encoding='utf-8') as handle:
                tree = ast.parse(handle.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and ' ' in node.value:
                    out.append((f'{os.path.basename(path)}:{node.lineno}', node.value))
            spec = importlib.util.spec_from_file_location('claims_' + os.path.basename(path)[:-3], path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for pid, (_day, _time, _slug, line, _tags) in getattr(module, 'NEW', {}).items():
                out.append((f'{os.path.basename(path)}:NEW[{pid}]', f'{line}\n\n{module.TAIL} Link in bio.'))
        with open(os.path.join(ROOT, 'factory', 'schedule', 'phone-posts.html'), encoding='utf-8') as handle:
            for m in re.finditer(r'"(?:caption|line|on_screen|hook)":\s*("(?:[^"\\]|\\.)*")', handle.read()):
                out.append(('phone-posts.html', json.loads(m.group(1))))
        with open(os.path.join(ROOT, 'factory', 'bank', 'lines.json'), encoding='utf-8') as handle:
            out += [(row['id'], row['text']) for row in json.load(handle)['lines'] if row.get('status') == 'approved']
        with open(os.path.join(ROOT, 'factory', 'sprints', '2026-11-S120.json'), encoding='utf-8') as handle:
            for slot in json.load(handle)['slots']:
                out += [(f"S120 {slot['id']}.{k}", slot[k]) for k in ('title', 'premise', 'payoff', 'filed_caption', 'post')
                        if isinstance(slot.get(k), str)]
        return out

    def test_no_approved_line_is_refused(self):
        strings = self._strings()
        self.assertGreater(len(strings), 500)
        for where, text in strings:
            # The claims rules, and the invented time limits round 2 added to the scarcity rule. ("The dream-run
            # countdown", an idea-stage slot title, meets the older "countdown" word, as it did at HEAD.)
            problems = growth.claim_problems(text) + re.findall(growth.TIME_LIMIT, text, re.I)
            self.assertEqual(problems, [], where)

    def test_the_forecast_premise_passes(self):
        with open(os.path.join(ROOT, 'factory', 'sprints', '2026-11-S120.json'), encoding='utf-8') as handle:
            slot = next(s for s in json.load(handle)['slots'] if s['id'] == 'S07')
        self.assertIn('100 percent chance', slot['premise'])
        self.assertEqual(growth.claim_problems(slot['premise']), [])


class SceneInFrameTests(unittest.TestCase):
    """Each campaign scene is read with the gift it shows (finding 7): the words sit over a mug or a portrait."""

    def test_every_live_campaign_scene_passes_in_frame(self):
        for path in sorted(glob.glob(os.path.join(ROOT, 'campaigns', '*.json'))):
            with open(path, encoding='utf-8') as handle:
                scenes = json.load(handle)['scenes']
            self.assertEqual(media.scene_problems(scenes), [], path)

    def test_a_note_over_a_gift_is_refused_in_frame(self):
        old = [{'asset': 'portrait_unframed', 'headline': 'With a short note from the dog.',
                'text': "Signed with your dog's name and a paw."},
               {'asset': 'mug_black', 'headline': 'Your dog loves you too.', 'text': 'A short note from the dog goes on it too.'},
               {'asset': 'mug_black', 'headline': 'Your dog loves you too.', 'text': 'A short note from the dog comes in the box.'}]
        problems = media.scene_problems(old)
        self.assertEqual(sorted({p.split(':')[0] for p in problems}), ['scene 1', 'scene 2'])
        self.assertTrue(all('words on a gift' in p for p in problems))
        self.assertEqual(media.scene_problems([{'asset': 'portrait_unframed', 'headline': 'And a short note from the dog.',
                                                'text': "In the box: signed with your dog's name and a paw."}]), [])


if __name__ == '__main__':
    unittest.main()


class RoundThreeTests(unittest.TestCase):
    """Lines the second reverification found wrongly refused or wrongly passed (13 Nov 2026)."""

    MUST_PASS = [
        'A portrait with bold lines and soft color.', 'The mug has clean lines.',
        'Every mug ships with a note signed "Love, Kuku" with a paw, in the box.',
        'Each gift comes with a short note from the dog, signed "Love, Kuku" with a paw, in the box.',
        'Your mug arrives with a note in the box, signed "Love, Kuku" with a paw.',
        'The packing slip carries the note, signed "Love, Kuku" with a paw.',
        'Two ways to save: 15% off two gifts, 20% off three or more.', 'For the two of you: two gifts save 15%.',
        'Two gifts save 15%, every day.', 'Two gifts save 15% and they arrive in 3 to 7 days.',
        'There is still time: order by December 4 for Christmas.', 'Order by December 4 so you are not late.',
        'Order by December 4 for Christmas; after that, no promises.', 'By the 20th nap, I had won.',
        'My softest paw print is on your pillow.', 'Is there text on the mug? No, the note comes in the box.',
    ]
    MUST_REFUSE = [
        "Want your dog's note printed on the mug?", 'Want a mug that says "Love, Kuku"?',
        "Why not put your dog's words on a blanket?", 'Each mug is signed "Love, Kuku" and the note comes in the box.',
        'Order by December 4, and orders after that arrive by Christmas too.',
        'Order by December 4; late orders arrive by Christmas too.', 'Save 15% on any two gifts this weekend only.',
    ]

    def test_true_lines_pass_and_false_ones_refuse(self):
        for line in self.MUST_PASS:
            self.assertEqual(growth.claim_problems(line), [], line)
        for line in self.MUST_REFUSE:
            self.assertTrue(growth.claim_problems(line) or growth.problems(line), line)
