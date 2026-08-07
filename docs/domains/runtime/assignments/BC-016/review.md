# BC-016 — Review Record

status: review
owner: Claude
last_reviewed: 2026-08-07
reviewer: Claude
review_type: read-only semantic review
recommended_disposition: approve-with-notes

## Assignment reviewed

BC-016 — Historical Archive Inventory Integration (domain: runtime).

- Project Owner and final authority: Dad
- Project Lead and integration reviewer: Blu
- Implementation owner and Git steward: Codex
- Semantic reviewer: Claude

## Commit identity

```text
BC-016 exact base:
fdb6c7e150d3717172e08a1bc349a428187df45a

Inventory work commit (semantic review target):
9f6d705723a3ee6d26e47b80c634bc3c58495c83

Metadata record commit (review-branch base):
2685dd5a3d4e81498e5b72cc83fad5d664a4d76a

Review branch:
bc-016-semantic-review
```

The review branch was created detached from `2685dd5`, not from `main`. The
working tree was clean at branch creation and remained clean until this record
was written. Both the base and the work commit are ancestors of the metadata
commit; no history was rewritten.

## Commit-boundary verification

The metadata commit did not alter the substantive surface:

```text
git diff --exit-code 9f6d705 2685dd5 -- \
  docs/sources/historical_archives docs/sources/external_inputs.md \
  tools tests kernel/golden contracts/runtime \
  docs/domains/runtime/viability docs/architecture config
```

Exit 0. The metadata commit touched exactly the three expected paths:

```text
MANIFEST.sha256
docs/domains/runtime/assignments/BC-016/handoff.md
docs/worklogs/assignments.md
```

The work commit changed 20 paths, all inside the BC-016 collision domain.
`git diff --check` is clean. The metadata commit's inability to record its own
SHA is treated as the stated self-reference boundary, not a defect.

## Source records actually inspected

Governance and standard: `AGENTS.md`, `CLAUDE.md`, `docs/dev/docs_index.md`,
`docs/dev/assistant_coding_behavior.md`,
`docs/dev/domain_assignment_record_standard.md`, `docs/worklogs/assignments.md`.

Architecture and source authority: `docs/architecture/current_runtime.md`,
`docs/architecture/migration_centerline.md`, `docs/sources/authority_map.md`,
`docs/sources/cts_source_roles.md`, `docs/sources/external_inputs.md`,
`docs/sources/migration_memcap_2026-08-05.md`.

Runtime continuity: `index.md`, `decisions.md`, `worklog.md`, `failures.md`,
`next_steps.md`, and the BC-015 review record.

BC-016 surface: `assignment.md` (all 1221 lines), `handoff.md`, `validation.md`,
the prior pending `review.md`, and the complete
`docs/sources/historical_archives/` set — `README.md`,
`kernel_archive_inventory.json` (4.9 MB, 249 records), the 249-row CSV,
`snapshot_receipt.json`, `reconciliation_report.md`,
`milestone_recommendations.md`, `discovery_receipt.md` — plus
`tools/validate_historical_archive_inventory.py` and
`tests/historical_archives/test_validate_historical_archive_inventory.py`.

Cross-checked against the immutable CTS in `kernel/golden/v0.22.0/`, including a
direct byte-hash of the golden CTS ZIP.

## Inventory counts independently verified

Recomputed from `kernel_archive_inventory.json`, not read from `handoff.md`,
`validation.md`, or `discovery_receipt.md`:

| Measure | Recount | Reported | Match |
|---|---:|---:|:--:|
| Canonical inventory records | 249 | 249 | yes |
| Unique `archive_id` values | 249 | — | yes |
| `archive_file` records | 244 | 244 | yes |
| `current_branch_file_set` records | 3 | 3 | yes |
| `historical_source_folder` records | 2 | 2 | yes |
| Available / readable | 242 | 242 | yes |
| `unsupported_format` / `not_tested` | 7 | 7 | yes |
| Exact duplicate groups | 2 | 2 | yes |
| Milestones | 8 | 8 | yes |
| CSV data rows | 249 | 249 | yes |
| Manifest entries | 150 | 150 | yes |

Identifier space: `BLU-HIST-0001` through `BLU-HIST-0246` contiguous with no
gaps, plus `BLU-BRANCH-DEV`, `BLU-BRANCH-PREVIEW`, `BLU-BRANCH-RELEASE`. The 246
`BLU-HIST` records decompose exactly as 244 `archive_file` + 2
`historical_source_folder`, so no inventory record is missing or duplicated.

Every record carries the full required field set (verified: one identical key
set across all 249), a declared and resolvable `source_root_id`, and a
normalized relative path. All 249 paths are non-absolute, contain no `..`
traversal, use forward slashes only, and root at exactly `DevBuild`, `Preview`,
or `Release`.

The two `historical_source_folder` records are genuinely distinct sources, not
accidental duplicates of the branch file sets: `BLU-HIST-0014`
(`Release/!Archives/v0.6.x`) and `BLU-HIST-0090`
(`Release/!Archives/v0.9.0/2026-03-20_1252_CDT_Blu_PASS_RC_Stabilization_Patch`)
sit under `!Archives`, carry different hashes, and belong to different eras than
`DevBuild`, `Preview`, and `Release`.

