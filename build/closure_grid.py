"""Enumerate the v4.5 closure grid and print its published statistics.

Seven levers, every value sourced in the report and the Closure_Model tab.
Staffing is priced the way the district prices it: the "Response to the 10
Questions" Appendix A.1 fully loaded, 0-years-experience figure, so the model
and the district's own worksheet argue on the same basis.

WEIGHTING (v4.5). Each lever carries an explicit distribution and scenario
weights multiply. Two shapes only:
  triangular (weights 1-2-1): used when the record pins a central setting,
      so the documented central counts double and the two ends count once
  uniform (all settings equal): used when the record gives no defensible
      center, which is exactly where honesty forbids inventing one
The published median, middle half (25th to 75th percentile) and share of
scenarios that lose money are computed under these weights. The floor and
ceiling are the grid's true extremes and do not depend on weights.

  non-salary fixed capture:  50% / 75% / 100% of the $107,039 of building-
                             bound lines in the district's own closure
                             worksheet (Appendix A, archived), utilities,
                             telecom, maintenance and custodial supplies,
                             with the district's ~$20,000 insurance saving
                             added at the full stop: $53,519 / $80,279 /
                             $127,039. TRIANGULAR: the legs were built as
                             low / central / high reads of the same
                             worksheet lines. The worksheet's other $40,693,
                             general supplies, books, field trips and
                             printing, travels with the students
                             ($318/student, against our independently
                             measured $331) and is not avoidable
  fixed-position retention:  100% / 50% / 0% of the $214,104 of fixed-position
                             lines in the district's own MUNIS ledger, FY2026
                             actuals (school admin $115,397 + custodial
                             $49,655 + library $49,052; the district's own
                             staffing sheet prices the same four roles at
                             $209,700, within 2 percent). The
                             0%-retention leg is an attrition end state:
                             Appendix A.1 states all current staff would be
                             retained in year one, with savings recovered
                             only as staff across the district resign.
                             TRIANGULAR: half-recovered is the natural
                             center of an attrition path that starts at
                             zero and may finish at full
  teachers cut:              0 / 1 / 2 / 3 positions. The district's Appendix
                             A.1 prices 2 ("Elementary Teachers: 2,
                             $108,958.80"); its own Appendix B classroom
                             count supports 3 (six NMES homerooms absorbed,
                             only grades 2, 3 and 4 need a new room, so
                             three homerooms are recreated and three are
                             eliminated); year one is 0 by the district's
                             own retention note. UNIFORM: the district's own
                             documents disagree, so no leg gets extra weight.
                             Each position priced at the district's OWN
                             fully loaded basis, $54,479.40 (Appendix A.1,
                             0 years experience, benefits included).
                             Archived build/response_to_the_10_questions.pdf
  students lost:             0 / 10 / 20 / 30 / 40 / 50 percent of 128
                             (0 / 13 / 26 / 38 / 51 / 64 students; the site
                             slider caps at the same 50%, so the calculator
                             never prices outside the grid). UNIFORM: how many
                             families leave is the genuine unknown, the one
                             cost the district's response never prices, and
                             the record offers no central estimate
  SEEK add-ons per leaver:   $0 / $500 / $1,000 on top of the $4,626 base
                             (at-risk 15% weight on a ~72% FRL school,
                             exceptional-child weights, transportation
                             component, $100 capital outlay). TRIANGULAR:
                             the ~$500 middle is the documented read of
                             this school's actual add-ons
  property-value loss:       $0 / $47,500 / $95,000 (roughly 0-10 percent of an
                             estimated zone tax base; PVA records ask pending).
                             TRIANGULAR around the middle of the estimated
                             band. Kept as real foregone revenue: the board's
                             rate-setting practice does not raise rates to
                             compensate for zone valuation losses, so a
                             smaller base is lost revenue capacity, and the
                             equity hit lands on zone families either way
  added busing:              $20,000 / $63,000 / $190,000, derived bottom-up
                             with uncertainty carried in the stops: 2-4 zone
                             buses now terminating in Paris (~9-11 road miles
                             farther one-way), 2 loaded legs daily plus 0-2
                             deadhead legs, 175 days, $3.25-$4.75 per mile
                             (KDE/NAPT benchmark band; the July 2026 records
                             response produced the current routes but answered
                             N/A for any routing study or ride-time
                             analysis), the
                             high stop adding one $45,000 ride-time route
                             split. Per zone student: $160 / $492 / $1,495
                             against the district's $1,032 average.
                             TRIANGULAR: $63,000 is the derived central
                             estimate

net = capture + fixed_positions_cut + teachers_cut x $54,479.40
      - busing - leavers x (4,626 + add_ons) - property_loss

Run:  python build/closure_grid.py
Asserts the published statistics: 5,832 scenarios; weighted median -$20,007;
55 percent lose money; middle half -$137,095 to +$98,603; range -$591,545
to +$484,582; the all-staff-retained site default (-$130,749) sits at the
26th percentile. Unweighted median -$24,431 kept as a cross-check: the
weighting moves the median by about $4,000 and changes no conclusion.
"""
import statistics
from itertools import product

