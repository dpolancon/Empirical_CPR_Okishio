---
schema_version: 2
id: "t05-cpr-residual-testing"
title: "T05 — Residual Testing for the Cross-Product CPR"
type: "theory-task"
status: "blocked"
aliases: ["T05 CPR Residual Tests"]
tags: ["econometrics", "cointegration-testing", "cpr", "bootstrap"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
sequence: 5
depends_on: ["t02-normalized-design-and-rates", "t03-estimator-extension", "t04-transformed-fwl"]
resolves_concepts: ["cpr-cointegration-testing"]
source_dossiers: ["wagner-2023", "wagner-hong-2016"]
audit_questions: ["5.1", "5.2", "5.3"]
proof_status: "local-derivation-complete"
simulation_status: "smoke-failed-full-pending"
outcome: null
mathematical_status: "open"
scholarly_status: "awaiting-peer-review"
finite_sample_status:
  t50: "unsupported"
  t100: "unsupported"
---
# T05 — Residual Testing for the Cross-Product CPR

## Formal setup

Using T03, define
$$
\widehat u_t=y_t-\widehat a-\widehat b k_t-\widehat f\omega_t
 -\widehat d k_t\omega_{t-1},
\qquad
S_t=\sum_{j=1}^t\widehat u_j.
$$
The null is that the fitted CPR residual is stationary.

## Assumptions

- The $I(1)$ design, rank conditions, and local estimator limit in T03 hold.
- The residual long-run variance is finite and positive.
- Bootstrap blocks grow while their length divided by $T$ vanishes.
- Every bootstrap draw imposes the fitted cointegrating relation and
  re-estimates the complete augmented model.

## Lemmas

For an oracle stationary residual,
$\sum_{t=1}^TS_t^2=O_p(T^2)$; for an oracle random-walk residual it is
$O_p(T^4)$. For fitted residuals,
$$
T^{-1/2}S_{\lfloor Tr\rfloor}
\Rightarrow B_u(r)-\mathcal Q(r)'\mathcal M_\beta,
$$
where $\mathcal M_\beta$ is T03's first-four-coordinate mixed limit.

## Derivation

The statistic is
$$
J_T=
\frac{T^{-2}\sum_{t=1}^TS_t^2}{\widehat\Omega_{u\cdot v}}.
$$
The fixed-$b$ critical values are simulated from the complete Brownian
experiment, including the estimator projection. The second implementation
uses circular blocks from
$(\widehat u_t,\Delta k_t,\Delta\omega_t)'$, reconstructs both integrated
paths under the null, and re-estimates T03 before recalculating $J_T$.

## Rank conditions

The statistic is undefined as an operational test whenever T03 refuses the
normalized augmented design. Critical values from an additive-power CPR or a
reduced interaction regression are not substituted.

## Degenerate cases

An $I(0)$ wage share, singular common trend, cointegrated level regressors,
or local-to-unity ambiguity changes the fitted-residual projection. Those
cases remain diagnostic-only.

## Peer-reviewed evidence

Wagner (2023), DOI
[10.1007/s00181-022-02332-3](https://doi.org/10.1007/s00181-022-02332-3),
provides the residual-test architecture for its additive CPR. It does not
close the exact cross-product projection, which is derived locally here.

## Simulation design

The experiment reports fixed-$b$ limiting critical values and sample-specific
bootstrap values for $T=40,50,60,80,100,120$. Size is measured under a
stationary residual. Power uses random-walk additions with innovation scales
$0.25,0.50,1.00$ and corresponding $T^{-1/2}$ local alternatives.
Asymptotic references use $T=200,500,1000$.

## Results

The fixed-$b$ limit now includes the same fitted-residual Bartlett
long-run-variance randomness used by the finite-sample statistic. In the
250-replication smoke run, the nominal 5% rejection rate is 11.2% at $T=50$,
8.4% at $T=100$, and 5.6% at $T=1000$. Thus the small-sample gate still
fails, while the largest smoke cell is compatible with the asymptotic target.
The 250-outer bootstrap rejection rates are 2.4%, 5.2%, 6.0%, and 4.0% at
$T=50,100,500,1000$, respectively. Bootstrap size is encouraging, but the
two methods disagree by 8.8 percentage points at $T=50$, so the mandatory
two-method gate fails. Across the complete 40–120 neighborhood, fixed-$b$
size ranges from 6.4% to 11.6%, while bootstrap size ranges from 2.4% to 5.6%.

## Verdict

**Local statistic derived; calibration not validated.** The task remains
mathematically open and scholarly blocked. In particular, the new code must
not be described as a validated CPR cointegration test.

## Concept-note implications

Report the oracle order result separately from the fitted-residual test.
Until size gates pass, empirical applications should label $J_T$ as a
sensitivity diagnostic and show both calibration methods.

## Remaining gaps

- Complete the full size and power experiment.
- Verify the bootstrap consistency conditions for the exact resampling law.
- Obtain a peer-reviewed theorem for the cross-product fitted projection.

## Related notes

- [CPR Cointegration Testing](../../concepts/cpr-cointegration-testing.md) · [[cpr-cointegration-testing|CPR Cointegration Testing]]
- [T03 — Estimator extension](t03-estimator-extension.md) · [[t03-estimator-extension|T03 — Estimator extension]]
- [T04 — Transformed FWL](t04-transformed-fwl.md) · [[t04-transformed-fwl|T04 — Transformed FWL]]
- [Size and power experiment](../results/t05-size-power.csv)
