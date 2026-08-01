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
  teacher trigger:       selectable hiring pace, one CLASSROOM teacher per
                         FULL new class of 18 / 21 / 24 added students BEYOND
                         the 25 open seats. Indexed on classroom teachers
                         (v4.4 review: 'index it on teacher staff, not fixed
                         staff'), and every leg is a real classroom count:
                         18 = smaller classes than the school runs today;
                         21 = today's actual class size (128 students across
                         six homerooms = 21.3); 24 = the district's own K-3
                         class cap (Appendix B). Support and other fixed
                         staff ride their own lever below, NOT this one.
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
                         enumerated in the headline grid, the SAME three legs
                         the closure model prices for each leaver, so the two
                         models treat state add-ons symmetrically

net = gain x (4,626 + add_ons - marginal) - teachers x salary
      - staff x classified - busing x gain
teachers = floor(max(0, gain - 25) / ratio)

Run:  python build/growth_grid.py
Asserts the published statistics: headline grid (add-ons enumerated, matching
the closure model) 19,683 scenarios, median +$140,331, floor +$3,331 (a
class of 18 at the top salary with every cost at maximum and no add-ons),
ceiling +$386,904, ZERO negative: with the district's own 25 open seats and
classroom-indexed hiring, growth pays in every scenario. Base-only cut:
median +$117,040.
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
    gains=range(10, 91, 10), ratios=(18, 21, 24), staff_pers=(0, 75, 50),
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
assert round(statistics.median(full)) == 140_331, statistics.median(full)
assert full[0] == 3_331 and full[-1] == 386_904, (full[0], full[-1])
neg_full = sum(1 for x in full if x < 0)
assert neg_full == 0, neg_full
assert round(statistics.median(base)) == 117_040, statistics.median(base)

# the site default is a real grid combo at the median rank (50.0%):
# 70 added, one class per 21 (today's class size; 2 teachers past the 25
# seats), entry-row $41,718 teacher, 1 per 50 support at $37,000, busing at
# its $1,000 maximum, $400 supplies, $500 add-ons (the closure default leg)
site_default = net(70, 21, 50, 41_718, 37_000, 1000, 400, 500)
assert site_default == 140_384, site_default
rank = sum(1 for x in full if x <= site_default) / len(full)
assert 0.49 < rank < 0.51, rank

print(f"headline (add-ons enumerated): {len(full):,} scenarios "
      f"| median ${statistics.median(full):,.0f} | floor ${full[0]:,.0f} "
      f"| ceiling ${full[-1]:,.0f} | {neg_full} negative")
print(f"base-only cut: median ${statistics.median(base):,.0f}")
print(f"site default: ${site_default:,} (rank {rank*100:.1f}%)")
