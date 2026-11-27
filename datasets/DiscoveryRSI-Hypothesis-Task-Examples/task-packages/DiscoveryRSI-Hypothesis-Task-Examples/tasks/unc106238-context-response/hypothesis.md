# Context-dependent transcript response to UNC106238 in macrophage-fibroblast coculture: an identifiable, composition-robust contrast

## Scientific opening and unresolved claim

The D2-T1 seed asks whether an intervention-associated transcript response depends on macrophage-fibroblast context. This is clinically important because a transcript program that appears responsive in a bulk or isolated cell preparation may not represent a useful therapeutic target when the relevant cell-cell context is absent or altered. If the response is context-dependent, prioritization should condition on the cellular microenvironment rather than rank targets by overall expression change.

The strongest claim currently supported by the available data is that E-MTAB-8316 contains a verified, donor-aware macrophage-condition contrast: six monocyte donors (four FLS donor clusters) measured under "none" and "UNC106238" conditions, with twelve condition samples total. The unresolved claim is narrower and falsifiable: the magnitude or direction of a prespecified intervention-associated transcript response differs between macrophage-present and macrophage-absent fibroblast contexts in a way that is not explained by donor, condition, batch, or sample-composition differences.

This is a hypothesis, not an established finding. The available data support a donor-aware exploratory comparison, not a claim of direct target causality.

## Prespecified intervention-associated transcript program

The intervention-associated transcript program is defined from the UNC106238 vs. none contrast in E-MTAB-8316 with the following prespecified selection criteria:

- |mean log2 fold change| >= 1.0 across the six monocyte donors
- Sign consistency >= 5/6 donors
- Feature overlap with the macrophage-condition contrast (shared gene identifiers)

These criteria are applied before any context comparison to avoid post-hoc selection bias. The program is a medication-associated transcript response, not a direct target action.

## Donor-aware pseudobulk analysis

The donor-aware pseudobulk analysis handles the nested structure of the data:

- Four FLS donor clusters
- Six nested monocyte donors
- Twelve condition samples (none vs. UNC106238)

Within each donor/condition, repeated context measurements are averaged before paired exploratory inference. Donor-level inference is used to account for the nested structure. The analysis is exploratory and does not claim direct target causality.

## Composition-robustness check

A composition-robustness check uses ridge regression with donor, condition, batch, and composition covariates. This check tests whether the context contrast is robust to sample-composition differences. The ridge regression is a sensitivity analysis, not a causal model.

## Bounded data-bound diagnostic

A bounded data-bound diagnostic tests whether the context contrast is supported by the available data without claiming direct target causality. The diagnostic:

1. Defines the prespecified intervention-associated transcript program from the UNC106238 vs. none contrast
2. Tests whether the magnitude or direction of the program differs between macrophage-present and macrophage-absent fibroblast contexts
3. Accounts for donor, condition, batch, and sample-composition differences
4. Reports supportive, adverse, and inconclusive outcomes

The diagnostic is a hypothesis test, not a confirmatory analysis. It does not establish direct target causality.

## Competing explanations

- Donor-level variation: The context contrast may be driven by a subset of donors rather than a general effect
- Condition-level variation: The context contrast may be driven by condition-specific effects rather than a general effect
- Batch-level variation: The context contrast may be driven by batch effects rather than a general effect
- Sample-composition differences: The context contrast may be driven by differences in sample composition rather than a general effect

## Method comparison

The baseline method is a donor-aware pseudobulk analysis with within-donor averaging and donor-level inference. The learned alternative is a ridge regression model with donor, condition, batch, and composition covariates. The ridge regression could reveal whether the context contrast is robust to sample-composition differences, which the baseline method loses.

The ridge regression is a sensitivity analysis, not a causal model. It does not establish direct target causality.

## Falsification criteria

The hypothesis is falsified if:

- The context contrast is not supported by the available data
- The context contrast is driven by donor, condition, batch, or sample-composition differences
- The context contrast is not robust to sample-composition differences

## Key references

[K1] The D2-T1 seed asks whether an intervention-associated transcript response depends on macrophage-fibroblast context. This is clinically important because a transcript program that appears responsive in a bulk or isolated cell preparation may not represent a useful therapeutic target when the relevant cell-cell context is absent or altered.

[K2] The strongest claim currently supported by the available data is that E-MTAB-8316 contains a verified, donor-aware macrophage-condition contrast: six monocyte donors (four FLS donor clusters) measured under "none" and "UNC106238" conditions, with twelve condition samples total.

[K3] The unresolved claim is narrower and falsifiable: the magnitude or direction of a prespecified intervention-associated transcript response differs between macrophage-present and macrophage-absent fibroblast contexts in a way that is not explained by donor, condition, batch, or sample-composition differences.
