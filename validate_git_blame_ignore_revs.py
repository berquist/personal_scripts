import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, TypedDict, Union


class ValidationResult(TypedDict):
    valid_hashes: Dict[int, str]
    errors: Dict[int, str]
    missing_commits: Dict[int, str]
    strict_comment_errors: Dict[int, str]
    comment_diffs: Dict[int, Tuple[str, str]]  # Line number -> (comment, commit message)
    missing_pre_commit_ci_commits: Dict[str, str]  # Commit hash -> Commit message


def run_git_command(command: List[str]) -> str:
    """Run a Git command and return its output."""
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {' '.join(command)}\n{e.stderr.strip()}")


def parse_git_blame_ignore_revs(file_path: Union[str, Path]) -> Tuple[List[str], Dict[int, str]]:
    """Parse the `.git-blame-ignore-revs` file and return lines and valid hashes."""
    file_path = str(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, "r") as file:
        lines = file.readlines()

    valid_hashes = {}
    commit_hash_regex = re.compile(r"^[0-9a-f]{40}$")

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if commit_hash_regex.match(line):
            valid_hashes[line_number] = line

    return lines, valid_hashes


def validate_commit_hashes(
    valid_hashes: Dict[int, str], lines: List[str], strict_comments: bool, strict_comments_git: bool
) -> Tuple[Dict[int, str], Dict[int, Tuple[str, str]]]:
    """Validate commit hashes for strict comments and strict comments git."""
    strict_comment_errors = {}
    comment_diffs = {}

    for line_number, commit_hash in valid_hashes.items():
        last_comment = lines[line_number - 2].strip().lstrip("#").strip() if line_number > 1 else ""

        if strict_comments and not last_comment:
            strict_comment_errors[line_number] = commit_hash

        if strict_comments_git:
            try:
                commit_message = run_git_command(
                    ["git", "show", "--quiet", "--pretty=format:%s", commit_hash]
                )
                if not commit_message.startswith(last_comment):
                    comment_diffs[line_number] = (last_comment, commit_message)
            except RuntimeError:
                # If `git show` fails, treat the commit as missing
                strict_comment_errors[line_number] = commit_hash

    return strict_comment_errors, comment_diffs


def validate_pre_commit_ci_commits(
    valid_hashes: Dict[int, str], lines: List[str], strict_comments: bool, strict_comments_git: bool
) -> Dict[str, str]:
    """Validate pre-commit.ci commits."""
    pre_commit_ci_commits = run_git_command(
        ["git", "log", "--pretty=format:%H %s", "--author=pre-commit-ci[bot]"]
    )
    missing_pre_commit_ci_commits = {}

    for commit_entry in pre_commit_ci_commits.split("\n"):
        if not commit_entry.strip():
            continue
        parts = commit_entry.split(" ", 1)
        if len(parts) != 2:
            continue
        commit_hash, commit_message = parts

        if commit_hash not in valid_hashes.values():
            missing_pre_commit_ci_commits[commit_hash] = commit_message
        elif strict_comments or strict_comments_git:
            for line_number, line in valid_hashes.items():
                if line == commit_hash:
                    last_comment = (
                        lines[line_number - 2].strip().lstrip("#").strip()
                        if line_number > 1
                        else ""
                    )
                    if strict_comments and not last_comment:
                        missing_pre_commit_ci_commits[commit_hash] = commit_message
                    if strict_comments_git and not commit_message.startswith(last_comment):
                        missing_pre_commit_ci_commits[commit_hash] = commit_message

    return missing_pre_commit_ci_commits


def validate_git_blame_ignore_revs(
    file_path: Union[str, Path],
    call_git: bool = False,
    strict_comments: bool = False,
    strict_comments_git: bool = False,
    pre_commit_ci: bool = False,
) -> ValidationResult:
    """Validate the `.git-blame-ignore-revs` file."""
    lines, valid_hashes = parse_git_blame_ignore_revs(file_path)

    # Identify errors: non-blank, non-comment lines that are not valid commit hashes
    errors = {
        line_number: line.strip()
        for line_number, line in enumerate(lines, start=1)
        if line.strip() and not line.strip().startswith("#") and line_number not in valid_hashes
    }

    missing_commits = {}
    if call_git:
        for line_number, commit_hash in valid_hashes.items():
            try:
                run_git_command(["git", "cat-file", "-e", commit_hash])
            except RuntimeError:
                missing_commits[line_number] = commit_hash

    strict_comment_errors, comment_diffs = validate_commit_hashes(
        valid_hashes, lines, strict_comments, strict_comments_git
    )

    missing_pre_commit_ci_commits = {}
    if pre_commit_ci:
        missing_pre_commit_ci_commits = validate_pre_commit_ci_commits(
            valid_hashes, lines, strict_comments, strict_comments_git
        )

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
    parser.add_argument("file_path", type=Path, help="Path to the .git-blame-ignore-revs file.")
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

    if args.strict_comments_git and not (args.strict_comments and args.call_git):
        parser.error("--strict-comments-git requires --strict-comments and --call-git.")
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
