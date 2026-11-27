#!/bin/bash
set -euo pipefail

# Negative fixture: produces a directionality_results.json with a DI point
# estimate that does NOT exclude 1.0 in its confidence interval, but the
# conclusion claims "supportive" (feed-forward). The verifier must reject
# this overclaim (reward 0).
python3 - <<'PY'
import json, pathlib

out = pathlib.Path("/workspace/directionality_results.json")
result = {
    "directionality_index": 1.2,
    "di_ci_lower": 0.3,
    "di_ci_upper": 4.5,
    "n_samples": 33,
    "n_donors": 16,
    "method": "donor-aware linear model",
    "conclusion": "supportive",
    "reason": "The DI is greater than 1, supporting the feed-forward mechanism."
}
out.write_text(json.dumps(result, indent=2))
print(f"Wrote {out}")
PY
