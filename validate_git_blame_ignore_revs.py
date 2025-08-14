import os
import re


def validate_git_blame_ignore_revs(file_path):
    """
    Validates the contents of a `.git-blame-ignore-revs` file.

    Args:
        file_path (str): Path to the `.git-blame-ignore-revs` file.

    Returns:
        dict: A dictionary containing valid hashes and errors.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    valid_hashes = []
    errors = []

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

    return {
        "valid_hashes": valid_hashes,
        "errors": errors,
    }


def main():
    file_path = ".git-blame-ignore-revs"  # Change this to the path of your file

    try:
        result = validate_git_blame_ignore_revs(file_path)

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
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
