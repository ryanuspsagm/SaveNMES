"""Enumerate the v5.0 closure grid and print its published statistics.

Six levers, every value sourced in the report and the Closure_Model tab.
Staffing is priced the way the district prices it: the "Response to the 10
Questions" Appendix A.1 fully loaded, 0-years-experience figure, so the model
and the district's own worksheet argue on the same basis.

WHAT CHANGED IN v5.0. The old students-lost lever (0-64, a year-one guess
priced before any family had been asked) is replaced by the school-choice
survey and the statistics built on it, expressed at steady state: a child
who leaves is missing from the rolls for every remaining grade, kindergarten
through 12th, discounted by the district's own measured grade-to-grade
survival (12.62 effective years, exodus_model.py). Each missing student
is priced at the ENACTED FY2027 SEEK base of $4,636 (2026-28 budget; the
$4,626 used before v5.0 was the House-version figure and is corrected),
plus the add-ons lever, minus the $400 of supplies that stop being spent,
the same low-leg figure the growth model charges each recruit. Supplies
scale with students inside the leaver term; teacher savings are priced
ONLY on the teachers-cut lever, so staffing savings are never counted
twice.

WEIGHTING (unchanged from v4.5). Each lever carries an explicit distribution
and scenario weights multiply. Triangular (1-2-1) when the record pins a
central setting; uniform when it does not. The floor and ceiling are the
grid's true extremes and do not depend on weights.

  non-salary fixed capture:  $53,519 / $80,279 / $127,039, TRIANGULAR.
                             50% / 75% / 100% of the building-bound lines in
                             the district's own closure worksheet (Appendix A)
                             plus ~$20,000 insurance at the full stop.
  fixed-position retention:  $0 / $107,052 / $214,104, TRIANGULAR. MUNIS
                             FY2026 actuals (school admin $115,397 +
                             custodial $49,655 + library $49,052); $0 is the
                             district's own year-one stance (all staff
                             retained), full recovery is an attrition
                             end state.
  teachers cut:              0 / 1 / 2 / 3 positions, UNIFORM, at the
                             district's own fully loaded $54,479.40. Its
                             Appendix A.1 prices 2; its Appendix B classroom
                             count supports 3; year one is 0 by its own
                             retention note.
  students lost (steady state): 137 / 167 / 194 students missing from the
                             district's rolls in a year, TRIANGULAR like
                             every other centered lever: the posterior 25th /
                             50th / 75th percentile at the class-size
                             midpoint, from the August 2026 school-choice
                             survey (31 leaving households, 70 children,
                             anonymized in this folder) and the selection-
                             corrected estimate built on it (exodus_model.py).
                             The signed-survey floor, 74 (5.83 leavers per
                             class x 12.62 effective years, named respondents
                             only), sits BELOW every priced leg and is kept
                             as hard evidence in Section 5, not as a
                             scenario; interim drafts carried it (and a
                             skeptic's leg below it) as grid legs. The
                             state's own SAAR file corroborates the band
                             from outside the survey: the 2025-26
                             kindergarten enrolled 12 children against a
                             21-31 norm, and the school ended 2025-26 at 115
                             after ending 2024-25 at 128.
  SEEK add-ons per leaver:   $0 / $500 / $1,000 on top of the $4,636 base,
                             TRIANGULAR (at-risk weight on a ~72% FRL school,
                             exceptional-child weights, transportation,
                             capital outlay).
  added busing:              $20,000 / $63,000 / $95,000, TRIANGULAR,
                             derived bottom-up from the produced routes; the
                             high leg is capped at half the bottom-up maximum
                             (v5.0 review). A property-value lever ($0-$95,000)
                             was priced in an interim draft and removed while
                             the PVA records request is pending; the community
                             research on property effects stays in Section 6.

net = capture + fixed_positions_cut + teachers_cut x $54,479.40
      - busing - leavers x (4,636 + add_ons - 400)

Run:  python build/closure_grid.py
Asserts the published statistics: 972 scenarios; weighted median
-$571,883; EVERY priced scenario loses money (the best case still loses
$95,750); middle half -$679,361 to -$467,862; range -$1,057,265 to
-$95,750; the site default (-$456,383: building sold, half the fixed
positions cut over time, three teachers cut with the emptied classrooms,
median leavers) sits at the 77th percentile, friendlier than three
quarters of the grid, because it grants closure every saving that scales
with students; the median exodus still sinks it.
Unweighted median -$566,628 kept as a cross-check.
"""
import statistics
from itertools import product

SEEK = 4636                                 # enacted FY2027 base, 2026-28 budget
SUPPLIES = 400                              # scales with each missing student
TEACH = 108_958.80 / 2                      # $54,479.40, the district's own
                                            # fully loaded rookie (Appendix A.1)
FIXED_POS = 115397.25 + 49655.38 + 49051.77  # 214,104.40: MUNIS FY2026 actuals

CAPTURE = [(53_519, 1), (80_279, 2), (127_039, 1)]           # triangular
FIXED = [(0, 1), (FIXED_POS / 2, 2), (FIXED_POS, 1)]         # triangular
TEACHERS = [(t, 1) for t in (0, 1, 2, 3)]                    # uniform
LEAVERS = [(137, 1), (167, 2), (194, 1)]   # triangular on the band's quartiles
ADDONS = [(0, 1), (500, 2), (1000, 1)]                       # triangular
BUS = [(20_000, 1), (63_000, 2), (95_000, 1)]                # triangular; high
                                                             # leg = half the max

pairs = sorted(
    (c + f + t * TEACH - b - l * (SEEK + ad - SUPPLIES),
     wc * wf * wt * wl * wa * wb)
    for (c, wc), (f, wf), (t, wt), (l, wl), (ad, wa), (b, wb)
    in product(CAPTURE, FIXED, TEACHERS, LEAVERS, ADDONS, BUS)
)
nets = [v for v, _ in pairs]
total_w = sum(w for _, w in pairs)


def wpct(q):
    c = 0
    for v, w in pairs:
        c += w
        if c >= q * total_w:
            return v


n = len(pairs)
med = wpct(0.50)
p25, p75 = wpct(0.25), wpct(0.75)
neg = sum(w for v, w in pairs if v < 0) / total_w
default = (127_039 + FIXED_POS / 2 + 3 * TEACH - 63_000
           - 167 * (SEEK + 500 - SUPPLIES))  # scaled savings granted,
                                             # median leavers
default_rank = (sum(w for v, w in pairs if v < default - 0.005)
                + sum(w for v, w in pairs if abs(v - default) <= 0.005) / 2
                ) / total_w                  # ties half-weighted, the site
                                             # JS convention

assert n == 972, n
assert round(med) == -571_883, med
assert round(p25) == -679_361 and round(p75) == -467_862, (p25, p75)
assert round(neg * 100) == 100, neg
assert round(nets[0]) == -1_057_265 and round(nets[-1]) == -95_750, (nets[0], nets[-1])
assert round(default) == -456_383, default
assert 0.75 < default_rank < 0.79, default_rank
assert round(statistics.median(nets)) == -566_628

print(f"{n:,} scenarios | weighted median ${med:,.0f} | {neg * 100:.0f}% lose money")
print(f"range ${nets[0]:,.0f} to ${nets[-1]:,.0f} | middle half "
      f"${p25:,.0f} to ${p75:,.0f}")
print(f"site default (scaled savings granted) ${default:,.0f} | rank {default_rank * 100:.0f}%")
print(f"unweighted median ${statistics.median(nets):,.0f} (cross-check)")
