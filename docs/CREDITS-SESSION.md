# The daily credits session

Krish pays monthly for credits that Higgsfield, Runway and 21st Dev wipe at each reset. Ruling (Krish, 2026-10-29): this engine may spend up to its share of each pool every cycle with no per-batch approval, and reports what it made. The engine's GitHub runner holds no generator keys, so the spending happens here. One scheduled Claude session runs this file each day, with the Control Center, Higgsfield, Runway and 21st Dev connectors attached (Krish, 2026-10-29: "Scheduled sessions").

It is not one of the seven jobs in `automations.json`. Control Center's scheduled task runs it, not the Codex or Cowork automations.

## Read first

1. `AGENTS.md` to the end, especially rule 4 (the product on screen is always the real design), rule 6 (no customer's details) and "Concept-level approval".
2. `PLAYBOOK.md` for the creative bar.
3. `docs/CONTROL-CENTER-BRIEF.md`, "Prepaid credits (protocol 1.16.0)".

## Every run

1. **Read the share.** Call `get_engine_credits({ engine: "heartside" })` on the Control Center connector.
   - If it answers `held: true`, `credits: null` or an error, stop and say so in one line. Null is unknown, never a share of zero.
2. **Set today's budget per pool.**
   - The budget is `remaining_for_you / days_left`, rounded down to whole outputs.
   - In the last three days before `use_by`, the budget is all of `remaining_for_you`.
   - Soonest wipe first.
3. **Pick the work.** In this order, and only what the pipeline really needs:
   1. **An approved concept.** Make production for a concept Krish approved, recorded in `CHANGES.md` or `NOW.md` with his words (concept-level approval, 29 Oct), at the creative bar in `PLAYBOOK.md`.
   2. **A checked concept still waiting for his look.** Make stills for one of the checked concepts in `campaigns/`, so he sees the breadth of concepts before he approves one.
   3. **21st Dev.** Make store interface components that heartside's own build work has asked for: a section, a product card, a gift picker. These are drafts for a heartside build session. Nothing is installed in the store.
   4. **Nothing.** If nothing above needs making, make nothing. Never invent work to use credits up.
4. **Follow the rules for every generation.**
   - **Stills before video.** Motion only for a concept Krish approved, or a still that has tested well.
   - **The real design.** The product is always the real design. AI makes dogs, rooms and motion, never a drawn product, and never AI "customers" holding or reviewing it.
   - **Words.** Heartside's voice rules apply to any words on screen.
5. **Reserve, generate, settle**, once per generation:
   1. `reserve_credit_spend({ engine: "heartside", pool, amount, asset, objective_key })`.
      - `amount` is the tool's own quote, or the block's `unit_costs` (a GPT Image still 2.75, a Seedance clip 210).
      - `asset` says what is being made, in words.
      - `objective_key` is `organic_orders` or `net_sales_usd`.
      - If it is refused, stop spending from that pool.
   2. Generate with the tool's connector.
   3. `settle_credit_spend({ spend_id, amount, receipt })`.
      - `amount` is what the provider actually charged.
      - `receipt` carries the job or generation ids.
      - Use amount `0` when the generation failed or charged nothing.
      - Settle before the next reserve: there is one open reservation at a time.
6. **Keep what you made.** Keep it in the tool's own library, in a project or folder named `Heartside credits YYYY-MM-DD`. Nothing is committed to this public repository.

## The walls

- Never publish, post, send, schedule, follow or comment.
  - Making is not publishing.
  - A post still goes through concept-level approval and the go-live step, or Krish by hand.
- Never past `remaining_for_you`. Never a top-up, a plan change, an upgrade or new money.
- No customer's photo, name, dog or answers in any prompt or output.
- Never report a session spend in a runner report as well. Control Center already counts it, and reporting it twice takes it off the share twice.

## End with

One line: what was made from each pool, credits spent and left, and where it is.

For example: "Higgsfield: 6 stills for the-couch-spot (16.5 credits, 2,383.5 left) in Heartside credits 2026-10-30. Runway: nothing needed. 21st Dev: 1 product card draft (5 credits)."
