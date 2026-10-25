# Competitions in OpenSWOS, in the original DOS 96/97, and in the SWOS 96/97 Mod

> **Sintesi (IT).** OpenSWOS rappresenta campionati e coppe con gli stessi record dell'originale SWOS
> (`Competition` + intestazioni league / cup / tournament / playoffs), oggi caricati da JSON
> (`bin/data_json/competitions/*.json`) ma con la stessa forma binaria del 1996. I *dati* (squadre,
> numero di divisioni, promozioni, gambe/supplementari/rigori per turno, gironi) sono quindi già
> modificabili; la *logica* dei formati è invece nel codice C tradotto 1:1 dall'assembly Amiga:
> calendari da tabelle fisse di coppie (2-24 squadre), classifica a criteri fissi (punti, differenza
> reti, gol fatti, nome), promozioni/retrocessioni a conteggi, play-off solo per l'Inghilterra,
> qualificazioni europee a 16 + 32 + 32 squadre con controlli rigidi (panic se il conto non torna).
> La Copa Libertadores è stata aggiunta come primo torneo "solo dati" più un modulo C dedicato.
> Il mod fa le stesse cose sull'eseguibile DOS con patch e stub: ha già quasi tutti i formati reali
> (Apertura/Clausura, split, play-out, promedio, league phase UEFA...), ma ognuno come codice
> separato. La conclusione è che nessuno dei due ha oggi un *motore dei formati* dichiarativo:
> è il pezzo da costruire (vedi `competition-engine-proposal.md`).

Status: draft for discussion, 2026-10-25. Branch `convergence-docs` of the fork `aminta/OpenSWOS`
(upstream commit `584367a`). Line numbers refer to that commit.

Reading guide: §1 gives the vocabulary, §2-§9 walk the season machinery of OpenSWOS, §10 compares
with the original DOS game, §11 with the Mod, §12 lists what is hard-coded vs data-driven, §13 the
open questions.

---

## 1. Vocabulary

- **Competition record** — the original game's description of one competition: a common head
  (`Competition`: `comp_id`, `type`, `team_number`, `begin_month`/`end_month`, name/team-list
  offsets) followed by a type-specific body. Four bodies exist: **league**, **cup**, **tournament**
  (groups and/or knockout stages) and **playoffs** (a small cup attached to a league).
- **compId** — byte 0 of every record, a `uint8_t` (`include/comp_identity.h:99`). Since the
  "dynamic competition" refactor it is the runtime identity (`COMPID_englishLeague = 46`, ...);
  57 named ids exist in `comp_identity.h`.
- **DIY competition** — the game's generic runtime container (`DIYCompetition` /
  `DIYCompetitionEx`, mainly in `src/diy_competition.c`): the one structure that is actually
  *played*. Every league, cup or tournament is copied into it, played, and copied back.
- **Working copy (`*Copy`)** — in a career, every static record has a mutable twin
  (`src/career_comp_copies.c`), rebuilt from the template at career start
  (`InitCareer`, `src/career_init.c:628`).
- **Career contest table** — the list of competitions a career runs (`_careerContests`, extended at
  runtime by `Comp_AppendCareerContest`, `src/competition_data.c:1616`; lookup `Comp_ById`,
  `src/competition_data.c:1647`).
- **Country table** — `_competitionsTable[256]` (`src/competition_data.c:1983`): per country code,
  `{primary (league), skip, secondary (cup), tertiary (second cup)}`.
- **Region table** (`QualifyingGroup`, e.g. `_europeTable`, `src/competition_data.c:1712`): the
  competitions and countries of a continent.

## 2. Where formats come from: data files vs code

### 2.1 Data (editable today)

`bin/data_json/competitions/` (about 220 KB; format described in `docs/DATA_PIPELINE.md`,
`docs/DATA_JSON.md`):

