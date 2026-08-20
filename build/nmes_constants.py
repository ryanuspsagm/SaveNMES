"""Single source of truth for the load-bearing constants shared by the
model scripts. Every value here is cataloged with its primary source in
build/sources.json and machine-verified against the archived documents by
tests/verify_sources.py. Edit a value HERE, never in a downstream script;
the published artifacts and the test suites are rebased from these.

The site's inline JavaScript cannot import this file, so index.html
carries literal copies; tests/sync_check.py asserts the site's JS
constants match the grids these values drive.
"""

SEEK_BASE = 4626        # enacted FY2027 SEEK base guarantee per AADA:
                        # 2026 Ky. Acts ch. 168 (HB 500), p. 20, archived at
                        # build/ky_acts_2026_ch168_hb500.pdf
ADDON_CENTRAL = 500     # central SEEK add-ons leg; the at-risk weight alone
                        # (15% of base per free-lunch child, ~72% FRL) carries it
ADDON_LEGS = (0, 500, 1000)
SUPPLIES = 400          # non-teaching variable cost per student (MUNIS-measured
                        # $331; the growth model charges recruits the same figure)
TEACH = 108_958.80 / 2  # $54,479.40: the district's own fully loaded
                        # 0-years-experience teacher (Response Appendix A.1)
FIXED_ADMIN = 115_397.25      # school administration, MUNIS FY2026 actuals
FIXED_CUSTODIAL = 49_655.38   # custodial pay and benefits, same ledger
FIXED_LIBRARY = 49_051.77     # library, same ledger
FIXED_POS = FIXED_ADMIN + FIXED_CUSTODIAL + FIXED_LIBRARY   # 214,104.40

POP_TODAY = 115         # SAAR 2025-26 end-of-year count (the "today" basis)
POP_OFFICIAL = 128      # SAAR 2024-25 end-of-year count (anchors the capacity
                        # and cost comparisons, never called "today")
COHORT = 21.5           # entering class per year: midpoint of the recent
                        # 19-24 SAAR per-grade range; ten-year K average 22.2

CAPTURE_LEGS = (53_519, 80_279, 127_039)   # 50/75/100% of the district's own
                                           # building-bound lines + insurance
BUS_LEGS = (20_000, 63_000, 95_000)        # bottom-up; high leg = half the
                                           # $190,000 route-split maximum
LEAVER_LEGS = (117, 136, 154)              # posterior quartiles of the leave
                                           # share at steady state, from
                                           # exodus_model.py (k floored at 3.3)
