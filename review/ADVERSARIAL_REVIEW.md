# Adversarial Review of the Primary Claims

**Date:** July 20, 2026 (three days before the July 23 community meeting)
**Method:** Six independent adversarial reviewers, each attacking one domain of the
project's claims from the district's side: finance, academics and enrollment,
busing and geography, facility capacity, external source verification, and a
full steelman of the district's case. Every headline number was independently
recomputed from the workbook, the build scripts, and the archived primary
sources; the geometry pipeline was re-run from the raw SABS polygon and
reproduced exactly. The repo's own 31-check consistency suite passes; internal
sync was not re-litigated. Full reports are in `review/01_finance.md` through
`review/06_steelman_district_case.md`.

**Headline verdict:** the core thesis survives hostile review. The audited
deficit is real (not a budget artifact), the closure calculator nets correctly
with no double counting (and generously omits receiving-school add-section
costs), the SEEK-per-leaver deduction is conservative, the geometry reproduces
from official data, the facility-plan numbers are transcribed letter for letter
from the district's own documents, and the site is current (no board vote has
occurred; SEEK figures and the 128 enrollment verify against public sources).
What does not survive is the packaging: one contaminated calculation, one
mislabeled headline metric, two internal contradictions, and a handful of
sentences that breach the project's own no-motive pledge. All are cheaply
fixable, and several corrected numbers still win the argument.

---

## P0: Fix before July 23 / before formal submission

### 1. Meeting venue conflict (time-critical, resolve within 72 hours)
The site and PDF say July 23, 6:30 p.m., **North Middletown Community Center**.
WKYT (July 17), the only reachable independent source, says the meeting is
**"at the school."** Same date, time, and program, different building. Sending
families to the wrong building Thursday evening is the worst possible failure
mode for this page. Confirm with organizers today; correct index.html and PDF
p.3, or get WKYT to correct.

### 2. The 58.2 is not "the state's own accountability composite"
The executive summary, Section 8, Figure 7's caption, and the site FAQ all
attribute 58.2 to the state. It is SchoolDigger's proprietary normalized score,
and the workbook's own source note says so: School_Data!A2, "not KDE's official
rating. Confirm vs KDE Open House datasets before formal submission." That
confirmation was never done (and could not be done from this sandbox; KDE was
unreachable). The district can pull up the official KDE report card at the
podium, show a different number, and call the headline fabricated. This is the
single easiest public kill-shot available to them.
**Fix:** pull the official 2024-25 KDE scores for all three schools, present
those as primary, demote SchoolDigger to a supporting cross-year yardstick, and
purge the phrase "accountability composite" everywhere. The underlying
comparison is probably directionally right, so this costs nothing.

### 3. The levy path is computed on a contaminated base (scored Broken as stated)
The $386K / $787K / $1.2M path applies 4% growth to $9,641,017 of **total**
collections, which includes roughly $2.05M of restricted FSPK/debt-service tax
(Tax_History!B33), money the report itself thunders "cannot pay a teacher."
The workbook already knows the right answer: Alternatives row 4 computes the
levy on the GF-only base ($7.83M, giving $313,162 in year one). The model
argues with itself on its flagship alternative, and Tax_History G32 admits the
split is unverified.
**Fix:** rebase on GF-only collections: roughly $313K / $639K / $978K, about
37% of the deficit and 85%+ of the actual annual drawdown by year three. The
corrected levy still beats closure roughly 2.7x. Take the haircut before an
opponent takes it for you, and reconcile Alternatives row 4 with Tax_History.

### 4. The 3-positions assumption is internally contradicted and the calculator hides the district's case
The load-bearing number of the whole campaign ($250K-$600K on the hero strip)
assumes closure cuts only 3 positions. Two problems:
- **Self-contradiction:** the Redistricting tab credits 1-2 sections avoided
  for moving just 30 students out of the receiving schools. Apply that same
  elasticity to 128 students moving the other way and closure frees 4-8
  sections. The project cannot hold both.
