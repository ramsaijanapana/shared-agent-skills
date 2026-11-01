from pathlib import Path

from check_version_badge import check_version_badge, main


def test_check_version_badge_passes_real_repo(repo_root: Path) -> None:
    assert check_version_badge(repo_root) == []


def test_check_version_badge_detects_mismatch(minimal_package: Path) -> None:
    readme = minimal_package / "README.md"
    readme.write_text(
        "[![Version](https://img.shields.io/badge/version-9.9.9-blue.svg)](openpackage.yml)\n",
        encoding="utf-8",
    )
    errors = check_version_badge(minimal_package)
    assert any("does not match" in err for err in errors)


def test_main_returns_zero_when_badge_matches(minimal_package: Path) -> None:
    readme = minimal_package / "README.md"
    readme.write_text(
        "[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](openpackage.yml)\n",
        encoding="utf-8",
    )
    assert main(["--root", str(minimal_package)]) == 0


def test_main_returns_one_when_badge_missing(minimal_package: Path) -> None:
    assert main(["--root", str(minimal_package)]) == 1
