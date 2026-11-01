# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A++ loop closure: `docs/A++-LOOP.md`, `docs/ADD-PLUGIN.md`, skill section-presence validation, `scripts/check_version_badge.py`.
- pytest-cov 80% gate on `scripts/`, plugin_sync CLI exit tests, release `checksums.txt` SHA256 artifacts.
- Validation troubleshooting FAQ (`docs/CONTRIBUTING.md`) and plugin install troubleshooting (`docs/USAGE.md`).
- GitHub Actions `validate` workflow for package validation, version sync checks, plugin sync checks, and pytest.
- `REVIEW-360.md`, `IMPLEMENTATION-PLAN.md`, and dimension partials under `docs/review-360/` and `docs/implementation-plan/`.
- `CHANGELOG.md`, pre-commit hooks, README badges, and expanded contributor docs.
- Expanded pytest coverage for `validate.py` (frontmatter, naming, drift, versions, forbidden patterns, CLI exit codes).
- `tests/test_sync_version.py` for version sync automation (`scripts/sync_version.py` with `--check`).
- Root `CONTRIBUTING.md` pointer to `docs/CONTRIBUTING.md`.
- `scripts/check_plugin_sync.py` for standalone/plugin skill drift detection with diff preview.
- Prompt examples under `skills/agent-routing-orchestrator/examples/`.

## [0.5.0] - 2025-06-21

### Added

- Merged `agent-routing-orchestrator` skill replacing legacy cost/delegation skills.
- Claude Code marketplace and plugin metadata.
- Cross-platform install scripts for Codex, Claude, and `.agents` skill directories.
- `scripts/validate.py` for structure, version, and forbidden-pattern checks.
- Usage and design documentation.

[Unreleased]: https://github.com/ramsaijanapana/shared-agent-skills/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/ramsaijanapana/shared-agent-skills/releases/tag/v0.5.0
