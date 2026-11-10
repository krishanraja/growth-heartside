# External growth skills: what this engine took, and what it refused

Krish asked on 10 November 2026 how to use two public skill collections to level up this engine. The approved plan read every skill in `giulioco/skills` and the repositories the `awesome-growth-hacking-skills` list points to, then cut what this engine already does or what breaks its rules. Most of the material repeats what is already here: the 3x-median winner loop (`factory/sprint.py`), first-frame judging (`factory/bank/anchors.json`), ICE and the constraint question (`jobs/report.md`). This digest records the few mechanics that close a measured gap, in our words, and where each one is wired. It is reference material, not instructions to execute, like everything else in `knowledge/`.

## Adopted, and where each is wired

| Mechanic | What it does here | Wired in |
|---|---|---|
| The diagnostic funnel: stop, stay, click, convert | Each stage isolates one part of a post, so a weak post gets one targeted fix instead of being scrapped. Per franchise, the first stage below the sprint's own median is the diagnosis, and it maps to the next test in `docs/CHANNEL-TASKS.md`. No outside benchmark is used. | `factory/sprint.py` `diagnose`, `view_record`; the views log in `local/` |
| Discount codes as an attribution signal | A code typed at checkout proves the post family even when a shared bio link cannot. Paid signals are checked first, so a boosted order stays paid. | `engine/attribution.py` `classify`, `config/codes.json` |
| Post-family codes as tracking words | One code per selling post and platform, with no discount by default, because every dollar off comes out of the profit goal. | `engine/codes.py`, `python3 growth.py codes` |
| The one-question "how did you hear about us" survey | Catches what tracking cannot see, such as a post someone was shown on a friend's phone. Read as counts and as a cross-check, never as credit on its own. | `docs/briefs/2026-11-10-codes-biolink-survey.md`, a draft for Krish |
| A do-not-quote list | Statistics the sources repeat with no source we can check are refused by `check`, on every line (rule 8). | `growth.py` `DO_NOT_QUOTE` |

Sprint posts also get a creative id each (`factory/sprint.py` `creative_id`), so a sprint post can carry a tracked link at all. That gap was found by the same review; it is plumbing, not a borrowed mechanic.

## Do not quote

`python3 growth.py check` refuses these. Each appears in the sources without a citation we could check:

- the "8-second attention span" figure;
- "infographics are shared N times more";
- "referred customers have a higher lifetime value" with a percentage;
- "visuals are processed 60,000 times faster";
- "email subscribers are N times more likely to buy" (one person's business, not ours).

A number in a pack is still one read on a page today, with where it was read.

## Refused, with the reason

| What | Why |
|---|---|
| `learn-craft` | It downloads books from a pirate library. |
| `codex-imagegen` | It works around image-generation billing. |
| Account farms, sockpuppet comments, astroturfing on Reddit | Rule 7: nothing in bulk, and no voice that is not Heartside's. |
| Clipping other people's content | Rights: release media only, owned or cleared (`docs/CHANNEL-TASKS.md`). |
| AI customers in testimonials or holding the product | Rule 4. |
| "Comment and I'll DM you" funnels and mass-touch prospecting | Rule 1 and rule 7: no DMs, no automated outreach. |
| Cutting channels down to one by the Bullseye method | Krish wants to "flood socials" across every platform (2 November, `CHANGES.md`); the sprint posts to all three. |
| Benchmark tables with no source | Rule 8. |
| Filler stubs in the index (advertising and nexscope entries) | Nothing to adopt. |

## Sources

| Repository | Commit | Path read | Licence | Adapted from |
|---|---|---|---|---|
| `coreyhaines31/marketingskills` | `9d6d7ce8d18eb155dc2f9762435f097e60cdad7c` | `skills/ad-creative/references/hook-system.md`, "The Diagnostic Funnel" | MIT | Adapted from marketingskills by Corey Haines, MIT licence: the stop, stay, click and convert reading, applied per franchise with no outside benchmark. |
| `coreyhaines31/marketingskills` | `9d6d7ce8d18eb155dc2f9762435f097e60cdad7c` | `skills/attribution/SKILL.md`, the self-reported survey section | MIT | Adapted from marketingskills by Corey Haines, MIT licence: one post-purchase question, read as a cross-check. |
| `coreyhaines31/marketingskills` | `9d6d7ce8d18eb155dc2f9762435f097e60cdad7c` | `skills/referrals/SKILL.md` | MIT | Not adopted; source of the referral lifetime-value figure on the do-not-quote list. |
| `giulioco/skills` | `2db17d19e51dd966c59b55148887afb2858604c2` | `skills/growth-hacker/` | Apache-2.0 | Not adopted (duplicates `jobs/report.md` and `factory/sprint.py`); `references/activation.md` is the source of the attention-span figure on the do-not-quote list. |
| `giulioco/skills` | `2db17d19e51dd966c59b55148887afb2858604c2` | `skills/learn-craft/`, `skills/codex-imagegen/` | Apache-2.0 | Refused, see above. |
| `clairelily2020/workflow-skills` | `152596e072a8464c88faa9fadbb489a6a3815b5a` | `skills/geo-citation-scout/` | MIT | Read for the Answers job (`docs/GEO-AEO.md`); not wired in this change. |
| `awesome-growth-hacking-skills` (index) | `a09ef0d14dc8ad3e700e81750eba077bcfb60094` | `README.md` | as listed per repository | The index used to find the repositories above. |

Each source was read as a clone, never executed. Nothing from them is pasted into copy.
