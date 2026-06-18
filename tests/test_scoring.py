from pathlib import Path

import yaml

from aipr.models import UseCase
from aipr.scoring import assess


def test_document_ingestion_example_generates_medium_risk_warnings() -> None:
    data = yaml.safe_load(Path("examples/document-ingestion-quality-monitor/usecase.yaml").read_text())
    usecase = UseCase.model_validate(data)

    assessment = assess(usecase)

    assert 0 <= assessment.total_score <= 100
    assert assessment.base_risk_level == "Medium risk"
    assert assessment.risk_level == "Medium risk"
    assert not assessment.critical_findings
    assert any("Retrieval evaluation is incomplete" in finding.message for finding in assessment.findings)


def test_supplier_risk_example_has_critical_production_gates() -> None:
    data = yaml.safe_load(Path("examples/supplier-risk-intake-screener/usecase.yaml").read_text())
    usecase = UseCase.model_validate(data)

    assessment = assess(usecase)

    assert assessment.risk_level == "High risk"
    assert "Critical findings block" in assessment.production_gate
    assert any("human approval gate" in finding.message for finding in assessment.findings)
    assert any("Retrieval quality" in finding.message for finding in assessment.findings)


def test_research_curator_scores_higher_than_supplier_risk_screener() -> None:
    research_data = yaml.safe_load(Path("examples/research-knowledge-base-curator/usecase.yaml").read_text())
    supplier_data = yaml.safe_load(Path("examples/supplier-risk-intake-screener/usecase.yaml").read_text())

    research_assessment = assess(UseCase.model_validate(research_data))
    supplier_assessment = assess(UseCase.model_validate(supplier_data))

    assert research_assessment.total_score > supplier_assessment.total_score
    assert not research_assessment.critical_findings


def test_low_risk_internal_workflow_scores_higher_than_uncontrolled_external_workflow() -> None:
    internal = UseCase.model_validate(
        {
            "name": "Internal Assistant",
            "stage": "limited_production",
            "business": {
                "problem": "Repeated questions",
                "expected_impact": "Reduce support time",
                "users": ["Employees"],
                "external_output": False,
                "revenue_or_cost_impact": "low",
            },
            "rag": {
                "uses_rag": True,
                "chunking_strategy_defined": True,
                "source_citations_required": True,
                "retrieval_evaluation_exists": True,
                "rbac_filtered_retrieval": True,
            },
            "evals": {
                "golden_dataset_exists": True,
                "regression_tests": True,
                "hallucination_tests": True,
                "safety_tests": True,
            },
            "operations": {
                "incident_owner_defined": True,
                "rollback_plan": True,
                "support_process": True,
                "change_management": True,
            },
        }
    )
    external = UseCase.model_validate(
        {
            "name": "External Assistant",
            "business": {
                "external_output": True,
                "revenue_or_cost_impact": "high",
            },
            "human_in_the_loop": {
                "required": True,
                "approval_before_external_use": False,
            },
        }
    )

    assert assess(internal).total_score > assess(external).total_score
    assert any(
        "human approval gate" in finding.message
        for finding in assess(external).findings
    )


def test_critical_findings_cap_production_ready_risk_band() -> None:
    usecase = UseCase.model_validate(
        {
            "name": "Otherwise Mature External Workflow",
            "stage": "production_candidate",
            "business": {
                "problem": "Customer workflow",
                "expected_impact": "Reduce cycle time",
                "users": ["Customers"],
                "external_output": True,
                "revenue_or_cost_impact": "high",
            },
            "data": {
                "sources": ["Public knowledge base"],
                "data_classification": "public",
                "freshness_required": True,
                "access_control_required": True,
                "pii_or_sensitive_data": False,
            },
            "rag": {
                "uses_rag": True,
                "chunking_strategy_defined": True,
                "source_citations_required": True,
                "retrieval_evaluation_exists": True,
                "rbac_filtered_retrieval": True,
            },
            "model_architecture": {
                "providers": ["Provider"],
                "model_router": True,
                "fallback_model": True,
                "prompt_versioning": True,
                "business_logic_in_prompts": False,
            },
            "governance": {
                "rbacs_defined": True,
                "audit_logs": True,
                "privacy_review_done": True,
                "legal_review_done": True,
                "compliance_gates": True,
            },
            "human_in_the_loop": {
                "required": True,
                "approval_before_external_use": False,
                "escalation_defined": True,
                "reviewer_role": "Operations Lead",
            },
            "evals": {
                "golden_dataset_exists": True,
                "regression_tests": True,
                "hallucination_tests": True,
                "safety_tests": True,
            },
            "observability": {
                "token_tracking": True,
                "latency_tracking": True,
                "error_tracking": True,
                "cost_dashboard": True,
                "prompt_response_tracing": True,
            },
            "operations": {
                "incident_owner_defined": True,
                "rollback_plan": True,
                "support_process": True,
                "change_management": True,
            },
            "adoption": {
                "training_materials": True,
                "user_guides": True,
                "feedback_loop": True,
                "adoption_metrics": True,
            },
        }
    )

    assessment = assess(usecase)

    assert assessment.base_risk_level in {"Production-ready", "Strong production readiness"}
    assert assessment.risk_level == "High risk"
    assert assessment.risk_summary == "Pilot only until critical controls are resolved"
