# Creative inside the platform

Owner: Heartside production and publishing. Adopted 6 November 2026 from Krish's
`Social_Creative_UI_Best_Practices.docx`, version 1.0. Source SHA-256:
`d3ae673f2e4ff852954d050b8d514b224a8685d93caa2d1f3855cee509894f95`.
The supplied document is source material for this implementation, not authority to
publish, spend, change account settings, or replace a locked master.

## The rule

Approve **export + platform UI + final copy + crop**, per platform and placement.
A clean render, paid preview, upload success, or concept lock is not proof of
organic viewer readability. Organic review does not establish paid eligibility.
The implementation lives in `engine/creative_ui.py`; profile
`social-ui-2026-11-06-v1`. Its coordinates and export presets are house choices,
not official limits, permanent safe zones, or accessibility certification.

The reference's Android TikTok examples show search UI over the chat header,
messages and subtitles under metadata, and poor contrast for white native
controls. Expanded descriptions may legitimately obscure the scene. A creator
promotion strip is not assumed to appear to ordinary viewers: inspect a
non-owner view. Identify the media rectangle before measuring coordinates;
never scale the phone status/navigation bars into a video template.

## Production defaults

| Use | Starting export | Required surfaces |
|---|---|---|
| Instagram Reel / Story | 1080x1920 | full screen, feed, profile cover; Story stickers/reply region |
| TikTok video | 1080x1920 | feed, search entry, non-owner; audio art and AI/anchor labels |
| Facebook Reel | 1080x1920 | mobile feed, Page, opened player; final see-more boundary |
| Instagram / Facebook image or carousel | 1080x1350 | feed, profile/Page, actual crop of every slide |
| Threads / X image | 1080x1350 (square is an alternative) | timeline, opened media, grouping and link card |
| Pinterest image | 1000x1500 | home/search card, close-up, Save/control overlap |
| Pinterest / Threads / X vertical video | 1080x1920 | inline/card and opened viewer separately |

Only Instagram, Facebook and TikTok are active Heartside channels. The remaining
profiles are preparation guidance, not channel activation or automatic posting.
Confirm dimensions/features in the actual account and upload tool each campaign.

For 1080x1920 Reels/TikTok, start essential content inside x108–864, y288–1152.
Start subtitles at y960–1120, within those horizontal bounds. Backgrounds fill
the canvas; faces, product detail, payoff, mark and hook must stay readable.
Move subtitles within the content box to protect faces/products. If content
does not fit, split the beat or recompose the placement; do not shrink to tiny
type. Test normal, stress (longer text/search/labels/attachments) and expanded
states. Expansion needs an observed behaviour record, not an unobscured-video pass.

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

`factory/ui_layout.py` supplies the chat and film defaults. Exact locked master
specifications and matching slot-only variants retain legacy geometry; new
concepts get this profile. A placement repair of a legacy variant explicitly
opts in as a new candidate, rather than inheriting its old approval.
An intentional revision of a locked master sets `ui_profile` to the revision
above, which changes its fingerprint and requires fresh approval. Never silently
rewrite `factory/specs`, locks, release hashes or queued posts. In particular,
the 4 November ruling keeping F01/F02/F03/F05/F12 at y1440 remains recorded.
Search and roast outputs still need the same placement review; their legacy
geometry is not certified by the new chat/film helpers.

New-profile roast renders now use measured, bounded text and an intact fitted
product. New-profile film stills move only the picture beneath static subtitles;
zooming a flattened caption would invalidate its measured bounds. Existing
locked versions keep their original geometry. `factory/repair_ui.py` makes
separate editions from hash-bound clean sources, exact bank wording and shot
boundaries, with frame-count and original audio-bitstream verification.

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

New/recomposed specs must declare that profile before locking, so a later lock
cannot switch a build back to legacy geometry. Create a separately identified
candidate when changing a locked skeleton; the existing drift guard continues
to refuse rewriting its original lock. This is a new review, not a slot-only variant.

`engine/media.py` uses the same working region for new vertical recognition cards,
separate feed/Pin composition, and a new renderer revision. Oversized wording
fails fitting. Its old Example badge is removed under Krish's existing 2 Nov rule.

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
