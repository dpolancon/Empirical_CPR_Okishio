---
schema_version: 2
id: "grabarczyk-dissertation"
title: "Grabarczyk Dissertation"
type: "source-dossier"
status: "under-review"
aliases: ["Grabarczyk Dissertation"]
tags: ["econometrics", "source-intelligence"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "notebooklm"
publication_status: "doctoral-dissertation"
citation_key: "grabarczyk-dissertation"
doi: null
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebooklm_source_id: "c96685a6-db4f-40f2-975b-fe53312d9e03"
source_title: "Dissertation_Grabarczyk.pdf"
source_type: "pdf"
reviewed: false
audit_questions: ["1.1", "1.2", "2.1", "2.2", "3.1", "5.2", "5.3"]
---
# Grabarczyk Dissertation

> Curated audit draft; direct source checks completed for the decisive scope
> statements, with human review still required.

## Bibliographic identity

Grabarczyk dissertation on estimation and testing in cointegrating polynomial
regressions; exact degree metadata remains to be verified.

## Main contributions

- Shows that integer powers of integrated processes are not themselves
  conventionally integrated.
- Establishes asymptotic equivalence between FM-LIN and FM-CPR under stated
  bandwidth conditions.
- Extends IM-OLS inference and residual testing to CPRs under “full design.”

## Critical insights for the I(2) validation

The full-design condition can make fixed-$b$ and residual-test limits
nuisance-free, but critical values still depend on kernel, bandwidth,
deterministics, regressor count, and included powers.

## Formal results, assumptions, and rank conditions

FM-LIN equivalence uses a restricted bandwidth growth rate. Full design
requires the polynomial Brownian basis to be representable through a regular
transformation of standard Brownian motions.

## Limitations and prohibited inferences

No generic cross-product interaction theorem was located. Do not reinterpret
the dissertation's power basis as proof for $x_ty_t$.

## Audit links

Questions: `1.1`, `1.2`, `2.1`, `2.2`, `3.1`, `5.2`, `5.3`.

## Related notes

- [Polynomial Cointegration](../../../concepts/polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
- [CPR Cointegration Testing](../../../concepts/cpr-cointegration-testing.md) · [[cpr-cointegration-testing|CPR Cointegration Testing]]
