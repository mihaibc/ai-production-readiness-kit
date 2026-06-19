# Human-in-the-Loop Decision Tree

Use this when deciding whether an AI workflow needs human review.

Human review should be designed as part of the workflow, not bolted on after risk appears. This guide helps teams decide where approval, review, escalation, and reviewer accountability are required.

## Require Human Approval When

- The output goes to customers, partners, regulators, or the public.
- The workflow affects money, employment, legal terms, safety, access, or compliance.
- The system uses sensitive, confidential, or regulated data.
- A wrong answer could create material business or customer harm.
- The workflow is early-stage and has limited eval coverage.

## Allow Human Review After Output When

- The workflow is internal and low risk.
- Outputs are clearly advisory.
- Users can easily verify the answer from cited sources.
- No sensitive decision is automated.

## Escalation Questions

- Who reviews uncertain outputs?
- Who handles user disputes or corrections?
- What confidence, category, or policy threshold triggers escalation?
- How are reviewer decisions captured for future evals?

## Implementation Note

In `usecase.yaml`, capture this decision under `human_in_the_loop`. External, regulated, financial, legal, safety, access, or compliance-impacting outputs should have explicit approval before use.
