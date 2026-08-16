# scada-tag-audit

Pre-commissioning cross-vendor tag database drift audit for SCADA integrators.

Reads an Ignition HMI tag CSV export + a Rockwell Studio 5000 L5X export, reconciles them, and produces a self-contained HTML report flagging the drift patterns that break faceplates at commissioning-week: orphaned HMI bindings, type mismatches, and naming-convention drift between what the PLC exports and what the HMI references.

Runs on the integrator's laptop. No cloud upload. No vendor API dependency. No client data leaves the machine.

## Install

**Windows .exe** (recommended for integrators): download the latest from [Releases](https://github.com/Yveshby27/scada-tag-audit/releases).

Double-click to run (opens file-picker dialogs for both inputs), or invoke from a terminal with arguments.

**Python package** (for CLI-culture users):

```
pip install scada-tag-audit
```

Requires Python 3.10+.

## Quick start

Double-click `scada-tag-audit.exe` and select the two exports when prompted. Report opens in your default browser.

Or from a terminal:

```
scada-tag-audit --ignition path/to/tags.csv --rockwell path/to/routine.L5X --output drift-report.html
```

The HTML report is self-contained (no external dependencies), safe to email or archive.

## What it flags

| Category | Color | Severity | Meaning |
|---|---|---|---|
| Orphaned HMI binding | Red | High | HMI references a PLC tag that does not exist. Faceplate breaks at go-live. |
| Type mismatch | Purple | High | Same tag, incompatible data types PLC-side vs HMI-side (e.g. PLC REAL, HMI Int4). |
| Naming convention drift | Yellow | Medium | Reference resolves under normalization but not exact match (e.g. `Pump2_Run` vs `Pump_2_Run`). |
| Unit mismatch | Blue | Info | HMI declares engineering units; PLC counterpart has no EU metadata. |
| Orphaned PLC tag | Orange | Info | PLC tag exists but no HMI tag references it. Cleanup opportunity. |
| Exact match | Green | None | Reference resolves cleanly with compatible types. |

## How it works

The engine extracts PLC-side references from Ignition's OPC Item Paths (e.g. `[Global_PLC]Motor1_Run` → `Motor1_Run`) and matches them against Rockwell tag names from the L5X. When exact matches fail, it retries under name normalization (case-fold, prefix strip, separator collapse, letter-digit boundary insertion). Every reference that fails to resolve becomes an orphan. Every match with incompatible data types becomes a type-mismatch finding.

The HTML report groups findings by severity: actionable drift (commissioning breakers) at the top, informational rows below, exact matches collapsed at the bottom.

## Development

```
git clone https://github.com/Yveshby27/scada-tag-audit
cd scada-tag-audit
pip install -e ".[dev]"
pytest
```

## v0.1 scope + roadmap

Alpha. Ignition tag CSV + Rockwell L5X only. Wonderware .aaGDB, Kepware XML, FactoryTalk, Iconics, and OPC UA custom information models are on the v0.2+ roadmap if the wedge holds.

## Background

Notes on why this exists: [What small SCADA integrators actually ship when the tag database drifts](https://habchy.dev/research/scada-integrator-tag-drift).

If you run a small integrator shop (2-15 EE) delivering multi-vendor projects and the pain shape matches what you see, reach out. LinkedIn or email in the article.

## License

MIT
