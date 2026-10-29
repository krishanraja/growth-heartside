# Breed examples, stage 1: the supervisor's runbook for driving Codex

29 Oct 2026. Krish approved stage 1 only (6 paintings): "go and get codex to build out all the
assets, make sure you micromanage codex properly". He also said this batch "is going to set the tone
for everything". Stage 2 needs a person's review of stage 1 and a new yes from Krish.

**Who does what.** A Claude session (the supervisor) drives Codex with `codex exec`, one prompt per
step, in `~/growth-heartside` on Krish's machine. Codex never sees this file whole: it gets only the
step prompt below, sent verbatim with the `<...>` filled in. After every step the supervisor runs the
checks listed, opens every new image, and sends the next step only when the step passed. A failed
step stops the run and goes to Krish. Generation is never retried without Krish's yes.

**Source.** Heartside commit `eccc695c44d98008d5989bd118089acd762e465f` (branch
`claude/product-launch-readiness-mlh1bc`), folder `design/examples-2026-10-29-breeds/`. Raw files:
`https://raw.githubusercontent.com/krishanraja/heartside/eccc695c44d98008d5989bd118089acd762e465f/<path>`.
Heartside's own brief is at the end of this file, unchanged; this runbook implements it and is
stricter where they differ.

**Order.** The pilot job `golden-sentimental-portrait` runs through steps 1 to 9 and stops for
review. After Krish's "continue", the other five run through steps 3 to 9 one job at a time:
`lab-warm-portrait`, `frenchie-hilarious-portrait`, `doodle-over_the_top-portrait`,
`dachshund-sentimental-blanket`, `shepherd-warm-blanket`.

**Per-job settings.**

| Job | Gift | Frame or blanket | Home scene light (tone) |
|---|---|---|---|
| golden-sentimental-portrait | portrait | red oak frame | quiet early-morning window light |
| lab-warm-portrait | portrait | black frame | a cheerful sunny kitchen |
| frenchie-hilarious-portrait | portrait | white frame | a bright, playful, colourful room |
| doodle-over_the_top-portrait | portrait | black frame | velvet walls, gold light, a spotlight |
| dachshund-sentimental-blanket | blanket | cream sherpa | quiet early-morning window light |
| shepherd-warm-blanket | blanket | cream sherpa | a cheerful sunlit sofa |

All paths below are relative to `assets/heartside-examples-2026-10-29/` unless they start with `~`.

---

## Step 1. Setup (once)

**Send to Codex:**
```
You are in ~/growth-heartside. Do exactly this and nothing else:
1. git fetch origin && git checkout -B codex/heartside-examples-2026-10-29 origin/main
2. . .venv/bin/activate
3. python3 growth.py examples check --stage 1 --only golden-sentimental-portrait
Do not generate, download or edit anything else.
Reply with exactly three lines: the current branch, the commit (git rev-parse --short HEAD),
and the last line the check printed.
```
**Pass when:** the branch is `codex/heartside-examples-2026-10-29`, and the check printed a list of
missing files (not "the job list is wrong").

## Step 2. Can Codex make images here? (once)

**Send to Codex:**
```
Answer only, change nothing: in this environment, can you generate an image and edit an image
(image in, image out, with a text prompt) using your built-in OpenAI image generation, and save
the result as a PNG file at a path I give you? Which sizes can you produce: 1024x1024, 1024x1536,
1536x1024? Reply "yes" or "no" for each of: generate, edit from an input image, save to a path,
each size. Do not test it by generating anything.
```
**Pass when:** yes to edit from an input image, save to a path, and the job's size. If not, stop and
tell Krish; no other provider is used without his yes.

## Step 3. The reference photo (per job)

**Send to Codex:**
```
In ~/growth-heartside, find ONE real photo of a <breed> on unsplash.com or pexels.com.
Rules for the photo: one adult <breed> only; the whole head sharp, eyes and nose in focus; natural
colour and even light; no people or hands; no other animals; no text, logo or watermark; no costume;
prefer a three-quarter view that shows the body. Coat: <coat>.
Look at at least five candidates before choosing. Download the largest size (at least 1600 px on the
short side) to assets/heartside-examples-2026-10-29/photos/<dog>.jpg as a JPEG.
Add to assets/heartside-examples-2026-10-29/credits.json (create it if missing, keep other entries):
"<dog>": {"photographer": "...", "source_url": "<the photo's page URL>", "licence": "Unsplash License" or "Pexels License"}.
Do not generate any image. Do not commit.
Reply with: the page URL, the photographer, the pixel size, and one sentence on why this photo.
```
Coats: golden: golden; lab: black or yellow; frenchie: fawn or brindle; doodle: apricot or cream;
dachshund: red or black and tan, smooth coat; shepherd: black and tan.

