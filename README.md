# Empirical CPR Okishio

This repository audits the econometric foundations of a cointegrating
polynomial regression with an interaction of integrated variables.

The project separates four kinds of material:

- [`knowledge/sources/`](knowledge/sources/source-index.md) records immutable
  snapshots and source dossiers.
- [`knowledge/evidence/`](knowledge/evidence/notebooklm/econometric-audit-master.md)
  preserves the completed NotebookLM audit as append-only evidence.
- [`knowledge/concepts/`](knowledge/concepts/concept-index.md) contains the
  editable scholarly claims.
- [`knowledge/theory/`](knowledge/theory/theory-index.md) contains the
  dependency-ordered mathematical resolution tasks and reproducible checks.

Start with the [knowledge index](knowledge/knowledge-index.md). Generated
NotebookLM views, failed attempts, locally acquired papers, and raw Monte Carlo
draws are intentionally not versioned.

## Main commands

```powershell
python code\partition_audit_ledger.py
python code\validate_note_repository.py
python -m code.theory.run --task all
```

The historical NotebookLM audit is complete and is not rerun as part of the
local theory work.
