# Hardening Guide for "Saving North Middletown Elementary"

**For:** the author, Dr. Ryan Bradley
**Date:** July 20, 2026 (Version 2.2 of the report; three days before the July 23 meeting)
**Built from:** six independent adversarial reviews (finance, academics and
enrollment, busing and geography, facility capacity, external verification,
and a full steelman of the district's case), each run against the workbook,
the build scripts, the archived primary sources, and reachable public data.
Detailed evidence lives in `review/01_...md` through `review/06_...md`;
the prioritized findings are in `review/ADVERSARIAL_REVIEW.md`; the data
pulls you still need are in `review/NUMBERS_TO_VERIFY.md`.

**The verdict in one paragraph.** The core thesis survives hostile review.
The audited deficit is real, the closure arithmetic nets correctly (and
generously omits receiving-school costs), the geometry reproduces exactly
from the raw federal data, the facility-plan figures are transcribed letter
for letter from the district's own documents, and the site is current. The
exposure is concentrated in packaging: one contaminated calculation, one
mislabeled headline metric (already fixed on the austin-dev branch), two
internal contradictions, and about six sentences that breach your own
no-motive pledge. Every fix below is cheap, and the corrected numbers still
win the argument. Fix them before opponents find them, and the remaining
document is genuinely hard to discredit.

**Already done on austin-dev (commit 74cafab):** the SchoolDigger score is no
longer called "the state's own accountability composite" anywhere; the actual
statewide ranks (NMES 272nd of 685, Bourbon Central 545th, Cane Ridge 575th)
now appear in the PDF and on the site; "consistent cross-year yardstick" is
corrected to "same-year comparison across schools." PDF rebuilt, all tests
pass.

---

## Part 1. Before Thursday, July 23 (human tasks, ~30 minutes total)

1. **Confirm the meeting venue today.** Site and PDF say North Middletown
   Community Center; WKYT (July 17) told viewers "at the school." Same
   event, same time. Whichever is wrong, fix it: `index.html` "Show up
   Thursday" card and PDF p.3 timeline, or ask WKYT to correct. Sending
   families to the wrong building is the worst possible failure mode.
2. **Click the petition link.** The change.org URL under the primary CTA
   could not be reached from the review sandbox. If dead, fix `#petitionBtn`.
3. **Open savenmes.org** and confirm it serves the current repo (search the
   page for "272nd" once the branch is merged; if it is absent, the deploy
   is stale).
4. **Pull the official 2024-25 KDE data** from reportcard.kyschools.us for
   all three schools: the Overall Performance color rating, the four
   elementary indicator values, and percent Proficient/Distinguished by
   subject. This one pull unlocks fixes 2.1, 3.1, and 5.1 below and is the
   highest-value twenty minutes available.

## Part 2. Two data corrections to make the moment you have the KDE pull

### 2.1 Check whether the NMES "reading 50 / math 44" line is a transcription slip
The report says NMES matches the state average in reading (50) and math
(44). Those two figures exactly equal the state averages quoted in the same
sentence, and the reachable school-level fragments differ (5th grade reading
54, 4th grade math 41; the statewide elementary figures in the November 2025
release coverage were 49 and 43). If state averages were copied into the
school column, correct: PDF Section 5 ("The profile beneath the composite"),
workbook `School_Data!B30:C33`, and any site echo. If the numbers are
genuinely identical, add "coincidentally identical to the state average" so
nobody thinks it is a copy error.

### 2.2 Verify and then use Bourbon Central's TSI designation
A search snippet of KDE's 2025-26 Targeted Support and Improvement roster
(education.ky.gov/school/focschls) shows Bourbon Central identified for the
students-with-disabilities subgroup. Verify the PDF directly. If confirmed,
cite it wherever the receiving schools' performance is discussed: an official
federal-state designation is stronger than any third-party score and cannot
be dismissed as "a website." No designation was found for Cane Ridge or NMES.

## Part 3. The five highest-value number fixes (before any board submission)

### 3.1 Lead with the official rating and the three-year averages, not 58.2
Once you have the KDE colors, present them first, then the three-year
SchoolDigger averages (48.1 vs 26.4 vs 29.9), then the 2024-25 single year
(58.2, 272nd of 685) as supporting detail. The single-year hero is the best
year of a noisy series: NMES's standard deviation is 14.7, and in 2023 it
scored 32.1, below Cane Ridge. The averages are your armor because they
include your worst year. Add the sentence that defuses the district's best
counter in advance: "North Middletown's worst year of the current
assessment era (32.1) still beat Bourbon Central's best (29.9)."
Locations: site hero fact strip, PDF executive summary, Section 5 opening.

### 3.2 Rebase the levy path on General Fund collections only
The $386K / $787K / $1.2M path applies 4 percent to $9,641,017 of total
collections, which includes roughly $2.05M of restricted FSPK and
debt-service tax (`Tax_History!B33`), money your own report says cannot pay
a teacher. Your workbook already computes the correct version: Alternatives
row 4 uses the GF-only base (about $7.83M, so about $313K in year one,
$639K in year two, $978K in year three, roughly 37 percent of the deficit).
Fix `Tax_History` (B48 and the path rows), the site calculator constant
(`var base=9641017` in index.html), and PDF p.21. The corrected levy still
raises about 2.7 times the closure base case; take the haircut before a CFO
takes it for you. Also make `Tax_History!B37` a formula
(`=Assumptions!B24-B21`) instead of a hardcoded 2,648,086.

### 3.3 Publish the absorption reconciliation and widen the calculator
The 3-positions assumption is defensible only as a NET number (nine NMES
sections closed, roughly six re-created at receiving schools under the
KRS 157.360 caps), but nothing user-facing states that reconciliation, and
the site slider stops at 6, which hides the district's scenario. Fixes:
- Add a grade-by-grade table (their published enrollments, added students
  per grade per receiving school, where caps force new sections) to Section
  4 and a workbook tab.
- Raise the slider max to 9 or 10 and show that even at 8 net positions the
  saving is about $786K, still under a third of the deficit. The thesis
  survives the honest version; it does not survive being caught hiding it.
- Reconcile the elasticity contradiction: the Redistricting tab credits 1-2
  sections avoided for moving only 30 students, while closure of 128 frees
  only 3. Either haircut the Redistricting section credit (restate the
  fill-to-capacity line as roughly "$56K firm plus up to $170K contingent
  on section relief") or state explicitly why the elasticity is asymmetric
  (adding 10 per grade forces new sections at caps; removing 5 per grade
  rarely closes one).

### 3.4 Present every percentage against both denominators
The belittling shares (13.6, 24.2, 45.5 percent) divide by the pre-transfer
$2,648,086 gap; the runway math divides by the actual ~$1.15M drawdown. A
CFO recomputes in one slide: closure is 31.5 percent of the drawdown. Add a
small table showing each figure both ways, and lean on the ratio that is
denominator-proof: the levy raises about three times what closure saves
under either measure. Also update `Scenarios!E6`, which hardcodes "13.6%"
and "24.2%" as text.

### 3.5 Fix the capacity presentation (three edits)
- **State both Bourbon Central numbers.** 549 is the "To Become" figure for
  an unbuilt after-biennium project; the current 2021 rating is 521 (the
  workbook already holds it in `Facility_Plans!E7` while B13 hardcodes 549).
  The correction strengthens you: at 521 the net uncommitted seats fall
  from 59 to 31. Quote the plan's own "To Become 564/549" line, which
  projects Bourbon Central over capacity even after the project.
- **Rewrite "The seats are not there."** The district's own filings show its
  schools operating 13 to 38 percent over rating, so the flat impossibility
  claim collapses. Your FAQ already has the defensible form; use it
  everywhere: "Within the district's own current ratings the seats are not
  there; absorbing 128 children requires re-rating rooms, adding sections
  under the class-size caps, or capital work, none of which the district
  has costed or published."
- **Unify the framing.** Do not treat rated capacity as a soft "policy
  output" for NMES and a hard wall for the receivers. Shift the receiving
  constraint to physical facts: classroom counts, the Preschool Center over
  capacity in both plans, Cane Ridge at 453 in a building rated 422. And
  source the 459/453 receiving enrollments to a dated official count (the
  model self-flags them; SchoolDigger's 2024-25 page shows Bourbon Central
  at 483, so this number is live).

## Part 4. The credibility scrub (six sentences, one hour)

Your pledge (PDF p.28, README, site footer): "attributes no motive and
alleges no wrongdoing." Opposing counsel reads these aloud next to it.
Keep every fact; delete the innuendo.

| Location | Current | Replace with |
|---|---|---|
| PDF p.16 | "A school that stood 93 percent full against its rating in the 2021 plan did not become surplus in four years by itself." | "The records requested in Appendix B would show how much of the decline each of these decisions explains." |
| PDF p.12-13 | "the same pencil can raise North Middletown's rating back toward the 198" | "capacity ratings follow room assignments under 702 KAR 4:180, so they can be raised by the same lawful process that lowered them" |
| PDF p.13 | "at what point does deferred investment itself become the closure case?" | "the maintenance and project records in Appendix B would show whether the 2013-priced work was completed" |
| PDF p.11 / Appendix B | "Not improper in itself, but..." and "Where $6.9 million of recent borrowing went" | Delete "Not improper in itself"; Appendix B row: "The 2024 bond's stated project scope (official statement and BG-1)" |
| PDF p.6 / p.20 | "run exactly this play" / "extracting it from one town" | "tried this consolidation math" / "rather than concentrating it on one school" |
| Site hero/OG | "the one on the chopping block" / "The school they want to close is the one that works." | "The district's highest-scoring elementary is the one proposed for closure. Here are the numbers." |

Two smaller tone edits: soften the superintendent parenthetical ("public
statements and federal records differ, about 100 versus 128; Question 2
asks which count the analysis uses"), and change Appendix B's "The building
case, if one exists" to neutral phrasing. Also change the p.1 caveat from
"every figure should be re-verified" to "figures verified against the cited
primary sources as of [date]" once Part 1.4 and Part 2 are done; keep the
AI disclosure, pair it with the human verification statement.

## Part 5. Additions that close open flanks (before the board vote)

1. **A three-school demographic table** (FRL, EL, IEP, mobility) from the
   KDE report card, in Section 5 and the workbook. The district's natural
   rebuttal is "different population"; the reachable data suggests NMES is
   the poorest of the three, which converts their attack into your exhibit.
   Reconcile the internal FRL spread (73.8 to 93 depending on source) with
   one conservative figure and a community-eligibility footnote.
2. **A program-breadth section.** The materials are silent on specials,
   counselors, interventionists, and special-education delivery, which is
   every superintendent's lead academic argument for consolidation.
   Document what NMES students actually receive versus the receiving
   schools, and cite the small-schools literature already in your sources.
3. **Model Plan 4 (closure plus the menu) yourself.** It nets only about
   $100-200K more per year than Plan 3 before enrollment-loss risk (30
   leavers erase $139K), transition costs, and the closure under-delivery
   record. Owning the comparison converts the report's weakest structural
   omission into its strongest line: closure adds at most about 6 percent
   to the recovery plan and risks a school and a town to get it.
4. **Publish the alternatives haircut arithmetic.** Show raw sum, minus
   mutually exclusive lines (multi-age and fill-to-capacity cannot both
   happen), minus low-confidence lines, equals the range. Make the low
   bound only high and medium confidence items (about $800K), which still
   beats the $640K best closure case. Fix the site menu so its rows sum to
   the range it asserts, and resolve the attrition double-claim (the same
   retirements cannot staff both the closure case and the alternatives).
5. **Local co-signers.** Kentucky's open-records act limits requests to
   Kentucky residents, and the report states Bourbon County is no longer
   your home, so the district can lawfully deny your Appendix B requests.
   Have named local residents file them and co-sign the report; this cures
   the standing defect and the out-of-town-messenger attack in one move.
   Prioritize five requests (net-savings worksheet, condition assessment,
   bond official statement and BG-1, T-1 transportation report, capacity
   worksheets) and mark the rest follow-ups.
6. **Rewrite the mass-email template** to ask one question ("Will the board
   publish the net-savings worksheet before voting?") and encourage
   personalization; form-email bombardment hardens boards.

## Part 6. Smaller hardening items (as time allows)

- Busing: change "validates the $137,500 midpoint" to "brackets it" (your
  own bottom-up math centers near $99K), and add the scenario where
  elementary riders are absorbed into the existing 6-12 routes to Paris,
  which the report never mentions.
- Change the closure range ceiling to "$250K to $650K" (the current $600K
  ceiling sits below your own $640K district-favorable case).
- Deficit quality: publish the FY2025 gap net of identifiable one-time
  items (the ~$888K and ~$691K bus purchases); owning about $2.0M clean is
  stronger than defending $2.65M live.
- Split the $85K loaded cost into district-paid (about $62K) and state
  on-behalf, and rerun both closure and alternatives on the same number
  (the conclusion survives; the asymmetric use does not).
- Lead per-pupil with the state and local $14,173; keep $19,348 as the
  footnoted total (it includes about $5,175 of federal money the district
  neither keeps nor saves).
- Add the SABS 2015-16 vintage caveat to the site's map card (the PDF has
  it, the card does not), pin timestamped Wayback capture URLs for both
  DFP excerpts in `dfp_manifest.json`, and cite a source for the 10.0-mile
  US-460 measurement.
- Demote Boston to a footnote ceiling and lead the routing precedent with
  Fayette and Jefferson County; reconcile the 50-versus-400 bus figure or
  drop it.
- Label the KRS 157.370 point precisely: the density calculation is
  district-wide, and the zero marginal reimbursement on new miles holds
  "under the current biennium's appropriation."
- Date-stamp the $23.5M bonding capacity ("as of the FY2024 audit, before
  the 2024 issue") and pre-state the CTE counter: the capacity math
  supports building the career center and keeping NMES.
- Cite one instance of a KDE facility-plan waiver or soften "has granted
  other districts" to "the regulation permits a waiver request."
- Date-stamp the "93 percent full" claim (the plan's 161 count versus your
  series' 148 for 2021), print the current 74 percent utilization in your
  own voice under both denominators (174 and 198), and replace "four years
  old, not a generation old" with the stronger rebound argument: enrollment
  fell to 131 in 2017-18 and refilled to 160 within two years.

## Part 7. Do not weaken these (they survived everything)

- The audited $2.65M gap's existence (actuals, not budget figures), the
  $4,290,840 fund balance, and the ~$1.15M drawdown pace.
- The two-pots-of-money architecture and the restricted-versus-operating
  presentation (which is exactly why fix 3.2 matters).
- The SEEK-per-leaver deduction (conservative: base only, no add-ons).
- The closure calculator's netting (verified end to end, no double counts,
  and it generously books zero receiving-school costs; add a visible $0
  placeholder row so the conservatism shows).
- The geometry pipeline (reproduces exactly; the area-weighted assumption
  most likely understates your case, since the town sits at the school).
- The 1.2 road factor (bottom of the literature band; conservative).
- The density contrast (1.2 versus 5.1 per square mile; understated in
  your favor because Paris Independent's in-town students are excluded).
- The facility-plan transcriptions (letter for letter against the archived
  documents) and both plans' "Permanent" classification for NMES.
- The three-year score averages and the "worst year beats their best" fact.
- The ten-questions device, the falsifiable fall-2028 checkpoint (pair it
  with a reciprocal district commitment), and the corrections policy.
- The honest concessions (enrollment decline is real, the deficit is real,
  the AI disclosure): they are the credibility that makes everything else
  land. The fixes above exist to protect that credibility, not to spin.

## Suggested work order

1. Part 1 (today, thirty minutes, human only).
2. Part 4 scrub plus fixes 3.2 and 3.5 (one evening; pure edits and a
   rebuild; removes opposing counsel's three fastest wins).
3. Part 2 and fix 3.1 the moment the KDE pull lands.
4. Fix 3.3, 3.4 and Part 5 before any formal board submission.
5. Part 6 opportunistically.

After every edit: `python tests/run_all.py`, then rebuild the PDF and model
per the README so the three artifacts stay synchronized; the suite pins the
shared numbers and will catch drift.