**Supervisor checks:** open the photo. One dog of the right breed, sharp head, no people, text or
watermark; open the source URL and confirm the licence. A photo may be replaced (it is not a
generation) if it fails.

## Step 4. The painting (per job, one generation)

**Departure from heartside's brief (29 Oct, Golden pilot).** Heartside's prompt files are not used.
They made the model copy the photo (v1 to v3 on the review branch), and Krish asked for the
generation to be refined, not just accepted. Each job's prompt is its short composed prompt in
`docs/briefs/2026-10-29-heartside-painting-pipeline.md` ("The short prompts for the rest of stage 1";
the Golden used v5). Write it to `/tmp/<id>.txt` exactly as quoted there, without the leading `> `,
and read `size` from `jobs.json`. The findings go to heartside in that same brief.

**Send to Codex:**
```
Make exactly one image, once. Use your built-in image edit with this input image:
assets/heartside-examples-2026-10-29/photos/<dog>.jpg
The prompt is the entire content of the file /tmp/<id>.txt, word for word. Do not shorten it, do not
add anything, do not summarise it. Size <size>. Highest quality.
Save the result untouched as assets/heartside-examples-2026-10-29/paintings/<id>.png (PNG). If it is
not exactly <size>, crop around the dog to <size>; never pad or stretch.
Do not make a second version for any reason. Do not commit.
Reply with: the file path, its pixel size, and "1 generation used".
```
**Supervisor checks** (open the painting next to the photo): the same dog (face, ears, coat colour,
markings); the whole image in the job's medium; no letters, signature, extra dog, extra limb or
distorted eye; only the props in the job's `brief`; the tone reads at a glance; the bottom-right
note area is quiet. If it fails, stop and show Krish; no regeneration without his yes.

## Step 5. The cutout (per job)

**Send to Codex:**
```
Make a cutout of the dog from assets/heartside-examples-2026-10-29/paintings/<id>.png using rembg
with the model "isnet-general-use" (python: from rembg import remove, new_session). Keep the full
resolution and the same pixel size. Clean the edge: no halo, no bitten ears, tail or paws; keep fur
edges soft (a 1 px feather at most). The toy or accessory the dog holds stays with the dog.
Save as assets/heartside-examples-2026-10-29/cutouts/<id>.png (RGBA PNG, transparent background).
Do not generate any image. Do not commit.
Reply with: the path, the size, and the percent of fully transparent pixels.
```
**Supervisor checks:** view on grey and on black: clean edge, nothing of the dog cut off.

## Step 6. The crops (per job)

**Send to Codex:**
```
From assets/heartside-examples-2026-10-29/paintings/<id>.png make three crops:
crops/<id>-1x1.png 1080x1080, crops/<id>-4x5.png 1080x1350, crops/<id>-9x16.png 1080x1920
(all under assets/heartside-examples-2026-10-29/).
For each: scale the painting uniformly (same factor both ways) so the dog's face sits inside the
middle 80% of the canvas, and fill the canvas. Where the painting does not reach the canvas edge,
extend ONLY that empty area with your image edit, using a mask that protects every pixel of the
placed painting, in the painting's own style and light. Never scale non-uniformly, never pad with a
flat colour, never let the edit touch the dog or the painted area.
Do not commit.
Reply with: the three paths and sizes, and how many image edits you used (at most 3).
```
**Supervisor checks:** the dog identical in all three; no visible seam between painting and
extension; the face inside the middle 80%.

## Step 7. Base plates (per job, three generations)

**Send to Codex** (portrait jobs):
```
Generate three photographs, one each, no retries. Each shows a <frame colour> picture frame, thin and
simple, portrait orientation 2:3 (a 12 x 18 inch print), holding a plain, bright, completely blank
white print with nothing on it. Photorealistic, like a premium gift shop's product photo. No text,
logo, people's faces, other frames or artwork anywhere.
1. studio: the frame alone, standing straight-on on a soft cream surface against a soft cream wall,
   even soft light, the whole frame visible with margin. Save base/<id>-studio.png at 1024x1536.
2. home: the frame hanging straight on the wall of a lived-in American home, <home light>, the whole
   frame visible and square to the camera. Save base/<id>-home.png at 1024x1536.
3. hand: two adult hands (no face, no rings, no tattoos, five natural fingers each) hanging the frame
   on a pale wall, the frame square to the camera and fully visible. Save base/<id>-hand.png at 1024x1536.
Save under ~/growth-heartside/local/base/ (not under assets/). Do not commit.
Reply with: the three paths and "3 generations used".
```
**Send to Codex** (blanket jobs):
```
Generate three photographs, one each, no retries. Each shows a plain cream sherpa fleece blanket,
50 x 60 inches, completely blank with no pattern or print. Photorealistic, like a premium gift shop's
product photo. No text, logo, people's faces or other blankets.
1. studio: the blanket laid flat, seen from directly above, on a soft cream background, even soft
   light, the whole blanket visible with margin. Save base/<id>-studio.png at 1024x1024.
2. home: the blanket spread smoothly across the seat and back of a sofa in a lived-in American home,
   <home light>, a large flat area of the blanket facing the camera. Save base/<id>-home.png at 1536x1024.
3. hand: the blanket draped over a sofa arm with a hand smoothing it (no face, no rings, five
   natural fingers), the draped face of the blanket large and facing the camera. Save
   base/<id>-hand.png at 1024x1536.
Save under ~/growth-heartside/local/base/ (not under assets/). Do not commit.
Reply with: the three paths and "3 generations used".
```
**Supervisor checks:** each plate looks like a real photo of the real product (thin frame, true 2:3,
or a real-looking sherpa); straight corners; plausible hands; nothing printed on the product.

