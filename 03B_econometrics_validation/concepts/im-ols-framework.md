---
schema_version: 2
id: "im-ols-framework"
title: "IM-OLS Framework"
type: "concept"
status: "under-review"
aliases: ["IM-OLS Framework", "im_ols_framework", "Integrated Modified OLS"]
tags: ["econometrics", "cpr", "i2-trap-audit"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_snapshots: ["e-00-i2-trap", "e-01-i2-trap"]
source_dossiers: ["vogelsang-wagner-2014", "de-jong-wagner-2025", "stypka-et-al-2025"]
audit_questions: ["3.1", "3.2", "3.3"]
theory_tasks: ["t03-estimator-extension"]
---
# IM-OLS Framework

> Review-gated correction. The published IM-OLS theorem is for a conventional
> $I(1)$ cointegrating regression, not the proposed cross-product design.

## Formal claim

Vogelsang–Wagner transforms an $I(1)$ cointegrating regression into
$$
Sy_t=Sf_t'\delta+Sx_t'\beta+x_t'\gamma+Su_t,
$$
where the untransformed $x_t$ augmentation absorbs long-run endogeneity.
The method avoids explicit LRCV estimation for point estimation; this is not a
proof that cumulating an alleged $I(2)$ interaction validates IM-OLS.

## Assumptions and rank conditions

- The original regressor is $I(1)$ and the cointegrating error is $I(0)$.
- The transformed augmented design is full rank.
- Residual adjustment is required for pivotal fixed-$b$ inference.
- Fixed-$b$ critical values depend on bandwidth, kernel, deterministic terms,
  and design.

## Proof or theorem evidence

Vogelsang–Wagner's Theorem 2 supplies the augmented partial-sum estimator.
Question `3.2` establishes that fixed-$b$ inference has nonstandard, simulated
critical values. Question `3.3` records coefficient rates $T$ for $x_t$
and $T^{3/2}$ for $x_t^2$ in the CPR extension.

T03 now supplies a local augmented cumulative design, mixed-rate limit,
normalized rank gate, fixed-$b$ experiment, and joint block bootstrap.
After including fitted-residual fixed-$b$ variance randomness, its
250-replication smoke coverage is 90.4–95.2% at $T=50$ and 92.0–95.2% at
$T=100$. The 250-outer bootstrap covers only 82.0–94.0% and 81.2–90.8%,
respectively, so the mandatory agreement gate fails. The extension is locally
executable but neither locally validated nor peer-reviewed.

## Audit verdict

**Fail for the proposed extension.** Phase 3 rejects the claimed
$I(2)\rightarrow I(3)$ justification, nuisance-parameter “irrelevance,”
standard fixed-$b$ critical values, and the stated rate matrix.

## Required correction

Restrict authoritative IM-OLS claims to the published $I(1)$ model. Treat
T03's distinct-variable transformation and joint rate matrix as local research
work until its full fixed-$b$ and bootstrap gates pass and it is peer
reviewed.

## Implementation implications

Do not implement the E_01 IM-OLS specification as validated. Any exploratory
implementation must be labelled provisional and use simulated critical values
appropriate to the proven design.

## Unresolved questions

- The local joint limit still requires independent scholarly review.
- The observed fixed-$b$ undercoverage remains unresolved.
- The $I(0)$ wage-share branch requires a separate estimator.

## Related notes

- [Vogelsang–Wagner (2014)](../sources/dossiers/notebooklm/vogelsang-wagner-2014.md) · [[vogelsang-wagner-2014]]
- [de Jong–Wagner (2025)](../sources/dossiers/notebooklm/de-jong-wagner-2025.md) · [[de-jong-wagner-2025]]
- [Stypka et al. (2025)](../sources/dossiers/local/stypka-et-al-2025.md) · [[stypka-et-al-2025|Stypka et al. (2025)]]
- [T03 — Estimator extension](../theory/tasks/t03-estimator-extension.md) · [[t03-estimator-extension|T03 — Estimator extension]]
- [Polynomial Cointegration](polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
