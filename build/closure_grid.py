"""Enumerate the v4.2 closure grid and print its published statistics.

Seven levers, every value sourced in the report and the Closure_Model tab.
Staffing is priced the way the district prices it: the "Response to the 10
Questions" Appendix A.1 fully loaded, 0-years-experience figure, so the model
and the district's own worksheet argue on the same basis.

  non-salary fixed capture:  50% / 75% / 100% of the $107,039 of building-
                             bound lines in the district's own closure
                             worksheet (Appendix A, archived), utilities,
                             telecom, maintenance and custodial supplies,
                             with the district's ~$20,000 insurance saving
                             added at the full stop: $53,519 / $80,279 /
                             $127,039. The worksheet's other $40,693, general
                             supplies, books, field trips and printing,
                             travels with the students ($318/student, against
                             our independently measured $331) and is not
                             avoidable
  fixed-position retention:  100% / 50% / 0% of the $218,154 of fixed-position
                             salary lines (school admin $131,724 + custodial
                             $37,333 + library $49,097, all measured; the
                             district's own staffing sheet prices the same
                             four roles at $209,700, within 4 percent)
  teachers cut:              0 / 1 / 2 / 3 positions. The district's Appendix
                             A.1 prices 2 ("Elementary Teachers: 2,
                             $108,958.80"); its own Appendix B classroom
                             arithmetic supports 3 (six NMES homerooms
                             absorbed, only grades 2, 3 and 4 need a new
                             room, so three homerooms are recreated and
                             three are eliminated). The top leg credits the
                             stronger of the district's two figures. Each
                             position is priced at the district's OWN fully
                             loaded basis, $54,479.40 (Appendix A.1, 0 years
                             experience, benefits included), replacing the
                             former $50-75K cost lever: their number, their
                             basis. Archived
                             build/response_to_the_10_questions.pdf
  students lost:             0 / 10 / 20 / 30 percent of 128 (site slider runs
                             the full 0-100%)
  SEEK add-ons per leaver:   $0 / $500 / $1,000 on top of the $4,626 base
                             (at-risk 15% weight on a ~72% FRL school,
                             exceptional-child weights, transportation
                             component, $100 capital outlay)
  property-value loss:       $0 / $47,500 / $95,000 (roughly 0-10 percent of an
                             estimated zone tax base; PVA records ask pending)
  added busing:              $20,000 / $63,000 / $190,000, derived bottom-up
                             with uncertainty carried in the stops: 2-4 zone
                             buses now terminating in Paris (~9-11 road miles
                             farther one-way), 2 loaded legs daily plus 0-2
                             deadhead legs, 175 days, $3.25-$4.75 per mile
                             (KDE/NAPT benchmark band; the district's own
                             routing data was requested and answered N/A), the
                             high stop adding one $45,000 ride-time route
                             split. Per zone student: $160 / $492 / $1,495
                             against the district's $1,032 average.

net = capture + fixed_positions_cut + teachers_cut x $54,479.40
      - busing - leavers x (4,626 + add_ons) - property_loss

Run:  python build/closure_grid.py
Asserts the published statistics: 3,888 scenarios; median +$41,787; 40 percent
negative; range -$445,269 to +$488,631; middle half -$68,095 to +$152,136.
"""
import statistics

SEEK = 4626
CAPTURE = (53_519, 80_279, 127_039)         # district worksheet, building-bound
FIXED_POS = 131724 + 37333 + 49097          # 218,154 measured
TEACH = 108_958.80 / 2                      # $54,479.40, the district's own
                                            # fully loaded rookie (Appendix A.1)

nets = sorted(
    c + f + t * TEACH - b - l * (SEEK + ad) - pr
    for c in CAPTURE
    for f in (0, FIXED_POS / 2, FIXED_POS)
    for t in (0, 1, 2, 3)
    for l in (0, 13, 26, 38)
    for ad in (0, 500, 1000)
    for pr in (0, 47_500, 95_000)
    for b in (20_000, 63_000, 190_000)
)
n = len(nets)
med = statistics.median(nets)
neg = sum(1 for x in nets if x < 0)

assert n == 3_888, n
assert round(med) == 41_787, med
assert round(neg / n * 100) == 40, neg / n
assert round(nets[0]) == -445_269 and round(nets[-1]) == 488_631, (nets[0], nets[-1])
assert round(nets[n // 4]) == -68_095 and round(nets[3 * n // 4]) == 152_136

print(f"{n:,} scenarios | median ${med:,.0f} | {neg / n * 100:.0f}% lose money")
print(f"range ${nets[0]:,.0f} to ${nets[-1]:,.0f} | middle half "
      f"${nets[n // 4]:,.0f} to ${nets[3 * n // 4]:,.0f}")