- **The slider is capped at 6 positions**, so the site literally cannot express
  the district's scenario. Using the report's own coefficients, 9 sections at
  $85K plus the $290K fixed layer is about $1.05M gross, which retroactively
  validates the superintendent's "over a million dollars."
**Fix:** publish the grade-by-grade absorption reconciliation (9 NMES sections
closed minus N re-created at the receiving schools under KRS 157.360 caps = 3
net), state the classified-staff assumption explicitly, raise the slider to
9-10, and show that even at 8 net positions the saving is about $786K, still
under a third of the deficit. The thesis survives the honest version; it does
not survive being caught hiding it. Either haircut the Redistricting
section-avoidance credit or state why the elasticity is asymmetric.

### 5. Six sentences breach the report's own no-motive pledge
The pledge (PDF p.28, README, site footer): "attributes no motive and alleges
no wrongdoing." Opposing counsel reads these aloud next to it, in order:
- "A school that stood 93 percent full... **did not become surplus in four
  years by itself**" (p.16, the clearest breach)
- "**the same pencil** can raise North Middletown's rating" (p.12-13)
- "at what point does **deferred investment itself become the closure case**?" (p.13)
- "Not improper in itself, but..." and Appendix B's "**Where $6.9 million of
  recent borrowing went**" (p.11, p.30; the report states where it went on the
  same page)
- Site hero/OG: "**the one on the chopping block**," "**The school they want to
  close is the one that works**" (the shareable card is a full register harsher
  than the PDF, and "the one that works" insults the parents of 912 children at
  the schools whose board members the campaign needs)
**Fix:** keep every factual sequence, delete the innuendo clauses, replace each
with the neutral records-ask framing the report already uses elsewhere.
Credibility is the project's main asset; these sentences are ninety seconds of
cross-examination away from spending it.

---

## P1: Fix before board submission

### 6. The denominator switch
Every belittling percentage (13.6%, 24.2%, 45.5%) divides by the pre-transfer
$2,648,086 gap; the runway math divides by the actual ~$1.15M annual drawdown.
A CFO will recompute at the podium: base closure is 31.5% of the drawdown, the
favorable case 56%, an aggressive case ~75%. **Fix:** present every share both
ways in the same table, and lean on the denominator-proof ratio: the levy
raises ~3x what closure saves under either denominator.

### 7. Capacity: the double standard, the 549, and "the seats are not there"
- NMES's 174 rating is argued as "a policy output, not a physical constant"
  while the receiving schools' ratings are treated as hard walls. Same metric,
  opposite epistemics; pick one.
- **549 is not Bourbon Central's current rating.** The 2021 plan says 535/521
  current; 549 sits on the "To Become" line of an unbuilt after-biennium
  project. The workbook holds both (Facility_Plans E7=521 vs the hardcoded 549
  in B13). The error runs against the project: at 521 the net uncommitted seats
  fall from 59 to **31**, which strengthens the absorption argument. State both
  numbers, and quote the plan's own "To Become 564/549" line, which projects
  Bourbon Central over capacity even after the project.
- "The seats are not there" is stated as physical fact, but the district's own
  two plans show its schools operating 13-38% over rating (BCHS 799/704,
  Preschool 272/200, Cane Ridge 480/422). **Fix:** use the report's own better
  framing: within the current KBE-approved ratings the seats are not there, and
  absorbing 128 children requires re-rating, added sections under class caps,
  or capital work, none of which the district has costed or published.
- The receiving-school enrollments 459/453 driving the seat math are
  self-flagged in the model as unconfirmed. Source them to a citable record.

### 8. Lead with the three-year averages, not the best year
The hero "58.2 vs 26.5" is the single best year of a violently noisy series
(NMES SD 14.7; 2023 NMES scored 32.1, below Cane Ridge). The robust numbers
are the three-year averages, 48.1 / 26.4 / 29.9, which include NMES's worst
year ever, and the sentence "our worst year still beat Bourbon Central's best."
Make those the hero; keep 58.2 as supporting detail. Pre-empt the 32.1 attack
and the girls-85.7/boys-28.8 split (retire it or convert it into a program ask)
before the district uses them.

