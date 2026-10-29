# Codex card: Heartside breed examples, stage 1

Written 29 Oct 2026 by the growth engine's Claude session for Codex. Krish approved stage 1 only
(6 paintings) on 29 Oct ("go and get codex to build out all the assets"). Stage 2 needs a person's
review of stage 1 and a new yes from Krish; it is not in this card.

Follow this card exactly. Where it is stricter than heartside's brief below, the card wins. If any
step cannot be done as written, stop at that step, record it in `failures.json` and report. Do not
improvise a workaround.

## 0. Set up (no generation yet)

1. In `krishanraja/growth-heartside`, from the latest `main`, create the branch
   `codex/heartside-examples-2026-10-29`. Work and commit only there. Never push to `main`, and never
   touch `krishanraja/heartside`.
2. The source is heartside commit `eccc695c44d98008d5989bd118089acd762e465f` (branch
   `claude/product-launch-readiness-mlh1bc`), folder `design/examples-2026-10-29-breeds/`. Read files
   from `https://raw.githubusercontent.com/krishanraja/heartside/eccc695c44d98008d5989bd118089acd762e465f/<path>`.
   Never read them from heartside's `main`.
3. Run `python3 growth.py examples check --stage 1`. It downloads `jobs.json` into
   `assets/heartside-examples-2026-10-29/` and verifies it against a pinned hash. Expect it to list
   missing files. It must not say the job list is wrong; if it does, stop.
4. The six stage-1 jobs, and only these: `golden-sentimental-portrait`, `lab-warm-portrait`,
   `frenchie-hilarious-portrait`, `doodle-over_the_top-portrait`, `dachshund-sentimental-blanket`,
   `shepherd-warm-blanket`.

## 1. Image generation

