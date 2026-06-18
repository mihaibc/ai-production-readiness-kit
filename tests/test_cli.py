import json
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
    assert "Document Ingestion Quality Monitor" in result.output
    assert "Score Breakdown" in result.output


def test_init_copies_template(tmp_path: Path) -> None:
    output = tmp_path / "usecase.yaml"

    result = runner.invoke(
        app,
        ["init", "--template", "document-ingestion-quality-monitor", "--output", str(output)],
    )

    assert result.exit_code == 0
    assert output.exists()
    assert "Document Ingestion Quality Monitor" in output.read_text()


def test_init_blank_creates_blank_template(tmp_path: Path) -> None:
    output = tmp_path / "blank-usecase.yaml"

    result = runner.invoke(app, ["init", "--blank", "--output", str(output)])

    assert result.exit_code == 0
    assert output.exists()
    assert "New AI Workflow" in output.read_text()


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


def test_assess_command_outputs_json() -> None:
    result = runner.invoke(
        app,
        ["assess", "examples/document-ingestion-quality-monitor/usecase.yaml", "--format", "json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["usecase"]["name"] == "Document Ingestion Quality Monitor"
    assert payload["total_score"] == 73
    assert payload["gate"]["passed"] is True


def test_assess_command_fails_threshold_gate() -> None:
    result = runner.invoke(
        app,
        ["assess", "examples/document-ingestion-quality-monitor/usecase.yaml", "--min-score", "95"],
    )

    assert result.exit_code == 1
    assert "Gate failed" in result.output


def test_assess_command_fails_critical_gate() -> None:
    result = runner.invoke(
        app,
        ["assess", "examples/supplier-risk-intake-screener/usecase.yaml", "--fail-on-critical"],
    )

    assert result.exit_code == 1
    assert "critical finding" in result.output


def test_remediation_command_outputs_json() -> None:
    result = runner.invoke(
        app,
        ["remediation", "examples/supplier-risk-intake-screener/usecase.yaml", "--format", "json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["usecase"] == "Supplier Risk Intake Screener"
    assert payload["items"][0]["severity"] == "critical"
    assert payload["items"][0]["priority"] == 1
    assert payload["items"][0]["why_it_matters"]


def test_remediation_command_outputs_text_table() -> None:
    result = runner.invoke(
        app,
        ["remediation", "examples/document-ingestion-quality-monitor/usecase.yaml"],
    )

    assert result.exit_code == 0
    assert "Remediation Plan" in result.output
    assert "Recommended action" in result.output


def test_schema_command_writes_schema(tmp_path: Path) -> None:
    output = tmp_path / "schema.json"

    result = runner.invoke(app, ["schema", "--output", str(output)])

    assert result.exit_code == 0
    schema = json.loads(output.read_text())
    assert schema["title"] == "UseCase"
    assert "name" in schema["properties"]


def test_compare_command_outputs_json() -> None:
    result = runner.invoke(
        app,
        [
            "compare",
            "examples/supplier-risk-intake-screener/usecase.yaml",
            "examples/research-knowledge-base-curator/usecase.yaml",
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["score_delta"] > 0
    assert payload["before"]["name"] == "Supplier Risk Intake Screener"
    assert payload["after"]["name"] == "Research Knowledge Base Curator"


def test_compare_command_outputs_text_table() -> None:
    result = runner.invoke(
        app,
        [
            "compare",
            "examples/supplier-risk-intake-screener/usecase.yaml",
            "examples/research-knowledge-base-curator/usecase.yaml",
        ],
    )

    assert result.exit_code == 0
    assert "Assessment Comparison" in result.output
    assert "Category Delta" in result.output
