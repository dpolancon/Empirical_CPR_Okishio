# Empirical CPR Okishio

This repository audits the econometric foundations of a cointegrating
polynomial regression with an interaction of integrated variables.

The project separates four kinds of material:

- [`03B_econometrics_validation/sources/`](03B_econometrics_validation/sources/source-index.md) records immutable
  snapshots and source dossiers.
- [`03B_econometrics_validation/evidence/`](03B_econometrics_validation/evidence/notebooklm/econometric-audit-master.md)
  preserves the completed NotebookLM audit as append-only evidence.
- [`03B_econometrics_validation/concepts/`](03B_econometrics_validation/concepts/concept-index.md) contains the
  editable scholarly claims.
- [`03B_econometrics_validation/theory/`](03B_econometrics_validation/theory/theory-index.md) contains the
  dependency-ordered mathematical resolution tasks and reproducible checks.

Start with the [I(2) trap validation walkthrough](03B_econometrics_validation/bridges/i2-trap-validation-walkthrough.md),
then use the [vault index](03B_econometrics_validation/knowledge-index.md) to inspect the
underlying graph. Generated NotebookLM views, failed attempts, locally acquired
papers, and raw Monte Carlo draws are intentionally not versioned.

## Main commands

```powershell
python code\partition_audit_ledger.py
python code\validate_note_repository.py
python -m code.theory.run --task all
```

The historical NotebookLM audit is complete and is not rerun as part of the
local theory work.

The theory command defaults to the preregistered full profile over
`40 50 60 80 100 120 200 500 1000`. Use the non-promotional smoke profile
while developing:

```powershell
python -m code.theory.run --task t03 --profile smoke --sample-grid all
python -m code.theory.run --task t05 --profile smoke --sample-grid all
python -m code.theory.run --task t06 --profile smoke --sample-grid all
python -m code.theory.run --task t03 t05 t06 --profile smoke --workers 3
```

The full T03/T05/T06 calibration uses nested block bootstraps and supports
`--resume`. A smoke result can expose failures but cannot promote a theory
task or concept note.
