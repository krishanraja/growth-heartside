# Codex card: Heartside breed examples, stage 1

Written 29 Oct 2026 by the growth engine's Claude session for Codex. Krish approved stage 1 only
(6 paintings) on 29 Oct: "go and get codex to build out all the assets". He also said this batch
"is going to set the tone for everything", so the bar is a professional product shoot, not a draft.
Stage 2 needs a person's review of stage 1 and a new yes from Krish; it is not in this card.

Follow this card exactly. Where it is stricter than heartside's brief at the end, the card wins. If
a step cannot be done as written, stop at that step, record it in `failures.json` and report. Do not
improvise a workaround, and do not lower the bar to finish.

## 0. Set up (no generation yet)

1. In `krishanraja/growth-heartside`, from the latest `main`, create the branch
   `codex/heartside-examples-2026-10-29`. Work and commit only there. Never push to `main` or to any
   other branch, and never touch `krishanraja/heartside`.
2. The source is heartside commit `eccc695c44d98008d5989bd118089acd762e465f` (branch
   `claude/product-launch-readiness-mlh1bc`), folder `design/examples-2026-10-29-breeds/`. Read files
   from `https://raw.githubusercontent.com/krishanraja/heartside/eccc695c44d98008d5989bd118089acd762e465f/<path>`.
   Never read them from heartside's `main`.
3. Run `python3 growth.py examples check --stage 1`. It downloads `jobs.json` into
   `assets/heartside-examples-2026-10-29/` and verifies it against a pinned hash. Expect a list of
   missing files. If it says the job list is wrong, stop.
4. The six stage-1 jobs, and only these: `golden-sentimental-portrait`, `lab-warm-portrait`,
   `frenchie-hilarious-portrait`, `doodle-over_the_top-portrait`, `dachshund-sentimental-blanket`,
   `shepherd-warm-blanket`.

## 1. The pilot: one job, then stop

Do `golden-sentimental-portrait` alone, through every step below, to the full bar. Then:
`python3 growth.py examples check --stage 1 --only golden-sentimental-portrait` must end `ready for
review`. Commit, push the branch, report (section 7) and **stop**. Do not start the other five until
you are told "continue" after a review of the pilot. Anything the review asks you to change about
your method applies to the other five; the pilot itself is not redone unless Krish says so.

## 2. The reference photo

- Search Unsplash and Pexels for the breed. Look at several before choosing one.
- The one you choose: a single adult dog of that exact breed, the whole head sharp, eyes and nose
  in focus, natural colour, even light, no people or hands, no other animals, no text, logo or
  watermark, no costume. Prefer a three-quarter view that also shows the body, so the painting can
  show more than a head. Coat colour as the job's brief implies (a golden Golden, a black or yellow
  Lab is fine, a fawn or brindle Frenchie, an apricot or cream Doodle, a red or black-and-tan
  Dachshund, a black-and-tan German Shepherd).
- Download the largest size offered (at least 1600 px on the short side). Save it as
  `photos/<dog>.jpg`, and record photographer, page URL and licence in `credits.json`.
- Never a generated dog, and never a photo of a person's identifiable pet from social media.

## 3. The painting

- Your built-in OpenAI image generation, as an edit with the photo as the input image, the full
  prompt file text as the prompt (unchanged, nothing added), at the job's exact `size`, at the
  highest quality. If built-in generation is unavailable, stop and report. Do not call any API with
  a key, and do not use any other provider.
- One generation per painting. Save it untouched as `paintings/<id>.png`. If it came back another
  shape, crop around the dog to `size`; never pad.
- Before moving on, look at it and write in your report: is it the photo's dog (face, ears, coat,
  markings)? Is the whole image in the named medium? Any letters, extra props, a second dog, extra
  limbs or a distorted eye? Does the mood read as the job's tone? You may not regenerate; report.

## 4. Cutouts and crops

