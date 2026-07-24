---
schema_version: 2
id: "wagner-2023"
title: "Wagner (2023)"
type: "source-dossier"
status: "under-review"
aliases: ["Wagner 2023", "Wagner 2023 CPR residual tests"]
tags: ["econometrics", "source-intelligence"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "notebooklm"
publication_status: "peer-reviewed"
citation_key: "wagner-2023"
doi: null
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebooklm_source_id: "86a8d87b-e96b-4fe5-9a58-7e354e8bfe4b"
source_title: "Wagner2023.pdf"
source_type: "pdf"
reviewed: false
audit_questions: ["5.1", "5.2", "5.3"]
---
# Wagner (2023)

> Curated audit draft; direct scope verification completed, with human review
> still required.

## Bibliographic identity

Wagner (2023), “Residual-based cointegration and non-cointegration tests for
cointegrating polynomial regressions,” *Empirical Economics* 65, 1–31.

## Main contributions

- Derives residual tests with cointegration and non-cointegration nulls for CPRs.
- Shows how polynomial regressors alter the limiting projection functionals.
- Provides simulated critical values for empirically relevant full designs.

## Critical insights for the I(2) validation

Standard linear critical values are invalid because the limit distribution
changes; the source does not support automatic divergence to \(-\infty\).

## Formal results, assumptions, and rank conditions

Under the cointegration null, squared residual partial sums use \(T^{-2}\)
scaling. Nuisance-free tabulation requires full design.

## Limitations and prohibited inferences

The paper treats powers in the CPR basis, not the project's excluded
cross-product case. Do not reuse its tables without matching the exact design.

## Audit links

Questions: `5.1`, `5.2`, `5.3`.

## Related notes

- [CPR Cointegration Testing](../../../concepts/cpr-cointegration-testing.md) · [[cpr-cointegration-testing|CPR Cointegration Testing]]
- [Polynomial Cointegration](../../../concepts/polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
