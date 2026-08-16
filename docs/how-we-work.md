# How we work — scada-tag-audit

Project-side workflow visualization. Extends praxis's [`agentic-ai/docs/orchestration.md`](agentic-ai/docs/orchestration.md) with scada-tag-audit-specific flows.

For the universal praxis lifecycle (raw material → structured → work → gate → ship), read the inherited orchestration doc.

This file holds:
- Project-specific decisions on top of the universal lifecycle
- Deployment sequence + release cadence
- Client-communication rhythm (if applicable)
- Project-specific hooks / archetype notes / handler choices

---

## Project archetypes declared

**PROJECT_ARCHETYPES:** {{ARCHETYPES}}  (e.g. `mobile, api-backend`)

Praxis inherits the matching archetype libraries at `docs/agentic-ai/testing/archetypes/`, `docs/agentic-ai/sandboxes/archetypes/`, etc. See the archetype library entries for archetype-specific patterns.

---

## Provider choices

Documented via `/research provider-integration` notes; summarized here for quick reference:

- **Sandbox provider:** {{PROVIDER}} (see `docs/research/YYYY-MM-DD-<provider>.md`)
- **Testing framework:** {{FRAMEWORK}} per archetype
- **Mutation tool:** {{TOOL}}
- **Transcription (spec-processing voice handler):** {{TOOL}}
- **OCR (spec-processing image/PDF handler):** {{TOOL}}
- **Other project-specific tooling:** ...

---

## Deployment sequence

{{PROJECT_SPECIFIC_DEPLOY_SEQUENCE}}

<!-- e.g. for a webapp:
1. Backend deploy (Convex push) - via /go deploy dev
2. Client OTA if applicable, else native rebuild - via /go deploy prod
3. Post-deploy smoke via /live-test --run
4. Advance ticket to Verified prod after on-device confirmation

for a CLI:
1. Version bump (semver per SEMVER-DISCIPLINE)
2. Build (cross-platform matrix)
3. Publish to registry - via /go external-write registry
4. Announce - via /go external-write slack
-->

---

## Release cadence

{{RELEASE_CADENCE}}

<!-- e.g. "Weekly release; hotfixes per incident" -->

---

## Client-communication rhythm

{{CLIENT_COMMUNICATION}}

<!-- e.g. "Client DMs land in sources/clients/<slug>/dms/; captured within 24h;
     /ingest run daily; /synthesize into tickets weekly during triage session"
-->

---

## Project-specific hooks

{{PROJECT_HOOKS}}

<!-- Any hooks beyond the praxis-inherited set. E.g.:
- `.claude/hooks/deploy-safety-check.ps1` (fires PreDeploy)
- Custom lint enforcement per docs/standards/standards.md
-->

---

## Cross-project relationships

{{RELATED_PROJECTS}}

<!-- If this project depends on / is depended on by other praxis-managed projects,
     document the interfaces + coupling here.
-->

---

## Emergency escapes (project-specific)

{{PROJECT_EMERGENCY_ESCAPES}}

<!-- Beyond the universal ones in docs/agentic-ai/docs/using.md §Emergency escapes -->

---

## Related

- [`agentic-ai/docs/orchestration.md`](agentic-ai/docs/orchestration.md) — universal praxis lifecycle visualization
- [`agentic-ai/docs/using.md`](agentic-ai/docs/using.md) — universal daily command reference
- [`agentic-ai/docs/pipelines.md`](agentic-ai/docs/pipelines.md) — universal work-archetype pipelines
- [`agentic-ai/VOCAB.md`](agentic-ai/VOCAB.md) — locked vocabulary
- [`../CLAUDE.md`](../CLAUDE.md) — project constitution
