# AI production contract

Authoring and unattended production are different execution contexts. Codex or
Cowork can use the connected tools in that session. A GitHub Actions runner does
not inherit those connectors, private social logins or Vercel environment values.
Never copy a credential out of Control Centre to bridge the two.

The working unattended path makes no paid provider calls: it reuses provenance
checked product photos and a fictional AI scene, applies native motion/layouts,
synthesizes an original quiet score and runs pinned Kokoro neural narration locally. Fresh concepts, alternate licensed voices and motion
can be authored with connected tools, then imported once and reused. Do not call
this a live paid multi-provider orchestrator.

| Need | Authoring route | Product constraint |
|---|---|---|
| Research and scripts | Codex/ChatGPT, current public sources, verified product canon | No fabricated demand, reactions or sales |
| Fictional scene | Native image generation; Higgsfield image tools after model/quote discovery | Dogs and rooms only; real products composited afterward |
| Reusable motion | Higgsfield generation/status tools with current schema and quote | No generated product, fake customer or testimonial |
| Zero-cost neural voice | Local Kokoro-82M through the pinned ONNX runtime | Synthetic stock narrator, checked script, human review; see VOICE-LICENSES.md |
| Premium voice, music, sound | ElevenLabs speech/creative tools with discovered voice and current quote | Licensed voice, exact checked transcript, explicit synthetic provenance |
| Authorized founder film | HeyGen after identity/consent and quote checks | A real authorized speaker; never a fake buyer |
| Exact final production | Pillow and FFmpeg in this repository | Approved product pixels, readable typography, safe zones and checksums |

The native authoring image generator produced `assets/fictional/biscuit-entryway.png`.
Its companion JSON records source identity, disclosure and the unknown monetary
charge. It is a draft brand asset requiring human review. No prepaid-credit or
paid AI API request was submitted to Higgsfield, ElevenLabs or HeyGen.

## Reserve before a charged external request

Use a local request file with exactly these fields:

```json
{
  "provider": "elevenlabs",
  "capability": "voice",
  "brief": "Campaign C90 H02: approved fictional Buddy narration, exact checked script only",
  "source_sha": "5618a99829a0c9ef1291b73c20cda3d837c262de",
  "maximum_usd": "0.00",
  "quote_source": "Current connected-provider estimate; replace with actual evidence",
  "quote_observed_at": "2026-10-17T10:00:00+00:00"
}
```

This is a schema illustration, not a current zero-cost quote. Read the current
model, voice, rights, price and currency from the provider. Credits alone do not
establish a USD cost. If a quote cannot establish the maximum USD charge, do not
submit a paid job. The default monthly budget is zero. Only a separately
authorized budget may be passed as `--monthly-budget`.

```sh
python3 growth.py provider reserve local/requests/voice.json --monthly-budget 0
python3 growth.py provider status
```

### Prepaid credits inside an approved allocation

Ruling (Krish, 2026-10-22): generation within prepaid credits, inside a weekly
allocation he approved, counts as authorized; publication, ad spend, top-ups
and plan changes still need their own approval. Such a request adds two fields
and keeps `maximum_usd` at `"0"`, because it spends no new money:

```json
{
  "provider": "higgsfield",
  "capability": "image",
  "brief": "Before the door opens: a dog waiting at a front door, dog and room only",
  "source_sha": "<synced full product SHA>",
  "maximum_usd": "0",
  "quote_source": "Higgsfield transactions: GPT Image 2.5 Flare at 2.75 credits",
  "quote_observed_at": "2026-10-22T13:00:00+00:00",
  "prepaid_credits": "2.75",
  "allocation": "weekly-2026-10-22 approved by Krish"
}
```

```sh
python3 growth.py provider reserve local/requests/still.json --credit-allowance 110
```

`--credit-allowance` is the credits the allocation approved for that provider.
Every reservation under the same allocation counts against it, using actual
credits once a receipt records them. A prepaid receipt adds `actual_credits`.
A request with any `maximum_usd` above zero is new money and goes through the
USD budget as before; the prepaid path never widens it.

Reservations serialize in SQLite and include all providers in the same monthly
budget. Stable identity uses month, provider, capability, brief and source SHA;
refreshing a quote cannot silently create a second request. Put the creative ID
and variation in the brief when a genuinely separate asset is needed.

The commands do not call an API. In an authorized connected authoring session:
mark the reservation `submitted` once, submit the discovered tool once, then
track its returned job ID through supported status tools. A lost submission
response becomes `unknown`; never repeat it to get a new display or retry.
`unknown` can become confirmed `completed` or `failed`, never `submitted` again.
Only cancel a reservation before submission. Failures and completions need a
receipt with `job_id`, `actual_usd` and offset `observed_at`. Record actual cost
honestly even when it exceeds the quote; it blocks subsequent over-budget work.

```sh
python3 growth.py provider transition REQUEST_ID submitted
python3 growth.py provider transition REQUEST_ID completed --receipt local/requests/receipt.json
python3 growth.py provider import REQUEST_ID local/incoming/voice.mp3 narration local/requests/provenance.json
```

Replace placeholders with real IDs. The provenance file has `description`,
`rights`, `disclosure`, `transcript`. Import creates a checksum-bound record under
`local/provider-assets/` in `needs_human_review` state. It never approves media.
An operator reviewing a narration sets its record to `approved`; the production
spec then names that JSON record as `narration`. The renderer checks the source
SHA, transcript, file checksum and duration, ducks the score and rejects speech
that would be cut off. Changing that record creates a different creative revision.

AI imports cannot supply roles such as `mug_dog`, product art or customer proof.
Generation failures leave the deterministic production path usable. Reuse
approved assets before commissioning more. Paid submission retries are zero;
read-only source requests have bounded timeouts and scheduled retry opportunities.
