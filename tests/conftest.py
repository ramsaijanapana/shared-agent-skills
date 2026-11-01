from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def repo_root() -> Path:
    return ROOT


@pytest.fixture
def minimal_package(tmp_path: Path) -> Path:
    skill_name = "agent-routing-orchestrator"
    skill_dir = tmp_path / "skills" / skill_name
    plugin_dir = tmp_path / "plugins" / skill_name
    plugin_skill_dir = plugin_dir / "skills" / skill_name
    skill_dir.mkdir(parents=True)
    plugin_skill_dir.mkdir(parents=True)

    skill_md = f"""---
name: {skill_name}
description: Test skill for validation.
license: MIT
metadata:
  shared-agent-skills.version: "1.0.0"
---

# Test Skill

## Start With A Routing Contract

Test routing contract section.

## Session Log

Test session log section.

## Context Packet

Test context packet section.

## Completion Packet

Test completion packet section.

## Stop Rules

Test stop rules section.

## Final Integration

Test final integration section.
"""
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (plugin_skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    (tmp_path / "openpackage.yml").write_text(
        "name: shared-agent-skills\nversion: 1.0.0\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("# test\n", encoding="utf-8")
    (tmp_path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (tmp_path / "install.sh").write_text("#!/bin/sh\n", encoding="utf-8")
    (tmp_path / "install.ps1").write_text("# test\n", encoding="utf-8")

    marketplace_dir = tmp_path / ".claude-plugin"
    marketplace_dir.mkdir()
    (marketplace_dir / "marketplace.json").write_text(
        """{
  "name": "shared-agent-skills",
  "plugins": [
    {
      "name": "agent-routing-orchestrator",
      "source": "./plugins/agent-routing-orchestrator",
      "version": "1.0.0"
    }
  ]
}
""",
        encoding="utf-8",
    )

    plugin_meta_dir = plugin_dir / ".claude-plugin"
    plugin_meta_dir.mkdir()
    (plugin_meta_dir / "plugin.json").write_text(
        """{
  "name": "agent-routing-orchestrator",
  "version": "1.0.0"
}
""",
        encoding="utf-8",
    )
    return tmp_path
