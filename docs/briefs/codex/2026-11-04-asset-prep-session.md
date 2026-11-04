# Codex asset-prep session: finish the Heartside road to 10

Paste everything below the line into a fresh Codex session. It assumes no earlier context.

---

You are preparing social video assets for **Heartside** (heartside.io), Krish Raja's store of personalised gifts from your dog. This session prepares the assets: it builds, checks, files and hands off. A separate Codex thread does the scheduling and posting:

codex://threads/01a1a23e-de37-74f1-95a8-4a9bed2e756d

Your job is not finished until:
- every asset below is built, checked, locked by Krish and filed to Drive;
- the repository records all of it;
- the scheduling thread has its handoff message.

## 0. Where everything is

- **Repository:** `https://github.com/krishanraja/growth-heartside` (public), branch **`claude/runway-motion-batch`**. Work only on this branch; never on `main`.
  ```
  git clone https://github.com/krishanraja/growth-heartside.git   # skip if it is already on this machine
  cd growth-heartside
  git fetch origin claude/runway-motion-batch
  git checkout claude/runway-motion-batch
  git pull --ff-only
  python3 growth.py --self-test        # must print "self-test passed"
  ```
- **Read these, in this order, before touching anything:**
  1. `AGENTS.md`, all of it. It holds the rules: "you draft, Krish acts", the copy rules, no customer data, and concept-level approval.
  2. `docs/DRIVE-MAP.md`: what lives where in Drive, and who may write it. This is strict.
  3. `factory/README.md`: how a post is built, checked and locked.
  4. `docs/plans/2026-11-04-road-to-ten.md`: what was fixed today and what is still open.
  5. `docs/briefs/codex/2026-11-04-road-to-ten-builds.md`: the build card. This prompt replaces its order of work, but use it for detail.
  6. `docs/audits/2026-11-04-creative-audit.md`: the 10/10 bar every asset is judged against.
- **Assets folder.** Everything is on this machine, in the folder named by the `HEARTSIDE_ASSETS` environment variable. It holds `renders/`, `frames/`, `audio/` and `fonts/`; the music and voices are licensed and never go into git. It is the folder used to build the F04, F05 and F12 motion masters on 3 and 4 Nov.
  - If `HEARTSIDE_ASSETS` is unset, find that folder. If you cannot, stop and ask Krish for its path. Never rebuild with substitute music, voices or renders.
- **Output folder:** `HEARTSIDE_OUT`. If it is unset, the default is `local/media/factory`. `local/` is gitignored.
- **The Drive library** is `Heartside/05_Social-Library/Posts/<post id>/`. Only the library lane writes there:
  ```
  python3 factory/send_library.py <folder with media + manifest.json>
  ```
  - The lane needs the engine key. It reads `ENGINE_OPERATOR_TOKEN`, then `MINDMAKE_ENGINE_TOKEN`, then Windows Credential Manager `Mindmake/engine-operator-token`. Never print the key.
  - Krish's always-on computer writes each sent file into Drive within about 10 to 20 minutes.
  - Never upload into Drive by hand or through a Drive connector.

## 1. Hard rules for this session

1. **Never post, schedule or publish.** Never touch Buffer, Meta, TikTok or Instagram. That is the scheduling thread's job.
2. **Krish's words lock an asset, and only his words.** Show him each finished build and wait for his reply in this session. Never treat silence, an earlier approval or your own judgment as a lock.
3. **Before his lock, a build goes to Drive only as `review-reel` / `review-cover`.** After his lock, send it again under its plain name (`reel`, `cover`, `slideN`); the home computer replaces the earlier file in place. File names are `heartside_<id>_<slug>_<kind>.<ext>`. Slugs:

   | Id | Slug |
   |---|---|
   | F01 | becoming-the-mug |
   | F02 | project-nothing |
   | F03 | operation-stocking |
   | F05 | court-of-the-couch |
   | F10 | group-chat |
   | F11 | search-history |
   | F12 | head-of-security |
4. **Every word on screen comes from `factory/bank/lines.json`, with status `approved`.** Never invent or edit a line. If a line seems to need changing, propose it to Krish; never fix it yourself.
5. **The product on screen is always the store's real render, pixels unaltered.** No AI customers. No badges, no prices, no URLs and no calls to action on screen in organic posts. If a build shows "Make yours at Heartside.io", it is wrong.
6. **Run every check below before you show Krish anything.** If a check fails, fix it or report it plainly. Never show a failing file as ready.
7. **Commit only on `claude/runway-motion-batch`**, with Krish's words in the commit body as `Ruling (Krish, YYYY-MM-DD): ...`. End each commit with:
   ```
   Co-Authored-By: Codex <noreply@openai.com>
   ```

## 2. Where things stand (4 Nov, end of day)

