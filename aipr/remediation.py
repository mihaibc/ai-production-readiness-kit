from __future__ import annotations

from aipr.models import Assessment, Finding

CATEGORY_EFFORT = {
    "Business value and workflow fit": "medium",
    "Data readiness": "medium",
    "RAG / retrieval quality": "high",
    "Model architecture": "medium",
    "Governance and security": "high",
    "Human-in-the-loop": "high",
    "Human-in-the-loop design": "high",
    "Evals and quality assurance": "medium",
    "Observability and cost control": "medium",
    "Operations": "medium",
    "Operations and ownership": "medium",
    "Adoption and enablement": "low",
    "General": "medium",
}

CATEGORY_RATIONALE = {
    "Business value and workflow fit": "Keeps the workflow tied to a clear user, decision, and measurable outcome.",
    "Data readiness": "Reduces failures caused by unclear sources, weak classification, or missing access boundaries.",
    "RAG / retrieval quality": "Keeps answers grounded, permission-aware, and testable before users rely on them.",
    "Model architecture": "Reduces provider, prompt, and model-change dependency before launch.",
    "Governance and security": "Reduces privacy, access, audit, and compliance risk.",
    "Human-in-the-loop": "Prevents high-risk outputs from reaching users without accountable review.",
    "Human-in-the-loop design": "Prevents high-risk outputs from reaching users without accountable review.",
    "Evals and quality assurance": "Lets the team detect regressions and unsafe behavior before release.",
    "Observability and cost control": "Makes cost, latency, errors, and traceability visible before scale.",
    "Operations": "Ensures the workflow can be supported, rolled back, and owned after launch.",
    "Operations and ownership": "Ensures the workflow can be supported, rolled back, and owned after launch.",
    "Adoption and enablement": "Helps users understand the workflow, give feedback, and adopt it responsibly.",
    "General": "Improves readiness before expanding production use.",
}

SEVERITY_RANK = {"critical": 0, "warning": 1, "info": 2}


def remediation_items(assessment: Assessment, limit: int = 8) -> list[dict[str, object]]:
    items = [_item_from_finding(index + 1, finding) for index, finding in enumerate(assessment.findings)]
    existing_actions = {str(item["action"]) for item in items}

    for step in assessment.recommended_next_steps:
        if step not in existing_actions:
            items.append(_item_from_step(len(items) + 1, step))
        if len(items) >= limit:
            break

    items.sort(key=lambda item: (SEVERITY_RANK[str(item["severity"])], int(item["priority"])))
    for priority, item in enumerate(items[:limit], start=1):
        item["priority"] = priority
    return items[:limit]


def _item_from_finding(priority: int, finding: Finding) -> dict[str, object]:
    return {
        "priority": priority,
        "severity": finding.severity,
        "category": finding.category,
        "effort": effort_for(finding.category, finding.severity),
        "action": finding.recommendation,
        "why_it_matters": why_it_matters(finding.category),
    }


def _item_from_step(priority: int, step: str) -> dict[str, object]:
    return {
        "priority": priority,
        "severity": "info",
        "category": "General",
        "effort": effort_for("General", "info"),
        "action": step,
        "why_it_matters": why_it_matters("General"),
    }


def effort_for(category: str, severity: str) -> str:
    effort = CATEGORY_EFFORT.get(category, "medium")
    if severity == "critical" and category in {
        "Governance and security",
        "Human-in-the-loop",
        "Human-in-the-loop design",
        "RAG / retrieval quality",
    }:
        return "high"
    return effort


def why_it_matters(category: str) -> str:
    return CATEGORY_RATIONALE.get(category, CATEGORY_RATIONALE["General"])
