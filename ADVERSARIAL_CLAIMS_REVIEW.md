# Technical appendix (earlier adversarial review)

**Prefer the plain-language report:** [`CLAIMS_REVIEW_REPORT.md`](./CLAIMS_REVIEW_REPORT.md)

This file keeps the denser scorecard from the first multi-agent pass for readers who want file paths and technical detail.

---

## Overall verdict: FRAGILE

Cross-file arithmetic for headline scalars is mostly green. The thesis glue is not.

| # | Claim | Verdict |
|---|---|---|
| 1 | Structural GF deficit $2,648,086; reserves ~$1.1M/yr | WEAK (math holds; “structural” + mixed yardsticks) |
| 2 | Closure $250–600K / under a quarter | WEAK (default $361K syncs; range/framing fractured) |
| 3 | Alternatives $1.1–2.1M | FAILS as computed (hardcoded haircut) |
| 4 | Levy ~45.5%; tax rank | HOLDS math / WEAK framing |
| 5 | Bonding / building $ ≠ teachers | WEAK (wall strong; $23.5M currency soft) |
| 6 | BC 549; net 59 seats | OVERCLAIMED (DFP current 521; 549 is to-become) |
| 7 | NMES 93% in 2021; “half-empty” recent | 93% HOLDS; framing WEAK |
| 8 | Capacity “pencil” / Paris symmetry | SYMMETRY FAILS |
| 9 | 2026 transitional vs Permanent×2 | Directionally strong; 2026 draft not in repo |
| 10 | 110 sq mi / +~4 road mi / 78% | Geometry holds; “road” overclaimed |
| 11 | $340–612 busing per student | Not grounded |
| 12 | Scores 58.2 vs 26.5 / 19.3 | Arithmetic true; framing overreach |
| 13 | Premier / magnet growth | Aspiration |
| 14 | Scenario FY2029 $0.8M vs $3.7M | Illustrative only |

### Highest-severity attacks
1. Deficit ($2.65M) vs drawdown (~$1.15M) denominators mixed in thesis.
2. 549 vs 521 inflates net seats 31→59.
3. Alternatives band hardcoded; levy basis drifts (~$386K vs ~$313K).
4. Closure band fractured ($250–600K vs $361K vs $640K).
5. Crow-mile × 1.2 sold as road miles; busing $ from estimates.

### What survives
Exact GF deficit scalars; bond/CIP figures as cited; NMES 198/174 Permanent; 161/174≈93%; CR 422; reno totals; score/enrollment series sync; SABS area arithmetic for 2015–16 polygons.

Local confirmation: `Facility_Plans!E7=521` with formulas on 549; `zone_distances.json` `implied_road_factor=1.13`, `road_factor_applied=1.2`; Alternatives B19/B20 = 1100000 / 2100000.
