# AI Production Readiness Kit

[![CI](https://github.com/mihaibc/ai-production-readiness-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/mihaibc/ai-production-readiness-kit/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](pyproject.toml)
[![Ruff](https://img.shields.io/badge/lint-ruff-46a7f5.svg)](https://docs.astral.sh/ruff/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Issues](https://img.shields.io/github/issues/mihaibc/ai-production-readiness-kit)](https://github.com/mihaibc/ai-production-readiness-kit/issues)
[![Stars](https://img.shields.io/github/stars/mihaibc/ai-production-readiness-kit?style=flat)](https://github.com/mihaibc/ai-production-readiness-kit/stargazers)

A deterministic CLI and documentation kit for deciding whether an AI workflow is ready for real users.

Most AI demos fail after the prototype because nobody has checked the operational parts: data boundaries, retrieval quality, evals, governance, observability, cost, ownership, and human review. This project turns those checks into repeatable YAML, scores, reports, remediation plans, and CI gates.

## Why Developers Use It

- Score an AI workflow across ten production-readiness categories.
- Validate `usecase.yaml` files locally or in CI.
- Generate executive, balanced, or engineering Markdown reports.
- Export JSON for automation, dashboards, and pull-request checks.
- Compare two workflows or two versions of the same workflow.
- Start from realistic synthetic templates instead of a blank page.

The toolkit is intentionally deterministic. It does not call an LLM API, send data to a model provider, or hide scoring behind a black box.

## Quickstart

Install from GitHub:

```bash
uv tool install git+https://github.com/mihaibc/ai-production-readiness-kit.git
```

Create and assess a workflow:

```bash
aipr init --template document-ingestion-quality-monitor
aipr validate usecase.yaml --strict
aipr assess usecase.yaml --min-score 70 --fail-on-critical
aipr report usecase.yaml --style balanced --output report.md
```

Create a blank starter instead:

```bash
aipr init --blank --output usecase.yaml
```

PyPI publishing is not enabled yet; GitHub install is the supported path for now.

## Local Development

```bash
git clone https://github.com/mihaibc/ai-production-readiness-kit.git
cd ai-production-readiness-kit
uv sync --extra dev
uv run ruff check .
uv run pytest
uv build
```

If your environment restricts shared cache directories:

```bash
uv --cache-dir .uv-cache run ruff check .
uv --cache-dir .uv-cache run pytest
uv --cache-dir .uv-cache build
```

## Example Output

```text
Document Ingestion Quality Monitor
Score: 73 / 100
Risk: Medium risk - Production only with additional controls
Production gate: No critical production blockers identified.

Top Risks
1. WARNING: Retrieval evaluation is incomplete.
2. WARNING: Rollback plan is not fully defined.
3. WARNING: Incident ownership is not fully defined.
4. WARNING: No formal golden evaluation dataset is defined.
```

## Command Map

| Goal | Command |
|---|---|
| List starter templates | `aipr templates` |
| Create from a template | `aipr init --template document-ingestion-quality-monitor` |
| Create a blank file | `aipr init --blank --output usecase.yaml` |
| Validate schema | `aipr validate usecase.yaml` |
| Enforce completeness | `aipr validate usecase.yaml --strict` |
| Score readiness | `aipr assess usecase.yaml` |
| Fail weak assessments in CI | `aipr assess usecase.yaml --min-score 75 --fail-on-critical` |
| Generate a report | `aipr report usecase.yaml --style balanced --output report.md` |
| Explain a category | `aipr explain usecase.yaml --category evals` |
| Build a remediation plan | `aipr remediation usecase.yaml` |
| Export JSON schema | `aipr schema --output schema.json` |
| Compare two assessments | `aipr compare before.yaml after.yaml` |

JSON output is available for automation:

```bash
aipr assess usecase.yaml --format json
aipr remediation usecase.yaml --format json
aipr compare before.yaml after.yaml --format json
```

## Starter Templates

| Template | What it demonstrates |
|---|---|
| `document-ingestion-quality-monitor` | Ingestion quality, chunking, observability, and rollback gaps |
| `maintenance-log-summarizer` | Human-reviewed summarization for operational teams |
| `policy-compliance-faq-assistant` | RAG grounding, citations, auditability, and escalation |
| `research-knowledge-base-curator` | Lower-risk internal knowledge workflows with mature operations |
| `supplier-risk-intake-screener` | Sensitive decision support with production-blocking controls |

All examples are synthetic and generic. They are designed to teach reusable production-readiness patterns without relying on confidential customer, employer, or personal data.

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

Critical findings act as production gates. A workflow can keep its numeric score, but unresolved critical findings prevent an effective production-ready rating. This keeps the maturity score useful while making hard blockers visible.

## Reports

Reports can be exported in three styles:

| Style | Best for | Emphasis |
|---|---|---|
| `executive` | Heads of AI, CTOs, steering groups | Decision summary, top risks, required decisions |
| `balanced` | Mixed product and delivery reviews | Summary, score breakdown, findings, remediation |
| `engineering` | Engineering, data, platform, security teams | Control inputs, category rationale, field-level scoring |

`balanced` is the default.

## Repository Guide

| Path | Purpose |
|---|---|
| `aipr/` | Python package, CLI, scoring engine, templates |
| `aipr/starter_templates/` | Packaged starter `usecase.yaml` examples |
| `docs/` | Scorecards, templates, checklists, and operating guidance |
| `examples/` | Synthetic use cases with generated reports |
| `tests/` | CLI, scoring, report, remediation, comparison, and gate tests |
| `.github/workflows/ci.yml` | Lint, test, and build checks |

Key docs:

- [Schema reference](docs/11-usecase-yaml-schema.md)
- [GitHub Action usage](docs/12-github-action-usage.md)
- [Running an AI readiness review](docs/13-running-ai-readiness-review.md)
- [JSON output contracts](docs/14-json-output-contracts.md)
- [Scoring rationale](docs/15-scoring-rationale.md)
- [Release process](docs/16-release-process.md)

## Roadmap

- v0.1: CLI, scoring model, Markdown reports, docs, examples.
- v0.2: JSON output, CI gates, remediation, schema export, comparison, blank starter.
- v0.3: Dedicated GitHub Action wrapper for downstream readiness checks.
- v0.4: Lightweight web dashboard.
- v0.5: Team-level AI maturity assessment.

## Contributing

Contributions are welcome when they make the toolkit clearer, safer, more deterministic, or easier to adopt. Good first areas include docs, examples, validation messages, report templates, scoring explainability, and focused tests.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

Apache-2.0
