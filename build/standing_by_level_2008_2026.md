# Bourbon County's standing by level, 2008 to 2011 and 2022 to 2026

One page, three panels: elementary on top, middle school in the middle, high school at the bottom. Each panel plots Bourbon County's percentile among Kentucky districts (100 = top) with the rank under every point. Chart: `build/standing_by_level_2008_2026_chart.png`. Data: `build/standing_by_level_2008_2026.csv`.

## What is ranked in each era

- 2008 to 2011 (CATS era): the Kentucky Core Content Test percent proficient or distinguished, averaged across the four subjects the LRC district profiles report for every district at every level (reading, mathematics, science, writing). Ranked among the 174 districts of the time; 169 had a high school. The profiles were decoded for every district by `build/parse_oea_district_profiles.py`, with the state row checked on every page, and the 2009 and 2011 reports (whose text layer is a glyph substitution) checked against the readable 2010 report district by district.
- 2022 to 2026 (current system): the state's overall accountability score for the level, ranked among the 172 districts (168 with a high school). The overall score blends reading and mathematics, science, social studies and writing, English learner progress, the school climate survey and, for high school, postsecondary readiness and graduation.
- The CATS academic index itself is not online for this era, and the files for the systems in between (Unbridled Learning, 2012 to 2017, and the first years of the current law, 2018 to 2021) are no longer published, so no comparable by-level district ranking exists for 2012 to 2021. The chart leaves that gap open rather than bridging it.

## Standing each year

| School year | Level | Measure | Bourbon | Kentucky | Rank | Districts | Percentile | Reading and math only |
|---|---|---|---|---|---|---|---|---|
| 2007-08 | ES | KCCT four-subject average | 80.2 | 69.0 | 16th | 174 | 91st | 26th of 174, 84th pct |
| 2007-08 | MS | KCCT four-subject average | 47.0 | 58.0 | 150th | 174 | 14th | 132nd of 174, 24th pct |
| 2007-08 | HS | KCCT four-subject average | 43.5 | 44.0 | 82nd | 169 | 51st | 125th of 169, 25th pct |
| 2008-09 | ES | KCCT four-subject average | 73.5 | 68.2 | 52nd | 174 | 69th | 54th of 174, 69th pct |
| 2008-09 | MS | KCCT four-subject average | 54.5 | 59.0 | 119th | 174 | 31st | 123rd of 174, 29th pct |
| 2008-09 | HS | KCCT four-subject average | 43.5 | 44.8 | 98th | 169 | 42nd | 93rd of 169, 44th pct |
| 2009-10 | ES | KCCT four-subject average | 78.0 | 69.8 | 26th | 174 | 85th | 22nd of 174, 86th pct |
| 2009-10 | MS | KCCT four-subject average | 60.0 | 58.8 | 81st | 174 | 53rd | 98th of 174, 42nd pct |
| 2009-10 | HS | KCCT four-subject average | 41.8 | 44.2 | 102nd | 169 | 39th | 86th of 169, 48th pct |
| 2010-11 | ES | KCCT four-subject average | 73.5 | 71.0 | 70th | 174 | 59th | 66th of 174, 60th pct |
| 2010-11 | MS | KCCT four-subject average | 63.0 | 62.8 | 89th | 174 | 49th | 105th of 174, 39th pct |
| 2010-11 | HS | KCCT four-subject average | 47.0 | 48.8 | 96th | 169 | 43rd | 44th of 169, 73rd pct |
| 2021-22 | ES | Overall score (yellow) | 53.1 | 59.1 | 112th | 172 | 35th | |
| 2021-22 | MS | Overall score (yellow) | 52.1 | 53.3 | 110th | 172 | 36th | |
| 2021-22 | HS | Overall score (yellow) | 61.9 | 59.6 | 87th | 168 | 48th | |
| 2022-23 | ES | Overall score (yellow) | 56.3 | 67.1 | 132nd | 172 | 23rd | |
| 2022-23 | MS | Overall score (orange) | 37.3 | 56.1 | 162nd | 172 | 6th | |
| 2022-23 | HS | Overall score (yellow) | 62.5 | 63.1 | 111th | 168 | 34th | |
| 2023-24 | ES | Overall score (yellow) | 57.1 | 62.9 | 119th | 172 | 30th | |
| 2023-24 | MS | Overall score (orange) | 49.7 | 56.6 | 141st | 172 | 18th | |
| 2023-24 | HS | Overall score (orange) | 52.5 | 63.1 | 159th | 168 | 6th | |
| 2024-25 | ES | Overall score (orange) | 52.2 | 65.0 | 154th | 172 | 11th | |
| 2024-25 | MS | Overall score (yellow) | 57.8 | 60.8 | 104th | 172 | 40th | |
| 2024-25 | HS | Overall score (yellow) | 67.2 | 68.3 | 121st | 168 | 28th | |
| 2025-26 | ES | Overall score (orange) | 51.0 | 64.7 | 138th | 172 | 20th | |
| 2025-26 | MS | Overall score (orange) | 49.1 | 59.1 | 139th | 172 | 19th | |
| 2025-26 | HS | Overall score (orange) | 53.7 | 67.5 | 163rd | 168 | 3rd | |

## Reading the chart

- Elementary school level: 91st percentile in 2007-08 (16th of 174) and 59th in 2010-11 (70th of 174); 35th percentile in 2021-22 (112th of 172) and 20th in 2025-26 (138th of 172).
- Middle school level: 14th percentile in 2007-08 (150th of 174) and 49th in 2010-11 (89th of 174); 36th percentile in 2021-22 (110th of 172) and 19th in 2025-26 (139th of 172).
- High school level: 51st percentile in 2007-08 (82nd of 169) and 43rd in 2010-11 (96th of 169); 48th percentile in 2021-22 (87th of 168) and 3rd in 2025-26 (163rd of 168).

Percentile is the share of Kentucky districts scoring at or below Bourbon County that year, ties split; rank 1 is the highest district. The reading and math only column repeats the CATS-era ranking on those two subjects alone, as a check on the four-subject average. The two agree within 15 percentile points everywhere except HS 2007-08 (51st percentile on four subjects, 25th on reading and math); HS 2010-11 (43rd percentile on four subjects, 73rd on reading and math). Those high school gaps come from science and writing: Bourbon's high school science ran above the state in 2008 while its reading ran well below, and in 2011 its mathematics ran above the state while its writing ran far below. The four-subject average is the closer match to today's overall score, which also counts science and writing.
