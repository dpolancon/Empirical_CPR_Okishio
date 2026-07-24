---
id: wagner-hong-2016
type: source_intelligence
status: under_review
reviewed: false
aliases: ["Wagner Hong 2016", "Cointegrating Polynomial Regressions"]
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebook_source_id: "ada0bbf7-27ab-4bde-a61a-510d978d2811"
source_title: "WagnerHyunhong2016.pdf"
source_type: PDF
related_audit_phases: [1, 2, 4, 6]
related_audit_questions: ["1.1", "1.2", "1.3", "2.1", "2.2", "4.1", "4.3", "6.1"]
last_reviewed: 2026-07-23
---
# Wagner–Hong (2016)

> Curated audit draft; direct scope verification completed, with human review
> still required.

## Bibliographic identity

Wagner and Hong (2016), CPR fully modified estimation and inference for
integer powers of \(I(1)\) regressors.

## Main contributions

- Extends Phillips–Hansen FM-OLS to cointegrating polynomial regressions.
- Derives a zero-mean Gaussian-mixture estimator limit.
- Gives scaled-rank conditions for Wald and LM restrictions.

## Critical insights for the I(2) validation

The paper's Remark 1 explicitly imposes additive separability and excludes
cross-products of powers of distinct integrated regressors.

## Formal results, assumptions, and rank conditions

The innovation covariance must be nondegenerate, the normalized polynomial
moment matrix must be full rank, and a scaled restriction must satisfy
\(G_RRG\to R^*\) with full row rank.

## Limitations and prohibited inferences

This paper cannot validate the project's \(x_ty_t\) interaction, its asserted
\(I(2)\) classification, or an interaction-specific IM-OLS transformation.

## Audit links

Questions: `1.1`, `1.2`, `1.3`, `2.1`, `2.2`, `4.1`, `4.3`, `6.1`.

## Related notes

- [Polynomial Cointegration](../../concepts/polynomial_cointegration.md) · [[polynomial_cointegration]]
- [The I(2) Trap](../../concepts/i2_trap.md) · [[i2_trap]]
