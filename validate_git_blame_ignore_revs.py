import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Union


def validate_git_blame_ignore_revs(
    file_path: Union[str, Path], call_git: bool = False
) -> Dict[str, Union[List[str], List[Tuple[int, str]]]]:
    """
    Validates the contents of a `.git-blame-ignore-revs` file.

    Args:
        file_path (Union[str, Path]): Path to the `.git-blame-ignore-revs` file.
        call_git (bool): If True, ensures each commit is in the history of the checked-out branch.

    Returns:
        dict: A dictionary containing valid hashes and errors.
    """
    # Convert Path object to string if necessary
    file_path = str(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    valid_hashes: List[str] = []
    errors: List[Tuple[int, str]] = []
    missing_commits: List[str] = []

    # Regular expression for a valid Git commit hash (40 hexadecimal characters)
    commit_hash_regex = re.compile(r"^[0-9a-f]{40}$")

    with open(file_path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            # Skip blank lines and comments
            if not line or line.startswith("#"):
                continue

            # Validate the commit hash
            if commit_hash_regex.match(line):
                valid_hashes.append(line)
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

    return {
        "valid_hashes": valid_hashes,
        "errors": errors,
        "missing_commits": missing_commits,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a .git-blame-ignore-revs file."
    )
    parser.add_argument(
        "file_path",
        type=Union[str, Path],
        help="Path to the .git-blame-ignore-revs file.",
    )
    parser.add_argument(
        "--call-git",
        action="store_true",
        help="Ensure each commit is in the history of the checked-out branch.",
    )

    args = parser.parse_args()

    try:
        result = validate_git_blame_ignore_revs(args.file_path, args.call_git)

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
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
