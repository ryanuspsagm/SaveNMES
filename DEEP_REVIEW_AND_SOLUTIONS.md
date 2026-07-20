# Deep Multi-Agent Review: Holes, Rankings, and Fixes

**Branch:** `austin-cursor` · **Date:** July 20, 2026  
**Method:** Fresh multi-agent pass (number audit, logic attack, solutions design) plus live ranking lookups.  
**Companion reads:** [`CLAIMS_REVIEW_REPORT.md`](./CLAIMS_REVIEW_REPORT.md) (short plain summary) · [`ADVERSARIAL_CLAIMS_REVIEW.md`](./ADVERSARIAL_CLAIMS_REVIEW.md) (technical appendix)

---

## 1. Bottom line

The district’s money problem is real. Closing North Middletown alone almost certainly does not fix it.  
Several of the site’s sharpest comparisons still have holes: mixed budget yardsticks, Bourbon Central seats counted from a future “to become” number, an alternatives total that is partly typed in, and a “best school” story that **depends on which ranking source you pick**.

---

## 2. Most up-to-date school rankings (as of this review)

Kentucky does **not** publish one official statewide rank number. Different sites use different years and formulas. SchoolDigger (the site’s main scoreboard) blocked automated refresh (Cloudflare 403), so the table below uses other live sources.

### A. Kentucky Summative Assessment — 2024–25  
*(proficient + distinguished; from KDE-derived public data tables)*

| School | Reading | Math | Notes |
|---|---:|---:|---|
| **North Middletown** | **45%** | **45%** | Above district in both; math above state (42%), reading near state (47%) |
| **Bourbon Central** | **36%** | **23%** | Below district and state in both |
| **Cane Ridge** | ~**45%*** | ~**34%*** | *Public School Review county page (Math 34% / Reading 45%); confirm on KY Report Card |
| District elementary (district site) | 27% proficient + 11% distinguished reading; 24% + 4% math | | Different presentation than P+D combined |

**Takeaway from state tests:** North Middletown looks **stronger than Bourbon Central** on 2024–25 results. Versus Cane Ridge, the picture is closer—not a blowout “best vs worst” story.

### B. Third-party ranks (live July 2026)

| Source | North Middletown | Bourbon Central | Cane Ridge | Who looks “best”? |
|---|---|---|---|---|
| **GreatSchools** (cites 2024–25 KSA) | **7/10** | **5/10** | **4/10** | NMES |
| **U.S. News** (“2026” ranks; multi-year input) | **#474** / 667 KY elem. | **~#464** (secondary listing) | **#439** / 667 | **Cane Ridge** |
| **Public School Review** (“2026” label; tooltips cite older test years) | **#841** / 1,250 | **#821** / 1,250 | **#686** / 1,250 | **Cane Ridge** |
| **Site / SchoolDigger 0–100** (in repo; not re-fetched) | **58.2** | **26.5** | **19.3** | NMES (large gap) |

**Hole:** The hero line “58.2 vs 26.5” is a **SchoolDigger index**, not the state’s official ranking. On **U.S. News** and **Public School Review**, Cane Ridge ranks **above** North Middletown. A hostile board can say: “Your own ‘best school’ claim flips depending on the website.”

**Fair statement:** On the latest **state proficiency** tables and on **GreatSchools**, North Middletown looks better than Bourbon Central. It is **not** safely “#1 in the county on every ranking.” Soften “best elementary” language and always show KDE proficiency beside any aggregator score.

---

## 3. Number holes (ranked)

| Sev | Hole | What the site says | What’s wrong |
|---|---|---|---|
| **HIGH** | Two budget holes | “% of $2.65M deficit” vs “Plan 3 restores balance” | Balance story uses ~**$1.1M/yr** reserve drain. Same plan can look like a fix on one stick and a partial patch on the other. |
| **HIGH** | Bourbon Central **549** seats | “Rated capacity 549… net **59** seats for **128** kids” | 2021 facility plan **current** line is **521**. **549** is “to become” after an addition. At 521, net open seats ≈ **31**, shortfall ≈ **97**. |
| **HIGH** | Alternatives **$1.1–2.1M** | Conservative combined package | Hardcoded in the model after an overlap haircut—not a clean sum of the rows. Site-visible rows alone top out near **~$1.87M**. |
| **HIGH** | Levy base drift | Menu / calculator **~$386K** year one | Model Alternatives low uses a smaller tax base → **~$313K**. Same “menu,” two answers. |
| **HIGH** | Closure savings band | Hero **$250–600K** (9–23%) | Calculator default **$361,240**; favorable case **$640,000 (24.2%)** sits above the hero cap. |
| **MED** | “Road miles” | ~4 extra road miles | Crow-fly distance × planning factor **1.2** (measured pair implies **1.13**). Not district bus routes. |
| **MED** | Busing **$340–612**/student | Fill calculator verdict | Fixed estimate ÷ 30 students—not invoices or T-1 sheets. |
| **MED** | Academic harm | Move to much weaker schools | School averages ≠ proof each child loses learning; ranking sources disagree (see §2). |
| **MED** | Plan 3 “menu plus levy” | Recovery plan beats closure | Levy is already inside the menu—risk of sounding double-counted. |
| **LOW** | Zone **1.2** students/sq mi | Rural density claim | Recomputes ~**1.16**; map is **2015–16** federal boundaries (may be stale). |
| **LOW** | “Half-empty is new” | 93% full in 2021 plan | Occupancy math OK; long enrollment decline is still real (261 → 128). |

