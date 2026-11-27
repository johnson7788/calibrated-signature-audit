# Directional macrophage–fibroblast signaling: perturbation-based directionality test

## Scientific question

In fibroblast–macrophage cocultures, does macrophage-derived signaling drive a directional, feed-forward pro-fibrotic response in fibroblasts, or is the observed co-expression pattern better explained by a reciprocal or fibroblast-initiated circuit?

## Clinical importance

Fibrosis is a leading cause of organ failure, and the direction of cell-cell communication determines whether anti-inflammatory treatment (targeting macrophages) or fibroblast-targeted intervention is the appropriate first-line strategy. A macrophage-initiated feed-forward mechanism would prioritize macrophage depletion or reprogramming; a fibroblast-initiated or reciprocal mechanism would prioritize fibroblast-intrinsic targets. Distinguishing these two mechanisms is a consequential clinical decision that current cross-sectional expression data cannot resolve.

## Evidence already supported and unresolved claim

The available E-MTAB-8873 coculture data include fibroblast-only and macrophage-fibroblast conditions, with paired macrophage-positive and macrophage-negative samples and inhibitor conditions. The E-MTAB-8316 data include four FLS donor clusters with six nested monocyte donors and twelve condition samples. The GSE95588 coculture data provide additional paired condition comparisons.

The existing evidence shows that macrophage presence is associated with pro-fibrotic gene expression in fibroblasts, but does not establish the direction of signaling. The remission literature (NatMed_remission) describes persistent versus resolving fibrotic states in vivo but does not establish which intracellular circuit in fibroblasts is responsible for the directional response.

The unresolved claim is: does macrophage-derived signaling (e.g., TGF-beta, IL-1, or other cytokines) drive a feed-forward pro-fibrotic response in fibroblasts, or is the observed co-expression pattern better explained by a reciprocal or fibroblast-initiated circuit?

## Competing explanations

1. **Macrophage-initiated feed-forward mechanism**: Macrophage-derived signals (e.g., TGF-beta, IL-1) drive pro-fibrotic gene expression in fibroblasts. This would be supported by a temporal sequence where macrophage signals precede fibroblast response, and by inhibitor experiments that block the macrophage signal and reduce fibroblast pro-fibrotic expression.

2. **Reciprocal mechanism**: Macrophages and fibroblasts engage in a reciprocal signaling loop where each cell type drives the other's pro-fibrotic state. This would be supported by evidence that fibroblast-derived signals also drive macrophage pro-fibrotic state, and by inhibitor experiments that block either signal and reduce both cell types' pro-fibrotic expression.

3. **Fibroblast-initiated mechanism**: Fibroblasts initiate the pro-fibrotic response, and macrophages are recruited or activated as a consequence. This would be supported by evidence that fibroblast pro-fibrotic expression precedes macrophage activation, and by inhibitor experiments that block fibroblast signals and reduce macrophage pro-fibrotic state.

## Concrete estimand: Directionality Index (DI)

The directionality index is a quantitative measure that captures the asymmetry in signaling between macrophages and fibroblasts. It is defined as:

**DI = (Δ_FLS | macrophage perturbation) / (Δ_FLS | fibroblast perturbation)**

where:
- Δ_FLS | macrophage perturbation is the change in fibroblast pro-fibrotic gene expression when macrophage-derived signals are perturbed (e.g., macrophage-positive vs. macrophage-negative, or macrophage inhibitor vs. no inhibitor).
- Δ_FLS | fibroblast perturbation is the change in fibroblast pro-fibrotic gene expression when fibroblast-derived signals are perturbed (e.g., fibroblast inhibitor vs. no inhibitor, if available).

A DI > 1 indicates that macrophage-derived signals have a stronger effect on fibroblast pro-fibrotic expression than fibroblast-derived signals, supporting a feed-forward mechanism. A DI < 1 indicates the opposite, supporting a reciprocal or fibroblast-initiated mechanism. A DI ≈ 1 suggests symmetric signaling, consistent with a reciprocal mechanism.

### Practical implementation

In the available E-MTAB-8873 data, the directionality index can be estimated using the following paired comparisons:

1. **Macrophage-positive vs. macrophage-negative**: Compare fibroblast pro-fibrotic gene expression in macrophage-positive (Mpos) vs. macrophage-negative (Mneg) coculture conditions. This captures the effect of macrophage presence on fibroblast pro-fibrotic expression.

2. **Macrophage inhibitor vs. no inhibitor**: Compare fibroblast pro-fibrotic gene expression in macrophage inhibitor (Inhibitor) vs. no inhibitor (none) conditions. This captures the effect of blocking macrophage-derived signals on fibroblast pro-fibrotic expression.

