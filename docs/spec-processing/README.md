# Spec Processing

The 5-stage raw-material processing workflow at project scope. Full contracts inherited from praxis at [`../agentic-ai/spec-processing/`](../agentic-ai/spec-processing/).

**Workflow:** Raw → Ingest → Structured findings → Synthesize → Draft artifact → Review → Committed. See [`../agentic-ai/spec-processing/STAGES.md`](../agentic-ai/spec-processing/STAGES.md).

---

## What lives here

```
docs/spec-processing/
├── README.md              ← this file
└── processing-log.md      ← append-only ledger of /ingest invocations (audit trail)
```

Adapter/handler code lives at `.claude/spec-processing/handlers/` (project-side).

---

## Daily use

- **Raw material arrives?** Save under `sources/<subdir>/` first (per Sources spine convention).
- **Ingest it:** `/ingest sources/<path>` — dispatches to appropriate handler; produces typed extraction entries in sidecar.
- **Compose artifact:** `/synthesize <sources...> --into <spec|plan|scenario|adr|ticket>` — drafts artifact drawing on the typed entries.
- **Review:** operator reads the draft; addresses `decision-needed` inline; artifact advances to `reviewed`.
- **Commit:** `/go commit --scope <artifact>` — operator opens gate; commit happens.

Trivial one-liners can skip `/ingest` and go straight to `/intake` (which is the specialized shortcut for source → ticket).

---

## Handlers

Praxis defines contracts for 8 source-type handlers:

- **voice** — transcribe + diarize + extract
- **dm** — parse thread + extract
- **email** — parse thread + separate signal from noise + extract
- **call** — voice handler first, then topic segmentation + extract
- **image** — OCR + LLM-vision description + extract
- **video** — audio → voice handler + scene detection + keyframe → image handler
- **pdf** — text extraction (or OCR if scanned) + structure parsing + extract
- **brief** — parse structure + extract

Handler code (invoking Whisper / Tesseract / Claude vision / pdfplumber / etc.) lives at `.claude/spec-processing/handlers/<type>.<ext>` — project-authored per your stack. See [`../agentic-ai/spec-processing/HANDLERS.md`](../agentic-ai/spec-processing/HANDLERS.md) for the contract.

---

## Extraction schema

Every extracted entry is one of 7 typed shapes:
- **finding** — observation about current state
- **requirement** — must-be-true
- **constraint** — bounded rule
- **alternative** — considered option with verdict
- **stakeholder-position** — named person's stated stance
- **decision-needed** — open decision blocking progress
- **question** — clarification the source can't answer

See [`../agentic-ai/spec-processing/EXTRACTION-SCHEMA.md`](../agentic-ai/spec-processing/EXTRACTION-SCHEMA.md) for field definitions + usage per artifact type.

---

## Backward compatibility

Legacy sidecars with `insights_extracted[]` as string entries continue to work. `/synthesize` treats them as `finding` type with `confidence: low`. Re-running `/ingest` on a legacy source produces typed entries alongside (both preserved).

---

## Related

- [`../agentic-ai/spec-processing/README.md`](../agentic-ai/spec-processing/README.md) — full workflow home
- [`../agentic-ai/spec-processing/HANDLERS.md`](../agentic-ai/spec-processing/HANDLERS.md) — 8 handler contracts
- [`../agentic-ai/spec-processing/EXTRACTION-SCHEMA.md`](../agentic-ai/spec-processing/EXTRACTION-SCHEMA.md) — 7 typed entry shapes
- [`../agentic-ai/spec-processing/STAGES.md`](../agentic-ai/spec-processing/STAGES.md) — 5 stages
- [`../agentic-ai/sources/README.md`](../agentic-ai/sources/README.md) — Sources spine (extended)
