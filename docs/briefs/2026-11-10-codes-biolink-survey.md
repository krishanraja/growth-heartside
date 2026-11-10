# Codes, bio link and thank-you survey: drafts for Krish to switch on

Status: draft, nothing switched on. R-3 (`docs/briefs/2026-10-27-architecture.md`, 27 Oct) approved that the engine
**drafts** creator codes, post-family codes, a thank-you survey and per-post bio links, and that Krish switches each
one on. This is that draft for the sprint (`factory/sprints/2026-11-S120.json`). The engine creates no code, changes
no store setting and installs nothing (rules 1 and 9).

**North Star part it moves:** the number itself. Today a sprint sale cannot be counted: a shared bio link carries no
post, and until this change a sprint post could not carry a tracked link. With codes registered, an order that types
a post's code lands in the engine tier under that post's family. The number is unchanged until codes are live and
orders use them.

## 1. Post-family codes

- **What:** one code per selling slot and platform, a tracking word with **no discount**. Every dollar off comes out
  of the profit goal, so a discount is a separate decision for Krish, never a default.
- **Which slots:** intent `buy` and the signature lane only. A standalone joke never carries a code line
  (`docs/CHANNEL-TASKS.md`: no product slide, hashtag or shop link on an approved standalone joke).
- **The list:** `python3 growth.py codes` prints every draft: slot, platform, code, family and creative id. For the
  sprint that is 60 drafts, 20 signature slots on three platforms. Example: S01 on Instagram is `PRESS301I`, family
  `IG_EMO_C301`.
- **Switching one on (Krish):**
  1. In Shopify admin, Discounts, create the code exactly as printed. With no discount wanted, the store's own
     options decide how a zero-value code is made; if Shopify will not take one, tell the engine and it drafts the
     smallest alternative for your yes.
  2. Add its line to `config/codes.json` under `families`, for example `"PRESS301I": "IG_EMO_C301"`, in an
     interactive session. From that commit on, `engine/attribution.py` counts an order using it in the engine tier.
     Paid signals are still checked first, so a boosted order stays paid.
- **Where the code is said:** a caption or on-screen line on the selling post only, in Heartside's voice and through
  `growth.py check`. The words are drafted with the post, not here.

## 2. The bio-link landing (a brief for a heartside build session)

The store is heartside's; this repository never changes it (rule 9). A heartside session would build:

- one landing page for the profile link that lists the posts now live, newest first, each with its picture and the
  real product it ends on, linking to that product with the post's tracked link (`python3 growth.py link <url> <slot>`
  gives it);
- no badge, no invented proof and no price that is not the live store's;
- the page reads the post list from a file the engine can produce, so adding a post needs no store change.

**Blocker: TikTok has no clickable website on the profile** (Codex's 3 Nov audit, `docs/plans/2026-11-04-road-to-posting.md`).
Until the profile shows one, a TikTok viewer has nowhere to tap, so on TikTok the **code is the only signal** that
can tie a sale to a post. Either drop "Link in bio" from TikTok captions or add the link; that choice is Krish's.

## 3. The one-question thank-you survey

- **Question:** "How did you first hear about Heartside?"
- **Answers:** Instagram; TikTok; Facebook; a friend showed me; search; somewhere else.
- **Where:** the order thank-you page, set up in the heartside session; nothing is installed from here.
- **What the engine keeps:** counts per answer per week, nothing else. No answer is stored next to an order, a
  name, an email or a dog (rule 6).
- **How it is read:** a cross-check on attribution, never credit on its own. People remember the memorable touch,
  not the first one (marketingskills, attribution skill, MIT; `knowledge/corpus/external-growth-skills.md`).

## What Krish decides

1. Switch the codes on, all 60 or the signature posts going live first.
2. Discount or none (the draft says none).
3. Commission the bio-link page and the survey in a heartside session.
4. TikTok: add the website link or drop "Link in bio".
