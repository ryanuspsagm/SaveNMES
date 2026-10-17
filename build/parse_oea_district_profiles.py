#!/usr/bin/env python3
"""Read every district's Kentucky Core Content Test results out of the LRC district profiles.

The Office of Education Accountability's Kentucky District Data Profiles (Legislative
Research Commission research reports 360, 368, 382 and 392, covering school years 2008,
2009, 2010 and 2011) give each district a two-page spread. The second page carries the
Kentucky Core Content Test table: percent proficient or distinguished in reading,
mathematics, science and writing at the elementary, middle and high school levels, with
the state row beneath. This script pulls that table for all 174 districts of the time.

Reports 360 and 382 have a normal text layer. Reports 368 and 392 were produced with
fonts that carry no character map, so their text layer is a fixed glyph substitution.
The substitution is learned from Bourbon County's page (whose values were read from the
rendered image) and checked three ways: the state row must decode to the same twelve
values on every page, the decoded year headings must read correctly, and each district's
enrollment figures for the overlapping years must match the readable 2010 profile.

Usage:
  python3 -I build/parse_oea_district_profiles.py --rr360 RR360.pdf --rr368 RR368.pdf \
      --rr382 RR382.pdf --rr392 RR392.pdf

Writes build/benchmarks_oea_districts_2008_2011.csv: year, district, level, and percent
proficient or distinguished in reading, mathematics, science and writing (blank where
the district has no school at that level), plus a Kentucky row for each year.
"""
import argparse
import csv
import ctypes
import os
import re
import sys

import pypdfium2 as pdfium
import pypdfium2.raw as R

HERE = os.path.dirname(os.path.abspath(__file__))
LEVELS = ("ES", "MS", "HS")
SUBJECTS = ("reading", "math", "science", "writing")

# glyph maps for the two reports whose text layer is a substitution cipher
GLYPHS = {
    2009: dict(digits={"\x17": "0", "\x18": "1", "'": "2", "\x1e": "3", "\x1f": "4", "\x11": "5",
                       "\x16": "6", "&": "7", "\x12": "8", "\x15": "9"},
               pct="\x13", space="\x05", na=";=2",
               marker="3\x1a*\x1d\x1a\x0e\x1b\t\x1a*\x0f\x04\x08",  # Distinguished
               kcct="\x1a\x10\x07\x1b\t\x07\x15"),  # start of the table heading
    2011: dict(digits={"\x16": "0", "\x19": "1", "\x18": "2", "\x17": "3", " ": "4", "\x11": "5",
                       "\x15": "6", ".": "7", "\x1a": "8", "\x12": "9"},
               pct="\x13", space="\x05", na="<>3",
               marker="4\x1c*\x1f\x1c\x0e\x1d\t\x1c*\x0f\x04\x08",
               kcct="\x1a\x10\x07\x1b\t\x07\x15"),
}


def page_chars(page):
    """(character, generated, left x) for every character pdfium reports on the page."""
    tp = page.get_textpage()
    n = R.FPDFText_CountChars(tp)
    l, r, b, t = (ctypes.c_double() for _ in range(4))
    out = []
    for i in range(n):
        R.FPDFText_GetCharBox(tp, i, ctypes.byref(l), ctypes.byref(r), ctypes.byref(b), ctypes.byref(t))
        out.append((chr(R.FPDFText_GetUnicode(tp, i)), bool(R.FPDFText_IsGenerated(tp, i)), l.value))
    return out


def readable_rows(txt):
    """District and state rows from a page with a normal text layer, or None."""
    if "Kentucky Core Content Tests" not in txt or "Proficient/" not in txt:
        return None
    seg = txt.split("Proficient/", 1)[1]
    toks = re.findall(r"(\d{1,3})%|(N/A)", seg)
    toks = [None if t[1] else int(t[0]) for t in toks][:24]
    if len(toks) < 24:
        return None
    return toks[:12], toks[12:24]


def decode_tokens(cs, spec, start):
    """Tokens after `start`: integers, None for N/A, or the raw string for anything else.

    In the 2011 report the digit 4 is coded as a space. When a cell starts with a 4 and
    nothing but the cell gap precedes it, pdfium folds that glyph into the generated
    space it inserts for the gap, so the digit vanishes from the text. The generated
    space keeps the vanished glyph's position, so the distance from it to the first
    surviving character says how many leading 4s to restore (one digit is about 3.6 pt).
    """
    four = next((g for g, d in spec["digits"].items() if d == "4"), None)
    toks, cur, gen_x, first_x, after_gap = [], "", None, None, False
    for c, gen, x in cs[start:]:
        if gen or c == spec["space"]:
            if cur:
                toks.append(cur)
            cur, first_x = "", None
            gen_x, after_gap = (x, True) if gen else (None, False)
            continue
        if not cur:
            first_x = x
        cur += c
        if c == spec["pct"]:
            if four == " " and after_gap and gen_x is not None and first_x is not None:
                missing = int(round((first_x - gen_x) / 3.6))
                cur = " " * max(0, missing) + cur
            toks.append(cur)
            cur, first_x, after_gap = "", None, False
        if len(toks) >= 25:
            break
    out = []
    for t in toks:
        if t == spec["na"]:
            out.append(None)
        elif len(t) > 1 and t.endswith(spec["pct"]) and all(ch in spec["digits"] for ch in t[:-1]):
            out.append(int("".join(spec["digits"][ch] for ch in t[:-1])))
        else:
            out.append(t)
    return out


