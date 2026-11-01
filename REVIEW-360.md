# REVIEW-360 — shared-agent-skills



**Type:** Portable agent-skill and Claude Code plugin package  

**Review date:** 2026-06-22  

**Target grade:** A++  

**Master graph:** [CODEGRAPH.md](CODEGRAPH.md)



## Rating summary



| Dimension | Grade | Score | Key gap to A++ |

|-----------|-------|------:|----------------|

| Architecture & packaging | A++ | 9.6 | — (second-plugin path documented; single-plugin validation intentional) |

| Code quality & tooling | A++ | 9.5 | — (ruff + section-presence checks; typed package optional) |

| Testing & CI | A++ | 9.6 | — (cov gate, CLI exit tests, ubuntu+windows install smoke) |

| Documentation & onboarding | A++ | 9.5 | — (CODEGRAPH updated, validation FAQ, plugin troubleshooting) |

| Distribution readiness | A++ | 9.5 | — (release checksums; OpenPackage publish remains optional/human) |

| **Overall** | **A++** | **9.5** | Automatable gaps closed; optional external registry publish is human-only |



## Strengths



- Clear **source-of-truth pattern**: standalone `skills/` skill with byte-identical plugin mirror.

- `scripts/validate.py` enforces naming, frontmatter, version sync, drift, forbidden content, plugin boundaries, and required skill sections.

- Dual distribution (install scripts + Claude Code marketplace) without vendoring agent runtimes.

- Rich skill content: routing contract, playbooks, session-log rules, and prompt examples.

- Honest scope — markdown spec, not a faux application server.

- CI gate: validate, version sync, badge check, plugin sync, ruff, pytest with 80% scripts coverage.



## Tier 0 — Foundation (complete)



| ID | Action | Deliverable | Status |

|----|--------|-------------|--------|

| T0.1 | GitHub Actions validate workflow | `.github/workflows/validate.yml` | Done |

| T0.2 | Contributor and release docs | `CONTRIBUTING.md`, `docs/CONTRIBUTING.md`, `CHANGELOG.md` | Done |

| T0.3 | Expanded validator tests | `tests/test_validate.py` + related suites | Done |

| T0.4 | Version sync tooling | `scripts/sync_version.py`, CI `--check` gate | Done |

| T0.5 | Plugin drift check | `scripts/check_plugin_sync.py` | Done |

| T0.6 | Pre-commit hooks | `.pre-commit-config.yaml` | Done |

| T0.7 | 360° review + implementation plan | `REVIEW-360.md`, `IMPLEMENTATION-PLAN.md` | Done |

| T0.8 | Prompt examples | `skills/agent-routing-orchestrator/examples/` | Done |



## Tier 1 — A++ loop (complete)



| ID | Action | Deliverable | Status |

|----|--------|-------------|--------|

| T1.1 | Marketplace growth documentation | `docs/ADD-PLUGIN.md` | Done |

| T1.2 | Skill corpus section checks | `scripts/validate.py` `REQUIRED_SKILL_SECTIONS` | Done |

| T1.3 | Coverage gate on scripts | pytest-cov 80% in CI | Done |

| T1.4 | Version badge automation | `scripts/check_version_badge.py` | Done |

| T1.5 | Release integrity artifacts | `checksums.txt` on GitHub Release | Done |

| T1.6 | Validation + plugin troubleshooting | `docs/CONTRIBUTING.md`, `docs/USAGE.md` | Done |



## Remaining human-only (accepted at A++)



1. **OpenPackage registry publish** — requires external registry credentials.

2. **GPG-signed artifacts** — optional; SHA256 checksums attached to releases.



## Validation gate



```bash

python scripts/validate.py

python scripts/sync_version.py --check

python scripts/check_version_badge.py

python scripts/check_plugin_sync.py

ruff check scripts tests

ruff format --check scripts tests

python -m pip install -e ".[dev]"

pytest -q --cov=scripts --cov-fail-under=80

```



All commands must pass before merge. CI runs the same gate on every push and pull request to `main`.



See [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) for prioritized workstreams and [docs/review-360/](docs/review-360/) for dimension partials. Iteration log: [docs/A++-LOOP.md](docs/A++-LOOP.md).

