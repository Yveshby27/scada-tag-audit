# Testing

The Testing spine at project scope. Full contracts inherited from praxis at [`../agentic-ai/testing/`](../agentic-ai/testing/). This directory holds project data (test-list, failure-log, coverage-ledger, live-capabilities inventory).

**Central discipline:**

1. Every test names the break it catches (Gate A)
2. Every test exercises the real thing (Gate B)
3. Every test file passes mutation check (Gate C)
4. Failures are classified, not fake-fixed
5. Hermetic and live are separate tracks
6. Test-list IDs are stable forever — retire, never delete

Full details: [`../agentic-ai/testing/README.md`](../agentic-ai/testing/README.md).

---

## What lives here

```
docs/testing/
├── README.md                  ← this file
├── test-list.json             ← source of truth (created by /test --generate)
├── test-list.md               ← rendered view (auto-generated from JSON)
├── failure-log.md             ← append-only ledger of failures with classification dossiers
├── coverage-ledger.md         ← rolling coverage per feature area (auto-regenerated)
├── live-capabilities.json     ← real-world side effect inventory (created by /live-test --inventory)
└── dropped-cells.json         ← cells rejected at Gate A (kept so /test --expand-axes doesn't re-propose)
```

Actual test files live per project convention (`tests/`, `spec/`, `__tests__/`, etc.). Test-list entries carry `file:` pointers to the runnable files.

---

## Daily use

- **Adding new behavior?** Run `/test --generate <feature-area>` to author test-list entries + materialize test bodies.
- **Running tests?** `/test --run <scope>` executes hermetic tests in parallel HERMETIC sandboxes. Failures land in `failure-log.md`.
- **Handling failures?** `/test --heal <scope>` walks the failure loop — classifies each open entry, routes per classification.
- **Code touched?** The `test-staleness-detector.ps1` hook marks affected test-list entries `stale`. Reconcile via `/test --heal` or `/test --drift-check`.
- **Live verification?** `/live-test --run` — requires `/go external-write` first; runs in PERSISTENT sandbox with lock discipline.
- **Auditing?** `/test --audit <scope>` walks the WARNING-SIGNS checklist for tautological / mocked-only / change-detector tests.

---

## Test classes

- **unit** — pure functions, components in isolation
- **api** — backend function-level tests
- **integration** — cross-boundary tests with real components
- **e2e** — full-stack tests against the running app
- **journey** — seeded random walks with invariant assertions (state-machine testing)
- **visual** — screenshot regression
- **live-capability** — real delivery verification (live track only)

---

## Test tracks

- **hermetic** — default; parallel; deterministic; HERMETIC sandboxes; mocked externals
- **live** — separate; locked; real credentials; PERSISTENT sandbox; capability-verifying

Live never owns behavioral correctness; that's hermetic's job. Live owns delivery correctness (email actually sends, webhook actually arrives, charge actually processes).

---

## Sandboxes

Testing consumes the Sandboxes capability substrate (see [`../sandboxes/README.md`](../sandboxes/README.md)). Testing declares HERMETIC or PERSISTENT sandbox shape; the sandbox layer provides the interface; testing never mentions specific providers.

---

## Archetype libraries

Your project inherits archetype libraries matching declared `PROJECT_ARCHETYPES` in `CLAUDE.md`. Testing archetypes: webapp / mobile / cli / api-backend / data-pipeline. See [`../agentic-ai/testing/archetypes/`](../agentic-ai/testing/archetypes/).

---

## Related

- [`../agentic-ai/testing/`](../agentic-ai/testing/) — full spine home
- [`../agentic-ai/testing/QUALITY-GATES.md`](../agentic-ai/testing/QUALITY-GATES.md) — Gates A / B / C
- [`../agentic-ai/testing/FAILURE-LOOP.md`](../agentic-ai/testing/FAILURE-LOOP.md) — classification discipline
- [`../agentic-ai/testing/LIVE-VS-HERMETIC.md`](../agentic-ai/testing/LIVE-VS-HERMETIC.md) — track separation
- [`../agentic-ai/testing/WARNING-SIGNS.md`](../agentic-ai/testing/WARNING-SIGNS.md) — bad-test checklist
- [`../agentic-ai/playbooks/testing-methodology.md`](../agentic-ai/playbooks/testing-methodology.md) — deep methodology
- [`../sandboxes/README.md`](../sandboxes/README.md) — sibling substrate
