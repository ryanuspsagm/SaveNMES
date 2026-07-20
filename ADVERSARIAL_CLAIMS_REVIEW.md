# Adversarial review of primary claims

**Branch:** `austin-cursor` (from `main` @ `410c671`)  
**Method:** Six overlapping agents (finance, capacity, geography/busing, academics/alternatives, cross-cutting consistency, source provenance), plus local spot-checks.  
**Test baseline:** `sync_check.py` 31/0, `validate_all.py` 54/0 (pagination scan skipped; Playwright not run).

## Overall verdict: FRAGILE

Cross-file arithmetic for headline scalars is mostly green. The thesis glue is not. Savings bands, deficit percentages, and runway “restores balance” use different denominators; receiving-capacity math treats a DFP “To Become” figure as today’s rating; alternatives totals are hardcoded haircuts; geography dollars and road miles are model products dressed as measurements.

---

## Primary claims scorecard

| # | Claim | Verdict | Kill shot |
|---|---|---|---|
| 1 | FY2025 structural GF deficit $2,648,086 (~$2.65M); reserves fall ~$1.1M/yr | **WEAK** | Exact audit math holds; “structural” from two years is rhetoric. Cash drain after transfers is ~$1.15M/yr, not $2.65M. |
| 2 | Closure saves $250–600K/yr (9–23% of deficit); default ~$361,240 / 13.6% | **WEAK** | Default arithmetic syncs. Range is prose judgment; favorable case is **$640K / 24.2%** (outside hero cap); % uses before-transfer deficit; receiving-school add costs omitted. |
| 3 | Alternatives package $1.1–2.1M recurring beats closure | **FAILS as computed** | `$1.1M/$2.1M` are hardcoded yellow cells with an overlap haircut, not `SUM` of lines. Raw sum ~$1.74–3.12M. Site displayed rows peak ~$1.87M. |
| 4 | 3-yr levy path covers ~45.5%; Bourbon 52.4¢ second-lowest of nine | **HOLDS (math) / WEAK (policy framing)** | Compound path and rate rank check. 45.5% is year-three cumulative, not year-one (~14.6%). |
| 5 | Closing creates no bonding room; ~$23.5M unused capacity; building $ ≠ teachers | **WEAK** | Restricted-fund wall is strongest subclaim. `$23.5M` is FY2024 stock; currency after `$6.055M` issue unclear; CIP growth ≠ bond purpose proof. |
| 6 | BC rated capacity today 549; CR 422; net 59 seats for 128 kids | **OVERCLAIMED / PARTLY FALSE** | DFP current BC line is **535/521**; **564/549** is “To Become.” At 521: net **31**, shortfall **97**. Model stores E7=521 then formulas use 549. |
| 7 | NMES was 93% full in 2021 (161/174); “half-empty” is four years old | **93% HOLDS; framing WEAK** | 128/174≈74% today, not half-empty; decline is multi-decade. |
| 8 | Capacity 198→174 is a paper number; same pencil can raise it; symmetry with Paris | **SYMMETRY FAILS** | Paris ratings were **cut**, not raised. 549 needs construction if “addition,” not room-assignment edit. KBE/DFP process ≠ unilateral pencil. |
| 9 | 2026 “transitional” reverses two consecutive Permanent classifications | **DIRECTIONALLY STRONG; SOURCE GAP** | 2013/2021 Permanent confirmed in archives; 2026 draft not in repo. |
| 10 | NMES zone 110 sq mi / 38%; +~4 road mi avg; factor 1.13; 78% closer | **GEOMETRY HOLDS; “ROAD” OVERCLAIMED** | Area/%/78%/≈3.9 mi are 2015–16 SABS + area-grid products. Distances are crow×factor (cited 1.13, **applied 1.2**); not student-weighted; SABS may be stale. |
| 11 | Busing deltas $340–612 per rebalanced student | **NOT GROUNDED** | Fixed yellow totals ÷ 30; fill calculator net formula excludes busing. |
| 12 | Scores 58.2 vs 26.5 (and 19.3); 3-yr avgs 48.1/26.4/29.9 | **ARITHMETIC TRUE; FRAMING OVERREACH** | Peak-gap year; SchoolDigger secondary; CR 3-yr (29.9) > BC (26.4); SES confounds absent. |
| 13 | Grow NMES into premier elementary / magnet path | **ASPIRATION** | Enrollment trend contradicts growth story; not a budgeted operational plan. |
| 14 | Scenario FY2029: closure ~$0.8M vs recovery ~$3.7M | **ILLUSTRATIVE ONLY** | Point inputs (base $361K, mid $1.6M) vs adjacent ranges; uses drawdown denominator while thesis leads with $2.65M deficit. |

