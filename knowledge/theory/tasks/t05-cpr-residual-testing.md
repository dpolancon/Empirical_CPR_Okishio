---
schema_version: 2
id: "t05-cpr-residual-testing"
title: "T05 — Residual Testing for the Cross-Product CPR"
type: "theory-task"
status: "blocked"
aliases: ["T05 CPR Residual Tests"]
tags: ["econometrics", "cointegration-testing", "cpr"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
sequence: 5
depends_on: ["t02-normalized-design-and-rates", "t03-estimator-extension", "t04-transformed-fwl"]
resolves_concepts: ["cpr-cointegration-testing"]
source_dossiers: ["wagner-2023", "wagner-hong-2016"]
audit_questions: ["5.1", "5.2", "5.3"]
proof_status: "blocked"
simulation_status: "partial"
outcome: null
---
# T05 — Residual Testing for the Cross-Product CPR

## Formal setup

Let \(\widehat u_t=y_t-Z_t'\widehat\beta\) and
\(S_t=\sum_{j=1}^t\widehat u_j\). A residual stationarity statistic is built
from \(\sum_{t=1}^T S_t^2\), with normalization and nuisance correction
determined by the fitted CPR design and estimator.

## Assumptions

- The cointegrating residual is \(I(0)\) under the null.
- T02’s full design holds.
- The estimator contribution to the residual partial-sum limit is known.
- Long-run variance estimation is valid for the exact residual process.

## Lemmas

For an oracle stationary residual \(u_t\),
\[
S_{\lfloor Tr\rfloor}=O_p(T^{1/2}),\qquad
\sum_{t=1}^T S_t^2=O_p(T^2).
\]
For an oracle random-walk residual,
\[
S_{\lfloor Tr\rfloor}=O_p(T^{3/2}),\qquad
\sum_{t=1}^T S_t^2=O_p(T^4).
\]

## Derivation

The oracle orders follow from one and two applications of the invariance
principle. They justify \(T^{-2}\) scaling under a stationary-residual null.
They do not determine the fitted-residual limit because
\[
\widehat u_t=u_t-Z_t'(\widehat\beta-\beta),
\]
and the second term depends on T03’s unresolved estimator limit and on T02’s
mixed rates.

## Rank conditions

The statistic is nuisance-free only if the complete normalized design and the
estimator correction deliver the projection functional assumed by its
published critical values. Dropping or residualizing the interaction changes
that projection.

## Degenerate cases

Stationary \(\omega_t\), a singular common trend, and cointegrated level
regressors each change the design limit. Critical values for an additive-power
CPR cannot be assumed invariant to these cases.

## Peer-reviewed evidence

Wagner (2023), DOI
[10.1007/s00181-022-02332-3](https://doi.org/10.1007/s00181-022-02332-3),
derives residual tests for the paper’s additive CPR specification.
Wagner–Hong (2016) supplies the corresponding estimator for additive powers.
Neither admissible source closes the exact distinct cross-product projection.

## Simulation design

The committed diagnostic simulates oracle stationary and random-walk
residuals. It checks only the exponents of
\(\sum S_t^2\); no cross-product CPR critical values or bootstrap DGP are
fabricated.

## Results

The stationary-residual exponent is 1.994 against 2, and the unit-root-residual
exponent is 3.983 against 4. Both pass the rate tolerance. These checks validate
the oracle scaling distinction, not a fitted-residual test.

## Verdict

**Blocked.** \(T^{-2}\) is the correct oracle null order, but the exact
cross-product residual limit, nuisance correction, and critical values depend
on blocked T03.

## Concept-note implications

Do not reuse additive-CPR tables or report a cross-product cointegration test.
Retain the oracle scaling result as a diagnostic only.

## Remaining gaps

After T03 resolves, derive the fitted-residual projection, select the null and
alternative, and validate size and power for a fully specified bootstrap or
simulation DGP.

## Related notes

- [CPR Cointegration Testing](../../concepts/cpr-cointegration-testing.md) · [[cpr-cointegration-testing|CPR Cointegration Testing]]
- [T03 — Estimator extension](t03-estimator-extension.md) · [[t03-estimator-extension|T03 — Estimator extension]]
- [Residual rate checks](../results/t05-residual-rate-checks.csv)
