#!/usr/bin/env python3
"""Verify README version badge matches openpackage.yml."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from validate import DEFAULT_ROOT, read_openpackage_version

BADGE_RE = re.compile(r"!\[Version\]\(https://img\.shields\.io/badge/version-([^-]+)-blue\.svg\)")


def check_version_badge(root: Path) -> list[str]:
    errors: list[str] = []
    version_errors: list[str] = []
    package_version = read_openpackage_version(root, version_errors)
    errors.extend(version_errors)
    if not package_version:
        return errors

    readme = root / "README.md"
    if not readme.is_file():
        errors.append("missing README.md")
        return errors

    match = BADGE_RE.search(readme.read_text(encoding="utf-8"))
    if not match:
        errors.append("README.md: missing shields.io version badge")
        return errors

    badge_version = match.group(1)
    if badge_version != package_version:
        errors.append(
            f"README version badge {badge_version!r} does not match "
            f"openpackage.yml version {package_version!r}"
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check README version badge sync.")
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Package root to inspect (defaults to repository root).",
    )
    args = parser.parse_args(argv)
    errors = check_version_badge(args.root.resolve())

    if errors:
        print("Version badge check failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Version badge check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
