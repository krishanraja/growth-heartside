---
name: heartside-higgsfield-ui
description: The Higgsfield rules for Heartside generation - Unlimited models in the website through Codex first, Krish's Chrome when Codex's browser fails, the MCP on credits only inside a cap Krish names; model URLs and settings that keep a job Unlimited; MCP prices; downloads; prompts the generator skill's way. Use before writing any Higgsfield order or touching the Higgsfield MCP.
---

# Higgsfield on Krish's Unlimited plans

The rules live on the floor: `higgsfield-browser-ui-only`, `read-unlimited-before-ordering`,
`higgsfield-generator-method`, `chrome-or-machine-for-higgsfield` and `mcp-credit-route-with-cap`. This skill turns
them into steps.

## The routes, in order

| Route | Use it for | Never for |
|---|---|---|
| 1. The website, clicked by Codex in Krish's attached browser (`heartside-codex-studio`) | every Unlimited generation | n/a |
| 2. The website in Krish's Chrome (Claude in Chrome), when Codex's browser cannot reach Higgsfield | the same Unlimited-only jobs. Read the Generate button's cost before every click | any job whose Generate button shows credits |
| 3. The Higgsfield MCP, generating | only when the Unlimited window has closed or no browser works, on credits, inside a cap Krish names for that run | any run without his cap; any job not quoted first |
| The Higgsfield MCP, reading | `balance`, `show_generations`, `show_generation_by_ids`, cost quotes | n/a |
| The `higgsfield` CLI | nothing in Heartside production | everything: it never sees Unlimited |

Krish's words: "you are to use the browser UI only"; "Okay, you can use the MCP for stuff that doesn't reduce my
credits. As you know, I've got unlimited usage of Kling 3.0 for the next few hours, which can only be used in the UI";
"unlimited usage probably does not apply in the CLI". The generator skill is used for its method (section 5), never
its CLI.

## 1. Read today's Unlimited models first

1. Send Codex a read-only order: list every image and video model that shows the Unlimited label, with the time.
   Click nothing.
2. Build the order only on those models. If the brief names a model that is not Unlimited, re-route to an Unlimited
   one. Never stop to ask, and never buy.
   - Krish, 17 Nov: "its trying to use nano banana instead of bling 3.0 which is unlimited for today - I already told
     you this, why not even bother to look at what is unlimited in my account?"
3. What 17 Nov showed:
   - Images, Unlimited at 14:48 UTC: Nano Banana, Seedream 5.0 lite, Seedream 4.5, Kling O1, FLUX.2 Pro.
   - Nano Banana **Pro** was not Unlimited. Its switch opened a pass dialog at $5, $12 or $23.
   - Video: Kling 3.0 Unlimited for 16 to 17 Nov only. When it lapsed, it offered a $35 one-day pass.
   - Kling 2.5 Turbo Unlimited runs May 2026 to May 2027 (log, 16 Nov preflight).
   - Krish's fallback: "continue with the rest on kling 2.5 after midnight when kling 3.0 expires. or any other model I
     have unlimited usage of".
   - Kling 3.0 Unlimited closed by 02:00Z on 18 Nov. In Chrome it then showed 30 credits a clip at default settings.
   - These change. Read them again every day; never order from this list.

## 2. Model URLs and settings that keep a job Unlimited

- Open the model by its URL, never through the menus: images at `https://higgsfield.ai/ai/image?model=nano_banana`,
  video at `https://higgsfield.ai/ai/video?model=kling3_0`. A narrow tab shows the mobile layout, which hides the
  Unlimited control; the URL fixes it, and failing that, a viewport of at least 1440x900 and a reload.

- The video page opens on a default model (Seedance) and Kling 3.0 opens at 4K and 16:9. Both are paid. Every order
  states: the model, 1080p (or 720p), 9:16, the duration, audio off, enhance off.
- The Generate button must read **Unlimited**. A number on it ("Generate 30", "8.75") means credits: submit nothing.
- One Unlimited job at a time for the whole account. A second click gets the toast "You can generate 1 unlimited video,
  image & audio generation at a time". On 16 Nov only 3 of 20 clicks were accepted.
- A click is not acceptance. A job counts only when History shows it. If a click is unverified, check History before
  any retry, or the job runs twice.
- Krish's other ventures share the account and its slot. Their jobs in History are not yours. Ignore them and never
  ask him to stop them.
- The balance never moves. Read it with the MCP `balance` call before and after the session (952.35 on 17 Nov) and
  log both readings.

### Kling 2.5 Turbo in Krish's Chrome (18 Nov, the free fallback)

Kling 3.0's Unlimited switch ran one more free job on the morning of 18 Nov (the bedroom clip, about 07:30Z), then
opened the pass dialog ($35 a day) on every try. Kling 2.5 Turbo stayed Unlimited. The steps that worked, every clip:
1. Open `https://higgsfield.ai/ai/video?model=kling-v2-5-turbo`. It opens at 1080p pro ("Generate 6"): click
   "Change to std for Unlimited" (720p), turn Enhance off, then turn the Unlimited mode switch on (scroll the left
   panel to see it). The button must read "Generate Unlimited".
2. Remove the old start image first: hover it, click its X at the top right. Only then `find` the "Start frame"
   file input and `file_upload` the anchor to it. Uploading into the "Uploaded image" input while an image is in
   place put the anchor in both the start and end slots; that switches on Start-End mode, which forces 1080p and
   credits. If both slots fill, remove the end frame's X before anything else.
3. Wait 8 seconds after the upload before clicking Generate. A Generate click during the upload froze the page; a
   reload restored the form (anchor and prompt kept) with the Unlimited switch off again.
4. Click Generate by its coordinate, then confirm the job in MCP `show_generations` (`only_completed: false`). A
   click by element ref was twice not taken.
