from pathlib import Path

from typer.testing import CliRunner

from aipr.cli import app

runner = CliRunner()
EXPECTED_TEMPLATES = {
    "document-ingestion-quality-monitor",
    "maintenance-log-summarizer",
    "policy-compliance-faq-assistant",
    "research-knowledge-base-curator",
    "supplier-risk-intake-screener",
}


def test_templates_lists_examples() -> None:
    result = runner.invoke(app, ["templates"])

    assert result.exit_code == 0
    assert set(result.output.strip().splitlines()) == EXPECTED_TEMPLATES


def test_assess_command_scores_example() -> None:
    result = runner.invoke(app, ["assess", "examples/document-ingestion-quality-monitor/usecase.yaml"])

    assert result.exit_code == 0
    assert "AI Production Readiness Score" in result.output


def test_init_copies_template(tmp_path: Path) -> None:
    output = tmp_path / "usecase.yaml"

    result = runner.invoke(
        app,
        ["init", "--template", "document-ingestion-quality-monitor", "--output", str(output)],
    )

    assert result.exit_code == 0
    assert output.exists()
    assert "Document Ingestion Quality Monitor" in output.read_text()


def test_report_command_accepts_style(tmp_path: Path) -> None:
    output = tmp_path / "executive-report.md"

    result = runner.invoke(
        app,
        [
            "report",
            "examples/document-ingestion-quality-monitor/usecase.yaml",
            "--style",
            "executive",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert output.exists()
    assert "Executive AI Readiness Brief" in output.read_text()
