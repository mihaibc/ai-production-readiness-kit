# AI Risk Register

| Risk | Category | Severity | Owner | Mitigation | Status |
|---|---|---|---|---|---|
| Model behavior changes after provider update | Model architecture | Medium |  | Add prompt and model regression tests | Open |
| Retrieval returns documents user should not access | Governance / RAG | Critical |  | Enforce RBAC before retrieval | Open |
| External answer is sent without review | Human-in-the-loop | Critical |  | Require reviewer approval gate | Open |
| Cost increases without alerting | Observability | Medium |  | Add cost dashboard and thresholds | Open |
| No rollback path during incident | Operations | High |  | Define disable and rollback procedure | Open |

## Review Guidance

Every risk should have an owner, mitigation, status, and launch implication. Critical risks should block production until mitigated or formally accepted.
