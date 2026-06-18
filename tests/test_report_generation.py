from pathlib import Path

import yaml

from aipr.models import UseCase
from aipr.report import render_report, write_report
from aipr.scoring import assess


def test_report_contains_score_and_findings() -> None:
    data = yaml.safe_load(Path("examples/rfq-assistant/usecase.yaml").read_text())
    assessment = assess(UseCase.model_validate(data))

    report = render_report(assessment)

    assert "# AI Production Readiness Report: RFQ Sales Assistant" in report
    assert "Score:" in report
    assert "Critical Findings" in report
    assert "Production gate:" in report


def test_report_styles_render_different_outputs() -> None:
    data = yaml.safe_load(Path("examples/rfq-assistant/usecase.yaml").read_text())
    assessment = assess(UseCase.model_validate(data))

    executive = render_report(assessment, style="executive")
    engineering = render_report(assessment, style="engineering")
    balanced = render_report(assessment, style="balanced")

    assert executive.startswith("# Executive AI Readiness Brief")
    assert "Required Decisions" in executive
    assert engineering.startswith("# Engineering AI Production Readiness Report")
    assert "Control Inputs" in engineering
    assert balanced.startswith("# AI Production Readiness Report")


def test_write_report_creates_parent_directories(tmp_path: Path) -> None:
    usecase = UseCase(name="Small Internal Assistant")
    assessment = assess(usecase)
    output = tmp_path / "nested" / "report.md"

    written = write_report(assessment, output, style="executive")

    assert written == output
    assert output.exists()
    assert "Executive AI Readiness Brief" in output.read_text()
