#!/usr/bin/env bash
# shellcheck disable=SC2086

# format the contents of non-existent commits as one big patch

upstream="${1}"
head="${2}"
outname="${upstream}"_"${head}".patch

echo "" > ${outname}

echo ${upstream} ${head}
for sha1 in $(git cherry ${upstream} ${head} | awk '{print $2}'); do
    echo ${sha1}
    git format-patch --stdout -1 ${sha1} >> ${outname}
done
