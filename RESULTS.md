# RESULTS.md

# Verdict Criteria
I define "good" as: the SKUs cited are real and match what was actually asked,
no price/dimension/delivery information is invented, and unanswerable
questions are honestly refused rather than forced.

## Q1: Two-seater sofa, small living room, scandinavian, under ₹40,000
**SKUs retrieved (raw):** SB-1001, SB-1002, SB-1004, and 26 others
**SKUs shown to model:** SB-1001, SB-1002, SB-1004
**Answer:** Recommended SB-1001 (Aalto Two-Seater Sofa, scandinavian, ₹38,900)
as Best Match; listed SB-1002/1003/1004/1005 as Similar with the specific
reason each differs (wrong style or over budget).
**Verdict: Good** - exact match correctly prioritized; alternatives clearly
labeled, not hidden or invented.

## Q2: Dining tables that seat six
**SKUs retrieved (raw):** SB-2001, SB-2002, SB-2004, and 13 others
**SKUs shown to model:** SB-2001, SB-2002, SB-2004
**Answer:** SB-2001 and SB-2002 cited, both explicitly confirmed as six-seaters
in their descriptions.
**Verdict: Good** - correctly distinguished confirmed six-seat capacity from
tables where it isn't stated.

## Q3: Solid teak items
**SKUs retrieved (raw):** SB-5006, SB-9003, SB-2002, and 9 others
**SKUs shown to model:** SB-5006, SB-9003, SB-2002
**Answer:** All three genuine solid-teak products cited, spanning three
different categories (nesting tables, bookcase, dining table).
**Verdict: Good** - correctly matched on material alone, across categories,
without being wrongly filtered by category.

## Q4: Cheapest bed, and its size
**SKUs retrieved (raw):** SB-4004, SB-4002, SB-4005, and 23 others
**SKUs shown to model:** SB-4004, SB-4002, SB-4005
**Answer:** SB-4004 correctly identified as cheapest at ₹28,900, size stated
as 205x160x40 cm.
**Verdict: Good** - correct product, correct price comparison, correct size.

## Q5: Japandi bedroom - bed, side table, and lamp
**SKUs retrieved (raw):** SB-5001, SB-4001, and 25 others (SB-7002, the
japandi lamp, was among them)
**SKUs shown to model:** SB-5001, SB-4001, SB-4005, SB-4004
**Answer:** Correctly recommended SB-4001 (bed) and SB-5001 (side table).
Did not recommend a lamp- SB-7002 was retrieved but did not make it into
the final shortlist shown to the model.
**Verdict: Bad** - one of the three requested items (the lamp) was missing
from the answer.

## Q6: Chairs suited for a kitchen
**SKUs retrieved (raw):** SB-3003, SB-3006, and 7 others
**SKUs shown to model:** SB-3003, SB-3006
**Answer:** SB-3003 and SB-3006 were cited, both of which were provided to the
model and have catalogue evidence supporting their suitability for kitchen use.
**Verdict: Good** - correct, genuinely suited product cited with real
justification from its description.

## Q7: Bathroom vanities
**SKUs retrieved (raw):** none
**SKUs shown to model:** none
**Answer:** Honestly stated the catalogue does not have this.
**Verdict: Good** - correct refusal; this is one of the two intentionally
unanswerable questions.

## Q8: Walnut wardrobe delivered to Coimbatore by Friday
**SKUs retrieved (raw):** SB-6002, SB-6001, SB-6003
**SKUs shown to model:** SB-6002, SB-6001, SB-6003
**Answer:** SB-6002 correctly cited with its real details; explicitly stated
delivery information is not available, since delivery was actually asked
about.
**Verdict: Good**- real product cited, no invented delivery date, honest gap
stated because it was relevant to the question.

## Score
7/8 answered correctly (87.5%).

## Retrieval vs. generation split 

**Q5- retrieval problem.** SB-7002 (the japandi lamp) was present in the raw
retrieved candidates, so the search itself did not miss it. It was excluded
by the matching layer, which selects a fixed number of top-ranked items
across all requested categories combined, rather than reserving at least one
slot per category explicitly asked for. Because beds and side tables
outnumber lamps in the catalogue, they filled the available slots first. This
is a retrieval issue, not a generation problem- the model
never had the chance to consider the lamp at all.