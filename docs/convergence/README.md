# Convergence: the SWOS 96/97 Mod and OpenSWOS

> **Sintesi (IT).** Cartella dei documenti per sviluppatori sulla possibile convergenza tra il mod
> SWOS 96/97 (aminta/swos-9697-mod) e OpenSWOS. Stato: bozza da discutere, nessun codice. Gli appunti
> di lavoro per le sessioni AI sono in `ai-notes/` (separati di proposito).

Status: plan, 2026-10-25. Nothing here is implemented; nothing has been proposed upstream yet.

| Document | What it is | Read it when |
|---|---|---|
| [competitions-in-openswos.md](competitions-in-openswos.md) | How OpenSWOS, the original DOS 96/97 game and the Mod represent and run leagues and cups; what is data and what is code | before touching competition code or data |
| [competition-engine-proposal.md](competition-engine-proposal.md) | Convergence options, a deterministic competition engine, the declarative spec, API, tests, four real formats as examples, migration plan, licensing questions | discussing or starting the engine |
| [rule-catalogue.md](rule-catalogue.md) | Modules (add/remove leagues and cups as folders linked by named ports), the full catalogue of rule primitives from the Mod's World 2026-27, a complete CONCACAF module, the validator | designing or writing a module |
| [ai-development-guidelines.md](ai-development-guidelines.md) | How AI sessions work on the engine: contract first, tests, small PRs, no binary patches, determinism | before any AI-assisted change |

Background in the Mod's repository: `notes/CONVENTIONS.md` (format rules),
`release/world-2026-27-competitions.md` (the catalogue of real formats in World 2026-27).
