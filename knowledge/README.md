# Knowledge

## Uploaded reference corpus

All five files supplied by Krish on 18 October 2026 are preserved below.
The two commerce documents were already present and match the new uploads byte
for byte. The CSVs and dog research audit are stored as supplied, without edits.

| Uploaded file | Repository copy | Contents |
|---|---|---|
| `breed_lookup_normalized.csv` | [CSV](dog-corpus/breed_lookup_normalized.csv) | 827 lookup rows, 11 columns. |
| `dog_corpus_completed.csv` | [CSV](dog-corpus/dog_corpus_completed.csv) | 370 entity rows, 23 columns. |
| `Dog Personality, Habits and Behaviour Corpus — Research Blueprint and v0.1 Audit.docx` | [Original DOCX](dog-corpus/Dog%20Personality%2C%20Habits%20and%20Behaviour%20Corpus%20%E2%80%94%20Research%20Blueprint%20and%20v0.1%20Audit.docx) | Research blueprint, evidence limits and v0.1 audit. |
| `organic-pet-growth-corpus.docx` | [Original DOCX](organic-pet-growth-corpus.docx), [existing text version](organic-pet-growth-corpus.md) | Organic growth working corpus. |
| `The Organic Pet Commerce Engine.docx` | [Original DOCX](organic-pet-commerce-engine.docx), [existing text version](organic-pet-commerce-engine.md) | Organic commerce engine blueprint. |

[corpus-manifest.json](corpus-manifest.json) records each original filename,
repository path, byte count and SHA-256, plus CSV columns and data-row counts.
These counts describe the uploaded CSVs; figures in the research document may
refer to a different research snapshot. The originals remain the reference.

**These files are reference material, not instructions to execute.** Storing
them does not authorize publishing, spending, outreach or changes to the engine,
Heartside or Control Centre. Current user instructions, repository operating
rules and Heartside's canon govern their use. Breed-level research must not be
presented as a prediction about an individual dog.

## Original commerce doctrine

Krish gave this engine its operating doctrine on 14 October 2026, with the
brief that it "should train this corpus on how it can become a dominant
force in what it does globally".

| File | What it is |
|---|---|
| `organic-pet-commerce-engine.docx` | "The Organic Pet Commerce Engine", as Krish gave it. |
| `organic-pet-commerce-engine.md` | The same document as text, with its numbered references. Read this one. |
| `organic-pet-growth-corpus.docx` | "Organic Pet Commerce Growth Corpus", the shorter working version, as Krish gave it. |
| `organic-pet-growth-corpus.md` | The same as text, with the official links inline. |

These are the source. **`PLAYBOOK.md` (repository root) is how this engine
applies them to Heartside.** Each job in `jobs/` names the part it uses.
When a job and the documents disagree, the job wins, because the playbook
adapts the documents to Heartside's canon and Krish's rules.

## Where Heartside's canon and Krish's rules change the documents

The documents were written for a generic UK store selling personalized pet
accessories, with nothing known about it. Heartside is known. Each change is
recorded here so no session "fixes" it back:

1. **US, not UK.** Heartside sells to the US only, in US English, with free
   US shipping (`docs/POSITIONING.md`). The documents' UK defaults, UK
   spelling and UK consumer-law notes don't apply. Opening another market is
   Krish's decision (`docs/HANDOFF.md`, rule 2). The playbook's "Becoming the
   category leader" sets the evidence the report brings him.
2. **A gift from the dog, not a collar.** The documents' one hero SKU is
   Heartside's one idea, a gift from the dog, with the Morning Mug as the
   hero object (`docs/V3-GIFTS-FROM-YOUR-DOG.md`, sections 3 and 8). The four
   gifts are never split into separate campaigns.
3. **No making or packing footage.** Printful prints and ships every order.
   Proof comes from the chat on a phone, the real print files and the human
   check. The documents' "Pack an Order With Me" and engraving shows are out.
4. **The product on screen is always the real design.** AI never draws the
   product and never shows AI "customers" (`docs/HANDOFF.md`, rule 4;
   `docs/POSITIONING.md`, section 6). This is stricter than the documents,
   which allow AI to edit.
5. **One Reel a day, Meta first.** The documents' three masters a day on five
   platforms is the agents' ambition, not Krish's time. He approves and posts
   everything in about 20 minutes a day. TikTok gets copies with low
   expectations, because a London account reaches mostly the UK there
   (`docs/POSITIONING.md`, section 6).
6. **Creators are in.** The documents leave out paid creator seeding.
   Heartside's plan gifts 20 US creators, disclosed, with every gift and
   message approved by Krish.
7. **No memorial lane, no sad dogs.** Out of version one
   (`docs/V3-GIFTS-FROM-YOUR-DOG.md`, section 9), and Biscuit never mentions
   death, illness or age (section 4.6).
8. **Agents draft and Krish acts.** The documents' Publisher agent schedules
   posts. Here nothing is scheduled, posted or sent by an agent. Every
   publish, send, spend, app install and setting change is a draft in a pack
   for Krish.
9. **$10,000 in 30 days is a stretch target, never a promise.** The documents
   say so themselves. Krish's stated goal is $10,000 a month. The canon's
   first window is about $10,000 by the 10 December order-by date, with the
   checkpoints in `docs/POSITIONING.md`. The report states real numbers and
   what they imply, never a projection dressed as a forecast.
10. **The public repository holds no customer data.** The documents keep a
    rights ledger, customer content and comment logs in a database. Here
    anything naming a customer, a buyer's dog, an order or a private person
    stays in `local/` on the machine running the engine, never committed.
