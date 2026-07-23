---
id: im-ols-framework
type: canonical_concept
status: awaiting_audit
aliases: ["IM-OLS Framework", "im_ols_framework", "Integrated Modified OLS"]
source_snapshots: ["../notes/source_snapshots/i2_trap/E_00_I2_Trap.md", "../notes/source_snapshots/i2_trap/E_01_I2_Trap.md"]
audit_phases: [3]
audit_questions: ["3.1", "3.2", "3.3"]
last_reviewed: null
---
# IM-OLS Framework

> Not yet authoritative. Promote claims only after reviewing Phase 3 evidence.

## Formal claim

Pending validation of the partial-sum transformation and the estimator's
limiting distribution for mixed polynomial regressors.

## Assumptions and rank conditions

Pending validation of innovation, deterministic-term, full-rank, and
fixed-\(b\) assumptions.

## Proof or theorem evidence

Review questions `3.1`, `3.2`, and `3.3` against Vogelsang–Wagner and the
multivariate extension attributed to de Jong–Wagner.

## Audit verdict

**Pending.**

## Required correction

Do not claim that long-run covariance estimation is universally irrelevant
until the exact theorem and transformation are verified.

## Implementation implications

Validated rate matrices and inference determine the transformed regression,
standard errors, and coefficient interpretation.

## Unresolved questions

- What is the exact joint rate matrix for the interactive CPR?
- Does fixed-\(b\) inference require nonstandard critical values?

## Related notes

- [Vogelsang–Wagner (2014)](../notes/source_intelligence/vogelsang-wagner-2014.md) · [[vogelsang-wagner-2014]]
- [de Jong–Wagner (2025)](../notes/source_intelligence/de-jong-wagner-2025.md) · [[de-jong-wagner-2025]]
- [Polynomial Cointegration](polynomial_cointegration.md) · [[polynomial_cointegration]]
