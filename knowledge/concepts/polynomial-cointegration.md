---
schema_version: 2
id: "polynomial-cointegration"
title: "Polynomial Cointegration"
type: "concept"
status: "under-review"
aliases: ["Polynomial Cointegration", "polynomial_cointegration", "CPR"]
tags: ["econometrics", "cpr", "i2-trap-audit"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_snapshots: ["e-00-i2-trap", "e-01-i2-trap"]
source_dossiers: ["wagner-hong-2016", "phillips-hansen-1990", "saikkonen-1991"]
audit_questions: ["1.1", "1.2", "2.1", "2.2", "2.3"]
theory_tasks: ["t01-cross-product-limit", "t02-normalized-design-and-rates", "t03-estimator-extension"]
---
# Polynomial Cointegration

> Review-gated correction. The established CPR results do not automatically
> cover the project's cross-product interaction.

## Formal claim

A standard CPR contains deterministic terms and integer powers of underlying
\(I(1)\) processes with an \(I(0)\) regression error. Wagner–Hong derives
FM-OLS for an additively separable basis and explicitly excludes cross-products
of distinct integrated regressors.

## Assumptions and rank conditions

- Stationary innovations \(\eta_t=(u_t,v_t')'\) with a finite long-run
  covariance matrix.
- Positive-definite innovation covariance and a nondegenerate normalized
  polynomial design.
- Additive separability for the published Wagner–Hong result.
- A full-row-rank scaled restriction \(G_RRG\to R^*\) for Wald inference.

## Proof or theorem evidence

Wagner–Hong supplies the FM-CPR transformation and mixed-normal limit for
powers of \(I(1)\) regressors. Questions `2.1`–`2.3` reject asymptotic DOLS
rank failure, LRCV estimation on nonstationary levels, and FM-OLS with an
integrated regression error.

## Audit verdict

**Qualified fail.** CPR is a valid framework for the source's polynomial
basis, but the notes' interaction-specific extension and claimed DOLS/FM-OLS
failure mechanisms are unsupported.

## Required correction

State the additive-separability boundary explicitly. Treat DOLS regressor
proliferation as a finite-sample concern, and estimate FM corrections from
stationary innovations rather than an alleged \(I(2)\) spectral density.

## Implementation implications

Do not apply FM-CPR, DOLS, or their standard errors to the cross-product model
until its normalized moment limits and correction terms are derived.

## Unresolved questions

- No uploaded source proves the exact interaction-product case.
- The appropriate FM correction and rate matrix for a cross-product of
  distinct \(I(1)\) processes remain to be established.

## Related notes

- [Wagner–Hong (2016)](../sources/dossiers/notebooklm/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Phillips–Hansen (1990)](../sources/dossiers/notebooklm/phillips-hansen-1990.md) · [[phillips-hansen-1990]]
- [Saikkonen (1991)](../sources/dossiers/notebooklm/saikkonen-1991.md) · [[saikkonen-1991]]
- [The I(2) Trap](i2-trap.md) · [[i2-trap|The I(2) Trap]]
