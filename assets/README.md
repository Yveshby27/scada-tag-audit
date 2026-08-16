# `assets/`

Project assets live here — client-provided visual + design reference material. Screenshots, Figma exports, spec PDFs, voice memos not yet transcribed.

## Convention

The assets convention is inherited from praxis. It lives in the substrate:

- **Convention:** `docs/agentic-ai/assets-convention.md` (inherited from praxis `docs/assets-convention.md` at bootstrap).

## Structure — two homes

```
assets/
├── client/       tracked, curated, grep-searchable
└── inbox/        gitignored, ephemeral, pressure-release valve
```

## Rules of thumb

- **`assets/client/`** — canonical, tracked. Named `YYYY-MM-DD-<source>-<what>.<ext>`. Referenced from tickets via `attachments:` frontmatter. Update `assets/client/README.md` index as files land.
- **`assets/inbox/`** — dump raw files on receipt, no naming ceremony. Triage weekly: graduate keepers to `client/`, delete the rest. Nothing lives here > 7 days without a decision.
- **`.gitignore` snippet** — add to project's `.gitignore`:
  ```
  assets/inbox/*
  !assets/inbox/README.md
  !assets/inbox/.gitkeep
  ```
- **What NOT to put here:** source-code build assets (icons, splash, fonts — those live in `mobile-app/assets/`, `admin-web-app/public/`, etc.), files > 10 MB (link from blob storage), secrets.

## Distinction from Sources

- **Assets** = visual/design reference. Figma, screenshots, spec PDFs.
- **Sources** = raw communications. Voice memos, DMs, emails, calls. Lives under `sources/`.

Overlap edge case: a screenshot pasted inside a client DM lives in Sources with the DM (that's the said/sent record). A standalone Figma export lives in Assets.

## See also

- **Praxis convention:** `docs/agentic-ai/assets-convention.md`
- **Sources spine:** `docs/agentic-ai/sources/README.md`
