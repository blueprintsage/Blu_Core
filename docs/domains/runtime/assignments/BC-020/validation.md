# BC-020 — Validation Record

status: review
owner: Codex
last_reviewed: 2026-08-08

## Environment

- Host: Codex desktop on Windows, current local surface only
- Python: 3.12.10
- Git: 2.52.0.windows.1
- PowerShell: 5.1.19041.6456
- Observed surface: `codex_desktop_local_windows`, local checkout,
  `workspace-write`, `auto_review`, restricted network, workspace root
  `D:/Repos/Blu_Core`
- Standard-library-only BC-020 validator/tests; no new dependency
- Known limitation: contract validation proves structure and guardrails, not
  live Chat/Codex capability or security-grade provider behavior.

## Commands and results

### Complete validator and unit-test stack

```text
git diff --cached --check
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
python tools/validate_viability_audit.py
python -m unittest discover -s tests/viability -p "test_*.py"
python tools/validate_historical_archive_inventory.py
python -m unittest discover -s tests/historical_archives -p "test_*.py"
python tools/validate_historical_behavioral_archaeology.py
python -m unittest discover -s tests/historical_archaeology -p "test_*.py"
python tools/validate_successor_kernel_spec.py
python -m unittest discover -s tests/successor_kernel -p "test_*.py"
python tools/validate_host_adapter_contracts.py
python -m unittest discover -s tests/host_adapters -p "test_*.py"
```

Result:

```text
git diff --cached --check: passed
runtime contract validator: passed
runtime contract tests: Ran 21, OK
viability validator: passed
viability tests: Ran 9, OK
historical archive validator: passed
historical archive tests: Ran 12, OK
historical archaeology validator: passed
historical archaeology tests: Ran 18, OK
successor kernel validator: passed
successor kernel tests: Ran 40, OK
host adapter validator: passed
host adapter tests: Ran 25, OK
```

### Contract and evidence counts

```text
common contract JSON files: 6
adapter JSON files: 14
Chat capabilities: 52
Chat statuses: documented_possible 18; unknown 33; not_applicable 1
Chat evidence entries: 9
Codex capabilities: 52
Codex statuses: verified_available 27; verified_unavailable 6;
  documented_possible 4; unknown 14; not_applicable 1
Codex evidence entries: 21
security evidence rows: 15
successor components: 7
successor packets: 8
successor interfaces: 9
```

### Canonical manifest

Generated from staged Git bytes using `git ls-files` and `git show :<path>`,
then verified every SHA-256 against the staged blob bytes and compared path sets.

```text
manifest entries: 216
tracked expected (self-excluding): 216
missing: 0
extra: 0
mismatches: 0
```

### Scope, implementation, and publication checks

```text
git diff --name-only d4157e79fc7e2df6e1bd53b589cabfa19cd7238f --
  kernel/golden/v0.22.0 contracts/runtime contracts/successor
  docs/architecture/successor_*.md docs/sources/historical_archives
```

Result:

```text
staged changed files: 32, all inside the authorized collision domain
protected changed paths: 0
contracts/successor changed paths: 0
current CTS changed paths: 0
modern PASS/SkillForge changed paths: 0
adapter runtime source files under adapters/: 0
credential-assignment pattern hits in staged diff: 0
private attachment-path hits in staged diff: 0
```

## Golden-source verification

PowerShell parsed `kernel/golden/v0.22.0/SHA256SUMS` and recomputed SHA-256 for
every referenced file:

```text
golden checked: 8
golden failed: 0
```

The exact-base protected-path diff is empty. `contracts/successor/**` and the
seven-component/eight-packet/nine-interface generic design are unchanged.

## Negative tests

The 25-test BC-020 suite includes canonical success and negative cases for:

- missing/malformed files and duplicate IDs;
- unknown evidence refs and explicit unknown capability support;
- documentary evidence promoted to current availability;
- Host Adapter production of `TurnRequest` or ownership of Auth policy;
- product sign-in or host approval promoted to Blu authorization;
- conversation history or request-ref equality used as security binding;
- security grade without rollback evidence;
- mutable or rollback-prone attempt state;
- exact current time without a provider receipt;
- side-effect success without a receipt;
- incomplete filesystem/network scopes;
- unscoped/stale local probes;
- SUR-011 resolved by adapter policy or missing SUR-012 disposition;
- host-session state promoted to durability; and
- runtime adapter source under `adapters/`.

## Failed attempts

The safe client-version probe located the packaged Codex executable but direct
execution returned access denied. `client_version` therefore remains unknown;
the executable path and package directory are not used as a manufactured
version claim.

The first focused validator run reported one wording mismatch in the side-effect
rule (`No external side effect` versus the validator's explicit `not` token),
causing two canonical test failures. The normative rule was rewritten without
changing semantics to state that an external side effect "is not completed"
without a provider receipt. The validator and all 25 tests then passed.

## Validation boundary

Passing checks will establish only that the specification artifacts are
internally coherent, evidence-linked, secret-safe by declared checks, and do
not alter protected generic/current-runtime sources. They cannot prove a
future adapter implementation or provider guarantee.

The final clean-tree, exact commit, and push receipts are recorded after Git
operations and are not inferred from this pre-commit validation.
