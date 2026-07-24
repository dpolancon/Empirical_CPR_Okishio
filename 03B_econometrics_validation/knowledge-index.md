---
schema_version: 2
id: "knowledge-index"
title: "Econometric Knowledge Index"
type: "knowledge-index"
status: "under-review"
aliases: ["Econometric Knowledge Index", "econometric-knowledge-index", "I2 Audit Index"]
tags: ["econometrics", "knowledge-graph"]
created: "2026-07-23"
updated: "2026-07-24"
last_reviewed: "2026-07-24"
contains: ["source-index", "concept-index", "theory-index", "i2-trap-validation-walkthrough"]
---
# Econometric Knowledge Index

This repository separates immutable inputs, generated audit evidence, and
human-reviewed knowledge. NotebookLM output is evidence, not an authoritative
claim, until it is promoted into a reviewed concept note.

## Lifecycle

1. Immutable source snapshots and their hash manifest.
2. Source dossiers separated into NotebookLM, local peer-reviewed, and excluded
   collections.
3. The append-only NotebookLM master ledger.
4. Editable canonical concepts.
5. Dependency-ordered theory tasks with proof and simulation evidence.

The completed historical audit contains 13 source-intelligence responses and
18 phase answers. All 18 proposed validation metrics failed, so the current
concepts remain under review.

## Related walkthrough

- [I(2) Trap Validation Walkthrough](bridges/i2-trap-validation-walkthrough.md) · [[i2-trap-validation-walkthrough|I(2) Trap Validation Walkthrough]]

## Related vault navigation

- [Econometrics Validation Vault](vault-home.md) · [[vault-home|Econometrics Validation Vault]]

## Related indexes

- [Source Index](sources/source-index.md) · [[source-index|Source Index]]
- [Concept Index](concepts/concept-index.md) · [[concept-index|Concept Index]]
- [Theory Index](theory/theory-index.md) · [[theory-index|Theory Index]]

## Related source snapshots

- [E_00 I(2) Trap](sources/snapshots/i2-trap/e-00-i2-trap.md) · [[e-00-i2-trap|E_00 I(2) Trap]]
- [E_01 I(2) Trap](sources/snapshots/i2-trap/e-01-i2-trap.md) · [[e-01-i2-trap|E_01 I(2) Trap]]

## Related evidence

- [Canonical NotebookLM audit](evidence/notebooklm/econometric-audit-master.md)
- [Snapshot manifest](sources/snapshots/i2-trap/manifest.json)
- [Evidence manifest](_meta/evidence-manifest.json)
- [Path migration map](_meta/path-migration.json)
