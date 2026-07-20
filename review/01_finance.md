# Adversarial Review: Save NMES Financial Claims
**Reviewer stance: hostile school-district CFO. Sources: `build/build_model.py` (line refs), `NMES_Financial_Model.xlsx` (cell refs), `Saving_North_Middletown_Elementary.pdf` (page refs = printed page numbers +1 in PDF file), `index.html` (site JS). All arithmetic below independently recomputed and confirmed.**

---

## 1. The denominator switch: $2.65M "structural deficit" vs $1.15M actual drawdown

**CLAIM:** Closure saves $361,240 = "13.6% of the $2.65M structural deficit"; levy = "45.5%."
**ATTACK:** The project uses two different denominators depending on which flatters it. Every belittling percentage (13.6%, 24.2%, 45.5%) divides by the **before-transfers** deficit of $2,648,086 (Closure_Model!B21, `build_model.py:210`; Tax_History!B54, line 581; index.html `var DEFICIT=2648086`). But the Runway tab, the "three budget cycles" runway claim, and the Alternatives comparison all use the **after-transfers** drawdown of ~$1,145,561/yr (GF_Summary!D16, line 185; PDF p.24: "drawing it down at $1.1 to $1.2 million a year"). The ~$1.42M of transfers are, by the project's own admission (PDF p.3), "some of them recurring and legitimate resources." Against the number the district actually bleeds:
- Base closure = **31.5%** of the annual drawdown, not 13.6%.
- District-favorable $640K = **55.9%**.
- A CFO's aggressive case (~$860K, see section 3) = **~75%** — "closure stops three-quarters of the bleeding" is a devastating counter-soundbite.
**EVIDENCE:** GF_Summary!D16 = 1,145,561 vs Closure_Model!B21 denominator = 2,648,086. FY24 change −1,065,657; FY25 change −1,225,465.
**VERDICT:** Vulnerable. **SEVERITY: High** (this is the first thing a competent CFO will do at the podium).
**FIX:** Present every share **both ways** in the same table ("13.6% of the pre-transfer gap; 32% of the actual annual drawdown"), and lean on the one defense that is denominator-proof: the *ratio* — levy year-3 raises 3.3x the closure base case under either denominator. Also demand (as the report already does, but promote it) the transfer-sustainability breakdown, because the honest denominator lives between $1.15M and $2.65M.

## 2. Is the $2,648,086 deficit itself solid?

**CLAIM:** FY2025 structural deficit = $2,648,086 (Assumptions B24−B21).
**ATTACK (a) — budget-vs-actual artifact:** **Fails.** These are audited actuals (FY2025 audit, revenues $26,449,318 / expenditures $29,097,404, lines 111/114), not budget figures, and FY2024 shows a nearly identical actual gap (−$2,535,088). This attack should be pre-empted explicitly, because opponents of the closure elsewhere often use budget numbers; this project doesn't.
**ATTACK (b) — one-time items inside "structural":** Real vulnerability. PDF p.13 admits bus purchases of ~$888,000 and ~$691,000 in consecutive years and that "single-year jumps can carry one-time costs." If those buses ran through the General Fund (common in KY), up to ~$700-900K of FY2025's $29.1M expenditure is capital outlay, and the recurring deficit could be ~$1.8-2.0M, not $2.65M. Cuts both ways: it shrinks the scary headline but also *raises* closure's percentage share.
**ATTACK (c) — FY2023 comparability:** The near-balanced FY2023 (−$237,120) sits in the same Figure 2 with a footnote that its revenue uses "a different presentation of state pension payments" (PDF p.3). A CFO will note the three-year average deficit is ~$1.8M and accuse the project of anchoring on the worst year. The ESSER-cliff explanation (p.4) is a good defense — the FY25 gap is the *post-federal-money* run rate — but it's in prose, not in the model.
**EVIDENCE:** `build_model.py:109-114`; PDF pp.3-4, 13; Tax_History!B37 (line 562) — note this cell **hardcodes** 2,648,086 as a blue input instead of `=Assumptions!B24-B21`.
**VERDICT:** Holds on (a); Vulnerable on (b). **SEVERITY: Med.**
**FIX:** Add a "deficit quality" line: FY2025 gap net of identifiable one-time expenditures (bus purchases at minimum), sourced from the audit's capital-outlay function line. Owning a ~$2.0M "clean structural" figure is far stronger than defending $2.65M live. Make Tax_History!B37 a formula.

