# GitHub Action Wrapper Plan

The repository can already be used in GitHub Actions by installing the CLI and running `aipr validate` or `aipr assess`. A dedicated wrapper action is planned for a future version to make adoption easier in downstream repositories.

The wrapper should improve ergonomics without creating a second scoring implementation. The CLI remains the source of truth for validation, scoring, findings, JSON output, and report generation.

## Intended Inputs

| Input | Default | Description |
|---|---|---|
| `path` | `usecase.yaml` | Path to the use case file to assess. |
| `min-score` | none | Optional minimum readiness score. |
| `fail-on-critical` | `true` | Fail when critical findings are present. |
| `strict` | `false` | Run validation in strict mode before assessment. |
| `report-style` | `balanced` | Optional report style: `balanced`, `executive`, or `engineering`. |

## Intended Behavior

The wrapper should:

1. Install the pinned package version.
2. Run `aipr validate`.
3. Run `aipr assess --format json`.
4. Apply the configured score and critical-finding gates.
5. Optionally generate a Markdown report artifact.
6. Expose summary outputs for workflow annotations or PR comments.

## Proposed Outputs

| Output | Description |
|---|---|
| `score` | Final readiness score. |
| `risk-level` | Effective risk level after production gates. |
| `passed` | Whether the configured gate passed. |
| `critical-count` | Number of critical findings. |
| `report-path` | Path to the generated report, when requested. |

## Non-Goals For The First Wrapper

- No dashboard service.
- No remote data upload.
- No LLM-based scoring.
- No automatic issue creation.
- No policy exceptions hidden inside the action.

The first wrapper should stay thin and transparent. It should make the existing CLI easier to use in CI without creating a second scoring implementation.

Design priority: predictable pull-request feedback, stable outputs, and no hidden network calls beyond dependency installation.
