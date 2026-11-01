# Implementation Plan — Testing & CI

**Workstreams:** WS1, WS3, WS9 · **Priority:** P0 (Tier 0 complete)

## Actions

| # | Action | Status |
|---|--------|--------|
| 1 | `.github/workflows/validate.yml` | Done |
| 2 | CI: validate + sync --check + plugin sync + pytest | Done |
| 3 | `tests/test_validate.py` — positive and negative cases | Done |
| 4 | `tests/test_sync_version.py` | Done |
| 5 | `tests/test_plugin_sync.py` | Done |
| 6 | `tests/test_install_scripts.py` — smoke copy + legacy removal | Done |
| 7 | `pyproject.toml` dev extras + pytest config | Done |

## Deferred (Tier 1)

- CI matrix: ubuntu-latest + windows-latest for install scripts.
- pytest-cov with minimum coverage on `scripts/`.
