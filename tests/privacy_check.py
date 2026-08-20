"""Privacy validation for the anonymized school-choice survey.

The survey file build/survey_school_choice_2026_08_anonymized.csv holds
anonymized responses from families in a small town. Nothing resembling
personal information (names, dates of birth, addresses, emails, phone
numbers) may ever appear in it, because the file is published with the
repository.

Two parts:

1. HARD ASSERTIONS (exit nonzero on any failure):
   - the header is exactly the frozen column list, in order;
   - no column name resembles a personal-data field;
   - every cell in every column matches its strict expected shape
     (integer identifiers, plausible bare years, frozen value sets);
   - no cell anywhere matches a name-like, date-like, phone-like,
     or email-like pattern.

2. K-ANONYMITY REPORT (informational only, never fails the suite):
   quasi-identifiers are (kindergarten_year, destination, household
   size). Equivalence-class sizes are computed at child level and at
   household level; every class with k < 3 is printed along with a
   summary k-distribution, so a human can judge re-identification risk.

Run:  python tests/privacy_check.py
Needs: standard library only.
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CSV_PATH = REPO / "build" / "survey_school_choice_2026_08_anonymized.csv"

# ---- frozen schema ---------------------------------------------------------
EXPECTED_COLUMNS = [
    "household",
    "status",
    "child",
    "kindergarten_year",
    "fifth_grade_year",
    "destination",
    "detail_filled",
]

EXPECTED_STATUS = {
    "leaving",
    "staying",
    "staying_confirmed_by_organizer",
    "already_left",
}

EXPECTED_DESTINATIONS = {
    "Montgomery County",
    "Clark County",
    "Homeschool",
    "Private school",
    "Public school in district",
    "Other",
    "Other or undecided",
}

EXPECTED_DETAIL = {"yes", "no"}

YEAR_MIN, YEAR_MAX = 2005, 2045  # plausible bare school years, not dates

# ---- forbidden patterns ----------------------------------------------------
FORBIDDEN_HEADER = re.compile(
    r"name|first|last|surname|address|street|city|zip|email|e-mail|mail|"
    r"phone|tel|cell|mobile|dob|birth|\bdate\b|born|ssn|social|contact|"
    r"parent|guardian|signature",
    re.IGNORECASE,
)

PHONE_LIKE = re.compile(
    r"(\+?\d{1,2}[\s.-])?(\(?\d{3}\)?[\s.-])\d{3}[\s.-]?\d{4}|\d{7,}"
)
DATE_LIKE = re.compile(
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b|"
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}\b",
    re.IGNORECASE,
)
EMAIL_LIKE = re.compile(r"@")
# Two consecutive capitalized words that are not a frozen destination phrase.
NAME_LIKE = re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b")

failures = []


def fail(msg):
    failures.append(msg)


def check_cell_free_text(col, value, row_no):
    """Pattern scan applied to every cell regardless of column checks."""
    if EMAIL_LIKE.search(value):
        fail(f"row {row_no} col {col}: email-like cell {value!r}")
    if PHONE_LIKE.search(value):
        fail(f"row {row_no} col {col}: phone-like cell {value!r}")
    if DATE_LIKE.search(value):
        fail(f"row {row_no} col {col}: date-like cell {value!r}")
    if NAME_LIKE.search(value) and value not in EXPECTED_DESTINATIONS:
        fail(f"row {row_no} col {col}: name-like cell {value!r}")


def main():
    if not CSV_PATH.exists():
        print(f"FAIL: survey file missing: {CSV_PATH}")
        sys.exit(1)

    with open(CSV_PATH, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # 1. header must be exactly the frozen list, in order
    if header != EXPECTED_COLUMNS:
        fail(f"header mismatch: expected {EXPECTED_COLUMNS}, got {header}")

    # 2. no column name resembling personal data
    for col in header:
        if FORBIDDEN_HEADER.search(col):
            fail(f"column name resembles personal data: {col!r}")

    # 3. per-column strict shape checks + global pattern scan
    records = []
    for i, row in enumerate(rows, start=2):  # 1-based lines, header is line 1
        if len(row) != len(EXPECTED_COLUMNS):
            fail(f"row {i}: expected {len(EXPECTED_COLUMNS)} cells, got {len(row)}")
            continue
        rec = dict(zip(EXPECTED_COLUMNS, row))
        records.append(rec)
        for col, value in rec.items():
            check_cell_free_text(col, value, i)
        for col in ("household", "child"):
            if not re.fullmatch(r"\d{1,4}", rec[col]):
                fail(f"row {i}: {col} not a small integer: {rec[col]!r}")
        for col in ("kindergarten_year", "fifth_grade_year"):
            if not re.fullmatch(r"\d{4}", rec[col]) or not (
                YEAR_MIN <= int(rec[col]) <= YEAR_MAX
            ):
                fail(f"row {i}: {col} not a plausible bare year: {rec[col]!r}")
        if rec["status"] not in EXPECTED_STATUS:
            fail(f"row {i}: unexpected status {rec['status']!r}")
        if rec["destination"] not in EXPECTED_DESTINATIONS:
            fail(f"row {i}: unexpected destination {rec['destination']!r}")
        if rec["detail_filled"] not in EXPECTED_DETAIL:
            fail(f"row {i}: unexpected detail_filled {rec['detail_filled']!r}")

    print(f"survey rows checked: {len(rows)} (header + data lines = {len(rows) + 1})")
    if failures:
        print(f"\nFAIL: {len(failures)} privacy assertion(s) failed:")
        for msg in failures:
            print("  -", msg)
        sys.exit(1)
    print("hard assertions: all passed (schema, value sets, pattern scan)")

    # ---- k-anonymity report (informational, never fails) -------------------
    print("\n=== k-anonymity report (informational) ===")
    print("quasi-identifiers: (kindergarten_year, destination, household size)")

    by_household = defaultdict(list)
    for rec in records:
        by_household[rec["household"]].append(rec)
    hh_size = {h: len(v) for h, v in by_household.items()}

    # child level: each child keyed by (its year, its destination, its
    # household's size)
    child_classes = Counter(
        (rec["kindergarten_year"], rec["destination"], hh_size[rec["household"]])
        for rec in records
    )

    # household level: each household keyed by its full quasi-identifier
    # signature (sorted years of all children, sorted distinct destinations,
    # size), the view an attacker who knows a whole family would use
    hh_classes = Counter(
        (
            tuple(sorted(r["kindergarten_year"] for r in v)),
            tuple(sorted({r["destination"] for r in v})),
            len(v),
        )
        for v in by_household.values()
    )

    def report(label, classes, unit):
        print(f"\n-- {label} --")
        print(f"classes: {len(classes)}, {unit}: {sum(classes.values())}")
        small = sorted(
            (k for k, n in classes.items() if n < 3),
            key=lambda k: (classes[k], k),
        )
        if small:
            print(f"classes with k < 3 ({len(small)}):")
            for key in small:
                print(f"  k={classes[key]}  {key}")
        else:
            print("classes with k < 3: none")
        dist = Counter(classes.values())
        print("k-distribution (k: class count):")
        for k in sorted(dist):
            print(f"  k={k}: {dist[k]} class(es)")

    report("child level", child_classes, "children")
    report("household level", hh_classes, "households")

    print(
        "\nnote: the k-anonymity section is a report only; it never fails "
        "the suite and the data is not modified."
    )


if __name__ == "__main__":
    main()
