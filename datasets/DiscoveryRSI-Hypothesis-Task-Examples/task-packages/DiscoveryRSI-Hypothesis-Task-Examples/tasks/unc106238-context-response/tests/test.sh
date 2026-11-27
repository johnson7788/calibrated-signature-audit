#!/bin/bash
set -uo pipefail

# Verifier: evaluates declared solver outputs in /workspace.
# Writes numeric 0 or 1 to /logs/verifier/reward.txt and exits 0.

mkdir -p /logs/verifier
REWARD=0

# Check that results.json exists
RESULT_PATH="/workspace/results.json"
if [ ! -f "$RESULT_PATH" ]; then
  echo "results.json not found" > /logs/verifier/reward.txt
  echo "0" > /logs/verifier/reward.txt
  exit 0
fi

# Validate the result with Python
python3 - <<'PY'
import json, sys

try:
    with open("/workspace/results.json") as f:
        r = json.load(f)
except Exception as e:
    print(f"Failed to parse results.json: {e}")
    sys.exit(1)

errors = []

# Required top-level keys
for key in ["program", "baseline", "ridge", "outcome", "limitations"]:
    if key not in r:
        errors.append(f"Missing required key: {key}")

# Check outcome is valid
outcome = r.get("outcome")
if outcome not in ("supportive", "adverse", "inconclusive"):
    errors.append(f"Invalid outcome: {outcome}")

# Check program has criteria and genes
program = r.get("program", {})
if not isinstance(program, dict):
    errors.append("program is not a dict")
else:
    if "criteria" not in program:
        errors.append("program missing criteria")
    if "genes" not in program:
        errors.append("program missing genes")

# Check baseline has context_contrast
baseline = r.get("baseline", {})
if not isinstance(baseline, dict):
    errors.append("baseline is not a dict")
else:
    if "context_contrast" not in baseline:
        errors.append("baseline missing context_contrast")

# Check ridge has context_coefficient and composition_robust
ridge = r.get("ridge", {})
if not isinstance(ridge, dict):
    errors.append("ridge is not a dict")
else:
    if "context_coefficient" not in ridge:
        errors.append("ridge missing context_coefficient")
    if "composition_robust" not in ridge:
        errors.append("ridge missing composition_robust")

# Check limitations is non-empty
limitations = r.get("limitations", "")
if not isinstance(limitations, str) or len(limitations.strip()) == 0:
    errors.append("limitations is empty or not a string")

# Check for overclaiming: outcome supportive requires composition_robust True
if outcome == "supportive":
    if not ridge.get("composition_robust", False):
        errors.append("Outcome is supportive but ridge composition_robust is False")

# Check justification is present and non-empty
justification = r.get("justification", "")
if not isinstance(justification, str) or len(justification.strip()) == 0:
    errors.append("justification is empty or not a string")

# Check for overclaiming in justification
just_text = justification.lower()
if "causality is established" in just_text or "direct target causality" in just_text and "does not" not in just_text:
    errors.append("Justification overclaims direct target causality")

if errors:
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1)
else:
    print("Verifier passed")
    sys.exit(0)
PY

if [ $? -eq 0 ]; then
  REWARD=1
fi

echo "$REWARD" > /logs/verifier/reward.txt
exit 0
