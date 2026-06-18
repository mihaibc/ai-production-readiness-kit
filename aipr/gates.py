from __future__ import annotations

from aipr.models import Assessment


def evaluate_gate(
    assessment: Assessment,
    min_score: int | None = None,
    fail_on_critical: bool = False,
) -> dict[str, object]:
    failures: list[str] = []
    if min_score is not None and assessment.total_score < min_score:
        failures.append(f"Score {assessment.total_score} is below required minimum {min_score}.")
    if fail_on_critical and assessment.critical_findings:
        failures.append(f"{len(assessment.critical_findings)} critical finding(s) are unresolved.")
    return {
        "passed": not failures,
        "failures": failures,
        "min_score": min_score,
        "fail_on_critical": fail_on_critical,
    }
