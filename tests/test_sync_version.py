import json
from pathlib import Path

from sync_version import collect_versions, main, read_openpackage_version, sync_version


def test_read_openpackage_version(minimal_package: Path) -> None:
    assert read_openpackage_version(minimal_package) == "1.0.0"


def test_sync_version_updates_all_metadata(minimal_package: Path) -> None:
    sync_version(minimal_package, "2.0.0")
    versions = collect_versions(minimal_package)
    assert versions == {
        "openpackage": "2.0.0",
        "skill": "2.0.0",
        "marketplace": "2.0.0",
        "plugin": "2.0.0",
    }

    marketplace = json.loads(
        (minimal_package / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    plugin_json = json.loads(
        (
            minimal_package
            / "plugins"
            / "agent-routing-orchestrator"
            / ".claude-plugin"
            / "plugin.json"
        ).read_text(encoding="utf-8")
    )
    skill_text = (minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    plugin_text = (
        minimal_package
        / "plugins"
        / "agent-routing-orchestrator"
        / "skills"
        / "agent-routing-orchestrator"
        / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert marketplace["plugins"][0]["version"] == "2.0.0"
    assert plugin_json["version"] == "2.0.0"
    assert 'shared-agent-skills.version: "2.0.0"' in skill_text
    assert plugin_text == skill_text


def test_sync_version_refreshes_plugin_copy_after_skill_edit(minimal_package: Path) -> None:
    skill = minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\n# edited body\n", encoding="utf-8")
    sync_version(minimal_package, "1.0.0")
    plugin_skill = (
        minimal_package
        / "plugins"
        / "agent-routing-orchestrator"
        / "skills"
        / "agent-routing-orchestrator"
        / "SKILL.md"
    )
    assert plugin_skill.read_text(encoding="utf-8") == skill.read_text(encoding="utf-8")


def test_main_check_reports_mismatch(minimal_package: Path) -> None:
    openpackage = minimal_package / "openpackage.yml"
    openpackage.write_text(
        openpackage.read_text(encoding="utf-8").replace("1.0.0", "9.9.9"),
        encoding="utf-8",
    )
    assert main(["--check", "--root", str(minimal_package)]) == 1


def test_main_check_passes_when_in_sync(minimal_package: Path) -> None:
    assert main(["--check", "--root", str(minimal_package)]) == 0


def test_main_rejects_invalid_semver(minimal_package: Path) -> None:
    assert main(["not-a-version", "--root", str(minimal_package)]) == 2
