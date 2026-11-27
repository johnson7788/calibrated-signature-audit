#!/bin/bash
# Negative fixture: empty output files.
set -e

echo "" > /workspace/results.json
echo "" > /workspace/analysis_summary.txt

echo "Empty output fixture created successfully."
