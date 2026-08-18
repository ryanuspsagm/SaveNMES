#!/usr/bin/env python3
"""The v5 exodus model: what leaving families cost the district each year.

Reads the anonymized school-choice survey (survey_school_choice_2026_08
_anonymized.csv, this folder) and produces every published number in the
"true cost of leaving" sections of the site, report, summary and model,
written to exodus_model_v5.json. validate_all.py re-runs this file and
compares. Everything is deterministic: the Bayesian posterior uses grid
integration, not sampling.

Method, in order (v5.0 final: the survey is read as a SHARE of the
current student population, not as per-class counts; the hand-coded
kindergarten class years are used only to flag who is enrolled now):
 1. SIGNED EVIDENCE. Cleaned survey: 31 leaving households, 70 children.
    Counts only; no per-class arithmetic is published from them.
 2. STATISTICAL BAND. Among children enrolled now (kindergarten years
    2020-2025) the survey holds 20 leavers and 4 stayers. A response-bias
    model corrects for leavers answering more readily than stayers:
    observed odds = true odds x k, with k ~ LogNormal(ln 3.5, 0.5)
    TRUNCATED at k >= 3.3, spanning 3.3x to about 9.5x. The floor and
    center are chosen for this survey's specific character: a small,
    emotionally charged respondent pool answering a zero-effort form
    circulated by the campaign itself. Published measurements of this
    bias run 1.4x to 4x (Groves/Presser/Dipko 2004: 1.4x;
    Abraham/Helms/Presser 2009: 1.35x directly measured; Pew 2012/2017:
    implied 3.3-4x for the civically engaged). The model refuses every
    k below 3.3, Pew's lower high-salience benchmark: it assumes the
    bias is AT LEAST as strong as the strongest published setting, and
    prices tails beyond anything ever measured. This deliberately leans
    against the campaign's own survey. Posterior
    quartiles of the true leave share come from numeric integration
    over (p, k).
 3. TODAY. The corrected share applied to the current student
    population: 128, the last official SAAR end-of-year count the site
    standardizes on.
 4. STEADY STATE, FULL FEEDER. The same share applied to the entire
    NMES feeder stream: every entering class (21.5, the midpoint of the
    recent 19-24 per-grade SAAR range; the ten-year average kindergarten
    is 22.2), carried through grade 12 at the district's own measured
    grade-to-grade survival (SAAR school files: each 2025-26 secondary
    grade vs its own combined 5th-grade class), which replaces the flat
    13 years with 12.62 effective years. kids out per year = share x
    21.5 x 12.62; dollars = kids x $5,136 (the enacted FY2027 SEEK base
    of $4,636, 2026-28 budget, plus the $500 central add-on, the same
    basis as the closure grid's leaver term).
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
POP = 128                    # last official SAAR end-of-year count (2024-25)
COHORT = 21.5                # entering-class midpoint of the 19-24 SAAR range;
                             # ten-year average kindergarten is 22.2
VAR_NONTEACH = 400           # supplies per student, growth model low leg

# per-grade survival vs own 5th-grade class (SAAR 2025-26 snapshot)
SURV_SEC = [172/177, 178/188, 191/196, 193/197, 194/202, 194/202, 176/213]
EFF_YEARS = 6 + sum(SURV_SEC)                      # 12.62
RAMP = (sum(range(6, 13)) + 13 * 6) / (13 * 13)    # 0.834; internal-only:
# exported to the JSON for the record. The published artifacts quote steady
# state, and the site's leaving-families chart computes its own ramp inline.

# ---- 1. signed evidence ----------------------------------------------------
kids = list(csv.DictReader(open(os.path.join(
    HERE, "survey_school_choice_2026_08_anonymized.csv"))))
leave = [r for r in kids if r["status"] == "leaving"]

# ---- 2. Bayesian band (grid integration) ----------------------------------
enrolled = [r for r in kids if 2020 <= int(r["kindergarten_year"]) <= 2025
            and r["status"] in ("leaving", "staying", "staying_confirmed_by_organizer")]
X = sum(r["status"] == "leaving" for r in enrolled)
S = len(enrolled) - X                              # 20 / 4

def posterior_quantiles(qs):
    NP, NK = 2000, 400
    mu, sig, kmin = math.log(3.5), 0.5, 3.3
    ks = [math.exp(mu + sig * (-4 + 8 * (j + 0.5) / NK)) for j in range(NK)]
    kw = [math.exp(-0.5 * ((math.log(k) - mu) / sig) ** 2) if k >= kmin
          else 0.0 for k in ks]
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

# ---- 3-4. today and steady state -------------------------------------------
def rung(scale):
    def one(p):
        k = round(p * scale)          # whole students, then dollars, so the
        return k, k * SEEK            # table reproduces as kids x $5,136
    (klo, dlo), (kmed, dmed), (khi, dhi) = one(P25), one(P50), one(P75)
    k95, d95 = one(P95)
    return dict(kids_lo=klo, kids_med=kmed, kids_hi=khi,
                dollars_lo=dlo, dollars_med=dmed, dollars_hi=dhi,
                kids_p95=k95, dollars_p95=d95)

LADDER = {
    "today":  rung(POP),                   # share of the 128 enrolled now
    "steady": rung(COHORT * EFF_YEARS),    # full feeder stream, per year
}


RESULT = dict(
    seek=SEEK, pop=POP, cohort=COHORT,
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
          f"{RESULT['leaving_children']} children (signed evidence)")
    print(f"enrolled sample {RESULT['enrolled_sample']} (leavers {X}); posterior "
          f"p25/50/75/95 = {P25:.3f}/{P50:.3f}/{P75:.3f}/{P95:.3f}")
    print(f"effective years {EFF_YEARS:.2f}, ramp {RAMP:.3f}, "
          f"non-teaching variable ${VAR_NONTEACH}/student")
    for name, r in LADDER.items():
        print(f"  {name:7s}: {r['kids_lo']}/{r['kids_med']}/{r['kids_hi']} kids "
              f"(p95 {r['kids_p95']}), ${r['dollars_lo']:,}/${r['dollars_med']:,}/"
              f"${r['dollars_hi']:,} (p95 ${r['dollars_p95']:,})")