## 3. Only 3 teaching positions eliminated — the load-bearing assumption, and it's exposed

**CLAIM:** Closure eliminates 3 positions (Assumptions B53, yellow), giving $361,240 net.
**ATTACK (a) — the number:** NMES runs 9 homerooms + specials for 128 kids (~14.2/class). District arithmetic: the ~1,040 combined elementary students at cap-compliant sizes need ~46-48 sections; three schools currently run ~52+. A CFO will claim 6-7 certified positions plus classified staff (aides, office, custodial — the model cuts **zero classified** beyond the $175K/$115K fixed buckets). Hostile case: 7 certified × $85K + 4 classified × $40K + $290K fixed = **~$1.04M gross** — which *exactly validates the superintendent's "over a million"* — minus $137.5K busing and $46K SEEK = **~$860K net (32% of deficit, 75% of drawdown)**. The site's positions slider (`sPos min=2 max=6`) cannot even express this case; capping the slider at 6 looks like range engineering.
**ATTACK (b) — self-contradiction with the Redistricting tab:** This is the sharpest knife in the drawer. The fill-the-seats plan books **1-2 sections avoided at the receiving schools from moving just 30 students out** (Redistricting B28/B29, lines 287-288; $85-170K of the claimed $140-225K value). Apply that same elasticity (1 section per ~15-30 students) to closure's 128 students moving the *other* way and closure frees **4-8.5 sections** — the district-favorable case or worse. The project cannot hold "moving 30 kids frees 1-2 teachers" and "moving 128 kids frees only 3" simultaneously. Symmetrically, a CFO will note the project treats NMES's 174 capacity as "a policy output, not a physical constant" (Assumptions C12) when arguing growth, but treats the receiving schools' 549/422 ratings as hard walls when arguing closure infeasibility (Facility_Plans A26).
**Defenses that exist and should be foregrounded:** (i) the 3 is a *net* figure — PDF p.5 says the 128 kids still need "eight to nine classrooms' worth" and receiving schools would "add sections in several" grades; 9 NMES sections minus ~6 re-created = 3 net. The model never states this reconciliation — it reads as "only 3 cut, period." (ii) Facility_Plans B15/B17: net 59 uncommitted seats for 128 children, Cane Ridge already 31 over rating. (iii) The empirical record (PDF p.6: Stanford/California — "no reduction in teachers or staff"). (iv) Closure_Model books **no added-section cost at receiving schools** (offsets = busing + SEEK only, lines 204-207), which is *generous to the district* — say so loudly.
**VERDICT:** Vulnerable as presented (the underlying position is defensible, the presentation isn't). **SEVERITY: High.**
**FIX:** (1) Publish the section-by-section reconciliation: 9 sections closed − N re-created at BC/CR (grade-by-grade, against KRS 157.360 caps) = 3 net, and show the classified-staff assumption explicitly. (2) Extend the sensitivity table and slider to 8-10 positions and *show* that even at 8 positions net saving ≈ $786K ≈ 30% of deficit — the "under a third" framing survives; hiding the case doesn't. (3) Either haircut the Redistricting section-avoidance credit or state why elasticity is asymmetric (adding 10/grade forces new sections at caps; removing 5/grade rarely closes one). Right now 3(b) is a free hit.

## 4. $85,000 loaded cost per certified position

**CLAIM:** Assumptions B41 = $85,000 (yellow, "replace with district payroll data").
**ATTACK:** Kentucky certified salaries in rural districts run ~$50-58K. Crucially, KY teachers' TRS pension and much of health insurance are paid by the **state on-behalf** — those dollars flow through the audit's revenues *and* expenditures but never touch the district's discretionary General Fund. The district's own avoidable cost per position is plausibly ~$60-68K. Two consequences: (i) closure staff savings at 3 positions are overstated by ~$50-75K (this *helps* the project — net drops to ~$300K); (ii) but the same $85K inflates the project's own Alternatives lines: attrition alignment 4×$85K = $340K (line 385), multi-age reorg $170-255K (line 399), and the Redistricting section credits. The error is symmetric; the *use* is not — the alternatives package leans on more position-multiples (4 + 2-3 + 1-2) than the closure case (3).
**EVIDENCE:** `build_model.py:131, 385, 399`; PDF p.13 concedes functional lines "include allocated state pension payments made on the district's behalf."
**VERDICT:** Vulnerable (both directions). **SEVERITY: Med.**
**FIX:** Split the input into "district-paid loaded cost" (~$62K, used everywhere) and note the on-behalf share separately. Rerun both closure and alternatives on the same number and show the conclusion (levy >> closure; menu > closure) survives — it does, because the error cancels across the comparison.

## 5. The 10-leaver × $4,626 SEEK deduction

**CLAIM:** 10 families leave the district, each removing $4,626/yr.
**ATTACK:** (a) "They'd just transfer within the district — no SEEK loss." Weak attack: the plausible exits are real district exits — Montgomery County (Mt. Sterling is ~10 mi down US 460 from North Middletown; its elementaries score 65-69 vs Bourbon Central/Cane Ridge's 26.5/19.3, School_Data rows 16-17 vs 687-688), homeschool, private. HB 563 makes exit frictionless and the project's own score data makes it attractive. (b) Double-counting: none found — leavers' SEEK is deducted once; stayers' SEEK moves with them and is correctly not counted as a saving. (c) Minor asymmetry: outgoing students are docked full base revenue with **zero variable-cost relief**, while incoming transfer students in the Growth model cost $400 each. At 10 leavers that's a ~$4K quibble. (d) The $4,626 base-only figure actually *understates* the loss (no add-on weights, no $100/ADA capital outlay) — i.e., it is district-favorable, and the marginal SEEK loss per ADA really is ≈ base + add-ons (the local-effort deduction doesn't shrink when a pupil leaves). Sensitivity 0-30 is published (Closure_Model A26:B29).
**VERDICT:** **Holds.** **SEVERITY: Low.**
**FIX:** Cite the Texas/Chicago displaced-student attrition literature next to the "10" to move it from "judgment call" to "midpoint of observed post-closure exit rates," and credit ~$400/leaver variable relief for symmetry.

## 6. The 4% levy path: $386K / $787K / $1.2M — the base is contaminated with restricted money

**CLAIM:** 4% on FY2025 collections of $9,641,017 → cumulative $1,203,816/yr by year 3, "~45% of the deficit."
**ATTACK (a) — restricted-fund base (the serious one):** The $9,641,017 base (Tax_History!B48 = C43, lines 570/575) is **total** real+personal collections, which includes ~$2.05M of building-fund (FSPK) and debt-service tax (Tax_History!B33 = 2,052,786) — money that **cannot pay a teacher**, as the project itself thunders elsewhere ("restricted building dollars presented as operating relief" is one of its own four warned framings, PDF p.6!). Growth on the FSPK nickel doesn't relieve the General Fund, and the KRS 160.470 4%-revenue mechanics don't apply to the separately-levied nickel the same way. GF-relief math: 4% × $7,829,060 → **$313K yr-1, ~$978K cumulative yr-3 = 37% of deficit**, not 45.5%. Worse: **the model already knows this** — Alternatives row 4 computes the levy low as `=Assumptions!B35*B36` = $313,162 on the GF-only base (line 379), directly contradicting the $386K used on the site, in the PDF (p.21), and in Tax_History. The project is internally inconsistent on its flagship alternative, and the model itself flags "GF vs building-fund CENT split unverified" (Tax_History G32, line 565).
**ATTACK (b) — political realism:** The rate fell 61.3→52.4 since 2018. The compensating-rate/rollback explanation (PDF p.20) and the documented 2019 4%-take are decent armor, but assuming the board takes the 4% **three years running** — after publicly floating a school closure instead — is a projection, not a plan. Also the 45% share divides a year-3 compounded revenue by a *frozen* FY2025 deficit; with expenditures growing (raises, steps), the year-3 deficit will be larger.
**ATTACK (c) — like-for-like:** Recurring levy vs recurring saving is fair, and the 3.3x ratio is honest. But the framing implies levy-or-closure; they are not exclusive (see section 8).
**EVIDENCE:** `build_model.py:558, 570, 575-581, 379`; index.html `var base=9641017`; PDF p.21.
**VERDICT:** **Broken as stated** (the $386K/$1.2M GF-relief figures don't survive the restricted-fund objection the project itself teaches the audience to make). **SEVERITY: High.**
**FIX:** Rebase the entire levy path on GF-only collections ($7.83M → $313K/$639K/$978K, "over a third of the deficit — and covering 85%+ of the actual annual drawdown by year 3"), or document from the DOR levy files that the 4% calculation legally applies to the combined rate with proceeds allocable to GF. Reconcile Alternatives row 4 with Tax_History B48 — right now the workbook argues with itself. The corrected numbers still beat closure ~2.7x; take the haircut before an opponent takes it for you.

## 7. Alternatives package "$1.1 to $2.1 million"

**CLAIM:** Menu worth $1.1-2.1M/yr, "even the low end beats the most generous closure estimate."
**ATTACK:** (a) The headline range is a **hardcoded yellow judgment** (Alternatives B21/B22 = 1,100,000/2,100,000, lines 417-418), a haircut of a raw sum ($1.74M-$3.12M) that includes lines the site's menu doesn't even display (attendance recovery, attrition alignment, multi-age). The site's own six displayed rows sum to ~$1.10M low but only **~$1.87-1.94M high — the $2.1M top of the range cannot be reproduced from the page that asserts it**. (b) Mutual exclusivity inside the raw sum: "multi-age reorganization" (6-7 sections instead of 9) and "fill NMES to 174" (9 sections at ~19 kids) **cannot both happen** — 174 kids in 6-7 sections breaks the K-3 caps the project cites (KRS 157.360). Both feed the sum the haircut starts from. (c) Attrition arithmetic: the closure case's 3 positions are "via attrition only" (B53) *and* the alternatives claim 4 attrition positions district-wide (B48) — the same retirements can't staff both plans; a CFO will ask which. (d) Confidence laundering: Medicaid/E-rate ($100-250K) is rated "Low; needs evidence current claims are being missed" and shared services ($100-300K) "Low" in the model's own confidence column (lines 391-396), yet both sit inside the headline range. (e) The $400/student variable cost (B62) driving the fill-the-seats value is implausibly low; at a defensible ~$1,200-1,500/student the fill-NMES line drops from $140-225K to roughly $80-165K, and the Growth_Model adds one teacher for **46** added students. (f) Execution asymmetry: closure is one board vote; the package is ~10 initiatives with sustained "implementation discipline" — a CFO will risk-weight it at 50-60 cents on the dollar.
**EVIDENCE:** `build_model.py:378-419`; index.html menu table; PDF p.20 Figure 14 (which, to its credit, admits "ranges overlap and are not additive to the penny").
**VERDICT:** Vulnerable. **SEVERITY: High.**
**FIX:** Publish the haircut arithmetic: a table showing raw sum → minus overlapping/exclusive lines (pick multi-age OR fill-to-capacity, never both) → minus low-confidence lines for the "low" bound. Make the low bound *only* High/Medium-confidence items (levy $313K + delinquency $60K + admin $200K + transport $145K + fill $80K ≈ $800K — still > the $640K best closure case, which is the sentence that must survive). Fix the site so displayed rows sum to the claimed range.

## 8. The missing "Plan 4" — the false dichotomy a CFO will build on the spot

**CLAIM:** Scenarios tab: status quo vs closure ($0.8M FY2029 reserves) vs recovery plan ($3.7M).
**ATTACK:** Nothing stops the board from doing **closure + levy + the non-NMES menu items**. Strip the NMES-dependent lines (fill-to-capacity $140-225K, multi-age $170-255K) from the package and add closure's $361K: Plan 4 ≈ menu-minus-overlap + closure ≈ Plan 3 + ~$100-200K/yr, i.e., **Plan 4 financially dominates Plan 3** in the model's own arithmetic. The project's real case against Plan 4 is non-financial (town, academics at 58.2 vs 26.5/19.3 schools, enrollment-loss risk, the closure-savings literature) plus the enrollment-loss feedback — but the Scenarios sheet never models it, so the omission looks evasive. Also: Scenarios E6 hardcodes "13.6%" and "24.2%" as static *text* (line 517) — stale the moment any input moves.
**EVIDENCE:** `build_model.py:500-525`; PDF p.24.
**VERDICT:** Vulnerable. **SEVERITY: High.**
**FIX:** Add Plan 4 yourself, honestly: show it nets only ~$100-200K/yr more than Plan 3 *before* counting enrollment-loss risk (30 leavers erases $139K of it), transition costs, and the empirical record that closure savings under-deliver (Chicago −42% vs projection, PDF p.6). Owning the comparison converts the weakest structural point into the strongest rhetorical one: "closure adds at most 6% to the recovery plan and risks a school and a town to get it."

## 9. Transportation: "$2,913,654, up 20.3 percent"

**CLAIM:** Transport up 20.3% in FY2025 alone (implying base ≈ $2,421,990 in FY2024).
**ATTACK:** Single-year cherry-pick with no FY2023 baseline shown anywhere in the model; the same page admits bus purchases of ~$888K/$691K in consecutive years and that "single-year jumps can carry one-time costs" (PDF p.13). If fleet purchases sit in that line, the 20.3% is partly capital, the "fastest-growing budget line" framing wobbles, **and** the 5-10% "transportation optimization" alternative ($145-290K, computed as `=B42*B43/44`, lines 133-134, 389) is percentaged off an inflated base. There is also a tension to exploit: the project claims routing can *cut* 5-10% of the district's transport spend while insisting closure's added routes cost $137.5K — if a 20%-efficiency Boston-style optimization is available (site cites MIT/Boston), it's available under closure too.
Separate cherry-pick on the closure busing offset: the model's **own bottom-up estimate** is $51K-$147K (Transport_Geo B33/B34, lines 339-340, midpoint ~$99K), yet the Closure_Model uses a $75K-$200K "planning range" midpoint of $137,500 — chosen above the bottom-up midpoint, trimming closure savings by ~$38K.
**EVIDENCE:** `build_model.py:132, 325-342`; Assumptions B42-B44; PDF pp.4, 13.
**VERDICT:** Vulnerable. **SEVERITY: Med.**
**FIX:** Add FY2023 transport expense to Assumptions and show the multi-year trend; state whether bus purchases are inside the $2.91M (records ask if unknown); rebase the optimization range on transport-net-of-capital; and either use the bottom-up midpoint (~$100K) for the closure offset or justify the uplift (tiered-route breakage) explicitly.

## 10. Per-pupil $19,348 and the fill-the-seats "$19,348 → $14,339"

**CLAIM:** NMES spends $19,348/pupil (highest of three elementaries); filling seats cuts it 26%.
**ATTACK:** (a) $19,348 is the ESSA **total** including ~$5,175/pupil of federal money (B14−B15), much of it Title I tracking the school's 76-93% FRL population — money the district neither keeps nor saves on closure. The project uses this *correctly* against the superintendent's $1M (showing state/local is $1.81M), but a CFO will note the scary $19,348 is also the project's most-quoted number and it's the least GF-relevant one. (b) 2023-24 spending paired with 2024-25 enrollment (self-flagged, Redistricting A43). (c) The $14,339-at-capacity figure is mechanical dilution: fixed 2023-24 site cost + 46 × $400 over 174 kids; with a realistic marginal cost per student it's ~$14,600-15,000 — cosmetic, but the $400 is the same soft input attacked in 7(e).
**VERDICT:** Holds with bruises. **SEVERITY: Low-Med.**
**FIX:** Lead with the state/local $14,173 figure in headlines and keep $19,348 as the footnoted total; the closure argument only needs the smaller number.

## 11. Fund balance "$4,290,840, falling ~$1.1M a year"

**CLAIM:** As stated.
**ATTACK:** Both audited and correctly averaged ($1,065,657 and $1,225,465 → $1,145,561; GF_Summary D16). A CFO can only quibble that a two-year average is thin and that FY2026's budget (with a $1.41M contingency above the 2% floor, PDF p.4) may already bend the curve — i.e., the straight-line Runway is pessimistic about the district's own corrective capacity. Note the runway divides *unassigned-above-floor* ($3.34M) by the drawdown — "roughly three budget cycles" is defensible.
**VERDICT:** **Holds.** **SEVERITY: Low.**
**FIX:** Add the adopted FY2026 budget's projected change in fund balance as a fourth data point when it's citable.

## 12. Hardcodes, stale text, and range engineering (housekeeping)

- Tax_History!B37 hardcodes 2,648,086 (blue "input") instead of referencing Assumptions — a formula-integrity gift to a hostile auditor (`build_model.py:562`).
- Scenarios!E6 embeds "13.6%" / "24.2%" as static note text (line 517); site verdict strings embed "$2.65M".
- Alternatives!B21/B22 ($1.1M/$2.1M) are hardcoded conclusions dressed as a "conservative estimate" (lines 417-418).
- Site sliders bound the debate: positions capped at 6 (max-out net = $725K, 27.4%), busing floored at $75K, leavers capped at 30. Every cap is set exactly where the project's narrative stays intact.
- Cosmetic inconsistency: the stated closure range "$250,000 to $600,000" (PDF p.5, site Plan 2) has a ceiling **below** the project's own district-favorable case of $640,000 shown two sentences later. Opponents will call the range's top end shaved; make it "$250K-$650K."
**VERDICT:** Vulnerable (optics). **SEVERITY: Low-Med.** **FIX:** as itemized.

---

## Bottom line, ranked by danger

1. **Levy base contamination (section 6)** — the only claim I'd score **Broken**: $386K/$1.2M includes 4% growth on restricted FSPK/debt tax; the workbook's own Alternatives tab uses the correct $313K GF base. Fix before anyone else finds it; the corrected claim (37% of deficit, ~85%+ of drawdown) still wins.
2. **Denominator switch (section 1)** and **Plan 4 omission (section 8)** — the two framing attacks a CFO lands in the first five minutes.
3. **3-positions elasticity contradiction (section 3b)** — the Redistricting tab's section-avoidance credit hands the district the argument for 5-8 closure cuts. Reconcile or haircut it.
4. **Alternatives additivity (section 7)** — the $2.1M high end isn't reproducible from the site's own menu, and two menu lines are mutually exclusive.
5. What **holds outright**: the audited deficit's existence (not a budget artifact), the fund-balance/drawdown numbers, the SEEK-leaver deduction (actually conservative), the levy-vs-closure *ratio* (~3x, denominator-proof), and the model's genuinely district-favorable omission of receiving-school add-section costs. The report's habit of pre-flagging its own judgment calls (yellow cells, "four framings" on PDF p.6) is its best armor — the fixes above mostly consist of applying that same standard to the five places it slipped.
