---
schema_version: 2
id: "t06-state-dependent-inference"
title: "T06 — State-Dependent Inference"
type: "theory-task"
status: "blocked"
aliases: ["T06 State Dependent Wald Inference"]
tags: ["econometrics", "delta-method", "wald"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
sequence: 6
depends_on: ["t02-normalized-design-and-rates", "t03-estimator-extension"]
resolves_concepts: ["state-dependent-inference"]
source_dossiers: ["vogelsang-wagner-2014", "wagner-hong-2016"]
audit_questions: ["6.1", "6.2", "6.3"]
proof_status: "partial"
simulation_status: "partial"
outcome: null
---
# T06 — State-Dependent Inference

## Formal setup

For the interaction model, define the marginal effect with respect to
\(\omega\) at state \(s\) as
\[
\gamma(s)=\beta_\omega+s\beta_z,\qquad
c(s)=(0,0,1,s)'.
\]
Then \(\widehat\gamma(s)=c(s)'\widehat\beta\).

## Assumptions

- T02’s coefficient rates hold.
- The state is classified as fixed, estimated stationary, or integrated.
- The joint covariance between the estimator and any estimated state is known.
- Valid Wald inference additionally requires T03’s centered estimator limit.

## Lemmas

For fixed \(s=O(1)\),
\[
\widehat\gamma(s)-\gamma(s)
=O_p(T^{-1})+sO_p(T^{-3/2})=O_p(T^{-1}).
\]
For an integrated path state \(s_T=O_p(T^{1/2})\), both terms have order
\(T^{-1}\). For an independently estimated stationary mean
\(\widehat s-s_0=O_p(T^{-1/2})\),
\[
\widehat\gamma(\widehat s)-\gamma(s_0)
=c(s_0)'(\widehat\beta-\beta)
 +\beta_z(\widehat s-s_0)+\text{smaller terms},
\]
so state uncertainty can dominate the superconsistent parameter uncertainty.

## Derivation

Fixed-state variance is \(c(s)'\widehat V_\beta c(s)\). For a stochastic state,
the delta vector must include derivatives with respect to both \(\beta\) and
the state. An independently estimated stationary mean adds
\(\beta_z^2\widehat V_s\). A jointly estimated or integrated state additionally
requires cross-covariance terms and, for pathwise bands, the joint functional
limit rather than a pointwise scalar delta method.

## Rank conditions

The restriction gradient must retain rank after T02’s scaling. At an integrated
state, scaling the interaction coefficient and the state jointly is essential;
treating the observed level as fixed changes the limiting experiment.

## Degenerate cases

- If \(\beta_z=0\), first-order state-estimation uncertainty vanishes.
- A fixed policy value and a random observed integrated level are different
  inferential objects even when numerically equal.
- A stationary state estimated from the same innovations as \(\widehat\beta\)
  needs the omitted cross-covariance.

## Peer-reviewed evidence

Vogelsang–Wagner (2014) provides IM-OLS inference for linear cointegrating
regressions, while Wagner–Hong (2016) provides scaled restrictions in its
additive CPR class. Neither admissible source establishes the required joint
cross-product estimator/state limit.

## Simulation design

The diagnostic uses exogenous iid regression errors and compares a fixed state,
an observed integrated path state, and an independently estimated stationary
mean. For the last case it reports intervals with and without state uncertainty.

## Results

At \(T=500\) and \(T=1000\), corrected coverage is between 94.7% and 94.9% for
all three regimes and passes the 93–97% gate. Ignoring stationary-state
uncertainty reduces coverage from 91.1% at \(T=100\) to 73.1% at \(T=1000\)
because parameter uncertainty shrinks faster than state-estimation uncertainty.

## Verdict

**Blocked with a proved rate decomposition.** The three regimes and their
first-order variance components are resolved algebraically, but valid
endogenous cross-product Wald inference cannot close before T03.

## Concept-note implications

Every reported marginal effect must label its state as fixed, estimated
stationary, or integrated. Never plug an estimated state into a coefficient-only
variance formula.

## Remaining gaps

Derive the joint estimator/state functional limit under the eventual T03
estimator, including cross-covariances and simultaneous pathwise bands.

## Related notes

- [State-Dependent Inference](../../concepts/state-dependent-inference.md) · [[state-dependent-inference|State-Dependent Inference]]
- [T03 — Estimator extension](t03-estimator-extension.md) · [[t03-estimator-extension|T03 — Estimator extension]]
- [State inference results](../results/t06-state-inference-summary.csv)
