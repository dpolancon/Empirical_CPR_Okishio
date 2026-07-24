---
schema_version: 2
id: "de-jong-wagner-2025"
title: "de Jong–Wagner (2025)"
type: "source-dossier"
status: "under-review"
aliases: ["de Jong Wagner 2025", "Multivariate Polynomial IM-OLS"]
tags: ["econometrics", "source-intelligence"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_channel: "notebooklm"
publication_status: "unverified"
citation_key: "de-jong-wagner-2025"
doi: null
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebooklm_source_id: "3966dd86-315e-4c56-b307-88863d1679be"
source_title: "deJongWagner2025.pdf"
source_type: "pdf"
reviewed: false
audit_questions: ["3.1", "3.2", "3.3", "4.2"]
---
# de Jong–Wagner (2025)

> Curated audit draft; source-level human verification remains required.

## Bibliographic identity

NotebookLM source `deJongWagner2025.pdf`; publication identity remains to be
verified from the PDF.

## Main contributions

- Develops modified and fully modified estimators for panel CPRs.
- Uses sequential $T\to\infty$, then $N\to\infty$, asymptotics.
- Extends the panel analysis to individual and time fixed effects.

## Critical insights for the I(2) validation

It does not supply the required time-series IM-OLS theorem for an $I(2)$
cross-product. Its large-$N$ bias correction cannot be imported into the
project's single-country regression.

## Formal results, assumptions, and rank conditions

The reported limit uses $\sqrt N G_T^{-1}(\tilde\beta-\beta)$ after
time-series normalization. The result depends on panel independence and
sequential asymptotics rather than the project's mixed-order FWL design.

## Limitations and prohibited inferences

Do not cite this source for IM-OLS, cross-product integration order, or exact
FWL invariance. Publication status and the precise paper title remain pending.

## Audit links

Questions: `3.1`, `3.2`, `3.3`, `4.2`.

## Related notes

- [IM-OLS Framework](../../../concepts/im-ols-framework.md) · [[im-ols-framework|IM-OLS Framework]]
- [FWL Orthogonalization](../../../concepts/fwl-orthogonalization.md) · [[fwl-orthogonalization|FWL Orthogonalization]]
