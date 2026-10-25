# Rules for AI sessions in this project

- Owner: Davide Lorigliola (GitHub aminta). Reply to him in Italian; documents in English with an
  Italian summary at the top.
- Repo: fork `aminta/OpenSWOS` in `~/OpenSWOS`, branch `convergence-docs`; upstream
  `benbaker76/OpenSWOS` (remote `upstream`). Pre-approved outward action: only the fork itself.
  NEVER push, open PRs/issues upstream, or contact anyone (Playaveli, Ben Baker) without Davide's
  explicit ok in the current chat.
- `~/swos-mod` and its worktrees: READ ONLY (other SWOS sessions own them).
- GPL: OpenSWOS is GPL-3.0-or-later. Never copy OpenSWOS code into the Mod (Mod rule). Never
  copy Mod code here without Davide's relicensing decision.
- Budget: Davide is near weekly limits. Lean context: grep + targeted reads, no subagents, no
  DOSBox runs, no full builds unless asked.
- Commits: local only, message ends with the session's attribution line; read the sha from the
  commit output before reporting it.
- Milestones: one-line status to the "SWOS Regia" session (send_message) + 5-8 line Italian
  summary to Davide, then ask before pushing.
- Two spaces (Davide 2026-10-25): `ai-notes/` = notes for AI, `docs/convergence/` = docs for
  developers like Davide. Keep them separate; docs never depend on ai-notes.
- OpenSWOS house rules (`.claude/CLAUDE.md`): both targets must build, panics are signals,
  typed structs, saves = named JSON fields, list new docs in `docs/INDEX.md`.
