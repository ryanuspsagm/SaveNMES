"""Browser tests for index.html: calculators, charts, toggles, links, mobile.

Run:  python tests/test_site.py
Needs: pip install playwright, then `playwright install chromium` (or set
CHROMIUM_PATH to an existing Chromium binary). Chart.js is vendored in
tests/vendor so the tests run without internet access.
Exits nonzero if any check fails.
"""
import os
import re
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[1]
VENDOR = REPO / "tests" / "vendor" / "chart.umd.js"

issues, passed = [], []
def ok(name): passed.append(name)
def bad(name): issues.append(name)


def build_preview() -> str:
    html = (REPO / "index.html").read_text()
    if VENDOR.exists():
        html = html.replace(
            "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js",
            VENDOR.as_uri())
    tmp = Path(tempfile.mkdtemp()) / "preview.html"
    tmp.write_text(html)
    # local images resolve relative to the temp file; link them in
    for asset in re.findall(r'(?:src|href)="([^"#][^":]*?)"', html):
        if not asset.startswith(("http", "mailto", "tel", "file:")):
            src = REPO / asset
            if src.exists():
                (tmp.parent / asset).parent.mkdir(parents=True, exist_ok=True)
                (tmp.parent / asset).write_bytes(src.read_bytes())
    return tmp.as_uri()


def main():
    url = build_preview()
    with sync_playwright() as pw:
        kw = {"args": ["--no-sandbox"]}
        if os.environ.get("CHROMIUM_PATH"):
            kw["executable_path"] = os.environ["CHROMIUM_PATH"]
        b = pw.chromium.launch(**kw)
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(1200)

        if errors: bad(f"console/page errors: {errors}")
        else: ok("no JS console or page errors")

        n = pg.evaluate("Object.keys(Chart.instances).length")
        if n == 6: ok(f"{n} Chart.js charts instantiated")
        else: bad(f"expected 6 charts, got {n}")

        net = pg.text_content("#rNet").strip()
        verdict = pg.text_content("#rVerdict").strip()
        if net == "$361,240" and "13.6%" in verdict: ok("closure defaults $361,240 / 13.6%")
        else: bad(f"closure defaults: {net} / {verdict}")

        pg.fill("#sPos", "6"); pg.dispatch_event("#sPos", "input")
        pg.fill("#sBus", "75000"); pg.dispatch_event("#sBus", "input")
        pg.fill("#sLeav", "0"); pg.dispatch_event("#sLeav", "input")
        if pg.text_content("#rNet").strip() == "$725,000": ok("closure best case $725,000")
        else: bad(f"closure best case: {pg.text_content('#rNet')}")
        pg.fill("#sPos", "2"); pg.dispatch_event("#sPos", "input")
        pg.fill("#sBus", "200000"); pg.dispatch_event("#sBus", "input")
        pg.fill("#sLeav", "30"); pg.dispatch_event("#sLeav", "input")
        if pg.text_content("#rNet").strip() == "$121,220": ok("closure worst case $121,220")
        else: bad(f"closure worst case: {pg.text_content('#rNet')}")

        pg.fill("#sYrs", "1"); pg.dispatch_event("#sYrs", "input")
        lv1 = pg.text_content("#rLevy").strip()
        pg.fill("#sYrs", "3"); pg.dispatch_event("#sYrs", "input")
        lv3 = pg.text_content("#rLevy").strip()
        lverd = pg.text_content("#rLevyVerdict").strip()
        if lv1 == "$385,641" and lv3 == "$1,203,816" and "45.5%" in lverd:
            ok("levy compounder $385,641 year 1, $1,203,816 / 45.5% year 3")
        else: bad(f"levy: {lv1} / {lv3} / {lverd}")

        f1 = pg.text_content("#rFill").strip()
        fv = pg.text_content("#rFillVerdict").strip()
        if f1 == "$140,616" and "174 of 174" in fv and "$14,339" in fv:
            ok("fill planner defaults $140,616, full at $14,339")
        else: bad(f"fill planner defaults: {f1} / {fv}")
        pg.fill("#sSec", "2"); pg.dispatch_event("#sSec", "input")
        if pg.text_content("#rFill").strip() == "$225,616": ok("fill planner high case $225,616")
        else: bad(f"fill planner high: {pg.text_content('#rFill')}")
        pg.fill("#sRez", "40"); pg.dispatch_event("#sRez", "input")
        pg.fill("#sTr", "20"); pg.dispatch_event("#sTr", "input")
        tval = pg.eval_on_selector("#sTr", "e=>e.value")
        expect = 6 * 4626 - 46 * 400 + 2 * 85000
        if tval == "6" and pg.text_content("#rFill").strip() == f"${expect:,}":
            ok("fill planner clamps at the 46 open seats")
        else: bad(f"fill planner clamp: transfers={tval}")
        pg.fill("#sRez", "0"); pg.dispatch_event("#sRez", "input")
        pg.fill("#sTr", "0"); pg.dispatch_event("#sTr", "input")
        if "No students moved" in pg.text_content("#rFillVerdict"):
            ok("fill planner zero-move edge case")
        else: bad("fill planner zero-move verdict missing")

        boxes = pg.query_selector_all(".checkrow input[type=checkbox]")
        if boxes:
            before = pg.evaluate("Object.values(Chart.instances).map(c=>c.data.datasets.length).join(',')")
            boxes[0].click(); pg.wait_for_timeout(300)
            after = pg.evaluate("Object.values(Chart.instances).map(c=>c.data.datasets.length).join(',')")
            if before != after: ok("score toggles update chart datasets")
            else: bad("score toggle changed nothing")
        else: bad("no score toggle checkboxes found")

        kk = pg.evaluate("""() => {
            const d=[...document.querySelectorAll('#questions details')];
            d.forEach(x=>x.open=true);
            return d.length + ':' + d.filter(x=>x.open && x.querySelector('p').textContent.length>20).length
        }""")
        total, opened = kk.split(":")
        if total == opened == "10": ok("all 10 question accordions open with content")
        else: bad(f"accordions {opened}/{total}")

        missing = pg.evaluate("""() => [...document.querySelectorAll('nav a')]
            .map(a=>a.getAttribute('href'))
            .filter(h=>h.startsWith('#') && !document.querySelector(h))""")
        if not missing: ok("all nav anchors resolve")
        else: bad(f"nav anchors missing: {missing}")

        pg.set_viewport_size({"width": 390, "height": 844})
        pg.wait_for_timeout(400)
        overflow = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        if overflow <= 1: ok("no horizontal overflow at 390px")
        else: bad(f"mobile overflow {overflow}px")
        b.close()

    print(f"PASS: {len(passed)}")
    for p in passed: print("  +", p)
    print(f"FAIL: {len(issues)}")
    for i in issues: print("  -", i)
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
