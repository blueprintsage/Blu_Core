# Chat Host-Family Adapter Contract

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-020

## Surface model

The normalized family is `chatgpt`. Documentary examples include Chat,
ChatGPT Work on the web, and ChatGPT desktop Chat/Work surfaces, but the set is
not permanent or exhaustive. A live adapter must self-identify its actual
surface and dynamically report what exists now.

BC-020 did not have a supported runtime probe of Dad's separate live Chat
binding. Current Chat availability is therefore unknown unless a future
adapter self-report or host receipt supplies evidence. Documentary surface
claims remain `documented_possible`.

Current first-party documentation shows why a fixed Chat tool list would be
false:

- [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer) describes
  file/artifact workflows whose preview/review behavior depends on surface.
- [Plugins](https://learn.chatgpt.com/docs/plugins) describes skills,
  connectors, and MCP tools on supported surfaces while excluding other
  surfaces.
- [Web search](https://learn.chatgpt.com/docs/web-search) describes first-party
  search subject to workspace settings; search is not raw network access.
- [Projects and chats](https://learn.chatgpt.com/docs/projects) separates
  uploaded/connected project context from direct local-folder access.
- [Scheduled tasks](https://learn.chatgpt.com/docs/automations) describes
  surface- and workspace-dependent scheduling, recurrence, runs, and context.
- [Computer Use](https://learn.chatgpt.com/docs/computer-use) requires a
  supported surface/region, plugin state, OS/app permissions, and scoped use.

These sources are provenance records accessed 2026-08-08, not runtime probes.

## Binding behavior

The Chat adapter translates the raw host event while preserving attachment,
external-source, tool-result, event identity, and provenance metadata actually
provided. It emits a fresh capability report at startup/new binding and before
sensitive use. Missing exposure yields unknown or verified-unavailable based on
current evidence, never a hardcoded product list.

Uploaded sources map to `host_attachment`; connected sources map to
`external_source_object`; a path becomes `filesystem_object` only when the host
explicitly supplies filesystem semantics. Integrations are normalized by
provider, operation/read-write class, input/output scope, approval/Auth needs,
availability, and receipt behavior rather than embedded in kernel contracts.

## Current disposition

Documented Chat possibilities include text/image/file input, web search,
plugins/MCP/connectors, artifact creation, GUI actions, and scheduling on
supported surfaces. Current availability, exact time, filesystem/shell/Git,
provider receipts, signed-in identity/role evidence, security-grade host
session binding, replay evidence, and rollback-resistant attempt state remain
unknown for Dad's live Chat binding.

Product sign-in is not Blu authorization. Conversation/project identity is
correlation-only at most. If a future Chat binding cannot produce the complete
security evidence record, protected cross-turn authorization continuation is
unavailable on that binding.
