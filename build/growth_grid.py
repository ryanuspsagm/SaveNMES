"""Enumerate the v4.4 growth grid and print its published statistics.

The growth calculator prices recruiting NMES from 110 (the district's own
figure, source documentation still requested; last official count 128) up to
200 (the 2013 state-approved plan rated the building 198).

HEADROOM (v4.3, at the user's direction): the first 25 added students fill
seats the school already has open at the district's OWN grade-specific
class-size caps, published in Appendix B of its response (24 per room in
K-3, 28 in fourth, 29 in fifth). Applied to the 2024-25 grade counts
(22/22/19/22/16/27), the six existing homerooms hold 153 students against
128 enrolled: 25 open seats. The architect slide in the same packet rates
the building at 154, corroborating the count. This is the same standard the
district uses when it charges new classrooms at the receiving schools in
the closure case. Teachers increment beyond the 25 seats.

  added students:        10 to 90 (site slider runs every whole student)
  seats already open:    25 (fixed; the district's own Appendix B caps)
  teacher trigger:       selectable hiring pace, one teacher per FULL cohort
                         of 14 / 16 / 24 added students BEYOND the 25 open
                         seats. Every leg is measured, not assumed:
                         14 = today's staffing (128 students / 9.41 NCES
                         classroom-teacher FTE = 13.6); 16 = the median
                         students-per-teacher ratio in the eight federal-file
                         years NMES ran over 200 students (1996-2008, CCD,
                         archived build/bourbon_staffing_ratios_ccd.csv);
                         24 = the district's own K-3 class cap (Appendix B).
                         Priced at the certified schedule's entry-to-midpoint
                         rows: $41,718 / $49,150 / $56,583 (new positions are
                         new hires, not 25-year veterans)
  support staff:         none (best case) / 1 per 75 / 1 per 50 added
                         students, at the school's own classified lines:
                         $20,000 / $28,500 / $37,000 (support scales from
                         the first student; only teaching absorbs)
  busing per recruit:    $0 / $500 / $1,000 (district average transport spend
                         is $1,032 per enrolled student; $0 is real because
                         the district sets its own busing policy)
  marginal cost/student: $400 / $700 / $1,000 (measured student-scaling
                         spend at location 090 is $331)
  SEEK add-ons/student:  $0 / $500 / $1,000 above the $4,626 base (at-risk,
                         exceptional-child, transportation, capital outlay);
                         the published headline is the base-only median

net = gain x (4,626 + add_ons - marginal) - teachers x salary
      - staff x classified - busing x gain
teachers = floor(max(0, gain - 25) / ratio)

Run:  python build/growth_grid.py
Asserts the published statistics: base-only median +$102,780; 17 of the
6,561 base scenarios negative (0.26 percent), floor -$26,992 (a teacher
hired for every 14 added at the top salary with every other cost at
maximum), ceiling +$296,904; full-lever median +$125,150, ceiling +$386,904.
Growth pays in 99.7 percent of scenarios.
"""
import math
import statistics

SEEK = 4626
HEADROOM = 25  # open seats at the district's own Appendix B caps


def net(gain, ratio, staff_per, teacher_cost, staff_cost, bus, cps, addons):
    teachers = math.floor(max(0, gain - HEADROOM) / ratio)
    staff = 0 if staff_per == 0 else math.floor(gain / staff_per)
    return (gain * (SEEK + addons - cps) - teachers * teacher_cost
            - staff * staff_cost - bus * gain)


ARGS = dict(
    gains=range(10, 91, 10), ratios=(14, 16, 24), staff_pers=(0, 75, 50),
    tcosts=(41_718, 49_150, 56_583), scosts=(20_000, 28_500, 37_000),
    buses=(0, 500, 1000), cpss=(400, 700, 1000),
)


def grid(addon_values):
    return sorted(
        net(g, r, sp, tc, sc, b, c, ad)
        for g in ARGS["gains"] for r in ARGS["ratios"] for sp in ARGS["staff_pers"]
        for tc in ARGS["tcosts"] for sc in ARGS["scosts"]
        for b in ARGS["buses"] for c in ARGS["cpss"] for ad in addon_values)


base = grid((0,))
full = grid((0, 500, 1000))
assert len(base) == 6_561 and len(full) == 19_683
assert round(statistics.median(base)) == 102_780, statistics.median(base)
assert base[0] == -26_992 and base[-1] == 296_904, (base[0], base[-1])
neg_base = sum(1 for x in base if x < 0)
assert neg_base == 17, neg_base
assert round(statistics.median(full)) == 125_150, statistics.median(full)
assert full[-1] == 386_904, full[-1]

# the site default is a real grid combo at the exact median: 30 added,
# historical 1-per-16 pace, $49,150 teacher, 1 per 50 support at $37,000,
# $500 busing, $700 supplies, base-only (no hires trigger below 153)
site_default = net(30, 16, 50, 49_150, 37_000, 500, 700, 0)
assert site_default == 102_780 == statistics.median(base), site_default

print(f"base-only: {len(base):,} scenarios | median ${statistics.median(base):,.0f} "
      f"| floor ${base[0]:,.0f} | ceiling ${base[-1]:,.0f} "
      f"| {neg_base} negative")
print(f"with add-ons lever: {len(full):,} scenarios | median ${statistics.median(full):,.0f} "
      f"| ceiling ${full[-1]:,.0f}")
print(f"site default: ${site_default:,} (the exact grid median)")
