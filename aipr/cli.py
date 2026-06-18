from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import Annotated

import typer

from aipr.comparison import compare_payload
from aipr.gates import evaluate_gate
from aipr.models import OutputFormat, ReportStyle, UseCase
from aipr.remediation import remediation_items
from aipr.rendering import (
    assessment_payload,
    console,
    print_assessment_summary,
    print_category_explanation,
    print_comparison,
    print_json,
    print_remediation_plan,
    print_validation_error,
)
from aipr.report import render_report, write_report
from aipr.scoring import assess
from aipr.validation import UseCaseValidationError, load_usecase, validate_usecase_file

app = typer.Typer(help="Assess whether an AI workflow is ready for production.")
STARTER_TEMPLATE_ROOT = "starter_templates"
BLANK_TEMPLATE_PATH = ("templates", "usecase_blank.yaml")


def load_usecase_or_exit(path: Path) -> UseCase:
    try:
        return load_usecase(path)
    except UseCaseValidationError as exc:
        print_validation_error(exc)
        raise typer.Exit(1) from exc


@app.command()
def init(
    template: Annotated[str, typer.Option(help="Example template to copy.")] = "document-ingestion-quality-monitor",
    output: Annotated[Path, typer.Option(help="Destination YAML path.")] = Path("usecase.yaml"),
    overwrite: Annotated[bool, typer.Option(help="Overwrite an existing output file.")] = False,
    blank: Annotated[bool, typer.Option(help="Create a blank starter instead of copying an example.")] = False,
) -> None:
    """Create a starter usecase.yaml file."""
    source = (
        files("aipr").joinpath(*BLANK_TEMPLATE_PATH)
        if blank
        else files("aipr").joinpath(STARTER_TEMPLATE_ROOT, template, "usecase.yaml")
    )
    if not source.is_file():
        available = ", ".join(list_templates())
        raise typer.BadParameter(f"Unknown template '{template}'. Available templates: {available}")
    if output.exists() and not overwrite:
        raise typer.BadParameter(f"{output} already exists. Use --overwrite to replace it.")
    output.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    source_name = "blank starter" if blank else f"template [bold]{template}[/bold]"
    console.print(f"Created [bold]{output}[/bold] from {source_name}.")


@app.command("assess")
def assess_command(
    path: Annotated[Path, typer.Argument(help="Path to usecase.yaml.")],
    format: Annotated[OutputFormat, typer.Option(help="Output format: text or json.")] = "text",
    min_score: Annotated[int | None, typer.Option(help="Fail if the score is below this value.")] = None,
    fail_on_critical: Annotated[bool, typer.Option(help="Fail if any critical finding exists.")] = False,
) -> None:
    """Score an AI use case and print the readiness summary."""
    assessment = assess(load_usecase_or_exit(path))
    gate = evaluate_gate(assessment, min_score=min_score, fail_on_critical=fail_on_critical)
    if format == "json":
        print_json(assessment_payload(assessment, gate=gate))
    else:
        print_assessment_summary(assessment)
        if gate["failures"]:
            console.print("[bold red]Gate failed[/bold red]")
            for failure in gate["failures"]:
                console.print(f"- {failure}")
    if not gate["passed"]:
        raise typer.Exit(1)


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

    print_category_explanation(categories, assessment.findings)


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
def remediation(
    path: Annotated[Path, typer.Argument(help="Path to usecase.yaml.")],
    format: Annotated[OutputFormat, typer.Option(help="Output format: text or json.")] = "text",
) -> None:
    """Generate a prioritized remediation plan."""
    assessment = assess(load_usecase_or_exit(path))
    items = remediation_items(assessment)
    if format == "json":
        print_json({"usecase": assessment.usecase.name, "score": assessment.total_score, "items": items})
        return

    print_remediation_plan(assessment, items)


@app.command()
def schema(
    output: Annotated[Path | None, typer.Option(help="Write JSON Schema to this path.")] = None,
) -> None:
    """Export the usecase.yaml JSON Schema."""
    schema_text = json.dumps(UseCase.model_json_schema(), indent=2)
    if output is None:
        console.print(schema_text)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(schema_text + "\n", encoding="utf-8")
    console.print(f"Wrote schema to [bold]{output}[/bold].")


@app.command()
def compare(
    before: Annotated[Path, typer.Argument(help="Earlier usecase.yaml.")],
    after: Annotated[Path, typer.Argument(help="Later usecase.yaml.")],
    format: Annotated[OutputFormat, typer.Option(help="Output format: text or json.")] = "text",
) -> None:
    """Compare two readiness assessments."""
    before_assessment = assess(load_usecase_or_exit(before))
    after_assessment = assess(load_usecase_or_exit(after))
    payload = compare_payload(before_assessment, after_assessment)
    if format == "json":
        print_json(payload)
        return

    print_comparison(before_assessment, after_assessment, payload)


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
