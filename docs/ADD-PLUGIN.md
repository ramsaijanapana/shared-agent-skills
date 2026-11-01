# Adding a Second Claude Code Plugin

This marketplace currently ships **one** plugin (`agent-routing-orchestrator`). `scripts/validate.py` enforces that with `expected exactly one plugin` and hard-coded paths. You can add a second plugin without *relaxing* that gate — replace single-plugin assumptions with an explicit plugin registry and loop over registered plugins.

**Do not** append a second entry to `marketplace.json` until the tooling changes below land; validation will fail immediately.

## Prerequisites

- Read [DESIGN-PRINCIPLES.md](DESIGN-PRINCIPLES.md) and [CONTRIBUTING.md](CONTRIBUTING.md) skill conventions.
- Choose a plugin name: lowercase letters, numbers, hyphens only; 1–64 chars; no leading/trailing/consecutive hyphens. Name must match the skill folder and `plugin.json` `name`.
- Decide section requirements for the new skill (the orchestrator skill has six mandatory `##` headings checked today; a new plugin may need its own list or none).
- Keep `skills/<name>/SKILL.md` as the **source of truth**; the plugin copy under `plugins/<name>/skills/` stays byte-identical.

## Directory Layout

Mirror the existing plugin. Example for a hypothetical `session-log-helper`:

```
skills/
  agent-routing-orchestrator/
    SKILL.md
  session-log-helper/
    SKILL.md                          # source of truth

plugins/
  agent-routing-orchestrator/
    .claude-plugin/plugin.json
    skills/agent-routing-orchestrator/SKILL.md
  session-log-helper/
    .claude-plugin/plugin.json        # name must match folder
    skills/session-log-helper/SKILL.md  # copy of standalone skill

.claude-plugin/
  marketplace.json                    # one entry per plugin
```

Do not add runtime directories under any plugin (`agents/`, `commands/`, `hooks/`, `prompts/`, `schemas/`, `scripts/`).

## marketplace.json Changes

Add a second object to the `plugins` array (order is display order):

```json
{
  "name": "session-log-helper",
  "source": "./plugins/session-log-helper",
  "description": "…",
  "version": "0.5.0",
  "category": "development",
  "homepage": "https://github.com/ramsaijanapana/shared-agent-skills",
  "tags": ["skill", "session-log"]
}
```

Rules: `source` is `./plugins/<plugin-name>`; marketplace top-level `name` stays `shared-agent-skills`; each entry `version` must match that plugin's `plugin.json`, skill `metadata.shared-agent-skills.version`, and `openpackage.yml`.

Create `plugins/<name>/.claude-plugin/plugin.json` from the existing manifest shape.

## Validator Changes (Required Before Adding Plugin #2)

Update tooling **first**, then add files. Keep strict validation — generalize it.

### `scripts/validate.py`

| Today (single-plugin) | Multi-plugin replacement |
|-----------------------|----------------------------|
| `EXPECTED_PLUGIN_NAME` constant | `PLUGIN_REGISTRY: dict[str, PluginSpec]` — name → `{source, required_sections?}` |
| `plugin_dir = root / "plugins" / "agent-routing-orchestrator"` | Loop `for name, spec in PLUGIN_REGISTRY.items()` |
| Skill copy check for one pair | For each registry entry: `skills/<name>/SKILL.md` ↔ `plugins/<name>/skills/<name>/SKILL.md` |
| `len(plugins) != 1` | `len(plugins) == len(PLUGIN_REGISTRY)` and every entry matches registry (name, source, version) |
| `plugins[0]` marketplace checks | Find marketplace entry by `name`; reject duplicates or orphans |
| Version dict uses one skill | All registered skills' versions + each marketplace entry + each `plugin.json` + `openpackage.yml` must be equal |
| Section checks gated on `EXPECTED_PLUGIN_NAME` | Per-plugin `required_sections` in registry (or empty tuple) |

Do **not** remove the strict gate — change `exactly one` to `exactly N registered plugins`.

### `scripts/check_plugin_sync.py`

Replace `EXPECTED_PLUGIN_NAME` and `plugins[0]` checks with the same registry loop: verify each standalone skill matches its plugin mirror and that marketplace `source` paths align.

### `scripts/sync_version.py`

| Function | Change |
|----------|--------|
| `write_skill_version` | Loop all registry skill paths |
| `write_marketplace_version` | Update `version` on **each** matching `plugins[]` entry by name |
| `write_plugin_json_version` | Loop all `plugins/<name>/.claude-plugin/plugin.json` |
| `sync_plugin_skill_copy` | Copy each registered skill |
| `collect_versions` | Collect openpackage + every skill/marketplace/plugin.json version; fail if any differ |

### Other touch points

`tests/conftest.py` (multi-plugin fixture), `install.sh` / `install.ps1` (`SKILLS` list), CONTRIBUTING version-bump table, and user docs if install/discovery changes.

## Recommended Workflow

1. Define `PLUGIN_REGISTRY` in `validate.py` (export for reuse from sync/check scripts).
2. Generalize `check_plugin_sync.py` and `sync_version.py` to import the registry.
3. Extend tests; confirm current single-plugin tree still passes.
4. Scaffold `skills/<new>/`, `plugins/<new>/`, and `plugin.json` (do **not** edit marketplace yet).
5. Run `python scripts/sync_version.py` to copy skill and align versions.
6. Add marketplace entry; run full validation gate.
7. Update CHANGELOG and user-facing docs.

## Testing Checklist

- [ ] `pytest tests/ -q`; `python scripts/validate.py`; `check_plugin_sync.py`; `sync_version.py --check`
- [ ] `sync_version.py X.Y.Z` updates every skill, marketplace entry, and plugin.json
- [ ] `ruff check scripts tests` and format check; CI green on PR
- [ ] Manual Claude Code install confirms the new skill loads

Package semver is shared across all plugins via `openpackage.yml` today; per-plugin versioning needs an explicit policy change first.
