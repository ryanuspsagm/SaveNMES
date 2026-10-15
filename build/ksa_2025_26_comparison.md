# 2025-26 KDE accountability results: Bourbon County elementaries compared

Working note, not published on the site. Data: KDE Assessment and Accountability Data 2025-2026 (page published 10/14/2026), downloaded 2026-10-15; provenance in `build/kde_acct_2026_manifest.json`, extracted rows in `build/kde_acct_2026_*.csv`, and the same shapes as last year's files in `build/kde_ksa_2025_26.json` and `build/kde_levels_2025_26.json`. All-students rows, elementary level, as KDE published them. Figures in parentheses are the change from 2024-25 (`build/kde_ksa_2024_25.json`). Asterisks are KDE-suppressed cells. Regenerate everything with `python build/fetch_kde_acct_2026.py`.

## Headline

- North Middletown posted the lowest result of the four county elementaries in every subject, after being first in every subject in 2024-25. Reading fell from 41 to 21 percent proficient or distinguished (49 percent novice); math from 31 to 23. Science, social studies and writing are suppressed this year, but KDE still publishes their content indexes: 58.7, 22.2 and 25.0 against 75.0, 47.0 and 77.0 last year.
- NMES's overall indicator rate is 18.2, rating 1 (red), against 54.0 in 2024-25 and 74.5 in 2023-24. Both assessment indicators are red; climate and safety (a student survey) is yellow at 73.8.
- KDE has identified NMES for Comprehensive Support and Improvement (CSI), reason "Bottom 5%", first year identified. It is one of 53 CSI schools statewide, 19 of them newly identified this year and 38 of the 53 in Jefferson County; it is the only CSI school in Bourbon County.
- Bourbon Central: 54.1 (orange). Reading up 8 points to 46, math up 6 to 34, writing down 13 to 27. Its reading/math indicator is green; it is on the TSI list for students with disabilities.
- Cane Ridge: 55.9 (yellow), now the district's highest overall. Science, social studies and writing combined is green (social studies up 5 to 32); reading 40 (+3), math 25 (-2).
- Paris Elementary (Paris Independent): 52.6 (orange), up on the content index in four of five subjects (social studies the exception), and above NMES in every subject this year.
- Every county elementary, and the Bourbon County district as a whole, is below the Kentucky elementary average in every subject. Last year NMES beat the state in science and writing; no county school does now.

## 1. Percent proficient or distinguished, by subject

| Subject | Bourbon Central | Cane Ridge | North Middletown | Paris Elem. (Paris Ind.) | BCS district | KY elementary |
|---|---|---|---|---|---|---|
| Reading | 46 (+8) | 40 (+3) | 21 (-20) | 31 (+6) | 40 | 50 (+1) |
| Mathematics | 34 (+6) | 25 (-2) | 23 (-8) | 31 (+2) | 29 | 43 (+0) |
| Science | 31 (+5) | 32 (24-25: *) | * (24-25: 53) | 23 (24-25: *) | 30 | 40 (+3) |
| Social Studies | 30 (-1) | 32 (+5) | * (24-25: 36) | 18 (-4) | 29 | 38 (+0) |
| Combined Writing | 27 (-13) | 29 (+2) | * (24-25: 56) | 12 (+8) | 26 | 41 (-2) |

## 2. Content index, by subject

The content index (0 to 125: novice 0, apprentice 0.5, proficient 1, distinguished 1.25) is what the accountability status is built from, and KDE publishes it even for most suppressed cells, so it is the only like-for-like measure for NMES's science, social studies and writing this year.

| Subject | Bourbon Central | Cane Ridge | North Middletown | Paris Elem. (Paris Ind.) | BCS district | KY elementary |
|---|---|---|---|---|---|---|
| Reading | 60.1 (+4.6) | 57.7 (+1.2) | 36.5 (-22.0) | 49.6 (+7.0) | 56.4 | 68.7 (+1.0) |
| Mathematics | 47.9 (+2.5) | 43.8 (-4.1) | 41.8 (-6.9) | 48.9 (+2.0) | 45.5 | 61.0 (-0.5) |
| Science | 58.7 (+1.1) | 64.5 (+1.6) | 58.7 (-16.3) | 60.1 (+10.1) | 61.3 | 67.7 (+1.8) |
| Social Studies | 42.1 (-2.5) | 53.0 (+14.3) | 22.2 (-24.8) | 31.0 (-1.6) | 44.3 | 54.9 (-0.8) |
| Combined Writing | 49.4 (-11.4) | 50.4 (+1.7) | 25.0 (-52.0) | 35.5 (+9.8) | 47.1 | 63.5 (-0.9) |

## 3. Rank among the three Bourbon County Schools elementaries

Ranked on percent proficient or distinguished where all three are published, otherwise on the content index (marked CI). Paris Elementary is in a separate district and is left out of the ranking; it is above NMES on every row.

