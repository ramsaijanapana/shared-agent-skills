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
FORBIDDEN_TEXT_PATTERNS = tuple(
    "".join(parts)
    for parts in (
        ("codex-", "plugin-cc"),
        ("skill-", "codex"),
        ("skills-", "directory"),
        ("github.com/", "openai"),
        ("github.com/", "skills-", "directory"),
        ("DESIGN-", "INSPIRATION"),
        ("reference", " plugins"),
    )
)
EXPECTED_MARKETPLACE_NAME = "shared-agent-skills"
EXPECTED_PLUGIN_NAME = "agent-routing-orchestrator"
VERSION_RE = re.compile(r'^\s*version:\s*"?([^"\n]+)"?\s*$')


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter fence")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing frontmatter fence")
    fields: dict[str, str] = {}
    parent = ""
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if line.startswith(" "):
            if parent == "metadata" and ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip('"')
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parent = key.strip()
        fields[parent] = value.strip().strip('"')
    return fields


def read_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: expected top-level JSON object")
        return {}
    return value


def read_openpackage_version(errors: list[str]) -> str:
    path = ROOT / "openpackage.yml"
    if not path.is_file():
        errors.append("missing openpackage.yml")
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        match = VERSION_RE.match(line)
        if match:
            return match.group(1)
    errors.append("openpackage.yml: missing version")
    return ""


def main() -> int:
    errors: list[str] = []
    skill_versions: dict[str, str] = {}
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
        version = fields.get("shared-agent-skills.version", "")
        if not version:
            errors.append(f"{skill_dir.name}: missing shared-agent-skills.version")
        else:
            skill_versions[name] = version

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

    marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json", errors)
    plugin_json = read_json(PLUGIN_DIR / ".claude-plugin" / "plugin.json", errors)
    package_version = read_openpackage_version(errors)
    skill_version = skill_versions.get(EXPECTED_PLUGIN_NAME, "")

    if marketplace.get("name") != EXPECTED_MARKETPLACE_NAME:
        errors.append(".claude-plugin/marketplace.json: unexpected marketplace name")
    plugins = marketplace.get("plugins", [])
    if not isinstance(plugins, list) or len(plugins) != 1:
        errors.append(".claude-plugin/marketplace.json: expected exactly one plugin")
        plugin_entry = {}
    else:
        plugin_entry = plugins[0] if isinstance(plugins[0], dict) else {}
    if plugin_entry.get("name") != EXPECTED_PLUGIN_NAME:
        errors.append(".claude-plugin/marketplace.json: plugin name mismatch")
    if plugin_entry.get("source") != "./plugins/agent-routing-orchestrator":
        errors.append(".claude-plugin/marketplace.json: plugin source mismatch")
    if plugin_json.get("name") != EXPECTED_PLUGIN_NAME:
        errors.append("plugins/agent-routing-orchestrator/.claude-plugin/plugin.json: name mismatch")

    versions = {
        "skill": skill_version,
        "marketplace": str(plugin_entry.get("version", "")),
        "plugin": str(plugin_json.get("version", "")),
        "openpackage": package_version,
    }
    if len(set(versions.values())) != 1 or not skill_version:
        rendered = ", ".join(f"{key}={value or '<missing>'}" for key, value in versions.items())
        errors.append(f"version mismatch: {rendered}")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if pattern in text:
                errors.append(f"{path.relative_to(ROOT)}: forbidden text pattern {pattern!r}")

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
