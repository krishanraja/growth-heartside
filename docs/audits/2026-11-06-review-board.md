# Review board repair

Target: the local creative review for the38-file corrected library, not any social
post or production storefront. Krish supplied a screenshot of blank video players,
broken images and horizontal scrolling in the earlier HTML file preview.

Pass signal: every displayed image loads, each reel starts playback, captions are
available by platform and the board fits desktop and390px widths. Scope authorizes
reversible board repair only; paid/published actions remain excluded.

`factory/review_board.py` now renders and serves verified local files. Start from
the repository with `python factory/review_board.py local/creative-ui --serve`.
It binds only127.0.0.1:8767 and serves an explicit allowlist, not the private folder.
The entry point is http://127.0.0.1:8767/ on the computer running it. This address
is not a remotely accessible phone-review link. The process must remain running.

Verified6 November:
- All38 served file hashes match the selected release manifest.
- Video byte-range request returns206 with exactly the requested100 bytes.
- Request for an unselected private packet returns404.
- Browser readback:22/22 images loaded with nonzero natural size;8/8 videos ready,
  with correct nonzero durations and no media errors.
- Started all8 through visible Play buttons; playback advanced. This checks player
  function, not a repeat full-length creative or native-platform review.
- Desktop and390x844 responsive layout: no horizontal page overflow. Media wraps
  into a single column at narrow widths. Temporary viewport restored.
- Final screenshot: `local/creative-ui/board-fixed.jpg`. Local-only evidence and
  media remain excluded from git. The board remains open as the user deliverable.

The previous endpoint checks established CDN bytes, not successful rendering in
the user's file-preview client. That evidence gap caused the failed handoff.
No claim is made about the exact browser policy that blocked those remote loads.
