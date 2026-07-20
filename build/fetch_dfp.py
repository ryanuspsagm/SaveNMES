"""Fetch the Bourbon County Schools District Facility Plan, current and historical.

The District Facility Plan (DFP) is the document that sets each school's
rated student capacity and its classification (permanent, transitional).
KDE posts only the current plan; the Internet Archive's Wayback Machine
holds earlier versions of the same URL, which is how the historical
capacity record (and any quiet changes to it) can be recovered.

Run from the repo root on a machine with normal internet access:

    python build/fetch_dfp.py

Outputs, written next to this script:
    dfp_current.pdf              the plan as posted today
    dfp_wayback_<stamp>.pdf      one file per distinct archived version
    dfp_manifest.json            what was fetched, from where, with sizes

Then commit and push the outputs; the analysis scripts take it from there.
If a download fails, the same URLs are printed so they can be fetched in a
browser and saved under the same names.
"""
import hashlib
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (SaveNMES records research; contact ryanuspsagm@gmail.com)"}

DFP_URLS = [
    "https://education.ky.gov/districts/fac/Documents/Bourbon%20Co%20DFP.pdf",
    "https://education.ky.gov/districts/fac/documents/bourbon%20co%20dfp.pdf",
]
CDX = ("https://web.archive.org/cdx/search/cdx?url={target}"
       "&output=json&fl=timestamp,original,digest,length&filter=statuscode:200"
       "&collapse=digest")


def get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read()


def save(name, data):
    path = os.path.join(HERE, name)
    with open(path, "wb") as f:
        f.write(data)
    print(f"  saved {name} ({len(data):,} bytes)")
    return {"file": name, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()[:16]}


def main():
    manifest = {"current": None, "wayback": [], "errors": []}

    print("1. Current DFP from KDE")
    for url in DFP_URLS:
        try:
            data = get(url)
            if data[:4] == b"%PDF":
                rec = save("dfp_current.pdf", data)
                rec["url"] = url
                manifest["current"] = rec
                break
            manifest["errors"].append(f"not a PDF: {url}")
        except Exception as e:
            manifest["errors"].append(f"{url}: {e}")
    if not manifest["current"]:
        print("  FAILED. Open this in a browser and save as build/dfp_current.pdf:")
        print(f"  {DFP_URLS[0]}")

    print("2. Historical versions from the Wayback Machine")
    seen = set()
    for target in ["education.ky.gov/districts/fac/Documents/Bourbon Co DFP.pdf",
                   "education.ky.gov/districts/fac/documents/bourbon co dfp.pdf"]:
        try:
            rows = json.loads(get(CDX.format(target=urllib.parse.quote(target))))
        except Exception as e:
            manifest["errors"].append(f"CDX {target}: {e}")
            continue
        for ts, original, digest, _len in rows[1:]:
            if digest in seen:
                continue
            seen.add(digest)
            snap = f"https://web.archive.org/web/{ts}id_/{original}"
            try:
                data = get(snap, timeout=120)
                if data[:4] != b"%PDF":
                    manifest["errors"].append(f"not a PDF: {snap}")
                    continue
                rec = save(f"dfp_wayback_{ts}.pdf", data)
                rec["url"] = snap
                rec["captured"] = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"
                manifest["wayback"].append(rec)
            except Exception as e:
                manifest["errors"].append(f"{snap}: {e}")
    if not manifest["wayback"]:
        print("  No archived copies retrieved. Browse the history here and save any")
        print("  versions found as build/dfp_wayback_<YYYYMMDD>.pdf:")
        print("  https://web.archive.org/web/*/education.ky.gov/districts/fac/Documents/Bourbon*")

    with open(os.path.join(HERE, "dfp_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    n = len(manifest["wayback"]) + (1 if manifest["current"] else 0)
    print(f"done: {n} document(s), {len(manifest['errors'])} error(s); see dfp_manifest.json")
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