**What still recomputes cleanly:** Exact deficit **$2,648,086**; bond face **$6.055M**; NMES capacities **198 / 174**; Cane Ridge **422**; score & enrollment series match across site ↔ spreadsheet; tax rate **52.4¢** second-lowest among the nine plotted peers.

---

## 4. Logic holes (how a hostile board would put it)

1. “We never said one closure erases a multi-million-dollar hole—you graded our one step against your whole wish list.”  
2. “Plan 3 is four political fights (tax, rezoning, transfers, admin cuts) sold as one spreadsheet line.”  
3. “Changing a capacity number isn’t a magnet school, and a magnet that only exists on the page doesn’t fill seats.”  
4. “You’ve been shrinking for decades—you froze one flattering 2021 snapshot and called the emptiness sudden.”  
5. “You’re demanding courtroom worksheets from us while selling parents estimates and an urban Boston bus study.”

---

## 5. Solutions to every problem

Fix in this order: **(1) yardstick → (2) seats → (3) alternatives/levy → (4) closure band → (5) rankings & miles.**

| # | Problem | Concrete fix | Done when… |
|---|---|---|---|
| 1 | Mixed $2.65M vs $1.1M | Define both once. Every “covers X%” / “restores balance” line must name which metric. Show both %s on Plan 3. | No unlabeled “restores balance”; both numbers appear together |
| 2 | BC 549 vs 521 | Split “current rated **521**” vs “to-become **549**.” Never call 549 “today” without the caveat. | Table + charts + FAQ agree |
| 3 | Net 59 seats | Dual strip: current net ~**31** (shortfall ~**97**); if addition done, net **59** (shortfall **69**). Lead with: neither fits 128 cleanly. | Primary claim uses 521 |
| 4 | $1.1–2.1M haircut | Replace hardcoded totals with a selectable package that **sums included rows**; document mutual exclusions. | Changing a row changes the total; no magic constants |
| 5 | Levy $386K vs $313K | Pick one tax base; wire site calculator, Alternatives tab, and PDF to the same cell. | All three match within $1 |
| 6 | Closure $250–600 / $361 / $640 | Publish three labeled cases: Conservative / Base ($361K) / Favorable ($640K). Widen hero to **$250–640K** or move $640K to a footnote. | Hero max ≥ favorable, or favorable clearly outside |
| 7 | Crow × 1.2 as “road miles” | Say “straight-line ~3.3 mi; ~3.9 mi after ×1.2 planning factor—not route miles.” Request T-1 routes. | No unqualified “road miles” |
| 8 | $340–612 busing | Label “illustrative” or derive from model assumptions; ask district for cost-per-mile. | UI shows estimate / formula |
| 9 | Ranking / academic harm | Keep SchoolDigger chart with disclaimer; **add 2024–25 KDE proficiency table**; soften to “school-average gap, not proof each child declines.” | Dual source on every score claim |
| 10 | Premier / magnet growth | Label as a **scenario** tied to modeled transfers/rezoning; keep decline chart adjacent. | No implied funded program |
| 11 | Weak tests | Assert: package = sum of included rows; levy bases equal; primary seats use 521; dual yardstick on Plan 3. | New tests fail on regression |
| 12 | Stale SABS map | Stamp “NCES 2015–16; confirm with current GIS.” | Vintage on map + checkme |
| 13 | “Menu plus levy” | Either drop “plus levy” (levy already in menu) or remove levy from menu and add it only in Plan 3. | Levy counted once |
| 14 | No grade-by-grade seats | Keep the question; state clearly that aggregate seats ≠ grade fit until district publishes worksheets. | Explicit “unknown” |
| 15 | One-time closure costs | Add a one-time column (model placeholder $100K + “district must replace”). | Recurring vs one-time always shown |

### Suggested site copy patches (short)

**Capacity note (replace “rated capacity is 549”):**  
> Bourbon Central’s *current* 2021-plan rating is **521** seats (459 enrolled). The plan’s *to-become* rating after an addition is **549**. Using current ratings (521 and 422), net open seats are about **31** for **128** children—not enough without crowding, portables, or new sections.

**Hero scores (add under 58.2 vs 26.5):**  
> SchoolDigger 0–100 index (unofficial). On 2024–25 state tests, North Middletown: reading 45%, math 45%; Bourbon Central: 36% / 23%. Other public ranks (U.S. News, Public School Review) currently place Cane Ridge above North Middletown—so “best school” depends on the source.

**Plan 3 (replace “restores balance”):**  
> Against the ~$1.1M/year reserve drain, the midpoint package can close the gap on paper; against the $2.65M operating shortfall it covers only part. Figures assume selected menu lines do not overlap.

---

## 6. What remains fair to say (after fixes)

- The operating shortfall and reserve drain are real.  
- Building/bond money cannot pay teachers.  
- Closure savings in the few-hundred-thousand range do not erase a multi-million-dollar problem.  
- North Middletown outperforms Bourbon Central on 2024–25 state proficiency and on GreatSchools.  
- Receiving schools do not have a clean, grade-proven place for 128 children without more information from the district.  
- The board should publish worksheets before any vote.

---

## 7. Recommendation

Treat this review as a **repair list**, not a reason to abandon the case. Implement the top five fixes on the site and in the model, refresh rankings with KDE proficiency beside SchoolDigger, then re-run `tests/sync_check.py` with stronger assertions. Until then, the safest public line is:

> Closing North Middletown does not solve the deficit. The keep-and-recover options are real tools—but several headline comparisons on this site still need tightening before they should carry a board vote.