| File | Content (records) | Typical fields |
|---|---|---|
| `leagues.json` | 66 leagues | `divisions_count`, `rounds` (play each team n times), `points_for_win`, subs; per division `teams`, `promoted`, `promoted_po`, `relegated`, `relegated_po`, `qualifier_link_offset` |
| `cups.json` | 76 cups | `teams`, `away_goals_mode`, per round `{legs, extra_time, penalties}`, `team_seed_list` |
| `tournaments.json` | 14 tournaments (World Cup, Copa América, Copa Libertadores, ...) | `seeding_type`, `play_each_team`, per stage `{team_count, group_count, team_group_count}`, per round rules |
| `playoffs.json` | 7 play-off records (English divisions, ...) | like a small cup |
| `countries.json`, `country_competitions.json`, `qualifying.json`, `league_blocks.json`, `seed_buckets.json`, `career.json` | the graph that links countries, competitions, qualifications, seeding buckets | |

Two ways the JSON reaches the game (`docs/DATA_PIPELINE.md` §"Two mechanisms"): at runtime on SDL
(it *overwrites compiled records in place*), and at build time (Python emitters regenerate
`src/competition_data.c`, which both SDL and Amiga compile). The JSON is a **lossless image of the
1996 byte layout**: packed fields are split for editing (`round_rule_flags` -> `{legs, extra_time,
penalties}`), but nothing a 1996 record could not express can be expressed.

Since the refactor documented in `docs/COMPETITION_DYNAMIC_REFACTOR.md` (status: complete,
2026-09-30), a **new** competition can be added as pure data (heap-allocated record + working copy,
appended to the runtime tables). Copa Libertadores (`_copaLibertadores`, compId 128) was the proof;
the Amiga build gets it baked (`src/competition_data_copa_baked.c`).

### 2.2 Code (where the *rules* live)

Everything that decides *how* a season unfolds is C, translated function by function from the
Amiga 68k assembly (comments cite `SWOS2.s` line numbers). The main files:

| File | Lines | Role |
|---|---|---|
| `src/diy_competition.c` | 11 619 | the generic engine: init from record, fixtures, results, tables, cup brackets, ET/penalties, DIY design menus |
| `src/career_season.c` | 1 734 | season end: per-country processing, promotion/relegation, cup pick lists, national-team qualifying |
| `src/career_eurocups.c` | 790 | European places, European cup slots, draw, EC/WC national slots |
| `src/career_copa.c` | 290 | Copa Libertadores qualifier (champion + runner-up of 10 CONMEBOL leagues) |
| `src/competition_data.c` | 2 088 | generated tables (records, country/region tables, contest table) |
| `src/save_format_json.c` | — | JSON save (schema 3) and the competition JSON loader (~line 3020) |

## 3. Season / career flow

1. **Career start** — `InitCareer` (`src/career_init.c:628`) memcpy's every template into its
   working copy, walking the career contest table.
2. **During the season** — each competition is loaded into the DIY container
   (`InitCompetitionFromRecord`, `src/diy_competition.c:9460`; league `InitDIYLeagueFromRecord`
   `:9266`; cup `InitDIYCupFromRecord` `:9181`). The player's competition is played interactively
   (`DIY_PlayOrSimulateLeagueFixture` `:11317`, `DIY_PlayCupMatchAndAdvance` `:10994`); the others
   are advanced automatically.
3. **Season end** — `Career_AdvanceToNextSeason_UpdateCompetitions` (`src/career_season.c:1662`):
   - prepares the European (and Copa) qualification lists;
   - updates the European cup slots (`Career_UpdateEuroCupCompetitionSlot` etc.,
     `src/career_eurocups.c:465-521`);
   - for the player's country first, then for every country in `_careerCompetitionIdRemapTable`:
     `Career_ProcessCompetitionForNextSeason` (`:782`) -> primary (league, every division),
     secondary and tertiary (cups) -> then `Career_ProcessCompetitionForEuropeanCupQualification`
     (`src/career_eurocups.c:274`) and the Copa qualifier;
   - **hard count gate**: the appended team count must equal `0x50` (16 + 32 + 32) plus the Copa
     count, and the three European lists must be exactly 16 / 32 / 32, else panic `0x8998` /
     `0x8999` (`src/career_season.c:1712-1733`);
   - draws the European cups (`Career_DrawEuropeanCupTeamsAndCopyGrids`, `src/career_eurocups.c:612`)
     and stores promotion/relegation in the season info.

