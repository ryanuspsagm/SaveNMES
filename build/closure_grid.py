"""Enumerate the v3.9 two-tailed closure grid and print its statistics.

The seven levers and their values (every one sourced in the report and the
Closure_Model tab):
  positions eliminated:  2, 3, 4, 5            (four values)
  GF cost per position:  $50,000 / $60,000 / $75,000
  fixed cost avoided:    $58,774 (staff reassigned, utilities only)
                         $227,831 (mothballed: admin + custodial + plant)
                         $276,928 (sold: the above plus library and media)
  added busing:          $100,000 / $137,500 / $250,000
  families leaving:      0 / 10 / 30 students at the $4,626 SEEK base
  capacity debt service: $0 / $115,000 / $231,000
  assessment erosion:    $0 / $40,000 / $95,000

4 x 3 x 3 x 3 x 3 x 3 x 3 = 2,916 combinations, equal weights.
net = fixed + positions x cost - busing - leavers x 4626 - capdebt - erosion

v3.9 rebuilt this lever on the district's own FY2026 working budget,
location 090, General Fund, excluding state-paid on-behalf:
  school administration (program 077)      $131,724
  custodial (program 087)                   $37,333
  plant, utilities, sanitation, water (987) $58,774
  library and media (program 059)           $49,097
The three published cases are the three decisions a district can actually
make with those lines. v3.8 carried only two, $230,000 and $290,000, both
estimates and both assuming every fixed position is eliminated rather than
reassigned. Adding the reassignment case is what moves the median.

Run:  python build/closure_grid.py
Asserts the published statistics: median +$21,571; 25th/75th percentiles
-$104,726 / +$146,274; 1,314 of 2,916 (45.06 percent, published as 45)
negative; range -$556,006 to +$551,928.
"""
SEEK = 4626

# Measured fixed lines, FY2026 working budget, location 090, General Fund
ADMIN, CUSTODIAL, PLANT, LIBRARY = 131724, 37333, 58774, 49097
REDEPLOYED = PLANT                                  # 58,774
MOTHBALLED = ADMIN + CUSTODIAL + PLANT              # 227,831
SOLD = MOTHBALLED + LIBRARY                         # 276,928

nets = sorted(
    f + p * c - b - l * SEEK - d - e
    for p in (2, 3, 4, 5)
    for c in (50000, 60000, 75000)
    for f in (REDEPLOYED, MOTHBALLED, SOLD)
    for b in (100000, 137500, 250000)
    for l in (0, 10, 30)
    for d in (0, 115000, 231000)
    for e in (0, 40000, 95000)
)
n = len(nets)


def pctl(p):
    """Percentile as nets[int(p/100*n)], the convention used throughout the
    published statistics."""
    return nets[min(n - 1, int(p / 100 * n))]


median = pctl(50)
neg = sum(1 for x in nets if x < 0)

print(f"combinations: {n}")
print(f"fixed lever: {REDEPLOYED:,} / {MOTHBALLED:,} / {SOLD:,}")
print(f"range: {nets[0]:+,} to {nets[-1]:+,}")
print(f"median: {median:+,.0f}")
print(f"P25: {pctl(25):+,}")
print(f"P75: {pctl(75):+,}")
print(f"negative: {neg}/{n} = {neg / n * 100:.2f}%")

assert (REDEPLOYED, MOTHBALLED, SOLD) == (58774, 227831, 276928)
assert n == 2916
assert nets[0] == -556006 and nets[-1] == 551928
assert median == 21571
assert pctl(25) == -104726 and pctl(75) == 146274
assert neg == 1314  # 1314/2916 = 45.06 percent, published as "45 percent"
print("all published statistics reproduced")
