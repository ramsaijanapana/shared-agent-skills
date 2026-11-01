# Contributing

Thank you for improving `shared-agent-skills`. This repository ships a portable skill and Claude Code plugin, not an application runtime. Most contributions change markdown skill content, packaging metadata, or validation tooling.

## Before You Start

1. Read [DESIGN-PRINCIPLES.md](DESIGN-PRINCIPLES.md) for the routing model this package enforces.
2. Read [CODEGRAPH.md](../CODEGRAPH.md) for how standalone skills, plugin mirrors, installers, and validation fit together.
3. Skim [USAGE.md](USAGE.md) when changing user-facing behavior or examples.

## Development Setup

Requirements:

- Git
- Python 3.10+ (for validation, version sync, and tests)

Clone and validate the current tree:

```bash
git clone https://github.com/ramsaijanapana/shared-agent-skills.git
cd shared-agent-skills
python -m pip install -e ".[dev]"
pre-commit install
python scripts/validate.py
python scripts/check_plugin_sync.py
```

Run tests and lint:

```bash
pytest tests/ -q
ruff check scripts tests
ruff format --check scripts tests
```

Check that all version sources match:

```bash
python scripts/sync_version.py --check
```

## What To Change Where

| Change | Edit here |
|--------|-----------|
| Skill behavior, playbooks, routing rules | `skills/agent-routing-orchestrator/SKILL.md` |
| Plugin distribution copy | **Do not edit directly** — refresh with `sync_version.py` |
| Package semver | All four version sources (see below) |
| Claude marketplace metadata | `.claude-plugin/marketplace.json` |
| Plugin manifest | `plugins/agent-routing-orchestrator/.claude-plugin/plugin.json` |
| OpenPackage metadata | `openpackage.yml` |
| User onboarding / install docs | `README.md`, `docs/USAGE.md` |
| Prompt examples | `skills/agent-routing-orchestrator/examples/` |
| Validation rules | `scripts/validate.py`, `scripts/check_plugin_sync.py`, and `tests/` |
| Add a second Claude Code plugin | [ADD-PLUGIN.md](ADD-PLUGIN.md) — generalize tooling first, then layout and marketplace |
| Adding a second marketplace plugin | [docs/ADD-PLUGIN.md](ADD-PLUGIN.md) — extension procedure before relaxing single-plugin checks |

The standalone skill under `skills/` is the **source of truth**. The plugin copy under `plugins/.../skills/` must stay byte-identical. `scripts/validate.py` fails if they drift.

## Skill Conventions

- Folder name must match frontmatter `name`.
- Names: lowercase letters, numbers, and hyphens only; 1–64 characters; no leading, trailing, or consecutive hyphens.
- `description` is required and must be ≤ 1024 characters (used for skill discovery).
- `metadata.shared-agent-skills.version` must match the package version.
- `SKILL.md` body should stay ≤ 500 lines.
- Do not add runtime directories under `plugins/agent-routing-orchestrator/` (`agents/`, `commands/`, `hooks/`, `prompts/`, `schemas/`, `scripts/`).
- Avoid forbidden reference strings checked repo-wide by validation (other plugin ecosystems, design-inspiration boilerplate, etc.).

### Frontmatter parser limits

`scripts/validate.py` uses a **line-based frontmatter parser**, not a full YAML engine. Supported patterns:

- Opening/closing fences must be `---` on their own lines (Unix `\n` line endings in the fence region).
- Top-level `key: value` pairs (`name`, `description`, `license`, `metadata`, etc.).
- One level of nested keys under `metadata:` (indented with spaces), e.g. `shared-agent-skills.version`.

**Not supported** — use flat `metadata` keys or plain quoted strings instead:

- Multi-line block scalars (`|`, `>`)
- YAML anchors, aliases, or merge keys
- Lists or maps deeper than `metadata` → one nested key
- Tabs for indentation

If validation misreads frontmatter, simplify the YAML to match the patterns above.

## Version Bumps

Four locations must carry the same semver:

1. `openpackage.yml` → `version:`
2. `skills/agent-routing-orchestrator/SKILL.md` → `metadata.shared-agent-skills.version`
3. `.claude-plugin/marketplace.json` → `plugins[0].version`
4. `plugins/agent-routing-orchestrator/.claude-plugin/plugin.json` → `version`

Use the sync script instead of editing these by hand:

```bash
# Set a new version everywhere and refresh the plugin skill copy
python scripts/sync_version.py 0.6.0

# Verify sync without writing files
python scripts/sync_version.py --check
```

After bumping:

1. Add an entry to [CHANGELOG.md](../CHANGELOG.md) under `[Unreleased]` or a new version section.
2. Run `python scripts/validate.py`.
3. Run `pytest tests/ -q`.

## Pull Request Checklist

- [ ] Skill edits are in `skills/agent-routing-orchestrator/SKILL.md` only
- [ ] `python scripts/sync_version.py --check` passes (or you ran `sync_version.py` after a bump)
- [ ] `python scripts/check_plugin_sync.py` passes
- [ ] `python scripts/validate.py` passes
- [ ] `pytest tests/ -q` passes
- [ ] `ruff check scripts tests` and `ruff format --check scripts tests` pass
- [ ] README / USAGE updated when user-facing behavior changes
- [ ] CHANGELOG updated for user-visible or release-process changes

CI runs the same validation, version-sync check, and tests on every push and pull request to `main`.

## Troubleshooting validation failures

Run the validator from the repo root and fix errors top to bottom — earlier structural failures can hide later ones:

```bash
python scripts/validate.py
```

### Version mismatch

**Error:** `version mismatch: skill=..., marketplace=..., plugin=..., openpackage=...`

**Fix:** One or more of the four version sources is out of sync. Use the sync script instead of editing files by hand:

```bash
python scripts/sync_version.py --check          # verify only
python scripts/sync_version.py 0.5.0            # set semver everywhere + refresh plugin copy
python scripts/validate.py
```

The four locations are `openpackage.yml`, skill frontmatter `metadata.shared-agent-skills.version`, `.claude-plugin/marketplace.json` → `plugins[0].version`, and `plugins/.../plugin.json` → `version`.

If the README shields.io badge is stale after a bump, also run `python scripts/check_version_badge.py` (CI runs this separately from `validate.py`).

### Plugin drift

**Error:** `plugin: skill copy differs from skills/agent-routing-orchestrator/SKILL.md`

**Fix:** Edit `skills/agent-routing-orchestrator/SKILL.md` only — never the plugin mirror directly. Refresh the copy:

```bash
python scripts/check_plugin_sync.py    # shows a unified diff when copies differ
python scripts/sync_version.py --check # rewrites plugin copy when versions already match
```

Re-run `python scripts/validate.py` after syncing.

### Frontmatter errors

**Errors:** `missing opening frontmatter fence`, `missing closing frontmatter fence`, `missing shared-agent-skills.version`, `frontmatter name ... must match folder`, `description is required`, `description exceeds 1024 chars`

**Fix:** Confirm `SKILL.md` opens with `---` on its own line, then flat YAML, then a closing `---`. Use Unix `\n` line endings inside the fence region. Put the package version under `metadata:` as an indented `shared-agent-skills.version:` key. Ensure the folder name matches frontmatter `name`.

See [Frontmatter parser limits](#frontmatter-parser-limits) — block scalars, tabs, YAML anchors, and nesting deeper than `metadata` → one key are not supported.

### Forbidden patterns

**Error:** `<path>: forbidden text pattern '...'`

**Fix:** Remove or rephrase the matched substring anywhere in the repo. Validation flags legacy plugin-ecosystem references and vendor-specific boilerplate. Inspect `FORBIDDEN_TEXT_PATTERNS` in `scripts/validate.py` for the exact substrings — do not copy them into docs or tests.

Keep docs host-neutral and project-agnostic.

### SKILL.md line limit

**Error:** `agent-routing-orchestrator: SKILL.md exceeds 500 lines`

**Fix:** The validator counts every line in the file, including frontmatter. Move long prompt templates to `skills/agent-routing-orchestrator/examples/` and trim the main skill body to ≤ 500 lines, then sync the plugin copy.

### Other common errors

| Error | Fix |
|---|---|
| `missing required section '...'` | Restore the `##` heading named in the error (routing contract, session log, context/completion packets, stop rules, final integration) |
| `plugin: unexpected <dir>/ directory` | Remove forbidden dirs under `plugins/agent-routing-orchestrator/` |
| `expected exactly one plugin` | Do not add a second plugin without updating validation — see [ADD-PLUGIN.md](ADD-PLUGIN.md) |
| `README version badge ... does not match` | Update the shields.io badge in README or run `python scripts/check_version_badge.py` after `sync_version.py` |

## Reporting Issues

Include:

- Host environment (Codex, Claude Code, etc.)
- Install method (plugin, `install.sh`, manual copy)
- Expected vs actual routing behavior
- Relevant session-log excerpt if the issue is about logging or verification

## License

By contributing, you agree that your contributions are licensed under the MIT License in [LICENSE](../LICENSE).