The three branch file sets explicitly disclaim current authority in their own
notes: "The branch label is historical source organization and does not mean
current Blu runtime authority."

## Reconciliation totals independently verified

| Status | Recount | Reported | Match |
|---|---:|---:|:--:|
| `matched_path_and_hash` | 496 | 496 | yes |
| `matched_hash_different_path` | 2 | 2 | yes |
| `live_directory_only` | 2 | 2 | yes |
| `snapshot_only` | 0 | 0 | yes |
| `inventory_only` | 0 | 0 | yes |
| `hash_mismatch` | 0 | 0 | yes |
| `unavailable_for_verification` | 0 | 0 | yes |
| Total entries | 500 | — | — |

The 496 is not a single-axis figure and should not be read as one. Decomposed by
identity pair:

```text
external_discovery_output vs dad_kernel_root  matched_path_and_hash   247
external_discovery_output vs dad_kernel_root  live_directory_only       2
blu_kernel_snapshot       vs dad_kernel_root  matched_path_and_hash   249
dad_kernel_root           vs dad_kernel_root  matched_hash_diff_path    2
                                                              total   500
```

Two distinct comparison axes each cover the full inventory. The discovery axis
accounts for all 249 records as 247 matches plus 2 live-only; the snapshot axis
matches all 249; the 2 remaining entries are the internal duplicate pairs. 247 +
249 = 496.

The two `live_directory_only` entries are exactly `BLU-BRANCH-PREVIEW` (REC-0003)
and `BLU-BRANCH-RELEASE` (REC-0005), as expected — discovery omitted them
because their normalized content matched recorded archives, while BC-016
requires all three branch-root file sets. `BLU-BRANCH-DEV` was present in
discovery and reconciles as `matched_path_and_hash`.

Every `inventory_archive_id` resolves to a real record (0 invalid). Every
`left_source_identity` and `right_source_identity` uses a declared identity. No
source pair is unintentionally double-counted: the two axes are deliberately
distinct comparisons, not repeated ones. Both
`matched_hash_different_path` entries are backed by actually equal content
hashes (verified below). No authority winner is selected anywhere, and with zero
mismatches there was no occasion to.

## Snapshot verification assessment

The `independently_verified` / `verified_by: Codex` claim is well supported,
with one honest limit.

`snapshot_receipt.json` and the canonical `snapshots[0]` object are fully
consistent — I compared every key and found no divergence.

Identity separation is correct and explicit:

```text
outer ZIP SHA-256      0195ab2623e2bdd9d2da5b8f18170f238bb4dbd5df489e543589de112eba6613
payload manifest       38bc729f012243446ca29c3aed31802f2ec8d77473487cbd45a5bb710e3c88ff
live-root manifest     38bc729f012243446ca29c3aed31802f2ec8d77473487cbd45a5bb710e3c88ff
```

The outer container hash differs from both manifests; the two manifests match
each other, which is the actual payload-agreement claim. The receipt's own
limitations state that the outer hash "is not interchangeable with a live-folder
or payload-manifest hash," that "path-and-hash equality proves source identity
only; it does not prove historical behavior worked," and that the snapshot is
"recorded but not committed."

Evidence that Codex had the exact container rather than restating Blu's receipt:
`payload_manifest_sha256` and `live_root_manifest_sha256` are derived values that
do not appear in Blu's supplied receipt in the assignment packet, and the
manifest construction is documented in `discovery_receipt.md` (SHA-256 over
sorted UTF-8 relative-path, NUL, lowercase file SHA-256, LF records, applied
after removing the stable `Kernel/` wrapper). Those values cannot be produced
without processing the container. A further internal cross-check corroborates
it: the receipt's `nested_zip_files: 244` equals the 244 `archive_file`
inventory records exactly, and `zip_entries 302 − file_entries 279 = 23`
directory entries is coherent for the described tree.

All 279 live payload paths were compared to snapshot members with 0 live-only, 0
snapshot-only, and 0 mismatches, and `reconciliation_report.md` states the
completeness conclusion in exactly those terms.

Honest limit: I cannot reproduce the outer ZIP hash, because `Kernel.zip` is
correctly not committed. My verification establishes internal coherence,
identity separation, and derived-value corroboration — not an independent
recomputation of `0195ab26…`. Path-and-hash equality is nowhere used as evidence
of historical behavior or intent.

The snapshot was not committed: no `.zip`, `.7z`, `.tar`, `.tgz`, or `.rar` file
is tracked anywhere outside `kernel/golden/`.

## Authority-boundary assessment

Correct. All three declared source roots carry
`authority: non_authoritative_for_current_runtime`, and the validator enforces
that on every root. The four identities remain distinct and are never
substituted: `dad_kernel_root` (live historical tree), `blu_kernel_snapshot`
(outer container), `external_discovery_output` (generated inputs, source role
`generated_inventory_input`), and `kernel/golden/v0.22.0` (untouched current
CTS).

Hash-identity separation is enforced structurally through `sha256_type`: 244
records carry `archive_file_sha256` and 5 carry `folder_manifest_sha256`, with
`content_manifest_sha256` held as a separate field. The cross-tabulation is
clean — every `archive_file` uses a container hash, every file-set and folder
record uses a manifest hash. `README.md` names all five identities and states
they "are never substituted for one another."

