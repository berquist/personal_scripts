#!/usr/bin/env bash


print_bytes () {
    filename=$1
    pos=$2

    # https://stackoverflow.com/a/27240651/3249688
    a=0
    # max=$(cat $filename | wc -c)
    # while [[ $((++a)) -lt $max ]]; do
    while [[ $((++a)) -le $pos ]]; do
        cat $filename | head -c$a | tail -c1 | \
            xargs -0 -I{} printf '%c %#02x\n' {} "'{}"
    done
}

err_path=/tmp/iconv.error

for f in *; do
    type=$(file --mime "$f" | cut -d '=' -f 2)
    if [[ "$type" == "utf-8" ]]; then
        echo "$f"
        iconv -f utf-8 -t ascii < "$f" 1> /dev/null 2> $err_path
        if $(test -s $err_path); then
            byte_pos=$(rg -No "\b\d*$" $err_path)
            print_bytes $f $byte_pos
            rm $err_path
        fi
    fi
done
