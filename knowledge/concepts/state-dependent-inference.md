---
schema_version: 2
id: "state-dependent-inference"
title: "State-Dependent Inference"
type: "concept"
status: "under-review"
aliases: ["State-Dependent Inference", "state_dependent_inference", "Gamma Wald Test"]
tags: ["econometrics", "cpr", "i2-trap-audit"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_snapshots: ["e-00-i2-trap", "e-01-i2-trap"]
source_dossiers: ["wagner-hong-2016", "vogelsang-wagner-2014"]
audit_questions: ["6.1", "6.2", "6.3"]
theory_tasks: ["t06-state-dependent-inference"]
---
# State-Dependent Inference

> Review-gated correction. State-dependent inference must respect the CPR's
> mixed convergence rates.

## Formal claim

If \(\hat b-b=O_p(T^{-1})\),
\(\hat d-d=O_p(T^{-3/2})\), and
\(\omega_{\lfloor Tr\rfloor}=O_p(T^{1/2})\), then
\[
T(\hat\theta_{\lfloor Tr\rfloor}-\theta_{\lfloor Tr\rfloor})
\Rightarrow \mathcal M_b+\mathcal M_dW_\omega(r).
\]
The interaction-estimation error is therefore not negligible for a stochastic
\(I(1)\) evaluation state.

## Assumptions and rank conditions

- Joint convergence of \(\hat b,\hat d\), and the state process.
- Explicit treatment of \(\bar\omega\) as fixed, estimated \(I(0)\), or
  sample-dependent \(I(1)\).
- A scaled restriction matrix with a full-row-rank limit.

## Proof or theorem evidence

Question `6.1` corrects the leading variance order to \(T^{-2}\), not
\(T^{-1}\). Question `6.2` gives the nondegenerate \(T\)-scaled state-process
limit. Question `6.3` shows that, conditional on fixed \(\bar\omega\),
\((1-\bar\omega)-b-d\bar\omega=0\) is a linear restriction.

## Audit verdict

**Fail.** Phase 6 rejects the \(\sqrt T\) delta method, unconditional omission
of \(\operatorname{Var}(\hat d)\), and characterization of the fixed-state
restriction as nonlinear.

## Required correction

Use the joint mixed-rate covariance and state scaling. For fixed
\(\bar\omega\), implement a linear Wald restriction with
\(R=(-1,-\bar\omega)\); verify the scaled-rank condition before asserting a
\(\chi_1^2\) limit.

## Implementation implications

Do not report \(\sqrt T\)-normal confidence bands. Distinguish fixed-state
contrasts from a functional band indexed by an integrated state.

## Unresolved questions

- The exact joint limit depends on the still-unproved interaction CPR.
- The final test must decide whether \(\bar\omega\) is conditioned on or
  estimated jointly.

## Related notes

- [Wagner–Hong (2016)](../sources/dossiers/notebooklm/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Vogelsang–Wagner (2014)](../sources/dossiers/notebooklm/vogelsang-wagner-2014.md) · [[vogelsang-wagner-2014]]
- [IM-OLS Framework](im-ols-framework.md) · [[im-ols-framework|IM-OLS Framework]]
