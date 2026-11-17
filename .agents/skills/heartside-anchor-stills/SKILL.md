---
name: heartside-anchor-stills
description: How to make the one approved anchor still per set (image-to-image from a reference of the approved dog, Nano Banana Unlimited) and then run every shot of that set image-to-video from it, so a film is one dog in one room. Use before ordering any Heartside footage from Higgsfield.
---

# Anchor stills first, then image-to-video

Floor rule: `higgsfield-generator-method`. Krish, 17 Nov: "surely you should just generate anchor stills that you are
happy with first using codex in 2 min" and "yeah I think you need to use the
https://github.com/krishanraja/higgsfield-generator properly".

Why: the 17 Nov footage bank ran text-to-video from long dog-roll prompts. Every clip re-rolled the dog, the room and
the light. Kling also dropped every coat flaw the prompts listed. An anchor fixes the dog and the room once, and
Krish's eye judges it before any minutes of video are spent.

## Files

```
<STUDIO>/anchors/ref-hero.png        reference of the approved hero dog (a frame Krish passed)
<STUDIO>/anchors/ref-c.png           reference of the approved sidekick C
<STUDIO>/anchors/prompts/anc-<set>.txt    the anchor prompt, under 900 characters
<STUDIO>/anchors/anc-<set>_t<N>.png  each anchor take, downloaded
<STUDIO>/bank2/i2v/b2-<set>-NN.txt   the motion-only prompt for each shot of the set
```

## Step 1: the reference images (once per dog)

1. Use a frame of a dog Krish has already passed (`heartside-dog-realism`, "The cast"). Never a new roll in a timed
   window.
2. Find where that frame already lives in Higgsfield: an earlier upload, or the start image of an earlier job. Write
   its asset id in the order. On 17 Nov:
   - the hero was the start image of the d1-li-01 shot 2 jobs (assets `322e04ec`, `cd6271e4`);
   - C was the start image of the d1-li-04 shot 2 jobs (`d4865d69`, `959ff3a4`).
3. Never order Codex to upload `ref-hero.png` from disk through the website: that opens the file picker on Krish's
   screen (`heartside-codex-studio`, "Never ask Codex to").

## Step 2: write one anchor prompt per set

Each prompt is image-to-image and says only what changes. A template, about 90 words:

```
Keep the dog from reference image 1 exactly: same <coat colour> <coat type> coat, face, markings, build and <collar>.
Now it <what it is doing, one action>, <where: the room and two or three ordinary objects>, lit by <one light>.
Seen from <viewpoint: the foot of the bed | the dog's height | low down on the patio>.
The look of a still from an ordinary home video: soft, slightly grainy fur, a blown-out window, an ordinary
lived-in home, nothing else in the frame. Vertical 9:16.
```

For two dogs, add "and the <sidekick description> from image 2" and attach reference 2.

Before sending, check every prompt:
- [ ] under 900 characters (`wc -c`);
- [ ] one light source only, and no second light line anywhere;
- [ ] no "phone", "camera", "tripod", "charger", "hand" or "person": Nano Banana draws what you name;
- [ ] it never redescribes the dog beyond the "Keep ... exactly" line;
- [ ] it names only the objects you want in the frame.

## Step 3: order the anchors

- Nano Banana with the Unlimited label (not Nano Banana Pro), image page, 9:16, image-to-image. Use the references
  from step 1, by asset id.
- 2 takes per set, one job at a time. Log each as `anc-<set> | t<N> | DONE asset <id> | Nano Banana Unlimited`.
- End the turn when the takes are logged. Do not restart any video queue in the same order.

## Step 4: pick the anchor

1. Download each take (`heartside-higgsfield-ui`, section 3) and open it at full size with the Read tool.
2. Check it against `heartside-dog-realism`, plus:
   - [ ] the same dog as the reference: coat, markings, collar, build;
   - [ ] no object or body part the prompt did not ask for (17 Nov `anc-gr` t1 and t2: a phone and a hand);
   - [ ] the light the prompt asked for (17 Nov `anc-gr` t1: the orange sun never came);
   - [ ] room for the label band (y 330 to 1180 stays clear of the dog's face, `fixed-label-position`).
3. Reject a take with its reason in the log:
   `echo "$(date -u +%H:%M:%SZ) | Claude | anc-<set> t<N> rejected: <reason>" >> <STUDIO>/log.md`.
   Fix the prompt before the redo, not after.
4. Send Krish the best take per set in one image (side by side, `ffmpeg ... hstack`) and wait for his yes on the set.
   He is passing the dog and the room, so he must see them.

## Step 5: every shot of the set runs from the anchor

1. Each shot is Kling (Unlimited) image-to-video with the anchor as its start image. Reuse the anchor's own Higgsfield
   asset; never upload it.
2. The prompt is motion only (`<STUDIO>/bank2/i2v/`): what the dog does, the camera ("Handheld phone, a slight natural
   drift, no zoom"), and "Real dog weight and timing." Under 300 characters.
3. A later shot that must continue the last one starts from that clip's last frame. Extract it with
   `ffmpeg -sseof -0.1 -i <clip> -frames:v 1 <STUDIO>/stills/<id>_s<N>_start.png`, then let Codex reuse it via History,
   not an upload.
4. Every video line in the log names its anchor:
   `b2-<set>-NN | DONE asset <id> | Kling 3.0 Unlimited | from anc-<set>_t<N>`.

## Stop conditions

- No anchor approved for a set: run no video for that set.
- Two anchor rounds fail on the same fault: change the prompt's approach (viewpoint, light, objects). Never send a third
  identical order.
- The image page will not attach in Codex's browser: tell Krish in one line. While you wait, the shots whose anchors
  are approved keep running.

## Never

- Never run a set's shots as text-to-video once the set has an approved anchor. It re-rolls the dog.
- Never paste a 3,000-character dog-roll prompt into an image-to-image or image-to-video job.
- Never let a new dog appear in a set: one film, one dog, one room.
