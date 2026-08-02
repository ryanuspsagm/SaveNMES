# Save North Middletown Elementary

Community analysis opposing the closure of North Middletown Elementary School
(Bourbon County Schools, Kentucky). Written by Dr. Ryan Bradley, a former NMES
King, with the help of an AI research assistant. Every figure traces to a
public source cited in the report and on the site.

## What is here

- `index.html` - the interactive community website (single file, no build step;
  charts via Chart.js CDN). Edit text directly; sections are labeled.
- `Saving_North_Middletown_Elementary.pdf` - the 60-page report.
- `SaveNMES_Executive_Summary.pdf` - the two-page executive summary (built by `build/build_summary.py`).
- `NMES_Financial_Model.xlsx` - the 17-tab financial model (452 formulas).
- `build/` - Python scripts that regenerate the PDF, model, and report charts.
  Requires: `pip install reportlab openpyxl matplotlib`. Run
  `python build/make_charts.py`, then `python build/build_pdf.py`,
  and `python build/build_model.py`. `python build/fetch_sabs.py` pulls the
  official 2015-16 federal attendance boundaries (NCES SABS) into
  `build/sabs_zones.json`, already committed here; the map figure redraws from
  them automatically; `python build/zone_distances.py` then computes the
  actual zone distances the busing math uses. `python build/fetch_dfp.py` (run it on a machine with
  normal internet access) downloads the district's current District Facility
  Plan from KDE plus every distinct historical version held by the Wayback
  Machine, the documents that set each school's rated capacity and
  classification; commit the resulting `dfp_*.pdf` files and the capacity
  analysis picks them up. The district's current facility plan (KBE August 2021) and an excerpt of the
  prior plan (KBE June 2013, from the Wayback Machine) are archived as
  `build/dfp_current.pdf`, `build/dfp_2013_excerpt.png`, and
  `build/dfp_2021_excerpt.png`, with provenance in `build/dfp_manifest.json`;
  they back the capacity analysis and the model's Facility_Plans tab. The SABS fetch script uses a saved
  `sabs_zones_raw.json` if present, then tries the NCES REST endpoint, and falls
  back to the EDGE bulk download (`SABS_1516_SchoolLevels.zip` in `~/Downloads`,
  or set `SABS_ZIP`), so it works without a reachable NCES server - which
  matters, because that endpoint is currently returning HTTP 500.

## Tests

`python tests/run_all.py` runs the whole suite:

- `tests/validate_all.py` - cross-file consistency: page, tab, and formula
  counts; figure numbering; meeting details; board roster; local assets;
  the no-dash rule; pagination quality; headline claims.
- `tests/sync_check.py` - every shared number checked three ways: site
  JavaScript vs workbook cells vs report text.
- `tests/test_site.py` - browser tests for the calculators, charts,
  toggles, anchors, and mobile layout (needs `pip install playwright`
  and a Chromium; Chart.js is vendored so no internet is needed).

Run the suite after any edit and before any push.

## Live links wired into the site

- Petition: https://www.change.org/p/sos-save-our-school-north-middletown-elementary
- Report and model downloads are served from this repo via GitHub Pages.
- Board contacts: https://www.bourbon.kyschools.us/page/board-of-education

## Hosting

Any static host works. GitHub Pages: Settings -> Pages -> deploy from main,
and the site serves from `index.html` at the repo root.

Corrections welcome. This project criticizes decisions and asks for documents;
it attributes no motive and alleges no wrongdoing to anyone.

