#!/usr/bin/env python3
"""Validate shared-agent-skills package structure."""
from __future__ import annotations

import re
import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PLUGIN_DIR = ROOT / "plugins" / "agent-routing-orchestrator"
PLUGIN_SKILLS_DIR = PLUGIN_DIR / "skills"
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
FORBIDDEN_PLUGIN_DIRS = (
    "agents",
    "commands",
    "hooks",
    "prompts",
    "schemas",
    "scripts",
)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter fence")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing frontmatter fence")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def main() -> int:
    errors: list[str] = []
    if not SKILLS_DIR.is_dir():
        errors.append("missing skills/ directory")
        print("\n".join(errors))
        return 1

    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue
        try:
            fields = parse_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"{skill_dir.name}: {exc}")
            continue

        name = fields.get("name", "")
        desc = fields.get("description", "")
        if name != skill_dir.name:
            errors.append(f"{skill_dir.name}: frontmatter name {name!r} must match folder")
        if not NAME_RE.fullmatch(name):
            errors.append(
                f"{skill_dir.name}: name must be lowercase letters/numbers/hyphens, "
                "1-64 chars, and must not start or end with a hyphen"
            )
        if "--" in name:
            errors.append(f"{skill_dir.name}: name must not contain consecutive hyphens")
        if not desc:
            errors.append(f"{skill_dir.name}: description is required")
        if len(desc) > 1024:
            errors.append(f"{skill_dir.name}: description exceeds 1024 chars")

        body_lines = skill_md.read_text(encoding="utf-8").splitlines()
        if len(body_lines) > 500:
            errors.append(f"{skill_dir.name}: SKILL.md exceeds 500 lines")

    source_skill = SKILLS_DIR / "agent-routing-orchestrator" / "SKILL.md"
    plugin_skill = PLUGIN_SKILLS_DIR / "agent-routing-orchestrator" / "SKILL.md"
    if not plugin_skill.is_file():
        errors.append("plugin: missing agent-routing-orchestrator skill copy")
    elif source_skill.is_file() and plugin_skill.read_text(encoding="utf-8") != source_skill.read_text(encoding="utf-8"):
        errors.append("plugin: skill copy differs from skills/agent-routing-orchestrator/SKILL.md")

    for dirname in FORBIDDEN_PLUGIN_DIRS:
        if (PLUGIN_DIR / dirname).exists():
            errors.append(
                f"plugin: unexpected {dirname}/ directory; this package should enhance the current skill, "
                "not vendor command/runtime assets from another package"
            )

    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    plugin_json_path = PLUGIN_DIR / ".claude-plugin" / "plugin.json"
    for json_path in (marketplace_path, plugin_json_path):
        if not json_path.is_file():
            errors.append(f"missing {json_path.relative_to(ROOT)}")
            continue
        try:
            json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{json_path.relative_to(ROOT)}: invalid JSON: {exc}")

    for required in ("README.md", "LICENSE", "install.ps1", "install.sh", "openpackage.yml"):
        if not (ROOT / required).is_file():
            errors.append(f"missing {required}")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
