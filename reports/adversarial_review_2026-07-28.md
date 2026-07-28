# Adversarial review of savenmes.org (v3.8, commit `ce4e481`)

**Date:** July 28, 2026
**Target:** the published site (`index.html`), the financial model (`NMES_Financial_Model.xlsx`), the archived source data under `build/`, and the test suite.
**Posture:** hostile. The job here is to find what breaks, not to confirm what works. Where a claim survived the attack, that is stated too, because an adversarial review that only lists complaints is not usable.

---

## 0. Scope and method

**Verified directly:** every arithmetic claim on the page that can be recomputed; the closure grid (`build/closure_grid.py`, re-run); the calculator JavaScript against the grid and against the model; the KFICS state reports (all three, read from the archived `.xlsx`); the statewide spending file; the KDE non-resident workbook; the model's Assumptions, Closure_Model, Redistricting, Alternatives and Tax_History tabs; the full test suite (`tests/run_all.py`, plus the Playwright browser tests, run against a local Chromium).

**Not verified:** the live rendered site (this environment's network policy returns 403 for `savenmes.org`; the audit was run against the identical source — local `HEAD`, `main`, and `origin/main` are all `ce4e481`, and the deployed `index.html` was confirmed byte-identical through the GitHub API). Also not independently re-fetched: the FY2024/FY2025 audits, the KDE report-card files, KRS/KAR text, and the 49-page PDF line by line. The PDF's shared figures were checked only through `sync_check.py`, which confirms site/model/PDF agreement, not correctness against source.

**Test suite result:** `validate_all.py` and `sync_check.py` pass — 63 cross-artifact matches, 0 discrepancies. All 17 browser tests pass. See §3.4 for why that is a weaker guarantee than it looks.

---

## 1. What survived the attack

Stated first so the rest is calibrated.

- **The closure grid reproduces exactly.** `build/closure_grid.py` re-runs and asserts every published statistic: 1,944 combinations, range −$384,780 to +$565,000, median +$91,240, P25/P75 −$17,500/+$200,000, 559 negative (28.76%, published as 29%). Nothing is fudged.
- **The 99.6% statewide claim reproduces.** Restricting `KYRC24_FT_Spending_per_Student.csv` to A1 schools: 1,146 of 1,151 exceed $8,305 per student = **99.57%**. (The A1 restriction is not disclosed on the page; over all school types it is 99.24%. The claim is sound, the filter should be named.)
- **The non-resident numbers are exactly right and carefully defined.** From the archived KDE workbook: 436 non-residents enrolled in Bourbon County, of which 305 are Paris Independent (in-county) → **131 out-of-county**, **54 from Fayette**, **10 in Cloverport Independent**, **76 Bourbon residents enrolled out-of-county**, **net import 189**. Every one of these matches. The site's choice to publish 131 (out-of-county) rather than the flattering 436 is the correct call, and it made it.
- **KFICS condition figures are exact.** NMES 0.694064 → 0.702133 → 0.773295; Cane Ridge 0.812058 → 0.811765 → 0.728249; Bourbon Central 0.887637 → 0.819273 → 0.823017. The chart is accurate to the state file. NMES's four-year repair bill of **$3,099,148 is genuinely the smallest of the five schools** (BC $4.01M, CR $4.80M, HS $10.25M, MS $12.17M).
- **The 300-student breakeven reconstruction is arithmetically exact.** 128 × $19,348 = $2,476,544; ÷ $8,305 = 298.2.
- **The alternatives table foots.** The eleven line items sum to $1.595M–$2.888M ("about $1.6 to $2.9 million"); the three Moves partition those rows exactly.
- **The filled-to-capacity verdict is robust to its own worst methodological flaw.** §3.3 shows the staffing rule in the "fair test" table is not applied uniformly. I re-ran all six capacity scenarios under a genuinely uniform rule (sections crossed = round(Δstudents ÷ N), N ∈ {22, 24, 26}, applied identically to all three schools). **The "cheapest school" verdict is unchanged in all six scenarios at all three values of N.** The finding stands on its own; the flaw is in the audit trail, not the answer.
- **Several corrections run against the author's own case,** and are labelled as such: the v3.8 section charge that cut the fill package from $116K–$176K to $56K–$116K; the position cost cut from $85K to $60K; the disclosure of the $8,440 artifact, the Perry and Johnson counties best-cases, and the $1.03M "hostile paper case". That is real intellectual honesty and it should not be flattened by what follows.

---

## 2. Material findings

These are defects of fact or internal consistency. Each is reproducible from the repository.

### 2.1 The calculator does not implement the published model

`index.html:966` — `net = 290000 + p*c - b - l*4626 - o`.

The page tells the reader: *"These calculators run the same math as the full report and financial model"* (`:347`) and *"Every formula here matches the downloadable financial model"* (`:446`). They do not.

| | published grid (`closure_grid.py`) | calculator sliders |
|---|---|---|
| positions | 2, 3, 4, 5 | 2 → **6** |
| GF cost/position | $50K, $60K, $75K | $50K → **$85K** |
| added busing | **$100K**, $137.5K, **$250K** | **$75K** → **$200K** |
| fixed avoided | **$230K (mothball) / $290K (sold)** | **frozen at $290K, no control** |
| closure-triggered costs | $0–$326K (two levers) | $0–$330K (merged) |
| **reachable range** | **−$384,780 to +$565,000** | **−$278,780 to +$725,000** |

Consequences:

- A reader can drive the calculator to **+$725,000** — $160,000 above the ceiling of the range the hero strip calls "the honest range of yearly closure impact across 1,944 defensible scenarios."
- The calculator **cannot reach the published loss tail** of −$385,000. It bottoms out at −$278,780.
- The seventh lever (mothballed vs sold) is **absent from the calculator and frozen at the closure-favourable value.** At the default settings the frozen $290,000 is the single largest term in the equation — larger than the entire positions term.
- `tests/test_site.py:82` asserts `"-$278,780"` and names it *"closure v3 unfavorable tail"*. The regression suite has **encoded** the discrepancy rather than caught it.

This is the most serious finding in the review, because the calculator is the site's central invitation to the reader ("Do not take my word for it. Run the numbers yourself") and the closure range is the hero fact.

### 2.2 "Every one of them now comes from a document" is false

`index.html:373`: *"Seven inputs decide what a closure nets, and every one of them now comes from a document: the district's published salary schedule, its KDE filings, the class-size caps in KRS 157.360, the federal attendance-zone map, and this county's own history in Millersburg."*

The model's own Assumptions tab says otherwise:

| lever | model cell | model's own note |
|---|---|---|
| Principal & office avoided ($175,000) | `Assumptions!B51` | **"Estimate"** |
| Plant/utilities/insurance avoided ($115,000) | `Assumptions!B52` | **"Estimate; assumes building sold or repurposed"** |
| Positions truly eliminated (3) | `Assumptions!B53` | **"Estimate; via attrition only"** |
| Added busing ($137,500) | `Assumptions!B54` | **"Estimate; midpoint of $75K-$200K"** |
| Students leaving (10) | `Assumptions!B55` | **"Judgment call; see sensitivity table"** |
| Assessment erosion | `Closure_Model!E45` | **"Millersburg-calibrated; PVA records ask pending"** |

Only the SEEK base and the GF-borne position cost trace to published documents. The two "Estimate" cells that make up the frozen $290,000 are the **largest single input to the headline number**, and neither has a source. The sentence should be corrected; the estimates themselves are defensible and are already labelled honestly *inside* the model — the problem is only that the page claims more for them than the model does.

### 2.3 Three artifacts, three different busing ranges — and the headline statistics move

- `Assumptions!B54`: "midpoint of **$75K–$200K**"
- calculator slider `#sBus`: **$75,000–$200,000**
- `closure_grid.py`: **$100,000 / $137,500 / $250,000**

The grid is the odd one out, and it is the one that produces the published statistics. Re-running the grid with the model's own stated busing range:

| grid specification | median | % losing money |
|---|---|---|
| **as published** | **$91,240** | **28.8%** |
| busing $75K/$137.5K/$200K (the model's own range) | $116,220 | 23.3% |
| positions {2,3,4} instead of {2,3,4,5} | $61,500 | 34.6% |
| cost/position {50,60,70,75}K | $99,000 | 27.2% |
| extra busing point at $175K | $87,500 | 29.1% |

**The "median saves $91K" and "29% of scenarios lose money" are properties of the grid's design, not of the world.** A Cartesian product with equal weights is not a probability distribution: the median and the 29% are set by how many discrete points each lever was given. Substituting the model's own busing range — arguably the *more* defensible choice, since it is what both the Assumptions tab and the live calculator use — moves the loss share from 29% to 23%.

The hero fact strip presents "29% of scenarios lose money" with no indication that it is a uniform-weight grid artifact. The docstring in `closure_grid.py` says "equal weights"; the page never does.

### 2.4 The facility table contradicts its own footnote

`index.html:322`: `Bourbon Central | 602/564 | 535/521 | 459 (90 open)`

The note immediately below (`:325`) states the Today column uses **521** for Bourbon Central, explicitly disavowing 549 as *"a contingent To-Become figure tied to an expansion never built."* But 521 − 459 = **62**, not 90. The cell's 90 is 549 − 459 — the rating the note rejects.

Every other appearance on the page uses 62:

- the totalstrip at `:328` — "Net uncommitted seats … 31" = 62 open − 31 over ✓
- the prose at `:327` — "31 uncommitted at the approved 521 and 422; **59** only under the plan's contingent 549" (90 − 31 = 59) ✓
- Question 3 at `:510` — "521 and 422 … a net 31 uncommitted seats" ✓

So one cell in the most-quoted table on the page carries a number the rest of the page rejects — and it is the one that makes the receiving schools look **roomier**, i.e. it argues against the author. It is a transcription error, not a thumb on the scale, but it is in a table headed "What the district's own facility plans show," and a hostile reader will find it.

### 2.5 The levy yield: "audited" and "real estate only" are both wrong per the model

`index.html:410`: *"…priced at Bourbon's own **audited** yield of about $191,000 per cent of rate ($7,829,060 of General Fund collections across the 41.0 General Fund cents in KDE's levied-rates file), **real estate only, so the figures are conservative**."*

The model says three things that contradict this:

1. `Tax_History!G32`: *"GF vs building-fund **CENT split unverified**; dollar split is [audited]."* The dollar total is audited; the 41.0-cent denominator is not. Calling the resulting per-cent yield "audited" overstates it.
2. `Tax_History!G48`: the base is *"FY2025 General Fund **real + personal** collections."* Not real estate only.
3. `Tax_History!B14–B15`: Bourbon levies a **tangible/personal rate of 64.5¢** and a **motor-vehicle rate of 54.7¢** — separate rates that a real-estate increase does not move.

The direction of the error is the opposite of what the page claims. Putting real-**and-personal** collections in the numerator and real-estate cents in the denominator **overstates** the yield of a real-estate cent; it is not conservative. A cross-check confirms the gap: 41.0¢ on the FY2025 assessment of $1,843,569,625 (`Assumptions!B34`) yields $7,558,635, against $7,829,060 collected — collections run **3.6% above** what the real-property base alone supports, consistent with personal property being included.

**This matters for the site's single most quotable sentence.** At a real-estate-only yield of ~$184,357/cent, restoring the 2018 rate raises 8.9 × $184,357 ≈ **$1,640,777** against the $1,694,928 requirement — a **~$54,000 shortfall**, not the published *"covering that requirement to within $4,551."* The "almost to the dollar" framing is the most rhetorically load-bearing claim in Part Three and it rests on a denominator the model itself flags as unverified.

Related, smaller: the nine-district rate comparison ("second lowest of nine") compares **total** levied rates, which mix operating and building levies in different proportions by district — the page concedes this for Paris Independent (17.4¢ of building levies) but nowhere else. And "restore Bourbon's own 2018 rate" compares a 2018 total rate that carried **one** nickel against a 2025 total rate that carries **two**, so the General Fund rate being "restored" is roughly 6 cents below its 2018 level. That last one runs in the author's favour and is worth saying out loud.

### 2.6 The transitional-criteria section asserts a conclusion its own list does not support

`index.html:588–597`. The page states the rule: *"Kentucky keeps a school as a permanent center when it meets **four of six** criteria."* It then marks NMES as meeting criteria **1 (scores), 2 (bus rides), 3 (cost per student)** — and leaves **4 (equal programs), 5 (building condition), 6 (community support)** unmarked, with no claim either way.

Three of six is not four of six. Yet the callout beneath concludes: *"…the fair question to put to the district, in writing, is simple: **why label this school transitional when it meets that standard?**"*

The page has not shown that NMES meets the standard. On a site whose entire method is "every figure traces to a public record," asserting the threshold is met while demonstrating three-quarters of it is the kind of gap the district's counsel would find first. Criterion 6 (volunteer hours, PTA/PTO membership, an outside sponsor, a community service program) looks winnable on the evidence in the Voices section and should simply be documented. Criterion 5 is the one to be careful about: a 1948 building needing "at least 30 years of life left" is a substantive question, and the page's silence there is conspicuous next to how hard it works the KFICS condition index elsewhere.

### 2.7 KFICS: the favourable sub-metric is amplified, the unfavourable ones are absent

This is the sharpest selection problem on the site, because all of it sits in **the same rows of the same archived file** the page cites.

From `build/kfics_state_report_jul2026.xlsx`, tab `Rank A1 A5`, Bourbon County:

| Facility | **Kentucky School Score** | Condition Index | **Educational Suitability** |
|---|---|---|---|
| Bourbon Central | **0.781** | 0.823 | 0.656 |
| Bourbon County High | **0.736** | 0.793 | 0.567 |
| Cane Ridge | **0.662** | 0.728 | 0.465 |
| **North Middletown** | **0.634** | **0.773** | **0.217** |
| Bourbon County Middle | 0.574 | 0.596 | 0.508 |

The page (`:335`) reports **only the Condition Index**, the single column where NMES beats Cane Ridge, and concludes: *"The building proposed for closure is, on the state's own newest data, the healthiest small asset the district owns."*

The same row carries:

- **Kentucky School Score — the state's own overall figure for the building.** NMES is **fourth of five**, below Cane Ridge and well below Bourbon Central. This metric appears nowhere on the site.
- **Educational Suitability 0.21725 — the worst in the district by a factor of two**, against 0.465 at Cane Ridge and 0.656 at Bourbon Central. It appears once, as a *data-provenance* caveat ("identical to five decimal places to 2023, so that half of the aggregate appears carried forward rather than re-surveyed") rather than as a substantive finding. The staleness caveat is fair and correctly flagged — but a reader is never told that the number itself is the district's lowest, or that it is roughly a third of the receiving schools'.

A district responding to this site will lead with the Kentucky School Score. Publishing it first, with the argument about why Condition Index is the right measure for a keep-or-close decision and why a carried-forward suitability score should not be relied on, is a far stronger position than having it produced in rebuttal.

One further caution on the condition claim itself: between the Oct 2023 and Oct 2025 reports — the *same inspections, costs updated* — Bourbon Central's index moved **−0.068 on re-costing alone**. NMES's celebrated improvement is **+0.071**. The index is a ratio of repair cost to replacement cost; both move with construction-cost escalation. The claim "the only school whose condition improved" is accurate as stated on the 2020-21 → April 2026 comparison, but it is endpoint-sensitive (Bourbon Central improved on the most recent transition too), and the site's own data shows the metric can move seven points with no physical change.

---

## 3. Inference and framing

Not errors. Places where the argument claims more than the evidence carries, and where a competent opponent will push.

### 3.1 "The district's best elementary school" versus the state's actual headline number

The `og:description`, the hero, and the Part Two headline all assert NMES is the best elementary school in the county. On the state's **official 2024-25 overall accountability score** — the number Kentucky itself calls the school's score — NMES is **54.0 against Bourbon Central's 55.4**: second of three.

The site handles this at length and its explanation is legitimate: the composite blends status with year-over-year change, and NMES is being charged for its own 2023-24 spike. The status-measure table added in the most recent commit is genuinely good work.

But note what results: **the one number the state calls the overall score is the one number that appears in no table on the site.** It is discussed in prose twice and drawn as a line that crosses. Everything else — five subject proficiencies, five content indexes, two survey indexes — is tabulated. That asymmetry is exactly what a hostile reader looks for, and it is unnecessary: the site's own explanation is strong enough to survive printing the number.

Two related pressure points:

- **The volatility is treated asymmetrically.** NMES's composite runs 51.9 → 62.2 → 74.5 → 54.0 in four years — swings of ±20 points on a school with roughly twenty tested students per grade. The 74.5 is cited as evidence ("first by fourteen points"); the 54.0 is explained as a formula artifact. Both years are equally noisy. The site itself concedes the point elsewhere — SchoolDigger is "unreliable year to year for a school of NMES's size" — and then rests the hero fact on single-year subject rankings.
- **No uncertainty is reported anywhere.** "1st in all 5 reported subjects" rests on gaps like 41 vs 38 in reading and 31 vs 28 in mathematics, across a tested cohort in the dozens. Those differences are inside sampling noise. Meanwhile three of the five subjects are **below** the state average (reading 41 vs 49, mathematics 31 vs 43, social studies 36 vs 38) — disclosed accurately in the lede, but not in the fact strip that most readers will see. A site that asks the district to publish its worksheet should publish its own error bars.

### 3.2 The thirty-year closure record proves less than it is asked to prove

*"No case exists of a Kentucky district closing a rural town's elementary school, clearly saving money, and clearly improving scores. If the board believes it will be the first in thirty years, show us the data."*

This is the most quotable sentence on the site. It is also close to statistically vacuous, and for a reason the site itself supplies.

- The joint condition requires **two** noisy binaries to fire together. The site's own outcome data: of 42 measurable events, **11 improved, 10 declined, 21 flat** — a coin flip. If roughly a quarter of closures show clear gains and some similar fraction show clear savings, then across the small number of true rural-elementary comparables (the site names four), the *expected* count of joint successes is well under one. **Finding zero is what chance predicts.** Absence of a precedent in a handful of cases is not evidence that the precedent is impossible.
- **"40 percent of districts spent MORE than trend after closing"** is presented as damning. But the site argues, correctly, that the per-displaced-student measure is dominated by district-wide budget noise — the tails run past ±$13,000 per child, "more than any school even costs to run per student." Under pure noise the expected negative share is **50%**. Forty percent is, if anything, weak evidence *for* savings. The null is never run.
- **The measurement error swamps the estimate.** A method whose noise is an order of magnitude larger than its median ($1,102) cannot establish that savings of $6,250 are unattainable; it can only establish that this method cannot see them. The site is half-aware of this — it is exactly why the bottom-up model exists — but the histogram and the "40 percent" are still deployed as evidence rather than as a demonstration that the record is uninformative.

The narrower claim the data *does* support is already in the note at `:392` and is strong: *"no measurable precedent exists for the savings or the improvement this plan promises."* That is defensible. The thirty-years-and-never framing is not, and it is the version that will be quoted back.

### 3.3 The $6,250–$7,813 yardstick attributes to the closure a requirement the site says is not the closure's

The chart at `:391` labels the red bar **"THE PLAN: no new school, $800K to $1M required"** and prices it per displaced NMES child.

But the $800K–$1M is, on the site's own account (`:212`), what the superintendent said the district must **free up in operating money to bond $14 million** — from any source. And the site says so explicitly at `:215`: *"Any million dollars a year does that job. The untaken 4 percent levy does it. The alternatives package does it."*

Converting a district-wide bonding requirement into a closure-specific per-child hurdle, then benchmarking thirty years of closures against it, is a rhetorical move the underlying statement does not license. The district will say: *we never claimed the closure alone produces $900,000.* The site would be on firmer ground comparing the record against the administration's own unpublished $900,000 closure figure, flagged as unverified, rather than against the bonding target.

### 3.4 The evidentiary standard is asymmetric between the closure and the alternatives

The closure estimate is held to a 1,944-cell documented grid with published tails, a tornado chart, and a reproducible script. The alternatives menu — the thing that produces the headline "$1.1 to $2.1 million a year" — is compared against it directly in the totalstrip and in the Three Plans table.

The model rates its own alternatives. The page does not surface those ratings. From `Alternatives`:

| confidence | lines | value |
|---|---|---|
| **High** | 4% option; fill NMES | **$369K – $491K** |
| Medium | delinquency, attendance, attrition, admin restraint, transport, energy, district-wide recruitment | ~$1.03M – $1.85M |
| **Low** | Medicaid/E-rate/meals ("needs evidence current claims are being missed"); shared services with Paris Independent ("needs an interlocal feasibility study") | **$200K – $550K** |

So **only $369K–$491K of the $1.6M–$2.9M raw sum carries the model's own "High" rating** — 22% to 34% of it, and well below the published $1.1M floor. The page discloses that confidence ratings exist ("a confidence rating … are in the report and the downloadable model") but shows none of them, while the closure number opposite it is decomposed to seven levers on the page itself.

A specific instance of the same asymmetry: the page prints a fair caution that the 44.8% central-office growth may be *"accounting rather than hiring"* because Kentucky audits fold pension allocations into those lines — and then books **"Trim central-office growth back toward its FY2023 level: $224,000 to $450,000,"** whose high end is a full rollback of the very growth just flagged as possibly not real. `Assumptions!B47` sets the rollback share at 0.5 and labels it "Judgment call." Either the caveat or the high end should move.

### 3.5 The fill plan's largest lever is asserted, not measured

The planner's default moves **30 of 46 seats** by rezoning "students from the Paris-area zones," on the stated assumption that these are *"families already living closer to NMES than to the Paris schools"* (`Redistricting!C12`). No count of such students is ever produced. The page concedes it — *"an assumption the district can test against its real routing data"* — and then books the revenue in the alternatives table anyway.

Two smaller stretches in the same section:

- **"Filling NMES's 46 open seats takes fewer than one in five of the registered homeschoolers alone."** True arithmetic (46 ÷ 259 = 17.8%), but 259 is a **K-12, county-wide** count across two districts. NMES is a **K-5** school with a defined zone. The addressable pool is a fraction of 259, and the page does not say so.
- **The published $56K–$116K package range** varies only the two section sliders while freezing the student mix at 30/16/0. Changing the mix moves the answer a long way (46 transfers instead of 30 rezoned + 16 transfers gives roughly $194K before section costs). The alternatives table presents $56K–$116K as *the* range for "Fill NMES to capacity."

### 3.6 Millersburg

The disclosure discipline here is good — the two schools are carefully distinguished, Joy Global is named, and the note concedes that towns keeping their schools declined at nearly the same rate. One thing is missing from the chart's story: on the site's own indexed series, Millersburg fell **117.2 → 100.0 between 1980 and 2000 (−15%)**, a steeper decline than the **−11%** it experienced in the twenty years *after* the closure. The chart annotates the closure on a line that was already falling faster beforehand. Saying that explicitly would cost nothing and would pre-empt the obvious rebuttal.

---

## 4. Presentation, engineering, and editorial

### 4.1 The call to action is stale

`index.html:606` — the first and most prominent "Act Now" card is **"Show up Thursday — July 23 • 6:30 p.m."** Today is **July 28**. That meeting has passed. The second card, the July 29 planning-committee forum with public comment, is **tomorrow** and is the live one. On an advocacy site whose whole purpose is turnout at the next meeting, a past event in the lead card is the highest-cost defect on this list per unit of effort to fix.

### 4.2 A CDN failure silently kills all three calculators

`index.html:19` loads Chart.js from `cdnjs.cloudflare.com` with **no `integrity` / SRI attribute**. `index.html:768` then opens the entire application script with:

```js
if(typeof Chart==='undefined'){return}
```

The closure calculator, the levy compounder and the fill planner are **all defined after that guard**. If the CDN is blocked, slow, or unreachable — a school-district firewall, a rural connection, a corporate proxy — every chart renders as an empty box *and* every slider goes dead, while the page continues to display its hard-coded default values ($131,240, $977,568, $55,616) as though they were computed. The reader sees numbers and cannot move them, on a page whose thesis is "run the numbers yourself."

Two fixes, both small: move the calculator block above the `Chart` guard (or wrap only the chart code), and add SRI plus a vendored local fallback — `tests/vendor/` already holds a Chart.js copy for the browser tests, so the asset exists in the repo.

Separately, a third-party script with no integrity hash is a poor fit for a site whose credibility rests on document provenance.

### 4.3 The "fair test" table is hard-coded and its staffing rule is not uniform

`Redistricting!B103:D109` are **literal numbers, not formulas**. The rule is stated in `A101` ("$400 per student added or removed, plus or minus $85,000 per section vs today's staffing"), but the section deltas are described as "precomputed" and are not shown. Back-solving every cell recovers clean integers, so the arithmetic is sound — but the implied rule is not uniform:

| scenario | NMES | Bourbon Central | Cane Ridge |
|---|---|---|---|
| 2013 plan | +70 students, 3 sections (23/section) | +73, 2 (36.5) | **+39, 0 sections** |
| 2017 plan | +24, 1 (24) | +120, 6 (20) | +89, 2 (44.5) |
| 2021 plan | +46, 2 (23) | +30, 1 (30) | −39, **−4** (9.75) |
| peak 20-yr | +96, 3 (32) | +129, 6 (21.5) | **+34, 0 sections** |
| 2026 architect | +26, 1 (26) | **+8, 0** | −64, −4 (16) |
| 2026 draft | +26, 1 (26) | +149, 6 (24.8) | +86, 2 (43) |

Students per section crossed ranges from 9.75 to infinity. The page claims *"all three schools under the same rules"* (`:280`). Strictly, they are not.

**But:** almost every deviation runs **against** the author's conclusion (Cane Ridge absorbing 39 students free, Bourbon Central absorbing 73 at 36.5 per section, NMES paying 23 per section), and as noted in §1, imposing a genuinely uniform rule changes **no verdict in any of the six scenarios**. The fix is auditability, not arithmetic: make the cells formulas, publish the section deltas, and either drop the "same rules" phrasing or make it true.

### 4.4 The test suite proves internal agreement, not external validity

`sync_check.py` reports "63 matches, 0 discrepancies." Read the check names: every one is *site vs. model vs. PDF*. Not one compares a number to its cited source document. The suite would pass just as cleanly if a figure were wrong in all three artifacts — which is exactly the failure mode a project generating three artifacts from one author is most exposed to.

It also demonstrably missed the two internal contradictions in §2.1 and §2.4: it asserts the calculator's `-$278,780` as the unfavourable tail while `validate_all.py` separately confirms the site text says `-$385K`, and nothing checks the facility table's "90 open" against the note directly beneath it. Three cheap additions would close most of this: assert the calculator's reachable extremes equal the grid's published tails; assert every "(N open)" cell equals rating minus enrollment for the rating named in its own footnote; assert the busing range is identical across Assumptions, the grid script and the slider bounds.

Note also that the suite cannot run as documented: `README.md` says `pip install reportlab openpyxl matplotlib` and `pip install playwright`, but `validate_all.py` and `sync_check.py` both require **`pypdf`**, which is not listed anywhere.

### 4.5 Smaller items

- **Enrollment series** (`:874`): four pairs of identical consecutive values (2000–01 at 195, 2013–14 at 154, 2017–18 at 131, 2019–20 at 160) and a +29 one-year jump from 131 to 160, suggesting some carried-forward or imputed CCD values. Worth naming the vintage.
- **Two enrollment vintages are mixed without comment.** "NMES stood 93 percent full against its rating as recently as the 2021 plan" uses the plan's count of 161; the chart on the same page shows 148 for 2021 (85%). Both are real, from different sources — say which.
- **"The building held 261 children at its peak"** is the first value of a series that starts in 1989, for a school that opened in 1948. It is the peak *of the available record*.
- **`Closure_Model!A55`** still reads **"MILLERSBURG, 2007"** and `C56` still says "closed 2007", after v3.5 corrected the closure year to 2006 across the site and report. Cosmetic, but it is in the workbook the site invites people to download, and the correction is one the site advertises having made.
- **The tornado chart** (`:910`) labels ranges "Positions eliminated (2 to 5)" and "Cost per position ($50K to $75K)" that do not match the sliders directly above them (2 to 6, $50K to $85K).

### 4.6 Editorial and privacy

The Voices section has a stated consent protocol — identity confirmed, permission in hand, removal on request — which is more than most advocacy sites manage. Two things still sit uneasily:

- **Living private individuals are named without any indication of their consent.** The stories name roughly twenty current and former teachers and staff by name (several with married-name changes noted). The consent obtained is the *author's*, not the named teacher's. These are private people whose names are now attached to a live political dispute on an indexed public site.
- **One story identifies a named parent's minor child by disability** ("a child with Stage 1 autism") in a school with 128 students. The parent consented; the child cannot. In a cohort that size this is effectively identifying. Consider redacting the diagnosis while keeping the point about small-group instruction, which survives without it.

Both are the author's call, not errors. They are flagged because the site's own footer promises care, and because a district communications officer looking for a way to change the subject will look here.

---

## 5. Priority

**Fix before the July 29 forum:**

1. The stale July 23 card (§4.1) — one line.
2. The "90 open" cell (§2.4) — one number.
3. Move the calculator block above the Chart.js guard (§4.2) — three lines.

**Fix before the number is quoted again:**

4. Reconcile the calculator with the grid, or state plainly on the page that the sliders explore a wider space than the published range (§2.1).
5. Correct "every one of them comes from a document" (§2.2). The estimates are fine; the sentence is not.
6. Correct "audited" → the dollar total is audited, the cent split is not; drop "real estate only, so the figures are conservative"; re-derive the levy options on a real-estate-only yield and restate the $4,551 margin honestly, even if it becomes a shortfall (§2.5).
7. Pick one busing range and use it in all three artifacts (§2.3).
8. Either document criteria 4–6 or change "when it meets that standard" to "when it meets the criteria it can be shown to meet" (§2.6).

**Strengthen before the district responds:**

9. Publish the Kentucky School Score and the Educational Suitability figures with the argument for why the Condition Index is the right measure, rather than waiting to have them produced in rebuttal (§2.7).
10. Put the 2024-25 official composite (54.0 vs 55.4 vs 47.8) in a table alongside the status measures (§3.1).
11. Narrow the thirty-year claim to the version the data supports, and add the noise null (§3.2).
12. Surface the model's own confidence ratings on the alternatives table (§3.4).
13. Add error bars, or a sentence on cohort size, to the subject rankings (§3.1).

---

## 6. Overall

The document survives adversarial review better than most published advocacy analysis. Its sourcing is real, its archive is real, its corrections are real, it has repeatedly published findings against itself, and its central empirical claims — that NMES's per-student premium is a function of enrollment rather than management, that the receiving schools have roughly 31 uncommitted seats for 128 children, that the closure's plausible yield is a small fraction of the district's gap, that the district's own capacity ratings have moved by more than a hundred seats without construction — held up against every check I could run from the repository.

The failures are not fabrications. They are the failures of a fast-moving one-author project: three artifacts drifting apart (§2.1, §2.3), a claim about sourcing that outran what the model says (§2.2), a metric selected within a source file whose other columns are unflattering (§2.7), a rhetorical frame that is stronger than its statistics (§3.2, §3.3), and an evidentiary standard applied more strictly to the opponent's number than to its own (§3.4).

Every one of those is exactly what an opponent needs to change the subject from the argument to the arguer. On a site that stakes everything on "check my work," the fixes above are cheap, and they are worth more than any new evidence.

---

*Prepared as an independent adversarial review at the author's request. Findings are reproducible from this repository at commit `ce4e481`; the commands used are in the review's working notes. Where this review disagrees with the site, the site's own sources — not this document — should settle it.*
