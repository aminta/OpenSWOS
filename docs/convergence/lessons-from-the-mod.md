# Lessons from the Mod: real bugs and how the engine prevents them

> **Sintesi (IT).** I bug e le trappole veri incontrati dal Mod SWOS 96/97 tra settembre e ottobre 2026
> (segnalazioni dei giocatori, note di rilascio, note tecniche e messaggi di Davide in 53 sessioni), e per
> ognuno: perché è successo, quale regola o controllo del motore lo rende impossibile, e quale test lo
> blocca per sempre. La maggior parte nasce da un'unica causa: la regola stava nell'ordine del codice o in
> un limite nascosto dell'exe, invece che in un dato dichiarato e controllato.

Status: plan, 2026-10-25. Sources: the Mod's `release/notes-4.0.md` and `notes-4.0.1.md` (known limits and
fixes), `release/notes-world-2026-27.md`, `notes/CONVENTIONS.md` (pitfalls 18-19), `notes/domestic-schedule.md`,
`notes/sa401-exact-designs.md`, the sessions' handoff files in `internal/handoff/`, and Davide's messages in the
SWOS sessions (player reports from Pietro, the Siracusa and Mestre careers, Davide's own careers). References to
primitives are to `rule-catalogue.md`; test levels to `testing-strategy.md`.

---

## 1. Competition logic

| # | What happened (Mod) | Why | Engine prevention | Test |
|---|---|---|---|---|
| 1 | Milan won Serie A and the Conference League, then played the Europa League (Pietro, 4.0.1) | the Conference winner's slot was applied after, and over, the league champion's | entitlements + one precedence + guarantees (§3.12) | L3 scenario `league-champion-beats-uecl-winner`; L2 invariant "best entitlement" |
| 2 | One European place went to a club of the wrong association in some seasons (4.0 known limit) | place lists filled imperatively by several code paths (an earlier 1984-85 case: a list missing its terminator let one country take another's last place) | access lists resolved as a whole; guarantee "places per association = access list" checked every season end | L2 random seasons; L4 golden World 2026-27 |
| 3 | A promoted club never joined its new division's cup (Mestre to Serie C, no Coppa Italia Serie C); Siracusa's Coppa Italia never started after promotion | cup entrants frozen at the 2026-27 list | `cup.entrants_from_current_divisions` (§3.13) | L3 promotion + cup scenario over 2 seasons |
| 4 | A club promoted from Serie D was put in Serie C group A instead of C (Siracusa) | the promoted club took the relegated club's slot, ignoring geography | `groups.geographic_move` with a club `area` map; the validator checks every club has an area | L3 scenario per area; L2 invariant "club in its area's group" |
| 5 | A Serie D club saw the Serie C competitions and the Coppa Italia; a Serie C club saw the Coppa Italia A/B | the career showed every competition of the country | `visibility.real_only` (§3.10) | L5 career view test |
| 6 | In odd Serie D groups the club resting on the last matchday missed its play-off, decided by simulation; a later fix hung the season end and was reverted | the play-off was built per club after "its" last match | stages end when the *stage* ends (`stage.starts_after`), not per club; odd rounds are first-class (`round_robin.odd_rest`) | L2 odd sizes; L3 "rest on last matchday" |
| 7 | Argentina: the Clausura started while the Apertura play-offs were running | calendar weeks not reserved for the knockout | `stage.starts_after` + calendar validator (no club with two matches in a week) | L0 validator; L2 calendar invariant |
| 8 | Single-match play-offs showed replay dates | replay slots reserved by default | `calendar.no_phantom_replays` | L1 calendar builder |
| 9 | Copa do Brasil final went to extra time; the real rule is straight to penalties (since 3.2) | an inherited default decider | `decider.required`: no defaults | L0 validator rejects a round without a decider |
| 10 | CONCACAF Champions Cup: game plays away goals then penalties, real 2026 is away goals, extra time, penalties | a fixed set of tie modes | `decider` is an ordered list | L1 decider cases |
| 11 | Apertura champion, Trofeo de Campeones, MLS play-off winner, Malta's double winner not visible anywhere | titles decided beyond the table had no output | `titles` output + WINNERS view (§3.13) | L5 view test |
| 12 | Points reset at a split or tournament change confused players | the screen showed the league name only | `display.stage_in_title`, generated FORMAT text | visual check (L6) |
| 13 | Play-off zone missing from the table while "P.OFF" appeared in a corner; legend not matching painted zones | zones and legend computed separately | zones and legend both generated from outcome tags (`zones`) | L1 legend == zones |
| 14 | Libertadores group thirds to the Sudamericana play-off simulated, not played (4.0) | cross-cup move outside the played path | `cross_cup` ports; the career club plays any stage it enters | L3 scenario `q3-losers-to-sudamericana` and group-3rd variant |
| 15 | Nations without a national team: a Montenegrin called up by Yugoslavia | nationality mapped to the wrong team | national-team module declares eligible nationalities | L1 call-up eligibility (national-team layer, later) |
| 16 | Second teams could be promoted into their first team's league | no club relation in the data | `club.second_team` with per-country rules | L3 scenarios per country |

## 2. Hidden limits of the 1996 executable

| # | Limit hit | Where | Engine prevention |
|---|---|---|---|
| 17 | 24 clubs per league (pair tables) | Argentina 30, MLS 30 | no fixed sizes; generator for any n; validator warns only on UI limits |
| 18 | Odd tables are not real rounds (a club twice on some matchdays) | 15, 21 clubs; also present in OpenSWOS's tables | generated rounds; L2 invariant |
| 19 | The Mod's split engine holds at most 64 match days per league; the real 44-matchday calendars of Guatemala, El Salvador and Paraguay did not fit in 4.0 | split state | no fixed sizes |
| 20 | Team cache of 100 teams; career save = a fixed memory range | big worlds (English 4th division + league phase) | engine state in named JSON fields, no memory ranges |
| 21 | Season end checks "80 European entrants" and traps otherwise | the 1996 season end | counts come from the specs; the validator proves them before a season starts |
| 22 | In the team-strength calculation an average player price of zero (very weak clubs) caused a division by zero and a crash | strength calculation | input validation of squads (L0); property tests with degenerate squads |
| 23 | Country numbers were the same numbers used as menu ids: with several career worlds in one exe they clashed | multi-world exe | string ids with namespaces |

## 3. Process and testing

| # | What happened | Lesson | In the new project |
|---|---|---|---|
| 24 | A crash only in release builds (foreign market) because release data had pools test builds lacked (CONVENTIONS 17a) | test on the data you ship | golden worlds run on the shipped packs, not on test fixtures |
| 25 | A save made with one data version replayed on another looked like a hang | data versions must be explicit | save records pack id, version and hash; mismatch refused with a message |
| 26 | A text rewrite in a patcher silently skipped a load hook; season-3 trap (CONVENTIONS 19) | every generator asserts what it changed | importers and code generators assert counts; registry check fails on missing coverage |
| 27 | Serial harness runs shared module caches and produced false regressions | tests must be hermetic | each test builds its own world; no shared mutable caches |
| 28 | Rare cases reached by re-running seasons, wasting hours (Davide: "use cheats, not a thousand retries") | force, don't retry | scripted result provider (L3) |
| 29 | Shared data files changed before their engine change and broke other branches | data after engine | `module.json` declares the engine/schema version it needs; validator refuses newer data on an older engine |
| 30 | Rules re-invented per bug ("let's not reinvent the wheel every time", Davide 21/10) | one coherent rule set | primitives registry; a new rule is one reviewed PR with tests (guidelines) |
| 31 | Stray characters and titles too long for their bar | texts are data with limits | validator checks widths and the font's character set |

## 4. Patterns behind the list

1. **Order-dependent rules** (1, 2, 6, 7): the result depended on which code ran first. The engine resolves
   season ends as a whole, by declared precedence, and checks guarantees.
2. **Frozen or missing data** (3, 4, 16): lists that should be recomputed each season were fixed at the first
   season, or a datum was missing (a club's area, the first-team / second-team link). The engine derives entrants
   from the current state every season and the validator requires the data it needs.
3. **Implicit defaults** (8, 9, 10): a behaviour nobody chose. The schema has no defaults for rules that differ
   between competitions.
4. **Missing outputs** (5, 11, 12, 13): the engine knew something the player could not see. Every title, zone
   and visibility rule is an output of the spec, and the screens read it.
5. **Hidden limits** (17-23): sizes fixed in 1996. The engine has none; the validator warns only where the UI
   has a real limit.
6. **Untested paths** (24-28): tests that ran on other data, or relied on luck. Tests run on shipped data,
   are hermetic, and force their cases.
7. **Process rules** (29-31): data versions, re-invented rules, texts that do not fit. The validator and the
   primitives registry own them.
