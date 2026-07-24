---
schema_version: 2
id: "stypka-et-al-2025"
title: "Stypka et al. (2025)"
type: "source-dossier"
status: "validated"
aliases: ["CPR robustness of fully modified OLS"]
tags: ["econometrics", "fm-ols", "peer-reviewed"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "local"
publication_status: "peer-reviewed"
citation_key: "stypka-et-al-2025"
doi: "10.1017/S0266466624000033"
notebooklm_source_id: null
reviewed: true
audit_questions: ["2.2", "2.3", "3.1"]
---
# Stypka et al. (2025)

## Bibliographic identity

Stypka, O., Wagner, M., Grabarczyk, P., and Kawka, R. (2025),
“Cointegrating Polynomial Regressions: Robustness of Fully Modified OLS,”
*Econometric Theory* 41, 688–708.

## Main contributions

- Gives an asymptotic foundation for formal FM-OLS in the paper’s CPR class.
- Uses a kernel-weighted limit and a functional central limit theorem.
- Requires inclusion of every degree-one integrated regressor.

## Critical insights for the I(2) validation

The robustness result is important for powered CPR terms but does not erase the
need to verify that the exact lagged cross-product belongs to the stated model
class and satisfies its rank assumptions.

## Formal results, assumptions, and rank conditions

Formal FM-OLS and the CPR-specific fully modified estimator share a zero-mean
Gaussian-mixture limit under the paper’s assumptions. The project must not
extend that equivalence beyond the stated polynomial design without proof.

## Limitations and prohibited inferences

This dossier records no peer-reviewed theorem for arbitrary cross-products of
distinct integrated variables.

## Audit links

Questions: `2.2`, `2.3`, `3.1`.

## Related notes

- [IM-OLS Framework](../../../concepts/im-ols-framework.md) · [[im-ols-framework|IM-OLS Framework]]
- [T03 — Estimator extension](../../../theory/tasks/t03-estimator-extension.md) · [[t03-estimator-extension|T03 — Estimator extension]]
