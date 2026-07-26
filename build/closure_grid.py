"""Enumerate the v3 two-tailed closure grid and print its statistics.

The seven levers and their values (every one sourced in the report and the
Closure_Model tab):
  positions eliminated:  2, 3, 4, 5            (four values)
  GF cost per position:  $50,000 / $60,000 / $75,000
  fixed cost avoided:    $230,000 (mothballed) / $290,000 (sold)  (two values)
  added busing:          $100,000 / $137,500 / $250,000
  families leaving:      0 / 10 / 30 students at the $4,626 SEEK base
  capacity debt service: $0 / $115,000 / $231,000
  assessment erosion:    $0 / $40,000 / $95,000

4 x 3 x 2 x 3 x 3 x 3 x 3 = 1,944 combinations, equal weights.
net = fixed + positions x cost - busing - leavers x 4626 - capdebt - erosion

Run:  python build/closure_grid.py
Asserts the published statistics: median +$91,240; 25th/75th percentiles
-$17,500 / +$200,000; 559 of 1,944 (28.8 percent, published as 29) negative;
range -$384,780 to +$565,000.
"""
from itertools import product

SEEK = 4626
nets = sorted(
    f + p * c - b - l * SEEK - d - e
    for p in (2, 3, 4, 5)
    for c in (50000, 60000, 75000)
    for f in (230000, 290000)
    for b in (100000, 137500, 250000)
    for l in (0, 10, 30)
    for d in (0, 115000, 231000)
    for e in (0, 40000, 95000)
)
n = len(nets)


def pctl(p):
    """Percentile as nets[int(p/100*n)], the convention used throughout the
    published statistics (0.25*1944 and 0.75*1944 are exact integers)."""
    return nets[min(n - 1, int(p / 100 * n))]


median = pctl(50)
neg = sum(1 for x in nets if x < 0)

print(f"combinations: {n}")
print(f"range: {nets[0]:+,} to {nets[-1]:+,}")
print(f"median: {median:+,.0f}")
print(f"P25: {pctl(25):+,}")
print(f"P75: {pctl(75):+,}")
print(f"negative: {neg}/{n} = {neg / n * 100:.2f}%")

assert n == 1944
assert nets[0] == -384780 and nets[-1] == 565000
assert median == 91240
assert pctl(25) == -17500 and pctl(75) == 200000
assert neg == 559  # 559/1944 = 28.76 percent, published as "29 percent"
print("all published statistics reproduced")
