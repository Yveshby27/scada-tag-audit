# Sandboxes

The Sandboxes capability substrate at project scope. Full contracts inherited from praxis at [`../agentic-ai/sandboxes/`](../agentic-ai/sandboxes/).

**This directory holds documentation only.** The actual project data (provider adapter, config) lives at `.claude/sandboxes/`.

Sandboxes are a capability substrate — like hooks. Praxis owns the interface; you choose the provider and author the adapter.

---

## What lives here vs `.claude/sandboxes/`

**Here** (`docs/sandboxes/`):
- This README (pointer to praxis convention)
- Optional: project-specific sandbox notes

**In `.claude/sandboxes/`** (project code):
- `adapters/<provider>.ts` (or .py, .sh) — provider adapter code
- `config.json` — provider choice, pool sizes, egress rules
- `adapters/tests/` — adapter test suite

---

## Three patterns

- **HERMETIC** — ephemeral, default-deny egress, per-run isolation, seeded state. Default. Used for parallel hermetic tests, one-off subagent tasks, experiment runs.
- **PERSISTENT** — long-lived, real dev credentials, single-tenant, one-op lock. Used for live tests, staging-like verification.
- **SUBAGENT** — scratch workspace per subagent, capability-scoped, no bleed-back. Used for parallel subagent orchestration.

Full pattern details:
- [`../agentic-ai/sandboxes/HERMETIC.md`](../agentic-ai/sandboxes/HERMETIC.md)
- [`../agentic-ai/sandboxes/PERSISTENT.md`](../agentic-ai/sandboxes/PERSISTENT.md)
- [`../agentic-ai/sandboxes/SUBAGENT.md`](../agentic-ai/sandboxes/SUBAGENT.md)

---

## Choosing a provider

Provider choice is `provider-integration` research class. Run `/research "sandbox provider for <archetype>" --class provider-integration` first. Common candidates (2026-08-04):

- **e2b** — HERMETIC + SUBAGENT strong; fast spin-up; egress control
- **Modal** — general-purpose; strong SDK
- **Codesandbox / Stackblitz** — preview environments; less HERMETIC discipline
- **Self-hosted docker** — full control; more adapter work
- **RunPod** — GPU workloads

See archetype-specific guidance: [`../agentic-ai/sandboxes/archetypes/webapp.md`](../agentic-ai/sandboxes/archetypes/webapp.md), [`../agentic-ai/sandboxes/archetypes/agent-substrate.md`](../agentic-ai/sandboxes/archetypes/agent-substrate.md).

---

## Authoring an adapter

Follow [`../agentic-ai/sandboxes/TEMPLATE-provider-adapter.md`](../agentic-ai/sandboxes/TEMPLATE-provider-adapter.md). Six required operations:

1. `spin_up(spec) → SandboxHandle`
2. `run_in(handle, command, opts) → RunResult`
3. `capture_outputs(handle, paths) → Files`
4. `tear_down(handle) → void`
5. `set_egress(handle, policy) → void`
6. `attach_capability(handle, capability) → void`

Four optional: `snapshot`, `restore`, `stream_logs`, `list_active`.

Every provider-native error maps to a typed error from the interface. Never leak provider-native errors past the adapter.

---

## Egress policy

Every sandbox has an egress policy:
- **HERMETIC default:** `deny_all`
- **PERSISTENT default:** `permissive` (within account)
- **SUBAGENT default:** `allow_list` (empty)

Widening HERMETIC's allow-list is a decision — carries reason in config. See [`../agentic-ai/sandboxes/EGRESS-POLICY.md`](../agentic-ai/sandboxes/EGRESS-POLICY.md).

---

## Parallelism

HERMETIC pools scale widely (50-1000 concurrent typical). PERSISTENT is single-instance (lock discipline). SUBAGENT is medium (10-100 concurrent). Configure caps in `.claude/sandboxes/config.json`. See [`../agentic-ai/sandboxes/PARALLELISM.md`](../agentic-ai/sandboxes/PARALLELISM.md).

---

## Related

- [`../agentic-ai/sandboxes/`](../agentic-ai/sandboxes/) — full capability home
- [`../agentic-ai/sandboxes/INTERFACE.md`](../agentic-ai/sandboxes/INTERFACE.md) — the six-op contract
- [`../agentic-ai/playbooks/sandboxes-usage.md`](../agentic-ai/playbooks/sandboxes-usage.md) — deep methodology
- [`../testing/README.md`](../testing/README.md) — primary consumer of the interface
