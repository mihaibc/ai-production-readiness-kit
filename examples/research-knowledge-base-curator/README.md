# Research Knowledge Base Curator

This synthetic example assesses a workflow that ingests research notes, classifies topics, identifies stale content, recommends archive or review actions, and maintains a searchable internal knowledge base.

It is useful because lower-risk knowledge management workflows are often good candidates for early production AI adoption. The example shows what stronger readiness looks like when the workflow is internal, well-instrumented, and supported by feedback loops.

## What Developers Should Notice

| Area | Why it matters |
|---|---|
| Lifecycle controls | AI workflows need deletion, freshness, and archive paths. |
| Adoption loops | Feedback and usage metrics help improve quality after launch. |
| Operational maturity | Strong ownership and rollback reduce scale risk. |
| Contrast value | This example provides a healthier benchmark against riskier workflows. |

## Production-Readiness Risks

- document lifecycle management
- topic classification and freshness review
- lower-risk internal knowledge workflows
- adoption and feedback measurement
- mature operations with few blockers

## Expected Risk Profile

Low-medium. The workflow should show strong readiness with no critical findings, giving users a contrast against the higher-risk examples.

## Try It

```bash
aipr assess examples/research-knowledge-base-curator/usecase.yaml
aipr report examples/research-knowledge-base-curator/usecase.yaml --output examples/research-knowledge-base-curator/report.md
```
