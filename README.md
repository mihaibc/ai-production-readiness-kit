# AI Production Readiness Kit

Most AI projects fail after the demo because nobody checks whether the workflow is ready for production.

GitHub: [mihaibc/ai-production-readiness-kit](https://github.com/mihaibc/ai-production-readiness-kit)

This project helps teams assess AI workflows across:

- business value
- data readiness
- RAG quality
- model architecture
- governance and security
- human-in-the-loop design
- evaluations
- observability and cost
- operations
- adoption

It is intentionally deterministic. It does not call an LLM API, route data to a model provider, or score use cases with a black box.

## Who This Is For

- Heads of AI
- CTOs
- Engineering Managers
- Product leaders
- AI consultants
- Founders

## Quickstart

Install directly from GitHub:

```bash
uv tool install git+https://github.com/mihaibc/ai-production-readiness-kit.git

aipr init --template document-ingestion-quality-monitor
aipr validate usecase.yaml
aipr assess usecase.yaml
aipr report usecase.yaml --style balanced --output report.md
```

PyPI publishing is not enabled yet; GitHub install is the intended path for now.

For local development:

```bash
git clone https://github.com/mihaibc/ai-production-readiness-kit.git
cd ai-production-readiness-kit
uv sync --extra dev
uv run pytest
```

## Example Output

```text
AI Production Readiness Score: 73 / 100
Risk level: Medium risk / Production only with additional controls

Top risks
1. WARNING: Retrieval evaluation is incomplete.
2. WARNING: Rollback plan is not fully defined.
3. WARNING: Incident ownership is not fully defined.
4. WARNING: No formal golden evaluation dataset is defined.
```

## CLI Commands

```bash
aipr init --template document-ingestion-quality-monitor
aipr validate examples/document-ingestion-quality-monitor/usecase.yaml
aipr validate examples/document-ingestion-quality-monitor/usecase.yaml --strict
aipr assess examples/document-ingestion-quality-monitor/usecase.yaml
aipr report examples/document-ingestion-quality-monitor/usecase.yaml --style balanced --output reports/document-ingestion-report.md
aipr report examples/document-ingestion-quality-monitor/usecase.yaml --style executive --output reports/document-ingestion-executive.md
aipr report examples/document-ingestion-quality-monitor/usecase.yaml --style engineering --output reports/document-ingestion-engineering.md
aipr explain examples/document-ingestion-quality-monitor/usecase.yaml
aipr explain examples/document-ingestion-quality-monitor/usecase.yaml --category evals
aipr templates
```

Use `aipr validate --strict` in CI when missing ownership, business context, users, or data sources should fail the check.

Available starter templates:

- `document-ingestion-quality-monitor`
- `maintenance-log-summarizer`
- `policy-compliance-faq-assistant`
- `research-knowledge-base-curator`
- `supplier-risk-intake-screener`

All examples are synthetic and intentionally generic. They are designed to show reusable production-readiness patterns without depending on confidential, customer-specific, or employer-specific workflows.

## Report Styles

Reports can be exported in three styles:

| Style | Best for | What it emphasizes |
|---|---|---|
| `executive` | Heads of AI, CTOs, steering groups | Decision summary, top risks, required decisions |
| `engineering` | Engineering, data, platform, security teams | Category rationale, control inputs, remediation backlog |
| `balanced` | Mixed product and delivery reviews | Executive summary, score breakdown, findings, next steps |

`balanced` is the default.

## Scoring Model

The readiness score uses 100 points across ten categories:

| Category | Points |
|---|---:|
| Business value and workflow fit | 10 |
| Data readiness | 10 |
| RAG / retrieval quality | 10 |
| Model architecture | 10 |
| Governance and security | 15 |
| Human-in-the-loop design | 10 |
| Evals and quality assurance | 15 |
| Observability and cost control | 10 |
| Operations and ownership | 5 |
| Adoption and enablement | 5 |

Risk bands:

| Score | Risk level |
|---:|---|
| 0-39 | Not ready / prototype only |
| 40-59 | High risk / pilot only |
| 60-74 | Medium risk / production only with additional controls |
| 75-89 | Production-ready with minor gaps |
| 90-100 | Strong production readiness |

Critical findings act as production gates. The numeric score is still shown, but a workflow with unresolved critical findings cannot receive an effective production-ready risk level. This keeps the maturity score useful while preventing a high score from hiding missing controls such as human approval, RBAC, or retrieval evaluation.

## Why This Exists

AI demos are easy. Production AI workflows are hard because they need governance, evals, observability, access control, cost control, human review, and operational ownership.

This kit turns those concerns into a repeatable assessment that creates a better conversation before a workflow reaches real users.

## Repository Contents

- `aipr/` - Python package, CLI, scoring engine, templates
- `.github/workflows/ci.yml` - GitHub Actions checks for lint, tests, and package build
- `CONTRIBUTING.md` - contribution guidelines
- `CODE_OF_CONDUCT.md` - community expectations
- `docs/` - practical templates and checklists
- `docs/11-usecase-yaml-schema.md` - schema reference for `usecase.yaml`
- `docs/12-github-action-usage.md` - example CI usage for downstream repositories
- `examples/` - synthetic AI workflow examples with generated reports
- `tests/` - focused tests for scoring, CLI behavior, and report generation

## Development Checks

Run the same checks used by CI:

```bash
uv run ruff check .
uv run pytest
uv build
```

If your local environment has restricted cache permissions, use:

```bash
uv --cache-dir .uv-cache run ruff check .
uv --cache-dir .uv-cache run pytest
uv --cache-dir .uv-cache build
```

## Roadmap

- v0.1: CLI, scoring model, Markdown reports, docs, examples
- v0.2: richer templates and remediation guidance
- v0.3: GitHub Action for readiness checks in delivery workflows
- v0.4: lightweight web dashboard
- v0.5: team-level AI maturity assessment

## License

Apache-2.0