3. **Fibroblast inhibitor vs. no inhibitor** (if available): Compare fibroblast pro-fibrotic gene expression in fibroblast inhibitor vs. no inhibitor conditions. This captures the effect of blocking fibroblast-derived signals on fibroblast pro-fibrotic expression.

The directionality index is then calculated as the ratio of the macrophage perturbation effect to the fibroblast perturbation effect. If fibroblast inhibitor data are not available, the directionality index can be estimated using the macrophage-positive vs. macrophage-negative comparison as a proxy for the macrophage perturbation effect, and the macrophage inhibitor vs. no inhibitor comparison as a proxy for the fibroblast perturbation effect (under the assumption that the inhibitor specifically blocks macrophage-derived signals).

### Statistical analysis

The directionality index is estimated using a donor-aware linear model that accounts for the paired nature of the data:

**Model**: Δ_FLS ~ macrophage_perturbation + fibroblast_perturbation + donor + condition

where:
- Δ_FLS is the change in fibroblast pro-fibrotic gene expression (e.g., log2 fold change).
- macrophage_perturbation is a binary variable indicating whether macrophage-derived signals were perturbed (e.g., macrophage-positive vs. macrophage-negative, or macrophage inhibitor vs. no inhibitor).
- fibroblast_perturbation is a binary variable indicating whether fibroblast-derived signals were perturbed (e.g., fibroblast inhibitor vs. no inhibitor, if available).
- donor is a fixed effect accounting for donor-specific variation.
- condition is a fixed effect accounting for condition-specific variation.

The directionality index is then calculated as the ratio of the coefficient for macrophage_perturbation to the coefficient for fibroblast_perturbation.

## Discriminating test

The discriminating test is a perturbation experiment using the available inhibitor conditions in E-MTAB-8873. Specifically:

1. **Macrophage signal inhibition**: Block macrophage-derived signals (e.g., TGF-beta, IL-1) and measure the effect on fibroblast pro-fibrotic gene expression. If the fibroblast pro-fibrotic response is reduced, this supports the macrophage-initiated feed-forward mechanism.

2. **Fibroblast signal inhibition**: Block fibroblast-derived signals and measure the effect on macrophage pro-fibrotic state. If the macrophage pro-fibrotic state is reduced, this supports the reciprocal or fibroblast-initiated mechanism.

3. **Temporal sequence**: Use the paired macrophage-positive and macrophage-negative samples to establish a temporal sequence. If macrophage signals precede fibroblast response, this supports the macrophage-initiated feed-forward mechanism.

## Data bindings

- **E-MTAB-8873**: `/data/prepared/E-MTAB-8873.counts.tsv.gz`; metadata `/data/prepared/E-MTAB-8873.design.json`
  - Targeted assay; 445 measured feature columns in these retrieved matrices.
  - Preserve transcript identifiers. Unmeasured genes are unavailable.
  - Pseudobulk summarizes each recorded FLS/coculture sample.
  - Multiple contributing or reused donors require explicit dependence modeling; ordinary donor t-test disabled.

- **E-MTAB-8316**: `/data/prepared/E-MTAB-8316.counts.tsv.gz`; metadata `/data/prepared/E-MTAB-8316.design.json`
  - Four FLS donor clusters, six nested monocyte donors, twelve condition samples.
  - Average repeated context measurements within each donor/condition before paired exploratory inference.
  - No twelve-independent-donor claim.
  - Metadata cell-type labels and experimental readout must be reconciled with protocol before cell-specific claims.

- **GSE95588_coculture_htseq_counts**: `/data/prepared/GSE95588_coculture_htseq_counts.counts.tsv.gz`; metadata `/data/prepared/GSE95588_coculture_htseq_counts.design.json`
  - Duplicate and date-like gene labels retain distinct source rows; resolve their feature-map records before naming targets.
  - No guessed correction or count merging.
  - Expression exploration enabled; donor-aware inferential comparisons need verified column-to-GSM/donor mapping.
  - Coculture r1/r2 includes earlier GSE57723 data and cannot count as independent validation of that study.

## Supportive, adverse, and inconclusive outcomes

- **Supportive**: Macrophage signal inhibition reduces fibroblast pro-fibrotic gene expression, and the temporal sequence shows macrophage signals preceding fibroblast response. This supports the macrophage-initiated feed-forward mechanism.

- **Adverse**: Fibroblast signal inhibition reduces macrophage pro-fibrotic state, and the temporal sequence shows fibroblast signals preceding macrophage activation. This supports the reciprocal or fibroblast-initiated mechanism.

