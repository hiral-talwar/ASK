# NOTES.md

## (a) How retrieval works and why I chose it

I used keyword-based retrieval via minsearch, indexing every product across
its name, category, room, style, material, colour, and description. With
only 41 products, the catalogue's own wording already matches how customers
phrase questions- "scandinavian," "solid teak," "japandi" all appear
directly in the data. At this scale, keyword search performs comparably to
embeddings while adding zero cost and far less complexity, so I chose it over
vector or hybrid search. A separate matching layer then checks each retrieved
candidate against whatever the customer actually specified- category as a
hard constraint, plus style, material, colour, budget, and dimensions only
when explicitly mentioned- before anything reaches the model.

Known limitation: keyword search misses true synonyms absent from the
catalogue text (I hit this directly with "couch" failing to find sofas, fixed
by expanding known synonyms into the search query itself before retrieval),
and struggles with vague qualifiers like "small" that have no literal value
to compare. I'd move to embeddings if the catalogue grew significantly.

## (b) What I think is wrong with the spec (§5)

**"Index each product by its name field."** Built literally, most real
questions would return nothing, since customers describe rooms, styles, and
budgets, not product names. Instead, I indexed across all relevant fields.

**"Always return the top 3 products, for every question."** This contradicts
"if the catalogue does not cover the question, say so." Always forcing 3
results would mean unanswerable questions still surface irrelevant citations.
Instead, I retrieve broadly but only show and cite genuine matches- some
questions correctly return fewer than 3, or none.

**"Score yourself on the percentage of questions answered."** Literally, this
rewards forcing an answer onto intentionally unanswerable questions,
undermining the "say so honestly" rule. Instead, I counted an honest refusal
as a pass, not a failure.

## (c) How I used AI

**Tools and rough split:** I used Claude throughout- for initial
architecture (retrieval, the matching layer, prompt design) and for
debugging issues I found through my own testing. I'd estimate Claude wrote
roughly 75-80% of the initial implementation across `catalog.py`,
`retrieve.py`, `match.py`, `ask.py`, and `app.py`. All testing was mine: I
ran the assignment questions and additional queries myself, inspected the
retrieved SKUs and final responses, and identified every case where the
system behaved incorrectly before directing a fix.

**A real example of something wrong:** Claude's first version of category
detection in `match.py` only ever recognized a single category per question.
When I tested Q5 ("suggest a bed, a side table, and a lamp"), the system
said "we don't have a bed" even though a genuine japandi bed (SB-4001) exists
in the catalogue. I caught this by running the real question and knowing the
catalogue well enough to know that answer was wrong. I reported the exact
behavior, and the fix- detecting every category mentioned instead of just
the first- was written in direct response to my specific report, not caught
proactively by the assistant.

**One thing I wrote/decided myself:** I decided to compare raw retrieved
SKUs, SKUs actually shown to the model, and the final answer for every test
question, rather than treating each wrong answer as one undifferentiated
failure. This let me tell retrieval problems apart from generation problems
directly, which is what let me catch that the couch/sofa bug was a retrieval
issue rather than a matching or prompt issue.