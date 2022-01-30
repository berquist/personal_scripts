#!/usr/bin/env bash

set -eo pipefail

env_path_file=$HOME/.conda/environments.txt

while read -r env_path; do
    env_name=$(basename "${env_path}")
    if [[ $env_name == ".anaconda" ]]; then
        env_name="base"
    fi
    echo $env_name
    conda env export -n $env_name > environment_$env_name.yml
done < "${env_path_file}"
    