- **Inconclusive**: Neither inhibitor experiment produces a clear effect, or the temporal sequence is ambiguous. This would require additional data (e.g., single-cell time-series, perturbation experiments with more specific inhibitors) to resolve the direction of signaling.

## Method comparison

- **Simple baseline**: Donor-aware cell-type analysis using the available paired condition comparisons. This would establish the association between macrophage presence and fibroblast pro-fibrotic expression, but would not resolve the direction of signaling.

- **Learned/mechanistic alternative**: A perturbation experiment using the available inhibitor conditions in E-MTAB-8873. This would test the direction of signaling by blocking specific signals and measuring the effect on the other cell type's pro-fibrotic state. This alternative could reveal the direction of signaling, which the baseline loses.

## Selection reason

The perturbation experiment is the scientifically appropriate method for this question because it directly tests the direction of signaling, which is the unresolved claim. The simple baseline would not resolve the direction of signaling and would therefore not answer the question.

## Actual scientific deliverable

The actual scientific deliverable is a perturbation experiment using the available inhibitor conditions in E-MTAB-8873. The outputs that establish its completion are:

1. A table of fibroblast pro-fibrotic gene expression under macrophage signal inhibition.
2. A table of macrophage pro-fibrotic state under fibroblast signal inhibition.
3. A temporal sequence analysis showing the order of macrophage and fibroblast signaling.

## Alternatives not chosen

- **Single-cell time-series**: This would provide a more detailed temporal sequence, but is not available in the current datasets. It would require additional data acquisition.

- **More specific inhibitors**: This would provide a more specific test of the direction of signaling, but is not available in the current datasets. It would require additional data acquisition.

## Evidence that would justify revisiting deferred branches

- If the perturbation experiment produces inconclusive results, a single-cell time-series experiment would be justified to resolve the direction of signaling.
- If the perturbation experiment produces adverse results (supporting the reciprocal or fibroblast-initiated mechanism), a more specific inhibitor experiment would be justified to confirm the direction of signaling.

## Key references

[K1] Mosallanejad K, Hubeau C, Schwartz Sterman A, Tan Y. Macrophages and the Tissue Repair Circuit: Homeostasis, Autoimmune Diseases, and Resolution-Based Therapeutic Strategies. Cells. 2026;15(15):1412. doi:10.3390/cells15151412. PMC13464986.
- Claim: This review describes the bi-directional crosstalk between macrophages and heterogeneous fibroblast populations, and how sustained activation under inflammatory conditions drives maladaptive repair and fibrotic remodeling.
- Contribution: This proposal adds a concrete perturbation experiment to test the direction of signaling in fibroblast-macrophage cocultures, which the review does not establish.
- Limitation: This is a review article and does not provide original experimental data on the direction of signaling in fibroblast-macrophage cocultures.
- Locator: Abstract and Introduction.
- Inspection: excerpt_only.

[K2] Fatehi Hassanabad A, Sinha S, Jaffer A, et al. Human pericardial macrophages suppress cardiac fibrosis through cystatin C signaling after myocardial infarction. JCI Insight. 2026;11(17):e202383. doi:10.1172/jci.insight.202383. PMC13564072.
- Claim: This study establishes that human pericardial immune cells directly inhibit cardiac fibroblast fibrotic activity, and that fibronectin-expressing human pericardial macrophages are the primary driver of the pericardial antifibrotic actions through the release of cystatin C.
- Contribution: This proposal adds a concrete perturbation experiment to test the direction of signaling in fibroblast-macrophage cocultures, which the study does not establish.
- Limitation: This study focuses on pericardial macrophages and cardiac fibrosis, and does not establish the direction of signaling in fibroblast-macrophage cocultures.
- Locator: Abstract and Introduction.
- Inspection: excerpt_only.

[K3] Huang J, Yin X, Shi X, et al. Megakaryocytes in myelofibrosis: mechanisms of fibrotic niche remodeling and therapeutic implications. Biomark Res. 2026;14(1):128. doi:10.1186/s40364-026-01003-0. PMC13625257.
- Claim: This review synthesizes evidence linking abnormal megakaryocyte biology to fibrotic progression, and describes how megakaryocytes release or activate TGF-beta1, platelet factor 4, and other profibrotic mediators that interact with stromal, immune, and endothelial cells.
- Contribution: This proposal adds a concrete perturbation experiment to test the direction of signaling in fibroblast-macrophage cocultures, which the review does not establish.
- Limitation: This is a review article and does not provide original experimental data on the direction of signaling in fibroblast-macrophage cocultures.
- Locator: Abstract.
- Inspection: excerpt_only.
