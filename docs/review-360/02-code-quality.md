# Code Quality & Tooling — shared-agent-skills



**Dimension:** 2/5 · **Grade:** A++ (9.5/10)



## Strengths



- `scripts/validate.py` — cohesive validator: frontmatter, drift, versions, forbidden patterns, required skill sections.

- `scripts/sync_version.py` — atomic four-source version sync + plugin copy refresh.

- `scripts/check_plugin_sync.py` — focused drift check with unified diff preview.

- `scripts/check_version_badge.py` — README badge vs `openpackage.yml` sync.

- `ruff` + `ruff format` in `pyproject.toml`, pre-commit, and CI.

- Stdlib-only runtime deps for validation — no pip install required for end users.



## Gaps to A++



Optional only: typed installable package layout (`src/shared_agent_skills/`) and mypy — deferred; not required at current script size.



## Conventions enforced



- Skill names: `NAME_RE` — lowercase, 1–64 chars, no edge/consecutive hyphens

- Description ≤ 1024 chars; SKILL.md ≤ 500 lines

- Required H2 sections on orchestrator skill (routing contract, session log, packets, stop rules, final integration)

- Four version sources must match exactly

