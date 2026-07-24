---
schema_version: 2
id: "e01-i2-trap-snapshot"
title: "E_01 I(2) Trap Source Dossier"
type: "source-dossier"
status: "under-review"
aliases: ["E01 I2 Trap Source Dossier"]
tags: ["econometrics", "source-intelligence"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "notebooklm"
publication_status: "project-note"
citation_key: "e01-i2-trap-snapshot"
doi: null
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebooklm_source_id: "0c9a6214-5241-4e81-bfab-2a1a343f702c"
source_title: "E_01_I2_Trap.md"
source_type: "markdown"
reviewed: false
audit_questions: ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "3.1", "3.2", "3.3", "4.1", "4.2", "4.3", "5.1", "5.2", "5.3", "6.1", "6.2", "6.3"]
---
# E_01 I(2) Trap Source Dossier

> Curated audit draft for an internal snapshot; it is not independent evidence.

## Bibliographic identity

Project framework snapshot preserved under `03B_econometrics_validation/sources/snapshots/i2-trap/`.

## Main contributions

- Expands E_00 into an estimator and testing protocol.
- Supplies proposed rate matrices, FWL steps, residual tests, and Wald formulas.
- Includes implementation guidance and numerical claims requiring source checks.

## Critical insights for the I(2) validation

All 18 mandatory validation metrics failed. The most consequential errors are
the automatic $I(2)$ label, the IM-OLS extension, FWL commutation, residual
test scaling rationale, and $\sqrt T$ state-dependent inference.

## Formal results, assumptions, and rank conditions

The proposed “Theorem” labels are not substitutes for published results.
Wagner–Hong excludes cross-products, and Vogelsang–Wagner begins from an
$I(1)$ linear cointegrating regression.

## Limitations and prohibited inferences

Do not implement or cite its approximate critical values, simulated values, or
interaction rate claims until a source proves the exact design.

## Audit links

Questions: `1.1`–`6.3`.

## Related notes

- [Immutable E_01 snapshot](../../snapshots/i2-trap/e-01-i2-trap.md) · [[e-01-i2-trap|E_01 I(2) Trap]]
- [The I(2) Trap](../../../concepts/i2-trap.md) · [[i2-trap|The I(2) Trap]]