| Subject | Order (high to low) | basis |
|---|---|---|
| Reading | Bourbon Central (46) > Cane Ridge (40) > North Middletown (21) | P/D % |
| Mathematics | Bourbon Central (34) > Cane Ridge (25) > North Middletown (23) | P/D % |
| Science | Cane Ridge (64.5) > Bourbon Central = North Middletown (58.7) tied | CI |
| Social Studies | Cane Ridge (53) > Bourbon Central (42.1) > North Middletown (22.2) | CI |
| Combined Writing | Cane Ridge (50.4) > Bourbon Central (49.4) > North Middletown (25) | CI |

## 4. Accountability profile (status, change, combined rate, rating)

Rating colors: 1 red, 2 orange, 3 yellow, 4 green, 5 blue. In KDE's file the combined indicator rate equals status plus change, and the reading/math status equals the mean of the two content indexes (science, social studies and writing: the mean of the three); both identities check against every row below.

| School | Overall rate (rating) | Overall 24-25 | R/M status | R/M change | R/M combined (rating) | Sci/SS/W status | Sci/SS/W change | Sci/SS/W combined (rating) | Climate & safety (rating) | Federal classification |
|---|---|---|---|---|---|---|---|---|---|---|
| Bourbon Central | 54.1 (2 orange) | 55.4 | 54.0 | 3.5 | 57.5 (4) | 50.1 | -4.2 | 45.9 (2) | 77.8 (4) | TSI (Disability) |
| Cane Ridge | 55.9 (3 yellow) | 47.8 | 50.8 | -1.4 | 49.4 (2) | 56.0 | 5.9 | 61.9 (4) | 78.8 (4) | none |
| North Middletown | 18.2 (1 red) | 54.0 | 39.2 | -14.4 | 24.8 (1) | 35.3 | -31.0 | 4.3 (1) | 73.8 (3) | CSI (Bottom 5%) |
| Paris Elementary | 52.6 (2 orange) | 41.9 | 49.3 | 4.5 | 53.8 (3) | 42.2 | 6.1 | 48.3 (3) | 81.3 (4) | none |
| BCS district (ES) | 51.0 (2 orange) | n/a | 51.0 | -0.5 | 50.5 (2) | 50.9 | -3.0 | 47.9 (2) | 77.8 (4) | none |
| Kentucky (ES) | 64.7 (3 yellow) | n/a | 64.9 | 0.3 | 65.2 (4) | 62.0 | 0.0 | 62.0 (3) | 77.4 (4) | none |

## 5. Grade-level results, percent proficient or distinguished

Each cell is this year's grade with the same grade's 2024-25 figure in parentheses (a different cohort of children). Paris has no 2024-25 grade file in the repo.

| Grade / subject | Bourbon Central | Cane Ridge | North Middletown | Paris Elem. | BCS district | Kentucky |
|---|---|---|---|---|---|---|
| 3rd Reading | 45 (39) | 36 (34) | 18 (*) | 26 | 38 (36) | 49 (47) |
| 4th Reading | 46 (41) | 44 (44) | * (47) | 37 | 43 (43) | 50 (50) |
| 5th Reading | 43 (37) | 39 (32) | * (54) | 31 | 39 (38) | 51 (50) |
| 3rd Mathematics | 30 (30) | 21 (23) | 14 (*) | * | 24 (25) | 43 (43) |
| 4th Mathematics | 39 (28) | 26 (*) | 26 (41) | 31 | 32 (30) | 43 (44) |
| 5th Mathematics | 28 (27) | 27 (26) | * (46) | 31 | 28 (29) | 43 (43) |
| 4th Science | 28 (27) | 32 (*) | * (53) | 23 | 29 (31) | 40 (37) |
| 5th Social Studies | 30 (31) | 31 (29) | * (35) | 18 | 28 (31) | 38 (38) |
| 5th On Demand Writing | 23 (40) | 10 (23) | * (58) | 6 | 16 (35) | 35 (38) |
| 5th Editing and Mechanics | 41 (37) | 55 (27) | 16 (50) | 27 | 44 (35) | 48 (47) |

NMES novice shares where published: 3rd grade reading 64 percent, 3rd grade math 36, 4th grade math 52, 5th grade editing and mechanics 47. Statewide 3rd grade reading novice is 23 percent. NMES's published subgroup rows are economically disadvantaged only: reading 18 percent proficient or distinguished, math 27.

## 6. Federal classifications (ACCT_CSI_TSI_ATSI_2026.xlsx)

Statewide: CSI 53, TSI 77, ATSI 81. CSI years identified: 19 schools in year 1, 16 schools in year 2, 3 schools in year 5, 15 schools in year 6. The workbook does not give the identification rule; KDE's 2025 release described CSI as the bottom 5 percent of schools by level on the overall score, a graduation rate under 80 percent, or three years of ATSI, with new schools identified every year since House Bill 298 (2025).

| List | School | Level | Title I | Years identified | Reason |
|---|---|---|---|---|---|
| CSI | North Middletown Elementary School | ES | Y | 1 | Bottom 5% |
| TSI | Bourbon Central Elementary School | ES | Y | n/a | Disability |
| ATSI | Bourbon County Middle School | MS | N | 5 | Disability |

## 7. Reading the numbers

