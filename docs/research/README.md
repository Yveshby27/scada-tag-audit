# Research

Task-motivated research notes produced by [`/research`](../agentic-ai/skills/research.md). **Research is the foundation, not a step.**

**This directory holds project data (notes).** The full convention, schema, mechanical triggers, floor-and-ceiling depth guidance, refresh discipline, and 7 class templates live in [`../agentic-ai/research/`](../agentic-ai/research/) — inherited from praxis at bootstrap and upgradable via `praxis upgrade`.

---

## What lives here

```
docs/research/
├── README.md                              ← this file
├── triggers.yaml                          ← (optional) project-specific trigger overrides
└── YYYY-MM-DD-<slug>.md                   ← individual research notes
```

Notes are markdown with structured YAML frontmatter — same shape as ADRs and integration notes. No JSON pair.

---

## Daily use

- **Working on a new provider / dependency / architectural pattern / compliance surface?** Run `/research "<topic>" --class <class>` before writing the plan.
- **Task blocked by a research trigger?** The trigger detector hook fires when you touch a package manifest / new integration file / new ADR / project-configured research-trigger path without a covering research note. Resolve by running `/research`.
- **Refreshing?** `/research --refresh docs/research/YYYY-MM-DD-<slug>.md` — diff-driven, keeps history in the Refresh log.
- **Superseding?** `/research --supersede <old-note> --topic "<new topic>"` when the core question changed.
- **Retiring?** `/research --retire <note> --reason "<one-line>"` when the topic is no longer relevant to the project.

---

## Classes

Seven templates, chosen by decision class:

| Class | For |
|---|---|
| **provider-integration** | new external provider or SDK dependency |
| **architectural-pattern** | adopting a pattern the project hasn't shipped before |
| **security-model** | auth, session, encryption, threat modeling, cryptographic choice |
| **compliance** | regulatory / legal / privacy |
| **migration** | provider migration, database migration, major version migration |
| **scale** | performance / latency / throughput target |
| **general** | catch-all when specialized classes don't fit |

Full class descriptions + floor/ceiling: [`../agentic-ai/research/FLOOR-AND-CEILING.md`](../agentic-ai/research/FLOOR-AND-CEILING.md).

---

## The trigger contract

Mechanical detection — not vibes. Blocking triggers:

- New top-level dependency added (package manifest diff)
- New integration file being created (`references/integrations/<new-slug>.md`)
- New ADR being drafted (`references/adr/<new-NNNN>-*.md`)
- Ticket carries `research_needed: true` in frontmatter
- Project-configured research-trigger paths touched (`.claude/hooks/research-trigger-paths.json`)

Noted triggers:

- New API host referenced in code
- Performance / scale claim in a plan doc
- Prior research on this topic is stale

Full trigger rules + coverage checks: [`../agentic-ai/research/triggers.default.yaml`](../agentic-ai/research/triggers.default.yaml).

---

## Project-specific triggers

Add project-specific research-trigger classes in `triggers.yaml` here. Also configure `.claude/hooks/research-trigger-paths.json` for auth / payment / storage / messaging / project-specific research-warranted areas.

Do NOT silence default blocking triggers — if a default fires too often, that's a praxis promotion, not a local silence.

---

## Depth — floor and ceiling

- **Floor** — the minimum content per class for a note to be defensible. Enforced: `/research` refuses to mark authorable-complete without floor.
- **Ceiling** — depth guidance past which further investigation stops paying off. Operator's discretion above the ceiling; not enforced.

Full guidance per class: [`../agentic-ai/research/FLOOR-AND-CEILING.md`](../agentic-ai/research/FLOOR-AND-CEILING.md).

---

## Refresh discipline

Notes carry `last_verified_at` + `refresh_after_days`. `consolidate` Axis 7 walks notes and flags stale ones. Small regular refresh > large infrequent refresh.

Default refresh thresholds by class:
- provider-integration / security-model / compliance → 90 days
- migration / scale / architectural-pattern → 180 days
- general → 365 days

---

## Source tiers

Citations use praxis's tier system (see [`../agentic-ai/anchors/sources.md`](../agentic-ai/anchors/sources.md) if inherited, or [`../../docs/anchors/sources.md`](../../docs/anchors/sources.md)):

- **Tier 1** — primary / authoritative (RFCs, NIST, vendor official, regulator text)
- **Tier 2** — practitioner synthesis (engineering blogs, post-mortems, established newsletters)
- **Tier 3** — adjacent tooling docs
- **Tier 4** — real-time signal (X, Bluesky, forums)

Class-specific rules: security-model MUST have ≥1 Tier 1; compliance MUST cite regulatory text as Tier 1.

---

## Related

- [`../agentic-ai/research/README.md`](../agentic-ai/research/README.md) — full spine convention
- [`../agentic-ai/research/SCHEMA.md`](../agentic-ai/research/SCHEMA.md) — note frontmatter + body sections
- [`../agentic-ai/research/triggers.default.yaml`](../agentic-ai/research/triggers.default.yaml) — mechanical trigger definitions
- [`../agentic-ai/research/FLOOR-AND-CEILING.md`](../agentic-ai/research/FLOOR-AND-CEILING.md) — depth guidance per class
- [`../agentic-ai/playbooks/research.md`](../agentic-ai/playbooks/research.md) — deep methodology
- [`../context/README.md`](../context/README.md) — Context spine (consumes research)
