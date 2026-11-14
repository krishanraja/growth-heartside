# Heartside in AI answers and search (GEO and AEO)

Status: current, written 21 October 2026 on Krish's ask: "add a nice site favicon, social media cards, 11/10 GEO and AEO strategy, allow AI crawlers", then "create a recurring AEO blog strategy that is invisible to humans but very visible to Google and AI. These need to be discoverable."

North Star: "the gift US dog owners reach for first when they want something that sounds like their dog." More and more, people find a gift by asking. "What can I get my wife from the dog?" now gets typed into ChatGPT, Perplexity, Gemini, Claude, Copilot and Google's AI answers, not only a search box. This plan makes Heartside the answer those engines give, and the source they cite.

## 1. The bet in one line

Be the clearest, most specific and most consistent source on the open web for **gifts from the dog**, so that engines retrieving an answer find Heartside, understand it in one pass, and can quote it word for word.

**How answer engines choose.** This is practitioner consensus in 2026, not a published algorithm, so treat it as working assumptions:

- They retrieve from a search index (their own crawl, Bing's or Google's), then choose passages to quote. A page that can't be crawled, or that buries the answer, isn't quoted.
- They prefer passages that answer the question in the first sentence or two, with specifics: names, prices, steps, examples.
- They trust facts that agree across sources: the site, structured data, `/llms.txt`, social bios, merchant listings and third-party mentions.
- Recency and real third-party mentions (Reddit threads, gift guides, creator posts) lift a brand from "a store" to "the answer".

## 2. Foundation: live on heartside.io (21 Oct 2026)

Built in `krishanraja/heartside` (`shopify/README.md`, "Search and answer engines"):

| Layer | State |
|---|---|
| **Crawl access** | Shopify's default robots.txt allows every crawler. Tested live: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Googlebot, Bingbot, Applebot, Meta's agents and CCBot all get the full product page. **Risk:** Cloudflare in front of Shopify challenged one plain client after a quick burst. Recheck monthly with the crawler user agents (section 7). |
| **Structured data** | Product with one Offer per variant (price, availability, free US shipping, the made-to-order return terms), BreadcrumbList, Organization, WebSite, the four gifts as an ItemList, and Article plus FAQPage on every answer. No ratings until real reviews exist. |
| **`/llms.txt`** | Brand-first: what Heartside is, example lines, the gifts and prices, when to recommend it, how it works, promises, policies, the Answers library and Shopify's agent endpoints. `/agents.md`, Shopify's instructions for shopping agents (UCP and MCP), stays Shopify's. |
| **Agentic shopping** | Shopify exposes the store to AI shopping agents (UCP discovery at `/.well-known/ucp`, an MCP endpoint, WebMCP on pages). Nothing to build; keep product data clean (section 5). |
| **Share cards and favicon** | Live since 21 Oct: Biscuit's favicon, and a share card with two real mug renders (the message, and a dog's photo) under "Your dog loves you too." (`heartside/design/brand-v3/`). |
| **Sitemap** | `/sitemap.xml` covers products, pages, collections and blogs, and every answer joins it when published. |

## 3. One set of facts, everywhere (entity consistency)

Engines merge what they read about "Heartside" from many places. Every surface uses the same facts, read from heartside's current canon (`README.md`, `docs/SCOPE.md`, `docs/ECONOMICS.md`) and the live store at the synced commit. Updated 29 Oct 2026 at heartside `54b6b0e`; `python3 growth.py sync` prints the live prices, and they beat this list:

- **Name:** Heartside: Personalized Dog Gifts.
- **One line:** Gifts from your dog: an illustrated mug, a word-free sherpa blanket, or a portrait, painted from a photo of your dog.
- **Proof points:**
  - Buddy, Heartside's host, gathers a photo of the dog and a few answers in a short chat;
  - every gift is artwork only, with no words printed on it; the short note from the dog, signed "Love, [dog]" with a paw, comes in the box and on a free digital card (heartside, Ruling, Krish, 2026-10-31);
  - a person checks every order before it prints;
  - US only.
