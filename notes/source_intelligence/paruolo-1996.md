---
id: paruolo-1996
type: source_intelligence
status: under_review
reviewed: false
aliases: ["Paruolo 1996", "Paurolo1996"]
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebook_source_id: "6f93d684-3ba3-4684-a95d-84d256c22c9b"
source_title: "Paurolo1996.pdf"
source_type: PDF
related_audit_phases: [1]
related_audit_questions: ["1.1", "1.2"]
last_reviewed: 2026-07-23
---
# Paruolo (1996)

> Curated audit draft; direct scope verification completed, with human review
> still required.

## Bibliographic identity

Paruolo (1996), “On the determination of integration indices in I(2)
systems,” *Journal of Econometrics* 72, 313–356.

## Main contributions

- Estimates the numbers of \(I(0)\), \(I(1)\), and \(I(2)\) common components
  in a VAR system.
- Uses a two-stage sequence of regression and reduced-rank regression tests.
- Derives limiting Gaussian-functional rank-test distributions.

## Critical insights for the I(2) validation

The source addresses system-level linear \(I(2)\) integration indices. It does
not establish that a nonlinear product regressor is \(I(2)\).

## Formal results, assumptions, and rank conditions

The impact matrix and a projected derivative matrix satisfy nested reduced-rank
conditions that partition the system into integration indices.

## Limitations and prohibited inferences

Do not import Paruolo's VAR ranks into a single-equation CPR or bootstrap DGP
without proving an equivalent system representation.

## Audit links

Questions: `1.1`, `1.2`.

## Related notes

- [The I(2) Trap](../../concepts/i2_trap.md) · [[i2_trap]]
- [Polynomial Cointegration](../../concepts/polynomial_cointegration.md) · [[polynomial_cointegration]]
