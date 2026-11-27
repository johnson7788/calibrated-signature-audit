#!/bin/bash
set -euo pipefail

# Negative fixture: produces an empty output file.
# The verifier must reject this (reward 0).
touch /workspace/directionality_results.json
echo "Wrote empty output file"
