---
id: e01-i2-trap-snapshot
type: source_intelligence
status: under_review
reviewed: false
aliases: ["E01 I2 Trap Source Dossier"]
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebook_source_id: "0c9a6214-5241-4e81-bfab-2a1a343f702c"
source_title: "E_01_I2_Trap.md"
source_type: MARKDOWN
related_audit_phases: [1, 2, 3, 4, 5, 6]
related_audit_questions: ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "3.1", "3.2", "3.3", "4.1", "4.2", "4.3", "5.1", "5.2", "5.3", "6.1", "6.2", "6.3"]
last_reviewed: 2026-07-23
---
# E_01 I(2) Trap Source Dossier

> Curated audit draft for an internal snapshot; it is not independent evidence.

## Bibliographic identity

Project framework snapshot preserved under `notes/source_snapshots/i2_trap/`.

## Main contributions

- Expands E_00 into an estimator and testing protocol.
- Supplies proposed rate matrices, FWL steps, residual tests, and Wald formulas.
- Includes implementation guidance and numerical claims requiring source checks.

## Critical insights for the I(2) validation

All 18 mandatory validation metrics failed. The most consequential errors are
the automatic \(I(2)\) label, the IM-OLS extension, FWL commutation, residual
test scaling rationale, and \(\sqrt T\) state-dependent inference.

## Formal results, assumptions, and rank conditions

The proposed “Theorem” labels are not substitutes for published results.
Wagner–Hong excludes cross-products, and Vogelsang–Wagner begins from an
\(I(1)\) linear cointegrating regression.

## Limitations and prohibited inferences

Do not implement or cite its approximate critical values, simulated values, or
interaction rate claims until a source proves the exact design.

## Audit links

Questions: `1.1`–`6.3`.

## Related notes

- [Immutable E_01 snapshot](../source_snapshots/i2_trap/E_01_I2_Trap.md) · [[E_01_I2_Trap]]
- [The I(2) Trap](../../concepts/i2_trap.md) · [[i2_trap]]
