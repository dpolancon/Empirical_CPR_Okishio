---
id: i2-trap
type: canonical_concept
status: under_review
aliases: ["I(2) Trap", "i2_trap"]
source_snapshots: ["../notes/source_snapshots/i2_trap/E_00_I2_Trap.md", "../notes/source_snapshots/i2_trap/E_01_I2_Trap.md"]
audit_phases: [1]
audit_questions: ["1.1", "1.2", "1.3"]
last_reviewed: 2026-07-23
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

- [Paruolo (1996)](../notes/source_intelligence/paruolo-1996.md) · [[paruolo-1996]]
- [Wagner–Hong (2016)](../notes/source_intelligence/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [Polynomial Cointegration](polynomial_cointegration.md) · [[polynomial_cointegration]]
