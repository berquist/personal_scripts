#!/bin/bash

set -v
inputfilename="${1}"
stub="${inputfilename%.*}"
$(which cuby4) "${stub}".yaml >& "${stub}".out
mv optimized.xyz "${stub}".xyz
\rm grad.pdb
\rm -r job_*
