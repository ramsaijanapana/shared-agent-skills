#!/usr/bin/env python3
"""Sync package version across all version sources and refresh the plugin skill copy."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from validate import (
    DEFAULT_ROOT,
    EXPECTED_PLUGIN_NAME,
    SKILL_VERSION_RE,
    VERSION_RE,
    validate_package,
)


def read_openpackage_version(root: Path) -> str:
    path = root / "openpackage.yml"
    for line in path.read_text(encoding="utf-8").splitlines():
        match = VERSION_RE.match(line)
        if match:
            return match.group(1)
    raise ValueError("openpackage.yml: missing version")


def write_openpackage_version(root: Path, version: str) -> None:
    path = root / "openpackage.yml"
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    updated = False
    new_lines: list[str] = []
    for line in lines:
        stripped = line.rstrip("\r\n")
        if VERSION_RE.match(stripped):
            newline = line[len(stripped) :]
            new_lines.append(f"version: {version}{newline}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        raise ValueError("openpackage.yml: could not update version")
    path.write_text("".join(new_lines), encoding="utf-8")


def write_skill_version(root: Path, version: str) -> None:
    path = root / "skills" / EXPECTED_PLUGIN_NAME / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    updated, count = SKILL_VERSION_RE.subn(rf'\1"{version}"', text, count=1)
    if count != 1:
        raise ValueError(f"{path}: could not update shared-agent-skills.version")
    path.write_text(updated, encoding="utf-8")


def write_marketplace_version(root: Path, version: str) -> None:
    path = root / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    plugins = data.get("plugins", [])
    if not plugins or not isinstance(plugins[0], dict):
        raise ValueError("marketplace.json: missing plugin entry")
    plugins[0]["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_plugin_json_version(root: Path, version: str) -> None:
    path = root / "plugins" / EXPECTED_PLUGIN_NAME / ".claude-plugin" / "plugin.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def sync_plugin_skill_copy(root: Path) -> None:
    source = root / "skills" / EXPECTED_PLUGIN_NAME / "SKILL.md"
    dest = root / "plugins" / EXPECTED_PLUGIN_NAME / "skills" / EXPECTED_PLUGIN_NAME / "SKILL.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)


def collect_versions(root: Path) -> dict[str, str]:
    skill_path = root / "skills" / EXPECTED_PLUGIN_NAME / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    skill_match = SKILL_VERSION_RE.search(skill_text)
    marketplace = json.loads(
        (root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    plugin_json = json.loads(
        (root / "plugins" / EXPECTED_PLUGIN_NAME / ".claude-plugin" / "plugin.json").read_text(
            encoding="utf-8"
        )
    )
    return {
        "openpackage": read_openpackage_version(root),
        "skill": skill_match.group(2) if skill_match else "",
        "marketplace": str(marketplace["plugins"][0].get("version", "")),
        "plugin": str(plugin_json.get("version", "")),
    }


def sync_version(root: Path, version: str) -> None:
    write_openpackage_version(root, version)
    write_skill_version(root, version)
    write_marketplace_version(root, version)
    write_plugin_json_version(root, version)
    sync_plugin_skill_copy(root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sync version across openpackage.yml, skill frontmatter, marketplace, and plugin.json."
    )
    parser.add_argument(
        "version",
        nargs="?",
        help="Semver to write everywhere. Defaults to openpackage.yml when omitted.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Package root (defaults to repository root).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero when version sources differ; do not modify files.",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.check:
        versions = collect_versions(root)
        unique = set(versions.values())
        if len(unique) != 1 or not versions["openpackage"]:
            rendered = ", ".join(f"{key}={value or '<missing>'}" for key, value in versions.items())
            print(f"Version mismatch: {rendered}")
            return 1
        print(f"Versions in sync at {versions['openpackage']}.")
        return 0

    version = args.version or read_openpackage_version(root)
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        print(f"Invalid semver: {version!r} (expected MAJOR.MINOR.PATCH)", file=sys.stderr)
        return 2

    sync_version(root, version)
    errors = validate_package(root)
    if errors:
        print("Version sync completed but validation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print(f"Synced version {version} across all sources and refreshed plugin skill copy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