A league's divisions are processed in order (`processPrimaryCompetitionForNextSeason`,
`src/career_season.c:1573`): the player's division interactively, the others auto-simulated
(`Career_AutoAdvanceInternationalCompetitionFixtures`), each followed by
`DIY_UpdatePromotionRelegationScratchCounts` and the copy of its final order.

## 4. Fixtures and calendar

- **League fixtures come from fixed pair tables**, one per club count from 2 to 24
  (`_fixtureSchedulePtrTable[23]`, `src/swos_amiga_ptr_imports.c:1495`; readable copy in
  `src/fixture_data.c`). `getCurrentFixtureTeamPtrs` (`src/diy_competition.c:1823`) reads pair
  `sectionMatchesProgress` of the table for `totalMatchesInRound` clubs, maps positions through a
  per-competition shuffle (`shuffleAndPad`), and swaps home/away for the second cycle. The
  European Championship uses its own table (`_euroChampFixtureData`, by-id special case `:1843`).
- **Consequence**: more than 24 clubs in one table is impossible without new code, and the order of
  rounds is fixed by the table (a per-season "real fixture list" cannot be expressed).
- The odd-size tables are **not proper rounds**: OpenSWOS reads `n // 2` pairs as one match day,
  and in its own tables (`src/fixture_data.c`) 9 of the 15 "match days" for 15 clubs and 15 of 21
  for 21 clubs list a club twice (checked 2026-10-25 by grouping the pairs; even sizes are clean).
  The Mod found the same in the DOS exe and rewrote the tables (`tools/oddtables.py`, its
  docstring explains the career calendar trap this causes).
- **Calendar**: a competition has `begin_month`/`end_month` in 1/8-month units
  (`docs/DATA_PIPELINE.md`), and league phases switch on `phaseStartMonths[]`
  (`DIY_AdvanceLeagueProgressAfterMatch`, `src/diy_competition.c:1967`). Match days are spread over
  that window by the game; there are no explicit dates.

## 5. Tables and tie-breakers

`DIY_SortLeagueTableByStandings` (`src/diy_competition.c:571`) is a bubble sort per group with a
**fixed** order: points > goal difference > goals for > **alphabetical name**. No head-to-head, no
away goals in the table, no fair play, no play-off for the title, no point deductions. Points for a
win come from the record (`points_for_win`, 2 or 3). Groups of a tournament are sorted the same way;
"top N + best Kth" advancement exists through `divisionFactor` and a global re-rank
(`src/diy_competition.c` ~3848-3908, per `docs/COMPETITION_DYNAMIC_REFACTOR.md` §4).

## 6. Promotion and relegation

- Per division: `promoted` / `relegated` counts (+ `_po` play-off counts) in the league record.
- `DIY_UpdatePromotionRelegationScratchCounts` (`src/diy_competition.c:2272`) walks the sorted
  table: top `promoted` clubs get `scratch[globalTeamNumber]--`, bottom `relegated` get `++`; the
  scratch buffer then moves clubs between division files.
- **Play-offs are hard-wired to England**: `processDiyLeagueQualificationEntry`
  (`src/career_season.c:1458`) returns for any league other than `COMPID_englishLeague` and
  switches on the division index to pick `div1/2/3Playoffs`. A play-off for another country, a
  play-out, or a relegation play-off needs new C.
- Relegation is always by the season table: no multi-season averages (promedio), no aggregate
  tables, no split rounds, no Apertura/Clausura.

## 7. Cups: draws, legs, extra time, penalties

- Per round: `legs` (1/2), `extra_time`, `penalties` from `round_rule_flags`
  (`InitDIYCupFromRecord`, `src/diy_competition.c:9245-9246`); `away_goals_mode` per cup
  (`:9220`). The ET and shoot-out results of simulated matches are cached
  (`getCachedOrCalcExtraTimeResult` / `getCachedOrCalcPenaltyResult`, `:10232-10243`).
- Rounds halve (`matchPairsPerRound >>= 1`, `DIY_UpdateCompetitionProgress` ~`:2790`): a cup is a
  power-of-two bracket; byes are a separate per-round count in the DIY-cup design.
