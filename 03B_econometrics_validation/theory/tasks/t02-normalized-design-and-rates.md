---
schema_version: 2
id: "t02-normalized-design-and-rates"
title: "T02 — Normalized Design and Coefficient Rates"
type: "theory-task"
status: "resolved"
aliases: ["T02 Normalized Design Rates"]
tags: ["econometrics", "normalization", "rank"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
sequence: 2
depends_on: ["t01-cross-product-limit"]
resolves_concepts: ["i2-trap", "polynomial-cointegration"]
source_dossiers: ["chang-park-phillips-2001", "park-phillips-2001", "wagner-hong-2016"]
audit_questions: ["1.3", "2.1", "2.2", "3.2"]
proof_status: "passed"
simulation_status: "passed"
outcome: "qualified"
mathematical_status: "locally-qualified"
scholarly_status: "peer-reviewed"
finite_sample_status:
  t50: "diagnostic"
  t100: "diagnostic"
---
# T02 — Normalized Design and Coefficient Rates

## Formal setup

Let the $t$-th design row be
$$
Z_t=(1,x_t,\omega_t,x_t\omega_{t-\ell})
$$
and let
$$
D_T=\operatorname{diag}(1,T^{1/2},T^{1/2},T).
$$
Write $q(r)=(1,B_x(r),B_\omega(r),B_x(r)B_\omega(r))'$.

## Assumptions

- T01’s joint FCLT and fixed-lag conditions hold.
- The regression error $u_t$ is stationary and obeys the joint martingale or
  weak-dependence limit needed for the normalized score.
- The limiting Gram matrix $G=\int_0^1q(r)q(r)'\,dr$ is positive definite.
- Endogeneity corrections may change centering and covariance, but not the
  column-rate algebra established here.

## Lemmas

Column normalization gives
$$
T^{-1}D_T^{-1}Z'ZD_T^{-1}\Rightarrow
G=\int_0^1q(r)q(r)'\,dr.
$$
For an exogenous stationary regression error,
$$
T^{-1/2}D_T^{-1}Z'u\Rightarrow\int_0^1q(r)\,dB_u(r).
$$

## Derivation

From the normal equations,
$$
\sqrt{T}D_T(\widehat\beta-\beta)
=
\left(T^{-1}D_T^{-1}Z'ZD_T^{-1}\right)^{-1}
\left(T^{-1/2}D_T^{-1}Z'u\right).
$$
Consequently the coefficient rates are:

| Column | Column magnitude | Coefficient error |
|---|---:|---:|
| intercept | $1$ | $T^{-1/2}$ |
| $x_t$ | $T^{1/2}$ | $T^{-1}$ |
| $\omega_t$ | $T^{1/2}$ | $T^{-1}$ |
| $x_t\omega_{t-\ell}$ | $T$ | $T^{-3/2}$ |

These are joint-design rates. Normalizing only the interaction while ignoring
the other columns does not establish an estimator limit.

## Rank conditions

Full design requires $a'q(r)=0$ almost everywhere only when $a=0$.
Nonsingular two-dimensional Brownian support makes this condition plausible
for the four polynomial functions, but it must be imposed and checked. If the
two levels share one common trend, the degree-one columns are asymptotically
collinear and $G$ is singular.

## Degenerate cases

- Stationary $\omega_t$ requires
  $D_T=\operatorname{diag}(1,T^{1/2},1,T^{1/2})$, giving rates
  $T^{-1/2},T^{-1},T^{-1/2},T^{-1}$.
- Cointegrated levels have a vanishing normalized minimum eigenvalue even when
  the finite-sample matrix is invertible.
- A singular common trend produces exact degree-one collinearity.
- Near-singular long-run covariance produces poor conditioning without
  changing the formal rate exponents.

## Peer-reviewed evidence

The homogeneous nonlinear-rate foundation follows Chang, Park, and Phillips
(2001) and Park and Phillips (2001). Wagner and Hong (2016), DOI
[10.1017/S0266466615000213](https://doi.org/10.1017/S0266466615000213),
demonstrates the scaled-rank logic for its additive CPR design, but explicitly
does not close the distinct cross-product estimator problem.

## Simulation design

The 10,000-replication run uses all six T01 scenarios. Normalized Gram
eigenvalues are recorded for every design. OLS coefficient RMSE exponents are
checked for the three nonsingular integrated correlations and the
stationary-$\omega_t$ design.

## Results

All 16 coefficient-rate checks pass. The interaction RMSE exponents are
$-1.452,-1.465,-1.475$ for correlations $0,0.5,0.9$, against $-1.5$.
The stationary-$\omega_t$ interaction exponent is $-1.006$, against
$-1$. At $T=1000$, the cointegrated-level minimum eigenvalue is
$1.24\times10^{-4}$, while the singular design is numerically zero; both are
correctly classified as asymptotically deficient.

## Verdict

**Resolved / qualified.** The normalization and exogenous coefficient rates
are established conditional on full design. They do not validate a particular
endogeneity correction.

## Concept-note implications

Record $T^{-3/2}$ as the interaction-coefficient rate only for a
nondegenerate integrated cross-product design with stationary regression error.
Branch explicitly for stationary or cointegrated state variables.

## Remaining gaps

T03 must provide a valid estimator transformation and centered covariance
under endogeneity and serial correlation.

## Related notes

- [T01 — Cross-product limit](t01-cross-product-limit.md) · [[t01-cross-product-limit|T01 — Cross-product limit]]
- [Polynomial Cointegration](../../concepts/polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
- [Coefficient rate checks](../results/t02-rate-checks.csv)
