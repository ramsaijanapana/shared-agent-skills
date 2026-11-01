# Testing & CI — shared-agent-skills



**Dimension:** 3/5 · **Grade:** A++ (9.6/10)



## Strengths



- **GitHub Actions** — `.github/workflows/validate.yml` runs validate, version sync, badge check, plugin sync, ruff, pytest with coverage.

- **Pytest suite** — unit tests for all scripts including CLI exit codes.

- **Coverage gate** — `pytest-cov` with 80% minimum on `scripts/`.

- **Install smoke tests** — ubuntu + windows-latest in validate workflow.

- **Fixtures** — `minimal_package` conftest builds a valid tree for negative tests.

- **Real-repo gate** — `test_real_repo_passes_validation` ensures production tree stays valid.



## Gaps to A++



None automatable at current scope.



## CI gate commands



```yaml

python scripts/validate.py

python scripts/sync_version.py --check

python scripts/check_version_badge.py

python scripts/check_plugin_sync.py

ruff check scripts tests

ruff format --check scripts tests

pytest -q --cov=scripts --cov-fail-under=80

```

