# AI Production Readiness Report: Supplier Risk Intake Screener

## Executive Summary

Score: 52 / 100  
Risk level: High risk - Pilot only until critical controls are resolved.
Production gate: Critical findings block production readiness even when the numeric score is higher.

AI-assisted workflow that reviews synthetic supplier intake forms and public-style risk indicators to prepare an initial risk checklist for procurement review. The workflow supports human decision-making and does not approve suppliers.


## Score Breakdown

| Category | Score |
|---|---:|
| Business value and workflow fit | 10 / 10 |
| Data readiness | 10 / 10 |
| RAG / retrieval quality | 5 / 10 |
| Model architecture | 3 / 10 |
| Governance and security | 6.5 / 15 |
| Human-in-the-loop design | 5 / 10 |
| Evals and quality assurance | 3 / 15 |
| Observability and cost control | 6 / 10 |
| Operations and ownership | 1 / 5 |
| Adoption and enablement | 2 / 5 |

## Critical Findings

1. External outputs do not have a required human approval gate.
2. Retrieval quality is not validated against an evaluation set.

## Warnings

1. Sensitive data is in scope but RBAC is not fully defined.
2. RBAC-aware retrieval is incomplete for sensitive data.
3. Rollback plan is not fully defined.
4. Incident ownership is not fully defined.
5. Business logic is embedded in prompts without a model routing or abstraction layer.
6. Token, latency, or error tracking is incomplete.
7. No formal golden evaluation dataset is defined.

## Recommended Remediation Plan

1. Require approval by a named reviewer role before external use.
2. Create a golden retrieval dataset and track source coverage, misses, and wrong-document retrieval.
3. Complete RBAC roles, access boundaries, and audit expectations before production.
4. Verify permission-filtered retrieval with representative user roles.
5. Document how to disable the workflow, revert prompts/models, and notify affected users.

## Use Case Context

| Field | Value |
|---|---|
| Owner | Procurement Risk Team |
| Stage | prototype |
| External output | True |
| Data classification | confidential |
| Uses RAG | True |