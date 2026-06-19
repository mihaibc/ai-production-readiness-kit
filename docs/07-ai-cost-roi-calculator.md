# AI Cost and ROI Calculator

Use this worksheet to estimate whether an AI workflow has a credible value case.

Use workflow-level economics instead of model-call economics alone. The real cost of production AI often includes review time, rework, support, monitoring, retrieval infrastructure, and incident handling.

## Inputs

- Monthly users:
- Runs per user per month:
- Average input tokens per run:
- Average output tokens per run:
- Model cost per input token:
- Model cost per output token:
- Other infrastructure cost:
- Human review minutes per run:
- Current process minutes per run:
- Loaded hourly cost:

## Monthly Cost

```text
model_cost = input_tokens_cost + output_tokens_cost
human_review_cost = review_hours * loaded_hourly_cost
total_cost = model_cost + infrastructure_cost + human_review_cost
```

## Monthly Value

```text
time_saved = current_process_hours - new_process_hours
gross_value = time_saved * loaded_hourly_cost
net_value = gross_value - total_cost
```

## Decision Notes

Track value by workflow, not only by model call. The expensive part may be review time, failures, rework, or operational support rather than token cost.

Pair this worksheet with `aipr assess` so value, cost, and production controls are reviewed together.
