#!/usr/bin/env python3
"""Chart-content validator.

The numbers build/make_charts.py draws (annotations, spans, bar values) must
equal the numbers the model scripts produce. PDF text extraction cannot see
chart annotations, so without this check a chart can survive a re-base with
stale figures; Figure 7 shipped that way once. This validator recomputes the
model statistics from the single-source constants and asserts the drawing
literals in the make_charts source match them at the precision drawn.
"""
import os
import re
import statistics
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "build"))
from nmes_constants import (SEEK_BASE, SUPPLIES, TEACH, FIXED_POS,
                            CAPTURE_LEGS, BUS_LEGS, ADDON_LEGS, LEAVER_LEGS,
                            POP_TODAY)

SRC = open(os.path.join(REPO, "build", "make_charts.py"), encoding="utf-8").read()

ok, bad = [], []
def chk(cond, label): (ok if cond else bad).append(label)
def lit(text, label): chk(text in SRC, f"{label}: drawn literal {text!r}")

# ---- recompute the closure grid ------------------------------------------
W3 = (1, 2, 1)
pairs = sorted(
    (c + f + t * TEACH - b - l * (SEEK_BASE + ad - SUPPLIES),
     wc * wf * wl * wa * wb)
    for c, wc in zip(CAPTURE_LEGS, W3)
    for f, wf in zip((0, FIXED_POS / 2, FIXED_POS), W3)
    for t in (0, 1, 2, 3)
    for l, wl in zip(LEAVER_LEGS, W3)
    for ad, wa in zip(ADDON_LEGS, W3)
    for b, wb in zip(BUS_LEGS, W3))
nets = [v for v, _ in pairs]
tw = sum(w for _, w in pairs)
def wpct(q):
    c = 0
    for v, w in pairs:
        c += w
        if c >= q * tw:
            return v
med, p25, p75 = wpct(0.50), wpct(0.25), wpct(0.75)
floor, ceil = nets[0], nets[-1]
central = (CAPTURE_LEGS[1] + FIXED_POS / 2 + 2 * TEACH - BUS_LEGS[1]
           - LEAVER_LEGS[1] * (SEEK_BASE + ADDON_LEGS[1] - SUPPLIES))

# ---- Figure 5: closure spectrum -------------------------------------------
k = lambda v: round(v / 1000)
lit(f"a1.axvspan({k(floor)}, 0", "spectrum loss shading starts at the grid floor")
lit(f"a1.axvspan({k(p25)}, {k(p75)}", "spectrum middle-half band")
lit(f"a1.plot([{k(floor)}, {k(ceil)}]", "spectrum range endpoints")
lit(f"median: @${abs(k(med))}K LOST".replace("@", chr(92)), "spectrum median label")
lit(f"@${abs(k(p25))}K to @${abs(k(p75))}K lost".replace("@", chr(92)), "spectrum middle-half label")
lit(f"@${abs(k(floor))}K lost".replace("@", chr(92)), "spectrum worst-case label")
lit(f"@${abs(k(ceil))}K still lost".replace("@", chr(92)), "spectrum best-case label")
lit("every one of the 972", "spectrum all-lose text")

# ---- Figure 5 bottom: tornado ---------------------------------------------
lit(f"a2.axvline({central / 1000:.1f}", "tornado central line")
lit(f"LOSES @${abs(round(central / 1000))}K".replace("@", chr(92)), "tornado central label")
def sweep(delta_lo, delta_hi):
    return (central + delta_lo) / 1000, (central + delta_hi) / 1000
per_leaver = SEEK_BASE + ADDON_LEGS[1] - SUPPLIES
sweeps = {
    "fixed positions": ((0 - FIXED_POS / 2), (FIXED_POS - FIXED_POS / 2)),
    "leavers": (-(LEAVER_LEGS[2] - LEAVER_LEGS[1]) * per_leaver,
                (LEAVER_LEGS[1] - LEAVER_LEGS[0]) * per_leaver),
    "teachers": (-2 * TEACH, TEACH),
    "add-ons": (-LEAVER_LEGS[1] * 500, LEAVER_LEGS[1] * 500),
    "busing": (-(BUS_LEGS[2] - BUS_LEGS[1]), BUS_LEGS[1] - BUS_LEGS[0]),
    "capture": (CAPTURE_LEGS[0] - CAPTURE_LEGS[1], CAPTURE_LEGS[2] - CAPTURE_LEGS[1]),
}
for name, (dlo, dhi) in sweeps.items():
    lo, hi = sweep(dlo, dhi)
    chk(re.search(rf"{lo:.1f}, {hi:.1f}\)", SRC) is not None,
        f"tornado sweep for {name}: ({lo:.1f}, {hi:.1f})")

# ---- Figure 7: the Kentucky record ----------------------------------------
plan_lo, plan_hi = round(800000 / POP_TODAY), round(1000000 / POP_TODAY)
lit(f"axA.axvspan({plan_lo / 1000:.3f}, {plan_hi / 1000:.3f},", "record panel plan band")
lit(f"@${plan_lo:,}".replace("@", chr(92)), "record panel plan low label")
lit(f"@${plan_hi:,}".replace("@", chr(92)), "record panel plan high label")
lit(f", {plan_lo}, {plan_hi},", "record case-panel plan bar")
lit(f"LOSES @${round(-med / POP_TODAY):,} per displaced".replace("@", chr(92) * 2),
    "record panel model-median annotation")
lit(f"loses @${round(-ceil / POP_TODAY)}.".replace("@", chr(92) * 2),
    "record panel model-best annotation")
chk("713, 4414" not in SRC, "the retired positive model bar stays out of the record panel")

# ---- cliff chart -----------------------------------------------------------
m = re.search(r"ada = \[([\d., ]+)\]", SRC)
chk(m is not None, "cliff chart ADA series present")
if m:
    ada = [float(x) for x in m.group(1).split(",")]
    drop = int(ada[0] + 0.5) - int(ada[-1] + 0.5)   # published convention: half-up rounded endpoints
    lit(f"down about {drop}", "cliff chart attendance-drop annotation matches its own series")

print(f"PASS {len(ok)}")
print(f"FAIL {len(bad)}")
for b in bad:
    print("  -", b)
sys.exit(1 if bad else 0)