SEEK = 4626
TEACH = 108_958.80 / 2                      # $54,479.40, the district's own
                                            # fully loaded rookie (Appendix A.1)
FIXED_POS = 115397.25 + 49655.38 + 49051.77  # 214,104.40: MUNIS FY2026 actuals
                                              # (school admin 2410+2420, custodial
                                              # block of 2610, library 2222; see
                                              # build/munis_extract.py)

TRI = (1, 2, 1)
CAPTURE = [(53_519, 1), (80_279, 2), (127_039, 1)]           # triangular
FIXED = [(0, 1), (FIXED_POS / 2, 2), (FIXED_POS, 1)]         # triangular
TEACHERS = [(t, 1) for t in (0, 1, 2, 3)]                    # uniform
LEAVERS = [(l, 1) for l in (0, 13, 26, 38, 51, 64)]          # uniform
ADDONS = [(0, 1), (500, 2), (1000, 1)]                       # triangular
PROP = [(0, 1), (47_500, 2), (95_000, 1)]                    # triangular
BUS = [(20_000, 1), (63_000, 2), (190_000, 1)]               # triangular

pairs = sorted(
    (c + f + t * TEACH - b - l * (SEEK + ad) - pr,
     wc * wf * wt * wl * wa * wp * wb)
    for (c, wc), (f, wf), (t, wt), (l, wl), (ad, wa), (pr, wp), (b, wb)
    in product(CAPTURE, FIXED, TEACHERS, LEAVERS, ADDONS, PROP, BUS)
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
default = 127_039 - 63_000 - 38 * (SEEK + 500)   # all staff retained, central legs
default_rank = sum(w for v, w in pairs if v <= default) / total_w

assert n == 5_832, n
assert round(med) == -20_007, med
assert round(p25) == -137_095 and round(p75) == 98_603, (p25, p75)
assert round(neg * 100) == 55, neg
assert round(nets[0]) == -591_545 and round(nets[-1]) == 484_582, (nets[0], nets[-1])
assert round(default) == -130_749, default
assert 0.24 < default_rank < 0.28, default_rank
assert round(statistics.median(nets)) == -24_431   # unweighted cross-check

print(f"{n:,} scenarios | weighted median ${med:,.0f} | {neg * 100:.0f}% lose money")
print(f"range ${nets[0]:,.0f} to ${nets[-1]:,.0f} | middle half "
      f"${p25:,.0f} to ${p75:,.0f}")
print(f"site default (all staff retained) ${default:,.0f} | rank {default_rank * 100:.0f}%")
print(f"unweighted median ${statistics.median(nets):,.0f} (cross-check)")
