# Adversarial Review: Transportation & Geography Claims in "Saving North Middletown Elementary"

**Reviewer posture:** District transportation director, hostile. Goal: discredit the geography and busing analysis.
**Materials examined:** `build/fetch_sabs.py`, `build/sabs_zones.json`, `build/zone_distances.py`, `build/zone_distances.json`, `build/build_model.py` (Assumptions, Closure_Model, Transport_Geo, Redistricting sheets), PDF pp. 6-7, 17-20, 25-28, `index.html`. All headline numbers were independently recomputed (grid sample re-run from the raw polygon; results reproduced exactly: mean added 3.28 straight mi, 78.0% area share).

**Correction to the brief before anything else:** the tasking asserted the project claims "closure adds $140,000-$225,000/yr in busing costs." It does not. The busing claim is a **$75,000-$200,000 planning range with a $137,500 base case** (build_model.py:144, 157; index.html:236; PDF p.18). **$140,000-$225,000 is a different number entirely** — the fill-NMES-to-capacity *revenue* line (Redistricting!B30:B31 = $140,616/$225,616; index.html:297). Both are attacked below. If the district's rebuttal conflates these two numbers, the author will win that exchange; don't hand it to him.

---

## Attack 1 — Ten-year-old federal boundary data (SABS 2015-16)

**CLAIM:** The NMES zone is 110 sq mi, 38% of the county; zones drawn from "official" federal boundaries.

**ATTACK:** The entire map rests on the School Attendance Boundary Survey, 2015-16 collection — the *last* one ever taken, now a decade stale. SABS boundaries were self-reported by districts to NCES with known QA problems, and nothing in the repo demonstrates the 2015-16 lines are the 2026 lines. Every downstream number — 110 sq mi, 38%, 1.2 students/sq mi, 78%, mean added miles — inherits this vintage. As transportation director I'd say: "This map is from the Obama administration. We've adjusted lines since."

**EVIDENCE:** fetch_sabs.py:1-8 ("2015-16 was the last national collection, so treat the boundaries as that vintage"); sabs_zones.json source string "NCES EDGE SABS 2015-16 bulk download, Primary layer (leaid 2100540)" — NMES 110.3, Cane Ridge 120.2, Bourbon Central 58.6, total 289.1 vs Census land area 289.7 (110.3/289.7 = 38.1%, arithmetic checks). PDF p.17: "(2015-16, the last national collection)"; table footnote: "**The vintage is the caveat: the district should confirm nothing has moved since (Appendix B)**"; Fig. 13 caption repeats the vintage; Notes on the Data (p.25) repeats it again; index.html:288, 291 both state "2015-16."

**VERDICT: Holds** (on disclosure), **Vulnerable** (on currency). The disclosure is airtight — the vintage is flagged in at least five places, and the burden is explicitly tossed to the district. My "lines have changed" attack only works if I can produce a board minute redrawing them, and the district structure (same three elementaries, same names, same towns) is unchanged since 2015-16. If I bluff and the author FOIAs the boundary policy, I lose worse.

**SEVERITY: Low-Medium.** **FIX:** Obtain the district's current attendance-boundary policy/map (a one-page records request) and diff it against SABS; state the result rather than the caveat.

---

## Attack 2 — Area-weighted, not student-weighted: "78% of the zone" is not 78% of students

**CLAIM:** Mean added trip ~3.3 straight / ~3.9 road miles; 78% of the zone is closer to NMES.

**ATTACK:** I read zone_distances.py. The computation is a **uniform 0.006 degree grid over empty farmland** — 812 points weighted by *acreage*, not by where a single one of the 128 children lives (zone_distances.py:49-58: every interior grid point counted once; no population raster, no geocodes, nothing). "78%" is a statement about pasture. The PDF then slides from an area statistic into a child statistic in one sentence: "Averaged over the zone's area, closure adds about 4 road miles each way **to a child's trip**" (p.19). The website drops the qualifier entirely: "about four road miles more each way on average" (index.html:288). No student-weighted number exists anywhere in the repo. If the students cluster along the western US-460 corridor near Paris, the true mean collapses.

**EVIDENCE:** I re-ran the grid and stress-tested it:
- Reproduced: mean added 3.28 straight, share 0.780 (matches zone_distances.json:8,14).
- If students lived only in the zone's western strip (lon < −84.15, ~40% of the area): mean added ≈ **−0.35 mi** — closure *shortens* trips.
- If 50% of students cluster within 2 mi of the school (the town of North Middletown, pop. 610, sits at the school): mean added ≈ **+5.2 straight mi (~6.2 road)** — *worse* than the report claims. Maximum added distance in the whole zone is at the town itself (8.87 straight ≈ 10 road).

