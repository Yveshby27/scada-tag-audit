"""Drift detection engine.

Compares Ignition HMI-side tags against Rockwell PLC-side tags and surfaces
mismatches integrators typically discover at commissioning-week.

Drift categories (severity ordered):

    ORPHANED_HMI_BINDING   HMI references a PLC tag that does not exist         (red)
    ORPHANED_PLC_TAG       PLC tag not referenced by any HMI tag                (orange, info-only)
    TYPE_MISMATCH          Same tag, incompatible data types PLC vs HMI         (purple)
    NAMING_CONVENTION_DRIFT Reference resolves after normalization only         (yellow)
    UNIT_MISMATCH          HMI has EU, PLC counterpart is present but ambiguous (blue, info)
    EXACT_MATCH            HMI reference to PLC tag with matching type + name   (green)

The HMI-side (Ignition) is the "consumer": it names tags for display purposes
and references PLC tags via OPC Item Path. The PLC-side (Rockwell) is the
"producer": it names tags for logic-structure purposes.

Drift ripples from producer to consumer. A renamed PLC tag orphans every HMI
reference to the old name. That is the failure mode this engine surfaces.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from .parsers.ignition_csv import Tag


class DriftCategory(str, Enum):
    """Categorization of a single drift finding."""

    EXACT_MATCH = "exact_match"
    NAMING_CONVENTION_DRIFT = "naming_convention_drift"
    ORPHANED_HMI_BINDING = "orphaned_hmi_binding"
    ORPHANED_PLC_TAG = "orphaned_plc_tag"
    TYPE_MISMATCH = "type_mismatch"
    UNIT_MISMATCH = "unit_mismatch"


CATEGORY_COLOR = {
    DriftCategory.EXACT_MATCH: "green",
    DriftCategory.NAMING_CONVENTION_DRIFT: "yellow",
    DriftCategory.ORPHANED_HMI_BINDING: "red",
    DriftCategory.ORPHANED_PLC_TAG: "orange",
    DriftCategory.TYPE_MISMATCH: "purple",
    DriftCategory.UNIT_MISMATCH: "blue",
}


CATEGORY_SEVERITY = {
    DriftCategory.ORPHANED_HMI_BINDING: 1,
    DriftCategory.TYPE_MISMATCH: 2,
    DriftCategory.NAMING_CONVENTION_DRIFT: 3,
    DriftCategory.UNIT_MISMATCH: 4,
    DriftCategory.ORPHANED_PLC_TAG: 5,
    DriftCategory.EXACT_MATCH: 6,
}


@dataclass
class DriftFinding:
    """A single reconciliation result between HMI and PLC tag universes."""

    category: DriftCategory
    hmi_tag: Tag | None
    plc_tag: Tag | None
    reference_key: str
    notes: str = ""

    @property
    def color(self) -> str:
        return CATEGORY_COLOR[self.category]

    @property
    def severity(self) -> int:
        return CATEGORY_SEVERITY[self.category]


_STRIP_PREFIXES = ("HMI_", "TAG_", "IO_", "PLC_", "SCADA_", "hmi_", "tag_", "io_", "plc_")
_SEPARATOR_RE = re.compile(r"[\s\-\._]+")


def normalize_name(name: str) -> str:
    """Return a canonical form for name comparison.

    Rules:
        1. Strip common integrator prefixes
        2. Case-fold
        3. Insert underscore at letter-digit boundary
        4. Collapse [space _ - .] runs into single underscore
    """
    for prefix in _STRIP_PREFIXES:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    name = name.casefold()
    name = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", "_", name)
    name = _SEPARATOR_RE.sub("_", name)
    return name.strip("_")


def extract_plc_reference(hmi_tag: Tag) -> str | None:
    """Pull the PLC-side tag name that an HMI tag references, from OPC Item Path."""
    if not hmi_tag.address:
        return hmi_tag.name
    address = hmi_tag.address
    if "]" in address:
        address = address.rsplit("]", 1)[1]
    for sep in (".", ":"):
        if sep in address:
            address = address.rsplit(sep, 1)[1]
    return address.strip() or None


_TYPE_COMPAT = {
    "BOOL": {"Boolean", "Bit"},
    "SINT": {"Int1", "Int2", "Int4", "Short", "Byte"},
    "INT": {"Int2", "Int4", "Short"},
    "DINT": {"Int4", "Long", "Int8"},
    "LINT": {"Int8", "Long"},
    "REAL": {"Float4", "Float8", "Float", "Double"},
    "LREAL": {"Float8", "Double"},
    "STRING": {"String"},
}


def _types_compatible(plc_type: str | None, hmi_type: str | None) -> bool:
    if not plc_type or not hmi_type:
        return True
    if plc_type == hmi_type:
        return True
    compat = _TYPE_COMPAT.get(plc_type.upper())
    if compat is None:
        return False
    return hmi_type in compat


def reconcile(hmi_tags: list[Tag], plc_tags: list[Tag]) -> list[DriftFinding]:
    """Cross-reference HMI tags with PLC tags. Returns findings ordered by severity."""
    findings: list[DriftFinding] = []

    plc_by_exact: dict[str, Tag] = {t.name: t for t in plc_tags}
    plc_by_norm: dict[str, Tag] = {normalize_name(t.name): t for t in plc_tags}
    referenced_plc: set[str] = set()

    for hmi in hmi_tags:
        ref = extract_plc_reference(hmi)
        if not ref:
            continue

        exact = plc_by_exact.get(ref)
        if exact is not None:
            referenced_plc.add(exact.name)
            if not _types_compatible(exact.data_type, hmi.data_type):
                findings.append(
                    DriftFinding(
                        category=DriftCategory.TYPE_MISMATCH,
                        hmi_tag=hmi,
                        plc_tag=exact,
                        reference_key=ref,
                        notes=f"PLC type '{exact.data_type}' incompatible with HMI type '{hmi.data_type}'",
                    )
                )
            elif hmi.units:
                findings.append(
                    DriftFinding(
                        category=DriftCategory.UNIT_MISMATCH,
                        hmi_tag=hmi,
                        plc_tag=exact,
                        reference_key=ref,
                        notes=f"HMI declares units '{hmi.units}'; PLC tag has no unit metadata (Rockwell L5X does not store EU).",
                    )
                )
            else:
                findings.append(
                    DriftFinding(
                        category=DriftCategory.EXACT_MATCH,
                        hmi_tag=hmi,
                        plc_tag=exact,
                        reference_key=ref,
                    )
                )
            continue

        norm_ref = normalize_name(ref)
        norm_match = plc_by_norm.get(norm_ref)
        if norm_match is not None:
            referenced_plc.add(norm_match.name)
            # Type mismatch takes precedence over naming drift when both apply
            # (v0.1.1: bug fix — earlier releases only checked types in exact-match branch).
            if not _types_compatible(norm_match.data_type, hmi.data_type):
                findings.append(
                    DriftFinding(
                        category=DriftCategory.TYPE_MISMATCH,
                        hmi_tag=hmi,
                        plc_tag=norm_match,
                        reference_key=ref,
                        notes=f"PLC type '{norm_match.data_type}' incompatible with HMI type '{hmi.data_type}'. Also has naming drift: HMI references '{ref}' (normalized '{norm_ref}') vs PLC '{norm_match.name}'.",
                    )
                )
            else:
                findings.append(
                    DriftFinding(
                        category=DriftCategory.NAMING_CONVENTION_DRIFT,
                        hmi_tag=hmi,
                        plc_tag=norm_match,
                        reference_key=ref,
                        notes=f"HMI references '{ref}', normalized to '{norm_ref}'; PLC tag is '{norm_match.name}'. Reference resolves under normalization but not exact match.",
                    )
                )
            continue

        findings.append(
            DriftFinding(
                category=DriftCategory.ORPHANED_HMI_BINDING,
                hmi_tag=hmi,
                plc_tag=None,
                reference_key=ref,
                notes=f"HMI references PLC tag '{ref}'; no such tag in PLC export (exact or normalized).",
            )
        )

    for plc in plc_tags:
        if plc.name not in referenced_plc:
            findings.append(
                DriftFinding(
                    category=DriftCategory.ORPHANED_PLC_TAG,
                    hmi_tag=None,
                    plc_tag=plc,
                    reference_key=plc.name,
                    notes="PLC tag defined but not referenced by any HMI tag in this export.",
                )
            )

    findings.sort(key=lambda f: (f.severity, f.reference_key))
    return findings
