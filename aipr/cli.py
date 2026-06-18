from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from aipr.models import ReportStyle, UseCase
from aipr.report import render_report, write_report
from aipr.scoring import assess
from aipr.validation import UseCaseValidationError, load_usecase, validate_usecase_file

app = typer.Typer(help="Assess whether an AI workflow is ready for production.")
console = Console()
STARTER_TEMPLATE_ROOT = "starter_templates"


def load_usecase_or_exit(path: Path) -> UseCase:
    try:
        return load_usecase(path)
    except UseCaseValidationError as exc:
        print_validation_error(exc)
        raise typer.Exit(1) from exc


def print_validation_error(exc: UseCaseValidationError) -> None:
    console.print(f"[bold red]Invalid use case YAML:[/bold red] {exc.message}")
    for hint in exc.hints:
        console.print(f"- {hint}")


@app.command()
def init(
    template: Annotated[str, typer.Option(help="Example template to copy.")] = "document-ingestion-quality-monitor",
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
    assessment = assess(load_usecase_or_exit(path))
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
    assessment = assess(load_usecase_or_exit(path))
    if output is None:
        console.print(render_report(assessment, style=style))
        return
    written = write_report(assessment, output, style=style)
    console.print(f"Wrote report to [bold]{written}[/bold].")


@app.command()
def explain(
    path: Annotated[Path, typer.Argument(help="Path to usecase.yaml.")],
    category: Annotated[
        str | None,
        typer.Option(help="Show only one category by key, for example: evals, rag, observability."),
    ] = None,
) -> None:
    """Explain the scoring rationale and generated findings."""
    assessment = assess(load_usecase_or_exit(path))
    categories = assessment.categories
    if category:
        categories = [
            item
            for item in assessment.categories
            if item.key == category or item.name.lower() == category.lower()
        ]
        if not categories:
            available = ", ".join(item.key for item in assessment.categories)
            console.print(f"[bold red]Unknown category:[/bold red] {category}")
            console.print(f"Available categories: {available}")
            raise typer.Exit(1)

    category_names = {item.name for item in categories}
    for item in categories:
        console.print(f"[bold]{item.name}:[/bold] {item.score:g} / {item.max_score}")
        console.print(f"  {item.rationale}")
        table = Table(show_header=True)
        table.add_column("Field")
        table.add_column("Value")
        table.add_column("Score", justify="right")
        for detail in item.details:
            table.add_row(detail.field, detail.value, f"{detail.score:g} / {detail.max_score:g}")
        console.print(table)
    findings = [
        finding for finding in assessment.findings if not category or finding.category in category_names
    ]
    if findings:
        console.print("\n[bold]Findings[/bold]")
        for finding in findings:
            console.print(f"- {finding.severity.upper()}: {finding.message}")
            console.print(f"  Recommendation: {finding.recommendation}")


@app.command()
def validate(
    path: Annotated[Path, typer.Argument(help="Path to usecase.yaml.")],
    strict: Annotated[bool, typer.Option(help="Exit with an error when completeness warnings exist.")] = False,
) -> None:
    """Validate a usecase.yaml file without scoring it."""
    try:
        report = validate_usecase_file(path)
    except UseCaseValidationError as exc:
        print_validation_error(exc)
        raise typer.Exit(1) from exc

    console.print(f"[bold green]Valid use case YAML:[/bold green] {report.usecase.name}")
    if report.warnings:
        console.print("[bold yellow]Completeness warnings[/bold yellow]")
        for warning in report.warnings:
            console.print(f"- {warning}")
        if strict:
            raise typer.Exit(1)
    else:
        console.print("No completeness warnings found.")


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
