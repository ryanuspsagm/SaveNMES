# Adversarial Fact-Check Report — SaveNMES (checked 2026-07-20)

**Network caveat that shaped everything below:** this session's egress proxy enforces an allowlist that returned **403 on every direct fetch** — WebFetch failed even on `example.com`, and curl CONNECT tunnels were refused for change.org, bourbon.kyschools.us, savenmes.org, education.ky.gov, revenue.ky.gov, ballotpedia.org, api.github.com. **Only WebSearch worked.** So "unreachable" below means blocked-from-here, not confirmed-dead. Nothing below is a guess; every VERIFIED item traces to a search-corroborated source.

---

## VERIFIED (via reachable sources)

### 3. July 23 meeting — NOT stale (and the year is explicit)
- **FACT:** "July 23 • 6:30 p.m. • North Middletown Community Center" (`index.html`, "Show up Thursday" card) and PDF p.3 timeline "July 23 (scheduled) Community meeting set for 6:30 p.m. at the North Middletown Community Center."
- **SOURCE:** Read of index.html; full-text extraction of `Saving_North_Middletown_Elementary.pdf` (30 pp., "Version 2.2, July 20, 2026" on every page — the document is dated *today*).
- **RESULT: VERIFIED as upcoming.** July 23, 2026 is this Thursday (3 days out); "Thursday" matches the date. July 29 LPC forum also upcoming. The repo's last commit is timestamped 2026-07-20 12:52 UTC. No staleness.
- **BUT — one real discrepancy (see Contradicted section below on venue).**