- `cutouts/<id>.png`: background removal on the painting (rembg with `isnet-general-use`, or
  similar), then clean the edge: no halo, no bitten ears or tail, fur edges kept soft. Same size as
  the painting, transparent background.
- `crops/<id>-<ratio>.png`: place the painting on the ratio's canvas at one uniform scale, the dog's
  face inside the middle 80%, then extend only the empty area by an image edit with a mask that
  protects every pixel of the original painting. Never scale non-uniformly, and never let the edit
  touch the dog.

## 5. Mockups: the hard part

The look to hit: an unretouched-looking product photograph a premium gift shop would publish. At
phone size nobody should be able to tell the art was placed by code.

- **The base plate.** Generate the scene with the product blank: an empty frame with a plain white
  mat area (portrait), or a plain cream sherpa blanket (blanket). Match the real product on its live
  store page: a thin simple frame for the 12 x 18 portrait, a 50 x 60 inch sherpa that reads as
  fleece. One base plate per scene, three scenes per painting, so at most three generations per job.
- **The composite, by code, never by a model.** Find the print area's four corners (portrait) or the
  visible blanket surface (blanket). Warp the master painting into it with a perspective transform
  (portrait) or a perspective transform plus a gentle displacement map from the plate's folds
  (blanket). Then carry the plate's real light onto the art: multiply a blurred luminance of the
  blank print area over the art at 60 to 85 percent, and keep the frame's edge shadow on top. The
  painting's pixels are otherwise unchanged: no repainting, no style transfer, no model edit over it.
- **Scenes and tone.** Studio: the product alone on soft cream, even light. Home: a lived-in US home
  in the tone's light (Sentimental: quiet morning light; Warm: a cheerful kitchen or sofa;
  Hilarious: bright and playful; Over the top: velvet, gold light or a spotlight). In hand: the
  portrait being hung on a wall by two hands, or the blanket over a sofa arm. Hands only: five
  natural fingers each, no faces, no rings or tattoos that draw the eye.
- **Ratios.** Each scene at 1:1, 4:5 and 9:16, made from the one composite by crop or by a masked
  background extension, never by a new generation.
- **Your own reject check before saving each scene.** Straight, square frame corners; the art sits
  inside the frame, not over it; the mat and the reserved note area plain; no wrong shadows, no
  melted fingers, no warped dog, no text. If a scene fails it, record it as failed with the reason.

## 6. The review sheet, the manifest, the check

- `contact/<id>.jpg`: one sheet per job showing the photo, the painting, the cutout on grey, the
  three crops and the nine mockups, each labelled with its file name in the sheet's margin (labels
  in the sheet only, never on an asset).
- `manifest.json` exactly as heartside's brief says, one entry per file except photos and sheets.
- `python3 growth.py examples check --stage 1` (or `--only <id>` for the pilot) after each step and
  before each commit. It must end `ready for review`. A failed file goes in `failures.json` as
  `{"<path>": "<reason>"}`; leaving a file out without that is an error. Do not write `review.md`:
  a person writes it.

## 7. Report (after the pilot, and again at the end)

- the branch and the commit, and the check's last line;
- per job: painting, cutout, crops, scenes, each done or failed with the reason;
- your section 3 answers for each painting, and anything in section 5 you were not happy with;
- the number of image generations you made, by kind (paintings, base plates, extensions);
- the photo credits, one line per dog.

## 8. Never

- push to `main`, touch heartside, or edit anything outside `assets/heartside-examples-2026-10-29/`;
- generate a stage-2 job, a set, a retry or any extra item;
- use a generated dog as the reference photo, or a photo with people, text or a watermark;
- add words, letters, logos, watermarks or signatures to any asset;
- add a prop, costume or accessory the job's `brief` does not name, another dog, or a face;
- install anything beyond Pillow, NumPy, OpenCV and a background-removal package such as rembg;
- post, upload, share or send anything anywhere.

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
