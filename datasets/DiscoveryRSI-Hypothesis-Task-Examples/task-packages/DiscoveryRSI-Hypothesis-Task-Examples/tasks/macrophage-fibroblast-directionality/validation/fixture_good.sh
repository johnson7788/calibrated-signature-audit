#!/bin/bash
set -euo pipefail

# Synthetic positive fixture: produces a valid directionality_results.json
# with a plausible DI estimate and uncertainty, and a conclusion that
# correctly reflects the result (inconclusive when uncertainty is wide).
python3 - <<'PY'
import json, pathlib

out = pathlib.Path("/workspace/directionality_results.json")
result = {
    "directionality_index": 1.8,
    "di_ci_lower": 0.4,
    "di_ci_upper": 7.2,
    "n_samples": 33,
    "n_donors": 16,
    "method": "donor-aware linear model",
    "conclusion": "inconclusive",
    "reason": "The 95% confidence interval for the DI spans 1.0, so the data do not resolve feed-forward versus reciprocal signaling. Additional perturbation data are needed."
}
out.write_text(json.dumps(result, indent=2))
print(f"Wrote {out}")
PY
