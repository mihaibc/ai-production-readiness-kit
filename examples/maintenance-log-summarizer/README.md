# Maintenance Log Summarizer

This synthetic example assesses a workflow that summarizes equipment maintenance logs, detects recurring issue patterns, and prepares review notes for maintenance engineers.

It is useful because applied AI in engineering often supports expert review rather than replacing it. The example keeps the scenario generic while showing how summarization quality, human review, traceability, and operational ownership affect readiness.

## What Developers Should Notice

| Area | Why it matters |
|---|---|
| Human review | Summaries support expert decisions but should not trigger action alone. |
| Traceability | Reviewers need to move from summary back to the source log. |
| Evaluation | Pattern detection and recurring-issue summaries need representative tests. |
| Operations | Support process and ownership determine whether the workflow can scale. |

## Production-Readiness Risks

- summarization quality and trend extraction
- human review before operational action
- source traceability from summaries back to logs
- moderate eval maturity
- partial operational ownership

## Expected Risk Profile

Medium. The workflow is internal and human-reviewed, but evals and support processes need more maturity before wider use.

## Try It

```bash
aipr assess examples/maintenance-log-summarizer/usecase.yaml
aipr report examples/maintenance-log-summarizer/usecase.yaml --output examples/maintenance-log-summarizer/report.md
```
