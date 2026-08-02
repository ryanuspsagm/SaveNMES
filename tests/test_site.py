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
        if n == 8: ok(f"{n} Chart.js charts instantiated")
        else: bad(f"expected 8 charts, got {n}")
        nmore = pg.evaluate("document.querySelectorAll('details.more').length")
        if nmore >= 10: ok(f"{nmore} sections collapse to key points with More detail expanders")
        else: bad(f"only {nmore} section expanders found")
        strip = pg.query_selector(".range-bar")
        labs = pg.text_content(".range-labs") if pg.query_selector(".range-labs") else ""
        if strip and "loses $591,545" in labs and "saves $488,631" in labs and "loses $17,982" in labs:
            ok("nontechnical range strip shows worst / middle / best in plain words")
        else: bad(f"range strip missing or labels wrong: {labs[:80]}")
        nbars = pg.evaluate("document.querySelectorAll('.range-bar').length")
        niqr = pg.evaluate("document.querySelectorAll('.range-bar .iqr').length")
        glabs = pg.evaluate("document.querySelectorAll('.range-labs')[1] ? document.querySelectorAll('.range-labs')[1].textContent : ''")
        if nbars == 2 and niqr == 2 and "gains $141,780" in glabs and "gains $3,331" in glabs:
            ok("consolidated card: closure and growth bars side by side, IQR band on each")
        else: bad(f"consolidated range card wrong: bars={nbars} iqr={niqr} growth labs: {glabs[:80]}")
        you_c = pg.evaluate("document.getElementById('youClose').style.left")
        you_g = pg.evaluate("document.getElementById('youGrow').style.left")
        if you_c == "26%" and you_g == "50%":
            ok("percentile-scale bars: gold markers at the calculator defaults (26th / 50th)")
        else: bad(f"percentile markers at defaults: close={you_c} grow={you_g}")

        # --- Closure calculator: opens at the median scenario ---
        modelopen = pg.evaluate("document.querySelector('#model details.more').open")
        if modelopen: ok("calculators expanded by default")
        else: bad("calculator details not open by default")
        net = pg.text_content("#rNet").strip()
        rank = pg.text_content("#rRank").strip()
        if net == "-$130,749" and "26th percentile" in rank and "5,832 weighted scenarios" in rank:
            ok("closure default -$130,749 (all staff retained); percentile-only readout: 26th")
        else: bad(f"closure defaults: {net} / {rank}")
        gone_verdict = pg.evaluate("['rVerdict','rBar'].filter(i=>document.getElementById(i)).length")
        note_ok = pg.evaluate("document.body.textContent.includes(\"The default reflects the superintendent's written statement\")")
        if gone_verdict == 0 and note_ok:
            ok("closure verdict text removed; retained-staff default note present")
        else: bad(f"closure readout cleanup: leftover={gone_verdict} note={note_ok}")
        tax = pg.text_content("#rTax").strip()
        if "0.7 cents" in tax and "a month for the median homeowner" in tax:
            ok("tax-compensation line at the default loss: 0.7 cents of rate")
        else: bad(f"tax line at default: {tax[:80]}")

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
        if pg.text_content("#rTax").strip() == "":
            ok("tax-compensation line empty when the scenario saves money")
        else: bad(f"tax line should be empty at the ceiling: {pg.text_content('#rTax')[:60]}")

        # floor: 50% leakage corner
        pg.fill("#sCap", "0"); pg.dispatch_event("#sCap", "input")
        pg.fill("#sFix", "0"); pg.dispatch_event("#sFix", "input")
        pg.fill("#sTea", "0"); pg.dispatch_event("#sTea", "input")
        pg.fill("#sLeav", "50"); pg.dispatch_event("#sLeav", "input")
        pg.fill("#sAdd", "1000"); pg.dispatch_event("#sAdd", "input")
        pg.fill("#sProp", "95000"); pg.dispatch_event("#sProp", "input")
        pg.fill("#sBus", "190000"); pg.dispatch_event("#sBus", "input")
        if pg.text_content("#rNet").strip() == "-$591,545" and "0th percentile" in pg.text_content("#rRank"):
            ok("closure floor -$591,545 = grid min (calculator spans the whole grid)")
        else: bad(f"closure worst case: {pg.text_content('#rNet')} / {pg.text_content('#rRank')[:60]}")
        if pg.evaluate("document.getElementById('youClose').style.left") == "0%":
            ok("closure percentile marker follows the calculator (0% at the floor)")
        else: bad(f"marker at floor: {pg.evaluate('document.getElementById(`youClose`).style.left')}")
        if "3.1 cents" in pg.text_content("#rTax"):
            ok("tax-compensation line at the full-loss floor: 3.1 cents of rate")
        else: bad(f"tax line at floor: {pg.text_content('#rTax')[:80]}")

        # --- Growth calculator ---
        gro = pg.text_content("#rGro").strip()
        gverd = pg.text_content("#rGroVerdict").strip()
        gteach = pg.evaluate("document.getElementById('rGro').dataset.teachers")
        if gro == "$141,780" and "50th percentile" in gverd and "19,683 weighted scenarios" in gverd and gteach == "0":
            ok("growth default is the weighted median: $141,780, target 140, no hires; percentile-only readout")
        else: bad(f"growth defaults: {gro} / {gverd} / teachers={gteach}")
        pg.fill("#sGro", "200"); pg.dispatch_event("#sGro", "input")
        pg.fill("#sRat", "0"); pg.dispatch_event("#sRat", "input")
        pg.fill("#sTc", "56583"); pg.dispatch_event("#sTc", "input")
        pg.fill("#sSp", "2"); pg.dispatch_event("#sSp", "input")
        pg.fill("#sGb", "1000"); pg.dispatch_event("#sGb", "input")
        pg.fill("#sCps", "1000"); pg.dispatch_event("#sCps", "input")
        pg.fill("#sGad", "0"); pg.dispatch_event("#sGad", "input")
        if pg.text_content("#rGro").strip() == "$29,591":
            ok("worst reachable corner still pays: $29,591 (90 added, class of 18 at top salary, every cost maxed; grid-wide floor +$3,331)")
        else: bad(f"growth floor: {pg.text_content('#rGro')}")
        if pg.evaluate("document.getElementById('youGrow').style.left") != "50%":
            ok("growth percentile marker follows the calculator (moved off 50% at the corner)")
        else: bad("growth percentile marker did not move")
        pg.fill("#sGro", "153"); pg.dispatch_event("#sGro", "input")
        pg.fill("#sRat", "2"); pg.dispatch_event("#sRat", "input")
        teach_ds = pg.evaluate("document.getElementById('rGro').dataset.teachers")
        if teach_ds == "0":
            ok("headroom honored: 43 added students (to 153) hire no teacher at the district-cap class size")
        else: bad(f"headroom teachers: {teach_ds}")
        pg.fill("#sGro", "156"); pg.dispatch_event("#sGro", "input")
        pg.fill("#sRat", "0"); pg.dispatch_event("#sRat", "input")
        teach_ds = pg.evaluate("document.getElementById('rGro').dataset.teachers")
        if teach_ds == "1":
            ok("first hire lands at 21 students past the 25 open seats at the smaller-class setting")
        else: bad(f"first-hire teachers: {teach_ds}")
        pg.fill("#sRat", "1"); pg.dispatch_event("#sRat", "input")
        pg.fill("#sTc", "41718"); pg.dispatch_event("#sTc", "input")
        pg.fill("#sGro", "110"); pg.dispatch_event("#sGro", "input")
        if "No new students" in pg.text_content("#rGroVerdict"):
            ok("growth zero-gain edge case")
        else: bad("growth zero-gain verdict missing")

        # --- The plan, priced: calculator ---
        rplan = pg.text_content("#rPlan").strip()
        pverd = pg.text_content("#rPlanVerdict").strip()
        if rplan == "$921,393" and "$5.4 million of new bonds" in pverd and "23.0 million of building capacity" in pverd:
            ok("plan calculator default: $921,393 surplus buys the 5% raise, $5.4M bonds, $23.0M capacity")
        else: bad(f"plan defaults: {rplan} / {pverd[:100]}")
        pg.fill("#sPt", "10"); pg.dispatch_event("#sPt", "input")
        if "up to about a 9 percent raise" in pg.text_content("#rPlanVerdict"):
            ok("plan calculator caps the raise honestly (10% unaffordable at the low ends)")
        else: bad(f"plan raise cap: {pg.text_content('#rPlanVerdict')[:90]}")
        pg.fill("#sPt", "5"); pg.dispatch_event("#sPt", "input")
        pg.fill("#sPr", "0"); pg.dispatch_event("#sPr", "input")
        if "short of closing the $2.65 million gap" in pg.text_content("#rPlanVerdict"):
            ok("plan calculator reports the shortfall when the gap is not closed")
        else: bad(f"plan shortfall: {pg.text_content('#rPlanVerdict')[:90]}")
        pg.fill("#sPr", "100"); pg.dispatch_event("#sPr", "input")

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

        # --- Fill planner removed (duplicative of the growth calculator) ---
        gone_planner = pg.evaluate("['sRez','sTr','sRet','sSec','sAdd2','rFill'].filter(i=>document.getElementById(i)).length")
        if gone_planner == 0: ok("seat planner removed from Run the Numbers (duplicative of the growth calculator)")
        else: bad(f"{gone_planner} seat-planner elements still present")

        boxes = pg.query_selector_all(".checkrow input[type=checkbox]")
        if boxes:
            before = pg.evaluate("Object.values(Chart.instances).map(c=>c.data.datasets.length).join(',')")
            boxes[0].click(); pg.wait_for_timeout(300)
            after = pg.evaluate("Object.values(Chart.instances).map(c=>c.data.datasets.length).join(',')")
            if before != after: ok("score toggles update chart datasets")
            else: bad("score toggle changed nothing")
        else: bad("no score toggle checkboxes found")

        defaults_ok = pg.evaluate("!document.getElementById('tgKC').checked && document.getElementById('tgKO').checked && document.getElementById('tgKP').checked")
        if defaults_ok: ok("scores chart defaults: subjects on, composite off")
        else: bad("scores chart defaults wrong (tgKC should be off, tgKP/tgKO on)")

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
