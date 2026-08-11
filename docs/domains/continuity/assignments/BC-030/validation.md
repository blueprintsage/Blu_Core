# BC-030 — Validation Record

status: done
owner: Codex
last_reviewed: 2026-08-11

## Environment

- Host: Windows, PowerShell
- Language/runtime versions: Python 3.12.10; Git and PowerShell repository tools
- Optional dependencies available: none required by BC-030 validator
- Known limitations: no Local Mirror provider was implemented or executed

## Commands and results

### Base and branch

```text
git rev-parse HEAD
git branch --show-current
git status --short
```

Result before work: exact authorized base
`a5f149355bd68b2aea1695e5f25ec60a2cb88b0c`, branch
`bc-030-local-mirror-continuity`, clean tree. BC-020 and BC-020-C1 were `done`;
BC-030 was `spec-needed`.

### Reference identity

```text
Get-FileHash <supplied Local Mirror/MPLPB archive> -Algorithm SHA256
```

Result: `77745FA1FA726859EDD0CAF496241C2BA930E653A86A23BA0B2792FF9E8717F2`,
matching `config/source_authority.json`.

### Required validators and tests

```text
git diff --cached --check
git diff --check
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
python tools/validate_continuity_contracts.py
python -m unittest discover -s tests/continuity -p "test_*.py"
```

Result:

```text
staged and working-tree diff checks: passed
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
host adapter tests: Ran 34, OK
continuity validator: passed
continuity tests: Ran 34, OK
```

### Contract and scope counts

```text
successor components: 7
successor packets: 8
successor interfaces: 9
continuity JSON Schemas: 5
continuity focused tests: 34
changed files: 26
changed Python files: 2 (validator and tests only)
protected successor/current-runtime/adapter/architecture changes: 0
provider/runtime/LM Studio implementation files: 0
PASS/SkillForge path changes: 0
```

### Canonical manifest

Generated from staged Git blob bytes using `git ls-files` and
`git show :<path>`, then independently compared with the staged set and hashes.

```text
manifest entries: 239
tracked expected, self-excluding: 239
missing: 0
extra: 0
mismatches: 0
```

## Golden-source verification

Direct SHA-256 verification against
`kernel/golden/v0.22.0/SHA256SUMS`: 8/8 passed.

Exact-base diff over the golden kernel, current runtime contracts, generic
successor registries, adapters, architecture documents, and source-authority
configuration: empty.

## Negative tests

The 34 focused tests prove that validation rejects, among other cases:

- an eighth component, ninth packet, or tenth interface;
- bare `session` and new continuity packets;
- missing stable record/version identity;
- receipt-stage promotion, model/context self-certification, or failed-write
  state transition;
- unbounded or cross-scope retrieval;
- inferred provider availability;
- silent conflict overwrite, history deletion, or corruption repair;
- incomplete rehydration and `host_session`/`durable_external` conflation;
- weakened rollback/replay evidence or ordinary receipts promoted to protected
  authorization evidence;
- resolved SUR-011, false Local Mirror implementation/conformance, absolute path
  portability, changed archive identity, and executable implementation files.

## Failed attempts

- The initially guessed helper `python tools/verify_checksums.py` did not exist.
  The assignment uses direct SHA-256 verification against the canonical golden
  `SHA256SUMS` file instead.
- The first contract placement under `contracts/successor/continuity/` passed
  BC-030-focused checks but correctly failed the BC-020 regression validator,
  which protects the entire generic `contracts/successor/**` tree. The files were
  moved to the top-level `continuity/` specialization namespace, analogous to
  `adapters/`; all generic successor files remain unchanged and the full suite
  then passed.

## Validation boundary

These checks prove repository structure, finite vocabularies, cross-contract
invariants, source identity, protected-path isolation, and regression stability.
They do not prove a Local Mirror provider implementation, a durable write,
crash consistency, live availability, protected authorization capability,
runtime behavior, or model behavioral parity.

## Commit identity

- Substantive specification commit:
  `6812513d10eeb69f1e5b477617ffdccc52e5067b`
- Metadata method: this follow-up commit records the substantive SHA without
  attempting the impossible operation of embedding a commit's own final SHA in
  its tree.

## Final closure validation — 2026-08-11

Commands were rerun from `bc-030-closure` at exact integrated base
`c76843e82a42ab091810c110e8c01a4e32ed311e` after the authorized closure edits.

```text
git diff --check
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
python tools/validate_continuity_contracts.py
python -m unittest discover -s tests/continuity -p "test_*.py"
```

Results:

```text
git diff --check: passed
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
host adapter validator: one expected authorized-scope finding
  (contracts/successor/unresolved_register.json changed from the BC-020 base)
host adapter tests: Ran 34, OK
continuity validator: one expected authorized-scope finding
  (contracts/successor/unresolved_register.json changed from the BC-030 base)
continuity tests: Ran 34, OK
```

Both direct validator commands completed their contract checks but returned exit
1 because their historical Git-scope guards classify every change to
`contracts/successor/unresolved_register.json` as protected. This closure
explicitly authorizes the SUR-007-only reconciliation and explicitly excludes a
validator change, so the guards were left unchanged. Running each validator
against the identical staged tree without repository-history scope enforcement
passed, confirming that the one direct-command finding is the authorized path
change rather than a contract-content failure. The direct exit-1 results remain
the authoritative command receipts; they are not reported as passing.

Additional closure results:

```text
golden CTS SHA-256: 8/8 passed
canonical manifest: 239 entries; 239 tracked expected; 0 missing; 0 extra;
  0 duplicate; 0 mismatch against staged Git blob bytes
successor components: 7
successor packets: 8
successor interfaces: 9
state lifetimes: none, turn, host_session, durable_external
host_session != durable_external: preserved
SUR-007: resolved_at_generic_continuity_contract_level
SUR-011: unresolved_security_policy_input
Claude review blob changes: 0
golden kernel changes: 0
current CTS runtime changes: 0
provider/runtime/LM Studio/Chat/Codex implementation files added: 0
PASS/SkillForge path changes: 0
```

The manifest was regenerated from the canonical staged Git blob view, not the
CRLF-materialized working-tree bytes described in Claude note N11.

These checks establish specification consistency and closure bookkeeping only.
They do not prove live durability, provider availability, a durable write,
crash consistency, protected durable authorization, or runtime behavior.

The substantive closure commit is recorded by the metadata-only follow-up; the
metadata commit cannot record its own final identity.
