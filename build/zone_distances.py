"""Compute actual distances from the official NMES attendance zone geometry.

Uses build/sabs_zones.json (official SABS 2015-16 boundaries) and pure
stdlib: a grid sample of the zone's interior, great-circle distances to the
schools, and the one road pair that can be measured exactly (NMES to Paris
on US 460, ten miles) to calibrate a road factor. Writes
build/zone_distances.json, which the report and workbook cite.

Run:  python build/zone_distances.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NMES = (-84.1122, 38.1446)    # North Middletown Elementary, College Street
PARIS = (-84.2529, 38.2098)   # both receiving schools are in Paris
ROAD_US460 = 10.0             # measured road miles, NMES to Paris (US 460)
ROAD_FACTOR = 1.2             # applied elsewhere; the measured pair implies 1.13
GRID_STEP = 0.006             # about 0.4 miles


def gc_miles(a, b):
    lat0 = math.radians((a[1] + b[1]) / 2)
    dx = (a[0] - b[0]) * 69.172 * math.cos(lat0)
    dy = (a[1] - b[1]) * 68.972
    return math.hypot(dx, dy)


def point_in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def main():
    data = json.load(open(os.path.join(HERE, "sabs_zones.json")))
    nm = next(s for s in data["schools"] if "North Middletown" in s["name"])
    ring = [tuple(p) for p in nm["rings"][0]]
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    pts = []
    x = min(xs)
    while x <= max(xs):
        y = min(ys)
        while y <= max(ys):
            if point_in_ring(x, y, ring):
                pts.append((x, y))
            y += GRID_STEP
        x += GRID_STEP
    d_n = [gc_miles(p, NMES) for p in pts]
    d_p = [gc_miles(p, PARIS) for p in pts]
    pair = gc_miles(NMES, PARIS)
    far = max(pts, key=lambda p: gc_miles(p, PARIS))
    out = {
        "source": "computed from build/sabs_zones.json (SABS 2015-16)",
        "sample_points": len(pts),
        "pair_straight_mi": round(pair, 1),
        "pair_road_mi": ROAD_US460,
        "implied_road_factor": round(ROAD_US460 / pair, 2),
        "road_factor_applied": ROAD_FACTOR,
        "mean_added_straight_mi": round(sum(d_p) / len(pts) - sum(d_n) / len(pts), 1),
        "mean_added_road_mi": round((sum(d_p) / len(pts) - sum(d_n) / len(pts)) * ROAD_FACTOR, 1),
        "far_corner_straight_to_paris_mi": round(gc_miles(far, PARIS), 1),
        "far_corner_straight_to_nmes_mi": round(gc_miles(far, NMES), 1),
        "far_corner_road_to_paris_mi": round(gc_miles(far, PARIS) * ROAD_FACTOR, 0),
        "far_corner_road_to_nmes_mi": round(gc_miles(far, NMES) * ROAD_FACTOR, 0),
        "share_of_area_closer_to_nmes": round(
            sum(1 for a, b in zip(d_n, d_p) if a < b) / len(pts), 2),
    }
    json.dump(out, open(os.path.join(HERE, "zone_distances.json"), "w"), indent=1)
    for k, v in out.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
