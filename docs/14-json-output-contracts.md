# JSON Output Contracts

The CLI supports JSON output for automation and CI integrations. Fields documented here are intended to remain stable within the same minor version. Patch releases may add fields, but should not remove or rename documented fields.

Use these contracts for pull-request gates, dashboards, quality checks, score history, and internal developer tooling.

## Assessment JSON

Command:

```bash
aipr assess examples/document-ingestion-quality-monitor/usecase.yaml --format json
```

Shape:

```json
{
  "usecase": {
    "name": "Document Ingestion Quality Monitor",
    "owner": "Knowledge Platform Team",
    "stage": "pilot"
  },
  "total_score": 73,
  "base_risk_level": "Medium risk",
  "base_risk_summary": "Production only with additional controls",
  "risk_level": "Medium risk",
  "risk_summary": "Production only with additional controls",
  "production_gate": "No critical production blockers identified.",
  "categories": [
    {
      "name": "Business value and workflow fit",
      "key": "business",
      "score": 10.0,
      "max_score": 10,
      "rationale": "Checks whether the use case has a clear problem, users, impact, and delivery stage.",
      "details": []
    }
  ],
  "findings": [
    {
      "severity": "warning",
      "message": "Retrieval evaluation is incomplete.",
      "recommendation": "Expand retrieval evals to cover source coverage, misses, and wrong-document retrieval.",
      "category": "RAG / retrieval quality"
    }
  ],
  "recommended_next_steps": [],
  "gate": {
    "passed": true,
    "failures": [],
    "min_score": null,
    "fail_on_critical": false
  }
}
```

Notes:

- `usecase` is the normalized input object after YAML parsing.
- `categories` is ordered by the scoring model.
- `details` contains field-level scoring contributions for each category.
- `gate` is always included in `assess --format json`.
- `gate.failures` contains human-readable failure messages.

## Remediation JSON

Command:

```bash
aipr remediation examples/supplier-risk-intake-screener/usecase.yaml --format json
```

Shape:

```json
{
  "usecase": "Supplier Risk Intake Screener",
  "score": 52,
  "items": [
    {
      "priority": 1,
      "severity": "critical",
      "category": "Human-in-the-loop",
      "effort": "high",
      "action": "Require approval by a named reviewer role before external use.",
      "why_it_matters": "Prevents high-risk outputs from reaching users without accountable review."
    }
  ]
}
```

Stable item fields:

| Field | Type | Meaning |
|---|---|---|
| `priority` | integer | 1-based order for execution. |
| `severity` | string | `critical`, `warning`, or `info`. |
| `category` | string | Scoring category or `General`. |
| `effort` | string | Deterministic estimate: `low`, `medium`, or `high`. |
| `action` | string | Recommended remediation action. |
| `why_it_matters` | string | Short rationale for the category. |

## Comparison JSON

Command:

```bash
aipr compare examples/supplier-risk-intake-screener/usecase.yaml examples/research-knowledge-base-curator/usecase.yaml --format json
```

Shape:

```json
{
  "before": {
    "name": "Supplier Risk Intake Screener",
    "score": 52,
    "risk_level": "High risk"
  },
  "after": {
    "name": "Research Knowledge Base Curator",
    "score": 91,
    "risk_level": "Strong production readiness"
  },
  "score_delta": 39,
  "categories": [
    {
      "key": "governance",
      "category": "Governance and security",
      "before": 6.5,
      "after": 12.5,
      "delta": 6.0
    }
  ],
  "resolved_findings": [
    "Privacy review is not complete."
  ],
  "new_findings": []
}
```

Notes:

- `before` and `after` summarize the two assessments.
- `score_delta` is `after.score - before.score`.
- `categories` is ordered by the scoring model.
- Finding changes compare finding messages, not internal identifiers.

Consumers should ignore unknown fields so patch releases can add metadata without breaking integrations.
