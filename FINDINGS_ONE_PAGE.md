# Findings Report (One Page)

**Branch:** `austin-cursor` · July 20, 2026  
**Question:** Do the SaveNMES site’s big claims hold up?

## Verdict: MIXED / FRAGILE

Audit dollars and many facility-plan figures check out. The sharpest “closure loses / alternatives win” comparisons still overreach.

## What holds

- Operating shortfall ≈ **$2.65M** (exact **$2,648,086**); prior year ≈ **$2.54M**; reserves fall ≈ **$1.1M/year**.
- Building/bond money **cannot pay teachers**; **$6.055M** bond face matches the audit note cited.
- NMES capacity **198 → 174**; was **~93%** full in the 2021 plan; Cane Ridge rated **422**.
- Closure savings in the few-hundred-thousand range **do not erase** a multi-million-dollar hole.
- **2024–25 state tests:** NMES **45% / 45%** (R/M) vs Bourbon Central **36% / 23%**.

## Top holes

1. **Two yardsticks** — “% of $2.65M deficit” vs “restores balance” on ≈$1.1M reserve drain.  
2. **Seats** — Bourbon Central **549** is plan “to become”; **current is 521**. Net open seats fall ≈**59 → 31**; shortfall rises toward ≈**97** kids.  
3. **Alternatives $1.1–2.1M** — hardcoded haircut, not a clean row sum; levy **$386K vs $313K** basis drift.  
4. **Closure band** — hero **$250–600K** vs calculator **$361K** vs favorable **$640K**.  
5. **Rankings** — SchoolDigger 58.2 vs 26.5 favors NMES; **U.S. News / Public School Review currently rank Cane Ridge above NMES**. “Best school” depends on the source.  
6. **“Road miles”** — crow-fly × 1.2 factor, not district routes.

## Fix first

Lock one budget yardstick → show **521 vs 549** both ways → rebuild alternatives from selected rows → align closure cases → put KDE proficiency beside SchoolDigger.

## Fair public line

Closing NMES does not solve the deficit. Keep-and-recover tools are real—but several headline comparisons need tightening before they should carry a board vote.

---

## Quick compare: `austin-cursor` vs `austin-dev`

| | **austin-cursor** (this review) | **austin-dev** |
|---|---|---|
| Tip vs `main` | Ahead: review docs only | **Same commit as `main`** (`410c671`) — no unique review file |
| What it is | Standalone findings + solutions reports | Prior Claude red-team work **already merged into the site/PDF/model** |
| Stance on **549 seats** | Flags **549 as overclaim**; current DFP line **521** | Commit `93b3e89` **adopted 549 as rated capacity throughout** |
| Output type | Documents holes; does not change site claims yet | Applied fixes (SEEK year, tone, ten questions, scenarios, etc.) |
| Overlap | Both treat deficit as real; closure alone insufficient | Same core thesis; `austin-dev` lineage did **not** catch the 521/549 issue—it **hardwired 549** |

**Bottom line of the compare:** `austin-dev` improved product quality and tone; `austin-cursor` re-opens a capacity claim that `austin-dev`/`main` currently treat as settled. Highest-value next step: reconcile **521 vs 549** on `main` using the `austin-cursor` dual-label fix.
