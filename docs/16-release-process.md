# Release Process

This project does not publish to PyPI yet. Releases are currently GitHub-first, with install instructions pointing to the repository.

The release process should keep the CLI, documentation, generated reports, JSON contracts, and examples in sync.

## Local Checks

Run the full local verification set before tagging:

```bash
uv --cache-dir .uv-cache run ruff check .
uv --cache-dir .uv-cache run pytest
uv --cache-dir .uv-cache build
```

Manual smoke checks:

```bash
uv --cache-dir .uv-cache run aipr templates
uv --cache-dir .uv-cache run aipr init --template document-ingestion-quality-monitor --output /private/tmp/usecase.yaml --overwrite
uv --cache-dir .uv-cache run aipr assess examples/document-ingestion-quality-monitor/usecase.yaml --format json
uv --cache-dir .uv-cache run aipr remediation examples/supplier-risk-intake-screener/usecase.yaml --format json
uv --cache-dir .uv-cache run aipr compare examples/supplier-risk-intake-screener/usecase.yaml examples/research-knowledge-base-curator/usecase.yaml --format json
```

## Version Bump

1. Update the package version in `pyproject.toml`.
2. Move relevant `CHANGELOG.md` entries from `Unreleased` to the new version heading.
3. Confirm README examples still match the current CLI behavior.
4. Rebuild reports if example output changed.

## Tagging

After the release commit is merged:

```bash
git tag v0.2.0
git push origin v0.2.0
```

Create a GitHub release from the tag and paste the matching changelog section into the release notes.

## Future PyPI Publishing

When PyPI publishing is added, prefer trusted publishing from GitHub Actions instead of long-lived API tokens. The future release workflow should:

- run lint, tests, and build checks
- build source and wheel distributions
- upload only from protected release tags
- require repository maintainer approval for release environments

Do not add publishing automation until package naming, release ownership, and credentials policy are settled.

After PyPI publishing is enabled, update the README, GitHub Action usage docs, and release checklist in the same pull request.
