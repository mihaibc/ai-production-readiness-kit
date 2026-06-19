# Document Ingestion Quality Monitor

This synthetic example assesses an AI-assisted document ingestion workflow that extracts metadata, chunks documents, detects duplicates, validates parsing quality, and flags ingestion failures before documents enter a searchable knowledge base.

It is useful because many AI systems fail quietly at ingestion time: pages are skipped, metadata is wrong, chunks are malformed, duplicates pollute retrieval, or stale documents remain searchable. The example shows how readiness depends on ingestion quality controls, not only answer quality.

## What Developers Should Notice

| Area | Why it matters |
|---|---|
| Ingestion quality | Bad parsing and chunking become downstream retrieval failures. |
| Retrieval coverage | Source coverage and retrieval evaluation need explicit tests. |
| Observability | Processing failures, retries, cost, and latency need workflow-level visibility. |
| Operations | Incident ownership and rollback matter before broad rollout. |

## Production-Readiness Risks

- metadata extraction quality and regression testing
- chunking and source coverage controls
- processing observability for latency, cost, failures, and retries
- operational ownership for ingestion incidents
- partial evaluation coverage that should improve before broad production use

## Expected Risk Profile

Medium. The workflow is internal and operationally useful, but incomplete evals and rollback ownership should be improved before scaling.

## Try It

```bash
aipr assess examples/document-ingestion-quality-monitor/usecase.yaml
aipr report examples/document-ingestion-quality-monitor/usecase.yaml --output examples/document-ingestion-quality-monitor/report.md
```
