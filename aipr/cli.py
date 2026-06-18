from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from typing import Annotated

import typer
import yaml
from rich.console import Console
from rich.table import Table

from aipr.models import ReportStyle, UseCase
from aipr.report import render_report, write_report
from aipr.scoring import assess

app = typer.Typer(help="Assess whether an AI workflow is ready for production.")
console = Console()
STARTER_TEMPLATE_ROOT = "starter_templates"


def load_usecase(path: Path) -> UseCase:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise typer.BadParameter("Use case YAML must contain a mapping at the top level.")
    return UseCase.model_validate(data)


@app.command()
def init(
    template: Annotated[str, typer.Option(help="Example template to copy.")] = "rfq-assistant",
    output: Annotated[Path, typer.Option(help="Destination YAML path.")] = Path("usecase.yaml"),
    overwrite: Annotated[bool, typer.Option(help="Overwrite an existing output file.")] = False,
) -> None:
    """Create a starter usecase.yaml file."""
    source = files("aipr").joinpath(STARTER_TEMPLATE_ROOT, template, "usecase.yaml")
    if not source.is_file():
        available = ", ".join(list_templates())
        raise typer.BadParameter(f"Unknown template '{template}'. Available templates: {available}")
    if output.exists() and not overwrite:
        raise typer.BadParameter(f"{output} already exists. Use --overwrite to replace it.")
    output.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    console.print(f"Created [bold]{output}[/bold] from template [bold]{template}[/bold].")


@app.command("assess")
def assess_command(path: Annotated[Path, typer.Argument(help="Path to usecase.yaml.")]) -> None:
    """Score an AI use case and print the readiness summary."""
    assessment = assess(load_usecase(path))
    console.print(f"[bold]AI Production Readiness Score:[/bold] {assessment.total_score} / 100")
    console.print(f"[bold]Risk level:[/bold] {assessment.risk_level} / {assessment.risk_summary}")

    table = Table(title="Score Breakdown")
    table.add_column("Category")
    table.add_column("Score", justify="right")
    for category in assessment.categories:
        table.add_row(category.name, f"{category.score:g} / {category.max_score}")
    console.print(table)

    if assessment.findings:
        console.print("[bold]Top risks[/bold]")
        for index, finding in enumerate(assessment.findings[:5], start=1):
            console.print(f"{index}. {finding.severity.upper()}: {finding.message}")


@app.command()
def report(
    path: Annotated[Path, typer.Argument(help="Path to usecase.yaml.")],
    output: Annotated[Path | None, typer.Option(help="Report output path.")] = None,
    style: Annotated[
        ReportStyle,
        typer.Option(help="Report style: balanced, executive, or engineering."),
    ] = "balanced",
) -> None:
    """Generate a Markdown readiness report."""
    assessment = assess(load_usecase(path))
    if output is None:
        console.print(render_report(assessment, style=style))
        return
    written = write_report(assessment, output, style=style)
    console.print(f"Wrote report to [bold]{written}[/bold].")


@app.command()
def explain(path: Annotated[Path, typer.Argument(help="Path to usecase.yaml.")]) -> None:
    """Explain the scoring rationale and generated findings."""
    assessment = assess(load_usecase(path))
    for category in assessment.categories:
        console.print(f"[bold]{category.name}:[/bold] {category.score:g} / {category.max_score}")
        console.print(f"  {category.rationale}")
    if assessment.findings:
        console.print("\n[bold]Findings[/bold]")
        for finding in assessment.findings:
            console.print(f"- {finding.severity.upper()}: {finding.message}")
            console.print(f"  Recommendation: {finding.recommendation}")


@app.command()
def templates() -> None:
    """List available starter templates."""
    for name in list_templates():
        console.print(name)


def list_templates() -> list[str]:
    root = files("aipr").joinpath(STARTER_TEMPLATE_ROOT)
    if not root.is_dir():
        return []
    return sorted(path.name for path in root.iterdir() if path.joinpath("usecase.yaml").is_file())


if __name__ == "__main__":
    app()
