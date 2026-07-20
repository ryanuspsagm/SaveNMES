# Adversarial Review: Academic & Enrollment Claims — "Save North Middletown Elementary"

**Reviewer posture:** hostile statistician retained by Bourbon County Schools. Goal: discredit the academic case for keeping NMES open. Everything below is an attack your opponents can run; fix it before they find it.

**Verification status:** SchoolDigger's public pages returned 403 through the proxy, but search-indexed snippets independently corroborate the 2025 ranks (NMES 272/685, Bourbon Central 545/685, Cane Ridge 575/685 — consistent with 58.2 / 26.5 / 19.3 as normalized scores). **KDE's official report card and Open House datasets were unreachable (proxy 403 on education.ky.gov and reportcard.kyschools.us), so the official state accountability numbers could NOT be verified from this environment.** That matters enormously for Attack 1.

---

## ATTACK 1 — The 58.2 is not what the report says it is (metric misattribution)

**CLAIM:** Executive summary (PDF p.1-2): NMES is, *"on the state's own accountability composite, the district's highest-performing elementary, scoring 58.2 in 2024-25."* Section 8 (PDF p. ~17): *"a 58.2 accountability composite."* Figure 7 caption: *"The 2024-25 accountability composite."* Site FAQ (`index.html:331`): *"a school scoring 58.2."*

**ATTACK:** The 58.2 is **not the state's accountability composite**. It is SchoolDigger's proprietary, normalized 0-100 "Average Standard Score" — a third-party ranking statistic. The project's own workbook admits this: `School_Data!A2` — *"Scores are SchoolDigger's normalized 0-100 'Average Standard Score' from KDE test data - not KDE's official rating. Confirm vs KDE Open House datasets before formal submission."* The PDF's own sources appendix (item 4) repeats the disclaimer: *"not KDE's official rating."* So the document **contradicts itself**: the executive summary attributes to the state a number its own appendix says the state never issued. Kentucky's actual 2024-25 accountability system issues an Overall Performance Rating (color) built from indicator scores — the district can pull up the official KDE report card at the board meeting, show a number that is *not* 58.2 (and a color that may not be flattering), and announce that the report's headline academic figure is fabricated attribution. That one moment poisons every other number in the report, including the good ones.

**EVIDENCE:** `build/build_model.py:655`; workbook `School_Data!A2`; PDF text lines 49-50, 244, 537 vs. line 1043; the "confirm before formal submission" instruction was never executed — and I could not execute it either (KDE blocked from here). The verification the model itself demands is still outstanding at Version 2.2.

**VERDICT: BROKEN** (as attributed). The underlying comparison is probably directionally right, but the label is false and self-contradicted.

**SEVERITY: CRITICAL** — this is the single easiest public kill-shot available to the district.

**FIX:** Before any hearing: pull KDE's official 2024-25 school-level Overall scores/ratings for all three schools from reportcard.kyschools.us, present those as primary, and demote SchoolDigger to a supporting cross-year yardstick. Purge the phrases "the state's own accountability composite" and "accountability composite" everywhere (exec summary, Section 5, Section 8, Figure 7 caption, site FAQ). If the official KDE ratings tell the same story — they likely do — you lose nothing and become bulletproof.

---

## ATTACK 2 — The hero number is the best year of a violently noisy series

**CLAIM:** Site hero (`index.html:138`): "**58.2 vs 26.5**." Implicit: this gap characterizes the schools.

**ATTACK:** Computed from the model's full series (`School_Data!B15:S15`): NMES mean 58.6, **SD 14.7, range 32.1-87.9**, mean absolute year-over-year swing **8.5 points**, including a 22.0-point jump in a single year (32.1 → 54.1, 2023→2024). Two years ago NMES scored **32.1 — below Cane Ridge's 34.6**, i.e., in 2023 NMES was *not even second-best* in this district. With ~60-65 tested students (grades 3-5 of a 128-student K-5), the binomial standard error on a proficiency rate is ±6.5 points (95% CI ±13); the school's own subgroup split — girls 85.7, boys 28.8 (`School_Data!B35:B36`) — is the signature of tiny-cohort noise. The district's soundbite writes itself: *"Two years ago this 'best school' scored 32.1, below Cane Ridge. Their own chart shows it."* And note: **58.2 is only the 60th percentile statewide** (272nd of 685, per the PDF itself). "Best in a collapsing district" is not "excellent."