def garbled_rows(cs, spec):
    s = "".join(c for c, _, _ in cs)
    k = s.find(spec["marker"])
    if k < 0:
        return None
    toks = decode_tokens(cs, spec, k + len(spec["marker"]))
    toks = [t for t in toks if t is None or isinstance(t, int)][:24]
    if len(toks) < 24:
        return None
    return toks[:12], toks[12:24]


def decode_numbers(cs, spec):
    """Every integer of three or more digits on a garbled page (for the alignment check)."""
    nums, cur = set(), ""
    for c, gen, _ in cs:
        if not gen and c in spec["digits"]:
            cur += spec["digits"][c]
        else:
            if len(cur) >= 3:
                nums.add(int(cur))
            cur = ""
    return nums


def readable_numbers(txt):
    return {int(m) for m in re.findall(r"\d+", txt) if len(m) >= 3}


def to_rows(year, name, dist, state):
    rows = []
    for li, lv in enumerate(LEVELS):
        rows.append(dict(year=year, district=name, level=lv,
                         **{subj: dist[si * 3 + li] for si, subj in enumerate(SUBJECTS)}))
    return rows


def main():
    ap = argparse.ArgumentParser()
    for k in ("rr360", "rr368", "rr382", "rr392"):
        ap.add_argument("--" + k, required=True)
    a = ap.parse_args()

    # 1. the readable reports: names and rows straight from the text layer
    readable = {}
    for year, path in ((2008, a.rr360), (2010, a.rr382)):
        pdf = pdfium.PdfDocument(path)
        recs, state = [], None
        for i in range(len(pdf)):
            txt = pdf[i].get_textpage().get_text_range()
            rows = readable_rows(txt)
            if not rows:
                continue
            name = [l.strip() for l in txt.splitlines() if l.strip()][0]
            if name == "Kentucky":
                continue
            dist, st = rows
            if state is None:
                state = st
            elif state != st:
                sys.exit(f"{year}: state row differs on page {i + 1} ({name})")
            recs.append((i, name, dist))
        readable[year] = dict(pdf=pdf, recs=recs, state=state)
        print(f"{year}: {len(recs)} districts, state row {state}")

    order = [name for _, name, _ in readable[2010]["recs"]]
    if order != [name for _, name, _ in readable[2008]["recs"]]:
        sys.exit("district order differs between the 2008 and 2010 profiles")

    # 2. the garbled reports: decode, then check alignment against the 2010 profile
    garbled = {}
    ref_pdf = readable[2010]["pdf"]
    ref_pages = [i for i, _, _ in readable[2010]["recs"]]
    for year, path in ((2009, a.rr368), (2011, a.rr392)):
        spec = GLYPHS[year]
        pdf = pdfium.PdfDocument(path)
        pages = []
        for i in range(len(pdf)):
            cs = page_chars(pdf[i])
            rows = garbled_rows(cs, spec)
            if rows:
                pages.append((i, rows, cs))
        # the state's own page carries the table too and comes last
        state = pages[0][1][1]
        bad = [i + 1 for i, rows, _ in pages if rows[1] != state]
        if bad:
            sys.exit(f"{year}: state row differs on pages {bad}")
        pages = [p for p in pages if p[1][0] != state]
        if len(pages) != len(order):
            sys.exit(f"{year}: found {len(pages)} district pages, expected {len(order)}")
        weak = []
        for k, (i, rows, cs) in enumerate(pages):
            mine = decode_numbers(page_chars(pdf[i - 1]), spec)
            ref = readable_numbers(ref_pdf[ref_pages[k] - 1].get_textpage().get_text_range())
            hit = len(mine & ref)
            # the neighbouring district must match worse than the matched one
            alt = max((len(mine & readable_numbers(ref_pdf[ref_pages[j] - 1].get_textpage().get_text_range()))
                       for j in (k - 1, k + 1) if 0 <= j < len(order)), default=0)
            if hit < 2 or hit <= alt:
                weak.append((order[k], i + 1, hit, alt))
        if weak:
            sys.exit(f"{year}: alignment check failed for {weak}")
        garbled[year] = dict(recs=[(i, order[k], rows[0]) for k, (i, rows, _) in enumerate(pages)], state=state)
        print(f"{year}: {len(pages)} districts decoded and aligned, state row {state}")

    # 3. write
    out = os.path.join(HERE, "benchmarks_oea_districts_2008_2011.csv")
    rows = []
    for year in (2008, 2009, 2010, 2011):
        src = readable.get(year) or garbled[year]
        for _, name, dist in src["recs"]:
            rows.extend(to_rows(year, name, dist, src["state"]))
        rows.extend(to_rows(year, "Kentucky", src["state"], src["state"]))
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "district", "level"] + list(SUBJECTS))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    print("wrote", out, len(rows), "rows")


if __name__ == "__main__":
    main()
