# SaveNMES v5 Outline (user-edited, numbers filled) - working spec

THESIS (Key Points): The case against closing NMES is clear. Our model's median closure
saving is $25,394 a year (11,664-scenario grid, leaver add-ons priced). The district needs growth, not
closures. We ask the board to choose the growth path, and for four things.

PART ONE - THE CASE AGAINST CLOSING NMES (NMES-specific)
1. The school works. [have: scores table + history chart]
2. The school is not expensive. 20-yr cost/student vs district schools, neighbors, KY
   average [build: neighbor-district series]; enrollment-vs-cost-per-student curve
   anchored on 20 yrs enrollment + capacity [build].
3. What closure actually frees is small. Fixed-vs-variable breakdown bar chart with %
   per category + savable fraction highlighted [build from nmes_gl data]; retained-vs-
   eliminated table: staff moved = $58,774; all fixed positions cut = $276,928 [have].
   ANCHOR: the decision-relevant P&L (strict move-only rule). Cost that stops if the
   school does not exist: the fixed base only ($58,774-$276,928); variable spend
   ($331/student measured) moves with students; allocated overhead stays by
   definition. Revenue tied to students: SEEK + poverty federal, at risk only for
   leavers; local taxes never leave. Closure ADDS busing. Net: keeping NMES open
   costs a median $260 per student per year, and in 43% of scenarios it costs
   nothing. Context ladder: allocated loss $430K (the optics number) -> corrected
   for Title I skew ~$345K -> minus the district's own deficit share ~$130K ->
   decision-relevant median $33,240. One-line rebuttal: $19,348 is an allocation
   key, not a savings estimate.
4. What closure risks is large and recurring. Feeder framing for eastern Bourbon;
   lifetime SEEK per kindergartner = $63,890 (13 yrs at 1.0%/yr historical base growth);
   steps priced base-to-with-add-ons: 10% = $60K-$73K/yr, 20% = $120K-$146K, 30% =
   $176K-$214K; through gr12 $561K-$682K / $1.12M-$1.37M / $1.64M-$2.0M; lifetime
   per kindergartner $63,890 base, ~$72,000 with add-ons; $5.6M+ carried by current
   students. [have: step table]
5. The closure model, rebuilt on the new levers (11,664 scenarios; leavers now
   priced at base + the same $0/$500/$1,000 SEEK add-ons lever as the growth side):
   - non-salary fixed capture 50-100% ($29.4K-$58.8K)
   - fixed-position retention 100-0% ($0-$218,154)
   - teacher retention 100-0% (0-5 positions)
   - cost per position $50-75K
   - students lost 0-100% (grid values 0/10/20/30%; slider full range)
   - property-value loss 0-10% of est. zone base ($0-95K; PVA records ask pending)
   - busing +0-10% of district transportation ($0-270K)
   RESULTS: median $25,394 | 45% lose money | range -$549,401 to +$651,928 |
   middle half -$115,404 to +$165,903. Anchor on district elementary cost/student
   ($17,605, May 2026 table). Reproducible: build/closure_grid.py.
6. The growth calculator (FINAL, structurally non-negative): enrollment 110 up to
   200. Hiring scales strictly with the gain: a teacher is added only for each FULL
   cohort of 20-25 students beyond the ~40 seats existing sections absorb, priced at
   the certified schedule's entry-to-midpoint rows ($41,718-$56,583, because new
   positions are new hires, not 25-year veterans); support staff from none in the best case
   to 1 per 50 added students in the worst, at the school's own classified lines
   ($20,000-$37,000); busing
   $0-$1,000 per recruited student; marginal cost $400-$1,000 per student (measured
   student-scaling spend: $331).
   RESULTS: 6,561 scenarios | median +$142,800/yr | ZERO negative | range +$26,260
   to +$296,904 | at 200 enrolled median +$192,040. Exhaustive sweep of every slider
   position bottoms out at +$2,626 (a single recruited student at max costs).
   WHY IT CANNOT GO NEGATIVE: each student brings $4,626 against at most $2,000 of
   per-student charges, and a hire only triggers once its cohort's net revenue
   (20 x $3,626 = $72,520 minimum) exceeds the costliest new hire ($56,583).
   COMPARISON LINE: the median growth scenario (+$142,800) is 5.6x the median
   closure saving (+$25,394), and growth's WORST case beats closure's median.

