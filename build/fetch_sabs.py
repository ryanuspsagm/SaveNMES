"""Fetch Bourbon County's official school attendance boundaries from the
federal School Attendance Boundary Survey (SABS, 2015-16 collection).

SABS was collected by the National Center for Education Statistics with the
U.S. Census Bureau; 2015-16 was the last national collection, so treat the
boundaries as that vintage. NCES serves the polygons from a public ArcGIS
REST endpoint; no key or login is required.

Run:  python build/fetch_sabs.py
Writes build/sabs_zones.json. If that file exists, build/make_charts.py
draws the report's zone map (Figure 13) from the official boundaries
instead of the traced approximation, and prints each zone's area so the
Transport_Geo tab's yellow area cells can be replaced.

If this machine cannot reach nces.ed.gov, paste this URL into any browser
and save the response as build/sabs_zones_raw.json, then rerun this script:

https://nces.ed.gov/opengis/rest/services/K12_School_Locations/SABS_1516/MapServer/0/query?where=leaid%3D%272100540%27&outFields=*&outSR=4326&f=geojson
"""
import json
import math
import os
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "sabs_zones_raw.json")
OUT = os.path.join(HERE, "sabs_zones.json")

BASE = ("https://nces.ed.gov/opengis/rest/services/K12_School_Locations/"
        "SABS_1516/MapServer/0/query")
PARAMS = {
    "where": "leaid='2100540'",   # Bourbon County school district
    "outFields": "*",
    "outSR": "4326",
    "f": "geojson",
}


def ring_area_sq_mi(ring):
    """Shoelace area of a lon/lat ring, cos-corrected at the ring's latitude."""
    lat0 = sum(p[1] for p in ring) / len(ring)
    kx = 69.172 * math.cos(math.radians(lat0))   # miles per degree longitude
    ky = 68.972                                  # miles per degree latitude
    s = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        s += (x1 * kx) * (y2 * ky) - (x2 * kx) * (y1 * ky)
    return abs(s) / 2.0


def main():
    if os.path.exists(RAW):
        print(f"using saved response {RAW}")
        data = json.load(open(RAW))
    else:
        url = BASE + "?" + urllib.parse.urlencode(PARAMS)
        print("querying", url)
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                data = json.load(r)
        except Exception as e:
            raise SystemExit(
                f"could not reach nces.ed.gov ({e}).\n"
                f"Open the URL in the docstring in a browser, save the JSON "
                f"as {RAW}, and rerun.")

    feats = data.get("features", [])
    if not feats:
        raise SystemExit("no features returned; check the query")
    out = {"source": "NCES EDGE SABS 2015-16 (leaid 2100540)", "schools": []}
    for f in feats:
        props = f.get("properties", {})
        name = (props.get("schnam") or props.get("SrcName")
                or props.get("NAME") or "unknown")
        geom = f["geometry"]
        rings = (geom["coordinates"] if geom["type"] == "Polygon"
                 else [r for poly in geom["coordinates"] for r in poly])
        outer = [max(rings, key=len)] if geom["type"] == "Polygon" else rings
        area = sum(ring_area_sq_mi([tuple(p) for p in r]) for r in outer)
        out["schools"].append({
            "name": name,
            "ncessch": props.get("ncessch"),
            "area_sq_mi": round(area, 1),
            "rings": outer,
        })
        print(f"{name}: {area:,.1f} sq mi, {sum(len(r) for r in outer)} points")
    json.dump(out, open(OUT, "w"))
    print(f"wrote {OUT}; rerun make_charts.py and compare areas against the "
          f"Transport_Geo tab's yellow cells")


if __name__ == "__main__":
    main()
