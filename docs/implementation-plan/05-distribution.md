# Implementation Plan — Distribution

**Workstreams:** WS4, WS6 · **Priority:** P0 (Tier 0 complete)

## Actions

| # | Action | Status |
|---|--------|--------|
| 1 | Version sync across openpackage, skill, marketplace, plugin.json | Done |
| 2 | CI `--check` gate prevents drift merges | Done |
| 3 | Install scripts with legacy skill removal | Done |
| 4 | OpenPackage + Claude marketplace metadata | Done |
| 5 | GitHub Release workflow on semver tag | Done |
| 6 | Cross-platform install CI smoke (ubuntu + windows) | Done |

## Deferred (Tier 2)

- Optional OpenPackage publish automation.
- Signed checksums for release artifacts.

## Version bump procedure

```bash
python scripts/sync_version.py 0.6.0
# Update CHANGELOG.md
python scripts/validate.py && pytest -q
git tag v0.6.0 && git push origin v0.6.0
```

Tag push triggers `.github/workflows/release.yml` (validation gate + GitHub Release).
