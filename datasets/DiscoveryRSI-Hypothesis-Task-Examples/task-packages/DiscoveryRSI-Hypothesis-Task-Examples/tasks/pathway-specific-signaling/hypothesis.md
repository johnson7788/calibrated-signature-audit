# Pathway-specific directional macrophage–fibroblast signaling: resolving feed-forward versus nonspecific coculture

## Question

In human synovial fibroblast–macrophage cocultures, is the macrophage-associated fibroblast response driven by a specific macrophage-derived pro-fibrotic pathway (TNF, IL-1, or IL-6 signaling), or is it a nonspecific consequence of coculture composition, measurement, or donor selection?

## Clinical importance

The direction and mediator specificity of macrophage–fibroblast communication determine whether an early intervention should target macrophage signaling, fibroblast-intrinsic fibrotic programs, or both. In rheumatoid arthritis, persistent synovial fibrosis and tissue remodeling can limit function and response to therapy. A macrophage-initiated feed-forward circuit would favor strategies that block or reprogram macrophage-derived signals before fibroblast activation becomes self-sustaining. A reciprocal or fibroblast-initiated circuit would favor fibroblast-targeted intervention and would caution against assuming that macrophage depletion alone is sufficient. This is a consequential treatment-selection question, but the present experiment is an in vitro mechanistic proxy, not a clinical trial.

## Evidence already supported and unresolved claim

The inspected E-MTAB-8873 design contains 33 recorded fibroblast/coculture samples across 26 factor-table groups. The available growth conditions are `not co-cultured` (6 samples), `co-cultured with MerTK/CD206neg macrophages` (11), `co-cultured with MerTK/CD206pos macrophages` (13), and `co-cultured with MerTK/CD206neg and MerTK/CD206pos macrophages` (3). Available stimuli are `none` (23), `macrophages pre-treated with MerTK inhibitor` (5), and `macrophages pre-treated with lipopolysaccharide` (5). The design includes 16 donor labels, but some coculture samples contain two contributing donors and are marked `requires_contributing_donor_model`; therefore donor labels are not independent experimental units.

The available evidence supports only that macrophage presence and macrophage perturbation are associated with fibroblast expression changes. It does not yet establish which cell initiates the pro-fibrotic circuit, whether the signal is pathway-specific, or whether the observed directionality is robust to donor-specific baselines and alternative explanations. The unresolved claim is whether macrophage perturbation produces a reproducible, donor-aware fibroblast response that is asymmetric relative to the available reciprocal/feedback contrasts, rather than whether a fibroblast-initiated circuit is directly demonstrated.

## Competing explanations

1. **Macrophage-initiated feed-forward**: Macrophage-derived signals drive fibroblast pro-fibrotic expression. Blocking or changing macrophage signaling should change fibroblast expression in a reproducible direction, while fibroblast-only samples provide a stable baseline.
2. **Reciprocal loop**: Fibroblast and macrophage signals mutually reinforce one another. The available data can show asymmetry or lack of a clean unidirectional contrast, but cannot directly show fibroblast-to-macrophage causation because the measured matrix is fibroblast/coculture.
3. **Fibroblast-initiated or non-causal association**: Fibroblast expression may reflect fibroblast-intrinsic state, donor background, or technical variation rather than macrophage signaling. A donor-aware baseline and negative controls are needed before interpreting the perturbation contrast.
4. **Nonspecific coculture effect**: The observed fibroblast response may reflect general coculture conditions, composition, or measurement artifacts rather than a specific macrophage-derived pathway. A pathway-specific perturbation test is needed to distinguish this from a pathway-specific feed-forward signal.

## Executable directionality estimand: the macrophage-directionality index (MDI)

Because no fibroblast-inhibitor or fibroblast-specific perturbation condition is present in E-MTAB-8873, the original DI denominator is unavailable. We therefore define a **macrophage-directionality index (MDI)** rather than pretending to estimate a fibroblast-perturbation denominator.

