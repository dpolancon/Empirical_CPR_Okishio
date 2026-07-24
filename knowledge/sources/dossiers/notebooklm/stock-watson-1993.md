---
schema_version: 2
id: "stock-watson-1993"
title: "Stock–Watson (1993)"
type: "source-dossier"
status: "under-review"
aliases: ["Stock Watson 1993", "DOLS"]
tags: ["econometrics", "source-intelligence"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "notebooklm"
publication_status: "peer-reviewed"
citation_key: "stock-watson-1993"
doi: null
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebooklm_source_id: "69357ef3-68cd-4c3d-9545-58bcac917835"
source_title: "StockWatson1993_DOLS.pdf"
source_type: "pdf"
reviewed: false
audit_questions: ["2.1"]
---
# Stock–Watson (1993)

> Curated audit draft; source-level human verification remains required.

## Bibliographic identity

Stock and Watson (1993), “A Simple Estimator of Cointegrating Vectors in
Higher Order Integrated Systems.”

## Main contributions

- Gives canonical transformations for higher-order integrated systems.
- Uses dynamic leads and lags to obtain efficient single-equation estimates.
- Derives mixed-rate, chi-squared inference under recursive rank conditions.

## Critical insights for the I(2) validation

The paper concerns linear higher-order integrated systems. It does not prove
that a product of distinct \(I(1)\) levels belongs to one of those canonical
subspaces.

## Formal results, assumptions, and rank conditions

Recursive reduced-rank conditions partition \(I(d),I(d-1),\ldots\) common
trends and determine the block scaling matrix.

## Limitations and prohibited inferences

Do not use the paper's \(I(d)\) decomposition as a shortcut for nonlinear CPR
cross-products.

## Audit links

Question: `2.1`.

## Related notes

- [Polynomial Cointegration](../../../concepts/polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
- [The I(2) Trap](../../../concepts/i2-trap.md) · [[i2-trap|The I(2) Trap]]
