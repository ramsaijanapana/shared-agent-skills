from pathlib import Path

from check_plugin_sync import check_plugin_sync, main


def test_check_plugin_sync_passes_real_repo(repo_root: Path) -> None:
    assert check_plugin_sync(repo_root) == []


def test_check_plugin_sync_detects_drift(minimal_package: Path) -> None:
    plugin_skill = (
        minimal_package
        / "plugins"
        / "agent-routing-orchestrator"
        / "skills"
        / "agent-routing-orchestrator"
        / "SKILL.md"
    )
    plugin_skill.write_text(
        plugin_skill.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8"
    )
    errors = check_plugin_sync(minimal_package)
    assert any("differs from standalone source" in err for err in errors)


def test_main_returns_zero_when_in_sync(minimal_package: Path) -> None:
    assert main(["--root", str(minimal_package)]) == 0


def test_main_returns_one_on_drift(minimal_package: Path) -> None:
    plugin_skill = (
        minimal_package
        / "plugins"
        / "agent-routing-orchestrator"
        / "skills"
        / "agent-routing-orchestrator"
        / "SKILL.md"
    )
    plugin_skill.write_text(
        plugin_skill.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8"
    )
    assert main(["--root", str(minimal_package)]) == 1
