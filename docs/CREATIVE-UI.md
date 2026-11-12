# Creative inside the platform

Owner: Heartside production and publishing.

**Current profile: `social-corpus-2026-11-12-v2`** (Krish, 12 Nov 2026: "Ensure all social media posts
adhere to these best practices."). Source: [the 12 Nov corpus](../knowledge/social-media-creative-production-corpus-2026-11-12.md),
SHA-256 `483cf6c3ed3889e8b57279115fa31f9dc948ddb49e7e858aef3d94a2adeb5c93`. It supersedes the 6 Nov profile
`social-ui-2026-11-06-v1`, adopted from Krish's `Social_Creative_UI_Best_Practices.docx` (SHA-256
`d3ae673f2e4ff852954d050b8d514b224a8685d93caa2d1f3855cee509894f95`); the rest of this page keeps that
document's review method. Where every existing post stands: [the 12 Nov audit](audits/2026-11-12-corpus-audit.md).
The corpus is source material, not authority to publish, spend, change account settings or replace a locked master.

## The rule

Approve **export + platform UI + final copy + crop**, per platform and placement.
A clean render, paid preview, upload success, or concept lock is not proof of
organic viewer readability. Organic review does not establish paid eligibility.
The implementation lives in `engine/creative_ui.py`. Its coordinates and export presets are house choices
(the corpus marks them HOUSE RULE), not official limits, permanent safe zones, or accessibility certification.
"The frame is not the canvas the user can read" (corpus, last line).

Every renderer writes a **layout manifest**: each hook, subtitle, label, chat bubble, title, logo and
product box with its time span, bound to the file's SHA-256. `layout_errors` checks it against the regions
below and `export_errors` checks the encoded file. `factory/lock.py media` and `gate`, the release check,
`factory/audit.py` and `codex/check_picture.py` all hold a post that breaks either. A build without a
manifest (a legacy renderer) cannot pass.

The reference's Android TikTok examples show search UI over the chat header,
messages and subtitles under metadata, and poor contrast for white native
controls. Expanded descriptions may legitimately obscure the scene. A creator
promotion strip is not assumed to appear to ordinary viewers: inspect a
non-owner view. Identify the media rectangle before measuring coordinates;
never scale the phone status/navigation bars into a video template.

## Production defaults

| Use | Export | Required surfaces |
|---|---|---|
| Instagram Reel / Story | 1080x1920 | full screen, feed, profile cover; Story stickers/reply region |
| TikTok video, TikTok photo post | 1080x1920 | feed, search entry, non-owner; audio art and AI/anchor labels; every slide |
| Facebook Reel / Story | 1080x1920 | mobile feed, Page, opened player; final see-more boundary |
| Instagram / Facebook image or carousel | 1080x1350 (1080x1080 or 1080x1440 when the layout needs it); one size for every slide | feed, profile/Page, actual crop of every slide |
| YouTube Short / long-form / thumbnail | 1080x1920 / 1920x1080 / 1280x720 | preparation only: YouTube is not an active Heartside channel |
| Threads / X image | 1080x1350 (square is an alternative) | timeline, opened media, grouping and link card |
| Pinterest image | 1000x1500 | home/search card, close-up, Save/control overlap |

Only Instagram, Facebook and TikTok are active Heartside channels. The remaining
profiles are preparation guidance, not channel activation or automatic posting.
Confirm dimensions/features in the actual account and upload tool each campaign.

### Regions on a 1080x1920 canvas (corpus 3.5)

| Region | Box | What goes there |
|---|---|---|
| Full bleed | x 0 to 1080, y 0 to 1920 | backgrounds and footage; a crop is allowed |
| **Critical content** | **x 120 to 820, y 330 to 1180** | every hook, subtitle, label, chat, face, product detail and mark |
| Opening hook | x 140 to 820, y 360 to 720 | the first words, seen in the first 3 s |
| Subtitles | x 130 to 820, y 940 to 1160 | timed subtitles; they may move inside the critical box to clear a face or product |
| Logo or credit | x 140 to 780, y 360 to 940 | only if essential; never bottom right like a watermark |
| Closing line | x 140 to 820, y 820 to 1150 | a final payoff; no on-screen CTA on organic posts (Krish, 2 Nov) |
| Cover grid model | y 240 to 1680, full width | the central 3:4 profile-grid crop; a cover that cannot satisfy both this and full screen gets its own cover file |

Feed slides keep a 70 to 100 px design margin (the renderers use 90). On a 9:16 TikTok photo slide the line
sits in the hook region and the photo inside the critical box, on ink so TikTok's white controls stay visible.

### Words, timing and export

- **Hook:** one claim or question, at most 12 words, 3 to 7 the target; never a paragraph. Frame 1 shows the
  story (a dog, a payoff, a question), never a logo or an empty chat or search page. A title beat is 0.5 to 1.5 s.
- **Subtitles:** accurate words, 1 or 2 lines, at most 7 words a timed segment, 44 to 64 px, on a stable
  dark panel. The film renderer splits each voice line itself (`engine.creative_ui.segments`). One caption
  system only: a burned-in subtitle plus the platform's auto-captions is a fail.
