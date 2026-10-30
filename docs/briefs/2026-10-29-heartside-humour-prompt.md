# Claude Code prompt: make every Hilarious joke land (heartside)

29 October 2026. Paste into a Claude Code session on `krishanraja/heartside`. Same rules as the painter
fixes: no theme publish, no Teeinblue change, no push to `main`; one pull request. Generating images
spends credits, so the test batch below waits for Krish's yes.

---

Read heartside's README and canon first. Your job: make sure every Hilarious painting a customer can
get is genuinely funny at a glance, not just a nice picture of their dog.

**Why.** Painting the 24 breed examples showed that most Hilarious jokes in recipes v14
(`tools/print-art/recipes-v1.json`, `scene.joke`) land: the golden hogging the whole couch, the lab
"driving" the car, the dachshund at the coffee table like a chairman, the frenchie reviewing the film
with suspicion. The walk joke never did. Five versions (a parade leader, a person hurrying behind, a
proud trophy march, a five-star general) all came out as a handsome dog walking toward the camera, and
Krish rejected them: "if I was paying $119 I would not accept that". A customer who picks Hilarious
and answers "the morning walk" gets the same. Several other joke lines (`bed`, `feet`, `anywhere`,
`door`, `spin`, `cool`, `naps`) have never been painted at all, so nobody knows if they land.

**What makes a joke land in one picture** (from what worked): an absurd situation the eye reads
instantly, built only from what the owner said; a clear contrast between the dog's total seriousness
and the situation; a pose that is unmistakably not a normal dog photo. What failed: a joke that needs
a caption to explain it ("like a general"), a joke carried by the dog's attitude alone, and a joke
that needs a partial person.

1. **Rewrite the walk joke as a situation, not an attitude.** Strong candidates, all from the walk and
   the dog alone, no person and no props:
   - the sit-down strike: the dog lying flat out in the middle of the path, refusing to go one step
     further, utterly serious, the path stretching ahead;
   - the detective: nose pressed to one single blade of grass with total, furrowed concentration, as if
     solving a case;
   - the triumphant return: marching home exhausted but proud, tongue out, fur wild from the walk.
   Pick the strongest and keep the others in the spec as alternatives.
2. **Audit every joke line the same way.** For each of `couch`, `bed`, `feet`, `anywhere`, `walk`,
   `coffee`, `movie`, `naps`, `car`, `door`, `toy`, `spin`, `cool` and `none`: does it describe a
   situation readable with the caption covered? Rewrite any that rely on attitude, a caption or a
   partial person.
3. **Prove it with a test board before customers meet it.** Propose a batch of one painting per joke
   line (about 14), all with one example dog and one photo, using the store's own prompt builder and
   painter path. Show Krish the count and wait for his yes. Then show him the board, and keep only the
   lines he says are funny. A joke he rejects is rewritten and retested, never shipped.

Bump the recipe version, write the next `PROMPT-SPEC`, add a test that no Hilarious joke line contains
"like a" comparisons without a visible situation (or another guard you can justify), regenerate the
example prompts and the browser bundle, run the tests and builds, report each result, and open one pull
request with the test board linked.