### Exact conditions and samples

The MDI is computed from four condition groups, each defined by the intersection of `growth_condition` and `stimulus` in the E-MTAB-8873 design:

| Group | growth_condition | stimulus | Samples |
|-------|-----------------|----------|---------|
| FLS_only | `not co-cultured` | `none` | 6 |
| Mpos | `co-cultured with MerTK/CD206pos macrophages` | `none` | 13 |
| Mpos_Inh | `co-cultured with MerTK/CD206pos macrophages` | `macrophages pre-treated with MerTK inhibitor` | 5 |
| Mneg | `co-cultured with MerTK/CD206neg macrophages` | `none` | 11 |

The mixed condition (`co-cultured with MerTK/CD206neg and MerTK/CD206pos macrophages`, 3 samples) and LPS conditions (5 samples) are retained as sensitivity analyses, not primary contrasts.

### Estimand definition

For each fibroblast gene or gene module `g`, define:

**Macrophage-presence effect** (the feed-forward signal):
`E_presence(g) = mean_g(Mpos) - mean_g(FLS_only)`

**Macrophage-perturbation effect** (the inhibitor response):
`E_inhibitor(g) = mean_g(Mpos_Inh) - mean_g(Mpos)`

**Macrophage-directionality index**:
`MDI(g) = E_inhibitor(g) / E_presence(g)`

This index asks whether perturbing macrophage signaling reverses or attenuates the fibroblast response induced by macrophage presence. An MDI near zero suggests that the macrophage-presence response is not reproduced or reversed by the available macrophage perturbation; a negative MDI suggests attenuation/reversal of the macrophage-associated fibroblast response; a positive MDI suggests that the inhibitor changes fibroblast expression in the same direction as macrophage presence, which is adverse to a simple feed-forward interpretation. The index is undefined when the presence effect is near zero and must be reported gene-by-gene with uncertainty, not collapsed into an unsupported aggregate.

The full directional DI requiring a fibroblast perturbation contrast is explicitly deferred: it would require a fibroblast inhibitor, fibroblast-specific knockdown, or a fibroblast-to-macrophage readout. The MDI is therefore a bounded macrophage-perturbation test, not direct proof of feed-forward causality.

### Interpretation thresholds

- **MDI < -0.5 with uncertainty excluding zero**: Strong evidence for macrophage-initiated feed-forward signaling. The inhibitor attenuates or reverses the macrophage-presence response.
- **MDI near zero (-0.2 to 0.2) with uncertainty excluding a large negative value**: The macrophage-presence response is not reproduced by the inhibitor. This is adverse to a simple feed-forward interpretation.
- **MDI > 0.5**: The inhibitor changes fibroblast expression in the same direction as macrophage presence. This is strongly adverse to a feed-forward interpretation.
- **MDI undefined (E_presence near zero)**: The macrophage-presence effect is too small to compute a meaningful directionality index. This is inconclusive.

## Pathway-specific perturbation test

The MDI alone cannot distinguish a pathway-specific feed-forward signal from a nonspecific coculture effect. We therefore add a pathway-specific perturbation test that uses the LPS condition as an inflammatory perturbation and compares the direction and magnitude of the LPS effect with the MerTK inhibitor effect.

### LPS perturbation contrast

The LPS condition (`macrophages pre-treated with lipopolysaccharide`, 5 samples) is an inflammatory perturbation that should activate macrophage-derived pro-inflammatory and pro-fibrotic pathways (TNF, IL-1, IL-6). If the macrophage-presence response is driven by a specific macrophage-derived pathway, the LPS perturbation should produce a fibroblast response that is directionally coherent with the macrophage-presence response and the MerTK inhibitor effect. If the macrophage-presence response is a nonspecific coculture effect, the LPS perturbation should produce a fibroblast response that is not directionally coherent with the macrophage-presence response or the MerTK inhibitor effect.

### Pathway-specificity index (PSI)

For each fibroblast gene or gene module `g`, define:

