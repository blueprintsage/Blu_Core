# Codex Host-Family Adapter Contract

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-020

## Family and surfaces

The normalized family is `codex`. It is not synonymous with CLI, desktop,
cloud, IDE, local checkout, worktree, or one sandbox mode. First-party
documentation explicitly distinguishes [local, worktree, and cloud
environments](https://learn.chatgpt.com/docs/environments/modes), and describes
[sandbox](https://learn.chatgpt.com/docs/sandboxing),
[permission](https://learn.chatgpt.com/docs/permission-modes),
[web search](https://learn.chatgpt.com/docs/web-search),
[MCP](https://learn.chatgpt.com/docs/extend/mcp), and
[terminal](https://learn.chatgpt.com/docs/integrated-terminal) behavior as
surface/configuration dependent.

## Observed binding

BC-020 safely observed only `codex_desktop_local_windows`:

```text
OS: Microsoft Windows 10.0.19045 x64
execution environment: local checkout
sandbox: workspace-write
approval mode: auto_review
network: restricted; web search and named approved Git remote operations observed
workspace root: D:/Repos/Blu_Core
observed time: 2026-08-08T23:05:40-05:00
client/surface version: unknown
```

The version probe located the packaged executable but could not execute
`codex --version` inside the bounded environment. No version was inferred from
its installation path.

Operation receipts established text/structured input, the supplied attachment,
workspace/repository reads, workspace specification writes/creates, shell
execution with output/exit code, Git repository read plus branch creation and
approved fetch/pull, web search/page retrieval, and a single current-time
provider result. Current host metadata exposed dynamic tool, plugin/MCP,
artifact, thread, and automation interfaces. Metadata exposure alone does not
prove provider connection, permission, operation success, or a receipt.

The snapshot does not establish arbitrary filesystem delete/rename, raw
network, Git commit/push/PR, a durable continuity provider, saved memory,
verified account identity/role/credential evidence, or provider-backed
security-grade session state.

## Filesystem, shell, network, Git, and integrations

Filesystem operations and roots are independent claims. A `workspace-write`
surface may be able to write approved workspace paths while remaining unable to
act elsewhere. Shell receipts include working directory, sandbox/approval and
network scope, timeout behavior, exit code, available output, and limitations.

Web search, arbitrary outbound network, and MCP/plugin/app calls remain separate.
This turn's successful web calls and approved Git fetch/pull do not prove raw
network. Repository detection/read, Git write, branch, commit, push, remote, and
PR operations are independently reported. The substantive contract snapshot
does not claim commit or push availability before those operations occur.

External tool discovery preserves provider/tool identity, operation/read-write
class, approval/Auth requirements, scope, current exposure, and receipt
semantics. Individual integrations never become kernel dependencies.

## Time, scheduling, and security

The time provider proved exactly one current result and UTC offset for the
observed invocation; no permanent availability is inferred. The exposed
automation metadata proves only that a create/update/cancel/recurrence interface
is present. It does not prove provider/account connection, required permission,
operational usability, operation success, future execution, or receipt
availability, so all three operational scheduling capabilities remain `unknown`.
For documented desktop scheduled tasks only, future local execution may depend
on the relevant machine and app remaining powered on and available.

The observed interface supplies host action approval evidence for named
operations, but this is not Blu authorization. Its automatic reviewer is not
verified explicit user approval. No adapter-visible provider supplies host-
session integrity, request/result binding, prior-consumption/replay state, or
monotonic/rollback-resistant attempt state. Protected cross-turn authorization
continuation is therefore verified unavailable on this observed binding.
