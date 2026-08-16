# Collaboration

The **Freedom Doctrine** at project scope. Full contracts inherited from praxis at [`../agentic-ai/collaboration/`](../agentic-ai/collaboration/). This directory holds project data (the initiative log).

**Four-legged doctrine:**

1. **Freedom** — AI proposes freely inside the workspace; unbounded creative generation during tasks
2. **Gate** — you commit and you push; nothing user-visible ships without your `/go <scope>`
3. **Transparency** — AI nudges its thinking as it works; cost is not a constraint
4. **Initiative** — AI surfaces proposals + adversarial findings about praxis itself unprompted

Full DOCTRINE: [`../agentic-ai/collaboration/DOCTRINE.md`](../agentic-ai/collaboration/DOCTRINE.md).

---

## What lives here

```
docs/collaboration/
├── README.md              ← this file
└── initiative-log.md      ← append-only ledger of initiatives about praxis
```

---

## Daily use

- **Working a task?** The AI can propose alternatives / disagreements / rescopes via `/propose <title>` — proposals land in the current context brief's `proposals[]` section.
- **AI notices something about praxis?** It'll file `/initiative` — check the log periodically.
- **Ready to commit?** Run `/end-of-task-review` first (the pre-gate ritual). Read the output. Then `/go commit --scope "<feature>"` or narrower.
- **Ready to push?** `/go push` or `/go push origin/main`.
- **Broad delegation for a pairing session?** `/go all --until stop`. Close with `/gate close` at session end.
- **Check what scopes are outstanding?** `/gate status`.

---

## Initiative log format

Append-only. Never delete entries — rejected ones stay for audit.

Per entry:

```markdown
## I-NNN · YYYY-MM-DD · [class] · status

**Title:** ...
**Body:** ...
**Recommendation:** ...
**Affected:** ...
**Cross-links:** ...
```

Classes: `proposal`, `bug`, `security`, `efficiency`, `docs`, `coupling`, `edge-case`, `naming`, `testing`.

Statuses: `surfaced → discussed → adopted | rejected | parked | superseded`.

Full format spec: [`../agentic-ai/collaboration/INITIATIVE.md`](../agentic-ai/collaboration/INITIATIVE.md).

---

## Operator-side discipline

The doctrine dies without operator care. Repair patterns:

- **Punished a wild proposal too hard** → next session, explicitly re-invite: "I want to hear all your ideas."
- **Curt "k" that killed transparency** → re-invite: "give me nudges as you work; cost is not a concern."
- **Initiatives piling up in `surfaced`** → weekly review: "walk me through open initiatives."
- **Committed / pushed without `/go`** → audit `.claude/state/gate-scope.json`; re-establish practice.
- **Broad `/go all --until stop` never closed** → close with `/gate close` at natural session ends.

Full operator-side content in each leg contract: [`../agentic-ai/collaboration/FREEDOM.md`](../agentic-ai/collaboration/FREEDOM.md), [`../agentic-ai/collaboration/GATE.md`](../agentic-ai/collaboration/GATE.md), [`../agentic-ai/collaboration/TRANSPARENCY.md`](../agentic-ai/collaboration/TRANSPARENCY.md), [`../agentic-ai/collaboration/INITIATIVE.md`](../agentic-ai/collaboration/INITIATIVE.md).

---

## Related

- [`../agentic-ai/collaboration/README.md`](../agentic-ai/collaboration/README.md) — full doctrine home
- [`../agentic-ai/collaboration/DOCTRINE.md`](../agentic-ai/collaboration/DOCTRINE.md) — the four legs, mutual reinforcement, failure modes
- [`../agentic-ai/playbooks/collaboration-doctrine.md`](../agentic-ai/playbooks/collaboration-doctrine.md) — deep methodology
