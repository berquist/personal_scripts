#!/bin/bash

# findclass_jars.sh: https://stackoverflow.com/a/68411760

SCRIPTDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

find "${1}" -type f -name '*.jar' -exec "${SCRIPTDIR}"/findclass.sh '{}' "${2}" \;