- Use your built-in OpenAI image generation (the same model family the store's painter uses), as an
  edit from the reference photo, at the highest quality, at the job's exact `size`. If built-in
  generation is unavailable, stop and report. Do not call any API with a key, and do not use any
  other provider.
- One attempt per item. Never retry, never regenerate to "improve", never keep a second version.
- A painting is generated once. Cutouts, crops and mockups are made from it by code or by edits that
  leave the dog untouched.

## 2. Mockups: how to composite (stricter than the brief)

- The painting goes onto the product by code (for example Pillow or OpenCV: a perspective warp into
  the frame, a cylindrical warp around the mug, a displacement map for the blanket's folds), using
  the master PNG's own pixels. Never pass the painting to an image model to "place" it.
- The product body you composite onto (a plain mug with the job's interior colour, a plain cream
  sherpa blanket, an empty thin frame, and the room or hands around it) may be generated, with
  nothing printed on it. Match the real product exactly as heartside's brief describes. The real
  products are on the live store pages it names: open them and match the shape, the colours and the
  frame.
- The mug and portrait text area stays plain. No words anywhere.
- At most 18 mockup scenes in total (3 per painting); each ratio is a crop or extension of its scene,
  not a new generation.

## 3. Check before every commit

Run `python3 growth.py examples check --stage 1` after each step and before each commit. It must end
with `ready for review`. A file that failed goes in `assets/heartside-examples-2026-10-29/failures.json`
as `{"<path>": "<reason>"}`. Do not hide a failure by leaving a file out without recording it.
Do not write `review.md`: a person writes it.

## 4. Never

- push to `main`, touch heartside, or edit anything outside `assets/heartside-examples-2026-10-29/`;
- generate a stage-2 job, a set, or any extra item;
- use a generated dog as the reference photo, or a photo with people, text or a watermark;
- add words, letters, logos, watermarks or signatures to any image;
- add a prop, costume or accessory the job's `brief` does not name, another dog, or a face;
- install anything beyond Pillow, NumPy, OpenCV and a background-removal model such as rembg;
- post, upload, share or send anything anywhere.

## 5. Report

When `examples check --stage 1` says `ready for review`, commit, push the branch, and reply with:
- the branch and the commit;
- the check's last line;
- a table: job id, painting, cutout, crops, mockup scenes, each done or failed with the reason;
- the photo credits, one line per dog;
- anything you were unsure about, in one line each.

---

## Heartside's brief (unchanged, stage 1)

> You are making the example creative for Heartside, a store that paints a buyer's own dog onto a mug, a sherpa blanket or a framed portrait, with a short line from the dog. These assets will be used on the website, in paid ads, in organic social posts and as recurring dog characters, so make them clean, consistent and reusable.
>
> **Source.** The job list is `design/examples-2026-10-29-breeds/jobs.json` in the `krishanraja/heartside` repository, and each job's prompt is at its `prompt_file`. Run only the jobs whose `stage` is `1`.
>
> **Where to put things.** Work in your own repository. Put everything under `assets/heartside-examples-2026-10-29/`, with the folders named below, and do not push to heartside. When a stage is done, reply with that folder's path and the commit, and Heartside copies the approved files across.
>
> ### Step 1. The reference photo (stage 1, once per breed)
> Find one real photo of the breed under a free licence, such as Unsplash or Pexels. Choose a single dog, face clearly visible, good light, no people, and no text or watermark. Save it as `photos/<dog>.jpg`, with `<dog>` being the job's `dog` value. Record the photographer, the source URL and the licence in `credits.json`. Never use a generated dog as the photo: it stands in for a real customer's dog.
>
> ### Step 2. The painting (one per job)
> 1. Use the photo as the reference for the dog's identity only: the same face, ears, coat colour and markings, the same proportions. Do not copy its pose, framing or background.
> 2. Use the full text of the file at `prompt_file` as the prompt, unchanged. Do not shorten, summarise or add to it.
> 3. Generate one image at `size` with the same image model the store's painter uses (OpenAI's image model, as an edit from the photo), at its highest quality.
> 4. If it comes back in another shape, crop to `size` around the dog. Never add bars, borders or padding.
> 5. Save it as `paintings/<id>.png`. This is the master: everything below is made from it, and the painting itself is never repainted or restyled.
>
> ### Step 3. Reusable cuts of each painting
> - `cutouts/<id>.png`: the dog alone, from the painting, on a transparent background, at full resolution. These are used for stickers, ad overlays and the recurring characters, so make the edges clean.
> - `crops/<id>-1x1.png` (1080×1080), `-4x5.png` (1080×1350) and `-9x16.png` (1080×1920): the painting fitted to each ratio. Extend only the background where the painting is too small, in the painting's own style, and never alter the dog. Keep the dog's face inside the middle 80% so captions and buttons don't cover it.
>
> ### Step 4. Product mockups (the main deliverable)
> Place the master painting onto Heartside's real products. Composite the painting image itself as the product's printed surface, following the product's curve, folds or frame, so the painting stays exact. Never regenerate the art inside the mockup. Products, as sold on heartside.io:
> - **Mug** (`/products/your-dogs-illustrated-mug`): 11 oz white ceramic, with the inside and handle in black, dark blue, dark green, red or pink. The painting wraps the side, and the handle is on the right.
> - **Blanket** (`/products/your-dogs-personality-blanket`): 50 × 60 inch sherpa fleece, printed edge to edge, with no words.
> - **Portrait** (`/products/your-dogs-portrait`): a 12 × 18 inch vertical print in a simple thin frame.
>
> Each job's painting goes on its own `format` gift. Make three scenes per painting:
> 1. **Studio:** the product alone on a soft cream background, evenly lit. This is the shop shot.
> 2. **Home:** the product in a real, lived-in home moment that fits the tone:
>    - Sentimental: quiet morning light.
>    - Warm: a cheerful kitchen or sofa.
>    - Hilarious: a bright, playful setting.
>    - Over the top: a grand, theatrical setting, such as velvet, gold light or a spotlight.
> 3. **In hand:** the mug held in two hands, the blanket draped over a sofa arm, or the portrait being hung on a wall. Hands and arms are fine; show no faces.
>
> Save each scene at 1:1, 4:5 and 9:16, as `mockups/<id>/<scene>-<ratio>.png`. The scene is `studio`, `home` or `hand`; the ratio is `1x1`, `4x5` or `9x16`.
>
> **The set, once per breed:** that breed's three gifts together, the mug, the blanket and the portrait, each carrying one of that breed's paintings, in one home scene. This is the bundle shot. Save it as `mockups/<dog>-set/home-<ratio>.png` at all three ratios.
>
> ### Step 5. The manifest
> Write `manifest.json`: one entry per file, with:
> - `file`, `job` (or the dog, for a set), `breed`, `style`, `tone`, `gift`;
> - `kind`: `painting`, `cutout`, `crop`, `mockup` or `set`;
> - `scene` and `ratio`;
> - `uses`: any of `site`, `ad`, `social`, `character`.
>
> ### Rules for every asset
> - No words, letters, logos, watermarks or signatures anywhere. Heartside adds the dog's line and any captions itself, so leave the mug's and the portrait's text area as on the product, plain.
> - No props, costumes or accessories beyond the ones in the job's `brief`. No other dogs. No people's faces.
> - The dog in every asset is exactly the dog in its painting.
>
> ### Limits
> - Stage 1: at most 6 paintings, 6 cutouts and 18 mockup scenes.
> - Stage 2: at most 18 paintings, 18 cutouts, 54 mockup scenes and 6 sets.
> - Ratio variants and crops are edits of an image you already made, not new generations.
> - One attempt per item and no retries. Report anything that failed instead.
> - When finished, list every job id with its paintings, cutouts and mockups, and whether each is done or failed, with the reason for any failure.
