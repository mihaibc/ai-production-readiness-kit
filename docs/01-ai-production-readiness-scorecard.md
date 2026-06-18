# AI Production Readiness Scorecard

Use this scorecard before moving an AI workflow from demo to pilot or production.

| Category | Points | Production question |
|---|---:|---|
| Business value and workflow fit | 10 | Does this solve a real workflow problem with measurable impact? |
| Data readiness | 10 | Is the required data available, current, classified, and permissioned? |
| RAG / retrieval quality | 10 | Is retrieval evaluated, grounded, cited, and permission-aware? |
| Model architecture | 10 | Can the workflow tolerate model, provider, or prompt changes? |
| Governance and security | 15 | Are privacy, RBAC, audit, legal, and compliance controls defined? |
| Human-in-the-loop design | 10 | Are human approval and escalation gates explicit where risk requires them? |
| Evals and quality assurance | 15 | Can the team detect regressions, hallucinations, and unsafe outputs? |
| Observability and cost control | 10 | Can the team monitor tokens, latency, errors, cost, and traces? |
| Operations and ownership | 5 | Who owns incidents, rollback, support, and change management? |
| Adoption and enablement | 5 | Can users understand, trust, and improve the workflow? |

## Risk Bands

| Score | Interpretation |
|---:|---|
| 0-39 | Not ready / prototype only |
| 40-59 | High risk / pilot only |
| 60-74 | Medium risk / production only with additional controls |
| 75-89 | Production-ready with minor gaps |
| 90-100 | Strong production readiness |

## Production Gate Rule

The numeric score measures maturity across the full workflow. Critical findings are handled as production gates.

That means a workflow can keep its numeric score, but unresolved critical findings prevent an effective production-ready rating. This mirrors how production governance usually works: a strong overall assessment does not override a missing hard control such as human approval for external output, RBAC for sensitive data, or retrieval evaluation for RAG.

## Review Rhythm

Run the scorecard at intake, before pilot, before launch, and after material model, data, prompt, policy, or workflow changes.
