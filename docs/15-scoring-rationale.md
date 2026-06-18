# Scoring Rationale

The scorecard is deterministic and intentionally simple. It is designed to create a consistent readiness conversation, not to replace security, legal, privacy, or architecture review.

The total score is 100 points across ten categories. Boolean fields receive full credit when `true` and no credit when `false`. Fields that accept `partial` receive half credit when partially implemented. `unknown` is treated as not ready because an unknown control cannot be relied on in production.

## Category Allocation

| Category | Points | Why it matters |
|---|---:|---|
| Business value and workflow fit | 10 | Confirms the workflow has a clear problem, users, impact, and delivery stage. |
| Data readiness | 10 | Checks source clarity, classification, freshness, and access boundaries. |
| RAG / retrieval quality | 10 | Checks chunking, citations, retrieval evaluation, and permission-aware retrieval. |
| Model architecture | 10 | Checks provider dependency, fallback, prompt versioning, and prompt coupling. |
| Governance and security | 15 | Checks RBAC, audit logs, privacy, legal, and compliance gates. |
| Human-in-the-loop design | 10 | Checks whether review and escalation match the workflow risk. |
| Evals and quality assurance | 15 | Checks golden data, regression tests, hallucination tests, and safety tests. |
| Observability and cost control | 10 | Checks token, latency, error, cost, and trace visibility. |
| Operations and ownership | 5 | Checks incident ownership, rollback, support, and change management. |
| Adoption and enablement | 5 | Checks training, guides, feedback loops, and adoption metrics. |

## Field Examples

Use `true` when the control exists and is usable by the team today.

```yaml
evals:
  regression_tests: true
```

Use `partial` when the control exists but does not cover the full workflow, all user groups, or all release paths.

```yaml
observability:
  cost_dashboard: partial
```

Use `false` when the control does not exist or is only planned.

```yaml
operations:
  rollback_plan: false
```

Use `unknown` when the team cannot confirm the current state. Unknown values score like missing controls.

```yaml
governance:
  legal_review_done: unknown
```

## Production Gate Rules

The numeric score sets the base risk band:

| Score | Risk level |
|---:|---|
| 0-39 | Not ready |
| 40-59 | High risk |
| 60-74 | Medium risk |
| 75-89 | Production-ready |
| 90-100 | Strong production readiness |

Critical findings can override the effective production posture. When a workflow has unresolved critical findings, the score is still shown, but the assessment cannot present the workflow as production-ready. This prevents a strong category average from hiding missing controls such as approval gates, RBAC, privacy review, or retrieval evaluation.

## Critical Finding Examples

Critical findings are reserved for controls that can block responsible production use:

- Sensitive or external outputs without required human approval.
- RAG workflows without retrieval evaluation for high-impact decisions.
- Sensitive data workflows without access controls or governance review.
- Compliance-heavy workflows without auditability or approval gates.

Warnings identify meaningful gaps that should be planned before scale, but do not always block a controlled pilot.

Info items are next-step suggestions that improve maturity or adoption.
