---
id: phillips-hansen-1990
type: source_intelligence
status: under_review
reviewed: false
aliases: ["Phillips Hansen 1990", "FM-OLS"]
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebook_source_id: "3371fd51-9895-482e-b0be-60176877edd7"
source_title: "PhillipsHansen1990.pdf"
source_type: PDF
related_audit_phases: [1, 2]
related_audit_questions: ["1.3", "2.2", "2.3"]
last_reviewed: 2026-07-23
---
# Phillips–Hansen (1990)

> Curated audit draft; source-level human verification remains required.

## Bibliographic identity

Phillips and Hansen (1990), foundational fully modified estimation and
inference for cointegrating regressions with \(I(1)\) processes.

## Main contributions

- Introduces semiparametric corrections for endogeneity and serial correlation.
- Produces a zero-centered mixed-normal estimator limit.
- Supports standard Wald inference after the fully modified transformation.

## Critical insights for the I(2) validation

The long-run covariance is estimated from stationary errors and innovations,
not from nonstationary regressor levels.

## Formal results, assumptions, and rank conditions

The correction uses a finite, nonsingular innovation long-run covariance and a
stationary cointegrating error.

## Limitations and prohibited inferences

Do not feed an \(I(2)\) level into an LRCV estimator or claim that the original
FM-OLS theorem covers the project's cross-product.

## Audit links

Questions: `1.3`, `2.2`, `2.3`.

## Related notes

- [Polynomial Cointegration](../../concepts/polynomial_cointegration.md) · [[polynomial_cointegration]]
- [The I(2) Trap](../../concepts/i2_trap.md) · [[i2_trap]]
