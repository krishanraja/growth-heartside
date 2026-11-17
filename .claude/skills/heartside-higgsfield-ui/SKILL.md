---
name: heartside-higgsfield-ui
description: The Higgsfield rules for Heartside generation - Unlimited models only, in the website through Codex, never credits; which settings keep a job Unlimited; what the MCP may read; how to download takes; how to write prompts the generator skill's way. Use before writing any Higgsfield order or touching the Higgsfield MCP.
---

# Higgsfield on Krish's Unlimited plans

The rules live on the floor: `higgsfield-browser-ui-only`, `read-unlimited-before-ordering` and
`higgsfield-generator-method`. This skill turns them into steps.

## The three routes, and the only one that generates

| Route | Use it for | Never for |
|---|---|---|
| The website, clicked by Codex in Krish's browser (`heartside-codex-studio`) | every generation | n/a |
| The Higgsfield MCP | reads that never spend credits: `balance`, `show_generations`, `show_generation_by_ids` | generating, upscaling, editing, any paid call |
| The `higgsfield` CLI (`krishanraja/higgsfield-generator`) | nothing in Heartside production | everything: it runs on credits |

Krish's words: "you are to use the browser UI only"; "Okay, you can use the MCP for stuff that doesn't reduce my
credits. As you know, I've got unlimited usage of Kling 3.0 for the next few hours, which can only be used in the UI";
"unlimited usage probably does not apply in the CLI". The generator skill is used for its method (section 4), never
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
   - These change. Read them again every day; never order from this list.

## 2. Settings that keep a job Unlimited

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

## 3. Downloading takes (Claude, MCP read plus curl)

1. Get the job: MCP `show_generation_by_ids` with `jobs: [{"index": 0, "job_id": "<asset uuid>"}]`. Or use
   `show_generations` (type video, `only_completed: true`) for the recent list.
2. Download: `curl -s -o <STUDIO>/kling3/<id>_s<shot>_t<take>.mp4 "<results.rawUrl>"`. Stills go to
   `<STUDIO>/stills/` or `<STUDIO>/anchors/`.
3. Log it: `echo "$(date -u +%H:%M:%SZ) | Claude | downloaded <file> (<uuid8>)" >> <STUDIO>/log.md`.
4. Look at it at full size before calling it good (`heartside-dog-realism`).

## 4. Prompts, the generator skill's way

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
  - Never write "phone", "camera", "tripod" or "charger" in an image prompt.
- Count the length: `wc -c <prompt file>`. Over 900 characters is rewritten before it is sent.

## 5. Facts for planning

- Kling 3.0: 12 to 15 minutes a job on the evening of 17 Nov (7 minutes in the morning). Nano Banana: about 5 minutes.
- Nano Banana outputs 768x1344.
- The Codex in-app browser sometimes cannot attach to the image page while the video page works (17 Nov 15:49). If so,
  run the shot as Kling text-to-video, or wait for Krish to reattach.

## Never

- Never generate, upscale or edit through the MCP or the CLI.
- Never turn on an Unlimited switch that opens a purchase dialog, and never buy a pass.
- Never submit while the Generate button shows a number.
- Never retry an unverified click without checking History.