**Locked and filed in Drive.** Each file was read back from the library and matched its sha256. `library/manifest.json` lists each one with its sha256:
- F03 (with three meme labels);
- F04;
- F05;
- F06-dachshund (reel, cover, slides 1 to 4, recast to a chestnut dog that matches its mug);
- F06-lab (reel, slides 3 and 4);
- F06-frenchie;
- F07;
- F12;
- F01 and F02 (motion versions).

**The Buffer queue** (the scheduling thread owns it):
- 20 posts for 5 to 8 Nov were moved onto the locked files through permanent links and read back.
- F02 and F06-frenchie were already on their locked files.
- The old F10 cut's three 8 Nov posts are drafts and must not publish.

**What is left for this session:**

| # | Asset | State | What you do |
|---|---|---|---|
| A | **F10 group chat** | Spec ready (`factory/specs/F10.json`): opens with 3 messages on frame 1, no "WTF", no "mate", about 28.7 s. All its lines are approved (F10.c15b, c18b, c28b) | Build it, check it, get Krish's lock, file it |
| B | **F11 search history** | A new cut is in Drive as `heartside_F11_search-history_review-reel.mp4` (sha256 `8cc6079f38acfbfa22113205155701eccba754dc038db19278580b052053664d`). It opens on the first joke, and the last query shows whole | Rebuild it properly from the spec (`open_on_result`), check it, get the lock, file it |
| C | **Captions at y 1300** for F01, F02, F03, F05, F12 | The factory's default caption moved from y 1440 to 1300, clear of the Reels and TikTok caption zone. The locked masters still have 1440 | Rebuild each master, lay the locked motion back on, check, lock, file |
| D | **F06-frenchie at 5.8 s** | The audit saw a possible sliver of a human arm at the right edge | Look. Report what you find. Fix only that frame, and only if needed |
| E | **Nine corrected frames** | Made 4 Nov with Higgsfield (text removed, coat recast, room matched) | Put them in `$HEARTSIDE_ASSETS/frames/` so the specs build |

## 3. The work, in order

### Step 1: put the nine corrected frames in place

Download each frame into `$HEARTSIDE_ASSETS/frames/` and check its sha256. Any mismatch: stop and report it.

| File | URL | sha256 |
|---|---|---|
| t610c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_161651_05719601-fcae-47a0-a218-2e5211401614.png | cc9607f9fb1925eccf26215d2df99dbaeff99197f9219c5ff0a5c015e63fdd96 |
| t611c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_161651_5f0ebde6-d6b5-454c-b656-3b127fcbb7c1.png | 4b2afb0aa61d8142205c8cf8237378b88f89574e251d3a628fcb4dd26591a70c |
| t612c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_161652_2f277540-06c1-4f6b-aeca-882a669abaf2.png | 07c327191e99a3fa41ece0078d1e7d36f12032a4f696b9b25dd8dee80ee36267 |
| t613c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_161653_8974ec60-b7b0-4016-9398-a7a63deb129e.png | edd7ff78d7f3e9a8c25cac3cbb43b2c0f4038adef316f386beb48f38ecd39273 |
| f422c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_161653_b7ef5ba8-85d2-4e9b-b8dd-1c90983fd1bf.png | b43003494cdb29999089fe0af2c76e48e234a20f014792203ef212c2e20dfa7c |
| f420c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_161652_72e33b86-7119-4ce8-83e9-e7655c65f68a.png | 19cb8deb17654d59990716a0c5a176021bba8306e84c98a9b0897a3cc963958f |
| t622c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_162231_0e02d49d-9d03-4734-a26c-f424065054ee.png | 7ea92020c398050ce20a5b46f73c69f8d17e7b1aaff1dad5250e081c0d2f4758 |
| t623c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_162232_1efbadc3-2944-4f44-94e7-075766c86ffe.png | 5f30a3a756ed6776841e6a939d10535749f5ef530ccdf9d35f8753bf179f9ce5 |
| f701c.png | https://d8j0ntlcm91z4.cloudfront.net/user_3EHoG5PVkilXbvUobkwyA3pk0A2/hf_20261104_162234_beeadafe-e3eb-4d07-b6f7-3140606cb16a.png | d1c5a72179f271acaa42165a81f81ba9a537989ce461621432c91c1b0d9bbd37 |

Then run `python3 factory/lock.py check factory/specs/<id>.json` for F04, F06-dachshund, F06-lab, F07, F10 and F11. The only acceptable hold is "drift: this post no longer matches lock …" for F10 and F11. Those two get relocked in step 5. Any other hold means you stop and fix it before going on.

### Step 2: build F10 (A) first; it is the one blocking the queue

```
python3 factory/build.py --preview factory/specs/F10.json
python3 factory/audit.py <out folder>
python3 factory/lock.py media factory/specs/F10.json <mp4>
```