**LPS perturbation effect**:
`E_LPS(g) = mean_g(Mpos_LPS) - mean_g(Mpos)`

**Pathway-specificity index**:
`PSI(g) = E_LPS(g) / E_presence(g)`

This index asks whether the LPS perturbation produces a fibroblast response that is directionally coherent with the macrophage-presence response. A positive PSI suggests that LPS activates the same fibroblast response as macrophage presence, which is consistent with a pathway-specific feed-forward signal. A negative PSI suggests that LPS produces a fibroblast response in the opposite direction to macrophage presence, which is adverse to a pathway-specific feed-forward interpretation. A PSI near zero suggests that LPS does not reproduce the macrophage-presence response, which is adverse to a pathway-specific feed-forward interpretation.

### Pathway-specificity thresholds

- **PSI > 0.5 with uncertainty excluding zero**: Strong evidence for a pathway-specific feed-forward signal. The LPS perturbation produces a fibroblast response that is directionally coherent with the macrophage-presence response.
- **PSI near zero (-0.2 to 0.2) with uncertainty excluding a large positive value**: The LPS perturbation does not reproduce the macrophage-presence response. This is adverse to a pathway-specific feed-forward interpretation.
- **PSI < -0.5**: The LPS perturbation produces a fibroblast response in the opposite direction to macrophage presence. This is strongly adverse to a pathway-specific feed-forward interpretation.
- **PSI undefined (E_presence near zero)**: The macrophage-presence effect is too small to compute a meaningful pathway-specificity index. This is inconclusive.

### Combined pathway-specificity and directionality test

The pathway-specificity and directionality test is a combined test that requires both the MDI and the PSI to be directionally coherent. A gene or module is considered pathway-specific and directionally coherent if:

1. **MDI < -0.5 with uncertainty excluding zero**: The MerTK inhibitor attenuates or reverses the macrophage-presence response.
2. **PSI > 0.5 with uncertainty excluding zero**: The LPS perturbation produces a fibroblast response that is directionally coherent with the macrophage-presence response.

If both conditions are met, the evidence supports a pathway-specific feed-forward signal. If only one condition is met, the evidence is inconclusive and requires further perturbation or a time course. If neither condition is met, the evidence is adverse to a pathway-specific feed-forward interpretation.

## Population, variables, and temporal boundaries

- **Population**: human synovial fibroblast/coculture samples from E-MTAB-8873, restricted to samples with a recorded `donor_id`, `condition`, and `treatment`.
- **Baseline**: `condition = "not co-cultured"` and `treatment = "none"`.
- **Macrophage-positive**: `condition = "co-cultured with MerTK/CD206pos macrophages"` and `treatment = "none"`.
- **Macrophage-negative**: `condition = "co-cultured with MerTK/CD206neg macrophages"` and `treatment = "none"`.
- **Macrophage inhibitor**: `condition = "co-cultured with MerTK/CD206pos macrophages"` and `treatment = "macrophages pre-treated with MerTK inhibitor"`.
- **LPS condition**: `treatment = "macrophages pre-treated with lipopolysaccharide"` is retained as an exploratory inflammatory perturbation, not as a replacement for the inhibitor contrast.
- **Join key**: `sample_id` in the design file to the sample columns of the count matrix.
- **Time**: the design file records no time course. The experiment is a static coculture comparison; no temporal sequence claim is permitted.

## Method comparison

### Baseline: donor-aware paired linear model

Fit, for each fibroblast gene/module, a linear model with the observed log-expression as outcome:

`y ~ condition + treatment + donor_group + sample_group`

where `donor_group` is a fixed effect for each contributing-donor combination and `sample_group` is a fixed effect for each recorded sample. The primary baseline estimands are the macrophage-positive versus fibroblast-only coefficient and the macrophage-positive inhibitor versus macrophage-positive none coefficient. Use donor-group-aware bootstrap or permutation within donor groups for uncertainty. This baseline tests whether the macrophage-associated fibroblast expression change is reproducible after accounting for donor and sample dependence.

