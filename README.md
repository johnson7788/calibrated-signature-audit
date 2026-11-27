# calibrated-signature-audit

**Auditing omics signature claims — with a calibrated null.**

This repository accompanies the preprint:

> Guo Z. *Calibrating signature audits: nominal tests understate false-positive rates by up to five-fold.*
> Preprint: bioRxiv (submitted) · PDF: [paper/manuscript.pdf](paper/manuscript.pdf) · Data: [Hugging Face](https://huggingface.co/datasets/johnson/calibrated-signature-audit)

**Key finding.** At a nominal 5% level, ordinary signature audits declared **12.4%** and **24.6%** of random 100-gene signatures "robust" in two colorectal cancer cohorts (2.5–4.9× inflation). A size-matched **gene-set permutation calibration** restores false-positive rates to **4.0–6.4%**, while all 36 real signatures remain significant.

---

## Repository layout

```
pilot/                  # the audit toolkit (main deliverable)
├── cli.py              # command-line interface
├── audit.py            # audit engine (signature/scan, LOO, covariates, alpha sweep)
├── permutation.py      # gene-set permutation calibration (see paper)
├── split_half.py       # half-sample protocol
├── replication_matrix.py / cross_signature.py
├── prepare_microarray.py
├── SOP.md              # standard operating procedure
├── datasets.json       # registered datasets
├── data/               # processed matrices (small ones committed; see Data)
└── results/            # generated reports

paper/                  # manuscript, figures and supporting experiments
├── manuscript.md / .pdf
├── figures/            # 300 dpi figures
├── exp_null.py         # nominal false-positive rate experiment
├── exp_calibrated.py   # permutation calibration experiment
├── exp_realcal.py      # real-signature survival check
└── SUBMISSION_CHECKLIST.md

closed_loop/            # DiscoveryRSI-style executable research loop (supporting work)
src/, tests/            # upstream harness + tests
datasets/               # third-party task packages (see THIRD_PARTY_NOTICES.md)
docs/                   # upstream README backup
```

## Quick start

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e ".[test]" numpy pandas scipy scikit-learn statsmodels matplotlib
.venv/bin/pytest -q                         # 26 passed

# list registered datasets
.venv/bin/python -m pilot.cli datasets

# audit a claim (example: GSE50760 signatures)
.venv/bin/python -m pilot.cli audit --claims pilot/claims.gse50760.json --out /tmp/report.md

# regenerate every report in this repository (~20 s)
bash pilot/run_all.sh
```

Reproducing the paper's calibration numbers:

```bash
PYTHONPATH=. .venv/bin/python paper/exp_null.py        # nominal FPR (Table 1, left)
PYTHONPATH=. .venv/bin/python paper/exp_calibrated.py  # permutation FPR (Table 1, right)
PYTHONPATH=. .venv/bin/python paper/exp_realcal.py     # real signatures survive
MPLCONFIGDIR=/tmp/mpl .venv/bin/python paper/make_figures.py
```

## Data

Processed matrices, claim specifications, figures and the PDF are archived at
**Hugging Face: https://huggingface.co/datasets/johnson/calibrated-signature-audit**

Original data: NCBI GEO [GSE50760](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE50760),
[GSE95132](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE95132),
[GSE110224](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110224).
Raw files are not redistributed; processing scripts are in `pilot/prepare_*.py` and the dataset card.

## License

Our code (`pilot/`, `paper/`, `closed_loop/`) is released under the MIT License (see [LICENSE](LICENSE)).
Upstream components (`src/discovery_rsi/`, `datasets/`) are derived from
[Gen-Verse/DiscoveryRSI](https://github.com/Gen-Verse/DiscoveryRSI) under Apache-2.0;
see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Public datasets retain their original terms.

## Citation

```bibtex
@article{guo2026calibrating,
  title   = {Calibrating signature audits: nominal tests understate false-positive rates by up to five-fold},
  author  = {Guo, Zhicai},
  year    = {2026},
  note    = {Preprint},
  url     = {https://github.com/johnson7788/calibrated-signature-audit}
}
```

See [CITATION.cff](CITATION.cff) for machine-readable metadata.

## Acknowledgements

This work builds on the DiscoveryRSI harness and task packages
(Gen-Verse/DiscoveryRSI), and on public data from NCBI GEO and Expression Atlas.