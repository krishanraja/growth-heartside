---
name: heartside-audience-comments
description: How the Audience desk picks a third-party public dog post and drafts a comment Krish would leave himself, from his verdicts in the 4 to 7 Nov comment pilot. Covers the channel screen, inspecting the actual image, the joke, the three-per-channel cap and checking after posting. Use before drafting any comment on another account's post.
---

# Comments on other accounts' posts

The Audience desk reaches new people by joining conversations on other accounts' public dog posts as
@yourdoghasnotes. This skill is how to pick the post and write the line. It was salvaged on 18 Nov 2026 from the
unmerged branch `codex/audience-comment-skill` (the 4 to 7 Nov comment pilot). The 15 Nov salvage left it out because
the session then posted itself, which rule 1 forbade. Krish's 16 Nov ruling now covers comments ("Approve batches,
Codex posts"), so the craft is kept here and the posting follows the rules below.

## The rules that come first

- **Drafting is the desk's job; posting needs Krish's yes on the batch.** The desk drafts a batch: one comment per
  specific public post, each with its link and exact text, and whether it is top level or a reply. Codex posts only a
  batch Krish approved, exactly as approved, once each (AGENTS.md rule 1, scoped exception). A skip, a rewrite he
  posts himself, or a dropped draft closes that candidate.
- **No link, no selling, no template reused** (rule 7). Keep brand copy out of the joke.
- **Copy rules still apply** (rule 5): no exclamation marks, no em dashes, nothing that mocks the person.
- **Read `docs/HUMOUR.md` first.** A comment still needs its intelligent observation, stupid premise and slightly
  cruel payoff, aimed at the dog's situation.
- **Nobody's handle goes in this repository** (rule 6 and the 15 Nov salvage note). The working record of picks,
  accounts and verdicts lives in `local/lists/audience-comments.md` on the machine that runs the desk. Lessons go here
  or in `factory/floor.json` in general words.

## Screen the channel before the post

- Prefer public or community accounts whose purpose is conversation or information, such as parks, rating accounts
  and dog communities.
- Skip product-led accounts, sponsored posts, brand collaborations, launches, sales links and fundraising appeals. A
  funny reply deep in the comments still sits under the original pitch. Read the caption, collaborators and call to
  action. Krish withdrew a pick that approached a product-led channel through a supplement promotion.
- **Three comments per channel at most**, replies included, across the pilot, with no daily reset. Drafts that were
  never posted do not count. Ask Krish before going past three. Rotate when he asks, even below three.

## Pick the post

- It should be a recent post with a plausible US dog-owner audience and an active conversation. Activity beats the
  account's size. A large old post is not current reach.
- When likes are hidden, check the public plays on the Reels grid. Plays still say nothing about US audience or
  followers gained.
- Read the liked comments and replies. If an owner or foster is already in the thread, a reply to them can read more
  naturally than a top-level comment. Check that nobody has already made the same joke, and that the account has no
  reply from Heartside yet.

## Inspect the image, then write the joke

- **Look at the actual image or video before joking about what the dog is doing.** Alt text and captions can point to
  a candidate. They cannot tell you the dog's expression, predicament or punchline.
- **Never invent behaviour.** Krish rejected the monarch line ("that's a monarch. you can tell by the way it expects
  to be carried home 👑", a dog in butterfly wings) as making no sense. The pun needed a leap, and "expects to be
  carried home" was not in the picture. The replacement came from what was visible: wings and a leash. When a joke
  rests on the caption alone, say so in the draft.
- Find the one detail that makes this dog funny and give it a familiar human predicament. Use dry understatement, a
  dad joke or a pun only if it follows naturally. Read it aloud. Discard it if it could go under ten other posts, if
  the pun needs explaining, or if it misreads what the dog is doing.
- Leave sincere or sensitive threads alone when there is no natural opening.

## Krish's benchmarks (his own words)

- On a dog holding a shirt on a hanger for a resale shop: "Bro be wondering how he's ended up in a retail job after
  chasing his dreams (tennis balls)". The tennis ball gives a human phrase the dog's literal meaning.
- On dogs at Halloween: "a dog at halloween must be the closest thing to kid in a McDonalds ball pit. absolute
  mayhem", with a laughing emoji. It matches the scale of the chaos to a shared memory.
- Lowercase, conversational, and one context-specific emoji at the end. He added a 🐶 to one approved line and 😂🫠
  to another, so a fitting emoji can go in the first draft. It is not a signature.
- Keep his wording exactly when he supplies a line.

## After posting

- Codex reads each comment back live: the author is @yourdoghasnotes, and the text and target match the approved
  batch. It records the permalink as a `post_check` (`verified`, `mismatch` or `unavailable`) in the dated
  `docs/social/` event file that Claude checks and imports. Check for an existing Heartside reply before submitting,
  because a timed-out submit may have gone through.
- **Taste and growth are separate.** An approved comment proves taste, never growth. Comment likes and replies
  measure how it was received. Follows and profile visits over the same window only point a direction, because other
  activity overlaps. Claim followers, US geography or sales only with evidence
  (`docs/boost/2026-11-06-follower-acquisition-test.md`).
- Measure the desk by the share of independently written first drafts that Krish approves unchanged. Lines he wrote
  himself teach taste but are not wins. Record each verdict the way AGENTS.md says ("The engine learns from every
  session"): declines go in `factory/floor.json` with his words, and each verdict goes to the taste ledger.
