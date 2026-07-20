# Adversarial Review: Facility-Capacity Claims in SaveNMES
**Reviewer posture: district facilities consultant, retained to discredit the analysis.**
Primary source: `build/dfp_current.pdf` (KBE-approved August 2021 DFP, 4 pp., read in full). Secondary: `build/dfp_2013_excerpt.png`, `build/dfp_2021_excerpt.png`, `build/dfp_manifest.json`, `NMES_Financial_Model.xlsx` (Facility_Plans, Redistricting, Assumptions tabs), `index.html`, `build/build_pdf.py`, `tests/validate_all.py`.

What the primary source actually says, verbatim (dfp_current.pdf p.1, "SCHOOL CENTERS ... Student Enrollment Capacity"):

> a. Bourbon Central Elementary School (A1) — Permanent — K-5 Center — **535/521**
> To Become — Permanent — K-5 Center — **564/549**
> b. Cane Ridge Elementary School (A1) — Permanent — K-5 Center — **480/422**
> c. North Middletown Elementary School (A1) — Permanent — PK-5 Center — **161/174**
> d. Preschool/Head Start Center (A4) — Permanent — PS/HS Center — 272/200
> Note: Current enrollment is 80 full-day and 192 half-day students

The manifest's reading-order proof (272 = 80 + 192, so figures read enrollment/capacity) checks out against the PDF's own note. That part is airtight. Now the attacks.

---

## Attack 1 — The 521/549 shell game at Bourbon Central

**CLAIM (project):** "The receiving schools' rated capacities are 549 at Bourbon Central and 422 at Cane Ridge" (report, `build_pdf.py` lines 558, 956; site FAQ, `index.html` line 325; model Facility_Plans B13 `=549-Redistricting!B8`).

**ATTACK:** 549 is not Bourbon Central's rated capacity. The plan's **current** rating is 521. 549 sits on the "To Become" line — the long-range figure contingent on the plan's *after-biennium* Bourbon Central project (p.3, item 4: 63,320 gsf, $3,493,586, constructing "1 Custodial Receiving 250 nsf, 1 Kitchen Expansion 1,075 nsf, 1 Media Center Expansion 1,355 nsf" plus renovation of existing space for standard classrooms). That project was *scheduled after the 2022-24 biennium*; nothing in the record shows it was funded or built. The project's explanatory gloss — "Bourbon Central's rated capacity is 549, reflecting the addition in its 2021 plan" (`index.html` line 214; report caption, `build_pdf.py` line 519; model F7) — is an interpretation, not a quote: the word "addition" appears nowhere in the plan's Bourbon Central entry, and the constructed square footage is non-instructional (custodial, kitchen, media). Worse, the workbook is internally split: **Facility_Plans E7 = 521** while formula **B13 hard-codes the literal 549**, bypassing its own capacity column. I will put E7 and B13 on the same slide and call the whole model sloppy.

**EVIDENCE:** dfp_current.pdf p.1 quoted above; p.3 item 4; model E7=521, F7 note, B13 formula; site table row "Bourbon Central ... 535 / 521 ... 459, 90 open at its 549"; `tests/validate_all.py` line 85 pins E7=521 while line 91 pins the site to "549".

**Mitigating fact I must concede before opposing counsel finds it:** the error runs *against* the project. At the true current rating of 521, Bourbon Central has 62 open seats, not 90, and the "net uncommitted" figure falls from 59 to **31** — making the project's absorption argument *stronger*. They gave the district 28 free seats. Also unexploited by the project: the same To Become line projects enrollment 564 against capacity 549 — the district's own long-range plan shows Bourbon Central over capacity *even after* the project is built.

**VERDICT: Vulnerable** (as a sourcing/consistency matter; the underlying conclusion survives under either number).
**SEVERITY: Medium.** It hands me a "they can't even read their own source" opening even though the direction of error is conservative.
**FIX:** State both numbers everywhere: "rated 521 today; 549 only if the plan's unbuilt after-biennium project is completed — and even at 549, open seats (90) are fewer than NMES's 128 students, and the plan itself projects 564 enrolled there long-range." Change B13 to reference a labeled cell (e.g., an E-column "To Become" value) instead of a hard-coded literal, and quote the "To Become ... 564/549" line verbatim rather than glossing it as "the addition."

---

## Attack 2 — The 198 → 174 write-down

**CLAIM (project):** NMES's rated capacity fell from 198 (2013 plan, model C9) to 174 (2021 plan, model E9).