**COUNTERWEIGHT (use it):** The averages are genuinely robust. 3-yr 2023-25: NMES 48.1 vs BC 26.4 vs CR 29.9 — and 48.1 *includes* NMES's worst year ever, so it is anti-cherry-picked. Full KSA era (4-yr, 2022-25, no start-year gaming): NMES 48.0 vs BC 27.3 vs CR 32.1. NMES's **worst** KSA year (32.1) beats Bourbon Central's **best** (29.9). The ~20-point NMES-BC gap is ~1.7 NMES standard deviations — real signal, not noise. The PDF (p.8-9) already concedes small-n noise and the gender gap explicitly, which is to its credit.

**VERDICT:** Hero strip: **VULNERABLE** (it leads with the single best year, unlabeled). Three-year average claim (48.1/26.4/29.9): **HOLDS** — arithmetic verified, window includes NMES's nadir, robust to 4-yr extension.

**SEVERITY: HIGH** for the hero; the averages are your armor — lead with them.

**FIX:** Make "48.1 vs 26.4, three-year average" the hero and "58.2 in 2024-25" the supporting detail, not vice versa. Pre-empt the 32.1 attack in your own materials ("our worst year still beat Bourbon Central's best").

---

## ATTACK 3 — "Best elementary" is a recent condition, and the "consistent yardstick" isn't

**CLAIM:** Site (`index.html:182`): *"North Middletown outscores every elementary in the county, in either district."* PDF Section 5 title: "The District Would Be Closing Its Best Elementary School." Chart note (`index.html:193`): the score is *"a consistent cross-year yardstick."*

**ATTACK:** Over the model's own 17 reported years, NMES led the three district elementaries in only **9 of 17**. Bourbon Central was the district's best school 2007-2009 and 2012; **Cane Ridge beat NMES three straight years, 2016-2018, and again in 2023**. NMES itself has *fallen* from 87.9 (2010) to 58.2 — the district can invert your Figure 6: "every school declined; NMES simply declined less lately." Worse, calling the metric a "consistent cross-year yardstick" is untenable when the same model note (`School_Data!T14`) records **three different state assessment systems** across the window (CATS/KCCT 2007-11, K-PREP 2012-19, KSA 2021-25), and SchoolDigger normalizes *within each year* — so the series measures relative standing among KY schools, not consistent absolute performance. The Blue-Ribbon-era 87.9 and today's 58.2 are not on the same test or scale.

**VERDICT: VULNERABLE.** True in 2024 and 2025; false as a two-decade characterization; "consistent yardstick" is an overclaim your own footnotes contradict (the PDF's dashed regime markers on Figure 6 partially cover you; the site prose doesn't).

**SEVERITY: MEDIUM-HIGH.**

**FIX:** Rephrase to "the district's highest-scoring elementary in each of the last two years, and in 3 of the 4 years of the current state assessment." Change "consistent cross-year yardstick" to "a same-year comparison across schools, shown across two decades" and never compare 87.9 directly to 58.2 as if same-scale.

---

## ATTACK 4 — On actual proficiency, the "best school" is exactly average

**CLAIM:** Implied: NMES delivers exceptional academics worth preserving.

**ATTACK:** The model's own detail (`School_Data!B30:C33`, PDF p.8): NMES reading 50% proficient vs state 50%; math 44% vs state 44%. **Dead even with the state average in both core subjects.** The entire composite edge comes from writing (58 vs 38) and science (53 vs 37) — the two subjects a hostile audience weighs least and the two most vulnerable to small-n and single-grade testing artifacts. And the boys' composite of **28.8 is statistically indistinguishable from Bourbon Central's whole-school 26.5** — the district can claim half your student body already performs at receiving-school level. Meanwhile older public data (US News/GreatSchools cache: 32% math, 37% reading, evidently the 2023 dip year) is still live on the web for opponents to quote against you.

