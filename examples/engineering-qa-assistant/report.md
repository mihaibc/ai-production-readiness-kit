# AI Production Readiness Report: Engineering QA Assistant

## Executive Summary

Score: 54 / 100  
Risk level: High risk - Pilot only until critical controls are resolved.
Production gate: Critical findings block production readiness even when the numeric score is higher.

AI-assisted workflow for comparing inspection evidence with QA procedures, surfacing similar historical defects, and preparing review notes for quality engineers.


## Score Breakdown

| Category | Score |
|---|---:|
| Business value and workflow fit | 10 / 10 |
| Data readiness | 10 / 10 |
| RAG / retrieval quality | 5 / 10 |
| Model architecture | 3 / 10 |
| Governance and security | 6.5 / 15 |
| Human-in-the-loop design | 9 / 10 |
| Evals and quality assurance | 3 / 15 |
| Observability and cost control | 5 / 10 |
| Operations and ownership | 1.25 / 5 |
| Adoption and enablement | 1.25 / 5 |

## Critical Findings

1. Retrieval quality is not validated against an evaluation set.

## Warnings

1. Rollback plan is not fully defined.
2. Incident ownership is not fully defined.
3. Business logic is embedded in prompts without a model routing or abstraction layer.
4. Token, latency, or error tracking is incomplete.
5. No formal golden evaluation dataset is defined.

## Recommended Remediation Plan

1. Create a golden retrieval dataset and track source coverage, misses, and wrong-document retrieval.
2. Document how to disable the workflow, revert prompts/models, and notify affected users.
3. Assign an operational owner for failures, escalations, and production changes.
4. Version prompts and separate workflow rules from model-specific instructions.
5. Track token use, latency, errors, and cost per workflow before broader rollout.

## Use Case Context

| Field | Value |
|---|---|
| Owner | Quality Engineering |
| Stage | prototype |
| External output | False |
| Data classification | confidential |
| Uses RAG | True |