#!/usr/bin/env bash
# Resolve an OCI image tag to its full name with SHA256 digest using podman.

set -euo pipefail

if ! command -v podman &> /dev/null; then
    echo "Error: podman is not installed. Please install it (e.g., 'dnf install podman' or 'apt install podman')." >&2
    exit 1
fi

if [ $# -ne 1 ]; then
    echo "Usage: $0 <oci-image-tag>" >&2
    echo "Example: $0 rockylinux/rockylinux:8.10.20240528" >&2
    exit 1
fi

IMAGE_TAG="$1"

# Pull the image to ensure it's available locally (if not already cached)
podman pull "$IMAGE_TAG" > /dev/null 2>&1

# Use podman to inspect the image and extract the digest
DIGEST=$(podman inspect "$IMAGE_TAG" --format '{{.Digest}}')

if [ -z "$DIGEST" ]; then
    echo "Error: Could not resolve digest for ${IMAGE_TAG}" >&2
    exit 1
fi

# Construct the full image reference with SHA256
FULL_IMAGE="${IMAGE_TAG}@${DIGEST}"
echo "$FULL_IMAGE"
