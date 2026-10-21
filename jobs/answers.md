# Job: the Answers library (Wednesday)

Kind `answers`. `docs/GEO-AEO.md` sections 4 and 6. Time for Krish: about 10 minutes to approve two answers. You draft; you never publish, change the store, or edit the heartside repository.

1. `python3 growth.py sync`. Use the `heartside_sha` it prints. If the canon changed a price, product or promise, set every published answer that mentions it to `refresh` in `knowledge/aeo-question-bank.json`, and draft its update first.
2. Take the two highest-priority questions with status `todo` (or `refresh`) from `knowledge/aeo-question-bank.json`.
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
