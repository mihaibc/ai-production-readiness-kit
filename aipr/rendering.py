from __future__ import annotations

import json

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aipr.models import Assessment, CategoryScore, Finding
from aipr.validation import UseCaseValidationError

console = Console()


def print_validation_error(exc: UseCaseValidationError) -> None:
    console.print(f"[bold red]Invalid use case YAML:[/bold red] {exc.message}")
    for hint in exc.hints:
        console.print(f"- {hint}")


def risk_style(risk_level: str) -> str:
    if risk_level in {"Not ready", "High risk"}:
        return "bold red"
    if risk_level == "Medium risk":
        return "bold yellow"
    return "bold green"


def assessment_payload(assessment: Assessment, gate: dict[str, object] | None = None) -> dict[str, object]:
    payload: dict[str, object] = assessment.model_dump(mode="json")
    if gate is not None:
        payload["gate"] = gate
    return payload


def print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2))


def print_assessment_summary(assessment: Assessment) -> None:
    summary = (
        f"[bold]Score:[/bold] {assessment.total_score} / 100\n"
        f"[bold]Risk:[/bold] [{risk_style(assessment.risk_level)}]{assessment.risk_level}[/] "
        f"- {assessment.risk_summary}\n"
        f"[bold]Production gate:[/bold] {assessment.production_gate}"
    )
    console.print(Panel(summary, title=assessment.usecase.name, border_style="blue", box=box.ROUNDED))

    table = Table(title="Score Breakdown", box=box.SIMPLE_HEAVY)
    table.add_column("Category")
    table.add_column("Score", justify="right")
    table.add_column("Readiness", justify="right")
    for category in assessment.categories:
        ratio = category.score / category.max_score
        readiness = "strong" if ratio >= 0.8 else "partial" if ratio >= 0.5 else "weak"
        table.add_row(category.name, f"{category.score:g} / {category.max_score}", readiness)
    console.print(table)

    if assessment.findings:
        findings = Table(title="Top Risks", box=box.SIMPLE)
        findings.add_column("#", justify="right")
        findings.add_column("Severity")
        findings.add_column("Category")
        findings.add_column("Finding")
        for index, finding in enumerate(assessment.findings[:5], start=1):
            severity_style = "red" if finding.severity == "critical" else "yellow"
            findings.add_row(
                str(index),
                f"[{severity_style}]{finding.severity.upper()}[/]",
                finding.category,
                finding.message,
            )
        console.print(findings)


def print_category_explanation(
    categories: list[CategoryScore],
    findings: list[Finding],
) -> None:
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

    matched_findings = [finding for finding in findings if finding.category in category_names]
    if matched_findings:
        console.print("\n[bold]Findings[/bold]")
        for finding in matched_findings:
            console.print(f"- {finding.severity.upper()}: {finding.message}")
            console.print(f"  Recommendation: {finding.recommendation}")


def print_remediation_plan(assessment: Assessment, items: list[dict[str, object]]) -> None:
    console.print(Panel.fit(
        f"[bold]{assessment.usecase.name}[/bold]\n"
        f"Score: {assessment.total_score} / 100\n"
        f"Risk: [{risk_style(assessment.risk_level)}]{assessment.risk_level}[/] - {assessment.risk_summary}",
        title="Remediation Plan",
        border_style="blue",
    ))
    table = Table(box=box.SIMPLE_HEAVY)
    table.add_column("#", justify="right")
    table.add_column("Severity")
    table.add_column("Category")
    table.add_column("Effort")
    table.add_column("Recommended action")
    for item in items:
        severity = str(item["severity"]).upper()
        style = "red" if severity == "CRITICAL" else "yellow" if severity == "WARNING" else "cyan"
        table.add_row(
            str(item["priority"]),
            f"[{style}]{severity}[/]",
            str(item["category"]),
            str(item["effort"]),
            str(item["action"]),
        )
    console.print(table)


def print_comparison(
    before_assessment: Assessment,
    after_assessment: Assessment,
    payload: dict[str, object],
) -> None:
    delta = payload["score_delta"]
    console.print(Panel.fit(
        f"[bold]{before_assessment.usecase.name}[/bold] -> [bold]{after_assessment.usecase.name}[/bold]\n"
        f"Score: {before_assessment.total_score} -> {after_assessment.total_score} ({delta:+})\n"
        f"Risk: {before_assessment.risk_level} -> {after_assessment.risk_level}",
        title="Assessment Comparison",
        border_style="blue",
    ))
    table = Table(title="Category Delta", box=box.SIMPLE_HEAVY)
    table.add_column("Category")
    table.add_column("Before", justify="right")
    table.add_column("After", justify="right")
    table.add_column("Delta", justify="right")
    for row in payload["categories"]:
        table.add_row(row["category"], f"{row['before']:g}", f"{row['after']:g}", f"{row['delta']:+g}")
    console.print(table)

    if payload["resolved_findings"] or payload["new_findings"]:
        changes = Table(title="Finding Changes", box=box.SIMPLE)
        changes.add_column("Type")
        changes.add_column("Finding")
        for finding in payload["resolved_findings"]:
            changes.add_row("[green]Resolved[/]", finding)
        for finding in payload["new_findings"]:
            changes.add_row("[red]New[/]", finding)
        console.print(changes)
