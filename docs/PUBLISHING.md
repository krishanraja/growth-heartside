# Publishing playbook: how every Heartside asset goes out, channel by channel

This is the checklist a creative must pass before it is posted or boosted, plus the per-channel practice. It adds to `docs/CHANNEL-TASKS.md`, which owns the weekly loop and what to read from each post; this file owns what to build and check before release. It never edits a locked post: a post that fails here goes back to the engine.

- Paid use also follows `docs/PAID-BOOSTS.md`.
- Files follow `docs/BOOST-LIBRARY.md`.
- The quality bar and current scores are in `docs/audits/2026-11-04-creative-audit.md`.

Platform specs move. The numbers below are current as of 4 Nov 2026. Each release, check the platform's own preview, and for ads the Ads Manager safe-zone guardrail.

## 1. The master file (every channel)

| Item | Requirement | Check |
|---|---|---|
| Frame | 1080x1920, 9:16, H.264, 30 fps, AAC audio | `factory/lock.py media` |
| Loudness | -18 to -13 LUFS integrated | `factory/lock.py media` |
| Length | Organic 6 to 60 s, and 15 to 30 s where possible. Paid 15 to 30 s | `factory/audit.py` |
| First second | Motion, and a legible situation on frame 1: no blank interface, no tiny subject, no 2 s still | `factory/audit.py` `dead_open` |
| Ending | The real store render for the same breed and coat, on screen for at least the last 3 s | `factory/lock.py media` and a person |
| Organic text zone | Keep words between y=200 and y=1440. Nothing in the right 130 px, where the interface buttons sit | `factory/audit.py` and a person |
| Paid text zone | Keep words between y=270 and y=1250 (top 14% and bottom 35% clear) and 65 px in from each side | Ads Manager guardrail |
| Cover | 1080x1920. The story must read inside the centre 1080x1440, the 3:4 grid crop. No blank interface frame | A person |
| Sound-off | The joke works muted. Subtitles carry every spoken line | A person |
| AI labelling | Photorealistic AI dogs: switch on TikTok's AI-generated content label, and let Meta's "AI info" label stand | At upload |
| Music | Organic: the licensed Epidemic track. Paid: only music whose licence covers advertising (`docs/PAID-BOOSTS.md` gate 1) | Licence noted in the manifest |

## 2. Captions (every channel)

- Line 1 is the hook. It makes someone think "I'd send this to ___".
- Line 2 is Krish's line, word for word: "Gifts from your dog. Painted lovingly in your style of choice using our next-generation AI artists."
- Then the link (Facebook), or "Link in bio" (Instagram and TikTok).
- Then 2 to 3 specific hashtags (none on Facebook).
- House rules (AGENTS.md rule 5): US spelling, no exclamation marks, no em dashes or spaced hyphens used as dashes, no swearing or swear acronyms, nothing invented.
- `growth.py check` enforces what code can.
- A standalone joke post gets no "tag a mate" and no product slide (`docs/CHANNEL-TASKS.md`). Gift-led posts may ask for a tag.

## 3. Channel by channel

### Instagram (Reels and carousels)

- **Reels.** Upload the master, then set the cover from the cover file, not from a frame. Preview the grid tile: it crops to 3:4. Use "Share to Feed".
- **Carousels.** Slide 1 is the troll-dog hook, and the last slide is the product render. Up to 5 slides at 1080x1350 or 1080x1920 (all slides the same size).
- **Links.** The link lives in the bio, so the bio link must land on the gift shown in the week's gift-led posts.
- **What to read:** sends per reach first, then saves, then profile visits and link taps.
- **Boosting.** Promote from Ads Manager, never from the app's "Boost" button. The app button cannot run a separate paid cut, a paid UTM or a clean audience. The ad uses the paid cut, not the organic post, so organic results stay clean.

### Facebook (Page Reels and carousels)

- Post from the Heartside Page with the same master. The tracked link goes in the caption, with no hashtags.
- The first frame matters even more here: Facebook shows retention by second. F10 lost most of its viewers at 0:01.
- **What to read:** shares per reach for humour posts. For gift posts: outbound clicks, landing visits, attributed orders.
- **Boosting:** as on Instagram. One Meta campaign covers both, with placements limited to Reels for the test.

### TikTok

- **Upload.** Upload the master in the app or TikTok Studio, set the cover from the cover file, switch on the AI-generated content label, and add 3 hashtags.
- **Sound.** Keep the licensed track. A trending sound only with Krish's yes, and never on a post that might later run as a Spark Ad unless the sound is in TikTok's Commercial Music Library.
- **The first second is the whole game.** Start on a dog already doing something legible.
- **What to read:** completion and shares per 1,000 views against posts of a similar length. Early abandonment means test the first shot.
- **Before any TikTok spend:** the profile needs a clickable heartside.io link (it had none on 3 Nov).
- **Boosting:** Spark Ads only, from a post whose music is cleared for ads. The authorisation code is generated on the post, and the caption and music then cannot change.

### Pinterest and YouTube Shorts (not active)

- **Pinterest** is preparation only, until the engine supports it and Krish adds it (`docs/CHANNEL-TASKS.md`). It needs a 1000x1500 2:3 Pin and search words in the title, and it deep-links to the exact product.
- **YouTube Shorts** is not a Heartside channel (Krish, 29 Oct: Instagram, TikTok and Facebook only).

## 4. Release steps (Codex, from the library)

1. **Find the row.** Take the row from the live `02…` Sheet and the file from `Posts/<id>/` (organic), or the boost library (paid). Check the SHA-256 against the manifest.
2. **Check the release.**
   - **Posting:** check the approval column is marked, and that the lock fingerprint matches.
   - **Boosting:** also check that every gate in `docs/PAID-BOOSTS.md` is recorded in the manifest.
3. **Publish.** Publish once, with the cover, caption, labels and link exactly as built. Read back the live permalink, the media and the words.
4. **Write back.** Write `status`, `live_url` and `notes`. Read the post at 1 hour, 24 hours, 72 hours and 7 days, and record "not shown" for any number that is missing, never zero.
5. **Hand back what fails.** Anything that needs a crop, recut, caption change or new audio goes back to the engine. Never improvise it at upload.
