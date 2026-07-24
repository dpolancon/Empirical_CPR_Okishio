---
schema_version: 2
id: "t04-transformed-fwl"
title: "T04 — FWL in the Transformed Design"
type: "theory-task"
status: "resolved"
aliases: ["T04 Transformed FWL"]
tags: ["econometrics", "fwl", "linear-algebra"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
sequence: 4
depends_on: ["t02-normalized-design-and-rates"]
resolves_concepts: ["fwl-orthogonalization"]
source_dossiers: ["lovell-1963", "vogelsang-wagner-2014"]
audit_questions: ["4.1", "4.2", "4.3"]
proof_status: "passed"
simulation_status: "passed"
outcome: "proved"
mathematical_status: "locally-proved"
scholarly_status: "peer-reviewed"
finite_sample_status:
  t50: "robust"
  t100: "robust"
---
# T04 — FWL in the Transformed Design

## Formal setup

Let $y=X\alpha+Z\beta+u$, where $X$ contains nuisance columns and $Z$
contains the target columns. Let $S$ be a fixed linear transformation, such
as the cumulative-sum transformation used by an integrated regression.

## Assumptions

- $SX$ has full column rank.
- $Z'S'M_{SX}SZ$ is nonsingular.
- The same transformation $S$ is applied to the outcome and every design
  column.

## Lemmas

The ordinary FWL theorem gives
$$
\widehat\beta
=(Z'M_XZ)^{-1}Z'M_Xy.
$$
Applying it to the transformed regression
$$
Sy=SX\alpha+SZ\beta+Su
$$
gives
$$
\widehat\beta_S
=(Z'S'M_{SX}SZ)^{-1}Z'S'M_{SX}Sy.
$$

## Derivation

Partitioning the transformed normal equations and taking their Schur
complement yields exactly the second expression. Its target covariance block
is the inverse of $Z'S'M_{SX}SZ$.

Residualizing before transformation instead uses $SM_X$. In general,
$$
SM_X\neq M_{SX}S,
$$
because projection onto $\mathcal C(X)^\perp$ need not commute with $S$,
and $S\mathcal C(X)^\perp$ need not equal
$\mathcal C(SX)^\perp$. Equality requires additional commutation/invariant
subspace conditions, not merely linearity of $S$.

## Rank conditions

Both $SX$ and the transformed residualized target $M_{SX}SZ$ require full
column rank. These conditions are finite-sample algebraic prerequisites; T02
supplies the asymptotic rank discipline for the stochastic columns.

## Degenerate cases

- If $S$ is a scalar multiple of an orthogonal operator preserving both
  relevant subspaces, the two operations can commute.
- If $SZ$ lies in $\mathcal C(SX)$, the transformed target is unidentified.
- An invertible $S$ does not by itself imply commutation with $M_X$.

## Peer-reviewed evidence

Lovell (1963), DOI
[10.1080/01621459.1963.10480682](https://doi.org/10.1080/01621459.1963.10480682),
provides the peer-reviewed partial-regression foundation. The extension here is
the direct application of that theorem to the single transformed design.

## Simulation design

A deterministic seeded experiment uses 100 observations, three nuisance
columns, two target columns, and a cumulative-sum matrix $S$. It compares
the full transformed regression, transformed-design FWL, their covariance
blocks, and the two competing residualization operators.

## Results

The maximum coefficient difference is $2.66\times10^{-15}$, and the
covariance-block difference is $2.14\times10^{-17}$, both below $10^{-10}$.
The Frobenius norm of $SM_X-M_{SX}S$ is 14.253, decisively demonstrating
non-commutation.

## Verdict

**Resolved / proved.** FWL is valid inside the transformed regression. The
“residualize first, then transform” shortcut is invalid without a separately
proved commutation condition.

## Concept-note implications

Construct the integrated or otherwise transformed outcome and complete design
first. Residualize the transformed target and outcome against the transformed
nuisance columns.

## Remaining gaps

T03 must still justify the econometric transformation $S$ and covariance
estimator for the cross-product CPR.

## Related notes

- [FWL Orthogonalization](../../concepts/fwl-orthogonalization.md) · [[fwl-orthogonalization|FWL Orthogonalization]]
- [T03 — Estimator extension](t03-estimator-extension.md) · [[t03-estimator-extension|T03 — Estimator extension]]
- [FWL numerical check](../results/t04-fwl-check.json)
