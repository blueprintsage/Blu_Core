# Blu Core Assignment Log

status: active
owner: docs/worklogs
last_reviewed: 2026-08-12
canonical_base: 7aed76e

## Rules

1. Read `AGENTS.md` before claiming work.
2. One owner per assignment and collision domain.
3. Every implementation packet names its base branch or commit.
4. One assignment per checkout; parallel work uses branches and worktrees.
5. The implementing agent runs checks and commits verified work.
6. Completion moves to `review`; Dad or Blu authorizes integration.
7. Golden kernel files are never an implementation collision domain.
8. Assignment status follows: `spec-needed` → `ready` → `active` → `review` → `done`.
9. Use `blocked` when an assignment cannot safely continue; record the reason before changing scope.

## Implementation assignments

| ID | Assignment | Owner | Status | Packet | Base | Collision domain / notes |
|---|---|---|---|---|---|---|
| BC-010 | Extract machine-readable runtime contracts from CTS | Codex | done | `docs/domains/runtime/assignments/BC-010/assignment.md` | `7aed76e` | Work commit `40138b6e16f28c01904aae97158878468ee47ad0`; closed after corrective assignments BC-010-C1 and BC-010-C2; integrated reviewed state before closure `8a37ae3c62829f16f949f5896d2bef0542721565` |
| BC-010-C1 | Runtime contract extraction corrections | Codex | done | `docs/domains/runtime/assignments/BC-010-C1/assignment.md` | `38611bf4b8051c858dcbbc30a07904d0117211b3` | Repair work commit `63c8b692403fe5ec1a9433a8313a7980fbd55437`; closed after its remaining OPSEC classification issue was corrected by BC-010-C2; integrated reviewed state before closure `8a37ae3c62829f16f949f5896d2bef0542721565` |
| BC-010-C2 | OPSEC route classification repair | Codex | done | `docs/domains/runtime/assignments/BC-010-C2/assignment.md` | `424f80b254a02f057da6c82db5230377076fc415` | Repair work commit `06292ce0e2f326ef84988e030c7fe14402192859`; closed after Claude's `approve-with-notes` review with no blockers; integrated reviewed state before closure `8a37ae3c62829f16f949f5896d2bef0542721565` |
| BC-015 | Runtime viability audit | Codex | done | `docs/domains/runtime/assignments/BC-015/assignment.md` | `4b51427b361283715a24110409e031e191b52452` | Audit work commit `9936cc4be2f7f397deebccdf7400e8b7b774df08`; review commit `4ed7626`; Claude disposition `approve-with-notes` with no blockers; integrated reviewed state before closure `1f07333457b18895fbb04d5c776e3259d870f2f6` |
| BC-016 | Historical Archive Inventory Integration | Codex | done | `docs/domains/runtime/assignments/BC-016/assignment.md` | `fdb6c7e150d3717172e08a1bc349a428187df45a` | Work commit `9f6d705723a3ee6d26e47b80c634bc3c58495c83`; metadata commit `2685dd5a3d4e81498e5b72cc83fad5d664a4d76a`; Claude review `1e7796191360cb5b81ab70a716ffda1e97f77264`; disposition `approve-with-notes` with no blockers; all NB-1 through NB-10 remain preserved and carried forward; no archives or behavioral archaeology |
| BC-017 | Historical Behavioral Archaeology | Codex | done | `docs/domains/runtime/assignments/BC-017/assignment.md` | `4abae4865067d8a6ae0651017d4a564c09dde47b` | Work `dcad56f7d50252ab70e993aef7a763ed2bd3617b`; metadata `01a004835dbd3e3e2702ba34dcc06f81f2a600f8`; owner correction `110ce2e82e39f60fa2158494888359389b70600a`; original Claude review `c323cff06c9f111408f4a416817d78fc0f3e2d2b` returned B-01/B-02/B-03; closed after C1 and Claude re-review `bea9463f0dbbae1c3944c5f44a7843c757d7f0bb` approved with notes and no blockers; integrated reviewed state `b88902d997685057ee0e76709df7117f8a83f295`; closure commit `b0182581c16bbb4dbeced715ae6e35bcee8bf097` |
| BC-017-C1 | Historical Archaeology Review Corrections | Codex | done | `docs/domains/runtime/assignments/BC-017-C1/assignment.md` | `c323cff06c9f111408f4a416817d78fc0f3e2d2b` | B-01/B-02/B-03 correction only; work `87c4e49333d30a471a00483fc1384e1918626ee1`; metadata `fd7f1707e242aa0e9621ab9f7293364860cab21d`; Claude re-review `bea9463f0dbbae1c3944c5f44a7843c757d7f0bb`; `approve-with-notes`, no blockers; integrated reviewed state `b88902d997685057ee0e76709df7117f8a83f295`; closure commit `b0182581c16bbb4dbeced715ae6e35bcee8bf097` |
| BC-020 | Define Chat and Codex capability adapter contracts | Codex | done | `docs/domains/runtime/assignments/BC-020/assignment.md` | `d4157e79fc7e2df6e1bd53b589cabfa19cd7238f` | Work `09c484418e51365cf9b156cf304eebae7fecde5d`; metadata `ccf3206ad033d588246e09001d47ddce3ac50a31`; original Claude review `370278cd91fd9ecca2c64cd0953cae7ed63c4d16` returned BF-1; closed after BC-020-C1 and final Claude re-review `b51912a655d3f895651eb0bdbbe0c41ba1e7f132` (`approve-with-notes`, no blockers); integrated closure base `642a5df7340c4f87ac723bffb4d308fef09bf2b2`; closure commit `1e42c5dd2ee049fa5ebe4280692d1caecc0a3533`; specification only, no runtime implementation |
| BC-020-C1 | Scheduling Capability Evidence Correction | Codex | done | `docs/domains/runtime/assignments/BC-020-C1/assignment.md` | `370278cd91fd9ecca2c64cd0953cae7ed63c4d16` | BF-1 correction only; work `b770be849d625e924f7e65cae4efb8894a7e4c23`; metadata `8eb29165d5d59b99ccaa3b06fe6d8613dcaa11e2`; Claude re-review `b51912a655d3f895651eb0bdbbe0c41ba1e7f132`; `approve-with-notes`, BF-1 resolved, zero blockers; integrated closure base `642a5df7340c4f87ac723bffb4d308fef09bf2b2`; closure commit `1e42c5dd2ee049fa5ebe4280692d1caecc0a3533` |
| BC-030 | Define Local Mirror continuity schema and lifecycle | Codex | done | `docs/domains/continuity/assignments/BC-030/assignment.md` | `a5f149355bd68b2aea1695e5f25ec60a2cb88b0c` | Work `6812513d10eeb69f1e5b477617ffdccc52e5067b`; metadata `4c4ef004aef2d93937de3fdb4bbbdeae4f2d9843`; work integration `d679357426899c660d905326ef345d7229974b0b`; Claude review `adda640c05035d14057a22fb1ac85c19c326fe4f` (`approve-with-notes`, zero blockers); reviewed integration base `c76843e82a42ab091810c110e8c01a4e32ed311e`; SUR-007 resolved at generic contract level; SUR-011 preserved; specification-only, no provider/runtime/LM Studio implementation; closure `a77393d6fc63e644f57a70992af6fec050a2e802` |
| BC-040 | One-Blu Portability and Python Runtime Readiness | Codex | done | `docs/domains/runtime/assignments/BC-040/assignment.md` | `66e7ed52f5777bdef2e32c71a5e83b439b0d0ade` | Work `8516bd6845edaa3ef9b18077d91853ccc21e3c3b`; metadata `dc5429cabf03aff4ea8b383cbc1290789c370ebb`; work integration `a24cffc2fb3b3b7ffe3e0291915d0319a4db3e5f`; Claude review `127ae61e296fe0d07072e1320dec8ca8c4b1dfed` (`approve-with-notes`, zero blockers); reviewed integration base `8801ae138deb0261deff47d02269c7a16773c892`; closure `d78f58972327434c83d7e79a2cb9372e487a9629`; One-Blu portability complete with required Custom GPT and Python/LM Studio targets and optional Codex; final result `not_ready_for_python_phase1`, SUR-001 sole implementation blocker; no production runtime/provider/security implementation |
| BC-041 | Protected Security Phase 1 — Minimum OPSEC Match and Redaction Contract | Codex | done | `docs/domains/runtime/assignments/BC-041/assignment.md` | `699ee1485cef39ffbe70c3b8e848763af02596e0` | Work `9ccd17d75955db4b64e5df27a5751d36b6964330`; metadata `9849c60138940068a0fd900eb49ce7444531109d`; original Claude review `ade01082a7bf4ebe389af6deafc68ea207d989d9` returned B-1 and remains immutable; closed through BC-041-C1 correction tip `204a229e2c01b255f1a940129cb724fa33fb4755`, current-main integration `131a527a8fef1f42df327443c9966c9e2f66f528`, and final Claude correction review `f0998f78aaada899a16d4413170ef3689f04fe28` (`approve-with-notes`, zero blockers); closure commit recorded by metadata receipt; no runtime implementation |
| BC-041-C1 | Unicode Format-Character OPSEC Correction | Codex | done | `docs/domains/runtime/assignments/BC-041-C1/assignment.md` | `33b44608cb634d1fedeed7f5f70d405c3999ed02` | First correction `80e5b8554639c274f7baa69155ea9b83910f604c`; first metadata `54519493189a332e984409504c45210e759f18fc`; first Claude review `874852c1b548ba4a2539d796d23ab9d803a966c8`; mixed correction `2a9d6a28111ca9576bf6811e67ccca37f4d5dd39`; mixed metadata `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1`; second Claude review `f87588d0fa094c203fde3b847ab9bc3c28d1b3fe`; outer-edge correction `85e18f56f88ab113646cc3aab477687eda8b85af`; outer-edge metadata `d1c283ab21681f8a0550da32c2ec87e08eb2852d`; truth cleanup `204a229e2c01b255f1a940129cb724fa33fb4755`; final review `f0998f78aaada899a16d4413170ef3689f04fe28` (`approve-with-notes`, B-1'/B-1″ resolved, zero blockers); review import `3e77111b6d86879f591c7ab8c52a571c51e7c48e`; closure commit recorded by metadata receipt; implementation unauthorized |

## Design assignments

| ID | Assignment | Owner | Status | Notes |
|---|---|---|---|---|
| BC-001 | Establish bootstrap authority and golden source | Blu | done | Verified on clean `main` at `7aed76e`; live history has two commits rather than the four-commit bootstrap plan, but all protected artifacts and checksums passed |
| BC-018 | Successor Kernel Boundary Specification | Codex | done | Packet: `docs/domains/runtime/assignments/BC-018/assignment.md`; exact base `a5e68b3189c60e2d5b8acbe8a212d69b720dec58`; work `413574097f8426d10ce5cf284282ddab87f4bc93`; metadata `ec4a3c14e6aedb7164fc500b0c9a31486bcd11e8`; correction `3384db41996d975d079d2d7f83a8e8fea9f4fce5`; corrected head `34af2d6bad00430215bb7a7476f4eae582449ff2`; original Claude review `7796c7e738e0ff66b677c79314b80cf2bbb09a63` (`return-for-correction`); closed after BC-018-C1 and final Claude re-review `1f440546a076c9359afaf5e832882e588d71dfa6` (`approve-with-notes`, no blockers); integrated closure base `ce1cc235057a5de3d71fefbcee32e5617197cbb0`; closure `373092e98fef4d291365462baaa7f1ea2a8f065b`; no runtime implementation |
| BC-018-C1 | Cross-Turn Security State Correction | Codex | done | Packet: `docs/domains/runtime/assignments/BC-018-C1/assignment.md`; triggering review `7796c7e738e0ff66b677c79314b80cf2bbb09a63`; correction `a87e7d7ea57688212c7c8461b5630c6ddb55a00f`; metadata `b1e0f5c7ce3fddd7d71f6b2fa8050b0b55875b3c`; terminal-authority correction `311c572f3a28fe4e1cca04b75856faae3cfd6c60`; exact review head `0227f550d270ba9ffae2d1bd986117e718b13608`; Claude re-review `1f440546a076c9359afaf5e832882e588d71dfa6` (`approve-with-notes`, no blockers); closure-prep correction `90e30c6d685eaa35c9bdf1a666179c9882877d85`; metadata `e55be9986ade91d5cdb53ebee923b420f1520aee`; integrated closure base `ce1cc235057a5de3d71fefbcee32e5617197cbb0`; closure `373092e98fef4d291365462baaa7f1ea2a8f065b`; no runtime implementation |

## Completed

- BC-041 and BC-041-C1 closed together after the correction lineage through
  `204a229e2c01b255f1a940129cb724fa33fb4755` was integrated on current `main`
  at `131a527a8fef1f42df327443c9966c9e2f66f528`. Claude's final review
  `f0998f78aaada899a16d4413170ef3689f04fe28` is `approve-with-notes` with zero
  blockers; its exact record was imported at
  `3e77111b6d86879f591c7ab8c52a571c51e7c48e`. The original BC-041
  `return-for-correction` review remains immutable. B-1, B-1', and B-1″ are
  resolved; SUR-001 is resolved at the minimum Phase 1 contract level;
  technical readiness is green with no actual blockers. Python Runtime Phase 1
  remains unstarted and unauthorized, and automatic start is prohibited.
- BC-040 — One-Blu Portability and Python Runtime Readiness closed after
  substantive specification `8516bd6845edaa3ef9b18077d91853ccc21e3c3b`,
  metadata `dc5429cabf03aff4ea8b383cbc1290789c370ebb`, work integration
  `a24cffc2fb3b3b7ffe3e0291915d0319a4db3e5f`, Claude review
  `127ae61e296fe0d07072e1320dec8ca8c4b1dfed`, and reviewed integration base
  `8801ae138deb0261deff47d02269c7a16773c892`. Claude returned
  `approve-with-notes` with zero blocking findings. One canon serves the
  required ChatGPT Custom GPT and Python/LM Studio deployments; Codex remains
  optional best effort. The final readiness result remains
  `not_ready_for_python_phase1`, with SUR-001 as the sole actual blocker. No
  production runtime, LM Studio provider, Local Mirror provider, or protected
  security implementation was introduced. Substantive administrative closure:
  `d78f58972327434c83d7e79a2cb9372e487a9629`.
- BC-030 — Local Mirror Continuity Schema and Lifecycle closed at the
  specification boundary after substantive work
  `6812513d10eeb69f1e5b477617ffdccc52e5067b`, metadata
  `4c4ef004aef2d93937de3fdb4bbbdeae4f2d9843`, work integration
  `d679357426899c660d905326ef345d7229974b0b`, and Claude review
  `adda640c05035d14057a22fb1ac85c19c326fe4f` returned
  `approve-with-notes` with zero blockers. SUR-007 is resolved at the generic
  continuity-contract level; SUR-011 and all provider implementation inputs
  remain unresolved. Claude N1-N8 and instance-level schema-conformance notes
  carry forward as implementation-readiness inputs. Closure introduced no
  provider, successor Python runtime, LM Studio adapter, Chat/Codex adapter
  implementation, or PASS/SkillForge work. Reviewed integration base:
  `c76843e82a42ab091810c110e8c01a4e32ed311e`; closure commit
  `a77393d6fc63e644f57a70992af6fec050a2e802`.
- BC-020-C1 — Scheduling Capability Evidence Correction closed after
  substantive correction `b770be849d625e924f7e65cae4efb8894a7e4c23`, metadata
  `8eb29165d5d59b99ccaa3b06fe6d8613dcaa11e2`, and Claude re-review
  `b51912a655d3f895651eb0bdbbe0c41ba1e7f132` returned
  `approve-with-notes` with BF-1 resolved and zero blocking findings.
  Integrated closure base: `642a5df7340c4f87ac723bffb4d308fef09bf2b2`;
  closure commit: `1e42c5dd2ee049fa5ebe4280692d1caecc0a3533`.
- BC-020 — Chat and Codex Capability Adapter Contracts closed after the bounded
  BC-020-C1 correction and final semantic re-review. Original work
  `09c484418e51365cf9b156cf304eebae7fecde5d`, metadata
  `ccf3206ad033d588246e09001d47ddce3ac50a31`, and original Claude review
  `370278cd91fd9ecca2c64cd0953cae7ed63c4d16` remain preserved with the original
  `return-for-correction` disposition. Closure is administrative and introduces
  no adapter or successor runtime implementation. Closure commit:
  `1e42c5dd2ee049fa5ebe4280692d1caecc0a3533`.
- BC-018-C1 — Cross-Turn Security State Correction closed after Claude's
  re-review at `1f440546a076c9359afaf5e832882e588d71dfa6`
  approved with notes and no blocking findings. BF-1, BF-2, and BF-3 are
  resolved. SUR-011 remains future security-policy input and SUR-012 remains a
  blocking BC-020 host-evidence input. Integrated closure base:
  `ce1cc235057a5de3d71fefbcee32e5617197cbb0`.
- BC-018 — Successor Kernel Boundary Specification closed after BC-018-C1 and
  the independent semantic re-review. The original Claude review at
  `7796c7e738e0ff66b677c79314b80cf2bbb09a63` remains
  `return-for-correction` as immutable history. Final disposition is
  `approve-with-notes` with zero blocking findings. Closure changed no
  architecture contract and authorized no runtime implementation.
- BC-017-C1 — Historical Archaeology Review Corrections closed after Claude's
  re-review at `bea9463f0dbbae1c3944c5f44a7843c757d7f0bb` resolved B-01,
  B-02, and B-03 and returned `approve-with-notes` with no blocking findings.
  Correction work commit: `87c4e49333d30a471a00483fc1384e1918626ee1`;
  metadata commit: `fd7f1707e242aa0e9621ab9f7293364860cab21d`.
- BC-017 — Historical Behavioral Archaeology closed after the BC-017-C1
  correction and independent semantic re-review. Original work commit:
  `dcad56f7d50252ab70e993aef7a763ed2bd3617b`; metadata commit:
  `01a004835dbd3e3e2702ba34dcc06f81f2a600f8`; owner-observation correction:
  `110ce2e82e39f60fa2158494888359389b70600a`; original Claude review:
  `c323cff06c9f111408f4a416817d78fc0f3e2d2b`. The original
  `return-for-correction` decision remains preserved as audit history. Closure
  performed no new archaeology, archive import, or runtime implementation.
- BC-016 — Historical Archive Inventory Integration closed after Claude's
  `approve-with-notes` review with no blocking findings. Inventory work commit:
  `9f6d705723a3ee6d26e47b80c634bc3c58495c83`; metadata commit:
  `2685dd5a3d4e81498e5b72cc83fad5d664a4d76a`; Claude review commit:
  `1e7796191360cb5b81ab70a716ffda1e97f77264`. All non-blocking findings NB-1
  through NB-10 remain preserved and carried forward. The closure performed no
  archive import, behavioral archaeology, or runtime implementation.
- BC-015 — Runtime viability audit closed after Claude's
  `approve-with-notes` review with no blocking findings. Audit work commit:
  `9936cc4be2f7f397deebccdf7400e8b7b774df08`; review commit: `4ed7626`;
  integrated reviewed state before closure:
  `1f07333457b18895fbb04d5c776e3259d870f2f6`. The audit classified current
  viability and did not implement a runtime.
- BC-010 — Runtime contract extraction closed after corrective assignments
  BC-010-C1 and BC-010-C2; integrated reviewed state before closure:
  `8a37ae3c62829f16f949f5896d2bef0542721565`.
- BC-010-C1 — Corrections closed after BC-010-C2 repaired the remaining OPSEC
  classification issue; integrated reviewed state before closure:
  `8a37ae3c62829f16f949f5896d2bef0542721565`.
- BC-010-C2 — OPSEC route classification repair closed after Claude's
  `approve-with-notes` review with no blockers; integrated reviewed state before
  closure: `8a37ae3c62829f16f949f5896d2bef0542721565`.
- BC-001 — Blu Core bootstrap authority and CTS golden source verified at `7aed76e`.
- Governance, source authority, migration boundaries, golden CTS runtime, validation evidence, and completion records are present.
- All eight golden checksums passed.
- All repository manifest checksums passed.
- All seven extracted runtime files are byte-identical to their ZIP members.
- `git diff --check` passed.
- Working tree was clean and synchronized with `origin/main`.
- The documented four-commit bootstrap plan versus two-commit live history is a non-blocking provenance discrepancy. History was not rewritten.

## BC-010 — Golden Runtime Contract Extraction

### Assignment identity

- **Implementation owner:** Codex
- **Semantic reviewer:** Claude
- **Project Lead / integration reviewer:** Blu
- **Project Owner / final authority:** Dad
- **Exact base commit:** `7aed76e`
- **Starting branch:** clean `main` at `7aed76e`
- **Recommended work branch:** `bc-010-runtime-contracts`
- **Status at handoff:** `ready`

### Amendment — commit identity bookkeeping

- **Approved by:** Dad, by explicit instruction on 2026-08-05.
- **Defective original requirement:** BC-010 required one implementation commit
  while also requiring that commit's exact SHA to be recorded inside a tracked
  file in the same commit.
- **Why defective:** A Git commit cannot contain its own final hash. Changing
  the recorded hash changes the tree and therefore produces a different commit
  hash.
- **Authorized method:** Create one reviewable implementation commit, capture
  its exact SHA, then create one metadata-only commit that records the work SHA
  in the assignment handoff and this index.
- **Review target:** Claude's semantic review targets the implementation commit,
  not the metadata-only record commit.
- **Metadata boundary:** The record commit must not modify
  `contracts/runtime/**`, `tools/**`, `tests/**`, or `kernel/golden/**`.

### Objective

Extract the current CTS Markdown runtime into machine-readable contracts without
changing, replacing, normalizing, or reinterpreting the golden runtime.

BC-010 documents what Blu v0.22.0 currently declares. It does not implement the
future Python runtime and does not change current behavior.

### Required source order

Before changing files:

1. Read `AGENTS.md`.
2. Read `CODEX.md`.
3. Read `docs/dev/docs_index.md`.
4. Read `docs/dev/assistant_coding_behavior.md`.
5. Read this assignment.
6. Read:
   - `docs/architecture/current_runtime.md`
   - `docs/architecture/migration_centerline.md`
   - `docs/sources/authority_map.md`
   - `docs/domains/runtime/decisions.md`
   - `docs/domains/runtime/worklog.md`
   - `docs/domains/runtime/failures.md`
   - `docs/domains/runtime/next_steps.md`
7. Verify that `HEAD` descends from exact base `7aed76e`.
8. Verify the golden checksums before extraction.

### Authoritative inputs

Only the following files define the extraction source:

```text
kernel/golden/v0.22.0/00_Instructions.md
kernel/golden/v0.22.0/01_Persona.md
kernel/golden/v0.22.0/02_Operations_Law.md
kernel/golden/v0.22.0/03_Exec.md
kernel/golden/v0.22.0/04_Exec_Library.md
kernel/golden/v0.22.0/05_Commands.md
kernel/golden/v0.22.0/06_Programs.md
```

Project governance and architecture documents may constrain the extraction but
must not be used to invent runtime declarations absent from the golden files.

### Allowed collision domain

BC-010 may create or modify only:

```text
contracts/runtime/**
tools/validate_runtime_contracts.py
tests/contracts/**
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
```

`tools/validate_runtime_contracts.py`, if created, is contract-validation tooling.
It is not Blu runtime implementation.

Any additional file requires assignment amendment by Blu or Dad before editing.

### Protected and prohibited areas

Do not modify:

```text
kernel/golden/**
AGENTS.md
CLAUDE.md
CODEX.md
config/source_authority.json
docs/architecture/**
docs/sources/**
```

Do not:

- rewrite Persona or Operations Law;
- infer missing components into existence;
- merge duplicate or conflicting declarations silently;
- normalize source wording into a different behavioral rule;
- import Alice, SkillForge, Local Mirror, or `Blu_KB_Preview` content into the CTS contracts;
- implement routing, reminders, memory persistence, Local Mirror, PASS, or adapters;
- claim behavioral parity from schema validity alone;
- edit Git history or force-push.

### Required deliverables

Create a documented contract set under `contracts/runtime/` containing at least:

1. `README.md`
   - purpose and non-authority boundary;
   - golden source list;
   - extraction rules;
   - explanation that contracts describe the current Markdown runtime.

2. `source_map.json`
   - each extracted object mapped to its golden file and source section;
   - classification as explicit declaration, unresolved conflict, or intentionally unmodeled prose;
   - no invented source claims.

3. `component_registry.json`
   - declared component, service, library, Program, command owner, and runtime owner IDs;
   - status and ownership;
   - dependencies;
   - declared inputs and outputs when present;
   - source provenance;
   - unresolved or externally referenced components clearly marked as declared-but-not-implemented.

4. `route_registry.json`
   - mandatory restraint order;
   - RuntimeGate ingress order;
   - live slash-command routes;
   - ordinary-conversation fallback lane as declared by the golden runtime;
   - active, deferred, and unavailable route surfaces;
   - one-owner constraints.

5. JSON Schemas under `contracts/runtime/schemas/` for:
   - task packet;
   - ScopeLock;
   - terminal packet;
   - capability report;
   - current-turn execution receipt.

6. `parity_matrix.json`
   - behavioral requirements and test cases for:
     - ordinary conversation;
     - command routing;
     - one-owner enforcement;
     - restraint ordering;
     - ScopeLock containment;
     - fail-closed behavior;
     - artifact proof;
     - source and capability honesty;
     - Persona non-routing boundary;
     - Operations truth and anti-drift boundary;
     - active versus deferred commands;
     - hosted single-turn limitations.

7. `unresolved_register.json`
   - conflicts, underspecified fields, referenced-but-unimplemented owners, and
     declarations that cannot be converted deterministically without a later
     design decision;
   - each item must preserve source provenance and must not resolve itself.

8. Contract validation:
   - every JSON file parses;
   - registry IDs are unique within their declared namespace;
   - command stems have no duplicate public owner;
   - all source-map targets exist;
   - required schema files exist;
   - validator fails when a required contract file is missing or malformed.

9. Runtime-domain continuity updates:
   - work performed and files changed in `worklog.md`;
   - failed or unsafe extraction paths in `failures.md`;
   - the next safe step in `next_steps.md`.

### Extraction rules

- Preserve CTS terminology where it is structurally usable.
- Separate explicit source declaration from extraction inference.
- When declarations conflict, preserve the conflict in `unresolved_register.json`.
- When prose is expressive or semantic rather than deterministic, leave it
  model-facing and record why it was not reduced to a runtime field.
- Persona and Operations remain authoritative model-facing sources.
- Contract files are downstream representations and never outrank the CTS files.
- A missing implementation is recorded as missing; it is not created by registry entry.
- Do not treat a Markdown declaration as proof that a host capability exists.
- Keep the smallest schema that accurately represents the declared contract.

### Required checks

Run and record exact results for:

```text
git status --short
git rev-parse HEAD
git merge-base --is-ancestor 7aed76e HEAD
git diff --check
sha256sum -c kernel/golden/v0.22.0/SHA256SUMS
git diff --exit-code 7aed76e -- kernel/golden/v0.22.0
```

Also run the contract validator and JSON parse/schema checks introduced by the
assignment.

On Windows, an equivalent checksum command is acceptable, but the exact command
and output must be recorded.

### Completion conditions

Move BC-010 from `active` to `review` only when:

- all required deliverables exist;
- protected golden files remain byte-identical;
- all validation checks pass;
- runtime-domain logs are updated;
- the work is committed as one reviewable, revertible commit;
- the exact commit ID is recorded in this file;
- no behavior implementation was added.

### Implementation receipt

- **Work commit:** `40138b6e16f28c01904aae97158878468ee47ad0`
- **Review status:** `review`
- **Semantic review target:** `40138b6e16f28c01904aae97158878468ee47ad0`
- **Handoff:** `docs/domains/runtime/assignments/BC-010/handoff.md`
- **Record method:** authorized metadata-only follow-up commit under the
  amendment above
- **Push status:** not pushed

### Handoff format

Codex must report:

```text
Assignment: BC-010
Base commit:
Work commit:
Files changed:
Contracts created:
Validation commands:
Validation results:
Golden checksum result:
Known unresolved items:
Known risks:
Recommended semantic-review focus:
Working tree status:
Push status:
```

Claude then performs a read-only semantic review against the golden CTS source.
Claude does not modify the BC-010 implementation branch unless Blu or Dad issues
a separate correction assignment.

## Standing guardrails

- Bootstrap checks: `git diff --check` and
  `sha256sum -c kernel/golden/v0.22.0/SHA256SUMS`.
- Do not touch `kernel/golden/`.
- Blu's current CTS deployment is one GPT deployment instruction plus six
  kernel/runtime capsules.
- No Python Blu runtime exists yet.
- Contract-validation tooling is not runtime implementation.
- Do not restore legacy `library/` SkillForge routing.
- Do not begin BC-030 before its packet is approved and its base is named.
