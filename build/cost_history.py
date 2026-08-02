#!/usr/bin/env python3
"""Cost-per-student history for the chart on the site (chartHist).

Reads the archived state spending-per-student files in build/ and prints,
for each year 2018 to 2025, the all-funds total spending per student for
the three Bourbon County elementary schools and the mean across every
Kentucky school with "elementary" in its name (same method every year).

Sources, all archived in this folder:
  SPENDING_PER_STUDENT_1718.xlsx / SPENDING_PER_STUDENT_1819.xlsx
      KDE school spending files, sheet DATA, column TOTAL_PER_STU_ALLFUNDS
  spending_per_student_2020.csv .. spending_per_student_2023.csv
      KDE files, column "Total Spending per Student - All Fund Sources"
  KYRC24_FT_Spending_per_Student.csv / KYRC25_FT_Spending_per_Student.csv
      Kentucky Report Card financial transparency files, column
      "Total Expenditures Per Student"

The 2012 to 2017 points on the chart come from the older school-level
report era (bourbon_spending_per_student_2011_2017.csv) and are not
recomputed here.
"""
import csv, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))

SCHOOLS = {"NMES": "north middletown", "BCE": "bourbon central", "CRES": "cane ridge"}


def to_num(v):
    if v is None:
        return None
    s = str(v).replace(",", "").replace("$", "").strip()
    if not s or s in {"*", "---", "N/A"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def collect(rows, school_col, dist_col, total_col):
    """rows: iterable of dicts. Returns ({abbr: value}, ky_elem_mean)."""
    out, elem = {}, []
    for r in rows:
        name = (r.get(school_col) or "").strip()
        if not name or "district total" in name.lower():
            continue
        val = to_num(r.get(total_col))
        if val is None:
            continue
        low = name.lower()
        if "elementary" in low:
            elem.append(val)
        if "bourbon" in (r.get(dist_col) or "").lower():
            for abbr, needle in SCHOOLS.items():
                if needle in low:
                    out[abbr] = round(val)
    return out, round(statistics.mean(elem))


def read_xlsx(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True)["DATA"]
    it = ws.iter_rows(values_only=True)
    hdr = [str(h) for h in next(it)]
    return [dict(zip(hdr, row)) for row in it]


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


FILES = [
    (2018, "SPENDING_PER_STUDENT_1718.xlsx", "SCH_NAME", "DIST_NAME", "TOTAL_PER_STU_ALLFUNDS"),
    (2019, "SPENDING_PER_STUDENT_1819.xlsx", "SCH_NAME", "DIST_NAME", "TOTAL_PER_STU_ALLFUNDS"),
    (2020, "spending_per_student_2020.csv", "SCHOOL NAME", "DISTRICT NAME", "Total Spending per Student - All Fund Sources"),
    (2021, "spending_per_student_2021.csv", "SCHOOL NAME", "DISTRICT NAME", "Total Spending per Student - All Fund Sources"),
    (2022, "spending_per_student_2022.csv", "SCHOOL NAME", "DISTRICT NAME", "Total Spending per Student - All Fund Sources"),
    (2023, "spending_per_student_2023.csv", "SCHOOL NAME", "DISTRICT NAME", "Total Spending per Student - All Fund Sources"),
    (2024, "KYRC24_FT_Spending_per_Student.csv", "School Name", "District Name", "Total Expenditures Per Student"),
    (2025, "KYRC25_FT_Spending_per_Student.csv", "School Name", "District Name", "Total Expenditures Per Student"),
]


def main():
    results = {}
    for year, fname, school_col, dist_col, total_col in FILES:
        path = os.path.join(HERE, fname)
        rows = read_xlsx(path) if fname.endswith(".xlsx") else read_csv(path)
        vals, ky = collect(rows, school_col, dist_col, total_col)
        vals["KYELEM"] = ky
        results[year] = vals
        print(year, {k: vals[k] for k in ("NMES", "BCE", "CRES", "KYELEM")})
    return results


if __name__ == "__main__":
    main()
