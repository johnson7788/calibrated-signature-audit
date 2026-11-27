# Third-party notices

This repository contains components derived from third-party projects and public datasets.

## Gen-Verse/DiscoveryRSI (Apache-2.0)

- `src/discovery_rsi/` — the DiscoveryRSI harness (model-agnostic propose/critique/select/retain loop).
- `datasets/DiscoveryRSI-Hypothesis-Task-Examples/` — task packages and examples.
- `datasets/DiscoveryRSI-27B-modelcard/` — model card reference.

Upstream repository: <https://github.com/Gen-Verse/DiscoveryRSI>

These components are licensed under the Apache License, Version 2.0
(<https://www.apache.org/licenses/LICENSE-2.0>). The full license text is available at the
upstream repository (`LICENSE`). Modifications and additions made in this repository are
released under the MIT License (see the root `LICENSE`).

## Public datasets

- **GSE50760**, **GSE95132**, **GSE110224** — NCBI Gene Expression Omnibus (GEO).
  Original data remain subject to the GEO and submitter terms. Processed matrices
  redistributed here are derived from public files; see the dataset card for provenance.
- **Expression Atlas** differential-expression export for GSE50760 — EMBL-EBI.

## Tooling

- Python packages: numpy, pandas, scipy, scikit-learn, statsmodels, matplotlib, markdown,
  huggingface_hub — under their respective open-source licenses.