"""Enumerate the v4.5 growth grid and print its published statistics.

WEIGHTING (v4.5, matching the closure grid). Each lever carries an explicit
distribution and scenario weights multiply. Triangular (1-2-1, the documented
central setting counts double) where the record pins a center; uniform where
it does not. Here every cost lever is triangular, because every middle leg is
the documented central read: class size 21 is today's actual (128 students in
six homerooms), $49,150 is the certified schedule's middle row, $28,500 the
middle classified line, $500 busing and $700 marginal cost the middles of
their derived bands, $500 add-ons the documented read of this school's
actual add-ons. The added-students count stays UNIFORM: it is the target the
board chooses, not a chance the model should weight. The floor and ceiling
are the grid's true extremes and do not depend on weights.


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

  added students:        10 to 90 (the site slider moves in five-student
                         steps, which keeps every reachable setting inside
                         the grid's published floor and ceiling; off-step
                         targets can price a few thousand dollars below the
                         grid floor because the teacher trigger steps)
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
the closure model) 19,683 scenarios, weighted median +$141,780, middle half
+$94,520 to +$182,654, floor +$3,331 (a class of 18 at the top salary with
every cost at maximum and no add-ons), ceiling +$386,904, ZERO negative: with
the district's own 25 open seats and classroom-indexed hiring, growth pays in
every scenario. Base-only cut: weighted median +$117,780. Unweighted median
+$140,331 kept as a cross-check.
"""
import math
import statistics
from itertools import product

SEEK = 4626
HEADROOM = 25  # open seats at the district's own Appendix B caps


def net(gain, ratio, staff_per, teacher_cost, staff_cost, bus, cps, addons):
    teachers = math.floor(max(0, gain - HEADROOM) / ratio)
    staff = 0 if staff_per == 0 else math.floor(gain / staff_per)
    return (gain * (SEEK + addons - cps) - teachers * teacher_cost
            - staff * staff_cost - bus * gain)


GAINS = [(g, 1) for g in range(10, 91, 10)]                  # uniform: board's target
RATIOS = [(18, 1), (21, 2), (24, 1)]                         # triangular: 21 = today
STAFF_PERS = [(0, 1), (75, 2), (50, 1)]                      # triangular
TCOSTS = [(41_718, 1), (49_150, 2), (56_583, 1)]             # triangular
SCOSTS = [(20_000, 1), (28_500, 2), (37_000, 1)]             # triangular
BUSES = [(0, 1), (500, 2), (1000, 1)]                        # triangular
CPSS = [(400, 1), (700, 2), (1000, 1)]                       # triangular
ADDONS_FULL = [(0, 1), (500, 2), (1000, 1)]                  # triangular
ADDONS_BASE = [(0, 1)]


def grid(addon_pairs):
    return sorted(
        (net(g, r, sp, tc, sc, b, c, ad), w1 * w2 * w3 * w4 * w5 * w6 * w7 * w8)
        for (g, w1), (r, w2), (sp, w3), (tc, w4), (sc, w5), (b, w6), (c, w7), (ad, w8)
        in product(GAINS, RATIOS, STAFF_PERS, TCOSTS, SCOSTS, BUSES, CPSS, addon_pairs))


def wpct(pairs, q):
    tot = sum(w for _, w in pairs)
    c = 0
    for v, w in pairs:
        c += w
        if c >= q * tot:
            return v


base = grid(ADDONS_BASE)
full = grid(ADDONS_FULL)
full_nets = [v for v, _ in full]
assert len(base) == 6_561 and len(full) == 19_683
med = wpct(full, 0.50)
p25, p75 = wpct(full, 0.25), wpct(full, 0.75)
assert med == 141_780, med
assert p25 == 94_520 and p75 == 182_654, (p25, p75)
assert full_nets[0] == 3_331 and full_nets[-1] == 386_904
neg_full = sum(1 for x in full_nets if x < 0)
assert neg_full == 0, neg_full
assert wpct(base, 0.50) == 117_780, wpct(base, 0.50)
assert round(statistics.median(full_nets)) == 140_331   # unweighted cross-check

# the site default (v4.5 review) is the weighted median scenario itself:
# 30 added students (target 140), inside the 25 open seats plus a partial
# class at 1 per 21, so no teacher and no support hire trigger; central legs
# on class size, teacher cost and add-ons; $0 busing, $400 supplies. The
# calculator readout states only the percentile the chosen settings reflect.
site_default = net(30, 21, 50, 49_150, 37_000, 0, 400, 500)
assert site_default == 141_780 == med, site_default
tot_w = sum(w for _, w in full)
rank = sum(w for v, w in full if v < site_default) / tot_w
assert 0.48 < rank < 0.52, rank

print(f"headline (add-ons enumerated): {len(full):,} scenarios "
      f"| weighted median ${med:,.0f} | middle half ${p25:,.0f} to ${p75:,.0f} "
      f"| floor ${full_nets[0]:,.0f} | ceiling ${full_nets[-1]:,.0f} | {neg_full} negative")
print(f"base-only cut: weighted median ${wpct(base, 0.50):,.0f}")
print(f"site default: ${site_default:,} (rank {rank*100:.1f}%)")
print(f"unweighted median ${statistics.median(full_nets):,.0f} (cross-check)")
