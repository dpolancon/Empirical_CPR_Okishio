---
id: cpr-cointegration-testing
type: canonical_concept
status: under_review
aliases: ["CPR Cointegration Testing", "cpr_cointegration_testing", "CPR Residual Tests"]
source_snapshots: ["../notes/source_snapshots/i2_trap/E_00_I2_Trap.md", "../notes/source_snapshots/i2_trap/E_01_I2_Trap.md"]
audit_phases: [5]
audit_questions: ["5.1", "5.2", "5.3"]
last_reviewed: 2026-07-23
---
# CPR Cointegration Testing

> Review-gated correction. CPR-specific limits and critical values are
> required; the E_01 scaling and bootstrap claims were rejected.

## Formal claim

Under the null of cointegration the regression residual is \(I(0)\), so its
squared partial sums are \(O_p(T^2)\). The KPSS/Shin-type statistic therefore
uses \(T^{-2}\) scaling regardless of polynomial regressor order. Higher powers
alter the residual projection and limit distribution, not that exponent.

## Assumptions and rank conditions

- An \(I(0)\) residual under the cointegration null.
- The exact deterministic and polynomial design used for critical values.
- Full design when nuisance-free tabulation is claimed.
- A bootstrap DGP tied explicitly to the chosen null; no imported I(2)-VAR
  ranks without a source theorem.

## Proof or theorem evidence

Wagner (2023) derives CPR-specific residual test limits. Question `5.1`
rejects divergence of Phillips–Ouliaris statistics and instead identifies
wrong critical values as the problem. Question `5.2` fixes the squared
partial-sum exponent at two. Question `5.3` finds no source support for the
proposed I(2)-rank bootstrap.

## Audit verdict

**Fail.** All Phase 5 validation metrics failed.

## Required correction

Use CPR-specific simulated critical values for the proven design. Remove
\(T^{-4}\), automatic divergence, and bootstrap-rank assertions from the
implementation notes.

## Implementation implications

Do not reuse linear Phillips–Ouliaris critical values. Implement the
\(T^{-2}\) residual partial-sum statistic only after the exact cross-product
projection limit is established.

## Unresolved questions

- The residual statistic exponent is two under the cointegration null, but its
  cross-product-specific critical values are unknown.
- A valid bootstrap DGP for the exact interaction design remains unresolved.

## Related notes

- [Wagner (2023)](../notes/source_intelligence/wagner-2023.md) · [[wagner-2023]]
- [Grabarczyk dissertation](../notes/source_intelligence/grabarczyk-dissertation.md) · [[grabarczyk-dissertation]]
- [Polynomial Cointegration](polynomial_cointegration.md) · [[polynomial_cointegration]]
