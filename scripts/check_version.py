"""Compare package versions across a GitHub push."""

import argparse
from pathlib import Path
import subprocess
import tomllib


class Arguments(argparse.Namespace):
    before: str
    after: str
    output: Path | None


def version_at(revision: str, *, allow_poetry: bool = False) -> str:
    """Read the package version from a committed pyproject.toml."""
    content = subprocess.check_output(["git", "show", f"{revision}:pyproject.toml"], text=True)
    metadata = tomllib.loads(content)
    version = metadata.get("project", {}).get("version")
    if allow_poetry and version is None:
        version = metadata.get("tool", {}).get("poetry", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{revision}:pyproject.toml must define [project].version as a non-empty string.")
    return version


def main() -> None:
    """Write a version comparison for GitHub Actions."""
    parser = argparse.ArgumentParser(
        description="Detect a change to [project].version across a push.",
        epilog="Run from the repository root after fetching both revisions.",
    )
    parser.add_argument("-b", "--before", required=True, help="Commit before the push; all-zero SHA for a new branch.")
    parser.add_argument("-a", "--after", default="HEAD", help="Commit after the push (default: HEAD).")
    parser.add_argument("-o", "--output", type=Path, help="Append changed and version to a GitHub Actions output file.")
    args = parser.parse_args(namespace=Arguments())

    current = version_at(args.after)
    previous = None if args.before == "0" * 40 else version_at(args.before, allow_poetry=True)
    outputs = f"changed={str(previous != current).lower()}\nversion={current}\n"
    print(outputs, end="")
    if args.output is not None:
        with args.output.open("a", encoding="utf-8") as stream:
            stream.write(outputs)


if __name__ == "__main__":
    main()
