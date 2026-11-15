# Motion templates rendered by HyperFrames

Ruling (Krish, 2026-11-15): "Evaluate HyperFrames for generating reusable product video templates, animated gift
messaging, dog-personality creative, and campaign variations. Prefer existing shared rendering infrastructure. ...
Integrate only functionality that adds measurable value beyond the existing system." The evaluation and its
measurements are in [`docs/audits/2026-11-15-hyperframes-and-claude-ads.md`](../../docs/audits/2026-11-15-hyperframes-and-claude-ads.md).

[HyperFrames](https://github.com/heygen-com/hyperframes) (Apache 2.0, HeyGen) renders an HTML page, frame by frame,
in headless Chrome. It is used here for one thing the Pillow and FFmpeg factory does not do well: type that moves
with a browser's layout and easing (a gift line arriving word by word, kinetic type). Everything else stays in
`factory/build.py`. A HyperFrames post obeys the same rules and passes the same gates as any other post.

## What is here

| File | What it is |
|---|---|
| `package.json`, `package-lock.json` | HyperFrames `0.8.225` (31 Oct 2026) and GSAP `3.15.0`, pinned exactly. HyperFrames ships about 2.6 releases a day, so the pin moves only by hand, to a release at least two weeks old, with the test below re-run |
| `note/index.html` | The note template: the dog's gift line on a paper note, three words from frame one and the rest rising one by one, a paw, then the real store render held 3.5 s with a slow push-in |
| `example-note.json` | The capability-test spec of 15 Nov. Not a proposed post |
| `../hf.py` | The driver: resolves the words and the render, renders, encodes, checks |

## How a note post is made

```bash
cd factory/hyperframes && npm ci --ignore-scripts && cd ../..
```

```bash
HEARTSIDE_ASSETS=<library> python3 factory/hf.py <spec.json>
```

A spec carries no free text, like every factory spec:

```json
{"id": "N01-golden", "template": "note", "ui_profile": "social-corpus-2026-11-12-v2", "breed": "golden",
 "line": "F06.fr6", "end": {"renders": ["golden-sentimental-portrait.jpg"]}, "music": "<a library audio file>"}
```

`hf.py` then, in order:

1. runs `lock.py check` and refuses a held spec (`--preview` builds one anyway, for judging lines in place);
2. checks the render's SHA-256 against `factory/bank/renders.json` and hands Chrome the product already scaled the
   way `factory/common.py` scales it (Lanczos, lossless), drawn 1:1 on its first frame;
3. renders PNG frames (never HyperFrames' JPEG intermediates) and encodes them with the corpus export preset
   (`engine/creative_ui.py`), with the spec's `music` from the library or, without one, `engine/sound.py`'s local
   score as a placeholder;
4. writes the layout manifest and end frame `factory/build.py` writes, then runs `codex/check_picture.py` and
   `lock.py media`, and measures the product's pixels against the store file.

The result is `local/media/factory/<id>.mp4` and `local/hyperframes/<id>/result.json`. From there it is a post like
any other: `lock.py brief`, an independent reviewer, the tier 2 judge, and Krish's review board only at 9 or above.

## How it is contained

- **No telemetry.** HyperFrames sends usage to PostHog by default. `hf.py` sets `HYPERFRAMES_NO_TELEMETRY=1` and
  `DO_NOT_TRACK=1` and persists `telemetry disable` in its config; `hyperframes telemetry status` reads "disabled".
- **Nothing in your home folder.** `HOME` points at `local/hyperframes/.home`, which holds its config and the
  Chrome it downloads once (Chrome for Testing 152, about 260 MB). Update checks, auto-install and skill installs
  are off. Its Claude Code plugin and skills are not installed: they ask for a usage beacon on every use and steer
  to HeyGen's paid media.
- **Nothing fetched at render time.** GSAP and the fonts are local files copied into each build.
- **Never its cloud.** `hyperframes cloud`, Lambda, Cloud Run, `media-use` generation and the Pro skills are paid
  or keyed and are not used.

## What it costs

No licence or API cost: HyperFrames is Apache 2.0 and GSAP's standard licence is free. On a 4-core cloud container a
9.1 s reel took about 50 s to render and 6 s to encode, against about 145 MB of Node modules and the one-time
Chrome download. It needs Node 22 or later and FFmpeg, which every build machine here already has.