PART TWO - THE DISTRICT NEEDS GROWTH, NOT CLOSURES (district-wide)
1. Money problem: $2.65M gap, reserves -$1.1M/yr, aid cliff + 248 fewer funded
   students; ADD: the capital-to-GF sweep ($1.32M FY2026) is eating bonding capacity.
2. Enrollment problem: children flat 25 yrs, enrollment -10.2%, 450-550 outside with
   $2.1-2.3M. Hinge: competitive, not demographic; build a better product.
3. Revenue problem: lowest rate, only decline among neighbors. [have: 14-yr chart]
LEVER 1 - grow enrollment: Eminence case study (+37%, 4-in-10 nonresident) [build:
   Eminence-vs-Bourbon index chart from eminence_series.json]; district +10% to +30%
   enrollment = +$1.11M to +$3.32M/yr net of supplies.
LEVER 2 - inspect and cut fixed costs: total district fixed costs + cut ranges [build:
   district-wide fixed-cost rollup]; energy, routing ~$270K, admin restructure, do not
   cut teachers; range $960K-$1.9M.
LEVER 3 - align the tax rate: 0-100% restore to 2018 = $0 to $1,699,900/yr slider;
   statewide recall record [build: research]; HB 44 + options tables [have].
GROWTH PLAN, PRICED: interactive 3-move calculator [build]; triangular-distribution
   outcome: median $2,468,969/yr, IQR $2,300,270-$2,636,282 [computed].
THE CHOICE: two roads WITH outcome ranges: closure median $25,394 (45% lose) vs growth
   plan median ~$2.47M.
FOUR ASKS + HOW: Permanent; 4 years with public targets [build: proposed targets
   table]; grant/private funds; public commitment. How: record -> themed academy ->
   incentives -> grants.

DECISIONS TAKEN (flag if wrong):
a. Growth calc uses MARGINAL staffing (spec'd 1-per-20-25 as written gives a NEGATIVE
   median, -$21,920, because it charges average staffing; marginal version is the
   defensible economics and matches the class-cap math already published).
b. Calculator base = 110 (district's own figure, still flagged unsourced); ceiling 200
   on the slider with the 198 note (2013 state-approved rating).
c. Property-loss lever priced $0-95K pending the PVA records response.
d. New headline numbers REPLACE $21,571/45%/2,916 everywhere (site, report, summary,
   model, tests) - this is a v4.2 release with a corrections entry.

COST-PER-STUDENT ANCHOR (all current figures use the district's May 21, 2026 Cost of
Delivery table, read from the slide and archived as slide10_image16.png):
  NMES $19,080 | Bourbon Central $17,410 | Cane Ridge $17,403 | state avg $19,020
  EOY 2024/25 SAAR: 491 / 461 / 128 (elementary 1,080; NMES capacity listed 175, 73%)
  District elementary weighted cost/student: $17,605 (the calculators' anchor line)
  GROWTH anchor: NMES to 200 at marginal cost -> district elementary $16,405-$16,443
    per student (down 6.6-6.8%)
  CLOSURE anchor: even the sold case moves it only to $17,349 (down 1.5%); the grid
    median moves it 0.2%
  Decision ladder re-anchored: allocated loss $396,416 (latest table) -> ~$311K after
    Title I skew -> ~$182K NMES-specific -> $33,240 decision-relevant
  The 2023-24 federal $19,348 is retired to the history series and reconciliation
  only; the 300-breakeven reconstruction keeps it because that is the figure the
  district's own claim was built on.
  NOTE: the table's own EOY 24/25 enrollment is 128, which further isolates the "110"
  figure as unsourced; growth calculator base stays 110 with the caveat.