### 4b. SEEK base guarantee $4,586 FY2026 / $4,626 FY2027
- **SOURCE:** WebSearch → Kentucky Center for Economic Policy: "raising per-pupil funding from $4,586 to $4,626 in FY27 and $4,792 in FY28" ([kypolicy.org SEEK analysis](https://kypolicy.org/seek-payments-decline-in-2027/), [budget agreement analysis](https://kypolicy.org/budget-agreement-cuts-and-freezes-funding-for-most-services-continues-to-underfund-medicaid/)).
- **RESULT: VERIFIED** — both figures exact.

### 4d. NMES enrollment ~128
- **SOURCE:** WebSearch snippets citing NCES: "in 2025-2026 school year, the school served 128 students" ([NCES school detail](https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?Search=1&County=Bourbon+County&State=21&ID=210054000096)); WKYT quotes Supt. Begley as saying "around 100."
- **RESULT: VERIFIED** (128 per federal data). Note the site *already anticipates* the ~100-vs-128 discrepancy in Question 2 — that's honest framing, no fix needed.

### 4a (partial). Statewide school tax average ~65 cents
- **SOURCE:** WebSearch → kypolicy.org: 2024 average real-property school rate ~65 cents.
- **RESULT: PARTIALLY VERIFIED** — 65.1 is consistent with the ~65-cent figure; exact decimal and the Bourbon 52.4 could not be confirmed (rate book PDF blocked, see below).

### 5. News check — site is current, no board vote yet
- **SOURCE:** WebSearch → [WKYT July 16](https://www.wkyt.com/2026/07/16/residents-alumni-defend-small-town-school-closure-bourbon-county/), [WKYT July 17](https://www.wkyt.com/2026/07/17/community-meeting-planned-bourbon-co-elementary-school-danger-closing/), [Bourbon County Citizen July 16](https://www.bourboncountycitizen.com/2026/07/16/bourbon-county-schools-local-planning-committee-hosts-public-forum-regarding-nmes/), [FOX 56](https://fox56news.com/news/local/bourbon-county-schools-hosting-2nd-meeting-amid-concerns-for-fate-of-elementary-school/).
- **RESULT: VERIFIED.** LPC forum held Wed. July 15; committee then voted to reclassify NMES "transitional" (advisory only); ~100 supporters attended; **no board vote has occurred**. This matches the site's framing exactly ("On July 15, 2026, a planning committee voted…"). Supt. name **Larry Begley confirmed** by WKYT. The two news sources cited in the site's Sources list are real, live URLs.

### 2 (partial). Board roster names
- **SOURCE:** WebSearch → Ballotpedia: Bradley Wayne Purcell (Dist. 2), Miranda Wyles (Dist. 4, vs. Lana Fryman), Amanda McCauley Thornberry (Dist. 5) all ran in the Nov. 5, 2024 board elections; "Mandy" = Amanda Thornberry checks out.
- **RESULT: PARTIALLY VERIFIED** — three of five names independently corroborated as board candidates/members; Begley as superintendent confirmed. Ott and Buckler not found in search snippets (Ballotpedia page itself blocked). No evidence of turnover found, but winners of the 2024 races could not be confirmed.

---

## CONTRADICTED / NEEDS ATTENTION

### Meeting venue discrepancy — HIGH severity, time-critical (3 days out)
- **FACT ON SITE:** July 23 meeting "at the North Middletown Community Center, next to the fire department on Church Street."
- **CONTRADICTING SOURCE:** WKYT (July 17): supporters "are invited to a community meeting **at the school** next Thursday at 6:30 p.m." — same event (same date, time, "love letter" activity).
- **RESULT: CONTRADICTED by the only reachable independent source.** Either WKYT is loose with the venue or the site is — but sending families to the wrong building Thursday evening is the worst possible failure mode for this page.
- **FIX:** Confirm the venue with organizers today and either correct index.html + PDF p.3, or add "(venue per organizers; WKYT reported 'at the school' — confirm before you go)" — ideally get WKYT to correct if the site is right.

---

## COULD NOT REACH (egress-blocked — verify manually before Thursday)

| # | Fact | Source tried | Result |
|---|------|-------------|--------|
| 1 | Petition live + signature count | change.org URL (WebFetch + curl 403); 3 search attempts — exact slug not in search index | **UNREACHABLE / UNCONFIRMED.** A dead petition link under the site's primary CTA would be high severity. Manually open the URL; if dead, fix `#petitionBtn` in index.html |
| 2 | Board page live, full roster, emails | bourbon.kyschools.us (403), openhouse.education.ky.gov (403), ballotpedia.org (403) | UNREACHABLE for full roster/emails; 3 of 5 names + Begley corroborated (above) |
| 4a | Bourbon 52.4 exact | revenue.ky.gov 2025 Rate Book PDF (curl 403), education.ky.gov Taxes page (403) | UNREACHABLE — only the ~65-cent state average corroborated |
| 4c | $19,348 per-pupil | reportcard.kyschools.us (KDE's actual domain — note `kyreportcard.ky.gov` does not appear to exist), SchoolDigger (403) | UNREACHABLE. NKyTribune confirms 2024-25 per-pupil data was just released in the KY School Report Card, and SchoolDigger's snippet calls NMES spending "relatively high," but the exact figure is unconfirmed |
| 6 | savenmes.org live + matches repo ("58.2") | CNAME reads `savenmes.org`; direct fetch 403; api.github.com blocked | UNREACHABLE — cannot confirm the deployed site matches the repo, whose last commit was today 12:52 UTC |

## Bottom line
Nothing on the site is stale — the PDF is dated today, the July 23/29 events are upcoming, no board vote has happened, and the SEEK figures, enrollment, LPC-vote narrative, superintendent, and cited news stories all check out. The one live contradiction is the **July 23 meeting venue** (site: Community Center; WKYT: "at the school") — resolve that within 72 hours. The petition link, exact tax rates, $19,348, and the deployed savenmes.org could not be reached from this sandbox and need a 5-minute manual check from an unrestricted connection.

Sources: [WKYT 7/16](https://www.wkyt.com/2026/07/16/residents-alumni-defend-small-town-school-closure-bourbon-county/) · [WKYT 7/17](https://www.wkyt.com/2026/07/17/community-meeting-planned-bourbon-co-elementary-school-danger-closing/) · [Bourbon County Citizen 7/16](https://www.bourboncountycitizen.com/2026/07/16/bourbon-county-schools-local-planning-committee-hosts-public-forum-regarding-nmes/) · [FOX 56](https://fox56news.com/news/local/bourbon-county-schools-hosting-2nd-meeting-amid-concerns-for-fate-of-elementary-school/) · [KY Policy — SEEK](https://kypolicy.org/seek-payments-decline-in-2027/) · [KY Policy — budget](https://kypolicy.org/budget-agreement-cuts-and-freezes-funding-for-most-services-continues-to-underfund-medicaid/) · [NCES NMES](https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?Search=1&County=Bourbon+County&State=21&ID=210054000096) · [NKyTribune on 2024-25 report card data](https://nkytribune.com/2026/07/kentucky-residents-can-view-2024-25-local-school-financial-date-in-kentucky-school-report-card/)
