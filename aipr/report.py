from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from aipr.models import Assessment, ReportStyle

REPORT_TEMPLATES: dict[ReportStyle, str] = {
    "balanced": "report.md.j2",
    "executive": "report_executive.md.j2",
    "engineering": "report_engineering.md.j2",
}


def template_environment() -> Environment:
    template_path = files("aipr").joinpath("templates")
    return Environment(
        loader=FileSystemLoader(str(template_path)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_report(assessment: Assessment, style: ReportStyle = "balanced") -> str:
    template = template_environment().get_template(REPORT_TEMPLATES[style])
    return template.render(assessment=assessment, usecase=assessment.usecase).rstrip() + "\n"


def write_report(assessment: Assessment, output: Path, style: ReportStyle = "balanced") -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(assessment, style=style), encoding="utf-8")
    return output
