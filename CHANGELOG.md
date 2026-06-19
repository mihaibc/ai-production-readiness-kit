# Changelog

All notable changes to this project will be documented here.

## Unreleased

### Documentation

- Refreshed the README with repository health badges, clearer quickstart guidance, a command map, starter-template overview, and developer-focused navigation.
- Polished contributor, implementation, example, report, and issue-template documentation for a more professional open-source experience.

### Added

- JSON output support for assessment, remediation, and comparison workflows.
- Assessment gate options for minimum score and critical findings.
- Remediation, schema export, and comparison CLI commands.
- Blank starter template for new use cases.
- GitHub issue templates for bugs, scoring proposals, example proposals, and documentation improvements.

### Changed

- Refactored CLI internals into dedicated rendering, gate, remediation, and comparison modules.
- Expanded remediation output with priority, effort, category, severity, action, and rationale metadata.

- Added guidance for running AI readiness reviews.
- Added stable JSON output contract documentation.
- Added scoring rationale and production gate documentation.
- Added release process notes for GitHub-first releases and future PyPI publishing.
- Added a future GitHub Action wrapper plan.

## 0.1.0

- Initial CLI for AI production-readiness assessment.
- Added deterministic scoring across ten readiness categories.
- Added balanced, executive, and engineering Markdown report styles.
- Added validation command, schema reference, and GitHub-first usage docs.
- Added synthetic examples and packaged starter templates.
- Added CI checks for lint, tests, and package build.
