#!/usr/bin/env python3
"""Verify standalone skill and plugin skill copies stay in sync."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGIN_NAME = "agent-routing-orchestrator"
SOURCE_SKILL = Path("skills") / EXPECTED_PLUGIN_NAME / "SKILL.md"
PLUGIN_SKILL = Path("plugins") / EXPECTED_PLUGIN_NAME / "skills" / EXPECTED_PLUGIN_NAME / "SKILL.md"


def check_plugin_sync(root: Path) -> list[str]:
    errors: list[str] = []
    source = root / SOURCE_SKILL
    plugin_copy = root / PLUGIN_SKILL

    if not source.is_file():
        errors.append(f"missing source skill: {SOURCE_SKILL}")
        return errors

    if not plugin_copy.is_file():
        errors.append(f"missing plugin skill copy: {PLUGIN_SKILL}")
        return errors

    source_text = source.read_text(encoding="utf-8")
    plugin_text = plugin_copy.read_text(encoding="utf-8")
    if source_text != plugin_text:
        diff = difflib.unified_diff(
            plugin_text.splitlines(keepends=True),
            source_text.splitlines(keepends=True),
            fromfile=str(PLUGIN_SKILL),
            tofile=str(SOURCE_SKILL),
        )
        preview = "".join(list(diff)[:40])
        errors.append(
            "plugin skill copy differs from standalone source; "
            f"run `cp {SOURCE_SKILL} {PLUGIN_SKILL}` or sync manually.\n{preview}"
        )

    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    plugin_json_path = root / "plugins" / EXPECTED_PLUGIN_NAME / ".claude-plugin" / "plugin.json"
    for path in (marketplace_path, plugin_json_path):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(root)}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(root)}: invalid JSON: {exc}")
            continue
        if path == marketplace_path:
            plugins = payload.get("plugins", [])
            if not isinstance(plugins, list) or not plugins:
                errors.append("marketplace.json: expected at least one plugin entry")
                continue
            entry = plugins[0]
            if entry.get("source") != f"./plugins/{EXPECTED_PLUGIN_NAME}":
                errors.append("marketplace.json: plugin source path mismatch")
        else:
            if payload.get("name") != EXPECTED_PLUGIN_NAME:
                errors.append("plugin.json: name mismatch")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check plugin skill sync for shared-agent-skills.")
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Package root to inspect (defaults to repository root).",
    )
    args = parser.parse_args(argv)
    errors = check_plugin_sync(args.root.resolve())

    if errors:
        print("Plugin sync check failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Plugin sync check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
