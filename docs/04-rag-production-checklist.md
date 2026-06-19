# RAG Production Checklist

RAG is production-ready when retrieval is reliable, permission-aware, fresh, and observable.

Use this checklist for assistants, search workflows, knowledge-base tools, document question answering, and any system where generated output depends on retrieved context.

## Retrieval Quality

- Chunking strategy is documented.
- Retrieval is evaluated separately from generation.
- A golden query set exists.
- Failed and low-confidence queries are reviewed.
- Source coverage is monitored.

## Grounding

- Answers cite sources where users need verification.
- Citations map to the retrieved source material.
- The system can say when it does not know.
- Unsupported claims are measured in evals.

## Access Control

- Permissions are enforced before retrieval.
- Sensitive documents are filtered by user role.
- Retrieval logs do not leak restricted content.
- Access tests cover representative roles.

## Freshness

- Source refresh cadence is documented.
- Stale documents can be detected.
- Retired documents are removed from retrieval.

## Developer Handoff

Treat retrieval quality as a separately testable subsystem. A strong generation model cannot compensate for missing access controls, stale documents, or unmeasured retrieval misses.
