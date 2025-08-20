#!/bin/bash

# git_fix_branch_for_upstream.sh: When cloning a fork, the upstream repository
# is not set.  Attempt to get the correct upstream if it is not already set as
# a remote.  Then reset the current default branch to track the upstream's
# default.
#
# If the upstream remote is missing, finding it only works for GitHub.  If it
# is present, the remaining logic is forge agnostic.
#
# External dependencies:
#  - curl
#  - jq

# Perform our own error handling.
# set -eo pipefail

# This function assumes that a remote named "origin" is set.
get_github_api_url() {
    local origin_url
    origin_url=$(git remote get-url origin)

    if [[ "$origin_url" =~ ^git@github\.com:(.+)/(.+)\.git$ ]]; then
        echo "https://api.github.com/repos/${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    elif [[ "$origin_url" =~ ^https://github\.com/(.+)/(.+)\.git$ ]]; then
        echo "https://api.github.com/repos/${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    else
        echo ""
    fi
}

get_upstream_github_repo() {
    local api_url
    api_url="${1}"

    local response
    response="$(curl -s "${api_url}")"

    local is_fork
    is_fork="$(echo "${response}" | jq -r '.fork')"
    if [[ "${is_fork}" == "true" ]]; then
        local parent_repo
        parent_repo="$(echo "${response}" | jq -r '.parent.full_name')"
        echo "${parent_repo}"
    else
        echo ""
    fi
}

if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "Error: This script must be run inside a Git repository." >&2
    exit 1
fi

if ! git remote | grep -q upstream; then
    echo "No 'upstream' remote found. Attempting to determine the upstream repository..."

    github_api_url="$(get_github_api_url)"
    if [[ -z "${github_api_url}" ]]; then
        echo "Error: The 'origin' remote is not a GitHub repository or is in an unsupported format." >&2
        exit 1
    fi

    upstream_repo="$(get_upstream_github_repo "${github_api_url}")"
    if [[ -z "${upstream_repo}" ]]; then
        echo "Error: Unable to determine the upstream repository. The 'origin' remote may not be a fork." >&2
        exit 1
    fi

    echo "Upstream repository determined: ${upstream_repo}"

    git remote add upstream "https://github.com/${upstream_repo}.git"
    echo "Upstream remote added: https://github.com/${upstream_repo}.git"
fi

echo "Fetching upstream remote..."
git fetch upstream

default_branch="$(git remote show upstream | awk '/HEAD branch/ {print $NF}')"

if [[ -z "${default_branch}" ]]; then
    echo "Error: Unable to determine the default branch of the upstream remote." >&2
    exit 1
fi

echo "Default branch of upstream remote: ${default_branch}"

current_branch="$(git symbolic-ref --short HEAD)"

if [[ -z "${current_branch}" ]]; then
    echo "Error: Unable to determine the currently checked-out branch." >&2
    exit 1
fi

echo "Currently checked-out branch: $current_branch"

if [[ "${current_branch}" != "${default_branch}" ]]; then
    echo "Switching to the default branch of the upstream remote: ${default_branch}"
    git checkout "${default_branch}"
fi

tracking_branch="$(git rev-parse --abbrev-ref --symbolic-full-name "$default_branch@{upstream}" 2> /dev/null || true)"

if [[ "${tracking_branch}" != "upstream/${default_branch}" ]]; then
    echo "Setting upstream tracking for branch '$default_branch' to 'upstream/$default_branch'..."
    git branch --set-upstream-to="upstream/$default_branch" "$default_branch"
fi

echo "The current branch is now '$default_branch', tracking 'upstream/$default_branch'."
