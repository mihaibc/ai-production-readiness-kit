# Policy Compliance FAQ Assistant

This synthetic example assesses an internal assistant that answers questions from fictional policy documents with citations and escalation when answers are uncertain or potentially compliance-sensitive.

It is useful because policy assistants can appear low risk while still influencing employee behavior, approvals, or compliance interpretation. The example demonstrates why source attribution, audit logs, escalation, and retrieval evaluation matter.

## What Developers Should Notice

| Area | Why it matters |
|---|---|
| RAG grounding | Answers need citations that map to accessible source material. |
| Escalation | Ambiguous or compliance-sensitive questions need reviewer paths. |
| Auditability | Policy interpretation often needs traceable decisions and source context. |
| Retrieval evaluation | A confident answer is not useful if retrieval chose the wrong policy. |

## Production-Readiness Risks

- RAG answer grounding and source citations
- compliance-style review and escalation
- auditability for policy interpretation
- partial retrieval evaluation coverage
- governance requirements for policy-sensitive guidance

## Expected Risk Profile

Medium-high. The workflow has good controls, but incomplete retrieval evaluation and operational ownership should prevent casual expansion.

## Try It

```bash
aipr assess examples/policy-compliance-faq-assistant/usecase.yaml
aipr report examples/policy-compliance-faq-assistant/usecase.yaml --output examples/policy-compliance-faq-assistant/report.md
```
