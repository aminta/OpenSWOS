# Code map — competitions (OpenSWOS @ 584367a, Mod read-only)

## OpenSWOS
Data: `bin/data_json/competitions/` leagues.json (66) cups.json (76) tournaments.json (14)
playoffs.json (7) + countries/country_competitions/qualifying/league_blocks/seed_buckets/career.json.
JSON = lossless image of 1996 records. Runtime overwrite (SDL) or baked into src/competition_data.c.
Docs: docs/DATA_PIPELINE.md, DATA_JSON.md, COMPETITION_DYNAMIC_REFACTOR.md (compId refactor, done
2026-09-30), COPA_LIBERTADORES.md, SAVE_FORMAT_JSON.md, TESTS.md (gameplay replay rig only).

Identity: compId uint8, include/comp_identity.h:99 comp_id(); 57 COMPID_*; COMPID_englishLeague=46;
Copa=128. Comp_AppendCareerContest competition_data.c:1616, Comp_ById :1647,
_competitionsTable[256] :1983 (per country {league, skip, cup, cup2}), _europeTable :1712.
Working copies: career_comp_copies.c; InitCareer career_init.c:628.

Engine (diy_competition.c, 11.6k lines, 1:1 from SWOS2.s):
- InitCompetitionFromRecord :9460, InitDIYLeagueFromRecord :9266, InitDIYCupFromRecord :9181
  (round flags ET/pens :9245, awayGoalsMode :9220)
- fixtures getCurrentFixtureTeamPtrs :1823; tables _fixtureSchedulePtrTable[23]
  swos_amiga_ptr_imports.c:1495 (2..24 clubs; copy in fixture_data.c); EC special table :1843
- table sort DIY_SortLeagueTableByStandings :571 = points, GD, GF, NAME (no h2h)
- DIY_AdvanceLeagueProgressAfterMatch :1967 (phaseStartMonths)
- promo/releg DIY_UpdatePromotionRelegationScratchCounts :2272 (scratch[globalTeamNumber]+-)
- cup round halving ~:2790; draws DIY_ShuffleTeams :250 (Rand2 Fisher-Yates),
  DIY_SortAndShuffleTeamsByValue :277 (avg price pots)
- play DIY_PlayCupMatchAndAdvance :10994, DIY_PlayOrSimulateLeagueFixture :11317,
  ET/pens cache :10232-10243
Season end (career_season.c): Career_AdvanceToNextSeason_UpdateCompetitions :1662;
count gate 0x50 + Copa, panics 0x8998/0x8999 :1712-1733; Career_ProcessCompetitionForNextSeason
:782; processPrimaryCompetitionForNextSeason :1573; play-offs ENGLAND ONLY
processDiyLeagueQualificationEntry :1458.
European places career_eurocups.c: ProcessCompetitionForEuropeanCupQualification :274,
qualifyTeamsForUefaCup :231, draw Career_DrawEuropeanCupTeamsAndCopyGrids :612. Copa: career_copa.c.
RNG random.c Rand :41 Rand2 :66; _seed from tick menus.c:2636,3737,3773,3832; _replayFixedRandom.
Save: save_format_json.c, SAVE_JSON_SCHEMA_VERSION 3 :308, comp JSON loader ~:3020.

Verified 2026-10-25: odd tables not real rounds (15 clubs: 9/15 days a club twice; 21: 15/21).
No season/career golden test exists (only gameplay replay rig).

## Mod (~/swos-mod, read only)
Rules notes/CONVENTIONS.md (9 real formats exactly, 10 one tie-break setting per round, 15 force
results). Catalogue release/world-2026-27-competitions.md (EN then IT; Mexico :356, Argentina :404).
Liga MX there = single 34-round table (not Apertura/Clausura). Tools: careerworld, mkseason,
oddtables, longtable, pgroups, split, argcal/arg97, engine.py+gplay.c (play-offs/outs), lp36,
uefaq.c/.py (+ Python reference model in internal/), uefacoef, sacups/lib97/conti/cafcups,
statespec (spec compiler), zones, fmtpage/fmtprose/complist, ripool/worldpool, cobj.py (C into LE).
DOS facts: pair tables dseg_11F356[n-2]; season end cseg_91428 `cmp careerFileBuffer,80` + int 3;
g_selectedTeams = 100 teams.
