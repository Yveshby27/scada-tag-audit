"""CLI orchestration + double-click file-picker fallback for scada-tag-audit.

Two invocation modes:

    scada-tag-audit --ignition tags.csv --rockwell routine.L5X --output report.html
        (traditional CLI, CI-friendly)

    scada-tag-audit
        (no args; opens Windows file-picker dialogs for the two inputs,
         writes report next to the Ignition CSV, opens report in the default browser.
         This is the double-click path for GUI-culture integrators.)
"""

from __future__ import annotations

import sys
import webbrowser
from collections import Counter
from pathlib import Path

import click

from . import __version__
from .drift_engine import reconcile
from .parsers.ignition_csv import parse_ignition_csv
from .parsers.rockwell_l5x import parse_rockwell_l5x
from .report_gen import render_report, write_report


def _prompt_for_file(title: str, filetypes: list[tuple[str, str]]) -> Path | None:
    """Open a native file-picker dialog. Returns None if user cancels."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        return None

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path_str = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    if not path_str:
        return None
    return Path(path_str)


def _run(ignition_path: Path, rockwell_path: Path, output_path: Path, open_after: bool) -> int:
    """Core analysis run. Returns exit code (0 = clean, 1 = actionable drift, 2 = error)."""
    click.echo(f"Reading Ignition CSV: {ignition_path}")
    try:
        hmi_tags = parse_ignition_csv(ignition_path)
    except Exception as exc:
        click.echo(f"  ERROR: {exc}", err=True)
        return 2
    click.echo(f"  Parsed {len(hmi_tags)} HMI tags.")

    click.echo(f"Reading Rockwell L5X: {rockwell_path}")
    try:
        plc_tags = parse_rockwell_l5x(rockwell_path)
    except Exception as exc:
        click.echo(f"  ERROR: {exc}", err=True)
        return 2
    click.echo(f"  Parsed {len(plc_tags)} PLC tags.")

    click.echo("Running drift reconciliation ...")
    findings = reconcile(hmi_tags, plc_tags)

    counts = Counter(f.category.value for f in findings)
    for cat, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        click.echo(f"  {cat}: {count}")

    html = render_report(
        findings=findings,
        hmi_source=ignition_path.name,
        plc_source=rockwell_path.name,
        hmi_total=len(hmi_tags),
        plc_total=len(plc_tags),
        version=__version__,
    )
    written = write_report(html, output_path)
    click.echo(f"\nReport written to: {written}")

    actionable = sum(
        counts.get(k, 0)
        for k in ("orphaned_hmi_binding", "type_mismatch", "naming_convention_drift")
    )

    if open_after:
        try:
            webbrowser.open(written.as_uri())
        except Exception:
            pass

    if actionable:
        click.echo(f"\n{actionable} actionable finding(s). Open the report before commissioning.")
        return 1
    click.echo("\nNo actionable drift surfaced. Report includes informational and match rows.")
    return 0


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--ignition",
    "ignition_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to Ignition tag CSV export. Omit to open a file-picker dialog.",
)
@click.option(
    "--rockwell",
    "rockwell_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to Rockwell Studio 5000 L5X export. Omit to open a file-picker dialog.",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Path where the HTML report will be written. Default: 'scada-drift-report.html' next to the Ignition CSV.",
)
@click.option(
    "--no-open",
    "no_open",
    is_flag=True,
    default=False,
    help="Do not auto-open the report in the default browser after generation.",
)
@click.version_option(__version__)
def main(
    ignition_path: Path | None,
    rockwell_path: Path | None,
    output_path: Path | None,
    no_open: bool,
) -> None:
    """Reconcile Ignition HMI tags against Rockwell PLC tags; write drift report.

    Double-click the .exe with no arguments to use the file-picker dialogs.
    """
    if ignition_path is None:
        click.echo("No --ignition path provided; opening file picker ...")
        ignition_path = _prompt_for_file(
            title="Select Ignition tag CSV export",
            filetypes=[("Ignition tag CSV", "*.csv"), ("All files", "*.*")],
        )
        if ignition_path is None:
            click.echo("No Ignition CSV selected. Exiting.", err=True)
            sys.exit(2)

    if rockwell_path is None:
        click.echo("No --rockwell path provided; opening file picker ...")
        rockwell_path = _prompt_for_file(
            title="Select Rockwell Studio 5000 L5X export",
            filetypes=[("Rockwell L5X", "*.L5X *.l5x"), ("All files", "*.*")],
        )
        if rockwell_path is None:
            click.echo("No Rockwell L5X selected. Exiting.", err=True)
            sys.exit(2)

    if output_path is None:
        output_path = ignition_path.parent / "scada-drift-report.html"

    exit_code = _run(ignition_path, rockwell_path, output_path, open_after=not no_open)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
