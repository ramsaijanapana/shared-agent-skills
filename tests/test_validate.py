from pathlib import Path

import pytest

from validate import NAME_RE, main, parse_frontmatter, validate_package


def test_parse_frontmatter_reads_metadata_version(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        """---
name: demo-skill
description: Demo
metadata:
  shared-agent-skills.version: "0.1.0"
---

# Demo
""",
        encoding="utf-8",
    )
    fields = parse_frontmatter(skill)
    assert fields["name"] == "demo-skill"
    assert fields["shared-agent-skills.version"] == "0.1.0"


def test_parse_frontmatter_requires_opening_fence(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text("# no frontmatter\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing opening frontmatter fence"):
        parse_frontmatter(skill)


def test_parse_frontmatter_requires_closing_fence(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text("---\nname: demo-skill\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing closing frontmatter fence"):
        parse_frontmatter(skill)


@pytest.mark.parametrize(
    "name,valid",
    [
        ("agent-routing-orchestrator", True),
        ("a", True),
        (
            "bad--name",
            True,
        ),  # NAME_RE allows; validate_package rejects consecutive hyphens separately
        ("-bad", False),
        ("UPPER", False),
    ],
)
def test_name_regex(name: str, valid: bool) -> None:
    assert bool(NAME_RE.fullmatch(name)) is valid


def test_validate_package_passes_minimal_fixture(minimal_package: Path) -> None:
    assert validate_package(minimal_package) == []


def test_validate_package_detects_missing_skill_md(minimal_package: Path) -> None:
    (minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md").unlink()
    errors = validate_package(minimal_package)
    assert any("missing SKILL.md" in err for err in errors)


def test_validate_package_detects_plugin_drift(minimal_package: Path) -> None:
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
    errors = validate_package(minimal_package)
    assert any("skill copy differs" in err for err in errors)


def test_validate_package_detects_version_mismatch(minimal_package: Path) -> None:
    openpackage = minimal_package / "openpackage.yml"
    openpackage.write_text(
        openpackage.read_text(encoding="utf-8").replace("1.0.0", "9.9.9"),
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("version mismatch" in err for err in errors)


def test_validate_package_detects_invalid_skill_name(minimal_package: Path) -> None:
    bad_dir = minimal_package / "skills" / "Bad-Name"
    bad_dir.mkdir()
    (bad_dir / "SKILL.md").write_text(
        """---
name: Bad-Name
description: invalid
metadata:
  shared-agent-skills.version: "1.0.0"
---
""",
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("must match folder" in err or "lowercase" in err for err in errors)


def test_validate_package_requires_core_files(minimal_package: Path) -> None:
    (minimal_package / "README.md").unlink()
    errors = validate_package(minimal_package)
    assert any("missing README.md" in err for err in errors)


def test_real_repo_passes_validation(repo_root: Path) -> None:
    assert validate_package(repo_root) == []


def test_validate_package_detects_missing_skills_directory(tmp_path: Path) -> None:
    errors = validate_package(tmp_path)
    assert errors == ["missing skills/ directory"]


def test_validate_package_detects_consecutive_hyphens(minimal_package: Path) -> None:
    bad_dir = minimal_package / "skills" / "bad--name"
    bad_dir.mkdir()
    (bad_dir / "SKILL.md").write_text(
        """---
name: bad--name
description: invalid
metadata:
  shared-agent-skills.version: "1.0.0"
---
""",
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("consecutive hyphens" in err for err in errors)


def test_validate_package_detects_missing_description(minimal_package: Path) -> None:
    skill = minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    skill.write_text(
        """---
name: agent-routing-orchestrator
metadata:
  shared-agent-skills.version: "1.0.0"
---
""",
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("description is required" in err for err in errors)


def test_validate_package_detects_description_length_limit(minimal_package: Path) -> None:
    skill = minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    skill.write_text(
        f"""---
name: agent-routing-orchestrator
description: {"x" * 1025}
metadata:
  shared-agent-skills.version: "1.0.0"
---
""",
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("description exceeds 1024 chars" in err for err in errors)


def test_validate_package_detects_missing_shared_version(minimal_package: Path) -> None:
    skill = minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    skill.write_text(
        """---
name: agent-routing-orchestrator
description: ok
---
""",
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("missing shared-agent-skills.version" in err for err in errors)


def test_validate_package_detects_missing_skill_section(minimal_package: Path) -> None:
    skill = minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    plugin_skill = (
        minimal_package
        / "plugins"
        / "agent-routing-orchestrator"
        / "skills"
        / "agent-routing-orchestrator"
        / "SKILL.md"
    )
    updated = skill.read_text(encoding="utf-8").replace("## Session Log\n", "")
    skill.write_text(updated, encoding="utf-8")
    plugin_skill.write_text(updated, encoding="utf-8")
    errors = validate_package(minimal_package)
    assert any("missing required section 'Session Log'" in err for err in errors)


def test_validate_package_detects_skill_line_limit(minimal_package: Path) -> None:
    skill = minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    skill.write_text(
        skill.read_text(encoding="utf-8") + "\n".join(["line"] * 501), encoding="utf-8"
    )
    errors = validate_package(minimal_package)
    assert any("exceeds 500 lines" in err for err in errors)


def test_validate_package_detects_forbidden_plugin_directory(minimal_package: Path) -> None:
    (minimal_package / "plugins" / "agent-routing-orchestrator" / "scripts").mkdir()
    errors = validate_package(minimal_package)
    assert any("unexpected scripts/" in err for err in errors)


def test_validate_package_detects_invalid_marketplace_json(minimal_package: Path) -> None:
    (minimal_package / ".claude-plugin" / "marketplace.json").write_text(
        "{bad json", encoding="utf-8"
    )
    errors = validate_package(minimal_package)
    assert any("invalid JSON" in err for err in errors)


def test_validate_package_detects_name_folder_mismatch(minimal_package: Path) -> None:
    skill = minimal_package / "skills" / "agent-routing-orchestrator" / "SKILL.md"
    skill.write_text(
        skill.read_text(encoding="utf-8").replace(
            "name: agent-routing-orchestrator",
            "name: other-skill",
        ),
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("must match folder" in err for err in errors)


def test_validate_package_detects_marketplace_name_mismatch(minimal_package: Path) -> None:
    marketplace = minimal_package / ".claude-plugin" / "marketplace.json"
    marketplace.write_text(
        marketplace.read_text(encoding="utf-8").replace(
            '"name": "shared-agent-skills"',
            '"name": "wrong-marketplace"',
        ),
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("unexpected marketplace name" in err for err in errors)


def test_validate_package_detects_plugin_json_name_mismatch(minimal_package: Path) -> None:
    plugin_json = (
        minimal_package
        / "plugins"
        / "agent-routing-orchestrator"
        / ".claude-plugin"
        / "plugin.json"
    )
    plugin_json.write_text(
        plugin_json.read_text(encoding="utf-8").replace(
            '"name": "agent-routing-orchestrator"',
            '"name": "wrong-plugin"',
        ),
        encoding="utf-8",
    )
    errors = validate_package(minimal_package)
    assert any("name mismatch" in err for err in errors)


def test_validate_package_detects_missing_openpackage(minimal_package: Path) -> None:
    (minimal_package / "openpackage.yml").unlink()
    errors = validate_package(minimal_package)
    assert any("missing openpackage.yml" in err for err in errors)


def test_validate_package_detects_forbidden_text_pattern(minimal_package: Path) -> None:
    readme = minimal_package / "README.md"
    forbidden = "codex-" + "plugin-cc"
    readme.write_text(readme.read_text(encoding="utf-8") + f"\n{forbidden}\n", encoding="utf-8")
    errors = validate_package(minimal_package)
    assert any("forbidden text pattern" in err for err in errors)


def test_validate_package_detects_missing_plugin_skill_copy(minimal_package: Path) -> None:
    plugin_skill = (
        minimal_package
        / "plugins"
        / "agent-routing-orchestrator"
        / "skills"
        / "agent-routing-orchestrator"
        / "SKILL.md"
    )
    plugin_skill.unlink()
    errors = validate_package(minimal_package)
    assert any("missing agent-routing-orchestrator skill copy" in err for err in errors)


def test_main_returns_zero_on_valid_package(minimal_package: Path) -> None:
    assert main(["--root", str(minimal_package)]) == 0


def test_main_returns_one_on_invalid_package(minimal_package: Path) -> None:
    (minimal_package / "README.md").unlink()
    assert main(["--root", str(minimal_package)]) == 1
