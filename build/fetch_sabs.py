"""Fetch Bourbon County's official school attendance boundaries from the
federal School Attendance Boundary Survey (SABS, 2015-16 collection).

SABS was collected by the National Center for Education Statistics with the
U.S. Census Bureau; 2015-16 was the last national collection, so treat the
boundaries as that vintage.

Run:  python build/fetch_sabs.py
Writes build/sabs_zones.json. If that file exists, build/make_charts.py
draws the report's zone map (Figure 13) from the official boundaries
instead of the traced approximation, and prints each zone's area so the
Transport_Geo tab's yellow area cells can be replaced.

Three sources are tried in order, so the script works with or without a
reachable NCES server:

1. build/sabs_zones_raw.json, if you saved the REST response yourself.
2. The NCES ArcGIS REST endpoint (no key or login required). As of the last
   run this returns HTTP 500 - the whole /opengis service reports "Could not
   access any server machines" - so the shapefile fallback below is the
   working path.
3. The NCES EDGE bulk download, SABS_1516_SchoolLevels.zip. Get it from
   https://nces.ed.gov/programs/edge/Geographic/SchoolBoundaries and leave it
   in ~/Downloads, or point SABS_ZIP at it; set SABS_DIR instead if you have
   the shapefile already unpacked. The zip's Primary layer is the elementary
   one, which is what the report's map needs.

If you want to try the REST endpoint by hand, this is the query:

https://nces.ed.gov/opengis/rest/services/K12_School_Locations/SABS_1516/MapServer/0/query?where=leaid%3D%272100540%27&outFields=*&outSR=4326&f=geojson
"""
import json
import math
import os
import struct
import urllib.error
import urllib.parse
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "sabs_zones_raw.json")
OUT = os.path.join(HERE, "sabs_zones.json")
CACHE = os.path.join(HERE, "sabs_cache")      # unpacked shapefile, gitignored

LEAID = "2100540"                             # Bourbon County school district
LAYER = "SABS_1516_Primary"                   # elementary boundaries
R_MERC = 6378137.0                            # Web Mercator sphere radius, m

BASE = ("https://nces.ed.gov/opengis/rest/services/K12_School_Locations/"
        "SABS_1516/MapServer/0/query")
PARAMS = {
    "where": f"leaid='{LEAID}'",
    "outFields": "*",
    "outSR": "4326",
    "f": "geojson",
}

MEMBERS = [f"SABS_1516_SchoolLevels/{LAYER}{e}" for e in (".shp", ".shx", ".dbf")]
ZIP_CANDIDATES = [
    os.environ.get("SABS_ZIP"),
    os.path.expanduser("~/Downloads/SABS_1516_SchoolLevels.zip"),
    os.path.join(HERE, "SABS_1516_SchoolLevels.zip"),
]
DIR_CANDIDATES = [
    os.environ.get("SABS_DIR"),
    CACHE,
    HERE,
    os.path.expanduser("~/Downloads/SABS_1516_SchoolLevels"),
]


def ring_area_sq_mi(ring):
    """Shoelace area of a lon/lat ring, cos-corrected at the ring's latitude."""
    lat0 = sum(p[1] for p in ring) / len(ring)
    kx = 69.172 * math.cos(math.radians(lat0))   # miles per degree longitude
    ky = 68.972                                  # miles per degree latitude
    s = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        s += (x1 * kx) * (y2 * ky) - (x2 * kx) * (y1 * ky)
    return abs(s) / 2.0


# --- source 1 and 2: saved response, then the REST endpoint ----------------

def from_geojson(data):
    """Normalize a SABS geojson FeatureCollection into our school records."""
    feats = data.get("features", [])
    if not feats:
        raise SystemExit("no features returned; check the query")
    schools = []
    for f in feats:
        props = f.get("properties", {})
        name = (props.get("schnam") or props.get("SrcName")
                or props.get("NAME") or "unknown")
        geom = f["geometry"]
        rings = (geom["coordinates"] if geom["type"] == "Polygon"
                 else [r for poly in geom["coordinates"] for r in poly])
        outer = [max(rings, key=len)] if geom["type"] == "Polygon" else rings
        schools.append(record(name, props.get("ncessch"), outer))
    return "NCES EDGE SABS 2015-16 REST query (leaid %s)" % LEAID, schools


def fetch_rest():
    url = BASE + "?" + urllib.parse.urlencode(PARAMS)
    print("querying", url)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


# --- source 3: the bulk-download shapefile --------------------------------

def find_shapefile():
    """Return a directory holding LAYER.shp/.shx/.dbf, unpacking the zip once
    into build/sabs_cache/ if that is all we have. None if nothing is found."""
    for d in DIR_CANDIDATES:
        if d and os.path.exists(os.path.join(d, LAYER + ".shp")):
            return d
    for z in ZIP_CANDIDATES:
        if z and os.path.exists(z):
            print(f"unpacking {LAYER} from {z}")
            os.makedirs(CACHE, exist_ok=True)
            with zipfile.ZipFile(z) as zf:
                for m in MEMBERS:
                    with zf.open(m) as src, \
                            open(os.path.join(CACHE, os.path.basename(m)), "wb") as dst:
                        while True:
                            chunk = src.read(1 << 20)
                            if not chunk:
                                break
                            dst.write(chunk)
            return CACHE
    return None