## Report version history
Every published version stays available under `reports/`; each report's
corrections section lists what changed and why.
- v3.9 (July 29, 2026): the district's own ledger, plus nine corrections,
  four of which run against this project's own case.
  (1) THE LEDGER. An open records request produced the district's
  "Overall Cost by ORG" summary, its FY2024-FY2026 working budgets,
  payroll reports, salary schedules and the School Council staffing
  allocation. The district codes $1,285,310 to North Middletown against
  the $2,476,544 the 300-student breakeven was built on, and only
  $21,482,445 of a roughly $44M all-funds budget is coded to any school.
  Like-for-like, same year and same all-in basis: $2,611,980 reported
  against $1,593,309 coded, a gap of $1,018,671 in central overhead no
  closure removes. On the coded basis the school's breakeven is 80
  students and it enrolls 128. Published against us in the same section:
  on directly-coded dollars NMES's per-student premium is wider (9.6 and
  12.2 percent) than on the federal basis (3.6 and 6.7).
  (2) THE GRID REBUILT, the largest correction here. The fixed-cost lever
  carried two estimated values ($230,000 mothballed, $290,000 sold), both
  of which assumed every fixed position at the school is eliminated. It
  now carries three MEASURED values from the FY2026 working budget:
  $58,774 (staff reassigned, utilities only), $227,831 (mothballed) and
  $276,928 (sold). Grid goes 1,944 -> 2,916 combinations. Median saving
  $91,240 -> $21,571; negative share 29% -> 45%; range widens to
  -$556,006 / +$551,928. Assumptions B51/B52 re-based to the measured
  $131,724 / $96,107, so the School_Costs breakeven bar of 54 students is
  now formula-driven. The site calculator gains a fixed-cost control and
  now reaches both grid corners exactly, which it never could before.
  The record-vs-model comparison is restated as a bracket, not a
  convergence: the record's $818 per displaced student is an upper bound
  by construction, the bottom-up model now reads $169, and the plan's
  $6,250-$7,813 requirement sits outside both.
  (3) CORRECTIONS. The 99.6 percent statewide figure reattached to the
  $8,255 bar it belongs to (the corrected test fails 786 of 1,151, 68
  percent); the "38 to 69 students" real-breakeven bar withdrawn because
  its low end credited each child with federal money that follows the
  child, replaced by 54 to 69; the $9,848 "empirical marginal cost"
  retired, its sign flipping across every membership pair that can be
  sourced; the five-year growth trio republished as bands (about 16 /
  35-37 / 46-47 percent) with the base-year counts named; "total site
  spending" and "to the dollar" relabelled; the site closure calculator's
  sliders brought back inside the published grid.
  (4) ADMINISTRATION. The 44.8 percent increase decomposed from the
  district's own working budgets: administrative salaries DOWN about 8
  percent, growth concentrated in insurance, statutory tax collection
  fees, accrued sick leave paid at retirement, and professional services.
  Total district payroll FELL 0.7 percent ($30,410,725 to $30,201,047).
  Central office payroll grew 7.6 percent excluding sick leave, all of it
  the business office. Two director roles were consolidated, not added.
  (5) ENROLLMENT. County children aged 5-17 are flat for 25 years (3,594
  / 3,574 / 3,548) while district enrollment fell 10.2 percent. The
  private-or-homeschool share corrected DOWN from "about one in three" to
  450-550 children, 13-15 percent, after locating a single-age-band
  weighting artifact in the survey.
  (6) STAFFING AND RECORDS. NMES runs on 5.5 fixed positions against
  11.5 and 12.25 at the receiving schools, published beside the
  per-hundred ratio that cuts the other way. 33 records line items came
  back "N/A", including every closure, feasibility, boundary and
  ride-time analysis.
- v3.8 (July 26, 2026): correction and new-evidence release. (1) The
  fill planner now charges for new NMES sections under the class caps
  (KRS 157.360), a cost earlier versions missed; the package falls from
  $116,000-$176,000 to $56,000-$116,000, with every corner disclosed
  (minus $64,000 to $176,000). (2) The complete school-level cost
  record published: three reporting systems back to the 2000-01 report
  cards recovered from the Internet Archive, which put all four
  then-elementaries on one scale curve ($2,851 per student plus about
  $332,000 fixed per building, R-squared 0.97) and price Millersburg's
  2000-01 premium ($166,315) beside NMES's today ($155,776). KDE's
  unlisted LEARNING_ENVIRONMENT files (2011-12 to 2016-17), federal
  CRDC school-level salaries, and the NCES school-level finance survey
  are archived under build/. (3) The 300-student breakeven cited at
  the July committee meeting reconstructed from the state files: all-source
  cost (128 x $19,348 = $2,476,544 exactly) divided by state-only
  revenue ($8,305/member in 2022-23 gives 298); the corrected test
  fails every school in the district including both receiving schools,
  and 99.6 percent of Kentucky schools; the real breakeven (fixed base
  vs marginal revenue) was published as 38-69 students for NMES;
  v3.9 withdrew the lower bar and the honest range is 54-69. (4) The alternatives menu reorganized and fully priced as
  a three-move district-wide growth plan, with recruitment beyond
  NMES's seats newly priced ($106,000-$211,000); raw sums now $1.6M to
  $2.9M. New School_Costs model tab carries all of it live.
