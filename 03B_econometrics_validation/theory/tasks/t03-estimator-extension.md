---
schema_version: 2
id: "t03-estimator-extension"
title: "T03 — Estimator Extension to the Cross-Product Design"
type: "theory-task"
status: "blocked"
aliases: ["T03 Cross Product Estimators"]
tags: ["econometrics", "im-ols", "fixed-b", "bootstrap"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
sequence: 3
depends_on: ["t01-cross-product-limit", "t02-normalized-design-and-rates"]
resolves_concepts: ["polynomial-cointegration", "im-ols-framework"]
source_dossiers: ["phillips-hansen-1990", "stock-watson-1993", "vogelsang-wagner-2014", "wagner-hong-2016", "stypka-et-al-2025"]
audit_questions: ["2.1", "2.2", "2.3", "3.1", "3.2", "3.3"]
proof_status: "local-derivation-complete"
simulation_status: "smoke-failed-full-pending"
outcome: null
mathematical_status: "open"
scholarly_status: "awaiting-peer-review"
finite_sample_status:
  t50: "unsupported"
  t100: "unsupported"
---
# T03 — Estimator Extension to the Cross-Product Design

## Formal setup

For the exact project equation,
$$
y_t=a+b k_t+f\omega_t+d(k_t\omega_{t-1})+u_t,
$$
let $s_t=(k_t,\omega_t)'$, $v_t=\Delta s_t$, and
$q_t=(1,k_t,\omega_t,k_t\omega_{t-1})'$.  The locally derived estimator is
restricted to the branch in which both components of $s_t$ are $I(1)$.

## Assumptions

- The stationary vector $(u_t,v_t')'$ obeys a joint functional central
  limit theorem and has finite $4+\delta$ moments.
- Its innovation long-run covariance $\Omega_{vv}$ is nonsingular.
- The normalized augmented design has a positive limiting minimum eigenvalue.
- The interaction lag is fixed at one, so it disappears from the continuous
  path limit but is retained exactly in every finite sample.
- The $I(0)$ wage-share branch is diagnostic-only.

## Lemmas

The long-run projection and a Beveridge–Nelson remainder give
$$
U_t=\sum_{j=1}^t u_j
  =\lambda's_t+U_{u\cdot v,t}+o_p(T^{1/2}),
\qquad
\lambda=\Omega_{vv}^{-1}\Omega_{vu}.
$$
Consequently the two base integrated levels, not a fictitious stationary
$\Delta(k_t\omega_{t-1})$, are the required nuisance augmentation.

Writing $Q_t=\sum_{j=1}^tq_j$, the column orders of
$(Q_t',s_t')'$ are
$$
(T,T^{3/2},T^{3/2},T^2,T^{1/2},T^{1/2}).
$$
They imply the coefficient-rate matrix
$$
R_T=\operatorname{diag}(T^{1/2},T,T,T^{3/2})
$$
for $(a,b,f,d)$.

## Derivation

The implemented cumulative regression is
$$
Y_t=a\,t+bK_t+fW_t+dZ_t+
  \lambda_k k_t+\lambda_\omega\omega_t+\varepsilon_t,
$$
where $Y_t=\sum_{j\le t}y_j$, $K_t=\sum_{j\le t}k_j$,
$W_t=\sum_{j\le t}\omega_j$, and
$Z_t=\sum_{j\le t}k_j\omega_{j-1}$.

After column normalization, the limiting augmented row is
$$
\mathcal H(r)=
\left(
r,\int_0^rB_k,\int_0^rB_\omega,
\int_0^rB_kB_\omega,B_k(r),B_\omega(r)
\right)'.
$$
Continuous mapping then produces the local mixed limit
$$
\left(\int_0^1\mathcal H\mathcal H'\right)^{-1}
\int_0^1\mathcal H(r)B_{u\cdot v}(r)\,dr.
$$
The first four coordinates correspond to
$R_T(\widehat\beta-\beta)$; the final two nuisance coefficients need not be
consistent for a structural parameter.

The code solves the normalized system and transforms estimates back to the
original parameterization. Its covariance uses the integrated-error kernel
$\min(r,s)$. A Bartlett fixed-$b$ experiment and a circular joint
moving-block bootstrap are independent inference implementations.

## Rank conditions

The numerical gate is evaluated on the normalized six-column design. A
regression is refused when it is not full column rank, its minimum normalized
eigenvalue is at most $10^{-10}$, or its condition number exceeds
$10^{12}$. The singular-common-trend experiment must be refused. A
generalized inverse may be used to diagnose the failure but never to report
structural inference.

## Degenerate cases

- If $\omega_t$ is $I(0)$, its cumulative column and the interaction have
  different stochastic orders from this theorem. The implementation labels
  the result diagnostic-only.
- A local-to-unity wage share is reported separately because a short sample
  cannot reliably select the $I(0)$ or $I(1)$ theorem.
- Cointegrated $k_t$ and $\omega_t$, a singular common trend, and weak
  interaction variation can destroy the assumed rank.

## Peer-reviewed evidence

Vogelsang–Wagner (2014), DOI
[10.1016/j.jeconom.2013.10.015](https://doi.org/10.1016/j.jeconom.2013.10.015),
supports linear IM-OLS and fixed-$b$ inference. Wagner–Hong (2016) and
Stypka et al. (2025), DOI
[10.1017/S0266466624000033](https://doi.org/10.1017/S0266466624000033),
support their stated additive CPR classes. None of these papers is represented
as a peer-reviewed theorem for the exact distinct-variable interaction above.

## Simulation design

The committed harness covers $T=40,50,60,80,100,120,200,500,1000$;
innovation correlations $0,0.5,0.9$; serial coefficients $0,0.5$;
moderate and strong endogeneity; Gaussian and standardized Student-$t_5$
innovations; and the prespecified degenerate cases. The full profile uses
10,000 rate/fixed-$b$ replications and nested bootstrap calibration. The
smoke profile cannot change this task's verdict.

## Results

The fixed-$b$ simulator includes the nonvanishing randomness of its Bartlett
long-run-variance estimator and the fitted-level-residual adjustment. In the
250-replication smoke calibration, coefficient coverage ranges from 90.4% to
95.2% at $T=50$ and from 92.0% to 95.2% at $T=100$, inside the
prespecified fixed-$b$ anchor band. The 250-outer, 99-inner bootstrap covers
only 82.0–94.0% at $T=50$ and 81.2–90.8% at $T=100$. The methods therefore
fail the mandatory agreement gate, while some asymptotic fixed-$b$ smoke
cells also overcover. The neighboring fixed-$b$ range falls to 88.4–92.8%
at $T=60$, and bootstrap coverage remains below target throughout the
40–120 grid. Finite-sample status remains `unsupported`.

## Verdict

**Locally derived, not locally validated.** The exact augmented estimator and
mixed limit are now explicit and executable. Mathematical closure remains
open because the full calibration has not passed, and scholarly closure
remains blocked pending peer review.

## Concept-note implications

The estimator may be used only as a local research implementation. It must
report the integration-regime and rank gates, both inference methods, and the
finite-sample warning. It is not yet an authoritative empirical estimator.

## Remaining gaps

- Complete the full fixed-$b$ and nested-bootstrap calibration.
- Establish whether the observed undercoverage persists asymptotically.
- Develop a separate hybrid estimator theorem for $I(0)$ wage shares.
- Obtain peer review for the distinct-variable cross-product extension.

## Related notes

- [IM-OLS Framework](../../concepts/im-ols-framework.md) · [[im-ols-framework|IM-OLS Framework]]
- [T02 — Normalized design and rates](t02-normalized-design-and-rates.md) · [[t02-normalized-design-and-rates|T02 — Normalized design and rates]]
- [T04 — Transformed FWL](t04-transformed-fwl.md) · [[t04-transformed-fwl|T04 — Transformed FWL]]
- [Estimator experiment](../results/t03-imols-summary.csv)
