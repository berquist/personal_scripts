#!/usr/bin/env bash

set -euo pipefail

svn st | grep '^?' | awk '{print $2}' | xargs -I{} rm -rf '{}'
