"""Self-contained HTML report generator.

Produces a single-file HTML document with embedded CSS and no external
dependencies. Integrator emails the report or opens locally; no server, no
uploads, no network calls.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Template

from .drift_engine import CATEGORY_COLOR, DriftCategory, DriftFinding

_TEMPLATE = Template(
    """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SCADA Tag Drift Audit</title>
<style>
  :root {
    --fg: #1a1a1a;
    --muted: #6b6b6b;
    --bg: #ffffff;
    --border: #e0e0e0;
    --green: #16a34a;
    --yellow: #ca8a04;
    --red: #dc2626;
    --orange: #ea580c;
    --purple: #9333ea;
    --blue: #2563eb;
  }
  body {
    font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    color: var(--fg);
    background: var(--bg);
    max-width: 1200px;
    margin: 40px auto;
    padding: 0 24px;
  }
  h1 { font-size: 24px; margin-bottom: 4px; }
  .subtitle { color: var(--muted); margin-bottom: 32px; font-size: 13px; }
  .summary { display: flex; gap: 24px; flex-wrap: wrap; margin-bottom: 32px;
             padding: 16px 20px; border: 1px solid var(--border); border-radius: 6px; background: #fafafa; }
  .summary-item { display: flex; flex-direction: column; }
  .summary-count { font-size: 24px; font-weight: 600; }
  .summary-label { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
  table { width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 13px; }
  th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }
  th { background: #f5f5f5; font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.3px; color: var(--muted); }
  .cat-badge { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 11px;
               font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; color: #fff; white-space: nowrap; }
  .cat-green { background: var(--green); }
  .cat-yellow { background: var(--yellow); }
  .cat-red { background: var(--red); }
  .cat-orange { background: var(--orange); }
  .cat-purple { background: var(--purple); }
  .cat-blue { background: var(--blue); }
  .mono { font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; }
  .notes { color: var(--muted); font-size: 12px; max-width: 400px; }
  .footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--border);
            color: var(--muted); font-size: 12px; text-align: center; }
  .footer a { color: var(--muted); }
  section h2 { font-size: 16px; margin-top: 40px; margin-bottom: 8px; }
</style>
</head>
<body>

<h1>SCADA tag drift audit</h1>
<div class="subtitle">
  Ignition HMI export ({{ hmi_source }}) reconciled against Rockwell PLC export ({{ plc_source }}).
  Generated {{ generated_at }}.
</div>

<div class="summary">
  {% for cat, count in summary %}
  <div class="summary-item">
    <div class="summary-count">{{ count }}</div>
    <div class="summary-label"><span class="cat-badge cat-{{ colors[cat] }}">{{ cat }}</span></div>
  </div>
  {% endfor %}
  <div class="summary-item">
    <div class="summary-count">{{ hmi_total }}</div>
    <div class="summary-label">HMI tags</div>
  </div>
  <div class="summary-item">
    <div class="summary-count">{{ plc_total }}</div>
    <div class="summary-label">PLC tags</div>
  </div>
</div>

{% if actionable %}
<section>
<h2>Actionable drift ({{ actionable|length }})</h2>
<p class="subtitle">Findings that would surface at commissioning-week: broken HMI bindings, type mismatches, naming convention drift.</p>
<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Reference</th>
      <th>HMI tag</th>
      <th>PLC tag</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    {% for f in actionable %}
    <tr>
      <td><span class="cat-badge cat-{{ f.color }}">{{ f.category.value }}</span></td>
      <td class="mono">{{ f.reference_key }}</td>
      <td class="mono">{{ f.hmi_tag.name if f.hmi_tag else "" }}{% if f.hmi_tag and f.hmi_tag.data_type %} ({{ f.hmi_tag.data_type }}){% endif %}</td>
      <td class="mono">{{ f.plc_tag.name if f.plc_tag else "" }}{% if f.plc_tag and f.plc_tag.data_type %} ({{ f.plc_tag.data_type }}){% endif %}</td>
      <td class="notes">{{ f.notes }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
</section>
{% endif %}

{% if info_findings %}
<section>
<h2>Informational ({{ info_findings|length }})</h2>
<p class="subtitle">Orphaned PLC tags and unit-metadata gaps. Not commissioning-breaking; may indicate cleanup opportunity.</p>
<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Tag</th>
      <th>Type</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    {% for f in info_findings %}
    <tr>
      <td><span class="cat-badge cat-{{ f.color }}">{{ f.category.value }}</span></td>
      <td class="mono">{{ (f.plc_tag or f.hmi_tag).name }}</td>
      <td class="mono">{{ (f.plc_tag or f.hmi_tag).data_type or "" }}</td>
      <td class="notes">{{ f.notes }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
</section>
{% endif %}

{% if matches %}
<section>
<h2>Exact matches ({{ matches|length }})</h2>
<details>
<summary style="cursor: pointer; color: var(--muted); font-size: 13px;">Expand to see all clean references</summary>
<table>
  <thead>
    <tr>
      <th>Reference</th>
      <th>HMI tag</th>
      <th>PLC tag</th>
    </tr>
  </thead>
  <tbody>
    {% for f in matches %}
    <tr>
      <td class="mono">{{ f.reference_key }}</td>
      <td class="mono">{{ f.hmi_tag.name }}</td>
      <td class="mono">{{ f.plc_tag.name }} ({{ f.plc_tag.data_type or "" }})</td>
    </tr>
    {% endfor %}
  </tbody>
</details>
</section>
{% endif %}

<div class="footer">
Generated by <a href="https://github.com/Yveshby27/scada-tag-audit">scada-tag-audit</a> v{{ version }}.
Report is self-contained: no external network calls, no data leaves your machine.
</div>

</body>
</html>
"""
)


def render_report(
    findings: list[DriftFinding],
    hmi_source: str,
    plc_source: str,
    hmi_total: int,
    plc_total: int,
    version: str = "0.1.0",
) -> str:
    """Render findings into a self-contained HTML document."""
    counts = Counter(f.category.value for f in findings)
    summary = [(cat.value, counts.get(cat.value, 0)) for cat in DriftCategory]
    colors = {cat.value: CATEGORY_COLOR[cat] for cat in DriftCategory}

    actionable_cats = {
        DriftCategory.ORPHANED_HMI_BINDING,
        DriftCategory.TYPE_MISMATCH,
        DriftCategory.NAMING_CONVENTION_DRIFT,
    }
    info_cats = {DriftCategory.ORPHANED_PLC_TAG, DriftCategory.UNIT_MISMATCH}
    match_cats = {DriftCategory.EXACT_MATCH}

    actionable = [f for f in findings if f.category in actionable_cats]
    info_findings = [f for f in findings if f.category in info_cats]
    matches = [f for f in findings if f.category in match_cats]

    return _TEMPLATE.render(
        summary=summary,
        colors=colors,
        hmi_source=hmi_source,
        plc_source=plc_source,
        hmi_total=hmi_total,
        plc_total=plc_total,
        actionable=actionable,
        info_findings=info_findings,
        matches=matches,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        version=version,
    )


def write_report(html: str, output_path: str | Path) -> Path:
    """Write HTML to output_path; return resolved Path."""
    output_path = Path(output_path)
    output_path.write_text(html, encoding="utf-8")
    return output_path.resolve()
