# AI Production Readiness Report: RFQ Sales Assistant

## Executive Summary

Score: 64 / 100  
Risk level: High risk - Pilot only until critical controls are resolved.
Production gate: Critical findings block production readiness even when the numeric score is higher.

AI-assisted workflow for finding past proposal content, drafting RFQ responses, and routing them to solution architects for review before client submission.


## Score Breakdown

| Category | Score |
|---|---:|
| Business value and workflow fit | 10 / 10 |
| Data readiness | 10 / 10 |
| RAG / retrieval quality | 5 / 10 |
| Model architecture | 3 / 10 |
| Governance and security | 11.5 / 15 |
| Human-in-the-loop design | 9 / 10 |
| Evals and quality assurance | 3 / 15 |
| Observability and cost control | 8 / 10 |
| Operations and ownership | 1 / 5 |
| Adoption and enablement | 3.5 / 5 |

## Critical Findings

1. Retrieval quality is not validated against an evaluation set.
2. RAG uses sensitive data without fully defined RBAC-aware retrieval.

## Warnings

1. Sensitive data is in scope but RBAC is not fully defined.
2. Rollback plan is not fully defined.
3. Incident ownership is not fully defined.
4. Business logic is embedded in prompts without a model routing or abstraction layer.
5. No formal golden evaluation dataset is defined.

## Recommended Remediation Plan

1. Create a golden retrieval dataset and track source coverage, misses, and wrong-document retrieval.
2. Enforce permissions before retrieval and verify filtered retrieval in tests.
3. Complete RBAC roles, access boundaries, and audit expectations before production.
4. Document how to disable the workflow, revert prompts/models, and notify affected users.
5. Assign an operational owner for failures, escalations, and production changes.

## Use Case Context

| Field | Value |
|---|---|
| Owner | Sales Operations |
| Stage | pilot |
| External output | True |
| Data classification | confidential |
| Uses RAG | True |