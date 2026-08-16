# `sources/`

Project sources live here — the said/sent record. Voice memos, DMs, emails, call transcripts, business briefs.

## Convention

The sources convention is inherited from praxis. It lives in the substrate:

- **Convention + provenance sidecar template:** `docs/agentic-ai/sources/` (inherited from praxis `agentic-os/sources/` at bootstrap).
- **Cross-reference:** `VOCAB.md` §5 — Sources is a primary spine, not a phase.

## Structure

```
sources/
├── clients/<slug>/{voice,dms,emails,calls}/
├── operator/{voice,notes}/
└── business/
```

## Rules of thumb

- **Naming:** `YYYY-MM-DD-<channel>-<subject>.<ext>` — e.g. `2026-07-19-voice-payments-concerns.m4a`.
- **Provenance sidecar:** every non-markdown source gets a paired `.md` sidecar with matching filename stem. Sidecar carries `source_type`, `captured_at`, `channel`, `participants`, `tickets_derived`, `plans_derived`, `transcription_status`.
- **Git-tracked by default.** Sources are permanent record. Exceptions (sensitive material, huge binaries) get flagged separately.
- **Feeds `/intake`.** Save the source first, then invoke `/intake` pointing at the path. Tickets carry `derived_from:` back to the source.

## See also

- **Praxis abstract:** `docs/agentic-ai/sources/README.md` — full convention
- **Praxis skills:** `/intake` consumes sources; every actionable request starts here