### 9. Model Plan 4 (closure plus the menu) before the district does
Nothing stops the board from doing closure AND the levy AND the non-NMES menu
items. In the model's own arithmetic Plan 4 nets only ~$100-200K/yr more than
Plan 3, before enrollment-loss risk (30 leavers erases $139K), transition
costs, and the literature on closure under-delivery. Owning that comparison
converts the weakest structural omission into the strongest rhetorical line:
"closure adds at most ~6% to the recovery plan and risks a school and a town
to get it." Also: Scenarios E6 hardcodes "13.6%"/"24.2%" as static text.

### 10. The alternatives package needs its arithmetic published
The $1.1M-$2.1M headline is a hardcoded haircut of a raw sum that (a) the
site's own displayed menu cannot reproduce at the top end (rows sum to ~$1.9M),
(b) contains mutually exclusive lines (multi-age reorganization and
fill-NMES-to-174 cannot both happen), (c) double-claims the same attrition
retirements that the closure case uses, and (d) includes lines the model's own
confidence column rates "Low." **Fix:** publish the haircut table; make the low
bound only High/Medium-confidence items (~$800K), which still beats the $640K
best closure case, the one sentence that must survive.

### 11. Busing: "validates the $137,500 midpoint" overstates
The model's own bottom-up estimate is $51K-$147K with a midpoint near $99K;
$137,500 sits in the top third of the project's own computation. Say
"brackets" not "validates," or use the bottom-up midpoint (net saving rises to
~$400K, still under a sixth of the deficit; the thesis is robust to this). Also
model the district's best card: absorbing elementary riders into the existing
6-12 routes that already run from the zone to Paris every day. The report never
mentions those routes.

### 12. Add the three-school demographic table
No FRL/EL/IEP comparison exists anywhere in the materials, which leaves the
district's #1 rebuttal ("different population") unanswered. The public data
suggests the table helps the project (NMES appears to be the poorest of the
three at ~93% FRL, with the highest scores). Also reconcile the internal FRL
spread ("about three-quarters" vs 93%, a community-eligibility artifact) with
one conservative figure and a footnote.

### 13. Utilization and the "93 percent full" claim
The project never prints 128/174 = 74%, and the "93 percent full in 2021" stat
(a) uses the plan's stale 161 count while the project's own series says 148,
and (b) leans on the very 174 denominator the same paragraph attacks. Own the
74% in your own voice, show utilization under both denominators (174 and 198),
and replace "four years old, not a generation old" (falsified by the project's
own chart: 131 students in 2017-18) with the stronger rebound argument: the
school fell to 131 and refilled to 160 within two years.