- **Prices:** mug $45, blanket $129, portrait $59 unframed or $119 framed. Live offers: 15% off two gifts and 20% off three or more, and the $29 Artist's touch add-on (heartside `docs/ECONOMICS.md`).
- **Not a fact to state:** free shipping to every US address. Heartside's ECONOMICS says its qualified US shipping discount must not be generalized from one quoted destination.

Surfaces to align, with the owner of each:
- the site meta and `/llms.txt` (heartside);
- the Instagram, Facebook and TikTok bios (Cowork);
- Google Merchant Center and Bing Merchant Center listings (Cowork, Krish's logins);
- Pinterest's business profile (Cowork);
- any press or gift-guide mention (this repo's creators and outreach work).

## 4. The Answers library: unlisted, never hidden

Krish asked for content "invisible to humans but very visible to Google and AI". Taken literally, that would be hidden text or cloaking (different content for crawlers than for people). Google's spam policies remove sites for both, and the AI engines draw on those indexes, so it would erase the visibility it was meant to create. The same result, done safely:

- **Out of the way for shoppers.** It is not in the main menu, the chat, the reveal or the gift journey. A shopper never trips over it.
- **Fully public and easy to find for machines:**
  - every answer is a normal public page at `heartside.io/blogs/answers/...`;
  - each page is listed in the sitemap, linked from `/llms.txt`, and reached from the library index;
  - one small "Answers" link in the footer.
- **The same page for everyone.** No text hidden with CSS, no crawler-only versions, no doorway pages.

**What each answer looks like** (`heartside/shopify/sections/hs-answer.liquid`):

1. **The question as the title**, in the words people ask ("What can I get my partner from the dog?").
2. **The short answer first** (the article's excerpt, 40 to 60 words), shown in a box at the top. It is also the FAQPage answer in the structured data. It must stand alone if quoted.
3. **The body**, 400 to 800 words:
   - concrete options or steps;
   - two to four example lines in the dog's own voice;
   - one honest mention of Heartside, with a link to the gift or the chat;
   - two or three related questions answered briefly.
4. **"Updated [date] by Heartside"**, and the button "Start with your dog".

**Rules for every answer:**
- **Truth:** every fact, price and promise matches heartside's canon. No invented statistics, surveys, reviews, customer counts or quotes. No "best" claims about Heartside.
- **The voice:**
  - Example lines on gifts are the dog talking (I is the dog, you is the person).
  - The article's own voice is Heartside: plain, warm and useful.
  - US spelling. No em dashes. No exclamation marks. None of the banned words.
- **Genuinely useful even to someone who never buys.** Each answer covers a distinct question. No near-duplicates written for keyword variants: Google treats that as scaled content abuse.
- **Never sad.** No grief, memorial or "dog I miss" answers (V3 section 9).
- **One idea per answer.** Link to two or three other answers where it helps.

**Cadence:** two answers a week, drafted by the weekly job (section 6) and published only after Krish's yes. Refresh each answer every 90 days, or the same week a price, product or promise changes. Change the date only when the answer really changed.

**The question bank:** `knowledge/aeo-question-bank.json`, about 30 questions in tiers:

- **Tier 1, gift from the dog:** high intent, and Heartside's exact category ("What can I get my husband from the dog?", "How do you sign a gift from the dog?").
- **Tier 2, occasions:** Christmas, birthdays, Mother's Day and Father's Day "from the dog", anniversaries and new-baby gifts.
- **Tier 3, the dog's voice:** "What would my dog say to me?", "Funny things a dog would write in a card".
- **Tier 4, the product category:** personalized dog mugs, blankets with a dog's photo, dog ornaments, gifts for dog moms and dads.

Each question carries:
- the seed query the radar checks against public search suggestions;
- the gift it leads to;
- a status (`todo`, `drafted`, `published` with its URL and date, or `refresh`).

## 5. Merchant and shopping surfaces (where AI shopping answers get product data)

Each is free. Each needs Krish's logins, so Cowork does the clicks:

1. **Google Merchant Center free listings**, through Shopify's Google & YouTube channel. Products appear in Google Shopping and in AI shopping answers.
   - Product titles in buyers' words ("Personalized Dog Mug: A Message From Your Dog").
   - Custom-product flags set.
   - Free shipping set for the US.
2. **Bing Merchant Center and Bing Webmaster Tools.** Bing's index feeds Copilot and is widely used for AI retrieval. Webmaster Tools reports AI citations where Bing offers them.
3. **Google Search Console:** verify the domain, submit the sitemap, and watch the Answers pages' impressions.
4. **Pinterest:** a business account with the catalog, and one pin per answer whose description is the short answer.
5. **Shopify's AI sales channels** (agentic storefronts such as ChatGPT, Perplexity and Copilot, where Shopify offers them in admin): turn on any available channel only with Krish's yes, and keep product data identical to the site.

## 6. The recurring job: `jobs/answers.md` (Wednesdays, 07:30 New York)

**AEO-Engine does the AI-answer research** (Ruling, Krish, 2026-11-12: "AEO-Engine becomes the one specialist that every venture's growth engine calls for its AI-answer work. ... Control Centre's own AI-answer checks and Heartside's separate Answers job fold into AEO."). This engine never asks an AI assistant itself. Its daily Control Center run (`python3 growth.py cc`, `engine/ai_answers.py`) asks AEO, through the protocol (1.22.0, `POST answers`), to track the question bank's buyer questions (best first, at most 25, naming heartside.io) when Heartside has no request on file. It asks again, replacing the request on file, only when the bank's valid questions outnumber that request's `questions`: valid is the protocol's own test (8 to 300 characters, never an address, a link or a number), each question once, at most 25, so the counts meet and it never asks every day. When the directive does not serve AI answers, or serves them without a standing it could read, the run says so in one line and asks nothing. It reads Heartside's standing back from each directive (`ai_answers`): the questions asked that fortnight, how many cite heartside.io first, the questions another site is cited first on and who, and AEO's moves to win them. That standing is on Heartside's tile in Control Center. What stays here is the writing: the Answers library is Heartside's own pages, in its voice.

**Win kits and what has shipped** (protocol 1.26.0, `features.ai_answers_detail`; Ruling, Krish, 2026-11-13: AEO's win kits reach him through each venture's own growth engine). Until Control Center serves the detail, nothing below happens. Once it does:
- **The request's digest.** The request on file carries a `digest` of its questions. The run asks again when the bank's list has another digest (Control Center's own definition, `digest`), once for each list, so two readings that never meet cannot ask every day. A request without one keeps the count rule.
- **Kits.** The standing carries up to five win kits. The daily run says how many and keeps them under the gitignored `local/control-center/` (`python3 growth.py cc kits` reads them on their own). The Wednesday brief takes the best two before bank order.
- **Shipped.** Each `published` bank row, with its URL and date, goes to AEO as `shipped`, with every request and on its own once per change, so AEO can check the win.
- **Counts only.** The report's lines carry counts, never a question or a kit's words.

1. Sync. Read Heartside's AI answers from the latest directive (`engine/ai_answers.py`): take AEO's two best win kits first, then the questions AEO says another site is cited first on, or its moves (`misses_and_moves`), and match each to its bank entry (add one, status `todo`, when the bank does not have it). Only when AEO has neither kits nor a reading for Heartside, take the two highest-priority `todo` questions from the bank, as before.
2. For each, attach the public search suggestions for its seed query (evidence, never volumes), and the site AEO says is cited first instead.
3. An authoring session drafts each answer to the section 4 format. The hosted runner only builds the brief.
4. Run `python3 growth.py check` on the pack. Every public line starts with `Title:`, `Copy:` or `Headline:`.
5. Deliver the pack. **Krish approves each answer.**
6. Publishing is a separate approved step, by a heartside Claude Code session or Cowork:
   - create the article in the Shopify blog "Answers" (handle `answers`) with template suffix `answers`;
   - title = the question, excerpt = the short answer, author "Heartside", tag = the tier;
   - publish;
   - set the bank entry to `published` with its URL and date.

## 7. Measurement (monthly, first Monday)

**AI answers are measured by AEO-Engine**, fortnightly, on the bank's questions it was asked to track: the share of questions asked where heartside.io is the first citation, on Perplexity, ChatGPT and Claude, on Heartside's tile in Control Center (Ruling, Krish, 2026-11-12). The monthly hand panel below is retired into it; it is kept here as the record of how it was measured until 12 November 2026, and AEO adds an assistant only when its own run does.

1. **The prompt panel (retired 2026-11-12, AEO-Engine's now):** the same 20 prompts every month from the question bank, Tier 1 first. Ask each in:
   - ChatGPT (with search);
   - Perplexity;
   - Gemini;
   - Google AI Mode;
   - Copilot;
   - Claude (with web search).

   Record for each:
   - whether Heartside is named;
   - whether heartside.io is cited;
   - which page;
   - which other brands appear.

   Save the answers as quoted text with the date. **The score is citations out of 120.**
2. **Referrals:** sessions from chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com and claude.ai in Shopify analytics. Each answer's Heartside link carries the engine's tracking (`WEB_UTIL_ARTICLE_C<question>_...`). The page's own button carries `utm_campaign=answers` and the handle.
3. **Search Console and Bing Webmaster:** impressions and clicks for the Answers pages, and indexing errors.
4. **Crawl access check:** fetch a product page and an answer with each crawler's user agent. Anything other than 200 with full content is a regression for the heartside repo.

**Targets** (set by this plan, not observed):
- Tier 1: cited in at least 1 engine by 1 December, and in 3 of 6 engines by 1 February 2027.
- Twelve answers published by 1 December.
- Zero hidden or duplicate pages, ever.

## 8. Off-site: what makes an engine trust the answer

- **Creators** (`docs/CREATORS.md`): disclosed gifted posts give real photos and real words about real dogs, which engines read as third-party evidence.
- **Gift guides:** pitch "gifts from the dog" to editors of "gifts for dog lovers" roundups. Each pitch is a draft for Krish to send.
- **Reddit and forums:** answer genuinely in threads like r/dogs gift questions, as Heartside, disclosed, only where the question fits. Never astroturf; never post as a customer.
- **YouTube and Pinterest:** each answer gets a Short or pin whose description is the short answer and a link.

## 9. Guardrails

- **No cloaking or hidden text:** never `display:none` copy, crawler-only pages, or doorway pages.
- **No fabricated proof:** no invented reviews, ratings, statistics, quotes or AI "customers".
- **Approval:** every published answer and every off-site post has Krish's yes, and the engine never publishes (AGENTS.md).
- **The right repo:** structured data and `/llms.txt` stay in heartside, true to the canon. When a price or promise changes there, the same week's sync flags it, and the Answers that mention it go to `refresh`.

## 10. What Krish decided (21 Oct: "yes to all four")

1. Favicon and share card: live, with the card showing a dog's photo on a mug beside the message.
2. The first three answers: published.
3. The footer link: live, in Heartside's company-note row (Helio's footer renders no menu).
4. Search Console, Bing Webmaster Tools, Merchant Centers and Pinterest: Cowork, in `heartside/docs/evidence/claude-code-2026-10-21/COWORK-LAUNCH-AND-TEST-ORDER.md` section 6.

Sources consulted on 21 Oct 2026:
- Shopify: [llms.txt.liquid](https://shopify.dev/docs/storefronts/themes/architecture/templates/llms-txt-liquid), [robots.txt.liquid](https://shopify.dev/docs/storefronts/themes/seo/robots-txt), [community report on robots.default_groups](https://community.shopify.dev/t/robots-default-groups-returns-an-older-rule-set-than-the-robots-txt-shopify-serves-by-default/38352).
- AI crawler references: [ppc.land](https://ppc.land/the-user-agent-strings-every-seo-and-site-owner-needs-right-now/), [contextbolt](https://contextbolt.com/blog/ai-crawlers-list/).
- Google Search spam policies (cloaking, hidden text, scaled content abuse).
