import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, Tuple, TypedDict, Union


class ValidationResult(TypedDict):
    valid_hashes: Dict[int, str]
    errors: Dict[int, str]
    missing_commits: Dict[int, str]
    strict_comment_errors: Dict[int, str]
    comment_diffs: Dict[int, Tuple[str, str]]  # Line number -> (comment, commit message)
    missing_pre_commit_ci_commits: Dict[str, str]  # Commit hash -> Commit message


def validate_git_blame_ignore_revs(
    file_path: Union[str, Path],
    call_git: bool = False,
    strict_comments: bool = False,
    strict_comments_git: bool = False,
    pre_commit_ci: bool = False,
) -> ValidationResult:
    """
    Validates the contents of a `.git-blame-ignore-revs` file.

    Args:
        file_path (Union[str, Path]): Path to the `.git-blame-ignore-revs` file.
        call_git (bool): If True, ensures each commit is in the history of the checked-out branch.
        strict_comments (bool): If True, requires each commit line to have one or more comment lines above it.
        strict_comments_git (bool): If True, ensures the comment above each commit matches the first part of the commit message.
        pre_commit_ci (bool): If True, ensures all commits authored by `pre-commit-ci[bot]` are present in the file.

    Returns:
        ValidationResult: A dictionary containing valid hashes, errors, missing commits, strict comment errors, comment diffs, and missing pre-commit-ci commits.
    """
    # Convert Path object to string if necessary
    file_path = str(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    valid_hashes: Dict[int, str] = {}
    errors: Dict[int, str] = {}
    missing_commits: Dict[int, str] = {}
    strict_comment_errors: Dict[int, str] = {}
    comment_diffs: Dict[int, Tuple[str, str]] = {}
    missing_pre_commit_ci_commits: Dict[str, str] = {}

    # Regular expression for a valid Git commit hash (40 hexadecimal characters)
    commit_hash_regex = re.compile(r"^[0-9a-f]{40}$")

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Track whether the previous lines were comments
    has_comment_above = False
    last_comment = None

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        # Skip blank lines
        if not line:
            continue

        # Check for comments
        if line.startswith("#"):
            has_comment_above = True
            last_comment = line.lstrip("#").strip()
            continue

        # Validate the commit hash
        if commit_hash_regex.match(line):
            valid_hashes[line_number] = line

            # Check strict comments requirement
            if strict_comments and not has_comment_above:
                strict_comment_errors[line_number] = line

            # Reset comment tracking after a commit line
            has_comment_above = False
            last_comment = None
        else:
            errors[line_number] = line

    if call_git or strict_comments_git:
        # Fetch commit messages and verify existence using `git show`
        for line_number, commit_hash in valid_hashes.items():
            try:
                result = subprocess.run(
                    ["git", "show", "--quiet", "--pretty=format:%H %s", commit_hash],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                git_output = result.stdout.strip()
                if not git_output:
                    missing_commits[line_number] = commit_hash
                else:
                    commit_hash_from_git, commit_message = git_output.split(" ", 1)
                    if strict_comments_git:
                        last_comment = (
                            lines[line_number - 2].strip().lstrip("#").strip()
                            if line_number > 1
                            else ""
                        )
                        if not commit_message.startswith(last_comment):
                            comment_diffs[line_number] = (last_comment, commit_message)
            except subprocess.CalledProcessError:
                missing_commits[line_number] = commit_hash

    if pre_commit_ci:
        # Fetch all commits authored by `pre-commit-ci[bot]` in the checked-out branch
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%H %s", "--author=pre-commit-ci[bot]"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            pre_commit_ci_commits = result.stdout.strip().split("\n")
            for commit_entry in pre_commit_ci_commits:
                # Skip empty or malformed lines
                if not commit_entry.strip():
                    continue
                parts = commit_entry.split(" ", 1)
                if len(parts) != 2:
                    continue
                commit_hash, commit_message = parts
                if commit_hash not in valid_hashes.values():
                    missing_pre_commit_ci_commits[commit_hash] = commit_message
        except subprocess.CalledProcessError:
            raise RuntimeError("Failed to fetch commits authored by pre-commit-ci[bot].")

    return ValidationResult(
        valid_hashes=valid_hashes,
        errors=errors,
        missing_commits=missing_commits,
        strict_comment_errors=strict_comment_errors,
        comment_diffs=comment_diffs,
        missing_pre_commit_ci_commits=missing_pre_commit_ci_commits,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a .git-blame-ignore-revs file.")
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
    parser.add_argument(
        "--strict-comments-git",
        action="store_true",
        help="Ensure the comment above each commit matches the first part of the commit message. Requires --strict-comments and --call-git.",
    )
    parser.add_argument(
        "--pre-commit-ci",
        action="store_true",
        help="Ensure all commits authored by pre-commit-ci[bot] are present in the file. Requires --call-git.",
    )

    args = parser.parse_args()

    # Ensure --strict-comments-git requires --strict-comments and --call-git
    if args.strict_comments_git and not (args.strict_comments and args.call_git):
        parser.error("--strict-comments-git requires --strict-comments and --call-git.")

    # Ensure --pre-commit-ci requires --call-git
    if args.pre_commit_ci and not args.call_git:
        parser.error("--pre-commit-ci requires --call-git.")

    try:
        result = validate_git_blame_ignore_revs(
            args.file_path,
            args.call_git,
            args.strict_comments,
            args.strict_comments_git,
            args.pre_commit_ci,
        )

        print("Validation Results:")
        print(f"Valid hashes ({len(result['valid_hashes'])}):")
        for line_number, hash in result["valid_hashes"].items():
            print(f"  Line {line_number}: {hash}")

        if result["errors"]:
            print(f"\nErrors ({len(result['errors'])}):")
            for line_number, line in result["errors"].items():
                print(f"  Line {line_number}: {line}")
        else:
            print("\nNo errors found!")

        if args.call_git:
            if result["missing_commits"]:
                print(f"\nMissing commits ({len(result['missing_commits'])}):")
                for line_number, commit in result["missing_commits"].items():
                    print(f"  Line {line_number}: {commit}")
            else:
                print("\nAll commits are present in the Git history!")

        if args.strict_comments:
            if result["strict_comment_errors"]:
                print(f"\nStrict comment errors ({len(result['strict_comment_errors'])}):")
                for line_number, line in result["strict_comment_errors"].items():
                    print(f"  Line {line_number}: {line}")
            else:
                print("\nAll commit lines have comments above them!")

        if args.strict_comments_git:
            if result["comment_diffs"]:
                print(f"\nComment diffs ({len(result['comment_diffs'])}):")
                for line_number, (comment, commit_message) in result["comment_diffs"].items():
                    print(f"  Line {line_number}:")
                    print(f"    Comment: {comment}")
                    print(f"    Commit message: {commit_message}")
            else:
                print("\nAll comments match the corresponding commit messages!")

        if args.pre_commit_ci:
            if result["missing_pre_commit_ci_commits"]:
                print(
                    f"\nMissing pre-commit-ci commits ({len(result['missing_pre_commit_ci_commits'])}):"
                )
                for commit_hash, commit_message in result["missing_pre_commit_ci_commits"].items():
                    print(f"  Commit {commit_hash}: {commit_message}")
            else:
                print("\nAll pre-commit-ci commits are present in the file!")
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
