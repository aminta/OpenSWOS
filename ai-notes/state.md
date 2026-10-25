# State — OpenSWOS convergence (updated 2026-10-25)

## Done
- Fork aminta/OpenSWOS cloned to ~/OpenSWOS, branch convergence-docs from upstream 584367a.
- docs/convergence/: README, competitions-in-openswos.md (task 2), competition-engine-proposal.md
  (task 3), ai-development-guidelines.md (task 4); rows added to docs/INDEX.md.
- ai-notes/ (this folder) created on Davide's request: AI notes separate from developer docs.

## Decisions (proposed, not yet approved by Davide)
- Recommend option B+C: standalone C99 engine library + versioned data packs; faithful 1996 path
  stays default; 1996 formats become specs only when golden tests prove equivalence.
- Spec: JSON canonical + JSON Schema 2020-12, YAML for authoring; stage types rr / groups /
  league_phase / knockout / playoff / split / aggregate_table / average_table / single_match.
- Determinism: specified integer RNG, substreams hash(seed, season, purpose); stub result provider.
- First deliverable suggested to OpenSWOS: season golden test of the current game (phase 0).

## Open questions
- Davide: licence of the engine (GPL vs separate permissive lib), Mod code licence, data sources
  (Transfermarkt, EA FC ratings, Wikipedia CC BY-SA kits), pack distribution.
- OpenSWOS side (doc 1 §13): golden test welcome? engine beside faithful path? odd tables fix?
  widen compId? save migrations?

## Next step
- Waiting for Davide's review and ok to push the branch to his fork (no upstream contact).
- If approved later: draft schema/competition.schema.json.
