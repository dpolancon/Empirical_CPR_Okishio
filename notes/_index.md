---
id: econometric-knowledge-index
type: knowledge_index
status: active
aliases: ["Econometric Knowledge Index", "I2 Audit Index"]
last_reviewed: 2026-07-23
---
# Econometric Knowledge Index

This repository separates immutable inputs, generated audit evidence, and
human-reviewed knowledge. NotebookLM output is evidence, not an authoritative
claim, until it is promoted into a reviewed concept note.

## Lifecycle

1. **Source snapshots:** immutable `E_00` and `E_01` copies plus their hash manifest.
2. **Source intelligence:** 13 review-gated audit dossiers plus one explicitly
   excluded out-of-scope source.
3. **Audit evidence:** the append-only master ledger under `working_ledgers/notebooklm/`.
4. **Canonical concepts:** atomic, human-reviewed econometric claims under `concepts/`.

## Review statuses

| Status | Meaning |
|---|---|
| `awaiting_audit` | Structure exists, but NotebookLM evidence has not been reviewed. |
| `under_review` | Evidence is being checked against the cited source. |
| `validated` | The claim and its conditions have passed human review. |
| `disputed` | Evidence conflicts or the claim is not supported. |
| `excluded` | The source is outside the econometric audit corpus. |

The completed NotebookLM run contains 13 source-intelligence responses and 18
phase answers. All 18 proposed validation metrics failed, so the concept notes
remain `under_review` rather than `validated`.

## Related concept notes

- [The I(2) Trap](../concepts/i2_trap.md) · [[i2_trap]]
- [Polynomial Cointegration](../concepts/polynomial_cointegration.md) · [[polynomial_cointegration]]
- [IM-OLS Framework](../concepts/im_ols_framework.md) · [[im_ols_framework]]
- [FWL Orthogonalization](../concepts/fwl_orthogonalization.md) · [[fwl_orthogonalization]]
- [CPR Cointegration Testing](../concepts/cpr_cointegration_testing.md) · [[cpr_cointegration_testing]]
- [State-Dependent Inference](../concepts/state_dependent_inference.md) · [[state_dependent_inference]]

## Related source snapshots

- [E_00 I(2) Trap](source_snapshots/i2_trap/E_00_I2_Trap.md) · [[E_00_I2_Trap]]
- [E_01 I(2) Trap](source_snapshots/i2_trap/E_01_I2_Trap.md) · [[E_01_I2_Trap]]
- [Snapshot manifest](source_snapshots/i2_trap/manifest.json)

## Related source intelligence

- [Industrial policy beyond the hegemons — excluded](source_intelligence/industrial-policy-beyond-hegemons.md) · [[industrial-policy-beyond-hegemons]]
- [Grabarczyk dissertation](source_intelligence/grabarczyk-dissertation.md) · [[grabarczyk-dissertation]]
- [E_00 source dossier](source_intelligence/e00-i2-trap-snapshot.md) · [[e00-i2-trap-snapshot]]
- [E_01 source dossier](source_intelligence/e01-i2-trap-snapshot.md) · [[e01-i2-trap-snapshot]]
- [Engle–Granger (1987)](source_intelligence/engle-granger-1987.md) · [[engle-granger-1987]]
- [Paruolo (1996)](source_intelligence/paruolo-1996.md) · [[paruolo-1996]]
- [Pedroni (2000)](source_intelligence/pedroni-2000.md) · [[pedroni-2000]]
- [Phillips–Hansen (1990)](source_intelligence/phillips-hansen-1990.md) · [[phillips-hansen-1990]]
- [Saikkonen (1991)](source_intelligence/saikkonen-1991.md) · [[saikkonen-1991]]
- [Stock–Watson (1993)](source_intelligence/stock-watson-1993.md) · [[stock-watson-1993]]
- [Vogelsang–Wagner (2014)](source_intelligence/vogelsang-wagner-2014.md) · [[vogelsang-wagner-2014]]
- [Wagner (2023)](source_intelligence/wagner-2023.md) · [[wagner-2023]]
- [Wagner–Hong (2016)](source_intelligence/wagner-hong-2016.md) · [[wagner-hong-2016]]
- [de Jong–Wagner (2025)](source_intelligence/de-jong-wagner-2025.md) · [[de-jong-wagner-2025]]
