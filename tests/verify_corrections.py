"""Corrections stay corrected: no retracted figure leaks back in.

tests/corrections.json catalogs every restatement logged in the version
history (the site's history block and the report's version-history
pages), as {old, new, scope, note} entries. For each entry this script
asserts:

  1. the correction really is logged: its history_evidence strings
     appear in a version-history region;
  2. every old token is ABSENT from the site and from the report text
     outside the version-history regions (an occurrence is allowed only
     within an entry's allow_context window, for the report's one
     in-body mention that labels itself corrected);
  3. at least one new token is PRESENT outside history in each artifact
     the entry's scope names (site, report, or both).

History regions: for the site, the downloads section's details element
holding the version links; for the report, the text sliced from the
"Version history" heading to the Sources heading that follows the
corrections policy. Numeric tokens match with digit boundaries so an
old figure never trips on being a substring of a legitimate number
(248 must not match $248,611); word tokens match with letter boundaries.

Run:  python tests/verify_corrections.py
Needs: pip install pypdfium2
Exits nonzero if any check fails.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG = Path(__file__).resolve().parent / "corrections.json"

ok, bad = [], []
def chk(cond, label): (ok if cond else bad).append(label)


def squash(text):
    return re.sub(r"\s+", " ", text)


def token_re(tok):
    """Boundary-aware pattern: digits never extend into a larger number,
    words never sit inside a longer word."""
    pat = re.escape(tok)
    if any(ch.isdigit() for ch in tok):
        return re.compile(r"(?<![\d,.])" + pat + r"(?!\d)(?!\.\d)(?!,\d)")
    return re.compile(r"(?<![A-Za-z])" + pat + r"(?![A-Za-z])", re.IGNORECASE)


def site_texts():
    html = (REPO / "index.html").read_text()
    start = html.index('<details class="more"><summary>Version history')
    end = html.index("</details>", start) + len("</details>")
    return squash(html[:start] + " " + html[end:]), squash(html[start:end])


def report_texts():
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(REPO / "Saving_North_Middletown_Elementary.pdf"))
    full = "\n".join(pg.get_textpage().get_text_range() for pg in doc)
    start = full.index("Version history. Every version stays public")
    cp = full.index("Corrections policy:", start)
    end = cp + re.search(r"[\r\n]Sources\s*[\r\n]", full[cp:]).start()
    return squash(full[:start] + " " + full[end:]), squash(full[start:end])


def main():
    entries = json.loads(CATALOG.read_text())
    site_body, site_hist = site_texts()
    report_body, report_hist = report_texts()
    history = site_hist + " " + report_hist
    bodies = {"site": site_body, "report": report_body}

    chk(len(site_hist) > 1000 and len(report_hist) > 5000,
        "history regions located on the site and in the report")
    chk(len(entries) >= 12, f"corrections catalog holds {len(entries)} entries")

    for e in entries:
        eid, scope = e["id"], e["scope"]
        arts = ["site", "report"] if scope == "both" else [scope]

        # 1. the correction is logged in a version-history region
        missing_ev = [ev for ev in e.get("history_evidence", [])
                      if ev not in history]
        chk(not missing_ev,
            f"{eid}: logged in the version history"
            if not missing_ev else f"{eid}: history evidence missing: {missing_ev}")

        # 2. old tokens absent everywhere outside history (both artifacts,
        #    whatever the scope: a retracted figure is stale anywhere)
        leaks = []
        for name, body in bodies.items():
            for tok in e["old"]:
                for m in token_re(tok).finditer(body):
                    window = body[max(0, m.start() - 400):m.end() + 400]
                    if any(a in window for a in e.get("allow_context", [])):
                        continue
                    snippet = body[max(0, m.start() - 60):m.end() + 60]
                    leaks.append(f"{name}: {tok!r} at ...{snippet}...")
        chk(not leaks,
            f"{eid}: old token(s) absent outside history"
            if not leaks else f"{eid}: retracted token leaked:\n    "
            + "\n    ".join(leaks))

        # 3. a new token present outside history in each scoped artifact
        for name in arts:
            hit = any(token_re(tok).search(bodies[name]) for tok in e["new"])
            chk(hit, f"{eid}: corrected figure present on the {name}"
                if hit else f"{eid}: no new token {e['new']} on the {name}")

    print(f"PASS {len(ok)}")
    print(f"FAIL {len(bad)}")
    for b in bad:
        print("  -", b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
