#!/usr/bin/env bash
# Resolve an OCI image tag to its full name with SHA256 digest using skopeo.

set -euo pipefail

if ! command -v skopeo &> /dev/null; then
    echo "Error: skopeo is not installed. Please install it (e.g., 'dnf install skopeo' or 'apt install skopeo')." >&2
    exit 1
fi

if [ $# -ne 1 ]; then
    echo "Usage: $0 <oci-image-tag>" >&2
    echo "Example: $0 rockylinux/rockylinux:8.10.20240528" >&2
    exit 1
fi

IMAGE_TAG="$1"

# Use skopeo to inspect the image and extract the digest
DIGEST=$(skopeo inspect "docker://${IMAGE_TAG}" --no-tags --raw | jq -r '.manifests[0].digest')

if [ -z "$DIGEST" ]; then
    echo "Error: Could not resolve digest for ${IMAGE_TAG}" >&2
    exit 1
fi

# Construct the full image reference with SHA256
FULL_IMAGE="${IMAGE_TAG}@${DIGEST}"
echo "$FULL_IMAGE"
