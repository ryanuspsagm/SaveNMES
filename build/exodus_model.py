#!/usr/bin/env python3
"""The v5 exodus model: what leaving families cost the district each year.

Reads the anonymized school-choice survey (survey_school_choice_2026_08
_anonymized.csv, this folder) and produces every published number in the
"true cost of leaving" sections of the site, report, summary and model,
written to exodus_model_v5.json. validate_all.py re-runs this file and
compares. Everything is deterministic: the Bayesian posterior uses grid
integration, not sampling.

Method, in order:
 1. FLOOR. Cleaned survey: 31 leaving households, 70 children, sorted by
    kindergarten class year; 70 kids over 12 class years = 5.83 leavers
    per class. The floor assumes only named respondents leave.
 2. STATISTICAL BAND. Among children enrolled now (kindergarten years
    2020-2025) the survey holds 20 leavers and 4 stayers. A response-bias
    model corrects for leavers answering more readily than stayers:
    observed odds = true odds x k, with k ~ LogNormal(ln 3, 0.5) (95% of
    prior mass between about 1.1x and 8x). The prior is anchored to
    published measurements of this bias: Groves/Presser/Dipko 2004
    (interested groups answer 1.4x more readily), Abraham/Helms/Presser
    2009 (engaged respondents 1.35x, directly measured), Pew 2012/2017
    (engaged people over-represented at implied ratios of 3-4x); the
    measured 1.4-4x band sits inside the prior's 1.1-8x. Posterior
    quartiles of the true leave share come from numeric integration
    over (p, k).
 3. SURVIVAL. A lost child is counted only for years they would actually
    have been enrolled. District cohort data (SAAR school files: each
    2025-26 secondary grade vs its own combined 5th-grade class) gives
    per-grade survival; the sum replaces the flat 13 years with 12.62.
 4. STEADY STATE. kids out per year = (leavers per class) x 12.62;
    dollars = kids x $5,136 (the enacted FY2027 SEEK base guarantee of
    $4,636, 2026-28 budget, plus the $500 central add-on, the same basis
    as the closure grid's leaver term).
 5. RAMP. Losses cover 6 grade cohorts in year one and deepen by one
    cohort a year until all 13 are hit in year 8; over a 13-year window
    that is 141 cohort-years of 169, factor 0.834.
 6. COST RESPONSE. Each departed student also stops costing the
    district about $400 of supplies and materials, the same low-leg
    figure the growth model charges each recruit, so the two models
    stay symmetric. This non-teaching variable cost scales with
    students and is embedded in the leaver term, not a separate lever.
    Teacher savings are priced ONLY on the closure grid's teachers-cut
    lever (the district's own 0-3 positions), so staffing savings are
    never counted twice.

Sources: survey CSV (this folder); SAAR enrollment reports 1999-2019 and
2022-23 through 2025-26 (this folder); school_council_allocation_2026_27.pdf;
munis_cost_by_org_fy2026.pdf.
"""
import csv, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SEEK = 4636 + 500          # enacted FY2027 base + central add-on = 5,136
C_LO, C_HI = 19, 24          # NMES per-grade cohort range, recent SAAR files
VAR_NONTEACH = 400           # supplies per student, growth model low leg

# per-grade survival vs own 5th-grade class (SAAR 2025-26 snapshot)
SURV_SEC = [172/177, 178/188, 191/196, 193/197, 194/202, 194/202, 176/213]
EFF_YEARS = 6 + sum(SURV_SEC)                      # 12.62
RAMP = (sum(range(6, 13)) + 13 * 6) / (13 * 13)    # 0.834

# ---- 1. survey floor -------------------------------------------------------
kids = list(csv.DictReader(open(os.path.join(
    HERE, "survey_school_choice_2026_08_anonymized.csv"))))
leave = [r for r in kids if r["status"] == "leaving"]
classes = {int(r["kindergarten_year"]) for r in leave}
PER_CLASS = len(leave) / len(classes)              # 5.83

# ---- 2. Bayesian band (grid integration) ----------------------------------
enrolled = [r for r in kids if 2020 <= int(r["kindergarten_year"]) <= 2025
            and r["status"] in ("leaving", "staying", "staying_confirmed_by_organizer")]
X = sum(r["status"] == "leaving" for r in enrolled)
S = len(enrolled) - X                              # 20 / 4

def posterior_quantiles(qs):
    NP, NK = 2000, 400
    mu, sig = math.log(3), 0.5
    ks = [math.exp(mu + sig * (-4 + 8 * (j + 0.5) / NK)) for j in range(NK)]
    kw = [math.exp(-0.5 * ((math.log(k) - mu) / sig) ** 2) for k in ks]
    dens = []
    for i in range(NP):
        p = (i + 0.5) / NP
        tot = 0.0
        for k, w in zip(ks, kw):
            th = p * k / (p * k + 1 - p)
            tot += w * th ** X * (1 - th) ** S
        dens.append(tot)
    total = sum(dens)
    out, acc, qi = [], 0.0, 0
    for i, d in enumerate(dens):
        acc += d
        while qi < len(qs) and acc >= qs[qi] * total:
            out.append((i + 0.5) / NP); qi += 1
    return out

P25, P50, P75, P95 = posterior_quantiles([0.25, 0.50, 0.75, 0.95])

# ---- 3-5. ladder -----------------------------------------------------------
def rung(per_class_lo, per_class_hi):
    klo, khi = per_class_lo * EFF_YEARS, per_class_hi * EFF_YEARS
    return dict(kids_lo=round(klo), kids_hi=round(khi),
                dollars_lo=round(klo * SEEK), dollars_hi=round(khi * SEEK))

LADDER = {
    "floor":   rung(PER_CLASS, PER_CLASS),
    "iqr_low": rung(P25 * C_LO, P25 * C_HI),
    "median":  rung(P50 * C_LO, P50 * C_HI),
    "iqr_high": rung(P75 * C_LO, P75 * C_HI),
    "p95":     rung(P95 * C_LO, P95 * C_HI),
}


RESULT = dict(
    seek=SEEK, class_lo=C_LO, class_hi=C_HI, per_class=round(PER_CLASS, 2),
    leaving_households=len({r["household"] for r in leave}),
    leaving_children=len(leave), enrolled_sample=len(enrolled),
    enrolled_leavers=X, posterior=dict(p25=round(P25, 3), p50=round(P50, 3),
                                       p75=round(P75, 3), p95=round(P95, 3)),
    eff_years=round(EFF_YEARS, 2), ramp=round(RAMP, 3),
    var_nonteach=VAR_NONTEACH, ladder=LADDER,
)

if __name__ == "__main__":
    out = os.path.join(HERE, "exodus_model_v5.json")
    json.dump(RESULT, open(out, "w"), indent=1)
    print(f"survey: {RESULT['leaving_households']} leaving households, "
          f"{RESULT['leaving_children']} children, {RESULT['per_class']} per class")
    print(f"enrolled sample {RESULT['enrolled_sample']} (leavers {X}); posterior "
          f"p25/50/75/95 = {P25:.3f}/{P50:.3f}/{P75:.3f}/{P95:.3f}")
    print(f"effective years {EFF_YEARS:.2f}, ramp {RAMP:.3f}, "
          f"non-teaching variable ${VAR_NONTEACH}/student")
    for name, r in LADDER.items():
        print(f"  {name:9s}: {r['kids_lo']}-{r['kids_hi']} kids/yr, "
              f"${r['dollars_lo']:,}-${r['dollars_hi']:,}/yr")
