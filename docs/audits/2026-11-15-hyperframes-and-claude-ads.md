# HyperFrames and Claude Ads: what each adds to the engine (15 Nov 2026)

Asked by Krish on 15 Nov 2026: "Improve Heartside's ability to produce effective creative and evaluate advertising
performance without increasing operational complexity", by evaluating
[HyperFrames](https://github.com/heygen-com/hyperframes) (at `490199c`) and
[Claude Ads](https://github.com/AgriciDaniel/claude-ads) (at `fc3908e`), integrating "only functionality that adds
measurable value beyond the existing system", and testing one creative workflow and one advertising analysis on
authorised data or fixtures. No live campaign, spend, publication or deployment was touched. Both repositories were
read without running their code; HyperFrames' published npm package was run, pinned, for the creative test.

**North Star.** Neither tool moves the number directly (organic net sales, trailing 4 weeks: $0, U5). The audit
protects it: it keeps paid visits out of the organic number and says which boost, if any, bought buying intent. The
template adds a format the engine can test. The work that moves the number this week is still the alibi family and
Instagram's path to the product (`docs/audits/2026-11-15-interest-vs-paid.md`).

## The calls

| | Verdict | Why |
|---|---|---|
| **HyperFrames** | **Integrated narrowly**: one motion template family (`factory/hf.py`, `factory/hyperframes/`), held to every existing gate | Browser layout and easing make text-led motion (a gift line arriving word by word, kinetic type) a short HTML file. The test render passed every gate after one fix the gate itself caught, kept the product's pixels exactly, and reproduced byte for byte |
| **Claude Ads** | **Not installed.** Its scoring method is re-implemented as deterministic code (`engine/ad_audit.py`) | Its Meta audit is 72 checks a model marks by judgement: no code reads the data, no benchmarks are bundled, nothing covers boosted or organic posts, and its optimise and launch skills contemplate applying changes once approved, which only prose stops. The method (pass, fail, unknown, not applicable; severity weights; evidence coverage) is the part worth having |

## What was built

```
Creative                                        Advertising
factory/specs-style JSON (line id, render)       boost records (engine/social.py, read by Codex in Ads Manager)
  -> lock.py check (bank, breeds, copy, sha)       + optional traffic file (Shopify sessions by channel, aggregates)
  -> factory/hf.py                                 -> engine/ad_audit.py: 10 checks, each bound to a ruling
       HyperFrames 0.8.225, pinned, no telemetry        -> score: health over known weight, coverage tiers
       PNG frames -> corpus export preset               -> diagnostics against Heartside's own other boosts
       layout manifest + end frame                      -> proposals for Krish's Yes (never acted on)
  -> codex/check_picture.py + lock.py media       growth.py ads audit; ads_audit.json in the Sunday report
  -> product pixel check against the store file
```

## Test 1: the creative workflow (the note template)

Spec `factory/hyperframes/example-note.json`: approved gift line `F06.fr6` ("You're slow at the door, but I'd wait
forever. Mostly for snacks.", tagged for any breed), the golden portrait render from the live store (SHA-256
matched `factory/bank/renders.json`), on a 9.1 s 1080x1920 reel.

| Check | Result |
|---|---|
| `lock.py check` (bank, approval hash, breed, copy rules, render bytes, profile) | pass |
| `codex/check_picture.py` (size, duration, export preset, fixed label box in the critical box, product ending held 3 to 4 s) | pass |
| `lock.py media` (sound, length, loudness -16.6 LUFS, export, layout manifest, product on screen for the last 3 s) | pass. Its first run held the render for an empty first frame; fixed by putting the line's first three words on screen from frame one |
| Product pixels, first product frame, before encoding, against the store file scaled the factory's way | identical (PSNR infinite, mean bias 0) |
| Product pixels after encoding | 38.47 dB; the existing pipeline on the same image, 38.53 dB |
| Reproducibility | two renders of the same spec gave the same MP4, byte for byte |
| Render and encode time | about 50 s and 6 s for 273 frames, 4-core container |
| Telemetry | disabled (`hyperframes telemetry status`: "disabled", source `HYPERFRAMES_NO_TELEMETRY`) |

Found and fixed during the test: letting Chrome downscale the store JPEG itself cost 3.3 dB on the product after
encoding (35.24 against 38.53), so `hf.py` now hands Chrome the product pre-scaled; and an empty card on frame one
failed the corpus's open-on-the-story rule.

Creative read, as the floor asks: the template works and the note scene has no dog and no visual payoff, so it
fails `dumb-stopping` as a post on its own. Its place is the gift-message beat inside a dog-led film, or the ending
of one. The test render goes to no review board. Sound in the test is `engine/sound.py`'s placeholder score; a post
takes the locked mix from the library.

## Test 2: the advertising analysis (the boost audit)

**Fixtures** (`tests/test_ad_audit.py`, synthetic, 10 tests pass). Six rule breaches a boost record can show, seeded
one at a time: over $20 a day, TikTok before a Meta winner, an engagement objective, an untagged home-page link,
a Meta boost running with paid visits counted as organic, and 100 paid visits with no cart. The audit caught 6 of 6,
each with a proposal; `boost_verdict`, the engine's only boost judgement before, names 1 of the 6.

**Authorised data** (the repository's own record: the F10 pilot in `docs/boost/2026-11-05-sandbox.md` and
`CHANGES.md`, and the 45-day Shopify session aggregates in `docs/audits/2026-11-15-interest-vs-paid.md`; inputs kept
in `local/ads/`, never committed):

```
Boost audit: 1 boost(s); evidence coverage 88.9% (normal); health 79.2; 1 fail, 1 unknown, 5 pass
  PASS    HS-B01 Approved before money moved: "We need to get the first paid test live ASAP."
  PASS    HS-B03 On Meta until Meta has a winner
  PASS    HS-B04 Landing page views objective
  PASS    HS-B05 Paid-tagged link to a product page: /products/your-dogs-illustrated-mug
  UNKNOWN HS-B09 Bought buying intent, not reach: no reading from Ads Manager yet
  PASS    HS-A01 facebook 6 to 7 Nov: 85 sessions (42.5 a day against 0.35), landing the mug page; boost on record
  FAIL    HS-A01 facebook 11 to 13 Nov: 379 sessions (126.3 a day against 0.35), 0 cart adds, landing /; no boost on record
```

It reproduces, from the record alone and in milliseconds, the reconciliation finding the 15 Nov audit wrote by
hand: the 11 to 13 Nov Facebook burst stays "paid or not unknown" until Codex reads Ads Manager.

## Not integrated, and why

- **HyperFrames' Claude Code plugin and skills.** Every skill asks for a usage beacon first, `media-use` steers to
  HeyGen sign-in and credits, and two are paid. The engine's own floor, cards and gates already direct the work.
- **HyperFrames' cloud, Lambda and Cloud Run renders, and its Studio app.** Paid or keyed; local renders suffice.
- **Its registry blocks.** Read for patterns (`notes-reveal`, `per-word-rise`); none copied, since their default
  copy is HyperFrames marketing and the house look is set by the corpus profile.
- **Replacing `factory/build.py` or `engine/media.py`.** They are faster for what they do and already locked.
- **Claude Ads' skills, agents, CLI, PDF reports and landing-page scripts.** Prose-gated writes, Playwright,
  WeasyPrint and image-generation keys for no gain over `growth.py` and the review board.
- **Its Meta export mapping.** It has no impressions, reach or clicks, so it cannot read a boost.
- **Channel performance analysis.** Claude Ads has nothing for organic posts or for paid against organic;
  `factory/loop.py`, `engine/insights.py` and the Sunday report's "What worked" already do this.

## Dependencies added

- Node packages, pinned in `factory/hyperframes/package-lock.json`: `hyperframes@0.8.225` (Apache 2.0) and
  `gsap@3.15.0` (GSAP standard licence, no charge), about 145 MB, installed with `npm ci --ignore-scripts`, never
  committed. Chrome for Testing 152 (about 260 MB) downloads once into `local/hyperframes/.home`.
- Python: none. `engine/ad_audit.py` uses the standard library.
- System: Node 22 or later and FFmpeg, already on every build machine here.

## Running costs

| Item | Cost |
|---|---|
| Licences and APIs | $0. No HeyGen, cloud render or generation call is made |
| A 9 s HyperFrames reel | About a minute of CPU on a 4-core container, inside the session or card that builds it |
| Disk | About 405 MB once per machine (Node modules and Chrome), plus about 270 MB of PNG frames per build in `local/` |
| The boost audit | $0 and milliseconds; it runs in the Sunday report job on GitHub Actions |
| Reading Ads Manager | Codex legwork in Krish's browser, already in the plan (`docs/PAID-BOOSTS.md`) |

## Revisit triggers

- Remove `factory/hf.py` and `factory/hyperframes/` if no note-family post reaches 9 at tier 2 within two weeks
  of the first card that uses it (31 Dec at the latest): the template must earn its place by a post.
- Move the HyperFrames pin only to a release at least two weeks old, re-running the test above.
- The audit's burst rule (5 times the channel's other days and at least 10 sessions a day) is a test assumption;
  change it once two boosts have been read in Ads Manager.
