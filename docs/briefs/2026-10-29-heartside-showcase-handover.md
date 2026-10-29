# Claude Code handover: bring the breed example artwork into heartside

29 October 2026. Paste the prompt below into a Claude Code session on `krishanraja/heartside`.

---

Read heartside's README, canon and `NOW.md` first, as every session does. Your job is to bring
Heartside's new example artwork into the store so it shows off the products and feels exciting, and,
when your build is done, to write the CoWork prompt that realigns the artwork in Shopify, Teeinblue and
anywhere else the store shows product images.

**The artwork.** Six example dogs, each painted in its own style, across four tones and all three
gifts. They were made from heartside's own painter prompt (recipes v10 to v12, the directed brief), one
generation each from a real stock photo, and approved by Krish one by one.

| Dog | Breed | Style |
|---|---|---|
| Maple | Golden Retriever | Painterly |
| Bear | Labrador Retriever | Cinematic |
| Bao | French Bulldog | Comic book |
| Clover | Goldendoodle | Vintage screenprint |
| Frank | Dachshund | Fine ink drawing |
| Juno | German Shepherd | Cut-paper collage |

- Source of truth: `krishanraja/growth-heartside`, PR #29 (branch `codex/heartside-examples-2026-10-29`),
  folder `assets/heartside-examples-2026-10-29/`, following your own brief in
  `design/examples-2026-10-29-breeds/README.md`. For every job: `paintings/`, `cutouts/` (transparent
  dog), `crops/` (1x1, 4x5, 9x16), `mockups/<job>/<studio|home|hand>-<ratio>.png`, `contact/`, the real
  reference `photos/<dog>.jpg` with `credits.json`, and `manifest.json` (breed, style, tone, gift,
  kind, scene, ratio and intended uses for every file).
- **Only use what the ledger approves.** `assets/heartside-examples-2026-10-29.approvals.json` lists
  every painting made; use a job only where it has an entry with `status` "approved", and check the
  painting's sha256 against it. 23 of 24 are approved; `shepherd-hilarious-portrait` and the six bundle
  shots (`mockups/<dog>-set/`) are still coming and will appear in the same places.
- The same set is filed for people in Google Drive: `Heartside/00_Brand-Assets/02_Imagery/Product-Examples`.

**What to build.** Art-direct it yourself; Krish wants it to show the products off and feel like magic,
accurate magic. One idea from him to consider, not a spec: the real-life dog transitions seamlessly
into its artwork and then into the product mockup (photo, then painting, then the gift), which this set
supports because each dog has its real photo, its painting, a clean cutout and mockups on every gift.
Other things the set makes possible: a breed and style gallery, one dog seen in all four tones, each
gift shown in studio, home and in-hand scenes, and the bundle shots for gift sets.

Rules that hold:
- Every one of these images is an Example. Label it so wherever it appears, and never present it as a
  customer, an order, a review or a result.
- Follow heartside's canon on voice, layout, performance and accessibility; keep pages fast (serve the
  right size of each image, never the full PNGs to a phone).
- Copy only approved files into heartside, recording where each came from (job, file, sha256).
- Remove the old gallery images that these replace (the pug examples) from the theme and repository
  wherever they are no longer used, after the new ones are in place.
- Do not publish the theme, push to `main`, or change Shopify or Teeinblue from this session: build on a
  branch, run heartside's tests and checks, and open one pull request with screenshots at phone and
  desktop width.

**Then write the CoWork prompt.** When the pull request is ready, write a CoWork prompt (saved in
heartside's docs, and given to Krish in your final message) that realigns the live artwork after he
merges and publishes: Shopify product media for the mug, blanket and portrait (replacing the old
gallery with the approved mockups, Example-labelled, in a sensible order per product), Teeinblue
templates, previews and the default artwork shown in the personaliser, collection and homepage
images, and anywhere else the old pug examples still appear. It must work only from the approved
files, change nothing it cannot verify, record what it replaced, and stop for Krish before anything
irreversible or customer-facing goes live.

Finish with the pull request link and the CoWork prompt.
