#!/bin/bash
set -uo pipefail
# Bounded readiness checks: imports, data headers, and tiny fixture.
# Does not run the full study.
# Uses set -uo pipefail without -e so that import check failures are handled explicitly.

FAILED=0

# 1. Check declared imports
if ! python3 -c "import pandas, numpy, scipy, sklearn" 2>/dev/null; then
  echo "Missing declared imports: pandas, numpy, scipy, sklearn"
  FAILED=1
fi

# 2. Check counts file header
COUNTS_PATH="/data/prepared/E-MTAB-8316.counts.tsv.gz/E-MTAB-8316.counts.tsv.gz"
if [ -f "$COUNTS_PATH" ]; then
  HEADER=$(zcat "$COUNTS_PATH" 2>/dev/null | head -1 | tr -d '\r\n')
  if [[ "$HEADER" != feature* ]]; then
    echo "Counts header does not start with 'feature': $HEADER"
    FAILED=1
  fi
else
  echo "Counts file not found: $COUNTS_PATH"
  FAILED=1
fi

# 3. Check design file is valid JSON list
DESIGN_PATH="/data/prepared/E-MTAB-8316.design.json/E-MTAB-8316.design.json"
if [ -f "$DESIGN_PATH" ]; then
  if ! python3 -c "
import json
with open('$DESIGN_PATH') as f:
    d = json.load(f)
assert isinstance(d, list), 'Design is not a list'
assert len(d) > 0, 'Design is empty'
assert 'sample_id' in d[0], 'Design missing sample_id'
" 2>/dev/null; then
    echo "Design file check failed"
    FAILED=1
  fi
else
  echo "Design file not found: $DESIGN_PATH"
  FAILED=1
fi

# 4. Tiny synthetic fixture check
if ! python3 <<'PY' 2>/dev/null
import json, tempfile, os
result = {
  "program": {"criteria": {}, "genes": ["TEST"]},
  "baseline": {"context_contrast": 0.1, "ci_lower": -0.1, "ci_upper": 0.3},
  "ridge": {"context_coefficient": 0.1, "p_value": 0.5, "composition_robust": True},
  "outcome": "inconclusive",
  "justification": "Tiny fixture.",
  "limitations": "Exploratory."
}
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(result, f)
    path = f.name
with open(path) as f:
    loaded = json.load(f)
assert loaded["outcome"] in ("supportive", "adverse", "inconclusive")
os.unlink(path)
print("Tiny fixture check passed")
PY
then
  echo "Tiny fixture check failed"
  FAILED=1
fi

if [ $FAILED -ne 0 ]; then
  echo "Readiness checks FAILED"
  exit 1
fi

echo "Readiness checks passed"
exit 0
