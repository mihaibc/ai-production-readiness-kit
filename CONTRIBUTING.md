# Contributing

Thanks for helping improve AI Production Readiness Kit.

This project is for teams that want practical, deterministic checks before AI workflows reach real users. The best contributions make the toolkit clearer, safer, easier to automate, or more useful in production delivery reviews.

## Good Contribution Areas

- Improve scoring clarity, rationale, or explainability.
- Add useful documentation, examples, starter templates, or review guides.
- Improve validation behavior and error messages.
- Add tests for CLI behavior, scoring, reports, JSON output, gates, or schema validation.
- Improve report templates for executive, balanced, or engineering audiences.
- Improve remediation, comparison, CI, schema export, or developer workflow support.
- Fix bugs in parsing, scoring, packaging, or command behavior.

## Project Principles

- Keep scoring and validation deterministic.
- Do not add an LLM API dependency to the scoring path.
- Use synthetic, generic examples only.
- Do not include employer, customer, personal, confidential, or proprietary information.
- Prefer small, focused pull requests with clear motivation.
- Keep CLI output useful for local developers and CI systems.
- Add or update tests when behavior changes.
- Update documentation for user-facing commands, fields, reports, or outputs.

## Local Setup

```bash
git clone https://github.com/mihaibc/ai-production-readiness-kit.git
cd ai-production-readiness-kit
uv sync --extra dev
```

Run the standard checks:

```bash
uv run ruff check .
uv run pytest
uv build
```

If your environment has restricted cache permissions:

```bash
uv --cache-dir .uv-cache run ruff check .
uv --cache-dir .uv-cache run pytest
uv --cache-dir .uv-cache build
```

## Working With Examples

Examples should be realistic enough to teach production-readiness thinking and generic enough to publish safely.

Each example should include:

- `README.md`
- `usecase.yaml`
- generated `report.md`

Generate a balanced report:

```bash
uv run aipr report examples/document-ingestion-quality-monitor/usecase.yaml --style balanced --output examples/document-ingestion-quality-monitor/report.md
```

When adding a new starter example, also add the matching packaged template:

```text
aipr/starter_templates/<template-name>/usecase.yaml
```

## Pull Request Checklist

Before opening a pull request:

- Run `uv run ruff check .`.
- Run `uv run pytest`.
- Run `uv build`.
- Update docs for user-facing behavior changes.
- Keep examples synthetic and generic.
- Confirm generated reports are refreshed when report templates or examples change.
- Confirm build artifacts, caches, and local environment files are not included.

## Commit Style

Use concise, descriptive commit messages:

```text
Add strict validation for readiness owners
Improve engineering report scoring detail
Refresh synthetic supplier-risk example
```

## Issue Quality

When opening an issue, include:

- the problem you want to solve
- who it helps
- the proposed behavior or documentation change
- commands, YAML snippets, or generated output when relevant
- any tradeoffs or risks

Do not include confidential data in issues, examples, screenshots, logs, or reports.
