---
id: saikkonen-1991
type: source_intelligence
status: under_review
reviewed: false
aliases: ["Saikkonen 1991", "Dynamic OLS"]
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebook_source_id: "d6a5173a-8bb2-41dd-8dfd-2d34c6ce8eb0"
source_title: "Saikkonen1991.pdf"
source_type: PDF
related_audit_phases: [2]
related_audit_questions: ["2.1"]
last_reviewed: 2026-07-23
---
# Saikkonen (1991)

> Curated audit draft; source-level human verification remains required.

## Bibliographic identity

Saikkonen (1991), time-domain efficient estimation of \(I(1)\) cointegrating
regressions through dynamic augmentation.

## Main contributions

- Augments the levels regression with leads and lags of stationary differences.
- Orthogonalizes the cointegrating error from short-run regressor innovations.
- Establishes mixed-normal estimation and chi-squared inference under its
  \(I(1)\) assumptions.

## Critical insights for the I(2) validation

The source does not establish asymptotic rank failure between levels and
differences. Parameter proliferation can still create finite-sample variance
and degrees-of-freedom problems.

## Formal results, assumptions, and rank conditions

The stationary augmentation block must have a nonsingular covariance and the
lead/lag truncation must satisfy the paper's growth conditions.

## Limitations and prohibited inferences

Do not claim that \(\Delta(x_ty_t)\) makes DOLS asymptotically singular without
a cross-product-specific rank calculation.

## Audit links

Question: `2.1`.

## Related notes

- [Polynomial Cointegration](../../concepts/polynomial_cointegration.md) · [[polynomial_cointegration]]
- [The I(2) Trap](../../concepts/i2_trap.md) · [[i2_trap]]
