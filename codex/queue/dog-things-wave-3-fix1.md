---
card: dog-things-wave-3-fix1
title: F50 only - make the Christmas card fill the end frame
spend_id: 1cfc68d6-34db-488d-8842-df5b65f9b4f0
max_minutes: 15
max_calls: 20
write_allow: [out/F50.mp4, build.py]
---
## Goal

Claude's full-size check of `out/F50.mp4` (card dog-things-wave-3) found one problem: the end shot shows
`inputs/heartside-christmas-card.jpg` too small to read on a phone, because the render has wide margins around the
two cards. Rebuild only F50. Change only that product shot:
- find the bounding box of the two cards inside the render (where it differs from its flat background);
- scale the render so that box is about 960 px wide, centered on the 1080x1920 frame on `#F4EFE6`;
- keep the same 3.5 s hold, with no push-in, text, badge or border;
- scale only: never recolor, redraw or edit the render's pixels.

Every other shot, label, timing and the cover stay byte-identical in output to the first build.

## Floor

- `real-product`: the store's render, unaltered except for scaling, held 3.5 s.
- Everything in card dog-things-wave-3 still applies.

## Acceptance

python3 -c "import subprocess;d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/F50.mp4']));print('ok' if abs(d-14.7)<0.2 else d)"

## Return

The rebuilt `out/F50.mp4` and the scale factor used.
