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
        if n == 8: ok(f"{n} Chart.js charts instantiated")
        else: bad(f"expected 8 charts, got {n}")

        net = pg.text_content("#rNet").strip()
        verdict = pg.text_content("#rVerdict").strip()
        if net == "$69,071" and "2.6%" in verdict and "reserves" in verdict:
            ok("closure v3.9 central default $69,071 / 2.6% deficit + drawdown framing")
        else: bad(f"closure defaults: {net} / {verdict}")
        rank = pg.text_content("#rRank").strip()
        if "2,916 scenarios" in rank and "%" in rank and "$21,571" in rank:
            ok("live grid-rank readout present with median and range context")
        else: bad(f"grid-rank readout: {rank}")

        pg.fill("#sFix", "2"); pg.dispatch_event("#sFix", "input")
        pg.fill("#sPos", "5"); pg.dispatch_event("#sPos", "input")
        pg.fill("#sCost", "75000"); pg.dispatch_event("#sCost", "input")
        pg.fill("#sBus", "100000"); pg.dispatch_event("#sBus", "input")
        pg.fill("#sLeav", "0"); pg.dispatch_event("#sLeav", "input")
        pg.fill("#sCap", "0"); pg.dispatch_event("#sCap", "input")
        pg.fill("#sEro", "0"); pg.dispatch_event("#sEro", "input")
        if pg.text_content("#rNet").strip() == "$551,928": ok("closure v3.9 favorable tail $551,928 = grid max")
        else: bad(f"closure best case: {pg.text_content('#rNet')}")
        pg.fill("#sFix", "0"); pg.dispatch_event("#sFix", "input")
        pg.fill("#sPos", "2"); pg.dispatch_event("#sPos", "input")
        pg.fill("#sCost", "50000"); pg.dispatch_event("#sCost", "input")
        pg.fill("#sBus", "250000"); pg.dispatch_event("#sBus", "input")
        pg.fill("#sLeav", "30"); pg.dispatch_event("#sLeav", "input")
        pg.fill("#sCap", "231000"); pg.dispatch_event("#sCap", "input")
        pg.fill("#sEro", "95000"); pg.dispatch_event("#sEro", "input")
        if pg.text_content("#rNet").strip() == "-$556,006" and "LOSES" in pg.text_content("#rVerdict"):
            ok("closure v3.9 unfavorable tail -$556,006 = grid min (calculator spans the whole grid)")
        else: bad(f"closure worst case: {pg.text_content('#rNet')} / {pg.text_content('#rVerdict')[:60]}")

        pg.fill("#sYrs", "1"); pg.dispatch_event("#sYrs", "input")
        lv1 = pg.text_content("#rLevy").strip()
        pg.fill("#sYrs", "3"); pg.dispatch_event("#sYrs", "input")
        lv3 = pg.text_content("#rLevy").strip()
        lverd = pg.text_content("#rLevyVerdict").strip()
        if lv1 == "$313,162" and lv3 == "$977,568" and "37%" in lverd and "drawdown" in lverd:
            ok("levy compounder $313,162 year 1, $977,568 / 37% deficit / drawdown year 3 (GF base)")
        else: bad(f"levy: {lv1} / {lv3} / {lverd}")

        f1 = pg.text_content("#rFill").strip()
        fv = pg.text_content("#rFillVerdict").strip()
        if f1 == "$55,616" and "174 of 174" in fv and "$14,827" in fv:
            ok("fill planner defaults $55,616 (v3.8 section debit), full at $14,827")
        else: bad(f"fill planner defaults: {f1} / {fv}")
        pg.fill("#sSec", "2"); pg.dispatch_event("#sSec", "input")
        if pg.text_content("#rFill").strip() == "$115,616": ok("fill planner high case $115,616 (2 avoided, 1 added)")
        else: bad(f"fill planner high: {pg.text_content('#rFill')}")
        pg.fill("#sAdd", "2"); pg.dispatch_event("#sAdd", "input")
        pg.fill("#sSec", "0"); pg.dispatch_event("#sSec", "input")
        worst = 16 * 4626 - 46 * 400 - 2 * 60000
        if pg.text_content("#rFill").strip() == f"-${abs(worst):,}":
            ok(f"fill planner worst corner -${abs(worst):,} (2 added, 0 avoided)")
        else: bad(f"fill planner worst corner: {pg.text_content('#rFill')}")
        pg.fill("#sAdd", "1"); pg.dispatch_event("#sAdd", "input")
        pg.fill("#sSec", "2"); pg.dispatch_event("#sSec", "input")
        pg.fill("#sRez", "40"); pg.dispatch_event("#sRez", "input")
        pg.fill("#sTr", "20"); pg.dispatch_event("#sTr", "input")
        tval = pg.eval_on_selector("#sTr", "e=>e.value")
        expect = 6 * 4626 - 46 * 400 + 2 * 60000 - 1 * 60000
        if tval == "6" and pg.text_content("#rFill").strip() == f"${expect:,}":
            ok("fill planner clamps at the 46 open seats")
        else: bad(f"fill planner clamp: transfers={tval}")
        pg.fill("#sRez", "0"); pg.dispatch_event("#sRez", "input")
        pg.fill("#sTr", "0"); pg.dispatch_event("#sTr", "input")
        pg.fill("#sRet", "0"); pg.dispatch_event("#sRet", "input")
        if "No students moved" in pg.text_content("#rFillVerdict"):
            ok("fill planner zero-move edge case")
        else: bad("fill planner zero-move verdict missing")
        # returning homeschool/private students: new money at the same base
        pg.fill("#sSec", "1"); pg.dispatch_event("#sSec", "input")
        pg.fill("#sRez", "20"); pg.dispatch_event("#sRez", "input")
        pg.fill("#sTr", "10"); pg.dispatch_event("#sTr", "input")
        pg.fill("#sRet", "16"); pg.dispatch_event("#sRet", "input")
        expect_ret = (10 + 16) * 4626 - 46 * 400 + 1 * 60000 - 1 * 60000
        if pg.text_content("#rFill").strip() == f"${expect_ret:,}" and "174 of 174" in pg.text_content("#rFillVerdict"):
            ok(f"fill planner returning-students case ${expect_ret:,}")
        else: bad(f"fill planner returns: {pg.text_content('#rFill')}")
        pg.fill("#sRez", "30"); pg.dispatch_event("#sRez", "input")
        pg.fill("#sTr", "16"); pg.dispatch_event("#sTr", "input")
        pg.fill("#sRet", "46"); pg.dispatch_event("#sRet", "input")
        if pg.eval_on_selector("#sRet", "e=>e.value") == "0":
            ok("fill planner caps returns at the 46 open seats")
        else: bad(f"fill planner return clamp: {pg.eval_on_selector('#sRet', 'e=>e.value')}")

        boxes = pg.query_selector_all(".checkrow input[type=checkbox]")
        if boxes:
            before = pg.evaluate("Object.values(Chart.instances).map(c=>c.data.datasets.length).join(',')")
            boxes[0].click(); pg.wait_for_timeout(300)
            after = pg.evaluate("Object.values(Chart.instances).map(c=>c.data.datasets.length).join(',')")
            if before != after: ok("score toggles update chart datasets")
            else: bad("score toggle changed nothing")
        else: bad("no score toggle checkboxes found")

        gone = pg.evaluate("['tldr','questions','roadahead'].filter(i=>document.getElementById(i)).length")
        if gone == 0: ok("off-layout sections absent (v4 simplified layout)")
        else: bad(f"{gone} off-layout sections still present")

        missing = pg.evaluate("""() => [...document.querySelectorAll('nav a')]
            .map(a=>a.getAttribute('href'))
            .filter(h=>h.startsWith('#') && !document.querySelector(h))""")
        if not missing: ok("all nav anchors resolve")
        else: bad(f"nav anchors missing: {missing}")

        pg.set_viewport_size({"width": 390, "height": 844})
        overflow = None
        for _ in range(10):
            pg.wait_for_timeout(250)
            overflow = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if overflow <= 1: break
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
