#!/bin/bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: ${0} <file_with_conflicts>"
    exit 1
fi

input_file="${1}"
base_name=$(basename "${input_file}")
dir_name=$(dirname "${input_file}")

extension="${base_name##*.}"
base_name_without_extension="${base_name%.*}"

if [[ "${base_name}" == "${base_name_without_extension}" ]]; then
    shebang=$(head -n 1 "${input_file}")
    if [[ "$shebang" =~ ^#!.*bash ]]; then
        extension="bash"
    elif [[ "$shebang" =~ ^#!.*python ]]; then
        extension="py"
    elif [[ "$shebang" =~ ^#!.*perl ]]; then
        extension="pl"
    elif [[ "$shebang" =~ ^#!.*ruby ]]; then
        extension="rb"
    else
        extension=""
    fi
fi

conflict_counter=0
current_section=""
file_template="${dir_name}/${base_name_without_extension}.%s.%s${extension:+.$extension}"

while IFS= read -r line; do
    if [[ "$line" =~ ^"<<<<<<<" ]]; then
        left_section=""
        middle_section=""
        right_section=""
        current_section="left"
        is_three_way=false
    elif [[ "$line" =~ ^\|\|\|\|\|\|\| ]]; then
        current_section="middle"
        is_three_way=true
    elif [[ "$line" =~ ^"=======" ]]; then
        current_section="right"
    elif [[ "$line" =~ ^">>>>>>>" ]]; then
        # shellcheck disable=SC2059
        left_file=$(printf "${file_template}" "left" "${conflict_counter}")
        # shellcheck disable=SC2059
        right_file=$(printf "${file_template}" "right" "${conflict_counter}")

        printf "%s" "${left_section}" > "${left_file}"
        printf "%s" "${right_section}" > "${right_file}"

        if $is_three_way; then
            # shellcheck disable=SC2059
            middle_file=$(printf "${file_template}" "middle" "${conflict_counter}")
            printf "%s" "${middle_section}" > "${middle_file}"
        fi

        conflict_counter=$((conflict_counter + 1))
    else
        case "$current_section" in
            left)
                left_section+="${line}"$'\n'
                ;;
            middle)
                middle_section+="${line}"$'\n'
                ;;
            right)
                right_section+="${line}"$'\n'
                ;;
            *)
                # Ignore lines outside of conflict regions
                ;;
        esac
    fi
done < "${input_file}"

echo "Processed ${conflict_counter} conflict(s)."
