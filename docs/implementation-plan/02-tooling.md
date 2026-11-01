# Implementation Plan — Code Quality & Tooling

**Workstreams:** WS3, WS4, WS5 · **Priority:** P0 (Tier 0 complete)

## Actions

| # | Action | Status |
|---|--------|--------|
| 1 | `scripts/validate.py` — structure, frontmatter, drift, versions | Done |
| 2 | `scripts/sync_version.py` — four-source atomic bump | Done |
| 3 | `scripts/check_plugin_sync.py` — drift with diff preview | Done |
| 4 | Expanded pytest for validate rules | Done |
| 5 | Pre-commit local validate hooks | Done |

## Deferred (Tier 1)

- Optional mypy on sync/validate modules.

## Done (Tier 1)

- `ruff` configuration for `scripts/` and `tests/` in `pyproject.toml`.
- Pre-commit `ruff` + `ruff-format` hooks.
- CI `ruff check` and `ruff format --check` gates.
- Frontmatter parser limits documented in `docs/CONTRIBUTING.md`.
