# Policy Compliance FAQ Assistant

This synthetic example assesses an internal assistant that answers questions from fictional policy documents with citations and escalation when answers are uncertain or potentially compliance-sensitive.

It is useful because policy assistants can appear low risk while still influencing employee behavior, approvals, or compliance interpretation. The example demonstrates why source attribution, audit logs, escalation, and retrieval evaluation matter.

Production-readiness risks demonstrated:

- RAG answer grounding and source citations
- compliance-style review and escalation
- auditability for policy interpretation
- partial retrieval evaluation coverage
- governance requirements for policy-sensitive guidance

Expected risk profile: medium-high. The workflow has good controls, but incomplete retrieval evaluation and operational ownership should prevent casual expansion.
