#!/bin/bash
# Verifier for the directional macrophage-fibroblast signaling task.
# Evaluates /workspace/directionality_results.json against the declared
# scientific criteria. Writes numeric 0 or 1 to /logs/verifier/reward.txt
# and exits 0 for both acceptance and rejection.
#
# IMPORTANT: This script must always exit 0. Rejection is signaled by
# writing 0 to the reward file, not by a nonzero exit status.

REWARD_FILE="/logs/verifier/reward.txt"
mkdir -p "$(dirname "$REWARD_FILE")"

write_reward() {
  echo "$1" > "$REWARD_FILE"
  exit 0
}

# --- Check that the output file exists and is non-empty ---
OUT="/workspace/directionality_results.json"
if [ ! -f "$OUT" ] || [ ! -s "$OUT" ]; then
  write_reward 0
fi

# --- Parse the JSON and validate structure, evaluate conclusion ---
python3 - <<'PY'
import json, sys, pathlib

out = pathlib.Path("/workspace/directionality_results.json")
try:
    data = json.loads(out.read_text())
except (json.JSONDecodeError, UnicodeDecodeError) as e:
    print(f"ERROR: cannot parse JSON: {e}", file=sys.stderr)
    sys.exit(1)

if not isinstance(data, dict):
    print("ERROR: top-level JSON is not an object", file=sys.stderr)
    sys.exit(1)

required = ["directionality_index", "di_ci_lower", "di_ci_upper", "conclusion"]
for field in required:
    if field not in data:
        print(f"ERROR: missing required field: {field}", file=sys.stderr)
        sys.exit(1)

di = data["directionality_index"]
ci_lo = data["di_ci_lower"]
ci_hi = data["di_ci_upper"]
conclusion = data["conclusion"]

for name, val in [("directionality_index", di), ("di_ci_lower", ci_lo), ("di_ci_upper", ci_hi)]:
    if not isinstance(val, (int, float)):
        print(f"ERROR: {name} is not numeric: {val!r}", file=sys.stderr)
        sys.exit(1)

if not isinstance(conclusion, str):
    print(f"ERROR: conclusion is not a string: {conclusion!r}", file=sys.stderr)
    sys.exit(1)

if not (ci_lo <= di <= ci_hi):
    print(f"ERROR: CI does not contain point estimate: [{ci_lo}, {ci_hi}] vs {di}", file=sys.stderr)
    sys.exit(1)

ci_spans_one = ci_lo <= 1.0 <= ci_hi
ci_above_one = ci_lo > 1.0
ci_below_one = ci_hi < 1.0

conclusion_norm = conclusion.strip().lower()

if conclusion_norm in ("supportive", "feed-forward", "feed forward"):
    if not ci_above_one:
        print(f"REJECT: conclusion 'supportive' but CI [{ci_lo}, {ci_hi}] does not exclude 1.0 on the low side", file=sys.stderr)
        sys.exit(1)
elif conclusion_norm in ("adverse", "reciprocal", "fibroblast-initiated"):
    if not ci_below_one:
        print(f"REJECT: conclusion 'adverse' but CI [{ci_lo}, {ci_hi}] does not exclude 1.0 on the high side", file=sys.stderr)
        sys.exit(1)
elif conclusion_norm in ("inconclusive", "indeterminate", "ambiguous"):
    if not ci_spans_one:
        print(f"REJECT: conclusion 'inconclusive' but CI [{ci_lo}, {ci_hi}] does not span 1.0", file=sys.stderr)
        sys.exit(1)
else:
    print(f"REJECT: unrecognized conclusion: {conclusion!r}", file=sys.stderr)
    sys.exit(1)

print("OK: conclusion is consistent with the confidence interval")
PY

rc=$?
if [ "$rc" -ne 0 ]; then
  write_reward 0
fi

write_reward 1
