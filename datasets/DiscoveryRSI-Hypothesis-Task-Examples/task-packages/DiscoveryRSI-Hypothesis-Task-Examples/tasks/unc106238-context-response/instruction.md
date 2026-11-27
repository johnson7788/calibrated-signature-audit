# Context-dependent transcript response to UNC106238 in macrophage-fibroblast coculture

## Scientific question and claim boundary

Test whether the magnitude or direction of a prespecified intervention-associated transcript response differs between macrophage-present and macrophage-absent fibroblast contexts in a way that is not explained by donor, condition, batch, or sample-composition differences. The data are from E-MTAB-8316, a donor-aware exploratory contrast with six monocyte donors nested within four FLS donor clusters, measured under `none` and `UNC106238` conditions. This is a hypothesis, not an established finding. A medication-associated transcript response is not direct evidence of target causality.

The strongest claim currently supported by the available data is that E-MTAB-8316 contains a verified, donor-aware macrophage-condition contrast with twelve condition samples total. The unresolved claim is narrower: the context contrast is not explained by donor, condition, batch, or composition differences.

## Required computation

1. Read the prepared counts and design files at the exact bound paths below. The counts file is a tab-separated gzip file with a `feature` column followed by sample columns. The design file is a JSON list of sample metadata objects.
2. Define the prespecified intervention-associated transcript program before any context comparison using the UNC106238 versus none contrast: mean absolute log2 fold change >= 1.0 across the six monocyte donors, sign consistency >= 5/6 donors, and feature overlap with the macrophage-condition contrast using shared gene identifiers.
3. Perform the donor-aware pseudobulk baseline: average repeated context measurements within each donor and condition, then use donor-level exploratory inference for the macrophage-present versus macrophage-absent contrast.
4. Fit the composition-robustness sensitivity analysis: ridge regression with donor, condition, batch, and sample-composition covariates. This is a sensitivity analysis, not a causal model.
5. Report the context contrast, uncertainty, donor-level pattern, and whether the contrast is robust to sample-composition differences. Report supportive, adverse, and inconclusive outcomes according to the declared criteria.

## Exact data bindings

- Counts: `/data/prepared/E-MTAB-8316.counts.tsv.gz/E-MTAB-8316.counts.tsv.gz`
- Design: `/data/prepared/E-MTAB-8316.design.json/E-MTAB-8316.design.json`

The counts header is `feature` followed by sample IDs such as `MK11`. The design records contain `sample_id`, `donor_id`, `condition`, `cell_type`, and `source_metadata`. Join counts sample columns to design `sample_id`.

## Required output

Write `/workspace/results.json` with at least:

- `program`: the prespecified transcript program and selection criteria applied
- `baseline`: donor-aware pseudobulk context contrast with uncertainty and donor-level results
- `ridge`: composition-robustness sensitivity analysis results
- `outcome`: one of `supportive`, `adverse`, or `inconclusive`, with a justification tied to the computed results
- `limitations`: explicit statement that this is exploratory and does not establish direct target causality

## Interpretation rules

Supportive means the context contrast is supported by the available data and is robust to donor, condition, batch, and sample-composition differences. Adverse means the contrast is not supported or is driven by donor, condition, batch, or composition differences. Inconclusive means the contrast is not robust to composition differences or the data are insufficient to distinguish the leading claim from its strongest rival. A result that is not robust to composition differences is not supportive, even if the raw contrast is large.

## Key references

[K1] Rao et al. (2025) describe monocyte state transitions after myocardial infarction, but do not establish a context-dependent transcript response to a specific intervention in macrophage-fibroblast coculture. This proposal tests a different question: whether an intervention-associated transcript response depends on macrophage-fibroblast context.

[K2] Liu et al. (2026) describe extracellular vesicle regulation in wound healing and scar formation by macrophages, fibroblasts, and their crosstalk, but do not establish a context-dependent transcript response to a specific intervention in macrophage-fibroblast coculture. This proposal tests a different question: whether an intervention-associated transcript response depends on macrophage-fibroblast context.

[K3] Mao et al. (2026) describe m6A methylation regulatory networks in pulmonary fibrosis, but do not establish a context-dependent transcript response to a specific intervention in macrophage-fibroblast coculture. This proposal tests a different question: whether an intervention-associated transcript response depends on macrophage-fibroblast context.

## Bibliography

- Rao SV, O'Donoghue ML, Ruel M, et al. Peripheral blood transcriptomes and a single-cell atlas suggest a monocyte-associated immune recovery-failure axis in STEMI. PLoS One. 2025. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0358983
- Liu T, Liu Y, Liu Y, et al. Extracellular vesicles in wound healing and scar formation: molecular regulation of macrophages, fibroblasts, and their crosstalk. Front Cell Dev Biol. 2026. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13613145/fullTextXML
- Mao L, Zhou D, Zhou G, Lu X. m6A methylation regulatory network in pulmonary fibrosis: Molecular mechanisms from RNA stability to cellular phenotype transition. Exp Ther Med. 2026. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13419677/fullTextXML

## What is not established

This experiment does not establish direct target causality, clinical efficacy, or a mechanism. It is an exploratory, donor-aware diagnostic. Clinical adjudication, independent replication, and perturbation evidence would be required for stronger claims.
