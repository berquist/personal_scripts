#!/bin/bash

# qdel range of values:
echo "Kill these jobs? (c-C to quit)"
echo $(seq -f "%.0f" $1 $2)
read response

echo "qdel $(echo $(seq -f "%.0f" $1 $2))"

qdel $(echo $(seq -f "%.0f" $1 $2))