### 14. The messenger and the records requests
"Bourbon County is no longer my home" plus the AI-assistance disclosure plus
"every figure should be re-verified before formal submission" hands the
district its closing argument, and, sharper: Kentucky's ORA (KRS 61.870(10))
limits requests to Kentucky residents, so the author may be unable to file
Appendix B himself. **Fix:** have named local residents co-sign and file the
requests (this cures the standing defect and the messenger problem at once);
do the re-verification and replace the caveat with "figures verified against
the cited primary sources as of [date]"; keep the AI disclosure. Prioritize
five requests and mark the rest follow-ups; rewrite the mass-email template to
ask one question ("Will the board publish the net-savings worksheet before
voting?") rather than demand.

### 15. Answer the program-breadth argument
The materials are silent on specials, counselors, interventionists,
special-education delivery, and staffing resilience, which is every
superintendent's lead academic argument for consolidation and the one that
moves board members uncomfortable with dollar talk. Document what NMES students
actually receive versus the receiving schools, and cite the small-schools
literature already in the sources (Howley/Johnson/Petrie).

---

## P2: Hygiene and hardening

- **Deficit quality:** up to ~$700-900K of FY2025 spending may be one-time bus
  purchases inside the $2.65M. Publish a "clean structural" figure (~$2.0M)
  net of identifiable one-time items; it is stronger to own it than defend
  $2.65M live. Make Tax_History!B37 a formula, not a hardcoded 2,648,086.
- **$85K loaded cost:** split district-paid (~$62K) from state on-behalf
  pension/health; rerun both sides on the same number (the error roughly
  cancels across the closure-vs-alternatives comparison, so the conclusion
  survives; the asymmetric use does not).
- **Transportation 20.3%:** single-year jump with no FY2023 baseline shown and
  possible capital inside the line; show the multi-year trend net of bus
  purchases, and rebase the 5-10% optimization range on it.
- **$19,348:** lead with the state/local $14,173 in headlines; the total
  including ~$5,175 federal is the least GF-relevant number and the most
  quoted.
- **Range consistency:** the stated closure range "$250K to $600K" has a
  ceiling below the project's own $640K district-favorable case; make it
  "$250K-$650K." Slider bounds (positions max 6, busing floor $75K, leavers
  cap 30) all sit exactly where the narrative stays intact; widen them.
- **Provenance:** pin exact timestamped web.archive.org capture URLs for the
  2013/2021 DFP excerpts in dfp_manifest.json; put the SABS 2015-16 vintage
  caveat on the site's map card itself (it is on the PDF but not the card);
  cite a source for the 10.0-mile US-460 measurement; compute road distances
  per leg (both receiving schools are currently collapsed to one Paris point).
- **Site phrasing:** "about four road miles more each way" should carry the
  "averaged over the zone's area" qualifier the PDF has (student-weighting
  likely makes the number worse for the district, since the town sits at the
  school, so consider publishing a Census-block-weighted mean).
- **Boston:** demote it to a footnote ceiling and lead with the in-state
  Fayette/Jefferson precedents already cited; reconcile the 50-vs-400 bus
  discrepancy or drop the number.
- **KRS 157.370:** add "district-wide" to the density explanation and label
  the zero-marginal-reimbursement point "under the current biennium's
  appropriation" (it flows from the freeze, not the statute).
- **$23.5M bonding capacity:** date-stamp it "as of the FY2024 audit, before
  the 2024 issue," and pre-state the CTE-center counter (the capacity math
  supports building the career center and keeping NMES).
- **KDE waiver claim (p.25):** cite one actual instance or soften to "the
  regulation permits a waiver request."
- **Superintendent parenthetical:** "(federal records show 128)" reads as an
  accusation; reframe as "public statements and federal records differ."
- **Fall 2028 target of 145:** keep the falsifiable commitment, but pair it
  with a reciprocal district commitment so it is not a one-way tripwire.

---

## What was verified and what was not reachable

Verified against live public sources: SEEK $4,586 FY2026 / $4,626 FY2027
(exact), NMES enrollment 128 (NCES), superintendent Larry Begley, the July 15
LPC vote and "transitional" reclassification narrative, three of five board
names, ~65-cent state average tax rate, and both news stories in the site's
source list. No board vote has occurred; nothing on the site is stale except
possibly the venue (item 1).

Not reachable from this sandbox (egress allowlist), needs a five-minute manual
check: the change.org petition link (a dead link under the primary CTA would be
high severity), the exact 52.4-cent Bourbon rate, the $19,348 per-pupil figure
against the new 2024-25 report card release, the full board roster and emails,
and whether the deployed savenmes.org matches this repo.

## The three highest-ROI changes (the ones opposing counsel least wants made)

1. **Purge the insinuation thread and unify the capacity framing** (items 5
   and 7). This removes both the character attack and the capacity rebuttal in
   one edit.
2. **Pre-empt the full-absorption savings model** (item 4). The district's
   path to "over a million" runs through the report's own coefficients; publish
   the reconciliation first and their worksheet arrives pre-rebutted.
3. **Localize the messenger, soften school-vs-school framing, and rebase the
   levy** (items 3, 5, 14). Every clause of "an out-of-state author and an AI
   want to raise your taxes and call your children's schools failures" is
   currently quotable. All three fixes cost nothing analytically.
