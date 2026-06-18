from __future__ import annotations

from aipr.models import Assessment


def compare_payload(before: Assessment, after: Assessment) -> dict[str, object]:
    before_categories = {category.key: category for category in before.categories}
    rows: list[dict[str, object]] = []
    for category in after.categories:
        before_score = before_categories[category.key].score
        rows.append({
            "key": category.key,
            "category": category.name,
            "before": before_score,
            "after": category.score,
            "delta": category.score - before_score,
        })

    before_findings = {finding.message for finding in before.findings}
    after_findings = {finding.message for finding in after.findings}
    return {
        "before": {
            "name": before.usecase.name,
            "score": before.total_score,
            "risk_level": before.risk_level,
        },
        "after": {
            "name": after.usecase.name,
            "score": after.total_score,
            "risk_level": after.risk_level,
        },
        "score_delta": after.total_score - before.total_score,
        "categories": rows,
        "resolved_findings": sorted(before_findings - after_findings),
        "new_findings": sorted(after_findings - before_findings),
    }
