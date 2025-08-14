import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import List, Tuple, TypedDict, Union


class ValidationResult(TypedDict):
    valid_hashes: List[str]
    errors: List[Tuple[int, str]]
    missing_commits: List[str]
    strict_comment_errors: List[Tuple[int, str]]


def validate_git_blame_ignore_revs(
    file_path: Union[str, Path], call_git: bool = False, strict_comments: bool = False
) -> ValidationResult:
    """
    Validates the contents of a `.git-blame-ignore-revs` file.

    Args:
        file_path (Union[str, Path]): Path to the `.git-blame-ignore-revs` file.
        call_git (bool): If True, ensures each commit is in the history of the checked-out branch.
        strict_comments (bool): If True, requires each commit line to have one or more comment lines above it.

    Returns:
        ValidationResult: A dictionary containing valid hashes, errors, missing commits, and strict comment errors.
    """
    # Convert Path object to string if necessary
    file_path = str(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    valid_hashes: List[str] = []
    errors: List[Tuple[int, str]] = []
    missing_commits: List[str] = []
    strict_comment_errors: List[Tuple[int, str]] = []

    # Regular expression for a valid Git commit hash (40 hexadecimal characters)
    commit_hash_regex = re.compile(r"^[0-9a-f]{40}$")

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Track whether the previous lines were comments
    has_comment_above = False

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        # Skip blank lines
        if not line:
            continue

        # Check for comments
        if line.startswith("#"):
            has_comment_above = True
            continue

        # Validate the commit hash
        if commit_hash_regex.match(line):
            valid_hashes.append(line)

            # Check strict comments requirement
            if strict_comments and not has_comment_above:
                strict_comment_errors.append((line_number, line))

            # Reset comment tracking after a commit line
            has_comment_above = False
        else:
            errors.append((line_number, line))

    if call_git:
        # Check if each valid hash exists in the Git history
        for commit_hash in valid_hashes:
            try:
                subprocess.run(
                    ["git", "cat-file", "-e", commit_hash],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                missing_commits.append(commit_hash)

    return ValidationResult(
        valid_hashes=valid_hashes,
        errors=errors,
        missing_commits=missing_commits,
        strict_comment_errors=strict_comment_errors,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a .git-blame-ignore-revs file."
    )
    parser.add_argument(
        "file_path",
        type=Path,  # Use Path as the type conversion function
        help="Path to the .git-blame-ignore-revs file.",
    )
    parser.add_argument(
        "--call-git",
        action="store_true",
        help="Ensure each commit is in the history of the checked-out branch.",
    )
    parser.add_argument(
        "--strict-comments",
        action="store_true",
        help="Require each commit line to have one or more comment lines above it.",
    )

    args = parser.parse_args()

    try:
        result = validate_git_blame_ignore_revs(
            args.file_path, args.call_git, args.strict_comments
        )

        print("Validation Results:")
        print(f"Valid hashes ({len(result['valid_hashes'])}):")
        for hash in result["valid_hashes"]:
            print(f"  {hash}")

        if result["errors"]:
            print(f"\nErrors ({len(result['errors'])}):")
            for line_number, line in result["errors"]:
                print(f"  Line {line_number}: {line}")
        else:
            print("\nNo errors found!")

        if args.call_git:
            if result["missing_commits"]:
                print(f"\nMissing commits ({len(result['missing_commits'])}):")
                for commit in result["missing_commits"]:
                    print(f"  {commit}")
            else:
                print("\nAll commits are present in the Git history!")

        if args.strict_comments:
            if result["strict_comment_errors"]:
                print(
                    f"\nStrict comment errors ({len(result['strict_comment_errors'])}):"
                )
                for line_number, line in result["strict_comment_errors"]:
                    print(f"  Line {line_number}: {line}")
            else:
                print("\nAll commit lines have comments above them!")
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
