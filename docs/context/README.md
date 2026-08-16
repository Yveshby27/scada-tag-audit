# Context

Task-scoped context briefs assembled by [`/gather-context`](../agentic-ai/skills/gather-context.md) — the mechanical assembly of the maximum-useful substrate for a specific piece of work.

**This directory holds project data (briefs).** The full convention, schema, assembly rules, ambiguity contract, and refinement protocol live in [`../agentic-ai/context/`](../agentic-ai/) — inherited from praxis at bootstrap and upgradable via `praxis upgrade`.

---

## What lives here

```
docs/context/
├── README.md              ← this file
├── rules.yaml             ← (optional) project-specific assembly rule overrides
└── briefs/
    ├── ACTIVE.md          ← generated index of open briefs (do not hand-edit)
    ├── <task-id>.json     ← machine layer — source of truth
    ├── <task-id>.md       ← rendered view — auto-generated, do not hand-edit
    └── retired/           ← briefs whose task has shipped or been retired
```

---

## Daily use

- **Starting a task?** Run `/gather-context <ticket-id | plan-path | intent>` before touching code.
- **Resuming a task?** Read the existing brief. If it's stale (`last_assembled_at` > 7 days), run `/audit-context <task-id>` or re-run `/gather-context`.
- **Closing a task?** `sync-context` walks the brief's `refinements[]` and routes each entry into memory / sources / references / plans / tickets / scenarios per [`../agentic-ai/context/REFINEMENT.md`](../agentic-ai/context/REFINEMENT.md).
- **Session end?** `consolidate` Axis 7 reports on brief health (stale assembly, blocking ambiguity carried over, refinement debt).

---

## The two levels of ambiguity

- **Blocking** — a Stop hook (see `.claude/hooks/context-ambiguity-gate.ps1`) prevents the agent from yielding to you with unresolved blocking ambiguity. You'll be asked to resolve, downgrade, or park.
- **Noted** — logged in the brief, doesn't halt work. Resolved during work or by refinement sweep.

Every ambiguity must **name the specific decision you'd need to make** to resolve it. Ambiguity that can't name a decision is under-reading, not ambiguity — the raising skill should read more first.

---

## Project rule overrides

Add feature-area code globs, project-specific source subdirs, or project-specific ambiguity detectors in `rules.yaml` here. Default rules ship in [`../agentic-ai/context/rules.default.yaml`](../agentic-ai/context/rules.default.yaml). Your `rules.yaml` extends the defaults — it does not replace them.

Do NOT override default detectors to silence them. If a detector fires "too often," the fix is a praxis promotion, not a local silence.

---

## Related

- [`../agentic-ai/context/README.md`](../agentic-ai/context/README.md) — full spine convention
- [`../agentic-ai/context/SCHEMA.md`](../agentic-ai/context/SCHEMA.md) — brief schema
- [`../agentic-ai/context/rules.default.yaml`](../agentic-ai/context/rules.default.yaml) — default assembly rules
- [`../agentic-ai/context/AMBIGUITY.md`](../agentic-ai/context/AMBIGUITY.md) — ambiguity contract
- [`../agentic-ai/context/REFINEMENT.md`](../agentic-ai/context/REFINEMENT.md) — refinement routing
- [`../agentic-ai/playbooks/context-assembly.md`](../agentic-ai/playbooks/context-assembly.md) — deep methodology
