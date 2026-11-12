# Publishing playbook: how every Heartside asset goes out, channel by channel

This is the checklist a creative must pass before it is posted or boosted, plus the per-channel practice. It adds to `docs/CHANNEL-TASKS.md`, which owns the weekly loop and what to read from each post; this file owns what to build and check before release. It never edits a locked post: a post that fails here goes back to the engine.

- Paid use also follows `docs/PAID-BOOSTS.md`.
- Choose the exact release file in [the current publishing library](../library/CURRENT.md). File and paid-use rules follow `docs/BOOST-LIBRARY.md`.
- The quality bar and current scores are in `docs/audits/2026-11-04-creative-audit.md`.

Platform specs move. For new/revised releases, [CREATIVE-UI.md](CREATIVE-UI.md)
and `engine/creative_ui.py` own composition and placement acceptance (6 Nov).
Export sizes below are house presets. Test the organic viewer independently of
the paid preview; preserve existing locked files and approved captions.

## 1. The master file (every channel)

| Item | Requirement | Check |
|---|---|---|
| Frame | 1080x1920, 9:16, H.264 yuv420p BT.709, constant 30 fps, at most 12 Mbps, AAC 48 kHz stereo, true peak at or under -1 dBTP (12 Nov corpus, section 10) | `factory/lock.py media`, `factory/audit.py` |
| Loudness | -18 to -13 LUFS integrated | `factory/lock.py media` |
| Length | Organic 6 to 60 s, and 15 to 30 s where possible. Paid 15 to 30 s | `factory/audit.py` |
| First second | Motion, and a legible situation on frame 1: no blank interface, no tiny subject, no 2 s still | `factory/audit.py` `dead_open` |
| Ending | The real store render for the same breed and coat, moving, for the last 3 to 4 s: never a dead outro, no on-screen CTA | `factory/lock.py media` and a person |
| Organic working region | Every 9:16 hook, subtitle, label, chat, face, product and mark inside x 120 to 820, y 330 to 1180; hook y 360 to 720; subtitles y 940 to 1160, 1 or 2 lines, at most 7 words a segment. House rule from the 12 Nov corpus, then inspect the exact UI | the layout manifest in `lock.py media`, native review |
| Boosted posts | Use the live approved post unchanged; separately inspect paid CTA, labels and exact placements. Organic clearance is insufficient | `docs/PAID-BOOSTS.md`, placement review |
| Cover | Separate cover composition. Face and headline inside the central 3:4 crop (y 240 to 1680) and the full-screen box; check actual profile grid, Reels tab and feed crops; no assumed permanent crop | Native preview and a person |
| Sound-off | The joke works muted. Subtitles carry every spoken line, timed. One caption system only: no platform auto-captions over burned-in subtitles | A person |
| AI labelling | Photorealistic AI dogs: switch on TikTok's AI-generated content label, and let Meta's "AI info" label stand | At upload |
| Music | The locked licensed track, organic and paid alike. Krish, 4 Nov: "I have the right license for the post type". Settled, never re-check | None |

## 2. Captions (every channel)

- New posts lead with one complete scene-specific thought and at most one useful action. Inspect rendered lines with the actual account name and labels.
- The repeated sales paragraph is no longer a default for new posts (Krish's supplied UI standard, 6 Nov). Previously approved exact captions remain unchanged until a new version is approved.
- Use a verified destination route: Facebook link, or the actual available profile link/sticker/product tag. Never assume a typed URL is tappable.
- Only relevant hashtags/topics; none on Facebook. Do not copy one platform's full caption to all others.
- House rules (AGENTS.md rule 5): US spelling, no exclamation marks, no em dashes or spaced hyphens used as dashes, no swearing or swear acronyms, nothing invented.
- `growth.py check` enforces what code can.
- A standalone joke post gets no "tag a mate" and no product slide (`docs/CHANNEL-TASKS.md`). Gift-led posts may ask for a tag.

## 3. Channel by channel

### Instagram (Reels and carousels)

- **Reels.** Upload the approved Instagram edition and separate cover. Inspect the current grid, Reels tab and feed previews with final copy. Use "Share to Feed" only as approved.
- **Carousels.** Slide 1 is the troll-dog hook, and the last slide is the product render. Up to 5 slides at 1080x1350 or 1080x1920 (all slides the same size).
- **Links.** The link lives in the bio, so the bio link must land on the gift shown in the week's gift-led posts.
- **What to read:** sends per reach first, then saves, then profile visits and link taps.
- **Boosting.** Promote the live post from Ads Manager with "Use existing post", never with the app's Boost button. Ads Manager gives the landing-page-views objective, a "Shop now" button to the product page with the paid tracking link, and a fixed budget per post. The post itself is never changed. The exact settings are in `docs/boost/2026-11-launch-packet.md`.

### Facebook (Page Reels and carousels)

- Post from the Heartside Page with its reviewed edition and concise Page-specific copy. Reusing the same bytes still requires a Facebook review. The tracked link goes in the caption, with no hashtags.
- The first frame matters even more here: Facebook shows retention by second. F10 lost most of its viewers at 0:01.
- **What to read:** shares per reach for humour posts. For gift posts: outbound clicks, landing visits, attributed orders.
- **Boosting:** the Instagram post's ad also runs on Facebook Reels and Feed. One campaign covers both.

### TikTok

- **Upload.** Use the TikTok-reviewed edition, separate cover, required AI label and useful hashtags. Check feed/search entry, normal/stress/expanded description and a non-owner view.
- **Sound.** Keep the licensed track. A trending sound only with Krish's yes.
- **The first second is the whole game.** Start on a dog already doing something legible.
- **What to read:** completion and shares per 1,000 views against posts of a similar length. Early abandonment means test the first shot.
- **Before any TikTok spend:** the profile needs a clickable heartside.io link (it had none on 3 Nov).
- **Boosting:** Spark Ads only. The authorisation code is generated on the post, and the caption and music then cannot change.

### Pinterest and YouTube Shorts (not active)

- **Pinterest** is preparation only, until the engine supports it and Krish adds it (`docs/CHANNEL-TASKS.md`). It needs a 1000x1500 2:3 Pin and search words in the title, and it deep-links to the exact product.
- **YouTube Shorts** is not a Heartside channel (Krish, 29 Oct: Instagram, TikTok and Facebook only).

## 4. Release steps (Codex, from the library)

1. **Find the row.** Take the row from the live `02…` Sheet and the file from `Posts/<id>/` (organic),. Check the SHA-256 against the manifest.
2. **Check the release.**
   - Run the exact placement review in `docs/CREATIVE-UI.md`, binding media, cover, copy, account, destination, labels and attachments. Missing required device/state evidence means hold for the new release, never invent a pass.
   - **Posting:** check the approval column is marked, and that the lock fingerprint matches.
   - **Boosting:** also check that every gate in `docs/PAID-BOOSTS.md` is recorded in the manifest.
3. **Publish.** Publish once, with the cover, caption, labels and link exactly as built. Read back the live permalink, the media and the words.
4. **Write back.** Write `status`, `live_url` and `notes`, plus template revision and the real viewer UI checks (device, state, evidence and any unverified gaps). Read the post at 1 hour, 24 hours, 72 hours and 7 days, and record "not shown" for any number that is missing, never zero. Track re-exports caused by normal-view UI collisions.
5. **Hand back what fails.** Anything that needs a crop, recut, caption change or new audio goes back to the engine. Never improvise it at upload.
