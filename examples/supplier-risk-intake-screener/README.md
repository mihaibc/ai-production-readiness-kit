# Supplier Risk Intake Screener

This synthetic example assesses a workflow that screens supplier intake forms and public-style risk indicators to create an initial risk checklist for procurement review.

It is useful because supplier risk screening can influence sensitive business decisions. The example demonstrates why human approval, auditability, compliance gates, and clearly bounded recommendations are required before production use.

## What Developers Should Notice

| Area | Why it matters |
|---|---|
| Decision support | The system may influence sensitive procurement outcomes. |
| Human approval | External or high-impact outputs need named reviewer approval. |
| Governance | Audit logs, compliance gates, and RBAC are launch controls. |
| Production gates | Critical findings can block readiness even when business value is high. |

## Production-Readiness Risks

- sensitive decision-support workflow
- compliance and procurement risk
- human approval gates
- audit logs and governance reviews
- production gates when critical controls are missing

## Expected Risk Profile

High. The workflow has clear value, but missing or incomplete approval and compliance controls should block production readiness.

## Try It

```bash
aipr assess examples/supplier-risk-intake-screener/usecase.yaml
aipr report examples/supplier-risk-intake-screener/usecase.yaml --output examples/supplier-risk-intake-screener/report.md
```
