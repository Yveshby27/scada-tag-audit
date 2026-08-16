"""Rockwell Studio 5000 L5X export parser.

L5X is XML. We walk all <Tag> elements at any depth (controller-scoped +
program-scoped + add-on-instruction-scoped) and normalize to Tag records.

Rockwell tag schema (abbreviated):

    <Tag Name="Motor1_Run"
         TagType="Base"           # Base | Alias | Produced | Consumed
         DataType="BOOL"          # BOOL / SINT / INT / DINT / REAL / STRING / UDT_name
         Radix="Decimal"
         ExternalAccess="Read/Write"
         AliasFor="OtherTag">     # only present when TagType=Alias
        <Description><![CDATA[Motor 1 run status]]></Description>
    </Tag>

We do not resolve alias chains in v0.1 (drift-engine treats aliases as
first-class references and flags dangling AliasFor separately).

Rockwell tags do not carry engineering units natively (EU lives in the
controller's HMI tag alias layer or PlantPAx equivalents). We leave Tag.units
as None for Rockwell rows.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from .ignition_csv import Tag


def parse_rockwell_l5x(path: str | Path) -> list[Tag]:
    """Parse a Rockwell L5X export into a list of Tag records."""
    tags: list[Tag] = []
    path = Path(path)
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        raise ValueError(f"Malformed L5X at {path}: {exc}") from exc

    root = tree.getroot()
    for tag_el in root.iter("Tag"):
        name = tag_el.get("Name")
        if not name:
            continue

        description_el = tag_el.find("Description")
        description = ""
        if description_el is not None and description_el.text:
            description = description_el.text.strip()

        data_type = tag_el.get("DataType")
        alias_for = tag_el.get("AliasFor")

        raw = {k: v for k, v in tag_el.attrib.items()}
        if description:
            raw["Description"] = description

        tags.append(
            Tag(
                name=name,
                address=alias_for,
                data_type=data_type,
                units=None,
                source="rockwell",
                raw=raw,
            )
        )

    return tags