- v3.7 (July 26, 2026): the recallable levy options beyond 4 percent
  (KRS 160.470), priced at Bourbon's own audited yield of about $191,000
  per cent of General Fund rate ($7,829,060 across 41.0 GF cents). Four
  benchmark rates (match Harrison 57.7, the regional median 60.3 with
  Fayette excluded, Bourbon's own 2018 rate 61.3, Clark 65.5) with the
  cost to the median $211,600 home ($21.16 per year per cent) and the
  direct bond capacity of each. Sequencing result: restoring the 2018
  rate raises $1,699,479, covering the FY2026-trend operating gap plus
  the end of the $1,320,939 capital sweep ($1,694,928) to within $4,551,
  which unlocks roughly $35 million of construction capacity with
  nothing closed. Site levy card, report Section 9, Tax_History rows
  70-91, all formulas live.
- v3.6 (July 26, 2026): fourteen years of school levies across nine area
  districts, from KDE's Local District Tax Levies files (Total Real
  Estate column), cross-checked against the DOR rate books for 2024-2025
  where all nine districts reconcile exactly: every neighbor's levied
  rate rose (Bath +72.3 percent, Scott +38.9, Harrison +34.2, Clark
  +22.2, Fayette +18.4, Paris +17.2); Bourbon County's is the only rate
  lower than in 2012 (-5.4 percent), with the HB 44 rate-vs-revenue
  caveat and Bourbon's own five 4-percent years disclosed. New Figure
  21, site chart, Tax_History rows 56-68, and archived series
  (`build/ky_levy_history_2012_2026.csv`, `build/levy_series.json`).
- v3.5 (July 26, 2026): correction release from a 36-agent adversarial
  audit of the entire case (117 raw findings, 22 confirmed after
  verification, all fixed): Building Fund transfer component $1,098,663
  per the GF ledger (with the packet's own $30 internal discrepancy
  disclosed); Bourbon Central's current approved rating corrected to 521
  (549 is the plan's contingent To-Become figure tied to unbuilt work),
  net receiving seats 31 and draft paper seats 244; avoided sections
  repriced at the GF-borne $60K (fill package $116K-$176K); Millersburg
  closure year corrected to 2006 per the federal record and the distance
  to about nine road miles; FY2026 contingency $1,489,853; "best in
  three years"; science-suppression caveats added; SchoolDigger averages
  labeled; Montgomery four-elementaries caveat; bonding scenario no longer
  double counts the swept building-fund stream ($21M/$25M); the
  1,944-scenario grid enumerated by `build/closure_grid.py`; the full
  30-year closure dataset archived (`build/ky_closure_events_full.csv`
  plus finance and score extracts); outcome statistics restated on the
  refined corpus (42 events: 11 improved, 10 declined, 21 flat;
  displacement gradient -0.38); stale workbook cells and an off-by-one
  cell reference fixed.
- v3.4 (July 26, 2026): the full closure distribution published (163 events
  per displaced student, median $1,102, 40 percent negative, tails beyond
  the physical ceiling shaded as budget noise); case panel rebuilt to rural
  elementaries only after a comparability validation (Adair 2006 added with
  its new-school disclosure; Somerset 1999 and Montgomery 2018 reclassified
  as city grade reshuffles, Montgomery having opened a new elementary the
  same year); the $8,440 small-denominator artifact published with its
  explanation ($541 inside the plausible window); convergence check added:
  the record's plausible median ($818) vs this model's independent
  bottom-up median ($713).
- v3.3 (July 26, 2026): thirty years of Kentucky rural closures tested
  from the federal record (339 closures since 1995; 72 towns lost their
  last school; median district saved nothing vs state or size-matched
  trends; every plausible case pays $2,000 to $4,800 per displaced
  student vs the plan's required $6,250 to $7,813; no case of a rural
  elementary closure with clear savings and clear score gains; Perry and
  Johnson counties disclosed as the record's best cases); new KY_Closures
  model tab; closure datasets archived under `build/` as CSVs.
- v3.2 (July 26, 2026): the recruitment pool, measured three ways (259
  registered homeschoolers in the districts' own 2022-23 records; about one
  in three county school-age kids in private school or homeschool per ACS,
  up from one in eight pre-pandemic; KDE nonresident flows showing the
  district a net importer of 189 with 54 students from Fayette County);
  returning-student lever added to the fill planner and Redistricting tab;
  KDE Non-Resident report and Washington Post homeschool file archived
  under `build/`.
- v3.1 (July 26, 2026): building condition index for every school from all
  three KFICS State Reports the state has published (NMES the only building
  whose condition improved between inspection cycles; smallest four-year
  repair bill in the district); capacity-rule verification (702 KAR 4:180
  unamended since 2008, re-certified March 2025; state reports archived
  under `build/`).
- v3.0 (July 26, 2026): two-tailed closure economics with verified GF position
  costs; capacity scenarios across the 2013/2017/2021 plans, 20-year peaks,
  KFICS, and the draft table; Millersburg case study; version archive added.
- v2.7 (July 25, 2026): June 2026 capital-to-GF transfer; FY2026 close
  decomposition; recallable-nickel triple verification.
- v2.6 (July 20, 2026): bonding story; transport geography.
