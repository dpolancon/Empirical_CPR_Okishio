---
schema_version: 2
id: "cpr-cointegration-testing"
title: "CPR Cointegration Testing"
type: "concept"
status: "under-review"
aliases: ["CPR Cointegration Testing", "cpr_cointegration_testing", "CPR Residual Tests"]
tags: ["econometrics", "cpr", "i2-trap-audit"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_snapshots: ["e-00-i2-trap", "e-01-i2-trap"]
source_dossiers: ["wagner-2023", "grabarczyk-dissertation"]
audit_questions: ["5.1", "5.2", "5.3"]
theory_tasks: ["t05-cpr-residual-testing"]
---
# CPR Cointegration Testing

> Review-gated correction. CPR-specific limits and critical values are
> required; the E_01 scaling and bootstrap claims were rejected.

## Formal claim

Under the null of cointegration the regression residual is $I(0)$, so its
squared partial sums are $O_p(T^2)$. The KPSS/Shin-type statistic therefore
uses $T^{-2}$ scaling regardless of polynomial regressor order. Higher powers
alter the residual projection and limit distribution, not that exponent.

## Assumptions and rank conditions

- An $I(0)$ residual under the cointegration null.
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

T05 verifies the oracle $T^2$ and $T^4$ orders and now implements the local
fitted cross-product projection, Brownian critical-value experiment, and
null-imposed joint block bootstrap. After aligning the fixed-$b$ residual
adjustment, its smoke size is 11.2% at $T=50$, 8.4% at $T=100$, and 5.6%
at $T=1000$. Bootstrap size is 2.4% and 5.2% at the two small-sample
anchors, but the methods disagree by 8.8 percentage points at $T=50$.
Neither calibration is validated.

## Audit verdict

**Fail.** All Phase 5 validation metrics failed.

## Required correction

Use $T^{-2}$ scaling and retain both local calibration methods as research
diagnostics. Do not publish p-values until the prespecified size gates pass.
Remove $T^{-4}$, automatic divergence, and unsupported bootstrap-rank
assertions.

## Implementation implications

Do not reuse linear Phillips–Ouliaris critical values. Implement the
$T^{-2}$ residual partial-sum statistic only after the exact cross-product
projection limit is established.

## Unresolved questions

- The locally simulated critical values fail the current size gate.
- Full nested-bootstrap calibration and scholarly review remain unresolved.

## Related notes

- [Wagner (2023)](../sources/dossiers/notebooklm/wagner-2023.md) · [[wagner-2023]]
- [Grabarczyk dissertation](../sources/dossiers/notebooklm/grabarczyk-dissertation.md) · [[grabarczyk-dissertation]]
- [T05 — CPR residual testing](../theory/tasks/t05-cpr-residual-testing.md) · [[t05-cpr-residual-testing|T05 — CPR residual testing]]
- [Polynomial Cointegration](polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
