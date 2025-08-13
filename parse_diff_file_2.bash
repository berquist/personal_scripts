#!/bin/bash

set -euo pipefail
set -x

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <diff_file>"
    exit 1
fi

diff_file="$1"
diff_file_base_name=$(basename "$diff_file")
diff_file_dir_name=$(dirname "$diff_file")
diff_file_name_without_extension="${diff_file_base_name%.*}"

diffed_file_counter=-1 # Initialize to -1 to indicate no files have been processed yet

# Initialize variables for hunk processing
left_section=""
right_section=""
left_file_name=""
right_file_name=""
left_file_extension=""
right_file_extension=""
hunk_counter=0
left_start_line=""
right_start_line=""

# Function to sanitize filenames by replacing directory separators with underscores
sanitize_filename() {
    echo "$1" | tr '/' '_'
}

# Function to write the current hunk to files
write_hunk_to_files() {
    if [[ -n "$left_section" || -n "$right_section" ]]; then
        sanitized_left_file_name=$(sanitize_filename "$left_file_name_without_extension")
        sanitized_right_file_name=$(sanitize_filename "$right_file_name_without_extension")

        left_file="${diff_file_dir_name}/${diff_file_name_without_extension}.${diffed_file_counter}.left.${sanitized_left_file_name}.${hunk_counter}.${left_start_line}.${left_file_extension}"
        right_file="${diff_file_dir_name}/${diff_file_name_without_extension}.${diffed_file_counter}.right.${sanitized_right_file_name}.${hunk_counter}.${right_start_line}.${right_file_extension}"

        printf "%s" "$left_section" > "$left_file"
        printf "%s" "$right_section" > "$right_file"
    fi
}

# Read the diff file line by line
while IFS= read -r line; do
    if [[ "$line" == diff\ --git* ]]; then
        # Write the previous hunk before starting a new diffed file
        if ((diffed_file_counter >= 0)); then
            write_hunk_to_files
        fi
        # Start of a new diffed file (Git format)
        ((diffed_file_counter++))
        hunk_counter=0
        left_file_name=""
        right_file_name=""
        left_file_extension=""
        right_file_extension=""
        left_section=""
        right_section=""
    elif [[ "$line" == Index:\ * ]]; then
        # Write the previous hunk before starting a new diffed file
        if ((diffed_file_counter >= 0)); then
            write_hunk_to_files
        fi
        # Start of a new diffed file (Subversion format)
        ((diffed_file_counter++))
        hunk_counter=0
        left_file_name=""
        right_file_name=""
        left_file_extension=""
        right_file_extension=""
        left_section=""
        right_section=""
        # Extract the file name from the "Index:" line
        left_file_name="${line#Index: }"
        left_file_name_without_extension="${left_file_name%.*}"
        left_file_extension="${left_file_name##*.}"
        right_file_name="$left_file_name" # Subversion diffs don't specify a separate modified file name
        right_file_name_without_extension="$left_file_name_without_extension"
        right_file_extension="$left_file_extension"
    elif [[ "$line" == @@* ]]; then
        # Write the previous hunk before starting a new hunk
        if ((diffed_file_counter >= 0)); then
            write_hunk_to_files
        fi
        # Start of a new hunk
        ((hunk_counter++))
        # Extract hunk line numbers
        hunk_info="${line#@@ }"
        hunk_info="${hunk_info%% @@}"
        left_start_line="${hunk_info%%,*}" # Extract only the starting line number for the left file
        left_start_line="${left_start_line#-}"
        right_start_line="${hunk_info#* }"
        right_start_line="${right_start_line%%,*}" # Extract only the starting line number for the right file
        right_start_line="${right_start_line#+}"
        left_section=""
        right_section=""
    elif [[ "$line" == ---* ]]; then
        # Original file name (Git or Subversion format)
        left_file_name="${line#--- }"
        left_file_name_without_extension="${left_file_name%.*}"
        left_file_extension="${left_file_name##*.}"
    elif [[ "$line" == +++* ]]; then
        # Modified file name (Git or Subversion format)
        right_file_name="${line#+++ }"
        right_file_name_without_extension="${right_file_name%.*}"
        right_file_extension="${right_file_name##*.}"
    elif [[ "$line" == -* ]]; then
        # Line from the original file
        left_section+="${line:1}"$'\n'
    elif [[ "$line" == +* ]]; then
        # Line from the modified file
        right_section+="${line:1}"$'\n'
    elif [[ "$line" == \\* ]]; then
        # Ignore escaped lines (e.g., "\ No newline at end of file")
        continue
    else
        # Unchanged line (context line)
        left_section+="$line"$'\n'
        right_section+="$line"$'\n'
    fi
done < "$diff_file"

# Write the last hunk after processing the file
if ((diffed_file_counter >= 0)); then
    write_hunk_to_files
fi

echo "Processed $diffed_file_counter file(s) and $hunk_counter hunk(s)."