- **Ending:** the real product, moving, 3 to 4 s: Krish's floor `endings-land` keeps at least 3 s and the
  corpus forbids a dead outro. The "one next action" lives in the post description.
- **Export:** H.264 High, yuv420p, progressive, BT.709 SDR, constant 30 fps (or the source rate, 24 to 60),
  CRF 18 capped at 12 Mbps (a still or flat frame lands under 8 Mbps; that is a reviewer note, never padded),
  AAC 48 kHz stereo 192 kbps, true peak at or under -1 dBTP. `FFMPEG_VIDEO` and `FFMPEG_AUDIO` in
  `engine/creative_ui.py` are the one copy every renderer uses.
- Keep the clean master, the burned-in edition, the transcript, the cover and the platform copy as separate files.

- Chat: latest two or three messages at most, one payoff per beat, title below
  top UI. Every new message must fit; the renderer rejects a disappearing payoff.
  A readable carousel is an alternative for longer conversations. Fictional chat
  stays visibly creative; no fake input control, engagement count or notification.
- Film/mug: a narrower subtitle panel above metadata, dog expression and real
  product both visible. No caption repeating the same line as the post opening.
- Text: hook one short thought (usually 4–10 words); cover title usually 3–6.
  Speech captions one or two accurate timed lines with meaningful sounds;
  48–64px starting type, 64–96px short headlines at 1080 width. Read at normal
  speed, with time to see the image. Keep a corrected transcript with the edit.
- Contrast: house target 4.5:1 for ordinary text, assessed on the worst frame.
  Use a stable panel/scrim/outline. Inspect native white controls over light
  artwork; a background treatment must not compete with the story.
  The 6 Nov Buffer preview exposed invisible white controls on cream TikTok
  photo cards. `factory.ui_layout.photo_card` now uses brand ink around the
  photo and cream headlines for TikTok, while feed cards retain cream. The
  image and carousel TikTok presets are 1080x1920; this remains a house choice.
- Layers: keep picture, text, subtitles, branding and cover independently
  editable. Do not bake editor overlays, native controls, other-platform
  watermarks or required platform labels into the export. Preserve provenance.
- Branding: use intact supplied artwork, clear space and stable contrast;
  small and readable in the tested crop. Account identity stays brand-first.
  Never rely only on the avatar, truncated display name or final end card.
- Accessibility: use corrected native captions/uploaded tracks where supported.
  Preview with native and baked captions together; fix duplication/collision
  without removing the only accessible caption route. Alt text describes subject,
  action and essential words; it is separate from discovery copy.

`factory/ui_layout.py` supplies the chat, film and photo-card helpers; `factory/still.py` the still and
carousel slides; `engine/media.py` the campaign cards. **Placement is not content** (12 Nov): `ui_profile`
is no longer part of a lock's fingerprint, so every factory spec now declares the corpus profile and still
matches its lock (`lock.fingerprints` also accepts a lock recorded while the profile was in the skeleton).
A spec with no profile, or the retired 6 Nov one, is held by `lock.py check`. Content changes (words,
timings, sounds, products) still drift and still need Krish. Never silently rewrite `factory/specs`, locks,
release hashes or queued posts.

This supersedes the 4 November ruling that kept F01, F02, F03, F05 and F12's subtitles at y1440 for any
**new** edition: Krish's 12 Nov instruction covers all posts, and y1440 sits under TikTok's caption. Their
live posts are not touched. A film's `cap_y` now only moves its subtitles inside the critical box.

Renderers in the corpus profile move only the clean picture under static words (a zoomed caption would leave
its measured box); a card's slow push-in is recorded at its largest. A search query that cannot fit one
readable line (40 px floor) and a chat that cannot show four messages refuse to build: rewrite the line,
never shrink it. `factory/repair_ui.py` makes separate editions from hash-bound clean sources, exact bank
wording and shot boundaries, with frame-count and original audio-bitstream verification.

### Buffer delivery contract (verified 6 Nov)

