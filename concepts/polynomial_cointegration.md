---
id: polynomial-cointegration
type: canonical_concept
status: under_review
aliases: ["Polynomial Cointegration", "polynomial_cointegration", "CPR"]
source_snapshots: ["../notes/source_snapshots/i2_trap/E_00_I2_Trap.md", "../notes/source_snapshots/i2_trap/E_01_I2_Trap.md"]
audit_phases: [1, 2]
audit_questions: ["1.1", "1.2", "2.1", "2.2", "2.3"]
last_reviewed: 2026-07-23
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

- [Wagner–Hong (2016)](../notes/source_intelligence/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Phillips–Hansen (1990)](../notes/source_intelligence/phillips-hansen-1990.md) · [[phillips-hansen-1990]]
- [Saikkonen (1991)](../notes/source_intelligence/saikkonen-1991.md) · [[saikkonen-1991]]
- [The I(2) Trap](i2_trap.md) · [[i2_trap]]
