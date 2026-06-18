# Running an AI Readiness Review

Use this guide when a team wants to decide whether an AI workflow is ready for pilot, controlled production, or broader rollout.

## Who Should Attend

- Product or workflow owner
- Engineering owner
- Data owner
- Security, privacy, compliance, or legal reviewer when sensitive workflows are involved
- Operational owner who will handle incidents, support, and rollback
- Representative users or reviewers when adoption risk is high

## Evidence to Bring

- Current `usecase.yaml`
- Architecture sketch or workflow diagram
- Data source list and access-control notes
- Prompt, model, and retrieval change process
- Evaluation examples or test results
- Observability dashboard or logging plan
- Support, incident, and rollback owner
- Any human-review policy or approval flow

## Recommended Review Flow

1. Run `aipr validate usecase.yaml --strict`.
2. Run `aipr assess usecase.yaml --fail-on-critical`.
3. Review the score breakdown and production gate.
4. Run `aipr explain usecase.yaml --category evals` for weak categories.
5. Run `aipr remediation usecase.yaml` and convert actions into delivery work.
6. Compare before and after remediation with `aipr compare before.yaml after.yaml`.
7. Decide whether the workflow remains a demo, moves to pilot, or can launch with controls.

## How to Score `partial`

Use `partial` when a control exists but is not yet reliable enough to be a production gate.

Examples:

- An eval set exists, but it covers only happy paths.
- RBAC is designed, but not tested against representative roles.
- Cost tracking exists, but not at workflow or owner level.
- Human review exists informally, but the reviewer role or escalation path is unclear.

## Launch Blockers

Critical findings should block production unless a senior owner explicitly accepts the risk.

Common blockers:

- External output without human approval.
- Sensitive data without RBAC.
- RAG without retrieval evaluation.
- Sensitive RAG without permission-filtered retrieval.

## Review Outputs

At the end of the review, the team should have:

- Updated `usecase.yaml`
- Readiness score and risk band
- Critical findings and warnings
- Prioritized remediation plan
- Named owner for each action
- Clear decision: demo, pilot, controlled production, or blocked