**VERDICT: Vulnerable** — but the exposure is asymmetric, and mostly against *me*. The only plausible population concentration is the town at the school's doorstep, where added distance is the zone's *maximum* (the full 10-mile pair), so student-weighting almost certainly pushes the mean *above* 3.9 road miles, not below. The 78% area figure is honestly labeled "of the zone's **area**" in both the PDF (p.19) and workbook (build_model.py:369 "Share of the zone's area closer to NMES"). Still: the phrase "to a child's trip" (PDF) and the unqualified website sentence are technically unsupported, and the author *admits* he lacks the geocoded counts (PDF p.25; Transport_Geo A2 note).

**SEVERITY: Medium** (rhetorical exposure; the district holds the geocoded data and can produce a counter-number the author cannot check). **FIX:** Weight the grid by any public population proxy (Census blocks are free) and publish the student-weighted mean; change "a child's trip" to "the average point in the zone"; fix index.html:288 wording.

---

## Attack 3 — A county-wide road factor calibrated on exactly one road

**CLAIM:** US-460 pair = 10.0 road mi vs 8.9 straight → implied factor 1.13; 1.2 applied everywhere.

**ATTACK:** One measured pair, on the single straightest arterial in the zone, extrapolated to every farm lane in 110 sq mi. n=1 is not calibration; it's an anecdote. Worse, the 10.0 "measured" miles has no traceable source — endnote 27 cites "U.S. Route 460 mileage, North Middletown to Paris" with no odometer log, no GIS route, nothing (PDF p.27). And the mean-added-road number is produced by multiplying a *difference* of straight-line distances by the factor (zone_distances.py:69: `(mean d_P − mean d_N) × 1.2`), which is not how circuity works — road(A) − road(B) does not equal 1.2×(straight(A) − straight(B)) unless both legs share the factor, which side-road legs to NMES demonstrably don't.

**EVIDENCE:** zone_distances.py:18-19, 66-69; zone_distances.json:6-7 (1.13 implied, 1.2 applied); build_model.py:363-366 (Transport_Geo B57/B58, the 1.2 is a yellow judgment cell); PDF p.19 ("a road factor of 1.13 on the one pair that can be measured exactly; a conservative 1.2 is applied everywhere else").

**VERDICT: Holds, annoyingly.** Published rural circuity factors run ~1.2-1.4; the author *discarded* his favorable 1.13 measurement and applied 1.2 — the bottom of the literature band, on an arterial-dominated trip. Every direction I push the factor hurts *my* case: a true factor of 1.3-1.4 makes the far-corner ride 20-21 miles, not 18, and the added burden bigger. The single-pair critique lands as a style point ("amateur methodology") but the chosen value is defensible-to-conservative, and it's disclosed as a judgment cell. The difference-times-factor sloppiness changes the 3.9 by tenths of a mile.

**SEVERITY: Low.** **FIX:** Cite a source for the 10.0 (any routing engine printout); sample 5-10 OSM-routed pairs inside the zone for an empirical factor; compute road distances per leg before differencing.

**Bonus sub-attack (real, unaddressed):** zone_distances.py:17 collapses **both receiving schools to a single "Paris" coordinate** (comment: "both receiving schools are in Paris"). Bourbon Central and Cane Ridge are distinct campuses on different sides of Paris; the ~64 children hypothetically assigned to each would ride to different points. Nothing in the repo validates the single-point simplification or even records the two schools' coordinates (NCES publishes them; the repo cites that fact on p.19 without using it). Severity Low — error is plausibly ±1-2 miles either direction — but it's an unforced hole in a "measured on official geometry" pitch.

---

## Attack 4 — The busing cost number: the author's own bottom-up math doesn't support his own midpoint

**CLAIM:** Closure adds $75K-$200K/yr in busing; base case $137,500; the bottom-up estimate "validates the $137,500 midpoint."

**ATTACK (a) — the validation is spin.** Reverse-engineered from Transport_Geo (build_model.py:325-342): 3 routes × 40 mi/day × 170 days = 20,400 bus-miles × $2.50-$4.50 = **$51,000-$91,800**, plus one contingent bus at $55,000 → **$51K-$147K**. The midpoint of the author's own bottom-up range is **~$99K**, yet the closure model charges closure **$137,500** — the top third of his own computation, reachable only if the route tiers break *and* costs run near the high band. PDF p.19's claim that the bottom-up math "validates the $137,500 midpoint" is false on its face: it validates that $137,500 is *inside* a range whose center is $38,500 lower. Swap in $99K and the closure net saving rises from $361,240 to $399,740 (Closure_Model!B20 = fixed $290K + 3×$85K − busing − 10×$4,626; verified against index.html:479 `net=290000+p*85000-b-l*4626`).