- **Draws** use the game's PRNG: `DIY_ShuffleTeams` (Fisher-Yates with `Rand2`, `:250`),
  `DIY_SortAndShuffleTeamsByValue` (`:277`: sort by average player price, shuffle inside pots),
  fixed shuffle orders for 4 and 8 teams (`_diyShuffleOrder4Teams`, `_diyShuffleOrder8Teams`).
  No country protection, no "same group" constraints, no seeding by coefficient.
- Replays, "better-placed club advances", neutral ground and "not played if the gap is >= N
  points" do not exist.

## 8. European places and continental cups

`Career_ProcessCompetitionForEuropeanCupQualification` (`src/career_eurocups.c:274`) runs only for
European countries (first byte of the country entry == 0) and, per country, consumes ids from
eligibility lists: champion -> European Cup; cup winner (skipping the champion and the EC holder) ->
Cup Winners' Cup; then UEFA Cup places from the league order skipping every club already placed
(`qualifyTeamsForUefaCup`, `:231`). The number of places per country is the number of times the
country appears in the eligibility list, i.e. **data, but frozen 1996 data**: no coefficients, no
access list, no qualifying rounds. The Copa Libertadores qualifier (`src/career_copa.c`) is a
separate module with its own counts, added beside the European one and patched into the count gate.

## 9. Randomness, saves, tests

- **PRNG**: two table-driven 8-bit generators (`Rand`, `Rand2`, `src/random.c:41,66`). `_seed` is
  set from the clock tick in several menus (`src/menus.c:2636,3737,3773,3832`); a fixed value can be
  forced for replays (`_replayFixedRandom`). The match engine and the competition logic share the
  generators, so the season is reproducible only if every match is replayed identically.
- **Saves**: JSON, `SAVE_JSON_SCHEMA_VERSION 3` (`src/save_format_json.c:308`), competitions keyed by
  semantic id, working copies rebuilt from templates (only a few dynamic bytes saved). A version
  mismatch is refused (no migration).
- **Tests**: a strong recorded-match replay rig (`docs/TESTS.md`) for *gameplay*. I found no
  automated *season* or *career* golden test (season end, promotions, European places); the
  refactor docs verify these by hand / gdb.

## 10. Comparison with the original DOS 96/97

Sources: Zlatko Karakas's disassembly (`~/swos-mod/ref/swos.asm`, and github.com/zlatkok/swos-port),
the Mod's notes. OpenSWOS's own `docs/TESTS.md` states that the DOS build is a recompile of the
Amiga one, and the Mod's findings agree: the competition logic is the same.

| Topic | DOS 96/97 (as found by the Mod) | OpenSWOS |
|---|---|---|
| Records | same packed records, in the exe data segment | same layout, now JSON + generated C |
| Identity | by address (pointer compares) | by `compId` since the 2026 refactor |
| Fixtures | pair tables `dseg_11F356[n-2]` (n = 2..24), odd ones are not real rounds | same tables (`_fixtureSchedulePtrTable`) |
| Team cache | `g_selectedTeams` = 100 teams; career file = `careerFileBuffer .. g_selectedTeams` | buffers ported; JSON save removes the byte-range coupling |
| Season end | `cseg_91428`: record-count check `cmp careerFileBuffer, 80` then fatal trap `int 3` | same check as `PanicHaltLoop` codes `0x8998/0x8999` |
| Play-offs | England only | England only |
| New competition | impossible without patching code and data | possible as data (Copa) + a C module for its qualifier |

## 11. How the Mod extends the DOS game

The Mod (aminta/swos-9697-mod) keeps the 1996 exe and adds behaviour by patching the LE executable
(`tools/le.py`, `lepatch.py`), inserting nasm stubs in code caves (`nasmcave.py`) and, for complex
logic, small C modules compiled for i486 and linked into the exe (`tools/cobj.py`, e.g.
`uefaq.c`, `conti.c`, `gplay.c`, `statesim.c`). Data packs (`packs/`, `pack.json`) are compiled into
team files and tables by `mkseason.py` / `careerworld.py`. What it adds, by module (summary, not code):

