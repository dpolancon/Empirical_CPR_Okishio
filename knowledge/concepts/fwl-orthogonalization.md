---
schema_version: 2
id: "fwl-orthogonalization"
title: "FWL Orthogonalization"
type: "concept"
status: "under-review"
aliases: ["FWL Orthogonalization", "fwl_orthogonalization", "Orthogonalized Interaction"]
tags: ["econometrics", "cpr", "i2-trap-audit"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_snapshots: ["e-00-i2-trap", "e-01-i2-trap"]
source_dossiers: ["wagner-hong-2016", "vogelsang-wagner-2014"]
audit_questions: ["4.1", "4.2", "4.3"]
theory_tasks: ["t04-transformed-fwl"]
---
# FWL Orthogonalization

> Review-gated correction. Static FWL equivalence does not survive a
> pre-orthogonalize-then-partial-sum workflow automatically.

## Formal claim

FWL is an exact algebraic identity when partialling is performed within the
same regression and inner product. If \(S\) is the partial-sum operator,
generally \(SM_X\neq M_{SX}S\); consequently, orthogonalizing in levels and
then applying IM-OLS need not preserve the raw-interaction coefficient or its
t-statistic.

## Assumptions and rank conditions

- Identical transformed design, weights, deterministic controls, and covariance
  estimator on both sides of the FWL comparison.
- Full column rank of the relevant transformed design.
- Deterministic terms included jointly or partialled in the same metric.

## Proof or theorem evidence

Question `4.1` shows that projecting an \(O_p(T)\) product on \(I(1)\) levels
also produces an \(O_p(T)\) fitted component. Question `4.2` proves the
noncommutation of \(S\) and \(M_X\). Question `4.3` shows that demeaning or
detrending changes the limiting Brownian functional.

## Audit verdict

**Fail.** Phase 4 rejects the claimed negligible projection and exact
IM-OLS t-statistic invariance.

## Required correction

If orthogonalization is used for numerical conditioning, perform FWL inside
the final transformed regression and recompute its covariance estimator.
Never transfer a t-statistic from a different projection problem.

## Implementation implications

Treat orthogonalization as a parameterization choice, not as evidence that the
interaction's stochastic order or inference is unchanged.

## Unresolved questions

- The exact stochastic order of the residualized cross-product requires a
  model-specific limit.
- A numerically stable transformed-design FWL implementation still needs to be
  specified and tested.

## Related notes

- [Wagner–Hong (2016)](../sources/dossiers/notebooklm/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Vogelsang–Wagner (2014)](../sources/dossiers/notebooklm/vogelsang-wagner-2014.md) · [[vogelsang-wagner-2014]]
- [IM-OLS Framework](im-ols-framework.md) · [[im-ols-framework|IM-OLS Framework]]
