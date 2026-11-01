# Distribution Readiness — shared-agent-skills



**Dimension:** 5/5 · **Grade:** A++ (9.5/10)



## Strengths



- **Cross-platform installers** — `install.sh` and `install.ps1` with target matrix (codex, claude, agents, both, all).

- **Legacy cleanup** — installers remove superseded skills (`cost-aware-delegation`, `cross-agent-project-lead`).

- **OpenPackage manifest** — `openpackage.yml` for portable package metadata.

- **Claude Code plugin** — marketplace.json + plugin.json with version sync.

- **MIT license** — clear redistribution terms.

- **Release automation** — `.github/workflows/release.yml` validates on semver tag push, verifies tag/version alignment, publishes GitHub Release with CHANGELOG notes.

- **Release checksums** — `checksums.txt` (SHA256 of openpackage.yml, install.sh, install.ps1) attached to each release.

- **Version badge gate** — `scripts/check_version_badge.py` in CI.

- **Install CI smoke tests** — ubuntu + windows in validate workflow.



## Gaps to A++



| Gap | Status |

|-----|--------|

| OpenPackage registry publish automation | Human-only — external credentials |

| GPG-signed artifacts | Optional — SHA256 checksums satisfy integrity gate |



## Release procedure



```bash

python scripts/sync_version.py 0.6.0

# Update CHANGELOG.md with ## [0.6.0] section

python scripts/validate.py && pytest -q --cov=scripts --cov-fail-under=80

git tag v0.6.0 && git push origin v0.6.0

```



Pushing `v*` triggers release workflow: full gate, tag/version check, GitHub Release with CHANGELOG body and `checksums.txt`.