Set video title and frame selection under `video.metadata.title` and
`video.metadata.thumbnailOffset`, with `video.url` beside metadata. The current
route supports a 1000ms frame for Instagram/TikTok; omit the offset for Facebook
and inspect its automatic first frame. Separate JPG covers are references, not
applied custom thumbnails. See the official [VideoAssetInput](https://developers.buffer.com/types/VideoAssetInput.html)
and [VideoMetadataInput](https://developers.buffer.com/types/VideoMetadataInput.html).
Read back actual fields after every save; accepted input alone is insufficient.

Generated-source editions set supported Instagram/TikTok AI disclosure inputs.
Do not preserve a known incorrect false value merely because it was in the old
draft. Buffer's Facebook native flag and TikTok photo flag are not exposed by
the current route: use accurate visible copy disclosure, record the unsupported
native flag honestly, and inspect the platform at release. Source-photo posts
must not be falsely labelled generated.

Every spec declares the current profile before locking or building. Create a separately identified
candidate when changing a locked skeleton's content; the drift guard refuses rewriting its original lock.

`engine/media.py` renders vertical cards with the mark in the logo region, the hook in the hook region (up
to three lines), the product beneath it and the scene text in the subtitle band, writes a layout manifest
per platform reel, and encodes with the export preset (renderer version 10). Oversized wording fails
fitting. Its old Example badge is removed under Krish's existing 2 Nov rule.

## Platform copy and traffic

Compose the final description with the media. Lead with a complete scene-specific
thought, followed by at most one useful action and relevant hashtags/topic. The
long repeated shop paragraph is no longer the default for **new** posts. Exact
approved captions stay intact until a new version is approved. Judge visible
lines on a phone rather than treating a character count as a safe-zone guarantee.

- Instagram: verify profile link, Story sticker or available product tag as a
  viewer; typed caption URLs are not assumed clickable. Separate cover design;
  test current grid, Reels tab and feed crops rather than assuming one 3:4 crop.
- TikTok: concise opener and one verified route; include audio, AI and anchor
  regions. Compare owner/non-owner and feed/search views. Correct auto-captions.
- Facebook: Page-specific description, meaningful first frame and thumbnail.
  Check link destination/card and album grouping; a Reel, photo URL and link
  post are different presentations. Do not infer a crop from the Reel label.
- Threads: text-led premise; media adds proof or payoff. Use native longer text
  if available instead of a tiny paragraph screenshot. Relevant topic, no copied
  hashtag block. Check link preview and alt-text support in the actual route.
- X: short complete opening, one legible scene, no sentence split over a media
  collage. Check actual composer count, ALT presentation and inline/full-screen
  caption behaviour. Verify the native link and preview.
- Pinterest: card-first product/result, title meaning early, destination in the
  link field. Do not depend on description visibility. Keep Save controls clear;
  inspect tonal treatment of cream/near-white artwork and separate alt text.

For paid use, inspect the exact current placement, CTA, disclosures, rights and
eligibility. Reuse recorded rights for the same licensed use; a changed use needs
new evidence. TikTok ad templates are format/caption/anchor-specific and never
an organic guarantee. Public-source claims and field limits in the supplied
document are dated 6 Nov, not independently refreshed by this implementation.
Recheck the cited provider documentation at release, including the Pinterest
policy update the document flags for 12 Nov. Do not hardcode those limits as fact.

## Executable release check

Copy `config/creative-ui-release.example.json` to `local/creative-ui/`, fill the
actual metadata, and list every export/cover/transcript with its SHA-256. Paths
are repository-relative; private account and device evidence stays under `local/`.
For an automated proposal the exact filenames are
`local/creative-ui/<full revision>/<creative_id>.release.json` and `.review.json`.
Store captures inside `local/creative-ui/` too. The checkpoint exporter includes
this directory so the next scheduled runner can read back the same evidence.

```sh
python -m engine.creative_ui stub local/creative-ui/release.json local/creative-ui/review.json
python -m engine.creative_ui check local/creative-ui/release.json local/creative-ui/review.json
python factory/lock.py gate SPEC MP4 --release local/creative-ui/release.json --review local/creative-ui/review.json
```

The stub contains **unverified** verdicts. An actual reviewer records each
check and observation, device (Android/iOS where both matter, desktop for
timeline/link-led views), OS/app/tool version, date and evidence file hashes.
Each observation is `{device, state, verdict, evidence: [{path, sha256}]}`.
All states require `pass`, except `expanded`, which requires `observed`.
Minimum states: opening, busiest, ending, full playback, cover/card, normal,
stress, expanded, plus the platform surfaces in `SURFACES`. Carousels/images
include `all_slides`; Stories include `stickers`; paid includes `ad_preview`.
Record all devices required by the campaign; an untested required state holds.

The gate binds the entire payload, including account, platform, organic/paid,
copy, hashtags/topic, link, labels, native caption route, attachments, crop,
cover, media bytes and template revision. A change invalidates the review.
Evidence older than 31 days, future dates, missing files, incomplete checks and
stale bindings hold. Refresh per campaign and immediately after visible UI change,
even inside that 31-day ceiling. Capture overlays with platform, placement,
language, aspect ratio and state; record those details in `environment`.

This proves that complete, matching evidence was recorded; code cannot certify
what the screenshot depicts or substitute for a person watching the post.
`factory/lock.py gate` now requires the review. `engine/protocol.py` refuses an
automated posting proposal without the matching placement evidence, even if a
creative is marked approved. Recording an already-published result remains
possible: a bad UI check must not erase factual delivery history.

After authorized publication, scheduling records the real viewer permalink,
template revision, device, inspected states and any remaining gaps alongside
the release receipt. Track re-exports caused by normal-view UI collisions;
target zero collisions in approved normal-view checks. A preview is provisional
until the published viewer result is inspected. Any repair returns to production
as a new version; this policy never edits a live/queued post or authorizes spend.