**ATTACK:** I tried to break this three ways and mostly failed. (1) *Legibility:* the 2013 excerpt is fully legible — "North Middletown Elementary School — Permanent — PK-5 Center — **169/198**" — and the 2021 PDF says 161/174. The delta of 24 seats is real. (2) *Motive attribution* (which would breach the project's own README pledge, "it attributes no motive"): the report is disciplined — it explains the mechanism neutrally ("What changes a rated capacity under the state's facilities planning manual (702 KAR 4:180) is how rooms are counted... every room reassigned to preschool, intervention, special education services, or a computer lab lowers the official number without a brick moving"), and it explicitly notes "The write-down was not unique: Cane Ridge fell from 500 to 422 and Bourbon Central from 564 to 521." No "quietly," no alleged intent behind the historical write-downs. The site's phrase "**if ratings can be edited to make room in Paris**, the same pencil can raise NMES" (`index.html` line 216) is conditional, but it is the closest thing to insinuation in the corpus and I will read it aloud with a raised eyebrow; the report's version ("if the administration's answer is that ratings can be adjusted... that concedes the point") is cleaner. (3) *Provenance:* here I score a hit. `dfp_manifest.json` cites "web.archive.org capture of the education.ky.gov URL above (24 captures, Sep 2015 to Sep 2025)" — **no timestamped capture URL for either PNG**. A screenshot with an unpinned archive citation is a chain-of-custody gap I will exploit: "produce the exact capture, or it's a screenshot you made."

**VERDICT: Holds** on substance; the write-down happened and no motive is alleged.
**SEVERITY: Low** (substance) / **Medium** (provenance hygiene).
**FIX:** Pin exact `web.archive.org/web/<timestamp>/...` URLs for both excerpts in the manifest; soften "edited to make room in Paris" on the site to match the report's conditional framing.

---

## Attack 3 — "Net 59 uncommitted seats" and "The seats are not there"

**CLAIM (project):** 549 − 459 = 90 open at Bourbon Central; 453 − 422 = 31 over at Cane Ridge; 90 − 31 = **59 net uncommitted seats** for 128 children (model B13:B17, shortfall 69; report line 560 "The seats are not there"; site line 215).

**ATTACK — arithmetic:** Verified. B13=90, B14=31, B15=59, B16=128, B17=69. Site, report, and workbook agree. No error.

**ATTACK — inputs:** The 459/453 enrollments are *not in any archived primary source*. They come from "Report Section 4," and the model itself confesses doubt: Redistricting C8 reads "**confirm against current-year infinite campus counts**." The DFP's own figures are 535 and 480. I will demand the source-of-record for 459/453 and note that the entire 59-seat headline floats on two self-flagged numbers.

**ATTACK — the structural kill shot:** The claim treats DFP rated capacity as an absorption ceiling. **The district's own two plans prove it is nothing of the sort.** From the very documents the project archived: 2021 plan — BCHS at **799/704** (13% over rating), Preschool at **272/200** (36% over), Cane Ridge at **480/422** (14% over, and the district ran it that way). 2013 plan — BCHS at **881/637** (38% over), BCMS 616/515, Bourbon Central 602/564, Preschool 296/180. Four of six centers operated above rating in 2013. My steelman brief writes itself: "Bourbon County has routinely educated students 13-38% above DFP rating; the DFP is a capital-funding planning artifact, not a fire-code occupancy limit. At the 2013-era ratings the project itself validates for NMES (198), the receiving schools rate 564 + 500 = 1,064 against 912 enrolled — **152 open seats, more than enough for 128**." And the project's own centerpiece argument — capacity is "a policy output the district shapes through its own room assignments... it can be raised through the same process it was lowered" — *legitimizes* the district re-rating Bourbon Central and Cane Ridge upward to absorb NMES. The report's prepared rebuttal ("that concedes the point: the same adjustment raises North Middletown's capacity") is a symmetry argument about *what else the district could do*, not a refutation of *whether it can absorb the students*. There is also a vintage-selection problem I will hammer: the project holds the receiving schools to their written-*down* 2021 ratings (422) while arguing NMES should be credited back toward its written-*down-from* 2013 rating (198). Pick a plan year.

**VERDICT:** Arithmetic **Holds**; the flat assertion "The seats are not there" is **Vulnerable, bordering on Broken** as an impossibility claim. Within the four corners of the current plan it is true (even the most district-favorable reading, 90 open at 549, seats fewer than 128 without touching Cane Ridge); as a real-world constraint it collapses against the district's documented practice of operating over rating.
**SEVERITY: High.** This is the sentence I would put on my first slide.
**FIX:** The project's own FAQ (`index.html` line 325) already has the defensible framing — "What staff, sections, or space must be added, at what cost, from which fund?" — i.e., absorption is not impossible, it is *uncosted and unexplained*. Rewrite the report's "The seats are not there" to match: "Within the district's own current ratings, the seats are not there; absorbing 128 children requires re-rating rooms, adding sections under KRS 157.360 class caps, or capital work — none of which the district has costed or published." Then confirm 459/453 against a citable NCES/KDE record and put the citation in Redistricting C8.

---

## Attack 4 — NMES at 128/174: the 74% the project won't say out loud

**CLAIM (project, implicit):** NMES has "room to grow" at 128 against 174; "NMES stood **93 percent full** against its rating as recently as the 2021 plan; the 'half-empty school' is four years old, not a generation old" (`index.html` line 216; report, `build_pdf.py` lines ~538-541).

**ATTACK:** 128/174 = **73.6%** — below the ~85% utilization threshold districts customarily cite in closure reviews — and the number appears nowhere as a percentage in the site, report, or model. The project prints 128 and 174 side by side constantly but only ever computes the flattering 2021-vintage percentage. Worse, the 93% figure is **internally contradictory**: its denominator is the 174 rating that the *same paragraph* denounces as "a paper number the district itself controls." Against the 198 rating the project wants restored, 2021 was 161/198 = **81%** and today is 128/198 = **65%**. The project cannot simultaneously delegitimize the 174 and lean on it for its best utilization statistic — whichever denominator is legitimate, one of its two claims degrades. And "four years old, not a generation old" is falsified by the project's **own chart data** (`index.html` line 461): enrollment was **131 in both 2017 and 2018** (75% of 174; 66% of 198) before rebounding to 160, and the long slide began around 2009-2010 (224 → 177), a decade before the pandemic the report blames ("its window coincides with the district-wide attendance decline after the pandemic"). There is also a small numbers mismatch: the site's own series shows **148** for 2021 while the "93 percent" claim uses the DFP's 161 — different count dates, unexplained anywhere user-facing.

**VERDICT: Vulnerable.**
**SEVERITY: Medium-High.** Nothing is fabricated, but the framing invites a cherry-picking charge that a consultant can make stick in one chart.
**FIX:** Own the number: state 74% explicitly, present utilization under both denominators (174 and 198), and replace "four years old" with the accurate — and actually stronger — volatility argument the chart supports: enrollment fell to 131 in 2017-18 and *rebounded to 160 within two years*, demonstrating the school refills; pair it with the funded rebalancing plan that takes it to 174.

---

## Cross-cutting exposure

- **Staleness.** The archived plan's own cover reads "**NEXT DFP DUE: JUNE 2025**" — thirteen months ago. A 2026 draft (with the "transitional" label the project contests) evidently exists. I will argue every capacity figure above is superseded-in-waiting. The project's defense — the 2021 plan is the last *KBE-approved* plan, and it demands the new condition assessment be published — is legally correct and should be stated wherever the 2021 numbers are used.
- **What survives everything.** The verbatim record is genuinely strong where it matters: 174, 161, 422, 480, 521/535, 549/564, 272/200, the NMES cost items ($317,660 p.2; $325,000 p.2; $3,617,530 p.3; district need $43,389,464 p.4), and both plans classifying NMES "**Permanent**" all appear letter-for-letter in the archived documents, and the 2013 excerpt independently confirms 169/198 and the $1,920,970 renovation scope. The tests (`tests/validate_all.py` lines 84-92) actively pin the model to 521/422/174/198 and the prose to 549/59 — the discrepancy between those two pins is the codified version of Attack 1.

**Bottom line for my client:** I cannot break the documents — they are the district's own, correctly transcribed. I can break the *packaging*: the 549-as-current-rating gloss, the unpinned Wayback provenance, the unverified 459/453, "the seats are not there" stated as physical fact against a metric the district exceeds by up to 38% in its own filings, and a utilization argument that borrows the very denominator it attacks. Every one of these has a cheap fix, and the fixes would leave the project's core claim — that the current KBE-approved plan provides fewer rated seats than closure requires, and that the district has published no costed absorption plan — essentially untouchable.
