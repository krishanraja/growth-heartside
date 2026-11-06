# Unpublished creative correction

Date: 6 November 2026. Authority: Krish asked to integrate the supplied document,
correct all current unpublished posts, and recover the original images, including
Runway. This is the production continuation of the separate implementation audit.

## Delivered production

- Eight reels: F01, F03, F04, F05, F07, F12, F06-dachshund and F06-lab.
- Ten F06 carousel slides, twelve Thanksgiving platform images and eight reference
  covers: 38 selected files in `library/editions/2026-11-06-ui.json`.
- Original source stills recovered from generation history, approved Runway motion
  recovered from receipts, and historical motion located in the exact source
  workspace. No new paid generations. Real product artwork remains unchanged.
- Every reel retains the original AAC bitstream and decoded frame count. Shot
  boundaries and bank wording are checked before rendering. All 59 caption beats
  fit the working region without dropping or reordering words.
- Longer spoken lines use sequential two-line beats; captions avoid dog faces and
  product artwork. The picture moves beneath static text. No subtitle shrinking.
- Separate 4:5 feed and 9:16 TikTok photo compositions. Preview inspection caught
  low contrast between white TikTok controls and cream; six v2 TikTok cards now
  use ink backgrounds. Original photos and exact joke wording are retained.

## Persisted evidence

Private evidence lives in `local/creative-ui/` and
`C:/Users/krish/.scratch/heartside-quality-hold-20261106/`.

- `plans/` and `editions/*/render-receipt.json`: source and master hashes, exact
  frames, timed caption beats and unchanged audio hashes for eight real renders.
- `hosted-readback.json`: all 38 selected files downloaded independently from the
  library API and permanent CDN; every SHA-256 matches the local release.
- `drive-readback.json`: all 38 selected names, byte sizes and canonical parent
  folders observed in Drive. The connector strips checksum fields; this is not
  a claim of independently downloaded Drive-byte equality.
- `replacement-packet.json`: exact 33 IDs, final copy, attachment order and hashes.
  The scheduling chat is sole Buffer writer; production inspected previews only.
- Scheduling readbacks record exact persisted draft media, copy, title, selected
  frame, alt text, AI flags and metadata differences. 37 excluded drafts remain
  unchanged; published posts were not edited. No paid spending occurred.
- Final evidence: `final-persisted-readback.json` in the scheduling scratch folder
  and production `final-verification.json`. Production independently compared all
  33 persisted descriptions, ordered URLs, video titles/offsets and image alt text
  against the final packet. All matched. A local transport encoding defect was
  repaired in the packet only; Buffer's correct punctuation was preserved.
- `review.html` contains every selected delivery creative and per-platform copy.

## Preview findings and fixes

Buffer's authenticated previews were inspected for F12 TikTok, Instagram and
Facebook reels, all five dachshund Instagram carousel slides, and the Thanksgiving
TikTok photo layout. These are Buffer previews, not native device acceptance.

The original video metadata mapping was rejected silently: custom JPG video
thumbnail URLs are unsupported. The final route uses `video.metadata.title` and
`video.metadata.thumbnailOffset=1000` on Instagram/TikTok, automatic first frame
on Facebook. All 20 titles and 14 supported offsets persisted; six Facebook reels
use automatic thumbnails. Eight reference cover JPGs are not claimed applied.

Nine generated Instagram drafts originally had false AI flags; corrected to true.
Eight TikTok video flags were already true. Facebook's native flag and TikTok
photo flags are unsupported in this route. Explicit caption disclosures identify
generated scenes/photos; F19/F20/F21 retain their source-photo status. Unsupported
native fields are not falsely reported as set. Privacy/comment controls are not
exposed by the readback and were not changed.

## Implementation verification

- 25 focused creative UI, factory-lock and media tests pass, including actual
  FFmpeg media tests.
- All eight source-repair plans pass wording/timing validation; deliberately
  changed wording is rejected for each plan.
- A real 30-frame factory film render keeps subtitle bounds identical on first
  and last frames: `(108,960,864,1056)`, inside the working region.
- The reusable photo-card renderer reproduces all twelve delivered image hashes.
- Locked specifications and original library manifest remain unchanged.

## Release boundary

Status: corrected drafts, held. Physical-device Android/iOS, native search entry,
non-owner views, expanded descriptions, native caption interaction and final
profile crops remain unverified. The new evidence gate stays unverified for those
states. Do not describe Buffer preview review as native approval or imply that a
successful save publishes anything. Resume through the scheduling chat after
review clearance; recheck timestamps and never blindly restore elapsed slots.

Ten interim UI files remain unselected in Drive: three v1 covers, F06-lab v1
slide3 and six cream v1 TikTok cards. They are excluded by the selected manifest;
no new deletion authority is inferred. Original locked masters remain retained.

North Star: improves the clarity and usability of organic distribution. No new
organic sales measurement or conversion lift is claimed.
