---
schema_version: 2
id: "i2-trap"
title: "The I(2) Trap"
type: "concept"
status: "under-review"
aliases: ["I(2) Trap", "i2_trap"]
tags: ["econometrics", "cpr", "i2-trap-audit"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
source_snapshots: ["e-00-i2-trap", "e-01-i2-trap"]
source_dossiers: ["paruolo-1996", "wagner-hong-2016", "chang-park-phillips-2001", "stypka-wagner-2019"]
audit_questions: ["1.1", "1.2", "1.3"]
theory_tasks: ["t01-cross-product-limit", "t02-normalized-design-and-rates"]
---
# The I(2) Trap

> Review-gated correction. Phase 1 rejects the current notes; human source
> review is still required before this note becomes authoritative.

## Formal claim

For jointly \(I(1)\) levels satisfying a joint FCLT,
\[
T^{-1}x_{\lfloor Tr\rfloor}y_{\lfloor Tr\rfloor}
\Rightarrow B_x(r)B_y(r),\qquad
T^{-2}\sum_{t\leq Tr}x_ty_t\Rightarrow\int_0^rB_x(s)B_y(s)\,ds .
\]
These stochastic orders do not by themselves prove that \(x_ty_t\) is
\(I(2)\) in the conventional difference-stationary sense.

## Assumptions and rank conditions

- A joint invariance principle for the innovations of \(x_t\) and \(y_t\).
- A nondegenerate Brownian product after accounting for common trends.
- A full-rank normalized design for the exact cross-product specification.
- An \(I(0)\) regression error under the proposed cointegrating relation.

## Proof or theorem evidence

Question `1.1` distinguishes the Itô decomposition of the product from the
Riemann-integral limit of its partial sum. Question `1.3` confirms that
normalization stabilizes moment matrices but cannot change the scale-invariant
projection matrix. Wagner–Hong's model excludes cross-products, while
Grabarczyk states that powers of integrated processes are not themselves
integrated processes.

T01 now proves the product and partial-sum functional limits and rejects the
classical \(I(2)\) classification. T02 supplies the conditional full-design
normalization and coefficient rates. Both resolutions remain qualified by
their stated rank and innovation assumptions.

## Audit verdict

**Fail / disputed.** All three Phase 1 validation metrics failed. In
particular, the uploaded notes do not establish a source-backed theorem that
the interaction is a classical \(I(2)\) process.

## Required correction

Replace “\(x_ty_t\sim I(2)\)” with “a product regressor of stochastic order
\(O_p(T)\)” unless a theorem for the exact cross-product design proves the
stronger integration claim. Use \(T^{-2}\) for its partial-sum limit, not
\(T^{-3/2}\), and do not attribute \(\int B_x\,dB_y\) to
\(\sum x_ty_t\).

## Implementation implications

The implementation must use a normalization derived for the cross-product
basis and must not import an \(I(2)\)-VAR rank argument or CPR power result
without proving that it applies to this interaction.

## Unresolved questions

- Which published theorem covers cross-products of distinct integrated
  regressors in this single-equation design?
- Does the exact lagged interaction satisfy a usable joint FCLT and full-design
  condition?

## Related notes

- [Paruolo (1996)](../sources/dossiers/notebooklm/paruolo-1996.md) · [[paruolo-1996]]
- [Wagner–Hong (2016)](../sources/dossiers/notebooklm/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Chang, Park, and Phillips (2001)](../sources/dossiers/local/chang-park-phillips-2001.md) · [[chang-park-phillips-2001|Chang, Park, and Phillips (2001)]]
- [T01 — Cross-product limit](../theory/tasks/t01-cross-product-limit.md) · [[t01-cross-product-limit|T01 — Cross-product limit]]
- [T02 — Normalized design and rates](../theory/tasks/t02-normalized-design-and-rates.md) · [[t02-normalized-design-and-rates|T02 — Normalized design and rates]]
- [Polynomial Cointegration](polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
