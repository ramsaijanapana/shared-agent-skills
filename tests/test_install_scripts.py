import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _powershell_available() -> bool:
    return shutil.which("powershell") is not None or shutil.which("pwsh") is not None


def _bash_available() -> bool:
    return shutil.which("bash") is not None or shutil.which("sh") is not None


@pytest.mark.skipif(not _powershell_available(), reason="PowerShell not available")
def test_install_ps1_copies_skill_to_codex_home(tmp_path: Path) -> None:
    codex_home = tmp_path / "codex"
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "install.ps1"),
            "-Target",
            "codex",
            "-CodexHome",
            str(codex_home),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    installed = codex_home / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    source = ROOT / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    assert installed.is_file()
    assert installed.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")


@pytest.mark.skipif(not _powershell_available(), reason="PowerShell not available")
def test_install_ps1_removes_legacy_skills(tmp_path: Path) -> None:
    codex_home = tmp_path / "codex"
    legacy = codex_home / "skills" / "cost-aware-delegation"
    legacy.mkdir(parents=True)
    (legacy / "SKILL.md").write_text("legacy\n", encoding="utf-8")

    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "install.ps1"),
            "-Target",
            "codex",
            "-CodexHome",
            str(codex_home),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert not legacy.exists()


@pytest.mark.skipif(not _bash_available(), reason="bash/sh not available")
def test_install_sh_copies_skill_to_claude_home(tmp_path: Path) -> None:
    claude_home = tmp_path / "claude"
    shell = shutil.which("bash") or shutil.which("sh")
    assert shell is not None
    env = {"CLAUDE_HOME": str(claude_home)}
    result = subprocess.run(
        [shell, str(ROOT / "install.sh"), "claude"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, **env},
    )
    assert result.returncode == 0, result.stderr or result.stdout
    installed = claude_home / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    assert installed.is_file()


def test_install_sh_rejects_unknown_target() -> None:
    if not _bash_available():
        pytest.skip("bash/sh not available")
    shell = shutil.which("bash") or shutil.which("sh")
    assert shell is not None
    result = subprocess.run(
        [shell, str(ROOT / "install.sh"), "invalid-target"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