| Need | Mod module(s) | Notes |
|---|---|---|
| Historic career worlds, several worlds in one exe | `careerworld.py` | per-world place lists, management record |
| Odd leagues with real rounds | `oddtables.py` | rewrites the pair tables (circle method) |
| Leagues > 24 clubs | `longtable.py` | Argentina 30, MLS 30 |
| Parallel groups (Serie C 3x20, Serie D 9 groups) | `pgroups.py` | |
| Split / championship rounds | `split.py` | Scotland, Austria, Greece, Romania... |
| Apertura / Clausura (+ final phases) | `argcal.py`, `arg97.py` | real fixture lists, points reset |
| Promedio relegation | (Argentina modules) | multi-season averages |
| Play-offs / play-outs anywhere, "better placed advances", gap rule | `engine.py` + `gplay.c` | one shared tie-break setting per round (CONVENTIONS 10) |
| UEFA league phase (36-club table, pots, 8 opponents) | `lp36.py` | in the DIY group engine |
| UEFA qualifying rounds, access list, coefficients | `uefaq.c` / `uefaq.py`, `uefacoef.py` | Python reference model compared with the C port (0 diffs) |
| Other continents' cups | `sacups.py`, `lib97.py`, `conti.c` / `conti.py`, `cafcups.py` | |
| State championships (Brazil) | `statespec.py`, `statecup.py`, `statesim.c` | a spec compiler: the closest thing to a declarative format |
| Zone colours, legend, FORMAT pages | `zones.py`, `fmtpage.py`, `fmtprose.py`, `complist.py` | the list of formats is generated (`complist.py`) |
| Off-file pools, big team cache | `ripool.py`, `worldpool.py`, big cache switch | |

The Mod's rules for formats are in `notes/CONVENTIONS.md` (real formats exactly; one shared
tie-break engine; every rule documented; result-dependent tests forced, never re-run). Testing is
an automated harness that plays the real exe in DOSBox-X (`tools/swostest.py`).

**What this shows**: the Mod already has the *catalogue* of real formats (91 countries, 134
divisions, 87 national cups, 15 continental cups in World 2026-27, listed in
`release/world-2026-27-competitions.md`) and several *partial* spec languages (`pack.json`,
`statespec`, `complist`), but each format is implemented where it fit in the exe. The cost is
visible in its pitfalls list (CONVENTIONS 18-19): traps found late, load hooks that silently skip.

## 12. Hard-coded vs data-driven (OpenSWOS today)

| Aspect | Data-driven | Hard-coded |
|---|---|---|
| Teams per division, number of divisions | yes | max 24 per table (fixture tables) |
| Rounds (play each team n times), points for a win | yes | |
| Promotion / relegation counts | yes | always by the final table |
| Play-offs | count only | England only (`career_season.c:1458`) |
| Cup legs / ET / penalties per round, away goals | yes | power-of-two halving |
| Groups + knockout (tournament) | stage sizes | group sort order, advancement rules |
| Tie-breakers | — | points, GD, GF, name |
| Fixture order | — | fixed pair tables |
| Calendar | month window | no dates, no real fixtures |
| European places | eligibility lists (1996) | 16/32/32 counts, count gate panics |
| New continental cup | record (Copa) | its qualifier is C (`career_copa.c`) |
| Draw / seeding | seeding type | price-based pots, no country protection |
| Identity | compId (`uint8_t`) | at most 256 competitions |

## 13. Open questions (for the OpenSWOS side)

1. Is a season-level golden test welcome upstream (seeded season end, compare promotions / places /
   cup winners as JSON)? It would be the first deliverable of any convergence.
2. Would the project accept a new engine *beside* the faithful one (the faithful one stays the
   default, the new one runs mod data), or should everything go through the original records?
3. The odd-size fixture tables (§4, a club twice on some match days): is "faithful bug" or "fixed" preferred?
4. compId is one byte: is widening the identity acceptable (World 2026-27 alone has ~250
   competitions)?
5. Does the JSON save schema have a migration policy, or is refusing old versions final?
