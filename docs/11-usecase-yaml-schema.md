# usecase.yaml Schema Reference

`usecase.yaml` describes one AI workflow so the toolkit can validate, score, and report on production readiness. The schema is deterministic and does not send data to any model provider.

## Accepted Status Values

Most control fields accept:

| Value | Meaning | Score behavior |
|---|---|---:|
| `true` | Control exists and is ready enough for the current stage | full points |
| `partial` | Control exists but is incomplete, informal, or not fully verified | half points |
| `false` | Control is missing | zero points |

Use `partial` when the team has started a control but cannot yet rely on it as a production gate.

## Minimal Valid File

```yaml
name: Document Ingestion Quality Monitor
```

This passes schema validation, but `aipr validate --strict` will report completeness warnings because it lacks owner, description, business context, users, and data sources.

## Recommended Structure

```yaml
name: Document Ingestion Quality Monitor
owner: Knowledge Platform Team
stage: pilot
description: >
  AI-assisted workflow that validates document ingestion quality before content
  enters a searchable knowledge base.

business:
  problem: Document search quality drops when ingestion failures are not detected.
  expected_impact: Improve retrieval reliability by catching ingestion defects early.
  users:
    - Knowledge platform engineers
    - Search quality reviewers
  external_output: false
  revenue_or_cost_impact: medium

data:
  sources:
    - Synthetic PDF manuals
    - Generated metadata test files
  data_classification: internal
  freshness_required: true
  access_control_required: true
  pii_or_sensitive_data: false
```

## Top-Level Fields

| Field | Type | Required | Notes |
|---|---|---:|---|
| `name` | string | yes | Human-readable workflow name |
| `owner` | string | no | Team or role accountable for the workflow |
| `stage` | string | no | Example values: `idea`, `prototype`, `pilot`, `controlled_pilot`, `limited_production` |
| `description` | string | no | Short description of the workflow and boundary |

## Sections

### `business`

| Field | Type | Values |
|---|---|---|
| `problem` | string | workflow problem being solved |
| `expected_impact` | string | expected business, quality, speed, or risk impact |
| `users` | list of strings | primary users or reviewers |
| `external_output` | boolean | `true` when outputs reach customers, partners, regulators, or the public |
| `revenue_or_cost_impact` | string | `high`, `medium`, `low`, `none`, `unknown` |

### `data`

| Field | Type | Values |
|---|---|---|
| `sources` | list of strings | source systems, documents, logs, or datasets |
| `data_classification` | string | for example `public`, `internal`, `confidential`, `restricted` |
| `freshness_required` | status | whether freshness expectations are defined |
| `access_control_required` | status | whether access boundaries are defined |
| `pii_or_sensitive_data` | boolean | whether sensitive, regulated, or personal data is in scope |

### `rag`

| Field | Type | Values |
|---|---|---|
| `uses_rag` | boolean | whether retrieval is part of the workflow |
| `chunking_strategy_defined` | status | chunking strategy is documented and reviewed |
| `source_citations_required` | status | answers or reports cite sources where needed |
| `retrieval_evaluation_exists` | status | retrieval is evaluated separately from generation |
| `rbac_filtered_retrieval` | status | retrieval respects user/document permissions |

### `model_architecture`

| Field | Type | Values |
|---|---|---|
| `providers` | list of strings | model providers or internal model interfaces |
| `model_router` | status | model abstraction or routing exists |
| `fallback_model` | status | fallback behavior is defined |
| `prompt_versioning` | status | prompts are versioned and reviewable |
| `business_logic_in_prompts` | boolean | `true` means workflow rules are embedded in prompts |

### `governance`

| Field | Type | Values |
|---|---|---|
| `rbacs_defined` | status | roles and permissions are defined |
| `audit_logs` | status | required activity is auditable |
| `privacy_review_done` | status | privacy review is complete enough for current stage |
| `legal_review_done` | status | legal review is complete enough for current stage |
| `compliance_gates` | status | compliance launch gates are defined |

### `human_in_the_loop`

| Field | Type | Values |
|---|---|---|
| `required` | boolean | whether human review is expected |
| `approval_before_external_use` | status | approval is required before external output |
| `escalation_defined` | status | uncertain or risky cases have escalation paths |
| `reviewer_role` | string | role accountable for review |

### `evals`

| Field | Type | Values |
|---|---|---|
| `golden_dataset_exists` | status | representative examples with expected outcomes exist |
| `regression_tests` | status | prompt/model/retrieval changes are regression-tested |
| `hallucination_tests` | status | unsupported claims are tested or reviewed |
| `safety_tests` | status | unsafe, policy-sensitive, or harmful outputs are tested |

### `observability`

| Field | Type | Values |
|---|---|---|
| `token_tracking` | status | token usage is measured |
| `latency_tracking` | status | latency is measured |
| `error_tracking` | status | errors and failures are measured |
| `cost_dashboard` | status | cost is visible by workflow or owner |
| `prompt_response_tracing` | status | prompts, model versions, and responses are traceable where appropriate |

### `operations`

| Field | Type | Values |
|---|---|---|
| `incident_owner_defined` | status | production incidents have an owner |
| `rollback_plan` | status | disable, rollback, and communication paths exist |
| `support_process` | status | user support and triage are defined |
| `change_management` | status | model, prompt, data, and workflow changes are reviewed |

### `adoption`

| Field | Type | Values |
|---|---|---|
| `training_materials` | status | training material exists |
| `user_guides` | status | user guidance exists |
| `feedback_loop` | status | feedback can be collected and reviewed |
| `adoption_metrics` | status | usage or adoption is measured |

## Validation Commands

```bash
aipr validate usecase.yaml
aipr validate usecase.yaml --strict
```

Use `--strict` when completeness warnings should fail CI.

## Export JSON Schema

Use the schema command when you want editor support, downstream validation, or CI tooling:

```bash
aipr schema --output schema.json
```