Check F10 frame by frame, at 0, 0.5, 1, 1.5 s and then every 2 s, plus the last frame:
- frame 1 shows three messages; nothing is blank;
- no "WTF", no "mate", no exclamation marks, no em dashes;
- every bubble is inside the screen, with nothing clipped;
- the render bubble shows the real dachshund portrait;
- the end card is the four real mugs, held for at least 3 s;
- it lasts 27 to 30 s, at 1080x1920 with sound, between -18 and -13 LUFS.

### Step 3: build F11 (B)

`python3 factory/build.py --preview factory/specs/F11.json`. The spec has `open_on_result: true`.

Check it:
- frame 1 shows "how to say I love you without thumbs" with its answer "sit on their foot (works every time)";
- the last query, "put my own face on a mug: weird or genius", shows whole, not cut off at the start;
- it ends on the real dachshund mug.

`factory/audit.py` may flag the first frame as blank, because the search screen is mostly pale paper. If it does:
- confirm by eye that frame 1 shows the query and its answer;
- write that note when you show Krish.

### Step 4: rebuild the caption-safe masters (C)

For each of F01, F02, F03, F05 and F12:

1. Rebuild the master: `python3 factory/build.py --preview factory/specs/<id>.json`. Captions now sit at y 1300 (F01's p4 line also moved there).
2. Lay the locked motion back on:
   - **F01, F02, F03:** run `python3 factory/splice.py <master> <out> factory/motion/<id>.json`. Its default caption is 1300. For F03, then apply `factory/motion/F03-labels.json`: replace `MASTER` in that file with the path of the output you just made, run `factory/splice.py` again, and keep the three labels "Operation Stocking", "The beagle:" and "The gift:".
   - **F05, F12:** you built their motion versions on 4 Nov. Re-apply your own motion clips at `cap_y` 1300. Keep the end card from the locked master, with no on-screen "Make yours at Heartside.io".
3. Compare each new file with its locked file in Drive (sha256 in `library/manifest.json`), frame by frame:
   - only the caption position may differ;
   - the timing, voice, music, shots and end card must be identical.
4. Run `factory/audit.py` and `factory/lock.py media`.

### Step 5: show Krish and get his lock

1. Send every passing build to Drive as a review file:
   - make a folder holding the files, named `heartside_<id>_<slug>_review-reel.mp4`;
   - add `manifest.json` (`[{"post","file","bytes","sha256"}]`);
   - run `python3 factory/send_library.py <folder> --dry-run`, then the same command without `--dry-run`.
2. Show Krish in this session, one line per file: what changed, its score against the audit bar, and anything that is not perfect. Ask for "lock" (all), or the ones he names.
3. For each asset he locks:
   - run `python3 factory/lock.py lock factory/specs/<id>.json --by "<his exact words, with the date>"`. If the lock refuses only because of asset paths, write the lock file the same way `factory/locks/F03.json` was written, with a note;
   - send it again under its plain name (`heartside_<id>_<slug>_reel.mp4`) through the lane;
   - wait for the lane to report it ready;
   - read it back with `GET https://content-engine-flame-nu.vercel.app/api/library/file?library=heartside&path=Posts/<id>/<file>` (header `Authorization: Bearer <engine key>`), download the signed URL, and confirm the sha256 matches.
4. Update the records:
   - `library/manifest.json`: add each new locked file (status `locked`, its sha256, `lock_fingerprint`, an audit note), and mark the file it replaces `superseded 2026-11-0X by …`;
   - `CHANGES.md`: one entry with his words.
5. For anything he declines, record his words in `CHANGES.md`, report them to the taste engine if you have it, and fix it or stop. Never lock it anyway.

### Step 6: F06-frenchie at 5.8 s (D)

Look at the locked F06-frenchie reel at 5.6 to 6.0 s.
- If a human arm or hand is visible, show Krish the frame and propose the smallest fix. Do nothing until he says so.
- If it is clean, record "checked clean" in `docs/plans/2026-11-04-road-to-ten.md`.

### Step 7: commit, push, close out

1. `python3 growth.py --self-test` must pass.
2. Write `now-notes/2026-11-0X-asset-prep.md` with exactly these lines: `Status:`, `Changed:`, `Next:`, and `North Star check (date): holds.`
3. Commit on `claude/runway-motion-batch` with his `Ruling (Krish, …)` lines, then `git push -u origin claude/runway-motion-batch`.

## 4. Hand off to the scheduling thread (required, and do it as soon as F10 is locked)

Krish wants the schedule prepared as soon as possible.

- **The moment F10 is locked and filed, send this message** to `codex://threads/01a1a23e-de37-74f1-95a8-4a9bed2e756d`. Don't wait for the rest; the scheduling thread needs it now.
- **Send it again, updated, when F11 and the caption-safe masters are locked.**
- Fill in every `<…>` placeholder. Send only facts you checked; nothing guessed.

> **From the asset-prep session (Heartside), <date and time UTC>. Prepare the schedule now: Krish wants it ASAP.**
>
> Repository `krishanraja/growth-heartside`, branch `claude/runway-motion-batch`. Read `AGENTS.md`, `docs/DRIVE-MAP.md`, `docs/CHANNEL-TASKS.md` and `docs/plans/2026-11-04-road-to-ten.md` before acting.
>
> **Newly locked and in Drive** (`Heartside/05_Social-Library/Posts/<id>/`), each read back from the library:
>
> | Post | File | sha256 | Locked by Krish (his words, date) |
> |---|---|---|---|
> | F10 | heartside_F10_group-chat_reel.mp4 | <sha256> | "<words>" <date> |
> | <F11 and the others, as each is locked> | | | |
>
> **What to do in Buffer** (organisation `6adcc9a718f8902ff84c01d5`):
>
> 1. **F10.** The old cut's three posts are drafts and must stay off the feed until they carry the new file:
>    - TikTok `6aeae9142b43f8ba7d7c9a61`;
>    - Instagram `6aeae915e478396c274e533c`;
>    - Facebook `6aeae915d59713e43431a67a`.
>
>    Give each the new F10 file, keep its caption, and schedule it. 8 Nov 17:40, 17:45 and 17:50 UTC are still the planned slots, if they are in the future. Ask Krish to approve the slots in chat before re-queuing.
> 2. **F11.** Its queued posts (TikTok `6aeae904394911f9f1297334`, Instagram `6aeae904dc38f4d7badf16a6`, Facebook `6aeae904e478396c274e3712`; 5 Nov 14:15 to 14:25 UTC) carry the old locked cut. Once F11's new cut is locked, swap the media on all three. If they have already published, leave them.
> 3. **The caption-safe masters** (F01, F02, F03, F05, F12), once locked. For any of their posts still queued, swap the media. For posts already live, do nothing.
> 4. **Hosting rule.** Point Buffer only at a permanent public URL that serves the exact locked bytes. Before each edit, download that URL and check its sha256 matches. After each edit, read the post back: still scheduled, same caption and time, new file and length, and a thumbnail that renders.
>    - Never use the library's signed links. They expire after an hour, and that broke the F03 swap on 4 Nov.
>    - On 4 Nov the engine used Higgsfield's CDN (`d2ol7oe51mr4n9.cloudfront.net`). Buffer's own upload also works.
>    - Test one post first, then do the rest. Stop at the first problem and tell Krish.
> 5. **One risk to fix before it bites.** F02's posts (TikTok `6aeae907c63bd995bd1ee736`, Instagram `6aeae908394911f9f1297f10`; 5 Nov 20:10 and 20:15 UTC) point at the review server `heartside-review.5-161-56-37.sslip.io`. If that server is down at publish time, they fail. Move them to permanent hosting of the same locked file (sha256 `b06916ceebb692120549f21879…` in `library/manifest.json`), checked as in point 4.
> 6. **New schedule rows.**
>    - Follow `docs/DRIVE-MAP.md` rule 5. Only Krish marks `approved`, or says it in chat; record that as "Approved in chat <date>" in `notes`. A row with neither is never posted.
>    - If a new `02<letter>` Sheet is needed, confirm with Krish first: the map says the growth engine creates Sheets, and Krish asked this thread to prepare the schedule. Name the conflict rather than picking one.
> 7. **Boost test.** F12 (6 Nov) and F05 (8 Nov) are arms of the paid boost test (`docs/PAID-BOOSTS.md`, `docs/boost/2026-11-launch-packet.md`). Their queued posts now carry the locked motion versions. Don't change their captions or times without Krish.
>
> Report back to Krish: each post's id, new due time, the media sha256 you checked, and the readback result.

## 5. Done means all of these are true

- [ ] Nine frames in place, each sha256 checked.
- [ ] F10 built, checked, locked by Krish's words, filed under its plain name, and read back.
- [ ] F11 the same.
- [ ] F01, F02, F03, F05 and F12 caption-safe versions the same, or Krish declined each one in words, with those words recorded.
- [ ] F06-frenchie at 5.8 s checked, and recorded or fixed with his approval.
- [ ] `library/manifest.json`, `factory/locks/`, `CHANGES.md` and a now-note updated; self-test passes; committed and pushed to `claude/runway-motion-batch`.
- [ ] The handoff message sent to `codex://threads/01a1a23e-de37-74f1-95a8-4a9bed2e756d`, first as soon as F10 was locked, then updated with every later lock.
- [ ] Your final message to Krish lists each asset with its state (locked and filed, or declined), its sha256, and when the scheduling thread was told.

If anything blocks you (assets folder missing, lane refusing, a check you cannot pass), stop at that step. Tell Krish exactly what blocked you and what you need. Then carry on with every step that does not depend on it.
