"""Estimate: the NMES attendance zone's share of the Bourbon County Schools
property assessment roll.

No parcel-level roll with assessed values is publicly downloadable for Bourbon
County (the PVA's qPublic site is interactive-only; the state parcel services
carry no Bourbon values), so this is a documented ESTIMATE built entirely from
public endpoints and archived files:

  1. 2020 Census blocks for county 21017 from the Census TIGERweb REST service
     (housing units HU100, population POP100, land area, internal point),
     assigned to the three Bourbon County Schools attendance zones by
     point-in-polygon against build/sabs_zones.json (NCES EDGE SABS 2015-16).
     Blocks outside all three zones are the Paris Independent school territory.
  2. The 2025 DOR certified property values for Bourbon County by class
     (build/dor_certified_property_values_2007_2025.xlsx).
  3. The district's own FY2027 SEEK assessment of $2,400,209,505 as the
     denominator (build/seek_forecast_2026_27_data.xlsx), with Paris
     Independent's $444,349,093 confirming the district/independent split.

Each class is apportioned to the zone with a LOW / CENTRAL / HIGH assumption,
stated below. Farm land is the largest zone component and is assessed at
agricultural use value, which is why the zone's value share runs far below its
38 percent land share. Replace this estimate with the PVA's parcel roll
whenever the district or PVA produces it; the records ask is one file.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = json.load(open(HERE / "nmes_zone_blocks_2020.json"))

# --- census block facts (TIGERweb, 2020) -----------------------------------
county_hu, county_pop = S["county"]["HU"], S["county"]["POP"]
nz = S["zones"]["North Middletown Elementary School"]
zone_hu, zone_pop, zone_area = nz["HU"], nz["POP"], nz["AREA"]
county_area = S["county"]["AREA"]
assert county_hu == 9112 and county_pop == 20252
assert zone_hu == 1188 and zone_pop == 2625
SQMI = 2_589_988
assert abs(zone_area / SQMI - 110.1) < 0.2      # matches the SABS 110.3 sq mi
hu_share = zone_hu / county_hu                   # 13.0% of county housing
pop_share = zone_pop / county_pop                # 13.0% of county population
area_share = zone_area / county_area             # 38.0% of county land

# --- DOR 2025 certified, Bourbon County, taxable after homestead ------------
RES = 1_129_570_887 - 78_947_266 - 6_856_950     # residential lots, net HEX
FARM = 739_449_139 - 21_267_000 - 1_080_200      # farm at use value, net HEX
FARM_RESID = 398_052_991                         # farm residences (FCV), inside FARM
FARM_LAND = FARM - FARM_RESID                    # farm land+improvements at use value
COMM = 283_941_180 - 98_200
TANG = 138_223_550
PSC = 48_709_545 + 77_986_866 + 2_658_758        # PSC real + tangible + telecom
MV = 247_495_576 + 5_460_305                     # motor vehicles + boats
DISTRICT_ASSESSMENT = 2_400_209_505              # FY2027 SEEK, district territory
PARIS_ASSESSMENT = 444_349_093

# --- apportionment assumptions (LOW / CENTRAL / HIGH) ------------------------
housing_pool = RES + FARM_RESID                  # all dwelling value, one pool
cases = {}
for name, res_adj, farm_sh, comm_sh, tang_sh, psc_sh, mv_sh in [
        ("low",     0.70, 0.38, 0.02, 0.01, 0.15, 0.12),
        ("central", 0.80, 0.40, 0.04, 0.03, 0.25, 0.13),
        ("high",    0.90, 0.42, 0.07, 0.05, 0.35, 0.14)]:
    dollars = (housing_pool * hu_share * res_adj   # zone homes, valued below county mean
               + FARM_LAND * farm_sh               # farm land tracks land share
               + COMM * comm_sh
               + TANG * tang_sh
               + PSC * psc_sh                      # lines and substations track area
               + MV * mv_sh)                       # vehicles track population
    cases[name] = {"zone_dollars": round(dollars),
                   "share_of_district_roll": round(dollars / DISTRICT_ASSESSMENT, 4)}

out = {
    "what": ("Estimated share of the Bourbon County Schools assessment roll "
             "sitting inside the NMES attendance zone. An estimate, not the "
             "roll: replace with the PVA parcel file when produced."),
    "census_blocks": {"county_hu": county_hu, "zone_hu": zone_hu,
                      "zone_hu_share": round(hu_share, 4),
                      "zone_pop": zone_pop, "zone_pop_share": round(pop_share, 4),
                      "zone_land_share": round(area_share, 4),
                      "paris_territory_hu": S["unassigned_hu"]},
    "dor_2025_pools": {"housing_incl_farm_residences": housing_pool,
                       "farm_land_use_value": FARM_LAND, "commercial": COMM,
                       "tangible": TANG, "psc": PSC, "motor_vehicles_boats": MV},
    "district_assessment_fy2027": DISTRICT_ASSESSMENT,
    "paris_independent_assessment_fy2027": PARIS_ASSESSMENT,
    "estimate": cases,
    "gf_property_tax_from_zone": {
        k: round(v["share_of_district_roll"] * 7_829_060) for k, v in cases.items()},
}
json.dump(out, open(HERE / "nmes_zone_roll_estimate.json", "w"), indent=1)
for k, v in cases.items():
    print(f"{k:8} zone ${v['zone_dollars']:,} = {v['share_of_district_roll']*100:.1f}% "
          f"of the district roll; ~${out['gf_property_tax_from_zone'][k]:,} of GF property tax")
