"""Enumerate the v4.2 growth grid and print its published statistics.

The growth calculator prices recruiting NMES from 110 (the district's own
figure, source documentation still requested; last official count 128) up to
200 (the 2013 state-approved plan rated the building 198). Hiring scales
strictly with the enrollment gain, and NO absorption by existing classrooms
is assumed (v4.2 review): a teacher is charged for every full added cohort
starting with the first one.

  added students:        10 to 90 (site slider runs every whole student)
  teacher trigger:       one teacher per FULL cohort of 20 / 22 / 25 added
                         students, from the first student, priced at the
                         certified schedule's entry-to-midpoint rows:
                         $41,718 / $49,150 / $56,583 (new positions are new
                         hires, not 25-year veterans)
  support staff:         none (best case) / 1 per 75 / 1 per 50 added
                         students, at the school's own classified lines:
                         $20,000 / $28,500 / $37,000
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

Run:  python build/growth_grid.py
Asserts the published statistics: base-only median +$67,124; 106 of 6,561
base scenarios (1.6 percent) negative, floor -$53,252 (the costliest teacher
hired for every 20 students at maximum charges), ceiling +$255,186;
full-lever median +$87,890, ceiling +$345,186. Growth comes out ahead in
more than 98 percent of scenarios.
"""
import math
import statistics

SEEK = 4626


def net(gain, ratio, staff_per, teacher_cost, staff_cost, bus, cps, addons):
    teachers = math.floor(gain / ratio)          # no absorption credit (v4.2 review)
    staff = 0 if staff_per == 0 else math.floor(gain / staff_per)
    return (gain * (SEEK + addons - cps) - teachers * teacher_cost
            - staff * staff_cost - bus * gain)


ARGS = dict(
    gains=range(10, 91, 10), ratios=(20, 22, 25), staff_pers=(0, 75, 50),
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
assert round(statistics.median(base)) == 67_124, statistics.median(base)
assert base[0] == -53_252 and base[-1] == 255_186, (base[0], base[-1])
neg_base = sum(1 for x in base if x < 0)
assert neg_base == 106, neg_base
assert round(statistics.median(full)) == 87_890, statistics.median(full)
assert full[-1] == 345_186, full[-1]

print(f"base-only: {len(base):,} scenarios | median ${statistics.median(base):,.0f} "
      f"| floor ${base[0]:,.0f} | ceiling ${base[-1]:,.0f} "
      f"| {neg_base} negative ({neg_base/len(base)*100:.1f}%)")
print(f"with add-ons lever: {len(full):,} scenarios | median ${statistics.median(full):,.0f} "
      f"| ceiling ${full[-1]:,.0f}")
