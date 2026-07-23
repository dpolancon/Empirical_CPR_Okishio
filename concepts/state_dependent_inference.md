---
id: state-dependent-inference
type: canonical_concept
status: awaiting_audit
aliases: ["State-Dependent Inference", "state_dependent_inference", "Gamma Wald Test"]
source_snapshots: ["../notes/source_snapshots/i2_trap/E_00_I2_Trap.md", "../notes/source_snapshots/i2_trap/E_01_I2_Trap.md"]
audit_phases: [6]
audit_questions: ["6.1", "6.2", "6.3"]
last_reviewed: null
---
# State-Dependent Inference

> Not yet authoritative. Promote claims only after reviewing Phase 6 evidence.

## Formal claim

Pending validation of the delta-method distribution for
\(\theta=b+d\bar{\omega}\) and the Wald restriction for the inefficiency gap.

## Assumptions and rank conditions

Pending validation of joint convergence rates, stochastic versus fixed
\(\omega\), covariance terms, and differentiability of the restriction.

## Proof or theorem evidence

Review questions `6.1`, `6.2`, and `6.3` against Wagner–Hong,
Vogelsang–Wagner, and the validated CPR rate matrix.

## Audit verdict

**Pending.**

## Required correction

Do not discard the interaction-coefficient variance or covariance term until
the common normalization and evaluation point are established.

## Implementation implications

The verdict determines confidence bands for the state-dependent elasticity and
the valid Wald statistic for \(\Gamma=0\).

## Unresolved questions

- Which component dominates under the actual CPR normalization?
- Is \(\bar{\omega}\) treated as fixed, estimated, or stochastic in the final test?

## Related notes

- [Wagner–Hong (2016)](../notes/source_intelligence/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Vogelsang–Wagner (2014)](../notes/source_intelligence/vogelsang-wagner-2014.md) · [[vogelsang-wagner-2014]]
- [IM-OLS Framework](im_ols_framework.md) · [[im_ols_framework]]
