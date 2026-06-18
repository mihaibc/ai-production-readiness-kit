# LLM Observability Checklist

Production AI workflows need enough visibility to detect quality, reliability, and cost problems.

## Minimum Signals

- Request volume
- Success and error rate
- Latency by workflow step
- Token usage
- Cost by workflow, user group, or tenant
- Model and prompt version
- Retrieval source IDs
- Human approval and rejection rate

## Useful Operational Views

- Top failing prompts or use cases
- Highest-cost users or workflows
- Slowest workflow paths
- Retrieval misses and low-confidence answers
- Safety or policy-triggered responses
- Changes in score after model or prompt updates

## Launch Gate

Do not expand production usage until the team can answer: what changed, who was affected, how much it cost, and whether quality got worse.
