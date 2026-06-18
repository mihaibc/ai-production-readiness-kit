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


def test_validate_command_accepts_complete_example() -> None:
    result = runner.invoke(app, ["validate", "examples/document-ingestion-quality-monitor/usecase.yaml"])

    assert result.exit_code == 0
    assert "Valid use case YAML" in result.output


def test_validate_command_reports_schema_errors(tmp_path: Path) -> None:
    usecase = tmp_path / "bad-usecase.yaml"
    usecase.write_text("owner: Example Team\n", encoding="utf-8")

    result = runner.invoke(app, ["validate", str(usecase)])

    assert result.exit_code == 1
    assert "Invalid use case YAML" in result.output
    assert "name" in result.output


def test_validate_strict_fails_on_completeness_warnings(tmp_path: Path) -> None:
    usecase = tmp_path / "minimal-usecase.yaml"
    usecase.write_text("name: Minimal Example\n", encoding="utf-8")

    result = runner.invoke(app, ["validate", str(usecase), "--strict"])

    assert result.exit_code == 1
    assert "Completeness warnings" in result.output


def test_explain_command_accepts_category_filter() -> None:
    result = runner.invoke(
        app,
        ["explain", "examples/document-ingestion-quality-monitor/usecase.yaml", "--category", "evals"],
    )

    assert result.exit_code == 0
    assert "Evals and quality assurance" in result.output
    assert "evals.golden_dataset_exists" in result.output
    assert "Business value and workflow fit" not in result.output
    assert "Retrieval evaluation is incomplete" not in result.output
