# Implementation Plan

This document captures the product and engineering shape of the first usable AI Production Readiness Kit release. It is kept as a project note for maintainers and contributors who want to understand why the repository is structured the way it is.

## Product Scope

The toolkit provides:

- Python package and CLI named `aipr`
- YAML use-case schema
- deterministic readiness scoring
- risk bands, production gates, and findings
- Markdown report generation
- remediation, comparison, and JSON output workflows
- practical documentation templates
- synthetic starter examples with generated reports
- focused test coverage

The project intentionally stays lightweight: no hosted service, no model-provider dependency, and no LLM-based scoring.

## Product Decisions

- Keep the first version as a CLI and documentation repo.
- Make output useful to both engineering leaders and hands-on delivery teams.
- Use Apache-2.0 licensing and standard Python packaging.
- Keep examples synthetic, anonymized, and broadly reusable.
- Treat critical findings as production gates even when the numeric score is high.
- Keep future automation thin so the CLI remains the single scoring implementation.

## Current Implementation Areas

| Area | Status | Notes |
|---|---|---|
| Package skeleton and metadata | Complete | Managed through `pyproject.toml` and Hatchling. |
| Pydantic use-case schema | Complete | Documented in `docs/11-usecase-yaml-schema.md`. |
| Deterministic scoring | Complete | Ten-category model with weighted scoring. |
| Production gates | Complete | Critical findings can block production readiness. |
| CLI commands | Complete | `init`, `validate`, `assess`, `report`, `explain`, `remediation`, `schema`, `compare`, `templates`. |
| Report styles | Complete | Balanced, executive, and engineering Markdown outputs. |
| Synthetic examples | Complete | Five packaged starter templates with generated reports. |
| JSON contracts | Complete | Stable automation shapes documented for assess, remediation, and compare. |
| CI checks | Complete | GitHub Actions runs lint, tests, and package build. |
| Dedicated GitHub Action wrapper | Planned | See `docs/17-github-action-wrapper-plan.md`. |

## Verification

Run the standard local verification set:

```bash
uv --cache-dir .uv-cache run ruff check .
uv --cache-dir .uv-cache run pytest
uv --cache-dir .uv-cache build
```

Run smoke checks after CLI or report-template changes:

```bash
uv --cache-dir .uv-cache run aipr templates
uv --cache-dir .uv-cache run aipr validate examples/document-ingestion-quality-monitor/usecase.yaml --strict
uv --cache-dir .uv-cache run aipr assess examples/document-ingestion-quality-monitor/usecase.yaml --format json
uv --cache-dir .uv-cache run aipr remediation examples/supplier-risk-intake-screener/usecase.yaml --format json
uv --cache-dir .uv-cache run aipr compare examples/supplier-risk-intake-screener/usecase.yaml examples/research-knowledge-base-curator/usecase.yaml --format json
```

Regenerate example reports when report templates or example `usecase.yaml` files change:

```bash
uv --cache-dir .uv-cache run aipr report examples/document-ingestion-quality-monitor/usecase.yaml --style balanced --output examples/document-ingestion-quality-monitor/report.md
```

Repeat for each example directory.

## Near-Term Improvements

- Package a dedicated GitHub Action wrapper around the existing CLI.
- Add richer validation messages for common incomplete controls.
- Expand engineering report detail where it helps remediation planning.
- Add more examples for high-governance, low-risk automation, and RAG-heavy workflows.
- Prepare PyPI publishing once ownership, package naming, and release policy are settled.