**COUNTERWEIGHT:** The economically disadvantaged composite (57.1, 62nd percentile statewide) at a ~75-93% FRL school is genuinely strong and is the right card to lead with.

**VERDICT: VULNERABLE.** The composite headline oversells what the subject-level data shows; the PDF discloses the numbers honestly but frames "matches the state average" as a win.

**SEVERITY: MEDIUM.**

**FIX:** Reframe: the claim isn't that NMES is elite statewide; it's that it is at-or-above state average while the receiving schools are in the bottom quarter, with a high-poverty population. That's the defensible version. Prepare an answer for the boys/girls gap before the district asks.

---

## ATTACK 5 — No demographic comparison anywhere (the district's natural counter, left unanswered)

**CLAIM:** Implicit throughout: the score gaps reflect school quality, not student population.

**ATTACK:** Neither the PDF, the site, nor any workbook tab presents FRL / English-learner / IEP shares **side by side for the three schools**. The district's obvious counter: "NMES scores higher because it serves a different population." The Demographics tab is county population only; School_Data has NMES-only subgroup data. Additionally, the PDF says "about three-quarters" of NMES children qualify for FRL while PublicSchoolReview shows **93%** — under community eligibility these figures are slippery, and an unexplained 75-vs-93 discrepancy is a free credibility hit.

