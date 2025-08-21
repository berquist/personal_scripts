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
    comment_diffs: Dict[
        int, Tuple[str, str]
    ]  # Line number -> (comment, commit message)


def validate_git_blame_ignore_revs(
    file_path: Union[str, Path],
    call_git: bool = False,
    strict_comments: bool = False,
    strict_comments_git: bool = False,
) -> ValidationResult:
    """
    Validates the contents of a `.git-blame-ignore-revs` file.

    Args:
        file_path (Union[str, Path]): Path to the `.git-blame-ignore-revs` file.
        call_git (bool): If True, ensures each commit is in the history of the checked-out branch.
        strict_comments (bool): If True, requires each commit line to have one or more comment lines above it.
        strict_comments_git (bool): If True, ensures the comment above each commit matches the first part of the commit message.

    Returns:
        ValidationResult: A dictionary containing valid hashes, errors, missing commits, strict comment errors, and comment diffs.
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
        commit_hashes = list(valid_hashes.values())
        try:
            result = subprocess.run(
                ["git", "show", "--pretty=format:%H %s", "--no-patch"] + commit_hashes,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            git_output = result.stdout.strip().split("\n")
            git_commit_map = {
                line.split(" ", 1)[0]: line.split(" ", 1)[1] for line in git_output
            }

            for line_number, commit_hash in valid_hashes.items():
                if commit_hash not in git_commit_map:
                    missing_commits[line_number] = commit_hash
                elif strict_comments_git:
                    commit_message = git_commit_map[commit_hash]
                    last_comment = (
                        lines[line_number - 2].strip().lstrip("#").strip()
                        if line_number > 1
                        else ""
                    )
                    if not commit_message.startswith(last_comment):
                        comment_diffs[line_number] = (last_comment, commit_message)
        except subprocess.CalledProcessError:
            for line_number, commit_hash in valid_hashes.items():
                missing_commits[line_number] = commit_hash

    return ValidationResult(
        valid_hashes=valid_hashes,
        errors=errors,
        missing_commits=missing_commits,
        strict_comment_errors=strict_comment_errors,
        comment_diffs=comment_diffs,
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
    parser.add_argument(
        "--strict-comments-git",
        action="store_true",
        help="Ensure the comment above each commit matches the first part of the commit message. Requires --strict-comments and --call-git.",
    )

    args = parser.parse_args()

    # Ensure --strict-comments-git requires --strict-comments and --call-git
    if args.strict_comments_git and not (args.strict_comments and args.call_git):
        parser.error("--strict-comments-git requires --strict-comments and --call-git.")

    try:
        result = validate_git_blame_ignore_revs(
            args.file_path,
            args.call_git,
            args.strict_comments,
            args.strict_comments_git,
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
                print(
                    f"\nStrict comment errors ({len(result['strict_comment_errors'])}):"
                )
                for line_number, line in result["strict_comment_errors"].items():
                    print(f"  Line {line_number}: {line}")
            else:
                print("\nAll commit lines have comments above them!")

        if args.strict_comments_git:
            if result["comment_diffs"]:
                print(f"\nComment diffs ({len(result['comment_diffs'])}):")
                for line_number, (comment, commit_message) in result[
                    "comment_diffs"
                ].items():
                    print(f"  Line {line_number}:")
                    print(f"    Comment: {comment}")
                    print(f"    Commit message: {commit_message}")
            else:
                print("\nAll comments match the corresponding commit messages!")
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