- Suppression. Science is tested in 4th grade only, social studies and writing in 5th only, so at NMES each rests on one class. KDE withheld the level percentages for all three (and most of NMES's grade rows) but published the content indexes, which is why the tables above lean on the index.
- Cohort size. KDE's 2024-25 enrollment file counted 26, 19 and 28 students in NMES's 3rd, 4th and 5th grades. This year's 5th grade is last year's 4th, so the social studies and writing results rest on roughly 19 to 20 children, about five points per child. The reading and math figures cover all three grades, about 70 children, where one child is about 1.4 points; a 20-point fall in reading is not sampling noise at that size.
- The rate counts a drop twice. KDE's combined rate is status plus change, so this year's low status (39.2 reading/math, 35.3 science/social studies/writing) is reduced again by the fall from last year (-14.4 and -31.0) to give 24.8 and 4.3. On status alone both indicators rate orange (2); the change component makes them red. The same arithmetic lifted NMES in 2023-24, when rising scores produced the 74.5 the site and report cite. The overall rate is a weighted blend of the indicator rates in which the two assessment indicators carry nearly all the weight.
- Second year of decline in reading and math. KDE's 2024-25 file already showed NMES's reading/math change negative for both subgroups it published (-9.6 economically disadvantaged, -10.9 white); the all-students status implied by this year's file was 53.6 in 2024-25 and is 39.2 now.
- What CSI brings. For the schools identified in 2025, KDE described the process (Kentucky Teacher, December 2025, https://www.kentuckyteacher.org/news/2025/12/kentucky-board-of-education-discusses-recent-assessment-and-accountability-results-focuses-on-student-achievement/): an education recovery support team works with the school, KDE and Cognia run a diagnostic review, a turnaround team of school and community leaders writes an improvement plan, and the school becomes eligible to apply for federal school improvement funds. The same article gives the identification rule (bottom 5 percent of schools by level, graduation rate under 80 percent, or three years of ATSI) and says identification is now annual under House Bill 298 (2025). Kentucky's exit rules are worth reading in KDE's CSI guidance before the site says anything. Note the tension: the district is weighing closure of a school the state has just placed in a required improvement process.
- Not yet available. KDE served the Accountable_Summary_2026.CSV (subgroup indicator rates) and the all-datasets zip as empty files on three tries (content-length 0, origin last-modified this morning); the School Report Card suite with grade enrollment counts comes later in the fall. Re-pull both before any publication.

## 8. What this does to the site's current claims (nothing changed here)

- `index.html` line 245, Fact One: "On the state's 2024-25 tests, NMES is first in the county in every subject. It beats the state average in science and writing." True as dated, now the opposite on the current tests. The 2024-25 table at lines 247 to 257 and the composite chart series at lines 931 to 933 (NMES 74.5, 54.0) would take the 2025-26 points.
- The report builder repeats it at `build/build_pdf.py` lines 319 to 326 and the model at `build/build_model.py` lines 1218, 1243 and 1262.
- The tests pin the sentence: `tests/validate_all.py` lines 121 and 357 and `tests/sync_check.py` line 616 fail if "first in the county in every subject" leaves the page, so site, report, model and tests have to move together.
- The SchoolDigger validation and the Blue Ribbon and pre-COVID math claims are unaffected.

## 9. Series entries to append when the site is updated

```
kde_scores_history.json  reading_pd 2025-26: NMES 21, BC 46, CR 40, PE 31
                         math_pd    2025-26: NMES 23, BC 34, CR 25, PE 31
                         official_composite 2025-26: NMES 18.2, BC 54.1, CR 55.9, PE 52.6
                         state_elementary_pd 2025-26: Reading 50, Mathematics 43
kde_subjects_history.json per_subject 2025-26: BC Science 31 / Social Studies 30 / Writing 27;
                         CR 32 / 32 / 29; NMES null / null / null (suppressed; CI 58.7 / 22.2 / 25.0);
                         PE 23 / 18 / 12.  avg: BC 29.3, CR 31.0, NMES null, PE 17.7
```

## 10. Provenance

Page: https://www.education.ky.gov/Open-House/data/Pages/Assessment_Accountability_Datasets_2025-2026.aspx (published 10/14/2026 3:55 PM (as shown on the page)). Retrieved 2026-10-15. Downloaded with a browser User-Agent; education.ky.gov answers plain curl with HTTP 403. Accountable_Summary_2026.CSV and All_Datasets_Archive.Zip were served with Content-Length 0 (origin last-modified 2026-10-15 04:42 UTC) on three attempts and are not archived.

| File | Bytes | MD5 |
|---|---|---|
| Accountable_Profile_2026.CSV | 331,210 | d18c1c4bb49196166c54ea29592d6e27 |
| Accountable_Assessment_Performance_2026.CSV | 27,448,141 | 5abaa03fa278b26add3c9f166c3ccb05 |
| Assessment_Performance_by_Grade_2026.CSV | 55,715,316 | 6980cc09fcb7ebf2e7cffe86fa4be770 |
| ACCT_CSI_TSI_ATSI_2026.xlsx | 35,000 | 637bb50a07c02a42035729dd3a03d87d |
