# `docs/sessions/`

Session logs live here — one file per session at `YYYY-MM-DD.md` (or `YYYY-MM-DD-<slug>.md` if multiple sessions same day).

## Convention

The session-log format is inherited from praxis. It lives in the substrate:

- **Format + template + section conventions:** `docs/agentic-ai/session-logs/` (inherited from praxis `agentic-os/session-logs/` at bootstrap).
- **Locked section vocabulary:** see `VOCAB.md` §8 — Shipped / Decisions / Tried, didn't work / Pending on-device verification / Verified this session / Open / Active.

## Rules of thumb

- **Written at session close.** The `consolidate` skill sweeps first; `sync-context` reconciles; the session log is the final narrative artifact.
- **Two distinct verification sections.** "Pending on-device verification" (code shipped this session, not yet verified) and "Verified this session" (items promoted from prior sessions' pending lists). Never merge them — the split is the audit trail. See `VOCAB.md` §2 for the Done-vs-Verified rule.
- **Sections may be empty.** An empty "Shipped" section is a legitimate state (research-only or discovery-only session).
- **Archive at 90 days.** Move to `docs/sessions/archive/YYYY-MM/` during the drift-hygiene sweep.

## See also

- **Praxis abstract:** `docs/agentic-ai/session-logs/` — format, template
- **Praxis skills:** `consolidate`, `sync-context`, `harvest` all write to session logs
- **Vocabulary:** `VOCAB.md` §8 — session log sections
