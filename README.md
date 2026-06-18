# AI Production Readiness Kit

Most AI projects fail after the demo because nobody checks whether the workflow is ready for production.

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

```bash
pip install ai-production-readiness-kit

aipr init --template rfq-assistant
aipr assess usecase.yaml
aipr report usecase.yaml --style balanced --output report.md
```

For local development:

```bash
pip install -e ".[dev]"
pytest
```

## Example Output

```text
AI Production Readiness Score: 64 / 100
Risk level: High risk / Pilot only until critical controls are resolved

Top risks
1. CRITICAL: Retrieval quality is not validated against an evaluation set.
2. CRITICAL: RAG uses sensitive data without fully defined RBAC-aware retrieval.
3. WARNING: Sensitive data is in scope but RBAC is not fully defined.
4. WARNING: Rollback plan is not fully defined.
5. WARNING: Incident ownership is not fully defined.
```

## CLI Commands

```bash
aipr init --template rfq-assistant
aipr assess examples/rfq-assistant/usecase.yaml
aipr report examples/rfq-assistant/usecase.yaml --style balanced --output reports/rfq-report.md
aipr report examples/rfq-assistant/usecase.yaml --style executive --output reports/rfq-executive.md
aipr report examples/rfq-assistant/usecase.yaml --style engineering --output reports/rfq-engineering.md
aipr explain examples/rfq-assistant/usecase.yaml
aipr templates
```

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
- `docs/` - practical templates and checklists
- `examples/` - synthetic AI workflow examples with generated reports
- `tests/` - focused tests for scoring, CLI behavior, and report generation

## Roadmap

- v0.1: CLI, scoring model, Markdown reports, docs, examples
- v0.2: richer templates and remediation guidance
- v0.3: GitHub Action for readiness checks in delivery workflows
- v0.4: lightweight web dashboard
- v0.5: team-level AI maturity assessment

## License

Apache-2.0
