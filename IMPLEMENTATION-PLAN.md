# IMPLEMENTATION-PLAN — shared-agent-skills A++

**Source review:** [REVIEW-360.md](REVIEW-360.md)  
**Master graph:** [CODEGRAPH.md](CODEGRAPH.md)  
**Target:** Governance-grade skill package with CI, validation tests, and contributor docs.

---

## Tier 0 — Foundation (complete)

| WS | Title | Priority | Status |
|----|-------|----------|--------|
| 1 | GitHub Actions validate CI | P0 | Done |
| 2 | CONTRIBUTING + CHANGELOG | P0 | Done |
| 3 | Expanded `validate.py` tests | P0 | Done |
| 4 | `sync_version.py` + CI `--check` | P0 | Done |
| 5 | `check_plugin_sync.py` | P0 | Done |
| 6 | Pre-commit hooks | P0 | Done |
| 7 | REVIEW-360 + dimension partials | P0 | Done |
| 8 | Skill prompt examples | P0 | Done |
| 9 | Install script smoke tests | P1 | Done |
| 10 | README badges + validate section | P1 | Done |

Dimension partials: [docs/implementation-plan/](docs/implementation-plan/)

---

## Tier 1 — Release hygiene (complete)

| WS | Title | Priority | Status |
|----|-------|----------|--------|
| 11 | GitHub Release workflow on tag | P1 | Done |
| 12 | Windows + Linux install CI matrix | P2 | Done |
| 13 | `ruff` on scripts/ | P2 | Done |
| 14 | Second-plugin marketplace guide | P3 | Done |
| 15 | Skill section-presence validation | P2 | Done |
| 16 | pytest-cov 80% gate on scripts | P2 | Done |
| 17 | Version badge CI check | P2 | Done |
| 18 | Release SHA256 checksums | P3 | Done |

---

## Completed (Tier 0)

- **`.github/workflows/validate.yml`** — `validate.py`, `sync_version.py --check`, `check_plugin_sync.py`, `pytest`, install smoke on ubuntu + windows
- **`.github/workflows/release.yml`** — semver tag push runs validation gate, verifies tag/version alignment, creates GitHub Release from CHANGELOG
- **`scripts/sync_version.py`** — atomic semver across four version sources + plugin skill refresh
- **`scripts/check_plugin_sync.py`** — standalone vs plugin copy drift with diff preview
- **`tests/`** — validate, sync, plugin sync, install script smoke tests
- **`CONTRIBUTING.md`** + **`docs/CONTRIBUTING.md`** — setup, conventions, PR checklist
- **`CHANGELOG.md`** — Keep a Changelog format
- **`.pre-commit-config.yaml`** — whitespace, JSON/YAML, local validate hooks
- **`skills/agent-routing-orchestrator/examples/`** — branch review, architecture challenge, CI worker, handoff prompts
- **`REVIEW-360.md`** + **`docs/review-360/`** — 360° quality review
- **`IMPLEMENTATION-PLAN.md`** + **`docs/implementation-plan/`** — prioritized roadmap

---

## Verification

```bash
cd shared-agent-skills
python -m pip install -e ".[dev]"
pre-commit run --all-files   # optional locally
python scripts/validate.py
python scripts/sync_version.py --check
python scripts/check_version_badge.py
python scripts/check_plugin_sync.py
ruff check scripts tests
ruff format --check scripts tests
pytest -q --cov=scripts --cov-fail-under=80
```

Expected: all checks pass; real repo validates with zero errors.

---

## Skill edit workflow (maintainers)

1. Edit `skills/agent-routing-orchestrator/SKILL.md` only.
2. Run `python scripts/sync_version.py --check` (or `sync_version.py <ver>` on bump).
3. Run `python scripts/validate.py` and `pytest -q`.
4. Update `CHANGELOG.md` for user-visible changes.
5. Open PR — CI must be green.