**What the baseline reveals**: The baseline tells you whether the macrophage-presence effect and the inhibitor effect are statistically significant after accounting for donor and sample dependence. It does not tell you whether the two effects are directionally coherent with each other.

### Alternative: perturbation-based macrophage-directionality index

Fit the same donor-aware model, but estimate the two effect terms explicitly and calculate MDI for genes/modules with non-negligible presence effects. The alternative can additionally test the pattern across macrophage-positive, macrophage-negative, and mixed macrophage conditions, and compare inhibitor versus LPS perturbation patterns. It reveals whether the macrophage perturbation is directionally coherent with the macrophage-presence response, information that a single baseline coefficient loses.

**What the alternative reveals that the baseline loses**: The MDI captures the *ratio* of the inhibitor effect to the presence effect, which is a directionality measure that a single coefficient cannot provide. A gene can have a significant presence effect and a significant inhibitor effect in the baseline, but the MDI tells you whether the inhibitor *reverses* or *attenuates* the presence effect, which is the key question for distinguishing feed-forward from reciprocal signaling.

### Pathway-specific perturbation test

The pathway-specific perturbation test uses the LPS condition as an inflammatory perturbation and compares the direction and magnitude of the LPS effect with the MerTK inhibitor effect. The PSI captures the *ratio* of the LPS effect to the presence effect, which is a pathway-specificity measure that a single coefficient cannot provide. A gene can have a significant presence effect and a significant LPS effect in the baseline, but the PSI tells you whether the LPS *reproduces* or *reverses* the presence effect, which is the key question for distinguishing pathway-specific feed-forward from nonspecific coculture effects.

**What the pathway-specific test reveals that the baseline loses**: The PSI captures the *ratio* of the LPS effect to the presence effect, which is a pathway-specificity measure that a single coefficient cannot provide. A gene can have a significant presence effect and a significant LPS effect in the baseline, but the PSI tells you whether the LPS *reproduces* or *reverses* the presence effect, which is the key question for distinguishing pathway-specific feed-forward from nonspecific coculture effects.

### Why not a neural or high-dimensional model

The alternative is not a learned neural model. It is a mechanistically interpretable perturbation contrast. A neural or high-dimensional model would not resolve the missing fibroblast-perturbation contrast and could obscure the small, dependent sample structure. It is deferred because the question is a bounded perturbation comparison, not prediction.

### Resource and time budget

Both methods are CPU-only. The count matrix has 445 measured feature columns and 33 samples; after pseudobulk summarization, fitting per-gene linear models and donor-group-aware bootstrap uncertainty should take minutes on 2 CPUs and 8 GiB RAM. A complete exploratory analysis including module selection, MDI calculation, PSI calculation, and sensitivity checks is expected to complete in under 1 hour of managed compute. No GPU is required.

## Analysis and falsification

1. Pseudobulk each recorded sample and preserve source sample IDs.
2. Verify the design-to-count join and exclude samples without a valid donor label or condition.
3. Fit the donor-aware baseline for macrophage-positive versus fibroblast-only and inhibitor versus no-inhibitor contrasts.
4. Calculate MDI only for genes/modules with a prespecified minimum presence effect and report the denominator uncertainty.
5. Calculate PSI only for genes/modules with a prespecified minimum presence effect and report the denominator uncertainty.
6. Compare the direction and magnitude of the inhibitor effect with the presence effect, and inspect macrophage-negative and mixed conditions as sensitivity analyses.
7. Compare the direction and magnitude of the LPS effect with the presence effect, and inspect macrophage-negative and mixed conditions as sensitivity analyses.
8. Use donor-group-aware permutation/bootstrap uncertainty; do not treat 33 samples or 16 donor labels as independent.

### Supportive evidence

