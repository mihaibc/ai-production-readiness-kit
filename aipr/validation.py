from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError
from yaml import YAMLError

from aipr.models import UseCase


class UseCaseValidationError(ValueError):
    def __init__(self, message: str, hints: list[str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.hints = hints or []


@dataclass
class ValidationReport:
    usecase: UseCase
    warnings: list[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return not self.warnings


def load_usecase(path: Path) -> UseCase:
    return validate_usecase_file(path).usecase


def validate_usecase_file(path: Path) -> ValidationReport:
    data = load_yaml_mapping(path)
    try:
        usecase = UseCase.model_validate(data)
    except ValidationError as exc:
        raise UseCaseValidationError(
            f"{path}: use case YAML does not match the expected schema.",
            format_validation_errors(exc),
        ) from exc
    return ValidationReport(usecase=usecase, warnings=completeness_warnings(usecase))


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        raw_text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise UseCaseValidationError(f"{path}: file does not exist.") from exc
    try:
        data = yaml.safe_load(raw_text)
    except YAMLError as exc:
        raise UseCaseValidationError(
            f"{path}: YAML could not be parsed.",
            ["Check indentation, colons, list markers, and unclosed quotes."],
        ) from exc
    if not isinstance(data, dict):
        raise UseCaseValidationError(
            f"{path}: use case YAML must contain a mapping at the top level.",
            ["Start the file with fields such as `name:`, `owner:`, `stage:`, and `description:`."],
        )
    return data


def format_validation_errors(exc: ValidationError) -> list[str]:
    hints: list[str] = []
    for error in exc.errors():
        path = ".".join(str(part) for part in error["loc"]) or "root"
        message = str(error["msg"])
        hints.append(f"{path}: {message}")
    return hints


def completeness_warnings(usecase: UseCase) -> list[str]:
    checks = [
        ("owner", usecase.owner, "Add the team or role accountable for the workflow."),
        ("description", usecase.description, "Describe what the AI workflow does and where it is used."),
        ("business.problem", usecase.business.problem, "State the workflow problem this use case solves."),
        ("business.expected_impact", usecase.business.expected_impact, "Describe the measurable impact expected."),
        ("business.users", usecase.business.users, "List the primary users or reviewer groups."),
        ("data.sources", usecase.data.sources, "List the data or document sources the workflow depends on."),
    ]
    warnings: list[str] = []
    for field_name, value, guidance in checks:
        missing = not value if isinstance(value, (list, str)) else value is None
        if missing:
            warnings.append(f"{field_name} is not specified. {guidance}")
    return warnings
