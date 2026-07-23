---
id: polynomial-cointegration
type: canonical_concept
status: awaiting_audit
aliases: ["Polynomial Cointegration", "polynomial_cointegration", "CPR"]
source_snapshots: ["../notes/source_snapshots/i2_trap/E_00_I2_Trap.md", "../notes/source_snapshots/i2_trap/E_01_I2_Trap.md"]
audit_phases: [1, 2]
audit_questions: ["1.1", "1.2", "2.1", "2.2", "2.3"]
last_reviewed: null
---
# Polynomial Cointegration

> Not yet authoritative. Promote claims only after reviewing Phases 1 and 2.

## Formal claim

Pending a precise definition of the project model as a cointegrating
polynomial regression with mixed stochastic orders.

## Assumptions and rank conditions

Pending validation of CPR basis construction, normalization matrices,
endogeneity conditions, and long-run covariance requirements.

## Proof or theorem evidence

Review questions `1.1`, `1.2`, and `2.1`–`2.3` against Wagner–Hong,
Phillips–Hansen, Saikkonen, and Stock–Watson.

## Audit verdict

**Pending.**

## Required correction

Separate proven CPR results from intuitive extensions of conventional FM-OLS
or DOLS.

## Implementation implications

The validated framework will determine which regressor transformations and
bias corrections are admissible.

## Unresolved questions

- Which uploaded source proves the exact interaction-product case?
- Which DOLS and FM-OLS failure claims are asymptotic results versus finite-sample warnings?

## Related notes

- [Wagner–Hong (2016)](../notes/source_intelligence/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Phillips–Hansen (1990)](../notes/source_intelligence/phillips-hansen-1990.md) · [[phillips-hansen-1990]]
- [Saikkonen (1991)](../notes/source_intelligence/saikkonen-1991.md) · [[saikkonen-1991]]
- [The I(2) Trap](i2_trap.md) · [[i2_trap]]
