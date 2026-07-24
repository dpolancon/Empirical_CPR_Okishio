# T03 Rate–Bias Monte Carlo Diagnostic

## Scope and preregistration

This is a falsification-oriented diagnostic of the cross-product scaling, coefficient-rate, MSE-rate, and endogeneity claims. It does not prove a theorem and does not promote T03 from its blocked/open status.

- Seed: `20260724`
- Replications: `2000`
- Sample sizes: `50, 100, 250, 500, 1000`
- Batch size: `250`
- Slope-bootstrap replications: `2000`
- Structural parameters `BETA`: `[0.5, 1.0, -0.75, 0.25]`
- Error recursion: `u_t = 0.5 u_(t-1) + epsilon_u,t`
- The first lagged interaction observation uses `omega_0 = 0`.

The innovation covariance matrices, verified symmetric and positive definite before simulation, are:

```text
Sigma_0 = [[1.0, 0.5, 0.0], [0.5, 1.0, 0.0], [0.0, 0.0, 1.0]]
Sigma_E = [[1.0, 0.5, 0.7], [0.5, 1.0, 0.7], [0.7, 0.7, 1.0]]
```

Common standard-normal draws were transformed by explicit Cholesky factors. Because both scenarios share the same upper-left 2×2 block, the integrated regressor paths are identical across scenarios; only their relation to the error innovation changes.

## Estimators

1. `levels-OLS`: the complete levels design `[1, x_t, omega_t, x_t omega_(t-1)]`.
2. `cumulative-OLS-diagnostic`: cumulative dependent and structural columns only. This is not called IM-OLS.
3. `augmented-cross-product-IM-OLS`: the canonical cumulative design plus unaccumulated `x_t` and `omega_t` nuisance-projection columns.

All estimators use normalized Gram-matrix gates: full numerical rank, minimum eigenvalue above `1e-10`, and condition number below `1e+12`. Failed draws are recorded and excluded rather than rescued with a generalized inverse.

## Cross-product scaling

| Scenario | Metric | Primary exponent | Full-grid exponent | Reference |
|---|---|---:|---:|---:|
| exogenous-error | q_T | 0.975 | 1.02 | 1 |
| exogenous-error | partial_sum_q | 1.99 | 2.01 | 2 |
| severe-endogeneity | q_T | 0.975 | 1.02 | 1 |
| severe-endogeneity | partial_sum_q | 1.99 | 2.01 | 2 |

`T=50` is included as a stress point but is not decisive asymptotic evidence. The primary exponents use T=250,500,1000.

## Interaction-coefficient convergence

| Estimator | Scenario | Metric | Primary slope | 95% bootstrap CI | Reference | ±0.15 flag |
|---|---|---|---:|---:|---:|---|
| levels-OLS | exogenous-error | rmse | -1.47 | [-1.51, -1.42] | -1.5 | True |
| levels-OLS | exogenous-error | mse | -2.93 | [-3.03, -2.84] | -3 | True |
| levels-OLS | severe-endogeneity | rmse | -1.34 | [-1.39, -1.28] | -1.5 | False |
| levels-OLS | severe-endogeneity | mse | -2.67 | [-2.78, -2.57] | -3 | False |
| cumulative-OLS-diagnostic | exogenous-error | rmse | -1.64 | [-1.76, -1.52] | -1.5 | True |
| cumulative-OLS-diagnostic | exogenous-error | mse | -3.29 | [-3.52, -3.05] | -3 | False |
| cumulative-OLS-diagnostic | severe-endogeneity | rmse | -1.56 | [-1.64, -1.48] | -1.5 | True |
| cumulative-OLS-diagnostic | severe-endogeneity | mse | -3.12 | [-3.3, -2.96] | -3 | True |
| augmented-cross-product-IM-OLS | exogenous-error | rmse | -1.64 | [-1.76, -1.51] | -1.5 | True |
| augmented-cross-product-IM-OLS | exogenous-error | mse | -3.27 | [-3.53, -3.02] | -3 | False |
| augmented-cross-product-IM-OLS | severe-endogeneity | rmse | -1.64 | [-1.77, -1.51] | -1.5 | True |
| augmented-cross-product-IM-OLS | severe-endogeneity | mse | -3.28 | [-3.53, -3.02] | -3 | False |

A slope near −3 describes the decay of total squared error. It does not establish that the centered limit is unbiased: a bias of order T^(-3/2) contributes to MSE at exactly order T^(-3).

