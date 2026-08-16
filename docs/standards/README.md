# Standards

The Code Standards principle at project scope. Full contracts inherited from praxis at [`../agentic-ai/code-standards/`](../agentic-ai/code-standards/).

**Meta-principle:** code standards are a first-class project concern. Every project articulates them. Enforcement is machine where possible, review where not. Standards evolve deliberately.

---

## What lives here

```
docs/standards/
├── README.md              ← this file
├── standards.md           ← the declared standards doc (create per TEMPLATE-standards-doc.md)
└── exceptions.md          ← append-only ledger of granted exceptions
```

---

## Getting started

1. Copy [`../agentic-ai/code-standards/TEMPLATE-standards-doc.md`](../agentic-ai/code-standards/TEMPLATE-standards-doc.md) to `standards.md`
2. Choose your standard families from [`../agentic-ai/code-standards/FAMILIES.md`](../agentic-ai/code-standards/FAMILIES.md) (SOLID / KISS / YAGNI / DRY / functional-core-imperative-shell / hexagonal / clean-architecture / DDD / composition-over-inheritance / fail-fast / etc.) — pick 2-4 max
3. Author your first standards per category (naming / state / errors / testing / docs / dependencies / project-specific)
4. For each: statement + rationale + enforcement layer + applies-to scope + provenance
5. Wire mechanical enforcement (linter rules / hooks / test-list entries)
6. Create `exceptions.md` (empty initially)
7. Announce in session log

---

## Evolution

- Adding a standard = decision (see [`../agentic-ai/code-standards/EVOLUTION.md`](../agentic-ai/code-standards/EVOLUTION.md) §INTRODUCE)
- Removing a standard = decision (§DEPRECATE → §RETIRE)
- Replacing a standard = decision (§SUPERSEDE)
- Granting exceptions = decision with ledger entry (§GRANT EXCEPTION)
- Ad-hoc changes = drift; the discipline exists to prevent this

Quarterly review cadence per EVOLUTION.md keeps standards from rotting.

---

## Related

- [`../agentic-ai/code-standards/README.md`](../agentic-ai/code-standards/README.md) — meta-principle
- [`../agentic-ai/code-standards/CONTRACT.md`](../agentic-ai/code-standards/CONTRACT.md) — schema for standards.md + exceptions.md
- [`../agentic-ai/code-standards/FAMILIES.md`](../agentic-ai/code-standards/FAMILIES.md) — catalog of families to draw from
- [`../agentic-ai/code-standards/EVOLUTION.md`](../agentic-ai/code-standards/EVOLUTION.md) — how standards evolve
- [`../agentic-ai/code-standards/TEMPLATE-standards-doc.md`](../agentic-ai/code-standards/TEMPLATE-standards-doc.md) — scaffold
