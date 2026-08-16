"""End-to-end test: parse fixtures, reconcile, verify expected drift categories."""

from pathlib import Path

from scada_tag_audit.drift_engine import DriftCategory, reconcile
from scada_tag_audit.parsers.ignition_csv import parse_ignition_csv
from scada_tag_audit.parsers.rockwell_l5x import parse_rockwell_l5x
from scada_tag_audit.report_gen import render_report

FIX = Path(__file__).parent / "fixtures"


def test_parse_ignition_csv():
    tags = parse_ignition_csv(FIX / "ignition_tags_sample.csv")
    assert len(tags) == 11
    motor_run = next(t for t in tags if t.name == "Motors/Motor1_Run")
    assert motor_run.address == "[Global_PLC]Motor1_Run"
    assert motor_run.data_type == "Boolean"


def test_parse_rockwell_l5x():
    tags = parse_rockwell_l5x(FIX / "rockwell_tags_sample.L5X")
    assert len(tags) == 12
    motor_run = next(t for t in tags if t.name == "Motor1_Run")
    assert motor_run.data_type == "BOOL"


def test_reconcile_produces_expected_categories():
    hmi = parse_ignition_csv(FIX / "ignition_tags_sample.csv")
    plc = parse_rockwell_l5x(FIX / "rockwell_tags_sample.L5X")
    findings = reconcile(hmi, plc)

    by_cat = {cat: [] for cat in DriftCategory}
    for f in findings:
        by_cat[f.category].append(f)

    assert len(by_cat[DriftCategory.ORPHANED_HMI_BINDING]) == 1
    assert by_cat[DriftCategory.ORPHANED_HMI_BINDING][0].reference_key == "OldValve_Cmd"

    assert len(by_cat[DriftCategory.TYPE_MISMATCH]) == 1
    assert by_cat[DriftCategory.TYPE_MISMATCH][0].reference_key == "Motor2_Amps"

    naming_refs = {f.reference_key for f in by_cat[DriftCategory.NAMING_CONVENTION_DRIFT]}
    assert "Pump2_Run" in naming_refs
    assert "Temp1_C" in naming_refs

    orphan_plc_names = {f.plc_tag.name for f in by_cat[DriftCategory.ORPHANED_PLC_TAG]}
    assert "UnusedPlcTag_1" in orphan_plc_names
    assert "UnusedPlcTag_2" in orphan_plc_names

    assert len(by_cat[DriftCategory.EXACT_MATCH]) >= 1


def test_render_report_produces_valid_html():
    hmi = parse_ignition_csv(FIX / "ignition_tags_sample.csv")
    plc = parse_rockwell_l5x(FIX / "rockwell_tags_sample.L5X")
    findings = reconcile(hmi, plc)

    html = render_report(
        findings=findings,
        hmi_source="ignition_tags_sample.csv",
        plc_source="rockwell_tags_sample.L5X",
        hmi_total=len(hmi),
        plc_total=len(plc),
    )
    assert "<!DOCTYPE html>" in html
    assert "SCADA tag drift audit" in html
    assert "OldValve_Cmd" in html
    assert "Motor2_Amps" in html
