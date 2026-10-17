# Heartside acquisition strategy

Krish asked for an organic growth engine using the AI tools available to
produce delightful material and generate $10,000 in sales in a month.
The 17 October instruction keeps marketing and customer acquisition here;
product, purchase-flow and operations recommendations are in heartside's
[product handoff](https://github.com/krishanraja/heartside/pull/13).

## The acquisition loop

Build around recognition: "That is exactly our dog." A detail from an
ordinary household moment becomes content someone sends, a gift they can
make, and an invitation for another household to make its own. Every tool
should serve that connection.

The product already asks about greetings, shared spaces and routines. Turn
those into recurring formats, initially with licensed examples and later
with permissioned real stories. Do not mine private chat answers or infer
individual habits from the breed corpus.

| Format | Creative mechanism | Proof |
|---|---|---|
| Before the door opens | A familiar greeting makes someone send it to the person their dog waits for. | The same detail on the real gift. |
| The part only you know | A specific answer becomes a precise line and a product reveal. | The real chat and actual product artwork. |
| The gift from the other family member | A creator makes and gives a gift on behalf of their dog. | A real product in a real home, with gift disclosure and an honest reaction if filmed. |

`campaigns/waits-at-the-door.json` is the first working example, using the
approved Biscuit mug images. It is an audience creative, not customer proof.
The next concept can test hearing the car first, using matching approved
product imagery or a product-repo render before the media claims that detail.
Keep text readable muted and give each post one action.

The "Biscuit draws the moment" illustration idea is already in product canon.
It remains a separate product experiment. The initial acquisition system
can work with the approved photo gifts while that experiment is evaluated.

## The target and assumptions

Treat a 30-day launch sprint as the planning scenario. The older target of
cumulative sales by December 10 is different. A delayed launch reduces
selling days against a fixed calendar deadline. $10,000 is a management
target; there is no demonstrated v3 conversion baseline or sales forecast.

Use Shopify net product sales after discounts and reversals, excluding
taxes and shipping. The scenarios use approved launch prices; they are not
claims that the products are active today. Run `growth.py readiness` first.

| Assumed average basket | Orders for $10,000 | Sessions at 1.5% conversion | Sessions at 2.5% |
|---|---:|---:|---:|
| $29 | 345 | 23,000 | 13,800 |
| $48 | 209 | 13,934 | 8,360 |
| $89 | 113 | 7,534 | 4,520 |

The $48 hypothesis is the approved mug plus add-on ornament basket, subject
to verifying the actual bundle. At 2.5% conversion it requires about 279
qualified visits and seven orders daily. If one session arrives per 100
video views, the session target requires roughly 836,000 views; at one per
200 views it doubles. These are sensitivity calculations, not expected
click rates. Distribution needs evidence as well as creative quality.

Measure acquisition economics after physical gifts, affiliate commissions,
AI generation, remakes and relevant operating costs. The canon's estimated
mug contribution of $13.06 becomes about $7.26 after a 20% commission on a
$29 sale, before the other costs. Re-read current product costs and terms
before agreeing a commission or proposing spend. Revenue is not profit.

## Distribution in the first month

Keep Instagram and Facebook primary. Reuse suitable work for TikTok while
measuring actual audience geography. Existing store visits from a country
do not establish where any particular social account reaches viewers.

Prepare individually researched briefs for the approved pool of 20 US
creators during the first week. The former five-new-prospects-per-week pace
leaves little time for conversation, production, delivery and filming in a
30-day sprint. Krish still approves each gift and sends each individual
message. Gift-only seeding does not establish a commitment to post.

Record research, a specific reason for fit, agreement, gift approval,
delivery, publication, footage rights, known visits and orders, and cost.
Distinguish genuine commitments from hopes. Use the actual link or code
when attribution is available; report missing attribution explicitly.

Pinterest assets reuse useful stills with distinct search intent. Produce a
small number of substantive gift-intent pages through product-repo briefs.
Search is a longer-term source of demand; do not allocate invented month-one
orders to it. Consent-based recovery and reminder copy can recover existing
intent once the product session has configured and tested the flows.

## The sharing experiment

The existing card is already available on the choose-gifts screen. Test an
option at the reveal, when recognition is fresh, with a clear choice to
keep the gift private. A recipient's surprise matters. A shared link should
invite a new household to make a gift, with editable suggestions.

Growth owns the hypothesis, invitation copy, creative and reporting. The
product repo owns first-party implementation, privacy choices and the
event contract. Start with a static card and tracked links. A reusable
animated variant can follow; generated video for every visitor would add
cost before referral conversion is established.

Measure share intent, unique referred sessions, completed creations and
orders. A card render or share-dialog tap does not prove a send. A useful
early metric is new qualified visits per completed reveal. Do not assume
the loop is self-sustaining or credit all direct traffic to it.

## Production and tool roles

The daily output should be finished media with native captions, a clear
experiment and a short review. `docs/ENGINE.md` distinguishes implemented
commands from future provider work.

| Capability | Job |
|---|---|
| ChatGPT and Codex | Research, concepts, hooks, structured scripts, implementation and analysis with factual sources. |
| Existing Gemini and n8n | Approved product personalization and existing orchestration. |
| Image generation and Higgsfield | Optional approved fictional Biscuit scenes and backgrounds. |
| Higgsfield or Runway where connected | Reusable dog or room motion, keeping real products outside generative processing. |
| ElevenLabs | A consistent licensed Biscuit voice and restrained sound. |
| Canva and deterministic templates | Brand layouts, covers, carousels, Stories and Pins. |
| FFmpeg | Exact product imagery, typography, captions and final exports. |
| Shopify and platform reporting | Purchases, net sales, actual funnel behavior and attention metrics. |
| HeyGen | Optional authorized founder explanations after the first loop works. |

Access in an interactive session does not establish credentials or budgets
in a scheduled runner. Provider adapters should report capability,
authentication readiness and estimated cost. Paid requests need a configured
budget, idempotency and bounded retries. Reuse approved assets before
generating another one. The current renderer makes no paid provider calls.

## Learning and decisions

Store the concept, hook, buyer, mechanism, source assets, rights, output
revision, publication URL and observed metrics. Use the same concept number
across platforms. Keep actual publication separate from a generated draft.

Read 24-hour and 72-hour attention signals and retain a longer order and
refund view. Judge contribution and purchases first, then sessions, chat
completion, carts and sends per reach. Mark low-volume results inconclusive
and replicate promising mechanisms across separate posts before expanding
them. A single order does not establish a repeatable winner.

A shared Instagram bio link cannot identify which Reel caused a visit.
Preserve known creative IDs on direct links and keep unattributed traffic
explicit. A creator's link or Story sticker can supply more specific
evidence. Account-level sales must not be assigned to the most recent post.

Reconcile the older roast-versus-love-letter experiment with v3's rejection
of the HR builder. Test current recognition stories and gift proof. Do not
bring the retired HR concept back through an older experiment instruction.

One diagnostic checkpoint: after 200 relevant US sessions through a verified
live journey with no purchases, investigate acquisition quality and the
purchase path before increasing production. This is an operating checkpoint,
not a universal conversion benchmark. Product fixes return as briefs to
heartside. Changes to live policies and human fulfillment follow that repo.

## The first thirty days

| Period | Acquisition work | Evidence |
|---|---|---|
| Days 1–3 | Connect aggregate reporting and prepare media while the product session proves launch readiness. | Correct offer snapshot and reporting windows; purchase proof comes from heartside. |
| Days 4–7 | Finish three reusable templates and the approved creator pool's individual briefs. | Playable files, checked copy and actual publication records. |
| Days 8–14 | One master concept daily, native editions and the first sharing test once implemented. | Traffic quality, completed creations, creator progress and purchases. |
| Days 15–21 | Expand mechanisms that repeatedly produce useful visits or purchases. | Results across separate creatives and real acquisition costs. |
| Days 22–30 | Concentrate on the strongest buyer, channel, proof and basket; use verified recovery and permissioned proof. | Net sales and contribution with fulfillment capacity reported by the product session. |

An illustrative allocation is 15 orders in days 1–7, 35 in days 8–14, 60 in
days 15–21 and 100 in the last nine days. At an assumed $48 AOV, 210 orders
produce $10,080. Recalculate remaining requirements from actual sales,
conversion, AOV, creator delivery and selling days. These figures are targets,
not observed performance. Do not use an unconfirmed Christmas cutoff as
urgency for the first month.

The first milestone is one real-product film, one verified tracked purchase
journey, one real order and a report joining only what can be attributed.
The code in this build delivers the film, offer checks and reporting
foundation. The build also delivers local neural narration, fictional AI scene reuse,
native templates, persistent scheduled drafts and conservative evidence-based
replication candidates. Product purchase proof, fresh private-source collection
and authorized paid provider submissions remain explicit operating dependencies.
