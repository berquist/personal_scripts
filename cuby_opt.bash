#!/usr/bin/env bash

# cuby_opt.bash: Perform a Cuby4-based geometry optimization.

set -v
inputfilename="${1}"
stub="${inputfilename%.*}"
$(command -v cuby4) "${stub}".yaml >& "${stub}".out
mv optimized.xyz "${stub}".xyz
\rm grad.pdb
\rm -r job_*
