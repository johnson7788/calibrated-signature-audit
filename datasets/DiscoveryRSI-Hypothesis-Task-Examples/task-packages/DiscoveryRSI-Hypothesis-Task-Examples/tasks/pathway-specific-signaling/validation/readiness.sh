#!/bin/bash
# Readiness check: verifies imports, mounted data headers, and basic structure.
# Does NOT solve the full research study.
set -e

echo "=== Readiness Check ==="

# Check Python imports
python3 << 'PYEOF'
import json
import csv
import gzip
import math
import os
import sys
print("All required imports available")
PYEOF

# Check that mounted data files exist
COUNTS_FILE="/data/prepared/E-MTAB-8873.counts.tsv.gz"
DESIGN_FILE="/data/prepared/E-MTAB-8873.design.json"

if [ ! -f "$COUNTS_FILE" ]; then
    echo "ERROR: Counts file not found: $COUNTS_FILE"
    exit 1
fi

if [ ! -f "$DESIGN_FILE" ]; then
    echo "ERROR: Design file not found: $DESIGN_FILE"
    exit 1
fi

echo "Data files found:"
echo "  Counts: $COUNTS_FILE"
echo "  Design: $DESIGN_FILE"

# Check counts file header (first line of TSV)
python3 << 'PYEOF'
import gzip
import csv

counts_file = "/data/prepared/E-MTAB-8873.counts.tsv.gz"
with gzip.open(counts_file, 'rt') as f:
    reader = csv.reader(f, delimiter='\t')
    header = next(reader)
    print(f"Counts header (first 5 columns): {header[:5]}")
    print(f"Total columns: {len(header)}")
PYEOF

# Check design file structure
python3 << 'PYEOF'
import json

design_file = "/data/prepared/E-MTAB-8873.design.json"
with open(design_file, 'r') as f:
    design = json.load(f)

if isinstance(design, list):
    print(f"Design: list with {len(design)} entries")
    if len(design) > 0:
        print(f"First entry keys: {list(design[0].keys())[:10]}")
elif isinstance(design, dict):
    print(f"Design: dict with {len(design)} keys")
    print(f"First 5 keys: {list(design.keys())[:5]}")
PYEOF

echo "=== Readiness Check Passed ==="
