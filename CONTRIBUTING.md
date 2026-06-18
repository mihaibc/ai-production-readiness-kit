# Contributing

Thank you for considering a contribution to AI Production Readiness Kit.

This project is meant to help teams assess whether AI workflows are ready for production. Good contributions make the toolkit more practical, clearer, safer, or easier to adopt.

## Good Contribution Areas

- Improve scoring clarity or explainability.
- Add useful documentation, examples, or templates.
- Improve validation and error messages.
- Add tests for CLI behavior, scoring, report generation, or schema validation.
- Improve report templates for executive, balanced, or engineering audiences.
- Fix bugs in parsing, scoring, packaging, or CLI commands.

## Contribution Principles

- Keep the tool deterministic. Do not add an LLM API dependency to scoring or validation.
- Use synthetic and generic examples only.
- Do not include employer, customer, personal, confidential, or proprietary information.
- Prefer small, focused changes.
- Keep CLI output useful for both local use and CI.
- Add or update tests when behavior changes.
- Update documentation when user-facing commands, fields, or outputs change.

## Local Setup

```bash
git clone https://github.com/mihaibc/ai-production-readiness-kit.git
cd ai-production-readiness-kit
uv sync --extra dev
```

Run checks:

```bash
uv run ruff check .
uv run pytest
uv build
```

If your environment has restricted cache permissions, use:

```bash
uv --cache-dir .uv-cache run ruff check .
uv --cache-dir .uv-cache run pytest
uv --cache-dir .uv-cache build
```

## Working With Examples

Examples should be realistic enough to teach production-readiness thinking, but generic enough to be safe for public use.

Each example should include:

- `README.md`
- `usecase.yaml`
- generated `report.md`

Generate a balanced report:

```bash
uv run aipr report examples/document-ingestion-quality-monitor/usecase.yaml --style balanced --output examples/document-ingestion-quality-monitor/report.md
```

When adding a new starter example, also add the matching packaged template under:

```text
aipr/starter_templates/<template-name>/usecase.yaml
```

## Pull Request Checklist

Before opening a pull request:

- Run `uv run ruff check .`
- Run `uv run pytest`
- Run `uv build`
- Update docs for user-facing behavior changes.
- Keep examples synthetic and generic.
- Confirm no generated build artifacts, caches, or local environment files are included.

## Commit Style

Use concise, descriptive commit messages, for example:

```text
Add use case validation command
Improve engineering report scoring detail
Replace examples with generic readiness scenarios
```

## Questions and Ideas

If you are unsure whether an idea fits, open an issue with:

- the problem you want to solve
- who it helps
- the proposed behavior or documentation change
- any tradeoffs or risks