Full-grid and adjacent-sample local slopes are retained in the slopes CSV.

## Endogeneity diagnostic

| Estimator | Classification | T=500 scaled effect (95% CI) | T=1000 scaled effect (95% CI) |
|---|---|---:|---:|
| levels-OLS | NO_DETECTABLE_EFFECT | 0.267 [-2.28, 2.71] | -1.23 [-3.77, 1.28] |
| cumulative-OLS-diagnostic | NO_DETECTABLE_EFFECT | -0.206 [-2, 1.72] | -1.04 [-2.79, 0.581] |
| augmented-cross-product-IM-OLS | SUPPORTED_IN_THIS_DGP | -0.0879 [-0.963, 0.817] | -0.487 [-1.29, 0.312] |

The augmented estimator is classified as `SUPPORTED_IN_THIS_DGP` only when both T=500 and T=1000 confidence intervals include zero and its absolute scaled effect is smaller than both comparators. This is evidence for this DGP, not a general result.
The levels and unaugmented estimators also have confidence intervals that include zero at T=500 and T=1000. Thus this DGP does not detect a nonzero asymptotic mean-bias contrast for either comparator; the augmented classification follows the prespecified relative-effect rule and should not be read as evidence that the other two retain a nonzero mean bias.

Cumulation alone is not treated as an endogeneity correction. The canonical local derivation attributes correction to the augmented projection structure.

## T=50 finite-sample stress point

| Estimator | Scenario | Bias | RMSE | Scaled bias | Scaled RMSE |
|---|---|---:|---:|---:|---:|
| augmented-cross-product-IM-OLS | exogenous-error | 0.0016 | 0.121 | 0.564 | 42.6 |
| augmented-cross-product-IM-OLS | severe-endogeneity | 0.00152 | 0.0762 | 0.537 | 26.9 |
| cumulative-OLS-diagnostic | exogenous-error | 0.000903 | 0.122 | 0.319 | 43.2 |
| cumulative-OLS-diagnostic | severe-endogeneity | 0.0026 | 0.115 | 0.919 | 40.8 |
| levels-OLS | exogenous-error | -0.000578 | 0.0476 | -0.205 | 16.8 |
| levels-OLS | severe-endogeneity | -0.000835 | 0.0698 | -0.295 | 24.7 |

## Rank and numerical failures

| Estimator | Scenario | Rank failures | Numerical failures |
|---|---|---:|---:|
| augmented-cross-product-IM-OLS | exogenous-error | 0 | 0 |
| augmented-cross-product-IM-OLS | severe-endogeneity | 0 | 0 |
| cumulative-OLS-diagnostic | exogenous-error | 0 | 0 |
| cumulative-OLS-diagnostic | severe-endogeneity | 0 | 0 |
| levels-OLS | exogenous-error | 0 | 0 |
| levels-OLS | severe-endogeneity | 0 | 0 |

## Claim adjudication

- Cross-product level and partial-sum scaling: `SUPPORTED` under the prespecified exponent tolerance.
- T^(-3/2) RMSE rate for `levels-OLS`, `exogenous-error`: `SUPPORTED_IN_THIS_DGP`.
- T^(-3) MSE rate for `levels-OLS`, `exogenous-error`: `SUPPORTED_IN_THIS_DGP`.
- T^(-3/2) RMSE rate for `levels-OLS`, `severe-endogeneity`: `REJECTED_IN_THIS_DGP`.
- T^(-3) MSE rate for `levels-OLS`, `severe-endogeneity`: `REJECTED_IN_THIS_DGP`.
- T^(-3/2) RMSE rate for `cumulative-OLS-diagnostic`, `exogenous-error`: `INCONCLUSIVE`.
- T^(-3) MSE rate for `cumulative-OLS-diagnostic`, `exogenous-error`: `REJECTED_IN_THIS_DGP`.
- T^(-3/2) RMSE rate for `cumulative-OLS-diagnostic`, `severe-endogeneity`: `SUPPORTED_IN_THIS_DGP`.
- T^(-3) MSE rate for `cumulative-OLS-diagnostic`, `severe-endogeneity`: `SUPPORTED_IN_THIS_DGP`.
- T^(-3/2) RMSE rate for `augmented-cross-product-IM-OLS`, `exogenous-error`: `INCONCLUSIVE`.
- T^(-3) MSE rate for `augmented-cross-product-IM-OLS`, `exogenous-error`: `REJECTED_IN_THIS_DGP`.
- T^(-3/2) RMSE rate for `augmented-cross-product-IM-OLS`, `severe-endogeneity`: `INCONCLUSIVE`.
- T^(-3) MSE rate for `augmented-cross-product-IM-OLS`, `severe-endogeneity`: `REJECTED_IN_THIS_DGP`.
- Augmented-projection endogeneity claim: `SUPPORTED_IN_THIS_DGP`.

