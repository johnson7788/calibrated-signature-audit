#!/bin/bash
# Positive fixture: creates a valid results.json and analysis_summary.txt
# with correct structure and a consistent interpretation.
set -e

cat > /workspace/results.json << 'EOF'
{
  "presence_effects": {"GENE_A": 0.5, "GENE_B": 0.3},
  "inhibitor_effects": {"GENE_A": -0.3, "GENE_B": 0.05},
  "lps_effects": {"GENE_A": 0.4, "GENE_B": 0.1},
  "mdi": {"GENE_A": -0.6, "GENE_B": 0.167},
  "psi": {"GENE_A": 0.8, "GENE_B": 0.333},
  "mdi_uncertainty": {"GENE_A": [-0.8, -0.4], "GENE_B": [-0.1, 0.4]},
  "psi_uncertainty": {"GENE_A": [0.5, 1.1], "GENE_B": [0.1, 0.6]},
  "interpretation": {
    "supportive": "GENE_A shows MDI < -0.5 with uncertainty excluding zero and PSI > 0.5 with uncertainty excluding zero, supporting pathway-specific feed-forward signaling.",
    "adverse": "GENE_B shows MDI near zero, adverse to a simple feed-forward interpretation.",
    "inconclusive": "No genes have undefined MDI or PSI."
  },
  "donor_groups": ["donor1", "donor2"],
  "sample_count": 33,
  "gene_count": 2
}
EOF

cat > /workspace/analysis_summary.txt << 'EOF'
Analysis Summary
================
Genes analyzed: 2
Genes with defined MDI: 2
Genes with defined PSI: 2
Overall interpretation: GENE_A supports pathway-specific feed-forward signaling (MDI < -0.5, PSI > 0.5 with uncertainty excluding zero). GENE_B is adverse to a simple feed-forward interpretation (MDI near zero).
EOF

echo "Good fixture created successfully."
