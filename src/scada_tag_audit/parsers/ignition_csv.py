"""Ignition tag CSV export parser.

Ignition Designer exports tags as CSV with the following typical columns
(Ignition 8.x tag CSV format; column set may vary by tag provider):

    Path, Data Type, OPC Server, OPC Item Path, Engineering Units,
    Format String, Scaled, Scale Mode, Raw Low, Raw High, Scaled Low,
    Scaled High, Deadband, Deadband Mode, Documentation, Value

We normalize to the internal Tag record shape:

    Tag(
        name: str,               # tag path relative to provider
        address: str | None,     # OPC Item Path (PLC address reference)
        data_type: str | None,   # BOOL / Int4 / Float8 / String / etc.
        units: str | None,       # engineering units
        source: str,             # 'ignition'
        raw: dict,               # original row for downstream inspection
    )

We tolerate missing columns and irregular headers (integrators export subsets).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class Tag:
    """Vendor-normalized tag record."""

    name: str
    address: str | None = None
    data_type: str | None = None
    units: str | None = None
    source: str = ""
    raw: dict = field(default_factory=dict)


# Canonical column-name candidates. Ignition CSV headers vary across versions
# and tag-provider types; we accept any of the listed aliases per field.
_COL_ALIASES = {
    "name": ("Path", "Tag Path", "Name", "Tag Name"),
    "address": ("OPC Item Path", "Address", "Item Path", "OPC Path"),
    "data_type": ("Data Type", "DataType", "Type"),
    "units": ("Engineering Units", "Units", "EU", "Unit"),
}


def _pick(row: dict, aliases: tuple[str, ...]) -> str | None:
    """Return first non-empty value for any alias in the row, else None."""
    for key in aliases:
        val = row.get(key)
        if val is not None and val != "":
            return val.strip()
    return None


def parse_ignition_csv(path: str | Path) -> list[Tag]:
    """Parse an Ignition tag CSV export into a list of Tag records.

    Args:
        path: filesystem path to the CSV.

    Returns:
        List of Tag records, one per data row. Empty header-only files return [].
    """
    tags: list[Tag] = []
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            name = _pick(row, _COL_ALIASES["name"])
            if not name:
                continue
            tags.append(
                Tag(
                    name=name,
                    address=_pick(row, _COL_ALIASES["address"]),
                    data_type=_pick(row, _COL_ALIASES["data_type"]),
                    units=_pick(row, _COL_ALIASES["units"]),
                    source="ignition",
                    raw=dict(row),
                )
            )
    return tags


def parse_ignition_iterable(rows: Iterable[dict]) -> list[Tag]:
    """Parse pre-loaded row dicts (useful for tests and in-memory pipelines)."""
    tags: list[Tag] = []
    for row in rows:
        name = _pick(row, _COL_ALIASES["name"])
        if not name:
            continue
        tags.append(
            Tag(
                name=name,
                address=_pick(row, _COL_ALIASES["address"]),
                data_type=_pick(row, _COL_ALIASES["data_type"]),
                units=_pick(row, _COL_ALIASES["units"]),
                source="ignition",
                raw=dict(row),
            )
        )
    return tags
