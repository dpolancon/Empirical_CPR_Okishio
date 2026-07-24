from __future__ import annotations

import json

import numpy as np
import pandas as pd

from code.theory.imols import (
    BETA,
    fit_cross_product_imols,
    fit_naive_ols,
    level_design,
)
from code.theory.t03_rate_bias_diagnostic import (
    ARTIFACT_NAMES,
    AUGMENTED_IMOLS,
    CUMULATIVE_OLS_DIAGNOSTIC,
    DiagnosticConfig,
    ESTIMATORS,
    LEVELS_OLS,
    SCENARIO_COVARIANCES,
    fit_estimators_batch,
    generate_scenario_batch,
    lagged_interaction_batch,
    run_diagnostic,
    validate_covariance_matrices,
)


def test_covariance_matrices_are_symmetric_positive_definite():
    factors = validate_covariance_matrices()
    assert set(factors) == set(SCENARIO_COVARIANCES)
    for name, covariance in SCENARIO_COVARIANCES.items():
        np.testing.assert_allclose(covariance, covariance.T)
        assert np.all(np.linalg.eigvalsh(covariance) > 0.0)
        np.testing.assert_allclose(factors[name] @ factors[name].T, covariance)


def test_fixed_seed_draw_is_deterministically_reproducible():
    factor = validate_covariance_matrices()["severe-endogeneity"]
    first_rng = np.random.default_rng(np.random.SeedSequence([20260724, 50]))
    second_rng = np.random.default_rng(np.random.SeedSequence([20260724, 50]))
    first = generate_scenario_batch(first_rng.standard_normal((4, 50, 3)), factor)
    second = generate_scenario_batch(second_rng.standard_normal((4, 50, 3)), factor)
    for key in first:
        np.testing.assert_array_equal(first[key], second[key])


def test_lagged_interaction_matches_scalar_repository_convention():
    capital = np.array([[1.0, 2.0, 3.0], [-1.0, 4.0, 2.0]])
    wage_share = np.array([[0.4, 0.5, 0.6], [0.2, -0.1, 0.3]])
    interaction = lagged_interaction_batch(capital, wage_share)
    np.testing.assert_allclose(
        interaction,
        np.array([[0.0, 0.8, 1.5], [0.0, 0.8, -0.2]]),
    )
    for index in range(capital.shape[0]):
        scalar = level_design(capital[index], wage_share[index])
        np.testing.assert_allclose(interaction[index], scalar[:, 3])


def test_vectorized_estimators_match_scalar_references():
    rng = np.random.default_rng(771)
    factor = validate_covariance_matrices()["severe-endogeneity"]
    draw = generate_scenario_batch(rng.standard_normal((3, 100, 3)), factor)
    fits = fit_estimators_batch(
        draw["y"], draw["capital"], draw["wage_share"]
    )
    for replication in range(3):
        levels_beta, _ = fit_naive_ols(
            draw["y"][replication],
            draw["capital"][replication],
            draw["wage_share"][replication],
        )
        np.testing.assert_allclose(
            fits[LEVELS_OLS].estimates[replication],
            levels_beta,
            rtol=1e-9,
            atol=1e-10,
        )

        scalar_imols = fit_cross_product_imols(
            draw["y"][replication],
            draw["capital"][replication],
            draw["wage_share"][replication],
        )
        assert scalar_imols.rank_supported
        np.testing.assert_allclose(
            fits[AUGMENTED_IMOLS].estimates[replication],
            scalar_imols.beta,
            rtol=2e-8,
            atol=2e-9,
        )

        cumulative_design = np.cumsum(
            level_design(
                draw["capital"][replication],
                draw["wage_share"][replication],
            ),
            axis=0,
        )
        cumulative_y = np.cumsum(draw["y"][replication])
        scalar_unaugmented = np.linalg.lstsq(
            cumulative_design, cumulative_y, rcond=1e-12
        )[0]
        np.testing.assert_allclose(
            fits[CUMULATIVE_OLS_DIAGNOSTIC].estimates[replication],
            scalar_unaugmented,
            rtol=2e-8,
            atol=2e-9,
        )


def test_unaugmented_estimator_is_not_mislabeled_imols():
    assert CUMULATIVE_OLS_DIAGNOSTIC == "cumulative-OLS-diagnostic"
    assert "IM-OLS" not in CUMULATIVE_OLS_DIAGNOSTIC
    assert AUGMENTED_IMOLS in ESTIMATORS


def test_rank_failure_is_recorded_without_promoted_estimate():
    rng = np.random.default_rng(91)
    capital = np.cumsum(rng.standard_normal((4, 50)), axis=1)
    wage_share = capital.copy()
    design = np.stack(
        [
            np.ones_like(capital),
            capital,
            wage_share,
            lagged_interaction_batch(capital, wage_share),
        ],
        axis=2,
    )
    y = np.einsum("bti,i->bt", design, BETA)
    fits = fit_estimators_batch(y, capital, wage_share)
    for fit in fits.values():
        assert np.all(fit.rank_failure)
        assert np.all(np.isnan(fit.estimates))


def test_small_smoke_run_writes_expected_schemas(tmp_path):
    config = DiagnosticConfig(
        seed=20260724,
        replications=12,
        sample_sizes=(50, 100, 250),
        batch_size=6,
        bootstrap_replications=20,
        output=tmp_path,
        command_log=("python -m pytest -q::0",),
    )
    paths = run_diagnostic(config)
    assert len(paths) == len(ARTIFACT_NAMES)
    assert all(path.is_file() and path.stat().st_size > 0 for path in paths)

    summary = pd.read_csv(tmp_path / ARTIFACT_NAMES["summary"])
    assert {
        "estimator",
        "scenario",
        "sample_size",
        "coefficient",
        "successful_replications",
        "rank_failures",
        "numerical_failures",
        "mean_estimate",
        "mean_bias",
        "bias_mcse",
        "empirical_variance",
        "mse",
        "rmse",
        "scaled_mean_bias",
        "scaled_rmse",
        "scaled_error_q025",
        "scaled_error_q975",
        "endogeneity_scaled_bias_difference",
        "endogeneity_ci_low",
        "endogeneity_ci_high",
        "endogeneity_classification",
    }.issubset(summary.columns)
    assert set(summary["estimator"]) == set(ESTIMATORS)

    slopes = pd.read_csv(tmp_path / ARTIFACT_NAMES["slopes"])
    assert {
        "metric",
        "window",
        "estimated_slope",
        "ci_low",
        "ci_high",
        "theoretical_slope",
        "passes_tolerance",
    }.issubset(slopes.columns)

    scaling = pd.read_csv(tmp_path / ARTIFACT_NAMES["scaling"])
    assert {
        "metric",
        "median_absolute",
        "exponent_primary",
        "exponent_full_grid",
        "theoretical_exponent",
    }.issubset(scaling.columns)

    manifest = json.loads(
        (tmp_path / ARTIFACT_NAMES["manifest"]).read_text(encoding="utf-8")
    )
    assert manifest["seed"] == 20260724
    assert manifest["replications"] == 12
    assert manifest["unaugmented_estimator_is_canonical_imols"] is False
    assert manifest["raw_draws_written"] is False
    assert manifest["canonical_run_manifest_overwritten"] is False