BC-016 stayed inside its scope: identity integration, sanitization, checksum and
structural inventory, duplicate grouping, reconciliation, milestone
recommendation, static validation, and documentation. It did not conclude that
any historical feature worked, did not alter BC-015 classifications, did not
select successor architecture, did not restore anything, and did not modify the
current CTS.

## Privacy and path-sanitization assessment

Clean. This was the highest blocking risk and I did not rely on the validator's
regex.

I walked every nested string value in `kernel_archive_inventory.json` and
`snapshot_receipt.json` recursively against ten independent pattern families —
Windows drive paths, UNC prefixes, extended-length (`\\?\`) paths, POSIX
absolute and home prefixes, `users`/`home` segments, `file://` URIs, environment
home tokens (`%USERPROFILE%`, `$HOME`, `~/`), Windows special folders (AppData,
OneDrive, ProgramData, Program Files), remote-session markers, and placeholder
strings. **Zero hits in every category.**

I separately grepped the entire 20-file BC-016 diff — including notes, source
locators, CSV fields, reconciliation identities, milestone prose, and discovery
metadata — for the same families plus escaped backslashes. The only match in the
whole diff is a deliberately synthetic negative-test fixture at
`tests/historical_archives/test_validate_historical_archive_inventory.py:63`
(`"C:" + "\\Users\\example\\archive.zip"`), which uses a fictitious `example`
user and exists to prove the detector fires. That is not a leak.

CSV escaping preserves content exactly: no path or filename contains a comma or
quote, the longest path (142 characters) round-trips identically, and all paths
are ASCII.

## Duplicate and near-duplicate assessment

Verified independently and correct, with notably good discipline.

Both recorded groups check out fully: every member exists, every member's
`sha256` equals the group `sha256`, and every member record backlinks to its
group.

```text
DUP-001  02cf65e6…  BLU-HIST-0205, BLU-HIST-0210
DUP-002  d48a2995…  BLU-HIST-0122, BLU-HIST-0123
```

An independent scan for identical `archive_file_sha256` values across all 249
records finds **exactly two** collision groups — the two recorded. No exact
duplicate exists outside a recorded group, and no folder-manifest collisions
exist. Exactly 4 records carry a `duplicate_group`, matching 2 groups × 2
members. Differently named identical archives are retained as separate inventory
records rather than collapsed.

The strongest signal here: a scan at the **member-content** level finds six
`content_manifest_sha256` collision groups, but only the two container-hash
matches were assigned duplicate groups. The other four —
`BLU-BRANCH-PREVIEW`/`BLU-HIST-0170`, `BLU-BRANCH-RELEASE`/`BLU-HIST-0042`,
`BLU-HIST-0035`/`0036`, and `BLU-HIST-0172`/`0173` — are correctly described as
near-duplicate relationships and explicitly denied exact-duplicate status.
`reconciliation_report.md` states this directly and adds that "matching member
content does not establish identical container provenance or historical intent."
This is precisely the distinction the assignment required.

## Deflate64 and unreadable-source assessment

Correct and consistent across all seven records (`BLU-HIST-0045`, `0046`,
`0060`, `0074`, `0078`, `0081`, `0082`).

Each retains its archive-file SHA-256 and its central-directory listing
(`top_level_members` and `key_files_present`, both derivable from entry names
without decompression). None is labeled corrupt — `availability_status` is
`unsupported_format` and `integrity_status` is `not_tested`, applied uniformly,
and `reconciliation_report.md` states "No archive is classified corrupt or
permission-blocked."

Critically, no member-derived metric or capability claim was invented for them:
all seven have zero `notable_capability_markers` and zero `structural_metrics`.
They are seven of the nineteen records without metrics, and the other twelve are
`available` records that simply had none imported.

No milestone is one of the seven, so milestone selection does not depend on
unverified member content. The limitation is stated in the canonical
`limitations` block, in `README.md`, and in `reconciliation_report.md`.

## Date and version assessment

Honest, with one prose imprecision recorded as NB-5.

The fallback is self-documenting: the enum value is literally
`filesystem_last_write_time_utc_not_build_proof`, so the disclaimer travels with
every record rather than living only in a summary. 29 records carry it — 25
`archive_file`, 1 `historical_source_folder`, and 3 branch file sets. The "25"
figure in the reported results corresponds exactly to the `archive_file` subset;
both numbers are correct once the scope is stated.

Filename-derived dates are the dominant source (219 records
`archive_or_folder_filename`), consistent with the documented precedence of
filename over filesystem timestamp. The single
`archive_or_folder_filename_month_day_year` record is `BLU-HIST-0246`
(`Blu_v0_22_0_5_22_26_2104_CTS.zip` → 2026-05-22), given its own distinct
`date_source` label and `medium` version confidence rather than being folded in
with ordinary ISO-style filename parses. No timezone precision is invented; the
filename-derived dates are plain `YYYY-MM-DD` while only true filesystem
timestamps carry sub-second UTC offsets.

The two rejected ambiguous short-date parses are represented honestly in three
places: the canonical `limitations` block ("Two external short-date parses were
rejected as ambiguous task-file suffixes and replaced with explicitly labeled
filesystem timestamps"), `discovery_receipt.md`, and `failures.md` ("Numeric
filename suffixes are not automatically dates").

Imprecise versions are not presented as point releases: `v0.6.x` (1), `v0.8.x`
(3), and `v0.13.x` (3) retain the `.x` form. No milestone or report prose treats
a fallback date as authoritative chronology; `BLU-HIST-0020` and `BLU-HIST-0245`
display full timestamp strings in the milestone table, which are visibly
filesystem-derived and are not used to order any behavioral claim.

## Structural-metric assessment

The counting method is documented exactly as required, in `README.md`: Python
`splitlines()` for line count; ATX headings; declaration lines beginning with
module/component/service/library/program; RuntimeGate/gate tokens; exact `must`;
`validat*` forms; and `if|when|unless|otherwise` conditionals, all
case-insensitive.

Application is consistent: 230 of 249 records carry per-file metric entries
(1,565 files with `line_count`, `heading_count`, and `declared_module_count`;
420 files additionally carrying `gate_term_count`, `must_term_count`,
`validation_term_count`, and `conditional_term_count`, scoped to the
Exec-role files where those tokens are meaningful).

Metrics are consistently framed as indicators. `README.md` closes the section
with "Metrics are structural indicators only," and the canonical `limitations`
block and `failures.md` both deny that structure proves behavior, stability,
reliability, or recovery value. I found no passage anywhere in BC-016 that uses
a metric to assert a capability worked, a gate executed, a library was reliable,
or one architecture was behaviorally superior.

## Capability-marker assessment

Strong, and the security handling is the best part of this deliverable.

10,828 marker entries span 19 of the 23 listed categories. Every marker carries
`marker`, `exact_member_path`, `exact_heading_or_identifier`,
`evidence_classification`, and `occurrence_count`, so each is grounded in an
actual member path plus a heading, identifier, or documented structural
observation. `evidence_classification` distinguishes
`substantial_implementation_style_markdown` (7,499) from `merely_declared`
(3,329) — a presence gradient, not a behavior verdict.

Security handling: of 2,034 Auth and OPSEC markers, **1,321 have the identifier
redacted** (`exact_heading_or_identifier: null` plus
`identifier_redacted: "non-heading security-related excerpt omitted during
BC-016 integration"`), and the remaining 713 are Markdown headings such as
`## OPSEC / Privacy`. **Zero non-heading Auth or OPSEC identifiers were
retained.** No challenge answer, protected procedure, or protected render string
is present. This is exactly the discipline the assignment demanded, and it was
applied systematically rather than case by case.

Marker presence is never converted into `worked`, `stable`, `implemented`,
`reliable`, or `approved_for_recovery`. I checked prose as well as JSON keys:
every occurrence of those words across the seven historical-archive documents
and the four continuity documents is either a negation ("not evidence that a
feature worked or should be restored", "does not determine which historical
behaviors worked", "BC-016 performs no behavioral comparison"), an adjective for
the snapshot container ("stable outer `Kernel.zip`"), or a standard worklog
section heading. No narrative overstatement survives.

Four listed categories produced no markers: School Engine, plain Persona, plain
Mood, and Exec gates. Three are covered by adjacent categories actually used
(`PersonaLib`, `MoodLib`, and `gate_term_count` in the structural metrics). The
School Engine gap is real but consequence-free — `School_Engine` appears 89
times in the canonical JSON as a member filename in `top_level_members` and
`key_files_present`, so the material is inventoried and locatable for BC-017
even though it never became a marker category. Recorded as NB-6's sibling
observation rather than a defect, because the assignment made the marker list
permissive ("may record") and no claim depends on it.

## Milestone-representativeness assessment

Verified individually. All eight milestone entries match their inventory records
exactly on `version`, `date`, `branch`, `relative_path`, and `sha256`, and every
one of the 87 `overlapping_archives_it_replaces` IDs resolves to a real
inventory record (0 invalid). "Replaces" is defined in every entry as sampling
priority only, with "all archive identities remain in inventory" — no deletion
or authority transfer is implied.

Era coverage is complete: all eight substantive
`probable_architecture_era` values have a representative, including the two
smallest (`gatekernel_compact_transition_era`, 2 records;
`hardened_compact_cts_era`, 1 record) and the largest
(`preview_modular_kernel_era`, 78 records). The only unrepresented value is
`unclassified_branch_file_set`, which covers the three branch file sets and is
not an architecture era. **No important structural era is omitted**, and the set
stays at eight while covering all ten requested categories, which the assignment
expressly permits.

I tested each scrutinized claim against the whole inventory rather than
accepting the filename:

| Milestone | Claim | Independent grounding |
|---|---|---|
| BLU-HIST-0055 | Strong Teaching representative | Teaching **rank 1/249** (12 entries, 133 occurrences) |
| BLU-HIST-0127 | Reminder/time representative | time/date **rank 1/249**; reminders **rank 1/249** by occurrence (216) |
| BLU-HIST-0195 | Mood representative | MoodLib **rank 1/249** by occurrence (942) |
| BLU-HIST-0195 | Peak mega-Exec representative | **rank 1/249** on both total lines (18,969) and gate terms (247) |
| BLU-HIST-0211 | MMU/Read Lane representative | MMU joint-top tier (125 occurrences); Read Lane **rank 59/249** — see NB-4 |
| BLU-HIST-0245 | Mega-Exec → compact transition | lines fall 18,969 → 6,465 and declared modules 273 → 29 |

Notably, none of these rests on a suggestive filename — and in several cases the
filename actively points elsewhere (`0055` is named `PASS_NORMALIZE`, `0127` is
named `GateTest_03`, `0195` is named `devmode_live_diag_board`), so the labels
are marker- and metric-grounded rather than name-grounded. Only the Read Lane
half of `BLU-HIST-0211` is weakly supported.

I did not expand or alter the milestone set.

## Archived v0.22 handling assessment

Correct, and I verified the underlying fact directly.

`BLU-HIST-0246` is recorded as an ordinary historical archive identity:
`source_type: archive_file`, `source_root_id: dad_kernel_root`, era
`hardened_compact_cts_era`, sitting at
`DevBuild/!Archives/Blu_v0_22_0_5_22_26_2104_CTS.zip`. Its milestone entry states
"current runtime authority still remains the Blu_Core golden kernel."

I hashed `kernel/golden/v0.22.0/source_Blu_v0_22_0_5_22_26_2104_CTS.zip` myself:
it is `7b630e18…`, **byte-identical** to `BLU-HIST-0246`. BC-016 did not perform
or record that comparison, and — correctly — its records nowhere imply byte
identity with the golden source. The same bytes legitimately occupy two roles:
authoritative under `kernel/golden/`, and a non-authoritative historical archive
file under Dad's DevBuild tree. Keeping them as separate identities is the
required behavior, and the golden tree is unmodified. Recorded as NB-10 only as
a safe strengthening opportunity for BC-017.

## BC-015 historical-record assessment

Fully preserved. The BC-016 work commit changed nothing under
`docs/domains/runtime/assignments/BC-015/` or `docs/domains/runtime/viability/`
(diff exit 0), and the BC-015 viability validator still passes at this commit.

`docs/sources/external_inputs.md` keeps the original v0.15.2 paragraph verbatim
— archive unavailable, SHA-256 and member evidence unavailable, no contents
reconstructed — and adds a dated BC-016 entry recording that a broader source
became available afterward, that the canonical inventory now lives under
`docs/sources/historical_archives/`, that the material remains
non-authoritative, and that later availability "does not retroactively
invalidate or rewrite BC-015's honest handling of the v0.15.2 archive as
unavailable evidence during that earlier assignment."

`failures.md` promotes the same lesson in general form. Nothing in BC-016
suggests BC-015 was defective for proceeding without archives it did not have.

## External discovery reconciliation assessment

Discovery output is treated as an input, not as truth. `README.md` and the
assignment both classify it as `generated_inventory_input`, and every one of the
249 records carries `source_observation_class` — 3 `folder_manifest` (computed
by Codex) and 246 `external_inventory_import` (imported and then reconciled).
That labeling means no field silently passes as first-hand observation.

Independent checking is evidenced rather than asserted: all 249 records were
re-compared against the live root (247 matched, 2 live-only that discovery had
omitted), all 249 against the stable snapshot (249 matched), duplicates were
regrouped on container hash, two discovery date parses were rejected and
corrected, and milestones were re-verified against inventory checksums. The one
field family imported without independent recomputation is
`structural_metrics`, which `discovery_receipt.md` states plainly: "Structural
metrics: preserved from the documented external discovery rules." Given that
metrics are explicitly indicators only and are never used to support a
behavioral claim, that is an acceptable and disclosed reliance.

## Canonical JSON and CSV agreement

Exact. 249 JSON records and 249 CSV data rows; the archive-ID sets are equal and
all CSV IDs are unique. I compared every CSV row field-by-field against its JSON
record across `version`, `date`, `branch`, `source_type`, `relative_path`,
`filename`, `file_size_bytes`, `sha256`, `availability_status`,
`integrity_status`, `duplicate_group`, and `probable_architecture_era`: **zero
mismatches**, with JSON `null` correctly flattened to empty string.

`milestone_selected` is `true` on exactly 8 rows, and those 8 are precisely the
8 JSON milestones. No record is lost or corrupted through delimiter or quoting
issues — no field contains a comma or quote, and the longest path round-trips
byte-identically.

## Validator and test assessment

`tools/validate_historical_archive_inventory.py` is Python 3.12 standard library
only (`argparse`, `csv`, `json`, `re`, `sys`, `pathlib`, `typing`). It does not
extract archives, execute Blu, infer behavior, implement runtime logic, access
protected content, or modify any source. It is static inventory tooling.

Confirmed enforced: required files; JSON parse; top-level fields;
`schema_version` and `integration_assignment` pinning; source-root uniqueness
and mandatory non-authoritative authority; all inventory required fields; enum
closure on branch, source type, observation class, availability, integrity, and
confidence; SHA-256 formatting; `source_root_id` reference closure; relative-path
safety including `..` rejection; the `PROOF_KEYS` behavior-claim prohibition;
archive-ID uniqueness; duplicate-group ID uniqueness, minimum membership, member
existence, hash equality, **and member backlink**; milestone reference closure
with checksum match and safe paths; reconciliation ID uniqueness, archive-
reference closure, status enum, identity closure, path safety, and hash format;
snapshot required fields, hash format, authority boundary, and the
`independently_verified` ⇒ verifier-metadata rule; CSV/JSON count and ID-set
agreement; a path-leak sweep over every file in the archive directory; and a
repository-wide embedded-archive scan that exempts only `kernel/golden/`.

All twelve required negative tests are present, and each asserts its **specific**
intended error substring rather than merely a non-empty error list — so a
mutation that trips several checks cannot be satisfied by an unrelated failure.
I traced each: the intended check is the one asserted in every case. The
positive baseline (`test_canonical_inventory_passes`) runs against the real
repository root, which also exercises the embedded-archive scan.

Gaps are recorded as NB-2, NB-3, and NB-8. All are hardening opportunities; I
executed each missing check manually and only NB-1 surfaced a real issue.

## Manifest and protected-path assessment

`MANIFEST.sha256` contains 150 entries and correctly excludes itself. Every one
of the 150 entries matches the committed content — I verified this by hashing
each file under both the raw-working-tree and LF-normalized conventions: 104
match as raw bytes and 46 match LF-normalized, and **all 150 match under the
consistent LF/git-blob convention**. None fails under both.

Worth stating clearly so it is not mistaken for a defect: a literal
`sha256sum -c MANIFEST.sha256` on this Windows checkout reports 46 failures.
That is entirely a CRLF artifact — `core.autocrlf=true` with `* text=auto` means
Git materializes text files with CRLF while the manifest records canonical LF
content. I confirmed the convention is unchanged from BC-015 by comparing the
same manifest entry at `e629918` and `2685dd5` (identical hash), so BC-016
introduced nothing new here; which files happen to fail depends only on which
files a given checkout most recently re-materialized. The recorded hashes are
correct and are the stable, platform-independent choice.

Protected paths are clean. `kernel/golden`, `contracts/runtime`,
`docs/architecture`, `docs/domains/runtime/viability`, and `config` are
byte-identical between the base and the work commit, and again between the work
commit and the metadata commit. All eight golden CTS checksums verify. No
archive of any tracked type exists outside `kernel/golden/`. `discovery_receipt.md`
records that no source file was modified and that no temporary extraction was
created or left behind.

Validator results at this commit: runtime contracts PASS with 21 tests OK;
viability audit PASS with 9 tests OK; historical archive inventory PASS with 12
tests OK.

## No-behavioral-archaeology assessment

Confirmed. BC-016 compares only identity, structure, and marker presence. It
performs no cross-version semantic comparison and reaches no conclusion about
whether Teaching, reminders, Mood, MMU, Read Lane, or PASS worked or were
reliable, which legacy behavior should be recovered, which architecture should
be restored, or what a Python runtime should implement.

The era labels (`mega_exec_era`, `teaching_reminder_mood_pass_expansion_era`,
and so on) are structural and temporal groupings carried under a
`probable_architecture_era` field whose name hedges appropriately; none asserts
behavioral quality. `milestone_recommendations.md` closes with "BC-016 performs
no behavioral comparison. BC-017 may later test approved questions against these
exact identities," and every milestone frames its value as
`questions_it_can_help_answer` rather than answers.

## No-runtime-implementation assessment

Confirmed. The work commit added exactly two executable files —
`tools/validate_historical_archive_inventory.py` and its test — both static
inventory tooling. Everything else added or changed is Markdown, JSON, or CSV.

No routing, ScopeLock, Auth, OPSEC, reminders, scheduling, persistence, Local
Mirror, PASS, Teaching, command, Program, Persona, or Operations code or content
was implemented or altered.

## Blocking findings

None.

## Non-blocking findings

### NB-1 — Dangling inventory reference `BLU-HIST-0247` in the DevBuild file-set notes

- Path: `docs/sources/historical_archives/kernel_archive_inventory.json`,
  record `BLU-BRANCH-DEV`, third `notes` entry.
- Requirement: BC-016 review boundary §2 (no unknown inventory ID) and §15
  (record agreement).
- The note reads "Normalized member content matches external archive record
  BLU-HIST-0247." No such record exists: the inventory runs `BLU-HIST-0001`
  through `BLU-HIST-0246` with no gaps. The two analogous notes resolve and are
  independently correct — `BLU-BRANCH-PREVIEW` → `BLU-HIST-0170` and
  `BLU-BRANCH-RELEASE` → `BLU-HIST-0042` both exist and their
  `content_manifest_sha256` values genuinely match. `BLU-BRANCH-DEV`'s content
  manifest matches no record in the canonical inventory, so the claim cannot be
  checked from the committed data; the ID most likely belongs to the external
  discovery output's own numbering, which was not carried across.
- Non-blocking: the defect is confined to a prose note. No record is missing
  (246 `BLU-HIST` = 244 `archive_file` + 2 `historical_source_folder`), and it
  affects no checksum, reconciliation status, duplicate group, milestone,
  authority boundary, or privacy outcome. `BLU-BRANCH-DEV` itself reconciles
  correctly as `matched_path_and_hash` against both other identities.
- Follow-up: correct the note to cite the external inventory's identifier with an
  explicit "external discovery numbering" label, or state that the DevBuild file
  set has no canonical-inventory content-manifest match.

### NB-2 — Validator does not check the reference classes that would have caught NB-1

- Path: `tools/validate_historical_archive_inventory.py`.
- Requirement: BC-016 review boundary §16.
- Four absent invariants: archive IDs cited inside `notes` strings are never
  resolved; a record whose `duplicate_group` names a group missing from
  `duplicate_groups` would pass (the group→member backlink is checked, the
  member→group direction is not); duplicate milestone `archive_id` values would
  pass — `milestone_ids` is populated at line 263 and never read, so it is a dead
  variable; and no scan detects identical `archive_file_sha256` values omitted
  from a duplicate group, which is the check most likely to catch a genuinely
  missed duplicate.
- Non-blocking: I ran all four manually. Only the notes check fails (NB-1). Every
  `duplicate_group` value in use is defined, all 8 milestones are distinct, and
  an exhaustive hash scan finds exactly the two recorded collision groups.
- Follow-up: add the omitted-duplicate scan and the member→group backlink check
  as the two highest-value additions.

### NB-3 — Path-leak detection has narrow blind spots

- Path: `tools/validate_historical_archive_inventory.py`, `has_path_leak` and
  `is_relative_path`.
- Requirement: BC-016 review boundary §3 and §16.
- A bare UNC path (`\\MACHINE\share\file.zip`) carrying no drive letter and no
  `users`/`home` segment is not matched by any of the three patterns, so it would
  pass the free-text sweep over notes and prose. Percent-encoded traversal
  (`%2e%2e`) is not decoded before the `..` check. `is_relative_path` does reject
  UNC values in `relative_path` fields, because `\\MACHINE\...` normalizes to a
  POSIX-absolute `//MACHINE/...`, so structured path fields are protected; the gap
  is free text only. `file://` and extended-length `\\?\C:\` forms are caught via
  the drive-letter and POSIX-prefix patterns.
- Non-blocking: my independent ten-pattern recursive sweep found zero
  occurrences of any of these forms anywhere in BC-016. There is no present
  exposure; this is defense-in-depth for future inputs.

### NB-4 — `BLU-HIST-0211`'s "Read Lane" label and `high` confidence exceed the marker evidence

- Path: `docs/sources/historical_archives/milestone_recommendations.md` and the
  matching `milestone_recommendations` entry in the canonical JSON.
- Requirement: BC-016 review boundary §11 — each selection must have supporting
  marker or structural evidence, and confidence must be justified.
- The MMU half holds up: `BLU-HIST-0211` sits in the joint-top occurrence tier at
  125. The Read Lane half does not: 50 occurrences, **rank 59 of 249**, against
  `BLU-HIST-0244` at 122 and `BLU-HIST-0242`/`0243` at 116. `BLU-HIST-0245` —
  already in the milestone set — strictly outranks `0211` on both markers (MMU 8
  entries vs 4; Read Lane 4 entries vs 2). `selection_confidence: high` covers
  both halves of a label only half of which is supported.
- Non-blocking: severity guidance treats a milestone explanation that can be
  strengthened without changing the selected source as non-blocking, and the
  selection itself is sound — `BLU-HIST-0211` is the sole representative of
  `mega_exec_to_compact_transition_era` (33 records), which would otherwise lose
  coverage.
- Follow-up: relabel as "MMU representative; Read Lane secondary" or lower the
  confidence to `medium`, without changing the selected archive.

### NB-5 — README date-count sentence does not reconcile to a single total

- Path: `docs/sources/historical_archives/README.md`, Known limitations.
- Requirement: BC-016 review boundary §8.
- "Twenty-five external dates originally relied on filesystem timestamps; two
  additional ambiguous short-date parses were corrected to that same explicit
  fallback" reads as 27, while the committed data has 29 records carrying the
  fallback (25 `archive_file` + 1 `historical_source_folder` + 3 branch file
  sets), of which 26 are externally derived.
- Non-blocking: no date is misrepresented regardless of the summary, because the
  `date_source` enum value itself states the disclaimer on every affected record.
  This is a summary-arithmetic wording issue only.
- Follow-up: restate as exact counts by source type.

### NB-6 — `BLU-HIST-0091` lists four never-readable archives among the archives it "replaces"

- Path: `docs/sources/historical_archives/milestone_recommendations.md`,
  `BLU-HIST-0091` overlap list.
- Requirement: BC-016 review boundary §7 and §11.
- Four of the 25 listed overlaps (`BLU-HIST-0074`, `0078`, `0081`, `0082`) are
  Deflate64 records with zero markers and zero structural metrics. "Replaces" is
  correctly defined as sampling priority only, but asserting that `0091` is an
  adequate sampling substitute for archives whose member content was never
  readable reaches slightly past the available evidence.
- Non-blocking: the milestone selection itself does not depend on those records,
  no record is removed, and the Deflate64 limitation is stated in three places.
- Follow-up: annotate unreadable overlaps so BC-017 knows those four still
  warrant separate handling if a Deflate64-capable reader becomes available.

### NB-7 — `exact_heading_or_identifier` sometimes holds truncated content, not a heading or identifier

- Path: `docs/sources/historical_archives/kernel_archive_inventory.json`,
  `notable_capability_markers[].exact_heading_or_identifier`.
- Requirement: BC-016 review boundary §10 — markers must be grounded in an actual
  member path, heading, identifier, or documented structural observation.
- 231 of 9,507 populated values exceed 200 characters and are capped at exactly
  240, several cut mid-word. Some are neither headings nor identifiers but
  commentary lines lifted from historical documents (for example the ComponentGate
  and ExecLib size observations). The field name overstates what those entries
  contain.
- Non-blocking: no security-relevant content is involved — every non-heading Auth
  and OPSEC excerpt was redacted — and each entry still records a real
  `exact_member_path`, so grounding survives. The issue is field-name accuracy
  and readability.
- Follow-up: either rename to allow an excerpt form or add an
  `identifier_kind` discriminator distinguishing heading, identifier, and excerpt.

### NB-8 — Six implemented validator invariants have no negative test

- Path: `tests/historical_archives/test_validate_historical_archive_inventory.py`.
- Requirement: BC-016 review boundary §17.
- The duplicate-group backlink, unknown `source_root_id`, invalid reconciliation
  identity, unsafe milestone path, snapshot-authority, and embedded-archive checks
  all exist in the validator but are never exercised, so a future regression that
  disabled one would not be caught.
- Non-blocking: all twelve tests the assignment required are present and correct,
  and I verified each of these six checks by reading the implementation and
  confirming the committed data satisfies it.

### NB-9 — The approved packet contains a self-contradictory validation line

- Path: `docs/domains/runtime/assignments/BC-016/assignment.md`, "Required BC-016
  validation".
- The packet instructs verifying that "no committed file contains
  `source_root_id: dad_kernel_root`", while the same packet lists
  `dad_kernel_root` among "Approved root aliases" and requires external paths be
  converted to `source_root_id` plus `relative_path`. All 249 records use
  `dad_kernel_root`.
- Non-blocking, and Codex resolved it correctly: `dad_kernel_root` is a sanitized
  alias, not a personal path, so privacy is fully preserved and the substantive
  requirement is met. Recorded so Dad and Blu can correct the packet wording
  before a future assignment is checked against the contradictory line.

### NB-10 — The verified byte identity between `BLU-HIST-0246` and the golden CTS ZIP is not recorded

- Path: `docs/sources/historical_archives/kernel_archive_inventory.json`,
  `BLU-HIST-0246`.
- Requirement: BC-016 review boundary §12.
- BC-016 correctly does not imply identity with the golden source, since it did
  not perform that comparison. I performed it: the two are byte-identical
  (`7b630e18…`). Recording that verified relationship — while keeping the two as
  distinct source identities with distinct authority — would give BC-017 a
  precise anchor between the historical tree and the current CTS.
- Non-blocking: this is a safe strengthening opportunity, not a defect. The
  current records are correct as written.

## Correctly preserved unresolved identities

- The five hash identities — outer ZIP, archive-file, archive content manifest,
  live-root payload manifest, and branch file-set manifest — remain distinct,
  enforced structurally through `sha256_type` and stated in `README.md`,
  `snapshot_receipt.json` limitations, and `failures.md`.
- Seven Deflate64 archives retain hashes and central directories, stay
  `not_tested`, are never called corrupt, carry no invented member metrics, and
  are excluded from milestone selection.
- Filesystem timestamps carry their disclaimer inside the enum value itself and
  are never used to order chronology or select an authority winner.
- The two rejected ambiguous short-date parses are recorded in the canonical
  limitations, the discovery receipt, and `failures.md`.
- Four member-content near-duplicates are retained as separate records and
  explicitly denied exact-duplicate status.
- The Preview and Release branch file sets remain separately recorded live
  organizational identities despite matching archive content.
- Marker prominence, implementation-style Markdown, and structural metrics are
  consistently denied as behavioral evidence.
- 1,321 security-related non-heading excerpts are omitted with an explicit
  redaction note rather than silently dropped.
- BC-015's v0.15.2 unavailability is preserved verbatim, with later availability
  explicitly stated not to invalidate it.

## Recommended disposition

```text
approve-with-notes
```

BC-016 is correct on every point the assignment made blocking. Inventory counts,
reconciliation totals, duplicate groups, milestone references, and CSV/JSON
agreement are exact and independently reproducible. Source identities and
authority boundaries hold, and the container-versus-payload-versus-manifest
distinctions are enforced structurally rather than only described. Path
sanitization is clean under ten independent pattern families. Protected Auth and
OPSEC material was systematically redacted. The snapshot claim is supported by
derived values that could only come from the real container. No archive was
imported, no behavioral conclusion was drawn, BC-015 is untouched, and no runtime
was implemented.

## Exact required follow-up

None is blocking. Before BC-017 is authorized, Dad and Blu should decide on:

1. NB-1 — correct or remove the `BLU-HIST-0247` reference in `BLU-BRANCH-DEV`'s
   notes; it is the only factual error found in the committed records.
2. NB-4 — relabel `BLU-HIST-0211` or lower its confidence so the Read Lane claim
   matches its evidence, without changing the selected archive.
3. NB-2 and NB-3 — add the omitted-duplicate scan, the member→group backlink
   check, notes-reference resolution, and UNC free-text detection.
4. NB-6 — annotate the four unreadable archives inside `BLU-HIST-0091`'s overlap
   list.
5. NB-5, NB-7, NB-9, NB-10 — wording, field-naming, packet, and cross-reference
   improvements that can be folded into whichever assignment next touches these
   records.

BC-016 remains `review`. Dad and Blu own final closure and the authorization of
BC-017. This review does not authorize behavioral archaeology, archive import,
milestone changes, or any successor-runtime implementation.