**ATTACK (b) — near-zero marginal cost, the district's best card.** The district *already runs buses from the NMES zone to Paris every school day* — Bourbon County Middle and High are in Paris, so grades 6-12 from this zone ride that stem now. Rural Kentucky districts routinely run mixed-grade routes. Absorb the 109 elementary riders into redesigned existing runs and the marginal cost is a tier adjustment, not three new 40-mile round trips. The report never mentions the existing secondary routes. Add that every driving input is a yellow guess: 85% ridership (B20), 3 routes (B22), 170 days (B25), $2.50-$4.50/mile (B27-28), $55K/bus (B32) — build_model.py:326-338.

**ATTACK (c) — consistency with the $2.9M district spend.** $2.9M (Assumptions!B42, FY2025 audit) across a plausible ~30-bus rural fleet is ~$97K/bus-year fully loaded. Against that: the $55K "all-in cost per additional bus-year" the author uses is *low* by his own district's average, and fully-allocated cost per mile implied by the audit likely exceeds $4.50 — meaning the $2.50-$4.50 "marginal" band is internally coherent (marginal < average). This attack partially backfires: if I claim near-zero marginal cost for 20,400 new miles, I contradict my own budget's cost structure, and the report has pre-loaded the counter that state reimbursement on new miles is $0 under the frozen 2026-28 appropriation (Transport_Geo A18; PDF p.19), so every new mile is local money.

**VERDICT: Vulnerable.** The "$137,500 validated" sentence is the single most attackable sentence in the transportation section — the author's own arithmetic centers $40K lower, and the mixed-grade-route absorption scenario is unexamined. But the *conclusion* is robust: even at the district-favorable $75K (which the model itself tests — Assumptions!B67, Closure_Model!B34, the "red-team" case at ~$640K net), closure covers under a quarter of the $2.65M structural deficit. Moving busing from $137.5K to $51K shifts closure's deficit coverage from 13.6% to ~17% — nowhere near a decision flip.

