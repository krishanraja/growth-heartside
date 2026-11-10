# Heartside official icon

Approved by Krish, 10 November 2026:

> D. Make it official and I'll go and implement it as the website favicon, etc.

The official symbol is the geometric chestnut dachshund giving a playful wink while holding a cream envelope with a burgundy heart. It is an affectionate gift-giver. The burgundy background is part of this approved edition.

## Source and use

`heartside-icon-master.png` is a byte-identical copy of approved option D, 1254 x 1254 pixels. Its SHA-256 and all export hashes are in `manifest.json`. This is a raster master, not an SVG or editable vector. Do not auto-trace, remove its background, change the expression or regenerate the design as though those were approved changes.

Use this icon for social avatars, favicon and app icons. This decision approves the icon; no new wordmark is included. Earlier photorealistic, pixel, mascot and linocut candidates remain historical, not current branding.

## Website handoff

Krish owns implementation in the website repository. These are standard filename suggestions, not a claim that the site has changed:

- `favicon.ico`: bundled 16, 32 and 48 pixel sizes.
- `favicon-16.png`, `favicon-32.png`, `favicon-48.png`: individual browser icon exports.
- `apple-touch-icon.png`: 180 x 180.
- `icon-192.png`, `icon-512.png`: manifest/app exports.
- `social-avatar-1080.png`: square social profile upload.

Keep the approved original if a future vector redraw is commissioned. Tiny favicons naturally lose envelope and eye detail; the source is not silently simplified. Check the favicon in an actual browser after implementation, including cache refresh and light/dark browser chrome.

Typical website references, adapted to the site's existing framework:

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
```

The 192 and 512 pixel icons are also suitable for an existing web manifest. This handoff does not change the site's manifest or its theme color.
