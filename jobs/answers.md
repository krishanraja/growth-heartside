# Job: the Answers library (Wednesday)

Kind `answers`. `docs/GEO-AEO.md` sections 4 and 6. Time for Krish: about 10 minutes to approve two answers. You draft; you never publish, change the store, or edit the heartside repository.

AEO-Engine is the one AI-answers specialist (Ruling, Krish, 2026-11-12). It asks the AI assistants and says where Heartside is not cited first; this job never asks an assistant itself and only writes the answers. Heartside's daily Control Center run asks AEO to track the bank's questions and reads the standing back (`engine/ai_answers.py`).

1. `python3 growth.py sync`. Use the `heartside_sha` it prints. If the canon changed a price, product or promise, set every published answer that mentions it to `refresh` in `knowledge/aeo-question-bank.json`, and draft its update first.
2. Take two questions, AEO's first (`engine/ai_answers.py`):
   - **AEO's win kits first**, once Control Center serves them (`features.ai_answers_detail`, protocol 1.26.0; Ruling, Krish, 2026-11-13: AEO's win kits reach him through each venture's own growth engine).
     - `python3 growth.py cc kits` reads them and keeps them under the gitignored `local/control-center/` (it needs `CONTROL_CENTER_ENGINE_TOKEN`). The daily Control Center run keeps them the same way, on the machine it runs on.
     - **Only a session sees kits today.** The scheduled Wednesday run on GitHub Actions (`engine.yml`) has no kits: the daily Control Center run keeps them on its own short-lived runner, and they never ride the checkpoint, which is public. That run briefs from bank order until Krish decides whether `engine.yml` may carry the engine token for this one read (an open item). So on a Wednesday, run `python3 growth.py cc kits` first, in this session.
     - `python3 growth.py run --job answers --force` then briefs the top two kits by priority (the highest number first, as AEO-Engine ranks them), before bank order. Each brief carries the kit's title, its H2s, its capsule rules, the pages to beat (hosts only), its site fixes for a heartside build session, and the tracked link.
     - A new page's `target_url` is always in the Answers blog (step 5): AEO suggests `/answers/<slug>`, which the store cannot serve, so the brief uses `https://heartside.io/blogs/answers/<handle>` with this job's own handle.
     - A kit line the copy check refuses is dropped with a count, never rewritten. A kit for another site only (`off_site_only`) is not an Answers page and is passed over.
     - A kit is a brief, never copy: draft in Heartside's own words, and leave each site fix to a heartside build session.
     - A kit's words never go into a committed file, a commit message or a log.
   - **Then AEO's reading**, in the latest directive's `ai_answers` (`misses_and_moves`, kits first): the questions another site is cited first on, then AEO's moves.
   - Match each question to its entry in `knowledge/aeo-question-bank.json` (add it, status `todo`, when the bank does not have it). Only while AEO has neither kits nor a reading for Heartside, take the two highest-priority questions with status `todo` (or `refresh`) instead.
3. For each, read the public search suggestions for its seed query. They are evidence of how people phrase it, never volumes.
4. Draft each answer to the format in `docs/GEO-AEO.md` section 4:
   - **the question as the title**, in the words people use;
   - **a short answer of 40 to 60 words** that stands alone if quoted;
   - **a body of 400 to 800 words:**
     - concrete options or steps;
     - two to four example lines in the dog's own voice (I is the dog, you is the person), taken from or true to heartside's V3 4.2 lines;
     - one honest mention of Heartside, linking with `python3 growth.py link https://heartside.io/ WEB_UTIL_ARTICLE_C<question number>_H01_V1_<YYYYMMDD>`;
     - two or three related questions;
   - **a handle:** the question in lowercase, joined by hyphens.

   Use only facts from heartside's canon: prices, gifts, promises. No statistics, surveys, reviews, dates that aren't confirmed, or claims about other brands. Run edit passes A to E (`knowledge/COPY-DOCTRINE.md`).
5. Build the pack:
   - kind `answers`, one `store` item per answer;
   - `target_url` = `https://heartside.io/blogs/answers/<handle>`;
   - every public line starts with `Title:` (the question), `Copy:` (the short answer and each paragraph) or `Headline:` (each subheading), so `python3 growth.py check` holds it to the copy rules.
6. Run `python3 growth.py check` on the pack and fix everything it reports. Set each question to `drafted`, with the pack date.
7. Final message: the two questions, their short answers, and the publishing steps for whoever publishes once Krish says yes:
   - create the article in the Shopify blog "Answers" (handle `answers`): template suffix `answers`, author "Heartside", title = the question, excerpt = the short answer, tag = its tier;
   - publish it;
   - set the question to `published`, with the URL and date.

   That row is how AEO learns the answer shipped: once Control Center serves the detail, the daily run sends each `published` row with its URL and date to AEO as `shipped`, once per change, so AEO can check the win. Mark a row `published` only once its page is live, and never invent its URL or date.
