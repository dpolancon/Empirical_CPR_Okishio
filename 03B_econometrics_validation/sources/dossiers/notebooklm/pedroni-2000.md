---
schema_version: 2
id: "pedroni-2000"
title: "Pedroni (2000)"
type: "source-dossier"
status: "under-review"
aliases: ["Pedroni 2000"]
tags: ["econometrics", "source-intelligence"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "notebooklm"
publication_status: "peer-reviewed"
citation_key: "pedroni-2000"
doi: null
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebooklm_source_id: "9d86e85d-b9c0-4aec-b3a0-cbf9533b1155"
source_title: "Pedroni2000.pdf"
source_type: "pdf"
reviewed: false
audit_questions: ["2.2", "5.1"]
---
# Pedroni (2000)

> Curated audit draft; source-level human verification remains required.

## Bibliographic identity

Pedroni (2000), “Fully modified OLS for heterogeneous cointegrated panels.”

## Main contributions

- Develops FM-OLS for heterogeneous $I(1)$ cointegrated panels.
- Corrects panel-specific endogeneity and serial-correlation bias.
- Uses sequential $T$ then $N$ asymptotics.

## Critical insights for the I(2) validation

The estimator transforms stationary innovations in a linear $I(1)$ panel; it
does not provide a cross-product CPR correction.

## Formal results, assumptions, and rank conditions

The result assumes an $I(0)$ cointegrating error and panel-specific long-run
covariance quantities.

## Limitations and prohibited inferences

Do not import sequential panel asymptotics or critical values into the
single-country time-series model.

## Audit links

Questions: `2.2`, `5.1`.

## Related notes

- [Polynomial Cointegration](../../../concepts/polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
- [CPR Cointegration Testing](../../../concepts/cpr-cointegration-testing.md) · [[cpr-cointegration-testing|CPR Cointegration Testing]]
