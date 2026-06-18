from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from aipr.models import Assessment, CategoryScore, Finding, ScoreContribution, UseCase


def status_score(value: object, max_points: float) -> float:
    if value is True:
        return max_points
    if isinstance(value, str) and value.lower() == "partial":
        return max_points / 2
    return 0.0


def display_value(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "not specified"
    if value == "":
        return "not specified"
    return str(value)


def contribution(field: str, label: str, value: Any, score: float, max_score: float) -> ScoreContribution:
    return ScoreContribution(
        field=field,
        label=label,
        value=display_value(value),
        score=score,
        max_score=max_score,
    )


def is_missing(value: object) -> bool:
    return value is False


def is_incomplete(value: object) -> bool:
    return value is not True


def is_partial(value: object) -> bool:
    return isinstance(value, str) and value.lower() == "partial"


def text_score(value: str, max_points: float) -> float:
    return max_points if value.strip() else 0.0


def list_score(value: Iterable[object], max_points: float) -> float:
    return max_points if list(value) else 0.0


def clamp(score: float, max_points: int) -> float:
    return max(0.0, min(float(max_points), score))


def risk_band(score: int) -> tuple[str, str]:
    if score <= 39:
        return "Not ready", "Prototype only"
    if score <= 59:
        return "High risk", "Pilot only"
    if score <= 74:
        return "Medium risk", "Production only with additional controls"
    if score <= 89:
        return "Production-ready", "Minor gaps remain"
    return "Strong production readiness", "Ready for scaled production governance"


def apply_production_gate(
    score: int,
    base_level: str,
    base_summary: str,
    findings: list[Finding],
) -> tuple[str, str, str]:
    has_critical = any(finding.severity == "critical" for finding in findings)
    if not has_critical:
        return base_level, base_summary, "No critical production blockers identified."
    if score <= 39:
        return base_level, base_summary, "Critical blockers identified."
    return (
        "High risk",
        "Pilot only until critical controls are resolved",
        "Critical findings block production readiness even when the numeric score is higher.",
    )


def assess(usecase: UseCase) -> Assessment:
    categories = [
        score_business(usecase),
        score_data(usecase),
        score_rag(usecase),
        score_model_architecture(usecase),
        score_governance(usecase),
        score_human_in_the_loop(usecase),
        score_evals(usecase),
        score_observability(usecase),
        score_operations(usecase),
        score_adoption(usecase),
    ]
    total = round(sum(category.score for category in categories))
    findings = build_findings(usecase)
    base_level, base_summary = risk_band(total)
    level, summary, production_gate = apply_production_gate(total, base_level, base_summary, findings)
    next_steps = recommended_next_steps(findings, categories)
    return Assessment(
        usecase=usecase,
        total_score=total,
        base_risk_level=base_level,
        base_risk_summary=base_summary,
        risk_level=level,
        risk_summary=summary,
        production_gate=production_gate,
        categories=categories,
        findings=findings,
        recommended_next_steps=next_steps,
    )


def score_business(usecase: UseCase) -> CategoryScore:
    business = usecase.business
    impact_points = {"high": 3.0, "medium": 2.0, "low": 1.0, "none": 0.0, "unknown": 0.0}
    details = [
        contribution("business.problem", "Problem defined", business.problem, text_score(business.problem, 2), 2),
        contribution(
            "business.expected_impact",
            "Expected impact defined",
            business.expected_impact,
            text_score(business.expected_impact, 2),
            2,
        ),
        contribution("business.users", "Primary users listed", business.users, list_score(business.users, 2), 2),
        contribution(
            "business.revenue_or_cost_impact",
            "Impact level",
            business.revenue_or_cost_impact,
            impact_points.get(business.revenue_or_cost_impact, 0.0),
            3,
        ),
        contribution("stage", "Delivery stage set", usecase.stage, 1.0 if usecase.stage else 0.0, 1),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Business value and workflow fit",
        key="business",
        score=clamp(score, 10),
        max_score=10,
        rationale="Checks whether the use case has a clear problem, users, impact, and delivery stage.",
        details=details,
    )


def score_data(usecase: UseCase) -> CategoryScore:
    data = usecase.data
    sensitive_controls = 2.0
    if data.pii_or_sensitive_data and data.access_control_required is not True:
        sensitive_controls = 0.0
    details = [
        contribution("data.sources", "Data sources listed", data.sources, list_score(data.sources, 2), 2),
        contribution(
            "data.data_classification",
            "Data classification set",
            data.data_classification,
            2.0 if data.data_classification != "unknown" else 0.0,
            2,
        ),
        contribution(
            "data.freshness_required",
            "Freshness requirement defined",
            data.freshness_required,
            status_score(data.freshness_required, 2),
            2,
        ),
        contribution(
            "data.access_control_required",
            "Access control requirement defined",
            data.access_control_required,
            status_score(data.access_control_required, 2),
            2,
        ),
        contribution(
            "data.pii_or_sensitive_data",
            "Sensitive data has matching controls",
            data.pii_or_sensitive_data,
            sensitive_controls,
            2,
        ),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Data readiness",
        key="data",
        score=clamp(score, 10),
        max_score=10,
        rationale="Checks whether data sources, classification, freshness, and access boundaries are understood.",
        details=details,
    )


def score_rag(usecase: UseCase) -> CategoryScore:
    rag = usecase.rag
    if not rag.uses_rag:
        details = [
            contribution("rag.uses_rag", "RAG not used", rag.uses_rag, 10, 10),
        ]
        return CategoryScore(
            name="RAG / retrieval quality",
            key="rag",
            score=10,
            max_score=10,
            rationale="No retrieval layer is declared, so RAG-specific controls are not required.",
            details=details,
        )
    details = [
        contribution(
            "rag.chunking_strategy_defined",
            "Chunking strategy defined",
            rag.chunking_strategy_defined,
            status_score(rag.chunking_strategy_defined, 2.5),
            2.5,
        ),
        contribution(
            "rag.source_citations_required",
            "Source citations required",
            rag.source_citations_required,
            status_score(rag.source_citations_required, 2.5),
            2.5,
        ),
        contribution(
            "rag.retrieval_evaluation_exists",
            "Retrieval evaluation exists",
            rag.retrieval_evaluation_exists,
            status_score(rag.retrieval_evaluation_exists, 2.5),
            2.5,
        ),
        contribution(
            "rag.rbac_filtered_retrieval",
            "RBAC-filtered retrieval defined",
            rag.rbac_filtered_retrieval,
            status_score(rag.rbac_filtered_retrieval, 2.5),
            2.5,
        ),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="RAG / retrieval quality",
        key="rag",
        score=clamp(score, 10),
        max_score=10,
        rationale="Checks chunking, citations, retrieval evaluation, and permission-aware retrieval.",
        details=details,
    )


def score_model_architecture(usecase: UseCase) -> CategoryScore:
    architecture = usecase.model_architecture
    details = [
        contribution(
            "model_architecture.providers",
            "Provider list defined",
            architecture.providers,
            list_score(architecture.providers, 2),
            2,
        ),
        contribution(
            "model_architecture.model_router",
            "Model router or abstraction",
            architecture.model_router,
            status_score(architecture.model_router, 2.5),
            2.5,
        ),
        contribution(
            "model_architecture.fallback_model",
            "Fallback model",
            architecture.fallback_model,
            status_score(architecture.fallback_model, 2),
            2,
        ),
        contribution(
            "model_architecture.prompt_versioning",
            "Prompt versioning",
            architecture.prompt_versioning,
            status_score(architecture.prompt_versioning, 2),
            2,
        ),
        contribution(
            "model_architecture.business_logic_in_prompts",
            "Business logic outside prompts",
            architecture.business_logic_in_prompts,
            0.0 if architecture.business_logic_in_prompts else 1.5,
            1.5,
        ),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Model architecture",
        key="model_architecture",
        score=clamp(score, 10),
        max_score=10,
        rationale="Checks provider dependency, routing, fallback, prompt versioning, and prompt coupling.",
        details=details,
    )


def score_governance(usecase: UseCase) -> CategoryScore:
    governance = usecase.governance
    details = [
        contribution(
            "governance.rbacs_defined",
            "RBAC defined",
            governance.rbacs_defined,
            status_score(governance.rbacs_defined, 4),
            4,
        ),
        contribution(
            "governance.audit_logs",
            "Audit logs",
            governance.audit_logs,
            status_score(governance.audit_logs, 3),
            3,
        ),
        contribution(
            "governance.privacy_review_done",
            "Privacy review",
            governance.privacy_review_done,
            status_score(governance.privacy_review_done, 3),
            3,
        ),
        contribution(
            "governance.legal_review_done",
            "Legal review",
            governance.legal_review_done,
            status_score(governance.legal_review_done, 2),
            2,
        ),
        contribution(
            "governance.compliance_gates",
            "Compliance gates",
            governance.compliance_gates,
            status_score(governance.compliance_gates, 3),
            3,
        ),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Governance and security",
        key="governance",
        score=clamp(score, 15),
        max_score=15,
        rationale="Checks RBAC, auditability, privacy, legal review, and compliance gates.",
        details=details,
    )


def score_human_in_the_loop(usecase: UseCase) -> CategoryScore:
    human = usecase.human_in_the_loop
    if not human.required and not usecase.business.external_output:
        details = [
            contribution(
                "human_in_the_loop.required",
                "Human review not required for this workflow",
                human.required,
                10,
                10,
            ),
        ]
        return CategoryScore(
            name="Human-in-the-loop design",
            key="human_in_the_loop",
            score=10,
            max_score=10,
            rationale="No external or high-risk human gate is declared for this workflow.",
            details=details,
        )
    details = [
        contribution(
            "human_in_the_loop.required",
            "Human review required",
            human.required,
            2.0 if human.required else 0.0,
            2,
        ),
        contribution(
            "human_in_the_loop.approval_before_external_use",
            "Approval before external use",
            human.approval_before_external_use,
            status_score(human.approval_before_external_use, 4),
            4,
        ),
        contribution(
            "human_in_the_loop.escalation_defined",
            "Escalation path defined",
            human.escalation_defined,
            status_score(human.escalation_defined, 2),
            2,
        ),
        contribution(
            "human_in_the_loop.reviewer_role",
            "Reviewer role named",
            human.reviewer_role,
            text_score(human.reviewer_role, 2),
            2,
        ),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Human-in-the-loop design",
        key="human_in_the_loop",
        score=clamp(score, 10),
        max_score=10,
        rationale="Checks whether review, approval, escalation, and reviewer ownership are explicit.",
        details=details,
    )


def score_evals(usecase: UseCase) -> CategoryScore:
    evals = usecase.evals
    details = [
        contribution(
            "evals.golden_dataset_exists",
            "Golden dataset",
            evals.golden_dataset_exists,
            status_score(evals.golden_dataset_exists, 5),
            5,
        ),
        contribution(
            "evals.regression_tests",
            "Regression tests",
            evals.regression_tests,
            status_score(evals.regression_tests, 4),
            4,
        ),
        contribution(
            "evals.hallucination_tests",
            "Hallucination tests",
            evals.hallucination_tests,
            status_score(evals.hallucination_tests, 3),
            3,
        ),
        contribution("evals.safety_tests", "Safety tests", evals.safety_tests, status_score(evals.safety_tests, 3), 3),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Evals and quality assurance",
        key="evals",
        score=clamp(score, 15),
        max_score=15,
        rationale="Checks golden datasets, regression tests, hallucination tests, and safety tests.",
        details=details,
    )


def score_observability(usecase: UseCase) -> CategoryScore:
    observability = usecase.observability
    details = [
        contribution(
            "observability.token_tracking",
            "Token tracking",
            observability.token_tracking,
            status_score(observability.token_tracking, 2),
            2,
        ),
        contribution(
            "observability.latency_tracking",
            "Latency tracking",
            observability.latency_tracking,
            status_score(observability.latency_tracking, 2),
            2,
        ),
        contribution(
            "observability.error_tracking",
            "Error tracking",
            observability.error_tracking,
            status_score(observability.error_tracking, 2),
            2,
        ),
        contribution(
            "observability.cost_dashboard",
            "Cost dashboard",
            observability.cost_dashboard,
            status_score(observability.cost_dashboard, 2),
            2,
        ),
        contribution(
            "observability.prompt_response_tracing",
            "Prompt/response tracing",
            observability.prompt_response_tracing,
            status_score(observability.prompt_response_tracing, 2),
            2,
        ),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Observability and cost control",
        key="observability",
        score=clamp(score, 10),
        max_score=10,
        rationale="Checks token, latency, error, cost, and trace visibility.",
        details=details,
    )


def score_operations(usecase: UseCase) -> CategoryScore:
    operations = usecase.operations
    details = [
        contribution(
            "operations.incident_owner_defined",
            "Incident owner defined",
            operations.incident_owner_defined,
            status_score(operations.incident_owner_defined, 1.5),
            1.5,
        ),
        contribution(
            "operations.rollback_plan",
            "Rollback plan",
            operations.rollback_plan,
            status_score(operations.rollback_plan, 1.5),
            1.5,
        ),
        contribution(
            "operations.support_process",
            "Support process",
            operations.support_process,
            status_score(operations.support_process, 1),
            1,
        ),
        contribution(
            "operations.change_management",
            "Change management",
            operations.change_management,
            status_score(operations.change_management, 1),
            1,
        ),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Operations and ownership",
        key="operations",
        score=clamp(score, 5),
        max_score=5,
        rationale="Checks launch ownership, rollback, support, and change management.",
        details=details,
    )


def score_adoption(usecase: UseCase) -> CategoryScore:
    adoption = usecase.adoption
    details = [
        contribution(
            "adoption.training_materials",
            "Training materials",
            adoption.training_materials,
            status_score(adoption.training_materials, 1.5),
            1.5,
        ),
        contribution(
            "adoption.user_guides",
            "User guides",
            adoption.user_guides,
            status_score(adoption.user_guides, 1.5),
            1.5,
        ),
        contribution(
            "adoption.feedback_loop",
            "Feedback loop",
            adoption.feedback_loop,
            status_score(adoption.feedback_loop, 1),
            1,
        ),
        contribution(
            "adoption.adoption_metrics",
            "Adoption metrics",
            adoption.adoption_metrics,
            status_score(adoption.adoption_metrics, 1),
            1,
        ),
    ]
    score = sum(detail.score for detail in details)
    return CategoryScore(
        name="Adoption and enablement",
        key="adoption",
        score=clamp(score, 5),
        max_score=5,
        rationale="Checks training, user guides, feedback loops, and adoption measurement.",
        details=details,
    )


def build_findings(usecase: UseCase) -> list[Finding]:
    findings: list[Finding] = []
    add = findings.append

    if usecase.business.external_output and is_missing(usecase.human_in_the_loop.approval_before_external_use):
        add(Finding(
            severity="critical",
            category="Human-in-the-loop",
            message="External outputs do not have a required human approval gate.",
            recommendation="Require approval by a named reviewer role before external use.",
        ))
    if usecase.data.pii_or_sensitive_data and is_missing(usecase.governance.rbacs_defined):
        add(Finding(
            severity="critical",
            category="Governance and security",
            message="Sensitive data is in scope but RBAC is not defined.",
            recommendation="Define RBAC roles, access boundaries, and audit expectations before production.",
        ))
    if usecase.rag.uses_rag and is_missing(usecase.rag.retrieval_evaluation_exists):
        add(Finding(
            severity="critical",
            category="RAG / retrieval quality",
            message="Retrieval quality is not validated against an evaluation set.",
            recommendation=(
                "Create a golden retrieval dataset and track source coverage, misses, and wrong-document retrieval."
            ),
        ))
    if usecase.rag.uses_rag and usecase.data.pii_or_sensitive_data and is_missing(usecase.rag.rbac_filtered_retrieval):
        add(Finding(
            severity="critical",
            category="RAG / retrieval quality",
            message="RAG uses sensitive data without fully defined RBAC-aware retrieval.",
            recommendation="Enforce permissions before retrieval and verify filtered retrieval in tests.",
        ))
    if usecase.data.pii_or_sensitive_data and is_partial(usecase.governance.rbacs_defined):
        add(Finding(
            severity="warning",
            category="Governance and security",
            message="Sensitive data is in scope but RBAC is not fully defined.",
            recommendation="Complete RBAC roles, access boundaries, and audit expectations before production.",
        ))
    if usecase.rag.uses_rag and is_partial(usecase.rag.retrieval_evaluation_exists):
        add(Finding(
            severity="warning",
            category="RAG / retrieval quality",
            message="Retrieval evaluation is incomplete.",
            recommendation="Expand retrieval evals to cover source coverage, misses, and wrong-document retrieval.",
        ))
    if usecase.rag.uses_rag and usecase.data.pii_or_sensitive_data and is_partial(usecase.rag.rbac_filtered_retrieval):
        add(Finding(
            severity="warning",
            category="RAG / retrieval quality",
            message="RBAC-aware retrieval is incomplete for sensitive data.",
            recommendation="Verify permission-filtered retrieval with representative user roles.",
        ))
    if is_incomplete(usecase.operations.rollback_plan):
        add(Finding(
            severity="warning",
            category="Operations",
            message="Rollback plan is not fully defined.",
            recommendation="Document how to disable the workflow, revert prompts/models, and notify affected users.",
        ))
    if is_incomplete(usecase.operations.incident_owner_defined):
        add(Finding(
            severity="warning",
            category="Operations",
            message="Incident ownership is not fully defined.",
            recommendation="Assign an operational owner for failures, escalations, and production changes.",
        ))
    if usecase.model_architecture.business_logic_in_prompts and is_incomplete(usecase.model_architecture.model_router):
        add(Finding(
            severity="warning",
            category="Model architecture",
            message="Business logic is embedded in prompts without a model routing or abstraction layer.",
            recommendation="Version prompts and separate workflow rules from model-specific instructions.",
        ))
    if not all([
        usecase.observability.token_tracking is True,
        usecase.observability.latency_tracking is True,
        usecase.observability.error_tracking is True,
    ]):
        add(Finding(
            severity="warning",
            category="Observability and cost control",
            message="Token, latency, or error tracking is incomplete.",
            recommendation="Track token use, latency, errors, and cost per workflow before broader rollout.",
        ))
    if is_incomplete(usecase.evals.golden_dataset_exists):
        add(Finding(
            severity="warning",
            category="Evals and quality assurance",
            message="No formal golden evaluation dataset is defined.",
            recommendation="Build representative examples with expected outputs and known failure modes.",
        ))
    return findings


def recommended_next_steps(findings: list[Finding], categories: list[CategoryScore]) -> list[str]:
    steps: list[str] = []
    for finding in findings:
        if finding.recommendation not in steps:
            steps.append(finding.recommendation)
        if len(steps) == 5:
            return steps

    weakest = sorted(categories, key=lambda category: category.score / category.max_score)
    for category in weakest:
        step = f"Improve {category.name.lower()} before expanding production use."
        if step not in steps:
            steps.append(step)
        if len(steps) == 5:
            break
    return steps
