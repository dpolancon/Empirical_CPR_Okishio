---
schema_version: 2
id: "engle-granger-1987"
title: "Engle–Granger (1987)"
type: "source-dossier"
status: "under-review"
aliases: ["Engle Granger 1987"]
tags: ["econometrics", "source-intelligence"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "notebooklm"
publication_status: "peer-reviewed"
citation_key: "engle-granger-1987"
doi: null
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebooklm_source_id: "a632dafd-0b06-4e54-a0a5-d1e61958e35f"
source_title: "EngleGranger-CoIntegrationErrorCorrection-1987.pdf"
source_type: "pdf"
reviewed: false
audit_questions: ["1.2", "5.1"]
---
# Engle–Granger (1987)

> Curated audit draft; source-level human verification remains required.

## Bibliographic identity

Engle and Granger (1987), foundational representation and error-correction
results for cointegrated $I(1)$ systems.

## Main contributions

- Connects cointegration to an error-correction representation.
- Characterizes cointegrating vectors through the null space of the long-run
  impact matrix $C(1)$.
- Establishes the two-step long-run/short-run estimation logic.

## Critical insights for the I(2) validation

The paper supplies the definition that a valid cointegrating regression has an
$I(0)$ equilibrium error; it does not validate nonlinear cross-products or
CPR-specific critical values.

## Formal results, assumptions, and rank conditions

For cointegrating rank $r$, $C(1)$ has rank $N-r$ and a cointegrating
vector satisfies $\alpha'C(1)=0$.

## Limitations and prohibited inferences

Do not extend its linear $I(1)$ representation theorem to polynomial or
cross-product regressors without a separate limit theory.

## Audit links

Questions: `1.2`, `5.1`.

## Related notes

- [The I(2) Trap](../../../concepts/i2-trap.md) · [[i2-trap|The I(2) Trap]]
- [CPR Cointegration Testing](../../../concepts/cpr-cointegration-testing.md) · [[cpr-cointegration-testing|CPR Cointegration Testing]]
