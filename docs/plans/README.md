# `docs/plans/`

Feature plan docs live here — one file per feature at `<slug>.md`.

## Convention

The plan-doc format + lifecycle status vocabulary is inherited from praxis. It lives in the substrate:

- **Format + template:** `docs/agentic-ai/plan-docs/` (inherited from praxis `agentic-os/plan-docs/` at bootstrap).
- **Locked lifecycle vocabulary:** see `VOCAB.md` §1 — the 8-state `Status:` progression from `Not started` through `Shipped`.

## Rules of thumb

- **Every non-trivial feature starts with a plan doc.** The Feature Build pipeline (see `docs/pipelines.md`) begins by confirming the plan doc exists.
- **`Status:` advances only forward.** Regressions require a note in the plan doc explaining why.
- **`Code complete` is not `Verified`.** `Verified <env>` requires on-device / on-prod confirmation. See `VOCAB.md` §2.
- **`/end-of-task-review` before flipping past `Code complete (uncommitted)`.** 6-axis structured checkpoint; catches the class of gap that green gates + green tests miss.
- **One plan doc per feature.** Cross-cutting refactors span multiple features and get either their own plan doc or a `docs/plans/refactors/` subdirectory — instance decides.

## See also

- **Praxis abstract:** `docs/agentic-ai/plan-docs/` — format, template
- **Praxis pipelines:** `docs/pipelines.md` — Feature Build pipeline reads/writes plan docs
- **Praxis skills:** `/end-of-task-review`, `sync-context`, `consolidate` all interact with plan docs
- **Vocabulary:** `VOCAB.md` §1 — task lifecycle states
