---
id: cpr-cointegration-testing
type: canonical_concept
status: awaiting_audit
aliases: ["CPR Cointegration Testing", "cpr_cointegration_testing", "CPR Residual Tests"]
source_snapshots: ["../notes/source_snapshots/i2_trap/E_00_I2_Trap.md", "../notes/source_snapshots/i2_trap/E_01_I2_Trap.md"]
audit_phases: [5]
audit_questions: ["5.1", "5.2", "5.3"]
last_reviewed: null
---
# CPR Cointegration Testing

> Not yet authoritative. Promote claims only after reviewing Phase 5 evidence.

## Formal claim

Pending validation of the residual-based null, statistic, scaling exponent,
and bootstrap data-generating process for CPRs.

## Assumptions and rank conditions

Pending validation of integration orders, deterministic specification,
cointegrating ranks, and bootstrap restrictions.

## Proof or theorem evidence

Review questions `5.1`, `5.2`, and `5.3` against Wagner (2023) and the
Grabarczyk dissertation.

## Audit verdict

**Pending.**

## Required correction

Remove all approximate critical values or scaling claims that cannot be traced
to the exact source design.

## Implementation implications

The verdict determines the residual statistic, normalization, simulated
critical values, and bootstrap null.

## Unresolved questions

- What is the exact scaling exponent for this regressor basis?
- Which bootstrap scheme preserves the relevant polynomial stochastic orders?

## Related notes

- [Wagner (2023)](../notes/source_intelligence/wagner-2023.md) · [[wagner-2023]]
- [Grabarczyk dissertation](../notes/source_intelligence/grabarczyk-dissertation.md) · [[grabarczyk-dissertation]]
- [Polynomial Cointegration](polynomial_cointegration.md) · [[polynomial_cointegration]]
