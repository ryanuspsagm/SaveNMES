# Numbers to Dig Into (Author Checklist)

Compiled 2026-07-20 from the adversarial review plus targeted research. Items
marked [BLOCKED] could not be verified from the sandbox (KDE, SchoolDigger,
change.org, revenue.ky.gov, and reportcard.kyschools.us were unreachable) and
need a manual pull from a normal connection. Ordered by impact.

## A. Academic data (the headline exposure)

1. **[BLOCKED] Official 2024-25 KDE results for all three schools.** Pull each
   school's Overall Performance color rating (Blue/Green/Yellow/Orange/Red)
   and the four elementary indicator Status/Change values from
   reportcard.kyschools.us, plus the official KSA percent
   Proficient/Distinguished by subject. Present these as primary; keep
   SchoolDigger as the supporting cross-year yardstick. Kentucky publishes the
   color as the headline label; there is no public official numeric composite,
   which is exactly why the old "state's own accountability composite" wording
   was indefensible (now fixed on austin-dev).
2. **The NMES "reading 50% / math 44%" line may be a transcription error.**
   Those figures exactly equal the state averages the same sentence cites, and
   the reachable school-level fragments differ (5th-grade reading 54%,
   4th-grade math 41%, per SchoolDigger's KDE-derived tables; statewide
   elementary 2024-25 was 49% reading / 43% math per coverage of the November
   2025 KDE release). Re-pull NMES's actual school-level numbers for all five
   subjects before anyone else notices the coincidence. This also touches the
   "matches the state average" sentence in Section 5 and the workbook
   School_Data!B30:C33.
3. **Bourbon Central appears on KDE's 2025-26 TSI roster** (Targeted Support
   and Improvement, students-with-disabilities subgroup) per a single search
   snippet of the roster PDF at education.ky.gov/school/focschls. Verify the
   PDF directly. If confirmed, this is an official state/federal designation
   the materials can cite for a receiving school, far stronger than any
   third-party score. No CSI/TSI evidence surfaced for Cane Ridge or NMES.
4. **[BLOCKED] The SchoolDigger values 58.2 and 26.5 themselves.** The ranks
   (272/545/575 of 685) and Cane Ridge's 19.28 were independently confirmed;
   the other two scores were not surfaced and should be re-checked against the
   live pages before formal submission.
5. **Per-school FRL, EL, and IEP shares** for the three-school demographic
   table the materials lack. Reachable fragments: NMES 73.8-93% FRL depending
   on source and year, Bourbon Central ~66-70%, Cane Ridge ~56-67%; EL and IEP
   were unreachable everywhere. Pull from the KDE report card and reconcile
   the FRL spread with one conservative figure and a community-eligibility
   footnote.

## B. Finance (records requests / audit pulls)

6. **The GF vs restricted split of the $9,641,017 tax base.** The levy path
   compounds 4% on total collections including ~$2.05M of FSPK/debt-service
   tax; the workbook's own Alternatives row uses the GF-only base ($7.83M →
   $313K year one). Get the split from the DOR levy files or the audit and
   rebase the levy path; the corrected claim still beats closure ~2.7x.
7. **Receiving-school enrollments (459/453).** The model self-flags them
   ("confirm against current-year infinite campus counts"), the 2021 DFP says
   535/480, and SchoolDigger's 2024-25 page shows Bourbon Central at 483. The
   entire net-seats headline floats on these two numbers; pin them to a
   citable NCES/KDE count with a date.
8. **One-time items inside the $2,648,086 deficit.** The audit's
   capital-outlay function line will show whether the ~$888K/~$691K bus
   purchases ran through the General Fund; if so, the clean recurring deficit
   is nearer $2.0M. Owning that number is stronger than defending $2.65M live.
9. **Which of the ~$1.42M in transfers are recurring.** The honest deficit
   denominator lives between the $1.15M actual drawdown and the $2.65M
   pre-transfer gap; the transfer-sustainability breakdown (already an
   Appendix B ask) settles it.
10. **The district's actual loaded cost per certified position** (salary
    schedule plus district-paid benefits, net of state on-behalf pension and
    health). The $85K judgment cell inflates both sides of the ledger; the
    conclusion survives at ~$62K, but only if both sides are rerun on the
    same number.
11. **FY2023 transportation expense and the composition of the $2.91M line.**
    The "up 20.3 percent" claim is a single-year jump that may include fleet
    capital; the T-1 report gives cost per mile for the busing model.
12. **Current bonding capacity.** The $23.5M is from the FY2024 audit, before
    the $6.055M 2024 issue; get the current KDE bonding potential statement
    and date-stamp the figure wherever quoted.
13. **Classified staffing at NMES** (aides, office, custodial, cafeteria FTE)
    and grade-by-grade enrollments at all three schools, to publish the
    section-by-section absorption reconciliation that defends the
    3-net-positions assumption before the district publishes its own.

## C. Geography, capacity, logistics

14. **Current attendance-boundary policy/map** vs the 2015-16 SABS lines (a
    one-page records request); state the diff result instead of the caveat.
15. **The 2021 enrollment discrepancy (161 vs 148).** The "93 percent full"
    claim uses the DFP's 161; the project's own series says 148 for spring
    2021. Identify both count dates and date-stamp the claim, and check
    whether 2019=2020=160 is a hold-harmless duplicate.
16. **Timestamped Wayback captures** for the 2013/2021 DFP excerpts, pinned
    in dfp_manifest.json (chain-of-custody for the 198→174 exhibit).
17. **A citable source for the 10.0-mile US-460 measurement** and, ideally, a
    Census-block-weighted mean added distance (the current figure is
    area-weighted; student-weighting likely makes it larger, since the town
    sits at the school).

## D. Five-minute manual checks (site liveness)

18. **The change.org petition link** (a dead link under the primary CTA would
    be the cheapest embarrassment available).
19. **Bourbon's exact 52.4-cent rate** in the 2025 DOR rate book, and the
    65.1 state average decimal.
20. **$19,348 per-pupil** against the 2024-25 school-level financial data KDE
    released in July 2026.
21. **Full board roster and emails** (Ott and Buckler could not be
    corroborated from here; three of five members were).
22. **Deployed savenmes.org matches this repo** (spot-check a headline
    string), and the July 23 meeting venue (site says Community Center; WKYT
    said "at the school").
23. **One cited instance of a KDE facility-plan waiver/extension** to back
    the report's "has granted other districts" sentence, or soften it.