**SEVERITY: Medium-High** on credibility, **Low** on conclusion. **FIX:** Replace "validates the $137,500 midpoint" with "brackets it"; run a scenario where elementary riders are absorbed into existing secondary routes; demand the T-1 report (already Appendix B's ask) and publish cost-per-mile from it.

---

## Attack 5 — Double-counting / netting in the closure calculator

**CLAIM:** Net saving = fixed avoided + positions×$85K − busing − leavers×$4,626.

**ATTACK:** Traced end to end. Closure_Model (build_model.py:199-218): savings = $175K principal/office + $115K plant + 3×$85K positions = $545K; offsets = $137.5K busing + 10×$4,626 SEEK = $183,760; net **$361,240** = 13.6% of the $2,648,086 deficit — matches the PDF's "13.6%" (p.19 area, Scenarios E6) and index.html:479 exactly. Busing enters once. The $145K-$290K "transportation optimization" line lives only in the Alternatives/Plan-3 menu (build_model.py:389-390) and is *not* also credited inside the closure model — no double count. Sensitivity table (build_model.py:214-217) correctly holds busing fixed while varying leavers.

The residual attack is **framing, not arithmetic**: Plan 2 ("closure only") is denied the optimization savings, tax levy, and delinquency recovery that Plan 3 gets, though a district could do closure *plus* the menu. But the PDF itself concedes optimization is available "whichever way the boundary question is decided" (p.19), and the honest comparison — closure's *incremental* $361K on top of any menu — is what the report actually argues. One genuine omission runs in the **district's favor**: Closure_Model books *no* receiving-school cost line (added sections, space) despite the PDF asserting receiving schools would "add sections in several" grades (p.5) — the author under-charged closure.

**VERDICT: Holds.** **SEVERITY: N/A** (nothing to exploit; the omission found favors closure). **FIX:** Add an explicit $0 placeholder row for receiving-school costs so the conservatism is visible.

---

## Attack 6 — Receiving schools, and the capacity double standard (best genuine hit in this review)

**CLAIM:** Receivers are Bourbon Central (459) and Cane Ridge (453), ~64 students each; and — the $140K-$225K fill-to-capacity line.

**ATTACK (a):** The 64/64 split is invented. No published district consolidation plan is cited assigning NMES students anywhere; grade reconfiguration (which the report itself floats on p.25) would change every distance and cost number. All zone-distance math assumes both receivers at one Paris point (Attack 3 bonus).

**ATTACK (b) — the double standard:** When rated capacity hurts NMES, the report dissolves it: NMES's 174 rating is "**a policy output, not a physical constant**: the same building held 261 students in 1988-89" (build_model.py:102, Assumptions!B12 note). When rated capacity hurts the receivers, it suddenly binds: "Cane Ridge already **31 over**" its 422 rating, "59 uncommitted seats for 128 children" (index.html:325). Same document, same metric, opposite epistemics depending on which conclusion it serves. That is the sound bite I would put on a slide at the board meeting.

**ATTACK (c) — the $140K-$225K line:** Decomposed (build_model.py:285-290, Redistricting!B26-B31): 16 transfers×$4,626 = $74,016 hard revenue, minus $18,400 variable cost, **plus $85,000-$170,000 of "sections avoided or redeployed at receiving schools"** — i.e., 60-75% of the headline is a yellow judgment cell claiming that pulling just 15 students out of each 450-student Paris school frees 1-2 full teaching sections. Meanwhile the closure model credits only 3 positions for moving 128 students out of NMES. Removing 15 kids spread across six grade levels eliminates zero sections in any staffing model I run. The defensible core of that line is ~$56K, not $140K-$225K.

**EVIDENCE:** build_model.py:102, 265-266, 285-290; index.html:297, 316, 325; PDF pp. 5, 25. Computation verified: $140,616 / $225,616.

**VERDICT: Vulnerable** (b and c). The capacity double standard is real and internal; the sections-avoided assumption is the softest number given headline billing on the website (index.html:297 presents "$140,000 to $225,000" with no yellow-cell caveat). Partial mitigation: the workbook flags the cells yellow (build_model.py:287-288) and A41 admits receiving-school capacities are "a records ask."

**SEVERITY: Medium-High.** **FIX:** Reconcile the capacity argument — either ratings are soft everywhere or binding everywhere; restate the fill-to-capacity line as "$56K firm + up to $170K contingent on section relief"; put the caveat on the website, not just in the workbook.

---

## Attack 7 — Density arithmetic and the Paris Independent enclave

**CLAIM:** 1.2 students/sq mi (NMES zone) vs ~5.1 (Paris-based zones) vs 3.6 district-wide.

**ATTACK:** Verified: 128/110.3 = 1.16; (459+453)/178.8 = 5.10; 1,040/289.1 = 3.60. But the numerators are *school enrollments*, not zone residents (out-of-zone attendance uncounted — the caption admits "the closest public proxy"), and the SABS county-district polygons total 289.1 sq mi, i.e., they *include* the territory of Paris Independent Schools, a separate district whose elementary students are excluded from the numerator. So the map's denominators cover ground whose kids attend a district the map ignores.

**VERDICT: Holds.** Both distortions run the *wrong way for me*: adding Paris Independent's in-town students would raise Paris-area density well above 5.1 and sharpen the exact contrast the report wants. The proxy caveat is printed under the table (PDF p.17). Not worth raising in public; it invites a worse number.

**SEVERITY: Low.** **FIX:** Footnote the Paris Independent overlap explicitly to pre-empt the muddying attempt.

---

## Summary scorecard

| # | Claim | Verdict | Severity |
|---|-------|---------|----------|
| 1 | SABS 2015-16 geography, 110 sq mi / 38% | Holds (disclosed); Vulnerable on currency | Low-Med |
| 2 | Mean added miles / 78% (area-weighted) | Vulnerable in phrasing; bias likely favors report | Medium |
| 3 | Road factor 1.13→1.2 from one pair | Holds (value conservative); sloppy method | Low |
| 3b | Single "Paris" point for two receiving schools | Vulnerable | Low-Med |
| 4 | $137,500 busing base "validated" by bottom-up | Vulnerable ("validates" overstates; absorb-scenario unexamined) | Med-High / Low on conclusion |
| 5 | Netting in closure calculator | Holds (verified, no double-count; omission favors district) | — |
| 6 | Receiving schools + $140K-$225K fill line | Vulnerable (capacity double standard; sections-avoided assumption) | Med-High |
| 7 | Density contrast 1.2 vs 5.1 | Holds | Low |

**Nothing is Broken.** The geometry pipeline reproduces exactly from raw data, the closure arithmetic nets correctly, and the worst distortions I found (area-weighting, road factor, omitted receiving-school costs) mostly *understate* the author's own case. The three exploitable soft spots, in order: (1) the capacity double standard (Attack 6b) — a genuine internal contradiction; (2) "validates the $137,500 midpoint" when his own bottom-up centers at ~$99K, plus silence on absorbing riders into existing 6-12 Paris routes (Attack 4); (3) the "sections avoided" assumption carrying most of the $140K-$225K headline (Attack 6c). None of the three, corrected, moves closure's deficit coverage outside roughly 13-17% of the $2.65M structural gap — which is the report's actual thesis, and it survives this attack.
