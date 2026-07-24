---
id: stock-watson-1993
type: source_intelligence
status: under_review
reviewed: false
aliases: ["Stock Watson 1993", "DOLS"]
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebook_source_id: "69357ef3-68cd-4c3d-9545-58bcac917835"
source_title: "StockWatson1993_DOLS.pdf"
source_type: PDF
related_audit_phases: [2]
related_audit_questions: ["2.1"]
last_reviewed: 2026-07-23
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

- [Polynomial Cointegration](../../concepts/polynomial_cointegration.md) · [[polynomial_cointegration]]
- [The I(2) Trap](../../concepts/i2_trap.md) · [[i2_trap]]
