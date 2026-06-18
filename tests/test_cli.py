from pathlib import Path

from typer.testing import CliRunner

from aipr.cli import app

runner = CliRunner()


def test_templates_lists_examples() -> None:
    result = runner.invoke(app, ["templates"])

    assert result.exit_code == 0
    assert "rfq-assistant" in result.output


def test_assess_command_scores_example() -> None:
    result = runner.invoke(app, ["assess", "examples/rfq-assistant/usecase.yaml"])

    assert result.exit_code == 0
    assert "AI Production Readiness Score" in result.output


def test_init_copies_template(tmp_path: Path) -> None:
    output = tmp_path / "usecase.yaml"

    result = runner.invoke(app, ["init", "--template", "rfq-assistant", "--output", str(output)])

    assert result.exit_code == 0
    assert output.exists()
    assert "RFQ Sales Assistant" in output.read_text()


def test_report_command_accepts_style(tmp_path: Path) -> None:
    output = tmp_path / "executive-report.md"

    result = runner.invoke(
        app,
        [
            "report",
            "examples/rfq-assistant/usecase.yaml",
            "--style",
            "executive",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert output.exists()
    assert "Executive AI Readiness Brief" in output.read_text()
