# AI Production Readiness Kit Implementation Plan

## Scope

Build the first usable toolkit version:

- Python package and CLI named `aipr`
- YAML use-case schema
- deterministic readiness scoring
- risk bands and findings
- Markdown report generation
- practical documentation templates
- synthetic examples with reports
- focused test coverage

The article plan is intentionally out of scope for this pass.

## Product Decisions

- Keep the first version as a CLI and documentation repo, not a web app.
- Do not call LLM APIs or depend on a model provider.
- Make output useful to both engineering leaders and hands-on teams.
- Use Apache-2.0 licensing and standard Python packaging.
- Keep examples synthetic and anonymized.

## Implementation Checklist

1. Create package skeleton and project metadata.
2. Define a Pydantic schema for `usecase.yaml`.
3. Implement scoring across the ten readiness categories.
4. Add deterministic critical findings and recommendations.
5. Implement CLI commands:
   - `aipr init`
   - `aipr assess`
   - `aipr report` with `balanced`, `executive`, and `engineering` styles
   - `aipr explain`
   - `aipr templates`
6. Add Jinja2 Markdown templates.
7. Add four synthetic examples:
   - RFQ assistant
   - legal contract review
   - HR onboarding assistant
   - engineering QA assistant
8. Add user-facing docs for scorecards, intake, RAG, governance, observability, cost, risk, and maturity.
9. Add pytest coverage for scoring, CLI basics, and report generation.
10. Run local verification and fix any failures.
11. Add GitHub Actions CI for lint, tests, and package build.

## Validation

Minimum validation before considering the MVP complete:

- `python -m compileall aipr`
- `pytest`
- `ruff check .`
- `uv build`
- `aipr assess examples/rfq-assistant/usecase.yaml`
- `aipr report examples/rfq-assistant/usecase.yaml --style balanced --output /tmp/rfq-report.md`

If dependencies are not installed locally, verify after syncing the project environment.
