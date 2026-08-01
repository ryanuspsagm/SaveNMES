"""Enumerate the v4.2 closure grid and print its published statistics.

Eight levers, every value sourced in the report and the Closure_Model tab:
  non-salary fixed capture:  50% / 75% / 100% of the $58,774 plant-utilities
                             base (measured, FY2026 working budget, loc 090)
  fixed-position retention:  100% / 50% / 0% of the $218,154 of fixed-position
                             salary lines (school admin $131,724 + custodial
                             $37,333 + library $49,097, all measured)
  teacher retention:         100% to 0% of ~5 GF positions (0 / 2 / 3 / 5)
  GF cost per position:      $50,000 / $60,000 / $75,000
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

net = capture + fixed_positions_cut + teachers_cut x cost
      - busing - leavers x (4,626 + add_ons) - property_loss

Run:  python build/closure_grid.py
Asserts the published statistics: 11,664 scenarios; median +$69,575; 36 percent
negative; range -$469,401 to +$631,928; middle half -$56,860 to +$196,640.
"""
import statistics

SEEK = 4626
NONSALARY = 58774
FIXED_POS = 131724 + 37333 + 49097          # 218,154 measured
TRANSPORT = 2_700_000

nets = sorted(
    c + f + t * p - b - l * (SEEK + ad) - pr
    for c in (0.50 * NONSALARY, 0.75 * NONSALARY, 1.00 * NONSALARY)
    for f in (0, FIXED_POS / 2, FIXED_POS)
    for t in (0, 2, 3, 5)
    for p in (50_000, 60_000, 75_000)
    for l in (0, 13, 26, 38)
    for ad in (0, 500, 1000)
    for pr in (0, 47_500, 95_000)
    for b in (20_000, 63_000, 190_000)
)
n = len(nets)
med = statistics.median(nets)
neg = sum(1 for x in nets if x < 0)

assert n == 11_664, n
assert round(med) == 69_575, med
assert round(neg / n * 100) == 36, neg / n
assert round(nets[0]) == -469_401 and round(nets[-1]) == 631_928, (nets[0], nets[-1])
assert round(nets[n // 4]) == -56_860 and round(nets[3 * n // 4]) == 196_640

print(f"{n:,} scenarios | median ${med:,.0f} | {neg / n * 100:.0f}% lose money")
print(f"range ${nets[0]:,.0f} to ${nets[-1]:,.0f} | middle half "
      f"${nets[n // 4]:,.0f} to ${nets[3 * n // 4]:,.0f}")
