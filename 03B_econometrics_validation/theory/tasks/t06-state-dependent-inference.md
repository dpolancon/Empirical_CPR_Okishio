---
schema_version: 2
id: "t06-state-dependent-inference"
title: "T06 — State-Dependent Inference"
type: "theory-task"
status: "blocked"
aliases: ["T06 State Dependent Wald Inference"]
tags: ["econometrics", "delta-method", "wald", "simultaneous-bands"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
sequence: 6
depends_on: ["t02-normalized-design-and-rates", "t03-estimator-extension"]
resolves_concepts: ["state-dependent-inference"]
source_dossiers: ["vogelsang-wagner-2014", "wagner-hong-2016"]
audit_questions: ["6.1", "6.2", "6.3"]
proof_status: "local-derivation-complete"
simulation_status: "smoke-failed-full-pending"
outcome: null
mathematical_status: "open"
scholarly_status: "awaiting-peer-review"
finite_sample_status:
  t50: "unsupported"
  t100: "unsupported"
---
# T06 — State-Dependent Inference

## Formal setup

The project's capital elasticity and inefficiency gap are
$$
\theta(s)=\frac{\partial y}{\partial k}=b+d\,s,
\qquad
\Gamma(s)=1-s-\theta(s)=1-b-(1+d)s.
$$
The previous T06 implementation incorrectly evaluated the marginal effect
with respect to the wage share. The code and mathematical target now agree.

## Assumptions

- T03 provides a centered joint limit and covariance for $(\widehat b,\widehat d)$.
- A reported state is explicitly classified as fixed, integrated and
  observed, or estimated stationary.
- Integrated-path inference uses the joint estimator/state functional limit.
- The same complete normalized design and rank gate used by T03 applies.

## Lemmas

For a fixed $s=O(1)$,
$$
\widehat\theta(s)-\theta(s)
=O_p(T^{-1})+sO_p(T^{-3/2})=O_p(T^{-1}).
$$
For $s_T=\omega_{\lfloor Tr\rfloor}=O_p(T^{1/2})$, both coefficient terms
contribute at order $T^{-1}$. For an estimated stationary state,
$$
\frac{\partial\Gamma}{\partial s}=-(1+d),
$$
so treating the state as fixed generally omits a first-order component.

## Derivation

At a fixed state the elasticity contrast is
$c(s)=(0,1,0,s)'$. Conditional path bands apply this contrast at every
realized $\omega_{t-1}$. Unconditional bands additionally regenerate the
state path in the joint block bootstrap.

Pointwise efficiency uses $H_0:\Gamma(s)=0$. If the integrated state path
has nonzero variation, the uniform null $\Gamma(s)=0$ for the whole path is
equivalent to
$$
H_0:b=1,\qquad d=-1,
$$
and is tested as a two-restriction Wald hypothesis.

## Rank conditions

The contrast must retain rank after applying T02's mixed scaling. A uniform
path restriction is not identified from a constant state. Path bands start at
$$
r_0(T)=\max(0.15,10/T)
$$
to avoid an ill-conditioned initial segment.

## Degenerate cases

- If $d=0$, first-order state-estimation uncertainty in $\theta$ vanishes,
  but the gap still contains the state directly.
- An $I(1)$ wage share has no constant stochastic steady-state mean; a fixed
  value is a policy counterfactual.
- The $I(0)$ branch cannot use the T03 cumulative transformation and remains
  a documented negative diagnostic.

## Peer-reviewed evidence

Vogelsang–Wagner (2014) supports linear IM-OLS inference and Wagner–Hong
(2016) supports scaled restrictions in its additive CPR. The cross-product
estimator/state functional and bands are local extensions, not peer-reviewed
results.

## Simulation design

Fixed states are $0.40,0.50,0.60,0.70$. Pointwise path coverage is evaluated
at fractions $0.25,0.50,0.75,1.00$, and simultaneous conditional and
unconditional coverage uses a supremum-$t$ bootstrap. The uniform-gap test
is generated under $b=1,d=-1$. Samples are
$T=40,50,60,80,100,120,200,500,1000$.

## Results

The corrected target and all three state classifications are implemented.
For $s=0.50$, the 250-replication fixed-$b$ smoke coverage is 94.8% at
$T=50$ and 91.6% at $T=100$. The corresponding 250-outer bootstrap
coverage is 83.2% and 86.8%, so the methods fail the agreement gate.
Conditional path-band coverage is 92.8% and 96.0%, whereas unconditional
bands overcover at 98.8% and 100%. Fixed and pathwise intervals remain
unapproved. Across the complete 40–120 neighborhood, the fixed-state
bootstrap remains below 90% and unconditional bands cover 98–100%.

## Verdict

**Corrected and locally derived, but not validated.** Mathematical status
remains open until T03 and the full coverage experiment pass. Scholarly status
remains awaiting peer review.

## Concept-note implications

All applications must report $\theta(s)=b+ds$, not
$\beta_\omega+s\beta_d$. The gap is $1-b-(1+d)s$. Fixed-state, conditional
path, unconditional path, and estimated-$I(0)$ statements cannot share a
single standard error.

## Remaining gaps

- Complete fixed-$b$ and bootstrap coverage at the full replication counts.
- Resolve T03's observed undercoverage.
- Develop a separate stationary-state estimator before operational $I(0)$
  inference.
- Obtain peer review of the joint cross-product/state limit.

## Related notes

- [State-Dependent Inference](../../concepts/state-dependent-inference.md) · [[state-dependent-inference|State-Dependent Inference]]
- [T03 — Estimator extension](t03-estimator-extension.md) · [[t03-estimator-extension|T03 — Estimator extension]]
- [Fixed-state experiment](../results/t06-fixed-state-inference.csv)