---

## Highest-severity attacks (ranked)

1. **Deficit denominator ≠ runway denominator.** Site leads with before-transfer `$2.65M`; Runway / “Plan 3 restores balance” uses ~`$1.15M` after-transfer drawdown. Against drawdown, alt midpoint “works”; against the headline deficit it does not close the gap.

2. **549 vs 521 (To Become vs current).** Inflates net seats 31→59. Locked into site, PDF, model formulas, charts, and `validate_all.py` (which also requires E7=521).

3. **Alternatives $1.1–2.1M hardcoded + non-additive menu.** Plan 3 “menu plus levy” while levy is already inside the menu. Levy year-one basis drifts: site/PDF `$9.64M×4%≈$386K` vs Alternatives GF `$7.83M×4%≈$313K`.

4. **Closure range fractured across surfaces.** Hero `$250–600K` / 9–23%; calculator `$361K`; favorable `$640K` (PDF/model, not site hero); slider can exceed “under a quarter.”

5. **Geography: crow miles × padded factor + yellow busing $.** Tests ratify headline strings; they do not falsify method or SABS vintage.

6. **Academic harm is ecological, not causal.** SchoolDigger-only hero; missing receiver SES; boy composite at NMES ≈ BC school mean.

7. **Tests green-wash claim safety.** Sync/validate assert transcription and needles, not source truth, commensurable denominators, or DFP column selection.

8. **Provenance gaps on secondary aggregators and circular model citations.** Calculators “match the model” that authored the yellow cells; SchoolDigger/PublicSchoolReview carry hero enrollment/score claims.

---

## What survives hard attack

- Exact GF deficit scalars and fund-balance path against KDE audit math (as reconciled in-repo).
- `$6.055M` bond and CIP growth figures as stated from Note 4.
- NMES capacities 198 (2013) / 174 (2021), Permanent classification in both archived plans, 161/174 ≈ 93%.
- CR rated 422; NMES reno dollar totals (~$1.92M / ~$4.26M).
- Score and enrollment series identical across site ↔ model; 3-year averages recompute.
- SABS area arithmetic for the 2015–16 polygons (110.3 sq mi, ~38% of zone sum).

---

## Recommended fixes (if hardening claims)

1. Label BC capacity as **current 521 / to-become 549**; recompute net seats both ways; stop treating 549 as today’s rated capacity without proof the addition was built and rated.
2. Pick one deficit denominator for % claims and runway, or always show both.
3. Derive alternatives bounds from non-overlapping lines, or label the haircut and show raw vs conservative.
4. Align levy year-one basis across Alternatives tab and site/PDF.
5. Put `$640K` favorable case on the site or drop “under a quarter” language that depends on it.
6. Say “modeled crow-mile proxy” not “road miles”; disclose applied factor 1.2; demote Boston analogy.
7. Add KDE Open House checkmes beside SchoolDigger; soften causal academic-harm framing.
8. Extend tests to catch 521/549 dual use, levy-base drift, and deficit≠drawdown commensurability.

---

## Agent coverage

| Agent | Domain | Overlaps |
|---|---|---|
| Finance | Deficit, closure $, levy, bonds, SEEK, fill $ | Cross-cut, provenance |
| Capacity | 549/521, net 59, write-down, transitional, symmetry | Cross-cut, provenance |
| Geography | SABS, distances, busing $, Boston | Cross-cut, provenance |
| Academics / alternatives | Scores, premier growth, menu additivity, scenarios | Finance, cross-cut |
| Cross-cutting | Tests, drifts, thesis glue, timing | All |
| Provenance | DFP/SABS sources, checkme map, hostile Qs | Capacity, finance, geo |

Local confirmation: `Facility_Plans!E7=521` with formulas/notes on **549**; `zone_distances.json` has `implied_road_factor=1.13` and `road_factor_applied=1.2`; Alternatives B19/B20 hardcoded `1100000`/`2100000`.