These results cannot automatically promote T03. The task remains a local research extension with unresolved fixed-b/bootstrap calibration and scholarly-closure requirements beyond this rate/bias DGP.

## Reproducibility and executed commands

- `git status --short` → exit status `0`
- `git branch --show-current` → exit status `0`
- `python -m code.theory.t03_rate_bias_diagnostic --replications 20 --sample-sizes 50 100 250 500 1000 --batch-size 10 --bootstrap-replications 50 --output /tmp/t03-rate-bias-smoke` → exit status `0`
- `python -m pytest -q` → exit status `1 (pytest missing)`
- `python -m pip install --target /tmp/t03-pytest pytest==8.4.2` → exit status `0`
- `PYTHONPATH=/tmp/t03-pytest MPLCONFIGDIR=/tmp/matplotlib-cache python -m pytest -q` → exit status `1 (one diagnostic test failed before repair)`
- `PYTHONPATH=/tmp/t03-pytest MPLCONFIGDIR=/tmp/matplotlib-cache python -m pytest -q` → exit status `0 (12 passed)`
- `python code/validate_note_repository.py` → exit status `1 (notebooklm missing)`
- `python -m pip install --target /tmp/t03-note-deps 'notebooklm-py[browser]==0.5.0'` → exit status `0`
- `PYTHONPATH=/tmp/t03-note-deps python code/validate_note_repository.py` → exit status `1 (T01/T03 top-level notes missing frontmatter; NotebookLM views/attempts migration targets missing)`
- `MPLCONFIGDIR=/tmp/matplotlib-cache python -m code.theory.t03_rate_bias_diagnostic --seed 20260724 --replications 2000 --sample-sizes 50 100 250 500 1000 --batch-size 250 --bootstrap-replications 2000` → exit status `0`
- `PYTHONPATH=/tmp/t03-pytest MPLCONFIGDIR=/tmp/matplotlib-cache python -m pytest -q` → exit status `0 (12 passed after report repair)`
- `python -m code.theory.t03_rate_bias_diagnostic --seed 20260724 --replications 2000 --sample-sizes 50 100 250 500 1000 --batch-size 250 --bootstrap-replications 2000 --record-command git status --short::0 --record-command git branch --show-current::0 --record-command python -m code.theory.t03_rate_bias_diagnostic --replications 20 --sample-sizes 50 100 250 500 1000 --batch-size 10 --bootstrap-replications 50 --output /tmp/t03-rate-bias-smoke::0 --record-command python -m pytest -q::1 (pytest missing) --record-command python -m pip install --target /tmp/t03-pytest pytest==8.4.2::0 --record-command PYTHONPATH=/tmp/t03-pytest MPLCONFIGDIR=/tmp/matplotlib-cache python -m pytest -q::1 (one diagnostic test failed before repair) --record-command PYTHONPATH=/tmp/t03-pytest MPLCONFIGDIR=/tmp/matplotlib-cache python -m pytest -q::0 (12 passed) --record-command python code/validate_note_repository.py::1 (notebooklm missing) --record-command python -m pip install --target /tmp/t03-note-deps 'notebooklm-py[browser]==0.5.0'::0 --record-command PYTHONPATH=/tmp/t03-note-deps python code/validate_note_repository.py::1 (T01/T03 top-level notes missing frontmatter; NotebookLM views/attempts migration targets missing) --record-command MPLCONFIGDIR=/tmp/matplotlib-cache python -m code.theory.t03_rate_bias_diagnostic --seed 20260724 --replications 2000 --sample-sizes 50 100 250 500 1000 --batch-size 250 --bootstrap-replications 2000::0 --record-command PYTHONPATH=/tmp/t03-pytest MPLCONFIGDIR=/tmp/matplotlib-cache python -m pytest -q::0 (12 passed after report repair)` → exit status `0 (artifact generation reached)`

Software versions are recorded in the diagnostic manifest. Raw replication draws were not written or committed.
