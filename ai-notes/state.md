# State — OpenSWOS convergence (updated 2026-10-25)

## Done
- Fork aminta/OpenSWOS cloned to ~/OpenSWOS, branch convergence-docs from upstream 584367a.
- docs/convergence/: README, competitions-in-openswos.md, competition-engine-proposal.md,
  rule-catalogue.md (modules/ports + every Mod 2026-27 rule + CONCACAF module), testing-strategy.md
  (pyramid L0-L6, few E2E), lessons-from-the-mod.md (31 real bugs -> prevention -> test),
  ai-development-guidelines.md; Mermaid diagrams; INDEX.md row.
- 2026-10-25 full pass on Mod notes + Davide's messages in 53 SWOS sessions (extracted from
  ~/.claude/projects/*.jsonl user messages, keyword filter): catalogue §3.12 precedence/guarantees,
  §3.13 23 new primitives (second teams, direct_if_gap, title_seed, cuadrangulares, best_of, titles...).
- ai-notes/ (this folder) created on Davide's request: AI notes separate from developer docs.

## Decisions (proposed, not yet approved by Davide)
- Recommend option B+C: standalone C99 engine library + versioned data packs; faithful 1996 path
  stays default; 1996 formats become specs only when golden tests prove equivalence.
- Spec: JSON canonical + JSON Schema 2020-12, YAML for authoring; stage types rr / groups /
  league_phase / knockout / playoff / split / aggregate_table / average_table / single_match.
- Determinism: specified integer RNG, substreams hash(seed, season, purpose); stub result provider.
- First deliverable suggested to OpenSWOS: season golden test of the current game (phase 0).

## Decision relayed by Regia (Davide, 26/10/2026)
After Mod 4.0.2 (~1 Nov) the Mod adopts this proposal as its own architecture: specs IDENTICAL to the
convergence-docs schema; ONE portable C99 freestanding engine compiled three ways (into the 1996 exe via
tools/cobj.py like conti.c/uefaq.c, natively for tests, into the OpenSWOS fork); spec compiler JSON ->
compact versioned binary for the exe; thin asm bridge. Goal: users edit/add formats. Next doc touch must
add: (1) freestanding C, no libc, 486, small memory; (2) binary compiled spec form; (3) engine state in a
save trailer with versioning; (4) strict validation + clear errors for user-authored specs.
(5) Davide 26/10: EVERY world we add (not only career worlds) is ALWAYS available in ALL modes: CAREER,
FRIENDLY, SEASON and PRESET COMPETITIONS (clubs, national teams, leagues, cups, continental cups): a world registers teams and
competitions once, every mode lists them, no per-mode duplicate data.
No work requested now; budget tight until Thu 29; no push without Davide's ok.

## Open questions
- Davide: licence of the engine (GPL vs separate permissive lib), Mod code licence, data sources
  (Transfermarkt, EA FC ratings, Wikipedia CC BY-SA kits), pack distribution.
- OpenSWOS side (doc 1 §13): golden test welcome? engine beside faithful path? odd tables fix?
  widen compId? save migrations?

## Published
- Pushed to aminta/OpenSWOS convergence-docs (Davide ok 2026-10-25). No upstream PR/contact.
- Italian artifact of the developer docs: https://claude.ai/artifact/CUearZGHwKovnhV2c8XxC5
  sources in ai-notes/artifact-it/ (IT md + build_doc.py + tpl.html + mermaid cfg); repo docs stay English.
  Rebuild after doc changes: translate the delta into the IT copy, republish (v2 = 5 parts + PNG diagrams).

## Next step
- Waiting for Davide's review of the content; next contact with Playaveli only on his ok.
- If approved later: draft schema/competition.schema.json.
