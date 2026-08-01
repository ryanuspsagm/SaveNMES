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
        # v4.2 review: sections collapse to key points; open everything for testing
        pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
        pg.wait_for_timeout(600)

        if errors: bad(f"console/page errors: {errors}")
        else: ok("no JS console or page errors")

        n = pg.evaluate("Object.keys(Chart.instances).length")
        if n == 7: ok(f"{n} Chart.js charts instantiated")
        else: bad(f"expected 7 charts, got {n}")
        nmore = pg.evaluate("document.querySelectorAll('details.more').length")
        if nmore >= 10: ok(f"{nmore} sections collapse to key points with More detail expanders")
        else: bad(f"only {nmore} section expanders found")
        strip = pg.query_selector(".range-bar")
        labs = pg.text_content(".range-labs") if pg.query_selector(".range-labs") else ""
        if strip and "loses $591,545" in labs and "saves $488,631" in labs and "loses $21,971" in labs:
            ok("nontechnical range strip shows worst / middle / best in plain words")
        else: bad(f"range strip missing or labels wrong: {labs[:80]}")

        # --- Closure calculator: v4.2 grid defaults ---
        net = pg.text_content("#rNet").strip()
        verdict = pg.text_content("#rVerdict").strip()
        if net == "$54,539" and "2.1%" in verdict:
            ok("closure v4.2 central default $54,539 / 2.1% of the deficit")
        else: bad(f"closure defaults: {net} / {verdict}")
        rank = pg.text_content("#rRank").strip()
        if "5,832 scenarios" in rank and "66%" in rank and "-$21,971" in rank:
            ok("live grid-rank readout: 66% at defaults, median -$21,971")
        else: bad(f"grid-rank readout: {rank}")

        # ceiling: their fullest case
        pg.fill("#sCap", "2"); pg.dispatch_event("#sCap", "input")
        pg.fill("#sFix", "2"); pg.dispatch_event("#sFix", "input")
        pg.fill("#sTea", "3"); pg.dispatch_event("#sTea", "input")
        pg.fill("#sLeav", "0"); pg.dispatch_event("#sLeav", "input")
        pg.fill("#sProp", "0"); pg.dispatch_event("#sProp", "input")
        pg.fill("#sBus", "20000"); pg.dispatch_event("#sBus", "input")
        if pg.text_content("#rNet").strip() == "$488,631":
            ok("closure ceiling $488,631 = grid max")
        else: bad(f"closure best case: {pg.text_content('#rNet')}")

        # floor: 50% leakage corner
        pg.fill("#sCap", "0"); pg.dispatch_event("#sCap", "input")
        pg.fill("#sFix", "0"); pg.dispatch_event("#sFix", "input")
        pg.fill("#sTea", "0"); pg.dispatch_event("#sTea", "input")
        pg.fill("#sLeav", "50"); pg.dispatch_event("#sLeav", "input")
        pg.fill("#sAdd", "1000"); pg.dispatch_event("#sAdd", "input")
        pg.fill("#sProp", "95000"); pg.dispatch_event("#sProp", "input")
        pg.fill("#sBus", "190000"); pg.dispatch_event("#sBus", "input")
        if pg.text_content("#rNet").strip() == "-$591,545" and "LOSES" in pg.text_content("#rVerdict"):
            ok("closure floor -$591,545 = grid min (calculator spans the whole grid)")
        else: bad(f"closure worst case: {pg.text_content('#rNet')} / {pg.text_content('#rVerdict')[:60]}")

        # --- Growth calculator ---
        gro = pg.text_content("#rGro").strip()
        gverd = pg.text_content("#rGroVerdict").strip()
        if gro == "$73,000" and "50 added students" in gverd and "2 new teachers" in gverd:
            ok("growth default $73,000 at target 160 (2 teachers charged, no absorption credit)")
        else: bad(f"growth defaults: {gro} / {gverd}")
        pg.fill("#sGro", "120"); pg.dispatch_event("#sGro", "input")
        pg.fill("#sSp", "2"); pg.dispatch_event("#sSp", "input")
        pg.fill("#sGb", "1000"); pg.dispatch_event("#sGb", "input")
        pg.fill("#sCps", "1000"); pg.dispatch_event("#sCps", "input")
        if pg.text_content("#rGro").strip() == "$26,260":
            ok("growth grid floor $26,260 (10 students at max costs)")
        else: bad(f"growth floor: {pg.text_content('#rGro')}")
        pg.fill("#sGro", "110"); pg.dispatch_event("#sGro", "input")
        if "No new students" in pg.text_content("#rGroVerdict"):
            ok("growth zero-gain edge case")
        else: bad("growth zero-gain verdict missing")

        # --- 2018-rate restore slider (the only revenue lever on the site) ---
        gone4 = pg.evaluate("['sYrs','rLevy','rLevyVerdict'].filter(i=>document.getElementById(i)).length")
        if gone4 == 0: ok("4 percent compounder removed from the site")
        else: bad(f"{gone4} 4-percent-option elements still present")
        r18 = pg.text_content("#rR18").strip()
        if r18 == "$1,699,479":
            ok("2018 restore default $1,699,479 at 100% (ties to the $191K/cent yield)")
        else: bad(f"2018 restore default: {r18}")
        pg.fill("#sR18", "50"); pg.dispatch_event("#sR18", "input")
        if pg.text_content("#rR18").strip() == "$849,740":
            ok("2018 restore scales: $849,740 at 50%")
        else: bad(f"2018 restore at 50%: {pg.text_content('#rR18')}")

        # --- Fill planner (unchanged math, simplified verdict) ---
        f1 = pg.text_content("#rFill").strip()
        fv = pg.text_content("#rFillVerdict").strip()
        if f1 == "$55,616" and "174 of the 198" in fv:
            ok("fill planner defaults $55,616; at the 174 rating within the 2013-rated 198")
        else: bad(f"fill planner defaults: {f1} / {fv}")
        pg.fill("#sSec", "2"); pg.dispatch_event("#sSec", "input")
        if pg.text_content("#rFill").strip() == "$115,616": ok("fill planner high case $115,616 (2 avoided, 1 added)")
        else: bad(f"fill planner high: {pg.text_content('#rFill')}")
        pg.fill("#sAdd2", "2"); pg.dispatch_event("#sAdd2", "input")
        pg.fill("#sSec", "0"); pg.dispatch_event("#sSec", "input")
        worst = 16 * 4626 - 46 * 400 - 2 * 60000
        if pg.text_content("#rFill").strip() == f"-${abs(worst):,}":
            ok(f"fill planner worst corner -${abs(worst):,} (2 added, 0 avoided)")
        else: bad(f"fill planner worst corner: {pg.text_content('#rFill')}")
        pg.fill("#sAdd2", "1"); pg.dispatch_event("#sAdd2", "input")
        pg.fill("#sSec", "2"); pg.dispatch_event("#sSec", "input")
        pg.fill("#sRez", "40"); pg.dispatch_event("#sRez", "input")
        pg.fill("#sTr", "40"); pg.dispatch_event("#sTr", "input")
        tval = pg.eval_on_selector("#sTr", "e=>e.value")
        expect = 30 * 4626 - 70 * 400 + 2 * 60000 - 1 * 60000
        if tval == "30" and pg.text_content("#rFill").strip() == f"${expect:,}":
            ok("fill planner clamps at the 70 seats up to the 2013-rated 198")
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
        if pg.text_content("#rFill").strip() == f"${expect_ret:,}" and "174 of the 198" in pg.text_content("#rFillVerdict"):
            ok(f"fill planner returning-students case ${expect_ret:,}")
        else: bad(f"fill planner returns: {pg.text_content('#rFill')}")
        pg.fill("#sRez", "30"); pg.dispatch_event("#sRez", "input")
        pg.fill("#sTr", "16"); pg.dispatch_event("#sTr", "input")
        pg.fill("#sRet", "46"); pg.dispatch_event("#sRet", "input")
        vals = [pg.eval_on_selector(sel, "e=>e.value") for sel in ("#sRet", "#sTr", "#sRez")]
        expect_prio = 46 * 4626 - 70 * 400 + 1 * 60000 - 1 * 60000
        if vals == ["46", "0", "24"] and pg.text_content("#rFill").strip() == f"${expect_prio:,}":
            ok("returning-students slider keeps its value; seats freed from transfers first")
        else: bad(f"fill planner return priority: ret/tr/rez = {vals}, net {pg.text_content('#rFill')}")

        boxes = pg.query_selector_all(".checkrow input[type=checkbox]")
        if boxes:
            before = pg.evaluate("Object.values(Chart.instances).map(c=>c.data.datasets.length).join(',')")
            boxes[0].click(); pg.wait_for_timeout(300)
            after = pg.evaluate("Object.values(Chart.instances).map(c=>c.data.datasets.length).join(',')")
            if before != after: ok("score toggles update chart datasets")
            else: bad("score toggle changed nothing")
        else: bad("no score toggle checkboxes found")

        legacy = pg.evaluate("['alternatives','math','closure','tax','trim'].filter(i=>document.getElementById(i)).length")
        if legacy == 0: ok("legacy v4.1 section ids absent")
        else: bad(f"{legacy} legacy v4.1 section ids still present")

        order = pg.evaluate("""() => ['part1','school','cost','frees','risks','model','part2','money','grow','choice','asks','act','voices','downloads','sources']
            .map(i=>{var e=document.getElementById(i);return e?e.getBoundingClientRect().top+window.scrollY:-1})""")
        if all(v >= 0 for v in order) and order == sorted(order):
            ok("v4.2 section order: Part One (case) then model then Part Two (growth)")
        else: bad(f"section order wrong or missing: {order}")

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