5. Output is 716x1284, 5 s. Takes about 4 to 5 minutes. Identity drifts in the last second more often than
   Kling 3.0 (a collar vanished from 3.6 s to 4.4 s in the kitchen clip): check the last second at full size.

## 3. The MCP credit route (only inside Krish's cap)

Krish, 18 Nov: "why dont you just complete this entire task in higgsfield MCP - how many credits will that take", then
"go with a cap of 150, but make sure you do a small test to ensure the big run will be successful".

1. Quote every job first (`get_cost` or `estimate_video_cost`) and give Krish a table: job, model, credits each,
   count, total. Wait for his cap.
2. Prices quoted on 17 and 18 Nov:
   - Nano Banana: 1 credit.
   - Nano Banana Pro at 2K: 2 credits.
   - GPT Image 2.6: 0.25 credits at low quality, 2.75 at high 2K.
   - Kling 3.0 pro, 1080p, 5 s, no sound: 8.75 credits.
   The MCP cannot use Unlimited (`unlim.available` is false).
3. Test small: one still, check it at full size, then one clip, check it. Only then run the rest.
4. Log every paid job with its credits and a running total against the cap. Read `balance` before and after. The
   account is shared: on 18 Nov 7 credits went that no Heartside job spent, so record only your own jobs, and say so
   when the balance and your log differ.
5. Claude Code's auto-mode check sometimes blocks an MCP `generate_image` or `generate_video` call, with no reason
   given. Never work round it. Tell Krish in one line that he can allow those two tools in his settings, and carry on
   by another route.
6. The best anchor of 17 Nov came this way: Nano Banana Pro 2K, charity set (asset `b4ce2b0a`).

### Music beds (MCP, on credits, inside the cap)

Floor `music-defines-humour`. Krish, 18 Nov: "what music are you adding? this will define the humour score
substantialy".
1. Show Krish each film's music in one line (style, where it stops or switches, why it is funny) and wait for his
   answer before generating or mixing.
2. Original beds: MCP `generate_audio` with model `elevenlabs_music_v2_5`, `force_instrumental: true`,
   `use_unlim: false`. About 2.18 credits per 15 s (14 beds cost 22.01 on 18 Nov). There is no Suno model on this
   account.
3. A bed covers the whole film, end card included. Ask for the film's full length plus 1 s, and end the prompt with
   "with a clean ending". On 18 Nov 5 of 9 beds came back too short and had to be made again.
4. Check each bed's length with `ffprobe` before mixing (`heartside-assembly-panel-board`, section 1).

## 4. Downloading takes (Claude, MCP read plus curl)

1. Get the job: MCP `show_generation_by_ids` with `jobs: [{"index": 0, "job_id": "<asset uuid>"}]`. Or use
   `show_generations` (type video, `only_completed: true`) for the recent list.
2. Download: `curl -s -o <STUDIO>/kling3/<id>_s<shot>_t<take>.mp4 "<results.rawUrl>"`. Stills go to
   `<STUDIO>/stills/` or `<STUDIO>/anchors/`.
3. Log it: `echo "$(date -u +%H:%M:%SZ) | Claude | downloaded <file> (<uuid8>)" >> <STUDIO>/log.md`.
4. Look at it at full size before calling it good (`heartside-dog-realism`).

## 5. Prompts, the generator skill's way

Source: `krishanraja/higgsfield-generator`, `higgsfield-generate/references/prompt-engineering.md`.

- Under about 200 tokens (about 900 characters). Models distort with long prompts.
  - 17 Nov bank prompts were 1,900 to 3,300 characters. They contradicted themselves: one asked for "strong low orange
    late-afternoon sun" and also "pale early daylight through thin curtains".
  - Long prompts live in `<STUDIO>/anchors/prompts-long/`; the short ones that replaced them are in `anchors/prompts/`.
- Phrase it positively: "tack sharp", not "no blur". An "Avoid:" list of 20 items is the wrong shape.
- Image-to-image: say only what changes from the reference ("Now it lies asleep on an unmade bed...").
- Image-to-video: say only the motion and the camera ("The dog wakes, sits up, looks into the lens for a beat, then
  turns away. Handheld, slight drift, no zoom."). Never redescribe the start frame. See `<STUDIO>/bank2/i2v/`, 185 to
  251 characters each.
- Name only what should be in the frame. Nano Banana draws every object you name. "Phone held at the foot of the bed"
  put a phone, and a hand, in both 17 Nov bedroom anchors (`anc-gr` t1 and t2, rejected).
  - Describe the viewpoint ("seen from the foot of the bed", "seen from the dog's height"), never the device.
  - Never write "phone", "camera", "tripod", "charger" or "hand" in any prompt, a motion prompt included: say
    "Handheld, a slight natural drift", never "Handheld phone".
- Count the length: `wc -c <prompt file>`. Over 900 characters is rewritten before it is sent.

## 6. Facts for planning

- Kling 3.0: 12 to 15 minutes a job on the evening of 17 Nov (7 minutes in the morning). Nano Banana: about 5 minutes.
- Nano Banana outputs 768x1344.
- Kling 3.0 cannot fake one object hitting another: a branch against bridge rails passed straight through the posts
  (18 Nov). Plan shots where only the dog moves things it can really move.
- The Codex in-app browser sometimes cannot attach to the image page while the video page works (17 Nov 15:49). If so,
  run the shot as Kling text-to-video, or wait for Krish to reattach.

## Never

- Never generate through the MCP without Krish's cap for that run, and never through the CLI.
- Never turn on an Unlimited switch that opens a purchase dialog, and never buy a pass.
- Never submit while the Generate button shows a number.
- Never retry an unverified click without checking History.
