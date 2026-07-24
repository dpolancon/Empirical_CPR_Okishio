---
schema_version: 2
id: "lovell-1963"
title: "Lovell (1963)"
type: "source-dossier"
status: "validated"
aliases: ["Lovell FWL theorem"]
tags: ["econometrics", "fwl", "peer-reviewed"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "local"
publication_status: "peer-reviewed"
citation_key: "lovell-1963"
doi: "10.1080/01621459.1963.10480682"
notebooklm_source_id: null
reviewed: true
audit_questions: ["4.1", "4.2", "4.3"]
---
# Lovell (1963)

## Bibliographic identity

Lovell, M. C. (1963), “Seasonal Adjustment of Economic Time Series and
Multiple Regression Analysis,” *Journal of the American Statistical
Association* 58, 993–1010.

## Main contributions

- Extends the Frisch–Waugh partial-regression result.
- Identifies when prior linear adjustment agrees with including controls.
- Separates coefficient equivalence from valid variance calculation.

## Critical insights for the I(2) validation

FWL applies to the columns and outcome of one common regression problem. After
an integration or other linear transformation, nuisance projection must be
formed from the transformed nuisance design.

## Formal results, assumptions, and rank conditions

The nuisance and target matrices must have the ranks required by their
projections. Equality follows from the partitioned normal equations.

## Limitations and prohibited inferences

FWL alone supplies no stochastic-rate result for a residualized cross-product.

## Audit links

Questions: `4.1`, `4.2`, `4.3`.

## Related notes

- [FWL Orthogonalization](../../../concepts/fwl-orthogonalization.md) · [[fwl-orthogonalization|FWL Orthogonalization]]
- [T04 — Transformed FWL](../../../theory/tasks/t04-transformed-fwl.md) · [[t04-transformed-fwl|T04 — Transformed FWL]]
