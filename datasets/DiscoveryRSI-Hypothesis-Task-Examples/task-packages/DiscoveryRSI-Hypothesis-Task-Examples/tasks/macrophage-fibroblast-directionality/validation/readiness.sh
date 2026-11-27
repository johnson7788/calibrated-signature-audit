#!/bin/bash
set -euo pipefail

# Check that the data files are mounted and readable
for f in /data/prepared/E-MTAB-8873.counts.tsv.gz /data/prepared/E-MTAB-8873.design.json; do
  if [ ! -f "$f" ]; then
    echo "ERROR: Missing data file: $f" >&2
    exit 1
  fi
done

# Check that the counts file is a valid gzip TSV with the expected header
python3 - <<'PY'
import gzip, csv, sys

path = "/data/prepared/E-MTAB-8873.counts.tsv.gz"
with gzip.open(path, "rt", newline="") as fh:
    reader = csv.reader(fh, delimiter="\t")
    header = next(reader)
    # The counts matrix should have a feature column and sample columns
    if len(header) < 2:
        print("ERROR: counts.tsv.gz header has fewer than 2 columns", file=sys.stderr)
        sys.exit(1)
    # Verify the first data row parses
    row = next(reader)
    if len(row) != len(header):
        print("ERROR: counts.tsv.gz row length does not match header", file=sys.stderr)
        sys.exit(1)

print("OK: E-MTAB-8873.counts.tsv.gz header and first row validated")
PY

# Check that the design JSON is valid
python3 - <<'PY'
import json, sys

path = "/data/prepared/E-MTAB-8873.design.json"
with open(path) as fh:
    data = json.load(fh)
if not isinstance(data, (dict, list)):
    print("ERROR: design.json is not a dict or list", file=sys.stderr)
    sys.exit(1)
print("OK: E-MTAB-8873.design.json is valid JSON")
PY

echo "Readiness checks passed"
