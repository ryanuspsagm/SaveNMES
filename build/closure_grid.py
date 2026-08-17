"""Enumerate the v5.0 closure grid and print its published statistics.

Eight levers, every value sourced in the report and the Closure_Model tab.
Staffing is priced the way the district prices it: the "Response to the 10
Questions" Appendix A.1 fully loaded, 0-years-experience figure, so the model
and the district's own worksheet argue on the same basis.

WHAT CHANGED IN v5.0. The old students-lost lever (0-64, a year-one guess
priced before any family had been asked) is replaced by the school-choice
survey and the statistics built on it, expressed at steady state: a child
who leaves is missing from the rolls for every remaining grade, kindergarten
through 12th, discounted by the district's own measured grade-to-grade
survival (12.62 effective years, exodus_model.py). A new lever prices the
variable cost the district sheds as students leave, so the model now runs
the leaver cost net of cost response instead of assuming the district
sheds nothing.

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
  students lost (steady state): 38 / 73 / 137 / 167 / 194 students missing
                             from the district's rolls in a year, WEIGHTED
                             1-2-2-2-1. From the August 2026 school-choice
                             survey (30 leaving households, 69 children,
                             anonymized in this folder) and the selection-
                             corrected estimate built on it (exodus_model.py):
                             73 = the survey floor, named respondents only,
                             5.75 leavers per class x 12.62 effective years;
                             137 / 167 / 194 = the posterior 25th / 50th /
                             75th percentile at the class-size midpoint;
                             38 = half the floor, kept as the skeptic's leg
                             for intent that never becomes action. The state's
                             own SAAR file corroborates the band from outside
                             the survey: the 2025-26 kindergarten enrolled 12
                             children against a 21-31 norm, and the school
                             ended 2025-26 at 115 after ending 2024-25 at 128.
  SEEK add-ons per leaver:   $0 / $500 / $1,000 on top of the $4,626 base,
                             TRIANGULAR (at-risk weight on a ~72% FRL school,
                             exceptional-child weights, transportation,
                             capital outlay).
  variable cost shed per leaver: $0 / $1,585 / $2,642, TRIANGULAR. What the
                             district stops spending when a student leaves:
                             $2,642 = one teacher per 25.4 students (SBDM
                             allocation sheet, 463 students / 18.2 teachers)
                             at $54,479.40, plus $500 non-personnel
                             (assumption, flagged), if sections consolidate
                             perfectly; $1,585 = 60% consolidation friction;
                             $0 = the district's stated stance that all
                             staff are retained. The leaver term nets this
                             against the SEEK loss.
  property-value loss:       $0 / $47,500 / $95,000, TRIANGULAR (0-10% of an
                             estimated zone tax base; PVA records ask pending).
  added busing:              $20,000 / $63,000 / $190,000, TRIANGULAR,
                             derived bottom-up from the produced routes.

net = capture + fixed_positions_cut + teachers_cut x $54,479.40
      - busing - leavers x (4,626 + add_ons - shed) - property_loss

Run:  python build/closure_grid.py
Asserts the published statistics: 14,580 scenarios; weighted median
-$292,348; 88 percent lose money; middle half -$488,920 to -$111,080; range
-$1,322,925 to +$409,190; the all-staff-retained site default (-$310,159,
capture at full stop, floor leavers, nothing shed) sits at the 47th
percentile. Unweighted median -$283,934 kept as a cross-check.
"""
import statistics
from itertools import product

SEEK = 4626
TEACH = 108_958.80 / 2                      # $54,479.40, the district's own
                                            # fully loaded rookie (Appendix A.1)
FIXED_POS = 115397.25 + 49655.38 + 49051.77  # 214,104.40: MUNIS FY2026 actuals

CAPTURE = [(53_519, 1), (80_279, 2), (127_039, 1)]           # triangular
FIXED = [(0, 1), (FIXED_POS / 2, 2), (FIXED_POS, 1)]         # triangular
TEACHERS = [(t, 1) for t in (0, 1, 2, 3)]                    # uniform
LEAVERS = [(38, 1), (73, 2), (137, 2), (167, 2), (194, 1)]   # survey-anchored
ADDONS = [(0, 1), (500, 2), (1000, 1)]                       # triangular
SHED = [(0, 1), (1585, 2), (2642, 1)]                        # triangular
PROP = [(0, 1), (47_500, 2), (95_000, 1)]                    # triangular
BUS = [(20_000, 1), (63_000, 2), (190_000, 1)]               # triangular

pairs = sorted(
    (c + f + t * TEACH - b - l * (SEEK + ad - sh) - pr,
     wc * wf * wt * wl * wa * ws * wp * wb)
    for (c, wc), (f, wf), (t, wt), (l, wl), (ad, wa), (sh, ws), (pr, wp), (b, wb)
    in product(CAPTURE, FIXED, TEACHERS, LEAVERS, ADDONS, SHED, PROP, BUS)
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
default = 127_039 - 63_000 - 73 * (SEEK + 500 - 0)  # all staff retained,
                                                    # floor leavers, no shed
default_rank = sum(w for v, w in pairs if v <= default) / total_w

assert n == 14_580, n
assert round(med) == -292_348, med
assert round(p25) == -488_920 and round(p75) == -111_080, (p25, p75)
assert round(neg * 100) == 88, neg
assert round(nets[0]) == -1_322_925 and round(nets[-1]) == 409_190, (nets[0], nets[-1])
assert round(default) == -310_159, default
assert 0.45 < default_rank < 0.49, default_rank
assert round(statistics.median(nets)) == -283_934

print(f"{n:,} scenarios | weighted median ${med:,.0f} | {neg * 100:.0f}% lose money")
print(f"range ${nets[0]:,.0f} to ${nets[-1]:,.0f} | middle half "
      f"${p25:,.0f} to ${p75:,.0f}")
print(f"site default (all staff retained) ${default:,.0f} | rank {default_rank * 100:.0f}%")
print(f"unweighted median ${statistics.median(nets):,.0f} (cross-check)")
