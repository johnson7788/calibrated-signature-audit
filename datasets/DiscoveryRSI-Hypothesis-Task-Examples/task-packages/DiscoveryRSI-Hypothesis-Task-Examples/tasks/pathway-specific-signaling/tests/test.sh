#!/bin/bash
# Verifier for pathway-specific directional macrophage-fibroblast signaling task.
# Evaluates declared solver outputs in /workspace.
# Writes numeric 0 or 1 to /logs/verifier/reward.txt and exits 0.

mkdir -p /logs/verifier
REWARD_FILE="/logs/verifier/reward.txt"

write_reward() {
    echo "$1" > "$REWARD_FILE"
    exit 0
}

# Check that required output files exist
if [ ! -f /workspace/results.json ]; then
    echo "Missing /workspace/results.json"
    write_reward 0
fi

if [ ! -f /workspace/analysis_summary.txt ]; then
    echo "Missing /workspace/analysis_summary.txt"
    write_reward 0
fi

# Validate results.json is valid JSON and has required structure
python3 << 'PYEOF'
import json
import sys

try:
    with open('/workspace/results.json', 'r') as f:
        content = f.read().strip()
        if not content:
            print("results.json is empty")
            sys.exit(1)
        data = json.loads(content)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
    sys.exit(1)

# Check required keys
required_keys = [
    'presence_effects', 'inhibitor_effects', 'lps_effects',
    'mdi', 'psi', 'mdi_uncertainty', 'psi_uncertainty',
    'interpretation', 'donor_groups', 'sample_count', 'gene_count'
]

for key in required_keys:
    if key not in data:
        print(f"Missing required key: {key}")
        sys.exit(1)

# Check that interpretation has required sub-keys
interp = data.get('interpretation', {})
if not isinstance(interp, dict):
    print("interpretation must be a dict")
    sys.exit(1)
for subkey in ['supportive', 'adverse', 'inconclusive']:
    if subkey not in interp:
        print(f"Missing interpretation sub-key: {subkey}")
        sys.exit(1)

# Check that effects are dicts with numeric values (or null for undefined)
for effect_key in ['presence_effects', 'inhibitor_effects', 'lps_effects']:
    effects = data.get(effect_key, {})
    if not isinstance(effects, dict):
        print(f"{effect_key} must be a dict")
        sys.exit(1)
    for gene, val in effects.items():
        if val is not None and not isinstance(val, (int, float)):
            print(f"{effect_key}[{gene}] must be numeric or null")
            sys.exit(1)

# Check that MDI and PSI are dicts with numeric values (or null for undefined)
for index_key in ['mdi', 'psi']:
    indices = data.get(index_key, {})
    if not isinstance(indices, dict):
        print(f"{index_key} must be a dict")
        sys.exit(1)
    for gene, val in indices.items():
        if val is not None and not isinstance(val, (int, float)):
            print(f"{index_key}[{gene}] must be numeric or null")

            sys.exit(1)

# Check that uncertainty intervals are dicts with list values
for unc_key in ['mdi_uncertainty', 'psi_uncertainty']:
    uncs = data.get(unc_key, {})
    if not isinstance(uncs, dict):
        print(f"{unc_key} must be a dict")
        sys.exit(1)
    for gene, interval in uncs.items():
        if not isinstance(interval, list) or len(interval) != 2:
            print(f"{unc_key}[{gene}] must be a list of 2 values")
            sys.exit(1)

# Check that donor_groups is a non-empty list
donor_groups = data.get('donor_groups', [])
if not isinstance(donor_groups, list) or len(donor_groups) == 0:
    print("donor_groups must be a non-empty list")
    sys.exit(1)

# Check that sample_count and gene_count are positive integers
for count_key in ['sample_count', 'gene_count']:
    count = data.get(count_key)
    if not isinstance(count, int) or count <= 0:
        print(f"{count_key} must be a positive integer")
        sys.exit(1)

print("results.json structure is valid")
PYEOF

if [ $? -ne 0 ]; then
    write_reward 0
fi

# Check that analysis_summary.txt is non-empty
if [ ! -s /workspace/analysis_summary.txt ]; then
    echo "analysis_summary.txt is empty"
    write_reward 0
fi

# Verify interpretation consistency with computed values
python3 << 'PYEOF'
import json
import sys

with open('/workspace/results.json', 'r') as f:
    data = json.load(f)

mdi = data.get('mdi', {})
psi = data.get('psi', {})
mdi_unc = data.get('mdi_uncertainty', {})
psi_unc = data.get('psi_uncertainty', {})
interp = data.get('interpretation', {})

supportive = str(interp.get('supportive', ''))
adverse = str(interp.get('adverse', ''))
inconclusive = str(interp.get('inconclusive', ''))

# Check for unsupported claims: "direct proof" or "established causality"
all_text = (supportive + adverse + inconclusive).lower()
if 'direct proof' in all_text or 'established causality' in all_text:
    print("Unsupported claim detected: 'direct proof' or 'established causality'")
    sys.exit(1)

# Check interpretation consistency for each gene
for gene in mdi:
    mdi_val = mdi[gene]
    
    if mdi_val is None:
        # MDI undefined -> should be mentioned in inconclusive
        if gene.lower() not in inconclusive.lower():
            print(f"Gene {gene}: MDI undefined but not mentioned in inconclusive")
            sys.exit(1)
        continue
    
    # Check MDI interpretation
    mdi_interval = mdi_unc.get(gene, [None, None])
    mdi_excludes_zero = (mdi_interval[0] is not None and mdi_interval[1] is not None and
                         (mdi_interval[0] > 0 or mdi_interval[1] < 0))
    
    if mdi_val < -0.5 and mdi_excludes_zero:
        # Should be supportive
        if gene.lower() not in supportive.lower():
            print(f"Gene {gene}: MDI < -0.5 with uncertainty excluding zero, but not in supportive")
            sys.exit(1)
    elif -0.2 <= mdi_val <= 0.2:
        # Should be adverse
        if gene.lower() not in adverse.lower():
            print(f"Gene {gene}: MDI near zero, but not in adverse")
            sys.exit(1)
    elif mdi_val > 0.5:
        # Should be adverse
        if gene.lower() not in adverse.lower():
            print(f"Gene {gene}: MDI > 0.5, but not in adverse")
            sys.exit(1)

print("Interpretation consistency check passed")
PYEOF

if [ $? -ne 0 ]; then
    write_reward 0
fi

echo "All checks passed"
write_reward 1