**WHAT I FOUND (and you didn't publish):** the comparison likely *helps* you — web sources: NMES ~93% FRL, 11% Hispanic; Bourbon Central 68.3% FRL, 17.3% Hispanic; Cane Ridge 13% Hispanic, FRL 56-93% depending on source. NMES appears to be the *poorest* of the three, which converts the confound attack into your strongest exhibit ("highest-poverty school, highest scores"). EL and IEP shares remain unknown — Bourbon Central's higher Hispanic share suggests a possibly higher EL population, which is the one subgroup that could partially explain its collapse; you must know that number before the district weaponizes it or you get blindsided by it.

**VERDICT: VULNERABLE** — not because the data is against you, but because the analysis is absent and the FRL figures conflict.

**SEVERITY: HIGH** (it's the district's #1 rebuttal and your materials are silent).

**FIX:** Add a three-school demographic table (FRL, EL, IEP, mobility) from KDE report card data to Section 5 and the workbook; reconcile the 75%-vs-93% FRL figure with a CEP footnote.

---

## ATTACK 6 — Enrollment: 261 → 128 (the district's best fact, mostly well-handled — with one soft spot)

**CLAIM:** Peak 261 (1988-89), current 128, rated capacity 174; series 1989-2025 (`Demographics!E33:I50`, `index.html:461`).

**ATTACK & ASSESSMENT:** Enrollment has halved from peak and fallen every year since 2022 (153→145→135→128). Utilization is 128/174 = **73.6%** — and 128/198 (the 2013 rating) = 65%, or 49% of what the building "actually held." The project never prints a utilization percentage; it says "128 of 174" and "forty-six open seats." That said, the framing is unusually honest: the Demographics tab is literally headed *"An honest picture"* / *"HONEST BOTTOM LINE"* and concedes the county is flat-to-declining with organic growth "unlikely"; the PDF (p.18) says *"the district's enrollment decline is real and structural, and I will not pretend otherwise."* The capacity-as-policy-output argument (702 KAR 4:180, write-down 198→174 while receiving schools were also written down, Cane Ridge now 31 over its rating) is genuinely clever and cuts the "half-empty" narrative.

**The soft spot:** the "**93 percent full** as recently as the 2021 plan" claim (PDF p.12, `index.html:216`) uses the plan document's enrollment of 161 — but the project's **own series** says spring 2021 enrollment was **148** (148/174 = 85%), and 135-128 by 2024-25. The 161 is stale plan-file data (likely 2019-20, when the series shows 160). The district can say: "their 93%-full talking point is a four-year-old number their own spreadsheet contradicts." Also minor: the 1989-2014 series is "compiled by PublicSchoolReview," a tertiary source; and 2019=2020=160 exactly suggests a hold-harmless duplicate, not two real counts.

**VERDICT:** Series and honesty: **HOLDS.** The "93% full" framing: **VULNERABLE.**

**SEVERITY: MEDIUM** (the decline itself can't be fixed, only framed — and it largely is).

**FIX:** Date-stamp the 93% claim explicitly ("161 enrolled at the 2021 plan's count date") and pre-concede the current 74% utilization in your own voice before the district computes it for you; source the pre-2015 series to NCES directly.

---

## Summary table

| # | Claim | Verdict | Severity |
|---|---|---|---|
| 1 | 58.2 = "the state's own accountability composite" | **Broken** (misattributed; own appendix contradicts it; KDE verification still not done) | **Critical** |
| 2a | Hero "58.2 vs 26.5" | Vulnerable (best-year cherry-pick; 2023 NMES=32.1 < Cane Ridge) | High |
| 2b | 3-yr averages 48.1 / 26.4 / 29.9 | **Holds** (verified; includes NMES's worst year; robust to 4-yr window) | — |
| 3 | "Outscores every elementary" / consistent yardstick | Vulnerable (led 9 of 17 years; three assessment regimes) | Med-High |
| 4 | Exceptional academics | Vulnerable (reading/math exactly at state average; boys 28.8 ≈ BC's 26.5) | Medium |
| 5 | No demographic confound | Vulnerable (no 3-school FRL/EL/IEP table anywhere; 75% vs 93% FRL conflict) — though the data likely favors NMES | High |
| 6 | Enrollment 261→128, capacity 174 | Mostly Holds (honest framing); "93% full" figure contradicted by own series (148, not 161) | Medium |

**Bottom line:** the statistical core — a large, persistent KSA-era gap over the receiving schools, robust to averaging and inclusive of NMES's worst year — survives hostile review. What does not survive is the packaging: a third-party score repeatedly mislabeled as the state's official composite (with the workbook's own "confirm before formal submission" warning ignored), a best-year hero number, and a missing demographic table whose absence hands the district its easiest rebuttal even though the underlying demographics would likely strengthen the case.

Sources: [SchoolDigger NMES](https://www.schooldigger.com/go/KY/schools/0054000096/school.aspx), [SchoolDigger Bourbon Central](https://www.schooldigger.com/go/KY/schools/0054001576/school.aspx), [SchoolDigger Cane Ridge](https://www.schooldigger.com/go/KY/schools/0054000024/school.aspx), [KDE 2024-25 data release](https://www.kentuckyteacher.org/news/2025/11/kde-releases-2024-2025-assessment-and-accountability-data/), [KY School Report Card](https://reportcard.kyschools.us/), [PublicSchoolReview NMES](https://www.publicschoolreview.com/north-middletown-elementary-school-profile), [GreatSchools NMES](https://www.greatschools.org/kentucky/paris/118-North-Middletown-Elementary-School/), [Homes.com Bourbon Central](https://www.homes.com/school/paris-ky/bourbon-central-elementary-school/yymmg6dbbmf62/), [GreatSchools Cane Ridge](https://www.greatschools.org/kentucky/paris/116-Cane-Ridge-Elementary-School/). Key local files: `build/build_model.py` (lines 655, 679-681), workbook tabs `School_Data` (A2, B15:S17, B30:B36) and `Demographics` (E33:I50), `index.html` (lines 138, 182, 193, 216, 331), `Saving_North_Middletown_Elementary.pdf` (exec summary p.1-2; Section 5 pp.7-9; Section 7 pp.11-12; Section 8 p.17).