A reproducible macrophage-positive fibroblast response and a coherent attenuation/reversal under MerTK inhibition, with uncertainty excluding a null pattern for a prespecified fibroblast module. This would support a macrophage-perturbation-sensitive fibroblast response, not direct proof of feed-forward initiation.

### Adverse evidence

No reproducible macrophage-positive response, an inhibitor effect in the same direction as macrophage presence, or a pattern dominated by donor/sample artifacts. This would weaken the macrophage-initiated interpretation and would not establish fibroblast initiation.

### Inconclusive evidence

A small or unstable presence effect, undefined MDI for most genes, or conflicting patterns across macrophage-positive, macrophage-negative, mixed, inhibitor, and LPS conditions. This would require fibroblast-specific perturbation or a time course.

## Clinical decision framework

The result should inform the choice of an early intervention strategy in a future prospective study, not an immediate treatment recommendation.

- **If the prespecified fibroblast module shows a reproducible macrophage-positive response and inhibitor attenuation/reversal (MDI < -0.5 with uncertainty excluding zero)**, prioritize a macrophage-signaling-targeted intervention in a subsequent clinical or translational study.
- **If the inhibitor does not attenuate the response (MDI near zero), or if the response is similar across macrophage-positive, macrophage-negative, and mixed conditions**, prioritize a fibroblast-intrinsic intervention and do not assume macrophage targeting is sufficient.
- **If the result is inconclusive (MDI undefined for most genes, or conflicting patterns across conditions)**, defer the clinical decision and obtain fibroblast-specific perturbation or time-series data.

The threshold is not a universal numeric cutoff. It is a prespecified module-level effect with donor-aware uncertainty: the inhibitor effect must oppose or substantially reduce the macrophage-presence effect, and the uncertainty interval must not include a pattern compatible with no macrophage perturbation effect. A single gene or exploratory subgroup cannot trigger the decision.

## Data bindings

- **Counts**: `[source-host]/E-MTAB-8873.counts.tsv.gz`
- **Design**: `[source-host]/E-MTAB-8873.design.json`
- **Design columns**: `sample_id`, `donor_id`, `donor_status`, `condition`, `treatment`, `cell_type`, `tissue`, `age`, `sex`, `cells`, and `source_metadata`.
- **Count columns**: transcript identifiers and measured expression values; only the 445 measured feature columns are available.
- **Join**: `sample_id` from design to sample columns in counts.
- **Limitation**: targeted panel; unmeasured genes are unavailable. Multiple-contributing donors require dependence modeling. No time course is recorded.

## Key references

[K1] Feng M, Chen H, Liao L, Huang D, Shen J, Xiao L, Lu Q, Xie P. Cellular crosstalk and signaling networks in the rheumatoid arthritis synovial microenvironment. Int J Biol Sci. 2026. doi:10.1186/s12967-026-08482-7.
- Supports the biological context of macrophage-fibroblast crosstalk in the rheumatoid arthritis synovial microenvironment. It describes how cellular interactions drive RA along a pathological continuum but does not establish the direction of signaling in a specific coculture dataset.

[K2] Fatehi Hassanabad A, Sinha S, Jaffer A, et al. Human pericardial macrophages suppress cardiac fibrosis through cystatin C signaling after myocardial infarction. JCI Insight. 2026;11(17):e202383. doi:10.1172/jci.insight.202383.
- Provides evidence that macrophage-derived signals can directly modulate fibroblast fibrotic activity in a tissue-specific context. It bounds the claim by showing that macrophage effects are context- and mediator-specific, not a universal feed-forward rule.

[K3] Huang J, Yin X, Shi X, et al. Megakaryocytes in myelofibrosis: mechanisms of fibrotic niche remodeling and therapeutic implications. Biomark Res. 2026;14(1):128. doi:10.1186/s40364-026-01003-0.
- Illustrates how non-fibroblast cells can release profibrotic mediators that interact with stromal cells. It is a competing context for interpreting macrophage-derived signals and does not establish macrophage-fibroblast directionality in rheumatoid synovium.
