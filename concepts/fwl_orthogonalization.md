---
id: fwl-orthogonalization
type: canonical_concept
status: awaiting_audit
aliases: ["FWL Orthogonalization", "fwl_orthogonalization", "Orthogonalized Interaction"]
source_snapshots: ["../notes/source_snapshots/i2_trap/E_00_I2_Trap.md", "../notes/source_snapshots/i2_trap/E_01_I2_Trap.md"]
audit_phases: [4]
audit_questions: ["4.1", "4.2", "4.3"]
last_reviewed: null
---
# FWL Orthogonalization

> Not yet authoritative. Promote claims only after reviewing Phase 4 evidence.

## Formal claim

Pending validation of coefficient and test-statistic invariance after
partialling the interaction term with nonstationary regressors.

## Assumptions and rank conditions

Pending validation of deterministic components, projection spaces, mixed-order
scaling, and transformed-regression equivalence.

## Proof or theorem evidence

Review questions `4.1`, `4.2`, and `4.3` against Wagner–Hong,
Vogelsang–Wagner, and de Jong–Wagner.

## Audit verdict

**Pending.**

## Required correction

Do not present reduced multicollinearity as proof of unchanged asymptotic
inference without the required projection algebra.

## Implementation implications

The verdict determines the auxiliary regression, deterministic controls, and
whether inference can be transferred to the orthogonalized interaction.

## Unresolved questions

- Does the residual retain the full \(I(2)\) trend?
- Does the partial-sum transformation commute with the FWL projection used here?

## Related notes

- [Wagner–Hong (2016)](../notes/source_intelligence/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Vogelsang–Wagner (2014)](../notes/source_intelligence/vogelsang-wagner-2014.md) · [[vogelsang-wagner-2014]]
- [IM-OLS Framework](im_ols_framework.md) · [[im_ols_framework]]
