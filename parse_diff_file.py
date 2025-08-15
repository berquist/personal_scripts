import os
import sys


def sanitize_filename(filename: str) -> str:
    """Sanitize filenames by replacing directory separators with underscores."""
    return filename.replace("/", "_")


def write_hunk_to_files(
    diff_file_dir_name: str,
    diff_file_name_without_extension: str,
    diffed_file_counter: int,
    left_file_name_without_extension: str,
    right_file_name_without_extension: str,
    hunk_counter: int,
    left_start_line: str,
    right_start_line: str,
    left_file_extension: str,
    right_file_extension: str,
    left_section: str,
    right_section: str,
) -> None:
    """Write the current hunk to files."""
    if left_section or right_section:
        sanitized_left_file_name = sanitize_filename(left_file_name_without_extension)
        sanitized_right_file_name = sanitize_filename(right_file_name_without_extension)

        left_file = os.path.join(
            diff_file_dir_name,
            f"{diff_file_name_without_extension}.{diffed_file_counter}.left."
            f"{sanitized_left_file_name}.{hunk_counter}.{left_start_line}.{left_file_extension}",
        )
        right_file = os.path.join(
            diff_file_dir_name,
            f"{diff_file_name_without_extension}.{diffed_file_counter}.right."
            f"{sanitized_right_file_name}.{hunk_counter}.{right_start_line}.{right_file_extension}",
        )

        with open(left_file, "w") as lf, open(right_file, "w") as rf:
            lf.write(left_section)
            rf.write(right_section)


def process_diff_file(diff_file: str) -> None:
    """Process the diff file and write hunks to output files."""
    diff_file_base_name = os.path.basename(diff_file)
    diff_file_dir_name = os.path.dirname(diff_file)
    diff_file_name_without_extension, _ = os.path.splitext(diff_file_base_name)

    diffed_file_counter = -1  # Initialize to -1 to indicate no files have been processed yet
    hunk_counter = 0

    # Initialize variables for hunk processing
    left_section = ""
    right_section = ""
    left_file_name_without_extension = ""
    right_file_name_without_extension = ""
    left_file_extension = ""
    right_file_extension = ""
    left_start_line = ""
    right_start_line = ""

    with open(diff_file, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("---"):
                # Write the previous hunk before starting a new diffed file
                if diffed_file_counter >= 0:
                    write_hunk_to_files(
                        diff_file_dir_name,
                        diff_file_name_without_extension,
                        diffed_file_counter,
                        left_file_name_without_extension,
                        right_file_name_without_extension,
                        hunk_counter,
                        left_start_line,
                        right_start_line,
                        left_file_extension,
                        right_file_extension,
                        left_section,
                        right_section,
                    )
                # Start of a new diffed file (original file)
                diffed_file_counter += 1
                hunk_counter = 0
                left_file_name = line[4:]
                left_file_name_without_extension, left_file_extension = os.path.splitext(
                    left_file_name
                )
                left_file_extension = left_file_extension.lstrip(".")
                left_section = ""
                right_section = ""
            elif line.startswith("+++"):
                # Modified file name (new file)
                right_file_name = line[4:]
                right_file_name_without_extension, right_file_extension = os.path.splitext(
                    right_file_name
                )
                right_file_extension = right_file_extension.lstrip(".")
            elif line.startswith("@@"):
                # Write the previous hunk before starting a new hunk
                if diffed_file_counter >= 0:
                    write_hunk_to_files(
                        diff_file_dir_name,
                        diff_file_name_without_extension,
                        diffed_file_counter,
                        left_file_name_without_extension,
                        right_file_name_without_extension,
                        hunk_counter,
                        left_start_line,
                        right_start_line,
                        left_file_extension,
                        right_file_extension,
                        left_section,
                        right_section,
                    )
                # Start of a new hunk
                hunk_counter += 1
                # Extract hunk line numbers
                hunk_info = line[3:].split(" ")[0]
                left_start_line = hunk_info.split(",")[0].lstrip("-")
                right_start_line = hunk_info.split(" ")[1].split(",")[0].lstrip("+")
                left_section = ""
                right_section = ""
            elif line.startswith("-"):
                # Line from the original file
                left_section += line[1:] + "\n"
            elif line.startswith("+"):
                # Line from the modified file
                right_section += line[1:] + "\n"
            elif line.startswith("\\"):
                # Ignore escaped lines (e.g., "\ No newline at end of file")
                continue
            else:
                # Unchanged line (context line)
                left_section += line + "\n"
                right_section += line + "\n"

    # Write the last hunk after processing the file
    if diffed_file_counter >= 0:
        write_hunk_to_files(
            diff_file_dir_name,
            diff_file_name_without_extension,
            diffed_file_counter,
            left_file_name_without_extension,
            right_file_name_without_extension,
            hunk_counter,
            left_start_line,
            right_start_line,
            left_file_extension,
            right_file_extension,
            left_section,
            right_section,
        )

    print(f"Processed {diffed_file_counter} file(s) and {hunk_counter} hunk(s).")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <diff_file>")
        sys.exit(1)

    diff_file = sys.argv[1]
    process_diff_file(diff_file)


if __name__ == "__main__":
    main()
