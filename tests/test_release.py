"""Tests for version detection in the PyPI publishing workflow."""

from pathlib import Path
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_version.py"


def git(repository: Path, *args: str) -> str:
    """Run Git in an isolated test repository."""
    return subprocess.check_output(["git", "-C", str(repository), *args], text=True).strip()


def commit(repository: Path) -> str:
    """Commit fixture metadata without changing the user's Git configuration."""
    git(repository, "add", "pyproject.toml")
    git(repository, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "Test metadata")
    return git(repository, "rev-parse", "HEAD")


def write_project(repository: Path, version: str, description: str = "Initial") -> None:
    """Write package metadata for a test commit."""
    (repository / "pyproject.toml").write_text(
        f'[project]\nname = "release-test"\nversion = "{version}"\ndescription = "{description}"\n'
    )


@pytest.fixture
def repository(tmp_path):
    """Create a Git repository with an initial package version."""
    git(tmp_path, "init")
    write_project(tmp_path, "1.2.0")
    commit(tmp_path)
    return tmp_path


def check_version(repository: Path, before: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Run the CLI exactly as the workflow does."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--before", before, "--after", "HEAD", *args],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("version, changed", [("1.2.0", "false"), ("1.2.1", "true")])
def test_detects_version_changes_and_ignores_other_metadata(repository, version, changed):
    """Editing other metadata must not trigger publishing."""
    before = git(repository, "rev-parse", "HEAD")
    write_project(repository, version, description="Changed")
    commit(repository)

    result = check_version(repository, before)

    assert result.returncode == 0, result.stderr
    assert result.stdout == f"changed={changed}\nversion={version}\n"


@pytest.mark.parametrize("final_version, changed", [("1.2.1", "true"), ("1.2.0", "false")])
def test_compares_the_complete_multi_commit_push(repository, final_version, changed):
    """The last commit alone must not determine whether the version changed."""
    before = git(repository, "rev-parse", "HEAD")
    write_project(repository, "1.2.1")
    commit(repository)
    write_project(repository, final_version, description="Final commit")
    commit(repository)

    result = check_version(repository, before)

    assert result.returncode == 0, result.stderr
    assert result.stdout == f"changed={changed}\nversion={final_version}\n"


def test_new_main_branch_publishes_its_initial_version(repository):
    """A branch creation event has no previous version."""
    result = check_version(repository, "0" * 40)

    assert result.returncode == 0, result.stderr
    assert result.stdout == "changed=true\nversion=1.2.0\n"


def test_appends_github_actions_outputs(repository, tmp_path):
    """The job condition must receive the comparison result through GITHUB_OUTPUT."""
    output = tmp_path / "output"
    output.write_text("existing=value\n")
    result = check_version(repository, "0" * 40, "--output", str(output))

    assert result.returncode == 0, result.stderr
    assert output.read_text() == "existing=value\nchanged=true\nversion=1.2.0\n"


@pytest.mark.parametrize("version_field", ["", "version = 12\n"])
def test_invalid_version_metadata_fails(repository, version_field):
    """Missing or non-string versions must fail the version job."""
    before = git(repository, "rev-parse", "HEAD")
    (repository / "pyproject.toml").write_text(f'[project]\nname = "release-test"\n{version_field}')
    commit(repository)

    result = check_version(repository, before)

    assert result.returncode != 0
    assert "must define [project].version as a non-empty string" in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize("version, changed", [("1.2.0", "false"), ("1.2.1", "true")])
def test_compares_against_the_previous_poetry_metadata(repository, version, changed):
    """The first push after the uv migration must compare the existing main version."""
    (repository / "pyproject.toml").write_text('[tool.poetry]\nversion = "1.2.0"\n')
    before = commit(repository)
    write_project(repository, version)
    commit(repository)

    result = check_version(repository, before)

    assert result.returncode == 0, result.stderr
    assert result.stdout == f"changed={changed}\nversion={version}\n"
