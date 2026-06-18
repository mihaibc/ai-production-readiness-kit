from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Status = bool | Literal["partial", "unknown"]
Impact = Literal["high", "medium", "low", "none", "unknown"]
ReportStyle = Literal["balanced", "executive", "engineering"]


class FlexibleModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class Business(FlexibleModel):
    problem: str = ""
    expected_impact: str = ""
    users: list[str] = Field(default_factory=list)
    external_output: bool = False
    revenue_or_cost_impact: Impact = "unknown"


class DataReadiness(FlexibleModel):
    sources: list[str] = Field(default_factory=list)
    data_classification: str = "unknown"
    freshness_required: Status = False
    access_control_required: Status = False
    pii_or_sensitive_data: bool = False


class RagQuality(FlexibleModel):
    uses_rag: bool = False
    chunking_strategy_defined: Status = False
    source_citations_required: Status = False
    retrieval_evaluation_exists: Status = False
    rbac_filtered_retrieval: Status = False


class ModelArchitecture(FlexibleModel):
    providers: list[str] = Field(default_factory=list)
    model_router: Status = False
    fallback_model: Status = False
    prompt_versioning: Status = False
    business_logic_in_prompts: bool = False


class Governance(FlexibleModel):
    rbacs_defined: Status = False
    audit_logs: Status = False
    privacy_review_done: Status = False
    legal_review_done: Status = False
    compliance_gates: Status = False


class HumanInTheLoop(FlexibleModel):
    required: bool = False
    approval_before_external_use: Status = False
    escalation_defined: Status = False
    reviewer_role: str = ""


class Evals(FlexibleModel):
    golden_dataset_exists: Status = False
    regression_tests: Status = False
    hallucination_tests: Status = False
    safety_tests: Status = False


class Observability(FlexibleModel):
    token_tracking: Status = False
    latency_tracking: Status = False
    error_tracking: Status = False
    cost_dashboard: Status = False
    prompt_response_tracing: Status = False


class Operations(FlexibleModel):
    incident_owner_defined: Status = False
    rollback_plan: Status = False
    support_process: Status = False
    change_management: Status = False


class Adoption(FlexibleModel):
    training_materials: Status = False
    user_guides: Status = False
    feedback_loop: Status = False
    adoption_metrics: Status = False


class UseCase(FlexibleModel):
    name: str
    owner: str = ""
    stage: str = "idea"
    description: str = ""
    business: Business = Field(default_factory=Business)
    data: DataReadiness = Field(default_factory=DataReadiness)
    rag: RagQuality = Field(default_factory=RagQuality)
    model_architecture: ModelArchitecture = Field(default_factory=ModelArchitecture)
    governance: Governance = Field(default_factory=Governance)
    human_in_the_loop: HumanInTheLoop = Field(default_factory=HumanInTheLoop)
    evals: Evals = Field(default_factory=Evals)
    observability: Observability = Field(default_factory=Observability)
    operations: Operations = Field(default_factory=Operations)
    adoption: Adoption = Field(default_factory=Adoption)


class CategoryScore(BaseModel):
    name: str
    key: str
    score: float
    max_score: int
    rationale: str


class Finding(BaseModel):
    severity: Literal["critical", "warning", "info"]
    message: str
    recommendation: str
    category: str


class Assessment(BaseModel):
    usecase: UseCase
    total_score: int
    base_risk_level: str
    base_risk_summary: str
    risk_level: str
    risk_summary: str
    production_gate: str
    categories: list[CategoryScore]
    findings: list[Finding]
    recommended_next_steps: list[str]

    @property
    def critical_findings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == "critical"]

    @property
    def warnings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == "warning"]


def normalize_status(value: Any) -> Status:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "y"}:
            return True
        if lowered in {"false", "no", "n"}:
            return False
        if lowered in {"partial", "unknown"}:
            return lowered  # type: ignore[return-value]
    return False
