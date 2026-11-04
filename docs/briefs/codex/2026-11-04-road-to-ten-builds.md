# Codex card: rebuild the posts toward 10 on the home machine

Written 4 Nov 2026 by the growth engine. The plan is `docs/plans/2026-11-04-road-to-ten.md`.

## Hard lines

- **Build only.** Never post, schedule, or touch Buffer.
- **Send every build back as a `review-` file** (`review-reel`, `review-cover`), and never under a plain name. A file becomes the locked version only after Krish says "lock".
- **Never build with a `proposed` line except with `--preview`.** A preview is for Krish to judge, never for posting.

## Steps

1. **Get the branch.** Run `git pull` on `claude/runway-motion-batch`, then `python3 growth.py --self-test`.
2. **Put the nine corrected frames in `$HEARTSIDE_ASSETS/frames/`.** Download each one and check its sha256 before using it.

   | File | URL (Higgsfield CDN) | sha256 |
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

3. **Build F11 now** with `python3 factory/build.py factory/specs/F11.json --preview`. Its lines are approved; `--preview` is needed only because the spec drifts from its old lock. Check that frame 1 is mid-typing and that the last query reads whole.
4. **Build F10 and F06-lab when Krish approves their lines.** F10 should open with three messages and run about 28.7 s.
5. **Rebuild the film masters with captions at y 1300:** F01, F02, F03, F05, F12 (`python3 factory/build.py factory/specs/<id>.json --preview`). Then:
   - F01, F02, F03: lay the locked motion back on with `python3 factory/splice.py <master> <out> factory/motion/<id>.json`. Its default caption is now 1300.
   - F05, F12: lay your own motion clips back on with `cap_y` 1300.
6. **F06-frenchie:** look at 5.8 s for a sliver of a human arm at the right edge. Report what you find; fix only that frame.
7. **Check every build** with `python3 factory/audit.py <folder>` and `python3 factory/lock.py media <spec> <mp4>`. Send each as `review-reel` / `review-cover` through `factory/send_library.py`, and report each file's sha256.
