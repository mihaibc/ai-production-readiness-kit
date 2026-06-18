# GitHub Action Usage

Use the toolkit in another repository to validate and assess AI workflow definitions during pull requests.

## Example Workflow

```yaml
name: AI readiness

on:
  pull_request:
    paths:
      - "ai-use-cases/**/*.yaml"
  workflow_dispatch:

jobs:
  readiness:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install AI Production Readiness Kit
        run: uv tool install git+https://github.com/mihaibc/ai-production-readiness-kit.git

      - name: Validate use cases
        run: |
          for file in ai-use-cases/*.yaml; do
            aipr validate "$file" --strict
          done

      - name: Assess use cases
        run: |
          for file in ai-use-cases/*.yaml; do
            aipr assess "$file" --min-score 75 --fail-on-critical
          done
```

## Repository Layout

```text
ai-use-cases/
  document-ingestion.yaml
  supplier-risk-screening.yaml
```

Keep use-case files close to the delivery work they govern. A pull request that changes a prompt, retrieval source, model, or workflow should update the matching readiness file when controls change.

When the package is published to PyPI later, the install step can change to `uv tool install ai-production-readiness-kit`.

## Recommended Policy

- Use `aipr validate --strict` for schema and completeness checks.
- Use `aipr assess --min-score 75 --fail-on-critical` to fail weak or blocked assessments.
- Use `aipr assess --format json` when another CI step needs machine-readable output.
- Use `aipr remediation usecase.yaml --format json` when a workflow should collect recommended actions.
- Treat critical findings as launch blockers unless the risk is formally accepted.
- Store generated reports as release artifacts only when the team needs review evidence; otherwise, use CLI output in CI.
