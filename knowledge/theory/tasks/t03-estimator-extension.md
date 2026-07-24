---
schema_version: 2
id: "t03-estimator-extension"
title: "T03 — Estimator Extension to the Cross-Product Design"
type: "theory-task"
status: "blocked"
aliases: ["T03 Cross Product Estimators"]
tags: ["econometrics", "fm-ols", "dols", "im-ols"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
sequence: 3
depends_on: ["t01-cross-product-limit", "t02-normalized-design-and-rates"]
resolves_concepts: ["polynomial-cointegration", "im-ols-framework"]
source_dossiers: ["phillips-hansen-1990", "stock-watson-1993", "vogelsang-wagner-2014", "wagner-hong-2016", "stypka-et-al-2025"]
audit_questions: ["2.1", "2.2", "2.3", "3.1", "3.2", "3.3"]
proof_status: "blocked"
simulation_status: "partial"
outcome: null
---
# T03 — Estimator Extension to the Cross-Product Design

## Formal setup

Consider
\[
y_t=Z_t'\beta+u_t,\qquad
Z_t=(1,x_t,\omega_t,x_t\omega_{t-\ell})',
\]
where \(u_t\) may be contemporaneously correlated with the innovations driving
\(x_t\) and \(\omega_t\), and may be serially correlated.

## Assumptions

- T01 and T02 hold.
- Any proposed correction must be defined from stationary innovation objects.
- A closure result must cover the exact cross-product, fixed lag, complete
  design, and mixed rate matrix.
- Only a peer-reviewed theorem can close this task.

## Lemmas

For a contemporaneous product,
\[
\Delta(x_t\omega_t)
=x_{t-1}\Delta\omega_t+\omega_{t-1}\Delta x_t
 +\Delta x_t\Delta\omega_t.
\]
Hence \(\Delta z_t\) is not generally stationary. It cannot simply be inserted
as another \(I(0)\) first difference in textbook DOLS or FM-OLS.

## Derivation

- **DOLS:** leads and lags of \(\Delta x_t\) and \(\Delta\omega_t\) can address
  their innovation correlation, but a finite augmentation in a naively defined
  \(\Delta z_t\) is not justified because \(\Delta z_t\) has integrated-level
  multipliers.
- **Formal FM-OLS:** treating \((x_t,\omega_t,z_t)\) as a vector of ordinary
  \(I(1)\) regressors violates T01. A robustness theorem must explicitly cover
  the multivariate cross-product.
- **CPR FM-OLS:** Wagner–Hong’s published design is additive in powers of
  individual integrated regressors and excludes distinct cross-products.
- **IM-OLS:** the published 2014 theorem covers linear cointegrating
  regressions. The available arbitrary-cross-product extension is not
  peer-reviewed and therefore cannot satisfy the selected closure rule.

## Rank conditions

Any estimator theorem must use T02’s full normalized design and must state how
the long-run covariance correction interacts with a degree-two cross-product.
A correction derived for a singular or additive-power design is not portable.

## Degenerate cases

Exogenous iid errors make OLS centered and allow the rate experiment in T02,
but this special case does not validate an estimator for endogenous or serially
correlated errors. Stationary \(\omega_t\) changes the problem to a different
mixed stationary/integrated design.

## Peer-reviewed evidence

Phillips–Hansen (1990), Stock–Watson (1993), and Vogelsang–Wagner (2014) cover
linear cointegrating designs. Wagner–Hong (2016) covers additive CPR powers.
Stypka et al. (2025), DOI
[10.1017/S0266466624000033](https://doi.org/10.1017/S0266466624000033),
establishes formal FM-OLS robustness for its stated CPR class but supplies no
verified theorem here for arbitrary products of distinct integrated variables.

## Simulation design

The diagnostic DGP correlates \(u_t\) with the innovation in \(x_t\), uses a
correlation of 0.5 between integrated innovations, and reports conventional
OLS intervals. It deliberately does not pretend to implement a missing
cross-product correction.

## Results

Naive 95% coverage ranges from 70.0% to 81.5% across coefficients and sample
sizes. At \(T=1000\), coverage is 73.8% for \(x_t\), 75.7% for \(\omega_t\),
and 70.0% for the interaction. The failure persists even as coefficient biases
shrink.

## Verdict

**Blocked.** The exact cross-product estimator transformation and its centered
mixed-rate limit are not supported by an admissible peer-reviewed theorem.
Working-paper claims are retained as leads only.

## Concept-note implications

Do not label any DOLS, FM-OLS, or IM-OLS implementation valid for the target
interaction. Empirical work may report exogenous-OLS diagnostics but not
corrected inference until this gate is resolved.

## Remaining gaps

A peer-reviewed cross-product theorem must specify the augmented regression or
fully modified correction, residual adjustment, rate matrix, and covariance
estimator for the exact lagged design.

## Related notes

- [IM-OLS Framework](../../concepts/im-ols-framework.md) · [[im-ols-framework|IM-OLS Framework]]
- [T02 — Normalized design and rates](t02-normalized-design-and-rates.md) · [[t02-normalized-design-and-rates|T02 — Normalized design and rates]]
- [Estimator diagnostic](../results/t03-naive-estimator-diagnostic.csv)
