# Historical Behavior Transition Map

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-07
assignment: BC-017

This chronology records material behavioral transitions, not every semver
boundary. “Introduced” means declared or mechanically scaffolded in the cited
source; it does not assert successful execution.

| era / boundary | transition type | behavior change | evidence class | evidence locators |
|---|---|---|---|---|
| v0.6 | capability introduction | Auth gains explicit session role, bounded challenge, retry/lock, success, sign-out, and reset state. | mechanically scaffolded | E-00013-AUTH |
| v0.7.4.1 | model-facing consolidation | Persona, Anchors, Teaching, and manual memories carry natural-language control; Teaching has a full pedagogy before School. | historical declared | E-00020-PERSONA; E-00020-TEACH |
| v0.7 → early v0.8 | ownership move | Engine-style routing gives way to Exec as the single proposal selector and output owner. | mechanically scaffolded | E-00029-NOEXEC; E-00030-EXEC |
| early v0.8 | state-model introduction | School adds explicit student/day/block/class state, checkpoints, grades, gates, and selected-only mutation. | mechanically scaffolded | E-00031-SCHOOL |
| v0.8 normalization | validation change | Exec adds ABI, one-owner/selected-only rules, DateLib integration, and fail-closed handling while retaining current-turn/no-wake limits. | mechanically scaffolded | E-00057-EXEC |
| v0.9 | memory-model introduction | MMU adds candidate classification, validation, quarantine, precedence, typed pools, and compact preload. | mechanically scaffolded | E-00072-MMU |
| v0.9 | ownership move | Mood becomes a named library behavior rather than only Persona expression. | historical declared | E-00020-PERSONA; E-00093-MOOD |
| v0.9 rebuild | behavior disappearance | School/Teaching ownership is removed or archived during rebuild; later families restore teaching through different routing. | historical declared | E-00093-MOOD; E-00094-ROUTER |
| v0.10 → v0.11 | architecture reversal | Behavior Router temporarily replaces Exec, then Exec returns. | historical declared | E-00094-ROUTER |
| v0.13–v0.16 | Exec absorption | reminder/time, Auth, mood, memory, retrieval, and feature patches accumulate inside Exec and ExecLib. | mechanically scaffolded | E-00127-TIME; E-00195-MEGAEXEC |
| late v0.16 | memory-model change | StateTree, Memory Program, and MemoryPacket distinguish staged, in-session, and persistent concepts. | historical declared | E-00210-MEMORY |
| first v0.20 | secondary discovery | MMU is prominent; Read Lane evidence is secondary and insufficient for promotion. | historical declared | E-00211-MMU |
| v0.20 | validation/security refinement | Auth receives a targeted fix and ScopeLock/Wu Sao appear in late orchestration. | mechanically scaffolded | E-00223-AUTH; E-00243-SCOPELOCK |
| v0.20 contraction | Exec simplification | Exec contracts sharply, but some complexity remains displaced into ExecLib. | mechanically scaffolded | E-00195-MEGAEXEC; E-00200-CONTRACTION |
| v0.21 | ownership decomposition | Restructuring analysis identifies authority confusion from Exec absorption and extracts service detail behind a thinner scheduler. | historical declared | E-00245-RESTRUCTURE; E-00245-MIGRATION |
| v0.21 → v0.22 | behavior survival | output ownership, validation, fail-closed routing, anti-drift authority, and ScopeLock survive in a compact Exec. | cross-version persistent | E-00243-SCOPELOCK; E-00246-EXEC; E-CURRENT-EXEC |
| current CTS | host boundary exposed | current-turn routing survives, but durable persistence, background wake, and named Auth/OPSEC service implementations are not proven inside the seven files. | current source truth / unavailable | E-CURRENT-INSTRUCTIONS; E-CURRENT-EXEC; E-CURRENT-EXECLIB |
