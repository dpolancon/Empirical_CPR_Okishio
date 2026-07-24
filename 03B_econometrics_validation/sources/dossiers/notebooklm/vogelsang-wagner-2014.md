---
schema_version: 2
id: "vogelsang-wagner-2014"
title: "Vogelsang–Wagner (2014)"
type: "source-dossier"
status: "under-review"
aliases: ["Vogelsang Wagner 2014", "Vogelsang-Wagner linear IM-OLS"]
tags: ["econometrics", "source-intelligence"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "notebooklm"
publication_status: "peer-reviewed"
citation_key: "vogelsang-wagner-2014"
doi: null
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebooklm_source_id: "8c9b16c5-e8d2-4872-88ce-c427c4d4edfb"
source_title: "VogelsanWagner2014.pdf"
source_type: "pdf"
reviewed: false
audit_questions: ["3.1", "3.2", "3.3", "4.2", "6.1", "6.3"]
---
# Vogelsang–Wagner (2014)

> Curated audit draft; direct scope verification completed, with human review
> still required.

## Bibliographic identity

Vogelsang and Wagner (2014), “Integrated modified OLS estimation and fixed-b
inference for cointegrating regressions,” *Journal of Econometrics* 178,
741–760.

## Main contributions

- Introduces IM-OLS through an augmented partial-sum transformation.
- Avoids LRCV estimation and tuning choices for point estimation.
- Develops residual-adjusted fixed-$b$ inference.

## Critical insights for the I(2) validation

The base theorem starts with $I(1)$ regressors and an $I(0)$ error. The
untransformed $x_t$ augmentation absorbs the long-run endogeneity parameter.

## Formal results, assumptions, and rank conditions

The transformed regression includes $Sx_t$ and $x_t$; fixed-$b$ pivotality
requires adjusted residuals and yields nonstandard critical values.

## Limitations and prohibited inferences

Do not describe the method as an established $I(2)\rightarrow I(3)$
transformation for the project's interaction.

## Audit links

Questions: `3.1`, `3.2`, `3.3`, `4.2`, `6.1`, `6.3`.

## Related notes

- [IM-OLS Framework](../../../concepts/im-ols-framework.md) · [[im-ols-framework|IM-OLS Framework]]
- [State-Dependent Inference](../../../concepts/state-dependent-inference.md) · [[state-dependent-inference|State-Dependent Inference]]