## Step 8. The composites (per job, by code only)

**Send to Codex:**
```
Write and run one Python script, tools/compose_<id>.py under ~/growth-heartside/local/ (not in assets),
that places assets/heartside-examples-2026-10-29/paintings/<id>.png onto each base plate in
~/growth-heartside/local/base/<id>-{studio,home,hand}.png. Use only Pillow, NumPy and OpenCV.
Never send the painting to an image model.
For each plate:
1. Find the blank print area: for a frame, the four corners of the white print inside the frame; for
   a blanket, the visible blanket surface. Detect them, then save the points to
   local/base/<id>-<scene>-points.json, and draw them on a debug copy local/base/<id>-<scene>-debug.png.
2. Warp the painting into that area: a perspective transform for a frame; for a blanket, a
   perspective transform plus a gentle displacement map from the plate's own folds (the plate's
   blurred luminance gradient, strength low enough that the dog's face stays undistorted).
3. Carry the plate's light onto the art: multiply a Gaussian-blurred luminance of the blank area
   (normalised to its mean) over the warped art at 70 percent. Keep the frame's inner shadow on top.
   Leave the painting's pixels otherwise unchanged.
4. Save the scene at full size, then make 1080x1080, 1080x1350 and 1080x1920 versions by cropping;
   where a ratio needs more room than the plate has, extend only the surroundings with a masked image
   edit that protects the product and the art. Save as
   assets/heartside-examples-2026-10-29/mockups/<id>/<scene>-1x1.png, -4x5.png, -9x16.png.
Do not commit.
Reply with: the nine paths, any scene where corner detection needed a manual fix, and how many
image edits you used for extensions.
```
**Supervisor checks:** open all nine at phone size and full size. The art sits exactly inside the
frame's opening, not over the frame; straight edges; the light looks native; the note area and mat
plain; the dog undistorted; on blankets, the print follows the fabric without smearing the face.
A failed scene goes into `failures.json` with its reason; it is not redone without Krish's yes.

## Step 9. Sheet, manifest, check, commit (per job)

**Send to Codex:**
```
In ~/growth-heartside:
1. Make assets/heartside-examples-2026-10-29/contact/<id>.jpg: one sheet with the photo, the painting,
   the cutout on grey, the three crops and the nine mockups, each with its file name written in the
   sheet margin (never on an asset).
2. Update assets/heartside-examples-2026-10-29/manifest.json (a JSON list; keep other entries): one
   entry per painting, cutout, crop and mockup file of <id>, each with file (path relative to that
   folder), job "<id>", breed "<breed>", style "<style>", tone "<tone>", gift "<gift>", kind
   (painting, cutout, crop or mockup), scene and ratio where they apply, and uses (painting:
   ["site","ad","social"]; cutout: ["ad","social","character"]; crop and mockup: ["ad","social"]).
3. Any file of <id> that failed: add "<path>": "<reason>" to failures.json (create it if missing).
4. Run: python3 growth.py examples check --stage 1 --only <id>   (for the last job: --stage 1 only)
   It must end with "ready for review". If it does not, fix only what it names, and run it again.
5. git add assets/heartside-examples-2026-10-29 && git commit -m "breed examples: <id>"
   && git push -u origin codex/heartside-examples-2026-10-29
Do not add anything outside assets/heartside-examples-2026-10-29/. Do not write review.md.
Reply with: the commit, and the check's last line.
```
**Supervisor checks:** run the check yourself; open the contact sheet; confirm the commit touches
only `assets/heartside-examples-2026-10-29/`. After the pilot: stop and send Krish the contact sheet,
the generation count and your findings.

## Never (applies to every step)

Push to `main`, touch heartside, edit outside `assets/heartside-examples-2026-10-29/` and `local/`;
generate a stage-2 job, a set, a retry or an extra; use a generated dog as the photo; put words,
logos, watermarks or signatures in an asset; add props the job's brief does not name; post, upload
or send anything anywhere.

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