def read_dbf(path):
    """Yield (index, {field: value}) for every record in a dBASE table."""
    with open(path, "rb") as f:
        nrec, hlen, rlen = struct.unpack("<I H H", f.read(32)[4:12])
        fields = []
        while True:
            d = f.read(32)
            if d[:1] in (b"\r", b""):
                break
            fields.append((d[0:11].split(b"\x00")[0].decode("latin-1"), d[16]))
        f.seek(hlen)
        for i in range(nrec):
            rec = f.read(rlen)
            if not rec:
                break
            pos, row = 1, {}                    # pos 0 is the deletion flag
            for name, ln in fields:
                row[name] = rec[pos:pos + ln].decode("latin-1").strip()
                pos += ln
            yield i, row


def read_shx(path):
    """Return [(byte_offset, content_length)] per record, from the .shx index."""
    with open(path, "rb") as f:
        f.seek(24)
        flen = struct.unpack(">I", f.read(4))[0] * 2      # file length in bytes
        f.seek(100)
        out = []
        for _ in range((flen - 100) // 8):
            off, ln = struct.unpack(">I I", f.read(8))
            out.append((off * 2, ln * 2))
        return out


def unproject(x, y):
    """EPSG:3857 metres -> (lon, lat) degrees. The .prj is Web Mercator, but
    the rest of the pipeline expects lon/lat, as outSR=4326 returned."""
    return (x / R_MERC * 180.0 / math.pi,
            math.degrees(2.0 * math.atan(math.exp(y / R_MERC)) - math.pi / 2.0))


def signed_area(ring):
    """Shoelace in projected units; negative means clockwise, i.e. outer ring."""
    return sum(x1 * y2 - x2 * y1
               for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1])) / 2.0


def read_polygon(f, offset, length):
    """Parse one shapefile polygon record into [(signed_area, lon/lat ring)]."""
    f.seek(offset + 8)                          # skip the record header
    buf = f.read(length)
    shptype = struct.unpack("<i", buf[0:4])[0]
    if shptype == 0:
        return []                               # null shape
    if shptype != 5:
        raise SystemExit(f"unexpected shape type {shptype}, expected 5 (Polygon)")
    nparts, npoints = struct.unpack("<i i", buf[36:44])
    parts = list(struct.unpack(f"<{nparts}i", buf[44:44 + 4 * nparts]))
    pbase = 44 + 4 * nparts
    xy = struct.unpack(f"<{2 * npoints}d", buf[pbase:pbase + 16 * npoints])
    rings = []
    for i, start in enumerate(parts):
        end = parts[i + 1] if i + 1 < nparts else npoints
        proj = [(xy[2 * j], xy[2 * j + 1]) for j in range(start, end)]
        rings.append((signed_area(proj), [list(unproject(x, y)) for x, y in proj]))
    return rings


def from_shapefile(src):
    """Pull this district's elementary zones out of the bulk-download layer."""
    base = os.path.join(src, LAYER)
    hits = [(i, r) for i, r in read_dbf(base + ".dbf") if r.get("leaid") == LEAID]
    print(f"matched {len(hits)} {LAYER} records for leaid {LEAID}")
    if not hits:
        raise SystemExit("no records matched; check the leaid")
    index = read_shx(base + ".shx")
    schools = []
    with open(base + ".shp", "rb") as f:
        for i, row in hits:
            rings = read_polygon(f, *index[i])
            outer = [r for a, r in rings if a < 0]   # drop holes (CCW rings)
            if not outer:                            # orientation fallback
                outer = [r for _, r in rings]
            name = row.get("schnam") or row.get("SrcName") or "unknown"
            schools.append(record(name, row.get("ncessch"), outer))
    return ("NCES EDGE SABS 2015-16 bulk download, %s layer (leaid %s)"
            % (LAYER.split("_")[-1], LEAID), schools)


# --- shared ---------------------------------------------------------------

def record(name, ncessch, rings):
    area = sum(ring_area_sq_mi([tuple(p) for p in r]) for r in rings)
    print(f"{name}: {area:,.1f} sq mi, {sum(len(r) for r in rings)} points")
    return {"name": name, "ncessch": ncessch,
            "area_sq_mi": round(area, 1), "rings": rings}


def main():
    if os.path.exists(RAW):
        print(f"using saved response {RAW}")
        source, schools = from_geojson(json.load(open(RAW)))
    else:
        try:
            source, schools = from_geojson(fetch_rest())
        except (urllib.error.URLError, urllib.error.HTTPError, OSError,
                ValueError) as e:
            print(f"could not reach nces.ed.gov ({e}); trying the bulk download")
            src = find_shapefile()
            if not src:
                raise SystemExit(
                    "no local SABS shapefile either. Download "
                    "SABS_1516_SchoolLevels.zip from "
                    "https://nces.ed.gov/programs/edge/Geographic/SchoolBoundaries"
                    " into ~/Downloads (or set SABS_ZIP), then rerun.")
            source, schools = from_shapefile(src)

    json.dump({"source": source, "schools": schools}, open(OUT, "w"))
    print(f"wrote {OUT}; rerun make_charts.py and compare areas against the "
          f"Transport_Geo tab's yellow cells")


if __name__ == "__main__":
    main()
