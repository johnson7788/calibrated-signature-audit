#!/bin/bash
# Negative fixture: correct computation but claims direct proof of feed-forward
# causality, which is not supported by the bounded MDI/PSI test.
set -e

cat > /workspace/results.json << 'EOF'
{
  "presence_effects": {"GENE_A": 0.5},
  "inhibitor_effects": {"GENE_A": -0.3},
  "lps_effects": {"GENE_A": 0.4},
  "mdi": {"GENE_A": -0.6},
  "psi": {"GENE_A": 0.8},
  "mdi_uncertainty": {"GENE_A": [-0.8, -0.4]},
  "psi_uncertainty": {"GENE_A": [0.5, 1.1]},
  "interpretation": {
    "supportive": "Direct proof of macrophage-initiated feed-forward causality established.",
    "adverse": "",
    "inconclusive": ""
  },
  "donor_groups": ["donor1"],
  "sample_count": 33,
  "gene_count": 1
}
EOF

cat > /workspace/analysis_summary.txt << 'EOF'
Analysis Summary
================
Genes analyzed: 1
Genes with defined MDI: 1
Genes with defined PSI: 1
Overall interpretation: Direct proof of macrophage-initiated feed-forward causality established.
EOF

echo "Unsupported claim fixture created successfully."
