# State — OpenSWOS convergence (updated 2026-10-25)

## Done
- Fork aminta/OpenSWOS cloned to ~/OpenSWOS, branch convergence-docs from upstream 584367a.
- docs/convergence/: README, competitions-in-openswos.md, competition-engine-proposal.md,
  rule-catalogue.md (modules/ports + every Mod 2026-27 rule + CONCACAF module), testing-strategy.md
  (pyramid L0-L6, few E2E), ai-development-guidelines.md; Mermaid diagrams; INDEX.md row.
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

## Published
- Pushed to aminta/OpenSWOS convergence-docs (Davide ok 2026-10-25). No upstream PR/contact.
- Italian artifact of the developer docs: https://claude.ai/artifact/CUearZGHwKovnhV2c8XxC5
  sources in ai-notes/artifact-it/ (IT md + build_doc.py + tpl.html + mermaid cfg); repo docs stay English.
  Rebuild after doc changes: translate the delta into the IT copy, republish (v2 = 5 parts + PNG diagrams).

## Next step
- Waiting for Davide's review of the content; next contact with Playaveli only on his ok.
- If approved later: draft schema/competition.schema.json.
