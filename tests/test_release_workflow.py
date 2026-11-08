"""The release tag check must import sync_version the way GitHub Actions runs it.

pytest adds scripts/ via pythonpath. The release job does not, so a bare
`from sync_version import ...` at the repo root raises ModuleNotFoundError
and the tag push never publishes a GitHub Release.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


def test_release_tag_check_imports_from_repo_root(repo_root: Path) -> None:
    workflow = (repo_root / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    match = re.search(r"PKG_VERSION=\$\((.+)\)", workflow)
    assert match, "release workflow must capture the package version in a shell substitution"
    shell_cmd = match.group(1).replace("python ", f"{sys.executable} ", 1)

    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    result = subprocess.run(
        ["bash", "-c", shell_cmd],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "0.5.0"
