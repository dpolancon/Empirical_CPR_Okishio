"""Falsification-oriented Monte Carlo diagnostic for T01/T03 rate and bias claims.

This module is deliberately separate from the canonical ``run-manifest.json``
workflow.  It compares levels OLS, a clearly labelled unaugmented cumulative
OLS diagnostic, and the repository's augmented cross-product IM-OLS design.
The experiment can reject the rates and endogeneity claims it investigates;
it does not update the blocked/open status of T03.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np
import pandas as pd
import scipy
from scipy.signal import lfilter

matplotlib.use("Agg")
from matplotlib import pyplot as plt

from .imols import (
    BETA,
    COEFFICIENTS,
    coefficient_rates,
    fit_cross_product_imols,
    fit_naive_ols,
    level_design,
)


DEFAULT_SEED = 20260724
DEFAULT_REPLICATIONS = 2_000
DEFAULT_SAMPLE_SIZES = (50, 100, 250, 500, 1_000)
DEFAULT_BATCH_SIZE = 250
DEFAULT_BOOTSTRAP_REPLICATIONS = 2_000
PRIMARY_SAMPLE_SIZES = (250, 500, 1_000)
RATE_TOLERANCE = 0.15
RANK_TOLERANCE = 1e-10
CONDITION_LIMIT = 1e12
ERROR_SERIAL_COEFFICIENT = 0.5

LEVELS_OLS = "levels-OLS"
CUMULATIVE_OLS_DIAGNOSTIC = "cumulative-OLS-diagnostic"
AUGMENTED_IMOLS = "augmented-cross-product-IM-OLS"
ESTIMATORS = (LEVELS_OLS, CUMULATIVE_OLS_DIAGNOSTIC, AUGMENTED_IMOLS)

SCENARIO_COVARIANCES = {
    "exogenous-error": np.array(
        [[1.0, 0.5, 0.0], [0.5, 1.0, 0.0], [0.0, 0.0, 1.0]],
        dtype=float,
    ),
    "severe-endogeneity": np.array(
        [[1.0, 0.5, 0.7], [0.5, 1.0, 0.7], [0.7, 0.7, 1.0]],
        dtype=float,
    ),
}

ARTIFACT_NAMES = {
    "summary": "t03-rate-bias-diagnostic-summary.csv",
    "slopes": "t03-rate-bias-diagnostic-slopes.csv",
    "scaling": "t03-rate-bias-diagnostic-scaling.csv",
    "manifest": "t03-rate-bias-diagnostic-manifest.json",
    "convergence_figure": "t03-rate-bias-convergence.png",
    "endogeneity_figure": "t03-rate-bias-endogeneity.png",
    "report": "t03-rate-bias-diagnostic-report.md",
}


@dataclass(frozen=True)
class DiagnosticConfig:
    seed: int = DEFAULT_SEED
    replications: int = DEFAULT_REPLICATIONS
    sample_sizes: tuple[int, ...] = DEFAULT_SAMPLE_SIZES
    batch_size: int = DEFAULT_BATCH_SIZE
    bootstrap_replications: int = DEFAULT_BOOTSTRAP_REPLICATIONS
    output: Path = Path("03B_econometrics_validation/theory/results")
    command_log: tuple[str, ...] = ()


@dataclass(frozen=True)
class BatchFit:
    estimates: np.ndarray
    rank_failure: np.ndarray
    numerical_failure: np.ndarray
    minimum_eigenvalue: np.ndarray
    condition_number: np.ndarray


def validate_covariance_matrices() -> dict[str, np.ndarray]:
    """Validate and return explicit Cholesky factors for both DGP scenarios."""

    factors: dict[str, np.ndarray] = {}
    for name, covariance in SCENARIO_COVARIANCES.items():
        if not np.allclose(covariance, covariance.T, atol=0.0, rtol=0.0):
            raise ValueError(f"{name} covariance matrix is not symmetric")
        eigenvalues = np.linalg.eigvalsh(covariance)
        if not np.all(eigenvalues > 0.0):
            raise ValueError(f"{name} covariance matrix is not positive definite")
        factors[name] = np.linalg.cholesky(covariance)
    return factors


def lagged_interaction_batch(
    capital: np.ndarray, wage_share: np.ndarray
) -> np.ndarray:
    """Construct x_t * omega_{t-1}, using zero for the first lag."""

    capital = np.asarray(capital, dtype=float)
    wage_share = np.asarray(wage_share, dtype=float)
    if capital.ndim != 2 or capital.shape != wage_share.shape:
        raise ValueError("capital and wage_share must be equal-shape matrices")
    lagged = np.zeros_like(wage_share)
    lagged[:, 1:] = wage_share[:, :-1]
    return capital * lagged


def level_design_batch(capital: np.ndarray, wage_share: np.ndarray) -> np.ndarray:
    interaction = lagged_interaction_batch(capital, wage_share)
    return np.stack(
        (np.ones_like(capital), capital, wage_share, interaction), axis=2
    )


def generate_scenario_batch(
    standard_normals: np.ndarray, cholesky: np.ndarray
) -> dict[str, np.ndarray]:
    """Generate one scenario without any loop over the time dimension."""

    innovations = np.asarray(standard_normals, dtype=float) @ cholesky.T
    capital = np.cumsum(innovations[:, :, 0], axis=1)
    wage_share = np.cumsum(innovations[:, :, 1], axis=1)
    disturbance = lfilter(
        [1.0],
        [1.0, -ERROR_SERIAL_COEFFICIENT],
        innovations[:, :, 2],
        axis=1,
    )
    design = level_design_batch(capital, wage_share)
    y = np.einsum("bti,i->bt", design, BETA) + disturbance
    return {
        "capital": capital,
        "wage_share": wage_share,
        "disturbance": disturbance,
        "design": design,
        "y": y,
    }


def _fit_normalized_batch(
    design: np.ndarray,
    dependent: np.ndarray,
    scales: np.ndarray,
    structural_columns: int,
) -> BatchFit:
    """Fit a normalized batched system and refuse failed rank gates."""

    design = np.asarray(design, dtype=float)
    dependent = np.asarray(dependent, dtype=float)
    scales = np.asarray(scales, dtype=float)
    replications, sample_size, columns = design.shape
    if dependent.shape != (replications, sample_size):
        raise ValueError("dependent array does not match the batched design")
    if scales.shape != (columns,):
        raise ValueError("column scales do not match the batched design")

    normalized = design / scales[None, None, :]
    gram = np.einsum("bti,btj->bij", normalized, normalized) / sample_size
    eigenvalues = np.linalg.eigvalsh(gram)
    minimum = eigenvalues[:, 0]
    maximum = eigenvalues[:, -1]
    condition = maximum / np.maximum(minimum, np.finfo(float).eps)
    rank_failure = (
        (minimum <= RANK_TOLERANCE)
        | (condition >= CONDITION_LIMIT)
        | ~np.isfinite(condition)
    )
    numerical_failure = np.zeros(replications, dtype=bool)
    estimates = np.full((replications, structural_columns), np.nan)
    supported = np.flatnonzero(~rank_failure)
    if supported.size:
        score = (
            np.einsum(
                "bti,bt->bi", normalized[supported], dependent[supported]
            )
            / sample_size
        )
        try:
            normalized_coefficients = np.linalg.solve(
                gram[supported], score[..., None]
            )[..., 0]
            coefficients = normalized_coefficients / scales[None, :]
            finite = np.all(np.isfinite(coefficients), axis=1)
            estimates[supported[finite]] = coefficients[finite, :structural_columns]
            numerical_failure[supported[~finite]] = True
        except np.linalg.LinAlgError:
            for local_index, replication in enumerate(supported):
                try:
                    normalized_coefficient = np.linalg.solve(
                        gram[replication], score[local_index]
                    )
                    coefficient = normalized_coefficient / scales
                    if np.all(np.isfinite(coefficient)):
                        estimates[replication] = coefficient[:structural_columns]
                    else:
                        numerical_failure[replication] = True
                except np.linalg.LinAlgError:
                    numerical_failure[replication] = True
    return BatchFit(
        estimates=estimates,
        rank_failure=rank_failure,
        numerical_failure=numerical_failure,
        minimum_eigenvalue=minimum,
        condition_number=condition,
    )


def fit_estimators_batch(
    y: np.ndarray, capital: np.ndarray, wage_share: np.ndarray
) -> dict[str, BatchFit]:
    """Fit the three prespecified estimators with the canonical numerical gates."""

    sample_size = y.shape[1]
    levels = level_design_batch(capital, wage_share)
    cumulative = np.cumsum(levels, axis=1)
    cumulative_y = np.cumsum(y, axis=1)
    augmented = np.concatenate(
        (cumulative, capital[:, :, None], wage_share[:, :, None]), axis=2
    )
    return {
        LEVELS_OLS: _fit_normalized_batch(
            levels,
            y,
            np.array(
                [1.0, sample_size**0.5, sample_size**0.5, float(sample_size)]
            ),
            4,
        ),
        CUMULATIVE_OLS_DIAGNOSTIC: _fit_normalized_batch(
            cumulative,
            cumulative_y,
            np.array(
                [
                    float(sample_size),
                    sample_size**1.5,
                    sample_size**1.5,
                    sample_size**2.0,
                ]
            ),
            4,
        ),
        AUGMENTED_IMOLS: _fit_normalized_batch(
            augmented,
            cumulative_y,
            np.array(
                [
                    float(sample_size),
                    sample_size**1.5,
                    sample_size**1.5,
                    sample_size**2.0,
                    sample_size**0.5,
                    sample_size**0.5,
                ]
            ),
            4,
        ),
    }


def _log_slope(sample_sizes: list[int], values: list[float]) -> float:
    if len(sample_sizes) < 2 or any(value <= 0.0 for value in values):
        return float("nan")
    return float(
        np.polyfit(
            np.log(np.asarray(sample_sizes, dtype=float)),
            np.log(np.asarray(values, dtype=float)),
            1,
        )[0]
    )


def _slope_from_matrix(log_x: np.ndarray, log_y: np.ndarray) -> np.ndarray:
    centered = log_x - np.mean(log_x)
    return np.sum(log_y * centered[None, :], axis=1) / np.sum(centered**2)


def _bootstrap_slope_ci(
    errors_by_size: dict[int, np.ndarray],
    sample_sizes: tuple[int, ...],
    metric: str,
    rng: np.random.Generator,
    replications: int,
) -> tuple[float, float]:
    if any(size not in errors_by_size for size in sample_sizes):
        return float("nan"), float("nan")
    if any(errors_by_size[size].size < 2 for size in sample_sizes):
        return float("nan"), float("nan")
    log_x = np.log(np.asarray(sample_sizes, dtype=float))
    slopes: list[np.ndarray] = []
    for start in range(0, replications, 200):
        count = min(200, replications - start)
        boot_values = []
        for sample_size in sample_sizes:
            errors = errors_by_size[sample_size]
            indices = rng.integers(
                0, errors.size, size=(count, errors.size), endpoint=False
            )
            mse = np.mean(errors[indices] ** 2, axis=1)
            boot_values.append(np.sqrt(mse) if metric == "rmse" else mse)
        log_y = np.log(np.maximum(np.column_stack(boot_values), 1e-300))
        slopes.append(_slope_from_matrix(log_x, log_y))
    array = np.concatenate(slopes)
    return float(np.quantile(array, 0.025)), float(np.quantile(array, 0.975))


def _bootstrap_mean_ci(
    values: np.ndarray,
    rng: np.random.Generator,
    replications: int,
) -> tuple[float, float]:
    if values.size < 2:
        return float("nan"), float("nan")
    means: list[np.ndarray] = []
    for start in range(0, replications, 200):
        count = min(200, replications - start)
        indices = rng.integers(
            0, values.size, size=(count, values.size), endpoint=False
        )
        means.append(np.mean(values[indices], axis=1))
    array = np.concatenate(means)
    return float(np.quantile(array, 0.025)), float(np.quantile(array, 0.975))


def _summary_row(
    estimator: str,
    scenario: str,
    sample_size: int,
    coefficient: str,
    estimates: np.ndarray,
    rank_failures: int,
    numerical_failures: int,
) -> dict[str, Any]:
    coefficient_index = COEFFICIENTS.index(coefficient)
    truth = float(BETA[coefficient_index])
    finite = estimates[np.isfinite(estimates)]
    if finite.size == 0:
        values = {
            key: float("nan")
            for key in (
                "mean_estimate",
                "mean_bias",
                "median_estimation_error",
                "bias_mcse",
                "empirical_variance",
                "mse",
                "rmse",
                "scaled_mean_bias",
                "scaled_rmse",
                "scaled_error_q025",
                "scaled_error_q05",
                "scaled_error_q25",
                "scaled_error_q50",
                "scaled_error_q75",
                "scaled_error_q95",
                "scaled_error_q975",
            )
        }
    else:
        error = finite - truth
        scaled = coefficient_rates(sample_size)[coefficient_index] * error
        variance = float(np.var(finite, ddof=1)) if finite.size > 1 else float("nan")
        mse = float(np.mean(error**2))
        quantiles = np.quantile(
            scaled, [0.025, 0.05, 0.25, 0.50, 0.75, 0.95, 0.975]
        )
        values = {
            "mean_estimate": float(np.mean(finite)),
            "mean_bias": float(np.mean(error)),
            "median_estimation_error": float(np.median(error)),
            "bias_mcse": (
                float(np.std(error, ddof=1) / math.sqrt(error.size))
                if error.size > 1
                else float("nan")
            ),
            "empirical_variance": variance,
            "mse": mse,
            "rmse": math.sqrt(mse),
            "scaled_mean_bias": float(np.mean(scaled)),
            "scaled_rmse": float(np.sqrt(np.mean(scaled**2))),
            "scaled_error_q025": float(quantiles[0]),
            "scaled_error_q05": float(quantiles[1]),
            "scaled_error_q25": float(quantiles[2]),
            "scaled_error_q50": float(quantiles[3]),
            "scaled_error_q75": float(quantiles[4]),
            "scaled_error_q95": float(quantiles[5]),
            "scaled_error_q975": float(quantiles[6]),
        }
    return {
        "estimator": estimator,
        "scenario": scenario,
        "sample_size": sample_size,
        "coefficient": coefficient,
        "true_value": truth,
        "successful_replications": int(finite.size),
        "rank_failures": int(rank_failures),
        "numerical_failures": int(numerical_failures),
        **values,
    }


def _classify_endogeneity(
    rows: list[dict[str, Any]],
) -> dict[str, str]:
    by_key = {
        (row["estimator"], int(row["sample_size"])): row for row in rows
    }
    classifications: dict[str, str] = {}
    for estimator in ESTIMATORS:
        target_rows = [by_key.get((estimator, size)) for size in (500, 1_000)]
        if any(row is None or not np.isfinite(row["ci_low"]) for row in target_rows):
            classifications[estimator] = "INCONCLUSIVE"
            continue
        includes_zero = all(
            row["ci_low"] <= 0.0 <= row["ci_high"] for row in target_rows
        )
        if estimator == AUGMENTED_IMOLS:
            smaller = all(
                abs(row["scaled_bias_difference"])
                < abs(by_key[(comparison, int(row["sample_size"]))]["scaled_bias_difference"])
                for row in target_rows
                for comparison in (LEVELS_OLS, CUMULATIVE_OLS_DIAGNOSTIC)
            )
            classifications[estimator] = (
                "SUPPORTED_IN_THIS_DGP"
                if includes_zero and smaller
                else "NOT_SUPPORTED_IN_THIS_DGP"
            )
        elif includes_zero:
            classifications[estimator] = "NO_DETECTABLE_EFFECT"
        elif all(
            not (row["ci_low"] <= 0.0 <= row["ci_high"]) for row in target_rows
        ):
            classifications[estimator] = "ENDOGENEITY_EFFECT_DETECTED"
        else:
            classifications[estimator] = "INCONCLUSIVE"
    for row in rows:
        row["classification"] = classifications[row["estimator"]]
    return classifications


def _plot_convergence(
    summary: pd.DataFrame, path: Path, sample_sizes: tuple[int, ...]
) -> None:
    interaction = summary[summary["coefficient"] == "interaction"]
    figure, axis = plt.subplots(figsize=(9.5, 6.0))
    colors = {
        LEVELS_OLS: "#0072B2",
        CUMULATIVE_OLS_DIAGNOSTIC: "#D55E00",
        AUGMENTED_IMOLS: "#009E73",
    }
    markers = {"exogenous-error": "o", "severe-endogeneity": "s"}
    for estimator in ESTIMATORS:
        for scenario in SCENARIO_COVARIANCES:
            subset = interaction[
                (interaction["estimator"] == estimator)
                & (interaction["scenario"] == scenario)
            ].sort_values("sample_size")
            axis.loglog(
                subset["sample_size"],
                subset["mse"],
                marker=markers[scenario],
                color=colors[estimator],
                linestyle="-" if scenario == "exogenous-error" else "--",
                label=f"{estimator} — {scenario}",
            )
    anchor_size = 250 if 250 in sample_sizes else sample_sizes[len(sample_sizes) // 2]
    anchor_values = interaction.loc[
        interaction["sample_size"] == anchor_size, "mse"
    ].to_numpy(dtype=float)
    anchor = float(np.nanmedian(anchor_values))
    reference = anchor * (
        np.asarray(sample_sizes, dtype=float) / float(anchor_size)
    ) ** -3.0
    axis.loglog(
        sample_sizes,
        reference,
        color="black",
        linewidth=1.4,
        linestyle=":",
        label=f"slope −3 reference (anchored at observed T={anchor_size})",
    )
    if 50 in sample_sizes:
        axis.axvspan(46, 55, color="gray", alpha=0.12)
        axis.annotate(
            "T=50 stress",
            xy=(50, 0.03),
            xycoords=("data", "axes fraction"),
            xytext=(5, 5),
            textcoords="offset points",
            rotation=90,
            fontsize=8,
            color="dimgray",
        )
    axis.set_xlabel("Sample size T")
    axis.set_ylabel("MSE of interaction coefficient")
    axis.set_title("Cross-product coefficient convergence")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(fontsize=7, ncol=2)
    figure.savefig(path, bbox_inches="tight", dpi=160)
    plt.close(figure)


def _plot_endogeneity(
    summary: pd.DataFrame, endogeneity: pd.DataFrame, path: Path
) -> None:
    interaction = summary[summary["coefficient"] == "interaction"]
    colors = {
        LEVELS_OLS: "#0072B2",
        CUMULATIVE_OLS_DIAGNOSTIC: "#D55E00",
        AUGMENTED_IMOLS: "#009E73",
    }
    figure, axes = plt.subplots(1, 2, figsize=(12.5, 5.0))
    for estimator in ESTIMATORS:
        for scenario, linestyle in (
            ("exogenous-error", "-"),
            ("severe-endogeneity", "--"),
        ):
            subset = interaction[
                (interaction["estimator"] == estimator)
                & (interaction["scenario"] == scenario)
            ].sort_values("sample_size")
            axes[0].loglog(
                subset["sample_size"],
                np.abs(subset["mean_bias"]),
                color=colors[estimator],
                linestyle=linestyle,
                marker="o" if scenario == "exogenous-error" else "s",
                label=f"{estimator} — {scenario}",
            )
        subset = endogeneity[
            endogeneity["estimator"] == estimator
        ].sort_values("sample_size")
        center = subset["scaled_bias_difference"].to_numpy(dtype=float)
        lower = center - subset["ci_low"].to_numpy(dtype=float)
        upper = subset["ci_high"].to_numpy(dtype=float) - center
        axes[1].errorbar(
            subset["sample_size"],
            center,
            yerr=np.vstack((lower, upper)),
            color=colors[estimator],
            marker="o",
            capsize=3,
            label=estimator,
        )
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("Sample size T")
    axes[0].set_ylabel("|raw mean bias|")
    axes[0].set_title("Absolute interaction-coefficient bias")
    axes[0].grid(True, which="both", alpha=0.25)
    axes[0].legend(fontsize=6.8)
    axes[1].set_xscale("log")
    axes[1].axhline(0.0, color="black", linewidth=1.0, linestyle=":")
    axes[1].set_xlabel("Sample size T")
    axes[1].set_ylabel(r"$T^{3/2}[Bias_E-Bias_0]$")
    axes[1].set_title("Endogeneity-induced scaled-bias difference")
    axes[1].grid(True, which="both", alpha=0.25)
    axes[1].legend(fontsize=7)
    figure.savefig(path, bbox_inches="tight", dpi=160)
    plt.close(figure)


def _format_number(value: Any, digits: int = 3) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return "NA"
    return f"{number:.{digits}g}"


def _slope_claim_status(row: dict[str, Any]) -> str:
    """Combine the descriptive tolerance flag with the bootstrap interval."""

    theory = float(row["theoretical_slope"])
    ci_low = float(row["ci_low"])
    ci_high = float(row["ci_high"])
    passes = bool(row["passes_tolerance"])
    interval_available = math.isfinite(ci_low) and math.isfinite(ci_high)
    interval_includes = (
        ci_low <= theory <= ci_high if interval_available else False
    )
    if passes and interval_includes:
        return "SUPPORTED_IN_THIS_DGP"
    if not passes and interval_available and not interval_includes:
        return "REJECTED_IN_THIS_DGP"
    return "INCONCLUSIVE"


def _build_report(
    config: DiagnosticConfig,
    scaling: pd.DataFrame,
    summary: pd.DataFrame,
    slopes: pd.DataFrame,
    endogeneity: pd.DataFrame,
    classifications: dict[str, str],
    executed_commands: list[dict[str, Any]],
) -> str:
    scaling_rates = scaling[
        scaling["sample_size"] == min(config.sample_sizes)
    ][
        [
            "scenario",
            "metric",
            "exponent_primary",
            "exponent_full_grid",
            "theoretical_exponent",
        ]
    ]
    primary_slopes = slopes[
        (slopes["window"] == "primary")
        & (slopes["coefficient"] == "interaction")
    ]
    finite = summary[
        (summary["sample_size"] == 50)
        & (summary["coefficient"] == "interaction")
    ]
    failures = (
        summary.groupby(["estimator", "scenario"], as_index=False)[
            ["rank_failures", "numerical_failures"]
        ]
        .sum()
        .drop_duplicates()
    )
    lines = [
        "# T03 Rate–Bias Monte Carlo Diagnostic",
        "",
        "## Scope and preregistration",
        "",
        (
            "This is a falsification-oriented diagnostic of the cross-product "
            "scaling, coefficient-rate, MSE-rate, and endogeneity claims. It "
            "does not prove a theorem and does not promote T03 from its blocked/open status."
        ),
        "",
        f"- Seed: `{config.seed}`",
        f"- Replications: `{config.replications}`",
        f"- Sample sizes: `{', '.join(map(str, config.sample_sizes))}`",
        f"- Batch size: `{config.batch_size}`",
        f"- Slope-bootstrap replications: `{config.bootstrap_replications}`",
        f"- Structural parameters `BETA`: `{BETA.tolist()}`",
        f"- Error recursion: `u_t = {ERROR_SERIAL_COEFFICIENT} u_(t-1) + epsilon_u,t`",
        "- The first lagged interaction observation uses `omega_0 = 0`.",
        "",
        "The innovation covariance matrices, verified symmetric and positive definite before simulation, are:",
        "",
        "```text",
        f"Sigma_0 = {SCENARIO_COVARIANCES['exogenous-error'].tolist()}",
        f"Sigma_E = {SCENARIO_COVARIANCES['severe-endogeneity'].tolist()}",
        "```",
        "",
        (
            "Common standard-normal draws were transformed by explicit Cholesky "
            "factors. Because both scenarios share the same upper-left 2×2 block, "
            "the integrated regressor paths are identical across scenarios; only "
            "their relation to the error innovation changes."
        ),
        "",
        "## Estimators",
        "",
        "1. `levels-OLS`: the complete levels design `[1, x_t, omega_t, x_t omega_(t-1)]`.",
        (
            "2. `cumulative-OLS-diagnostic`: cumulative dependent and structural "
            "columns only. This is not called IM-OLS."
        ),
        (
            "3. `augmented-cross-product-IM-OLS`: the canonical cumulative design "
            "plus unaccumulated `x_t` and `omega_t` nuisance-projection columns."
        ),
        "",
        (
            "All estimators use normalized Gram-matrix gates: full numerical rank, "
            f"minimum eigenvalue above `{RANK_TOLERANCE:g}`, and condition number "
            f"below `{CONDITION_LIMIT:g}`. Failed draws are recorded and excluded "
            "rather than rescued with a generalized inverse."
        ),
        "",
        "## Cross-product scaling",
        "",
        "| Scenario | Metric | Primary exponent | Full-grid exponent | Reference |",
        "|---|---|---:|---:|---:|",
    ]
    for row in scaling_rates.to_dict("records"):
        lines.append(
            "| {scenario} | {metric} | {primary} | {full} | {theory} |".format(
                scenario=row["scenario"],
                metric=row["metric"],
                primary=_format_number(row["exponent_primary"]),
                full=_format_number(row["exponent_full_grid"]),
                theory=_format_number(row["theoretical_exponent"]),
            )
        )
    lines.extend(
        [
            "",
            (
                "`T=50` is included as a stress point but is not decisive asymptotic "
                "evidence. The primary exponents use T=250,500,1000."
            ),
            "",
            "## Interaction-coefficient convergence",
            "",
            "| Estimator | Scenario | Metric | Primary slope | 95% bootstrap CI | Reference | ±0.15 flag |",
            "|---|---|---|---:|---:|---:|---|",
        ]
    )
    for row in primary_slopes.to_dict("records"):
        lines.append(
            "| {estimator} | {scenario} | {metric} | {slope} | [{low}, {high}] | {theory} | {flag} |".format(
                estimator=row["estimator"],
                scenario=row["scenario"],
                metric=row["metric"],
                slope=_format_number(row["estimated_slope"]),
                low=_format_number(row["ci_low"]),
                high=_format_number(row["ci_high"]),
                theory=_format_number(row["theoretical_slope"]),
                flag=row["passes_tolerance"],
            )
        )
    lines.extend(
        [
            "",
            (
                "A slope near −3 describes the decay of total squared error. It "
                "does not establish that the centered limit is unbiased: a bias "
                "of order T^(-3/2) contributes to MSE at exactly order T^(-3)."
            ),
            "",
            "Full-grid and adjacent-sample local slopes are retained in the slopes CSV.",
            "",
            "## Endogeneity diagnostic",
            "",
            "| Estimator | Classification | T=500 scaled effect (95% CI) | T=1000 scaled effect (95% CI) |",
            "|---|---|---:|---:|",
        ]
    )
    for estimator in ESTIMATORS:
        cells = []
        for sample_size in (500, 1_000):
            subset = endogeneity[
                (endogeneity["estimator"] == estimator)
                & (endogeneity["sample_size"] == sample_size)
            ]
            if subset.empty:
                cells.append("NA")
            else:
                row = subset.iloc[0]
                cells.append(
                    "{value} [{low}, {high}]".format(
                        value=_format_number(row["scaled_bias_difference"]),
                        low=_format_number(row["ci_low"]),
                        high=_format_number(row["ci_high"]),
                    )
                )
        lines.append(
            f"| {estimator} | {classifications[estimator]} | {cells[0]} | {cells[1]} |"
        )
    lines.extend(
        [
            "",
            (
                "The augmented estimator is classified as `SUPPORTED_IN_THIS_DGP` "
                "only when both T=500 and T=1000 confidence intervals include zero "
                "and its absolute scaled effect is smaller than both comparators. "
                "This is evidence for this DGP, not a general result."
            ),
            (
                "The levels and unaugmented estimators also have confidence intervals "
                "that include zero at T=500 and T=1000. Thus this DGP does not detect "
                "a nonzero asymptotic mean-bias contrast for either comparator; the "
                "augmented classification follows the prespecified relative-effect "
                "rule and should not be read as evidence that the other two retain a "
                "nonzero mean bias."
            ),
            "",
            "Cumulation alone is not treated as an endogeneity correction. The canonical local derivation attributes correction to the augmented projection structure.",
            "",
            "## T=50 finite-sample stress point",
            "",
            "| Estimator | Scenario | Bias | RMSE | Scaled bias | Scaled RMSE |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in finite.to_dict("records"):
        lines.append(
            "| {estimator} | {scenario} | {bias} | {rmse} | {sbias} | {srmse} |".format(
                estimator=row["estimator"],
                scenario=row["scenario"],
                bias=_format_number(row["mean_bias"]),
                rmse=_format_number(row["rmse"]),
                sbias=_format_number(row["scaled_mean_bias"]),
                srmse=_format_number(row["scaled_rmse"]),
            )
        )
    lines.extend(
        [
            "",
            "## Rank and numerical failures",
            "",
            "| Estimator | Scenario | Rank failures | Numerical failures |",
            "|---|---|---:|---:|",
        ]
    )
    for row in failures.to_dict("records"):
        lines.append(
            f"| {row['estimator']} | {row['scenario']} | {int(row['rank_failures'])} | {int(row['numerical_failures'])} |"
        )

    q_pass = bool(
        np.all(
            np.abs(
                scaling_rates["exponent_primary"]
                - scaling_rates["theoretical_exponent"]
            )
            <= RATE_TOLERANCE
        )
    )
    lines.extend(
        [
            "",
            "## Claim adjudication",
            "",
            (
                f"- Cross-product level and partial-sum scaling: "
                f"`{'SUPPORTED' if q_pass else 'REJECTED_OR_INCONCLUSIVE'}` "
                "under the prespecified exponent tolerance."
            ),
        ]
    )
    for row in primary_slopes.to_dict("records"):
        claim = "T^(-3/2) RMSE rate" if row["metric"] == "rmse" else "T^(-3) MSE rate"
        lines.append(
            f"- {claim} for `{row['estimator']}`, `{row['scenario']}`: "
            f"`{_slope_claim_status(row)}`."
        )
    lines.extend(
        [
            (
                f"- Augmented-projection endogeneity claim: "
                f"`{classifications[AUGMENTED_IMOLS]}`."
            ),
            "",
            (
                "These results cannot automatically promote T03. The task remains "
                "a local research extension with unresolved fixed-b/bootstrap "
                "calibration and scholarly-closure requirements beyond this rate/bias DGP."
            ),
            "",
            "## Reproducibility and executed commands",
            "",
        ]
    )
    for command in executed_commands:
        lines.append(
            f"- `{command['command']}` → exit status `{command['exit_status']}`"
        )
    lines.extend(
        [
            "",
            "Software versions are recorded in the diagnostic manifest. Raw replication draws were not written or committed.",
            "",
        ]
    )
    return "\n".join(lines)


def _git_value(arguments: list[str], cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def run_diagnostic(config: DiagnosticConfig) -> list[Path]:
    """Run the complete diagnostic and write only compact artifacts."""

    if config.replications <= 0 or config.batch_size <= 0:
        raise ValueError("replications and batch size must be positive")
    if config.bootstrap_replications <= 0:
        raise ValueError("bootstrap replications must be positive")
    sample_sizes = tuple(sorted(set(config.sample_sizes)))
    if any(size < 10 for size in sample_sizes):
        raise ValueError("sample sizes must be at least 10")
    factors = validate_covariance_matrices()
    output = config.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    collected: dict[tuple[str, str, int], list[np.ndarray]] = {}
    failure_counts: dict[tuple[str, str, int], list[int]] = {}
    scaling_values: dict[tuple[str, int, str], list[np.ndarray]] = {}

    for sample_size in sample_sizes:
        rng = np.random.default_rng(
            np.random.SeedSequence([config.seed, 303, sample_size])
        )
        for start in range(0, config.replications, config.batch_size):
            count = min(config.batch_size, config.replications - start)
            standard_normals = rng.standard_normal((count, sample_size, 3))
            for scenario, factor in factors.items():
                draw = generate_scenario_batch(standard_normals, factor)
                interaction = draw["design"][:, :, 3]
                scaling_values.setdefault(
                    (scenario, sample_size, "q_T"), []
                ).append(np.abs(interaction[:, -1]))
                scaling_values.setdefault(
                    (scenario, sample_size, "partial_sum_q"), []
                ).append(np.abs(np.sum(interaction, axis=1)))
                fits = fit_estimators_batch(
                    draw["y"], draw["capital"], draw["wage_share"]
                )
                for estimator, fit in fits.items():
                    key = (estimator, scenario, sample_size)
                    collected.setdefault(key, []).append(fit.estimates)
                    counts = failure_counts.setdefault(key, [0, 0])
                    counts[0] += int(np.sum(fit.rank_failure))
                    counts[1] += int(np.sum(fit.numerical_failure))

    estimate_arrays = {
        key: np.vstack(pieces) for key, pieces in collected.items()
    }
    summary_rows: list[dict[str, Any]] = []
    for (estimator, scenario, sample_size), estimates in estimate_arrays.items():
        rank_failures, numerical_failures = failure_counts[
            (estimator, scenario, sample_size)
        ]
        for coefficient_index, coefficient in enumerate(COEFFICIENTS):
            summary_rows.append(
                _summary_row(
                    estimator,
                    scenario,
                    sample_size,
                    coefficient,
                    estimates[:, coefficient_index],
                    rank_failures,
                    numerical_failures,
                )
            )
    summary = pd.DataFrame(summary_rows).sort_values(
        ["estimator", "scenario", "sample_size", "coefficient"]
    )

    scaling_rows: list[dict[str, Any]] = []
    for scenario in SCENARIO_COVARIANCES:
        for metric, theory in (("q_T", 1.0), ("partial_sum_q", 2.0)):
            medians = {
                sample_size: float(
                    np.median(
                        np.concatenate(
                            scaling_values[(scenario, sample_size, metric)]
                        )
                    )
                )
                for sample_size in sample_sizes
            }
            primary_sizes = tuple(
                size for size in PRIMARY_SAMPLE_SIZES if size in medians
            )
            exponent_primary = _log_slope(
                list(primary_sizes), [medians[size] for size in primary_sizes]
            )
            exponent_full = _log_slope(
                list(sample_sizes), [medians[size] for size in sample_sizes]
            )
            for sample_size in sample_sizes:
                scaling_rows.append(
                    {
                        "scenario": scenario,
                        "sample_size": sample_size,
                        "metric": metric,
                        "median_absolute": medians[sample_size],
                        "exponent_primary": exponent_primary,
                        "exponent_full_grid": exponent_full,
                        "theoretical_exponent": theory,
                        "primary_passes_tolerance": (
                            abs(exponent_primary - theory) <= RATE_TOLERANCE
                            if math.isfinite(exponent_primary)
                            else False
                        ),
                    }
                )
    scaling = pd.DataFrame(scaling_rows)

    slopes_rows: list[dict[str, Any]] = []
    for estimator_index, estimator in enumerate(ESTIMATORS):
        for scenario_index, scenario in enumerate(SCENARIO_COVARIANCES):
            errors_by_size = {
                sample_size: estimate_arrays[
                    (estimator, scenario, sample_size)
                ][:, 3]
                - BETA[3]
                for sample_size in sample_sizes
            }
            metric_values = {
                "mse": {
                    size: float(np.nanmean(errors_by_size[size] ** 2))
                    for size in sample_sizes
                },
                "rmse": {
                    size: float(
                        np.sqrt(np.nanmean(errors_by_size[size] ** 2))
                    )
                    for size in sample_sizes
                },
            }
            for metric, theory in (("rmse", -1.5), ("mse", -3.0)):
                for window, sizes in (
                    (
                        "primary",
                        tuple(size for size in PRIMARY_SAMPLE_SIZES if size in sample_sizes),
                    ),
                    ("full-grid", sample_sizes),
                ):
                    slope = _log_slope(
                        list(sizes), [metric_values[metric][size] for size in sizes]
                    )
                    ci_low = ci_high = float("nan")
                    if window == "primary" and len(sizes) == 3:
                        ci_rng = np.random.default_rng(
                            np.random.SeedSequence(
                                [
                                    config.seed,
                                    707,
                                    estimator_index,
                                    scenario_index,
                                    0 if metric == "rmse" else 1,
                                ]
                            )
                        )
                        ci_low, ci_high = _bootstrap_slope_ci(
                            errors_by_size,
                            sizes,
                            metric,
                            ci_rng,
                            config.bootstrap_replications,
                        )
                    slopes_rows.append(
                        {
                            "estimator": estimator,
                            "scenario": scenario,
                            "coefficient": "interaction",
                            "metric": metric,
                            "window": window,
                            "sample_sizes": " ".join(map(str, sizes)),
                            "estimated_slope": slope,
                            "ci_low": ci_low,
                            "ci_high": ci_high,
                            "theoretical_slope": theory,
                            "absolute_error": abs(slope - theory)
                            if math.isfinite(slope)
                            else float("nan"),
                            "passes_tolerance": (
                                abs(slope - theory) <= RATE_TOLERANCE
                                if math.isfinite(slope)
                                else False
                            ),
                        }
                    )
                for lower, upper in zip(sample_sizes[:-1], sample_sizes[1:]):
                    slope = _log_slope(
                        [lower, upper],
                        [
                            metric_values[metric][lower],
                            metric_values[metric][upper],
                        ],
                    )
                    slopes_rows.append(
                        {
                            "estimator": estimator,
                            "scenario": scenario,
                            "coefficient": "interaction",
                            "metric": metric,
                            "window": "adjacent-local",
                            "sample_sizes": f"{lower} {upper}",
                            "estimated_slope": slope,
                            "ci_low": float("nan"),
                            "ci_high": float("nan"),
                            "theoretical_slope": theory,
                            "absolute_error": abs(slope - theory),
                            "passes_tolerance": abs(slope - theory)
                            <= RATE_TOLERANCE,
                        }
                    )
    slopes = pd.DataFrame(slopes_rows)

    endogeneity_rows: list[dict[str, Any]] = []
    for estimator_index, estimator in enumerate(ESTIMATORS):
        for sample_size in sample_sizes:
            exogenous = estimate_arrays[
                (estimator, "exogenous-error", sample_size)
            ][:, 3]
            endogenous = estimate_arrays[
                (estimator, "severe-endogeneity", sample_size)
            ][:, 3]
            valid = np.isfinite(exogenous) & np.isfinite(endogenous)
            paired_effect = (
                sample_size**1.5 * (endogenous[valid] - exogenous[valid])
            )
            ci_rng = np.random.default_rng(
                np.random.SeedSequence(
                    [config.seed, 808, estimator_index, sample_size]
                )
            )
            ci_low, ci_high = _bootstrap_mean_ci(
                paired_effect, ci_rng, config.bootstrap_replications
            )
            exogenous_bias = float(np.mean(exogenous[valid] - BETA[3]))
            endogenous_bias = float(np.mean(endogenous[valid] - BETA[3]))
            endogeneity_rows.append(
                {
                    "estimator": estimator,
                    "sample_size": sample_size,
                    "paired_successful_replications": int(np.sum(valid)),
                    "exogenous_mean_bias": exogenous_bias,
                    "endogenous_mean_bias": endogenous_bias,
                    "scaled_bias_difference": float(np.mean(paired_effect)),
                    "ci_low": ci_low,
                    "ci_high": ci_high,
                    "ci_includes_zero": ci_low <= 0.0 <= ci_high,
                }
            )
    classifications = _classify_endogeneity(endogeneity_rows)
    endogeneity = pd.DataFrame(endogeneity_rows)
    summary["endogeneity_scaled_bias_difference"] = np.nan
    summary["endogeneity_ci_low"] = np.nan
    summary["endogeneity_ci_high"] = np.nan
    summary["endogeneity_classification"] = ""
    for row in endogeneity_rows:
        mask = (
            (summary["estimator"] == row["estimator"])
            & (summary["sample_size"] == row["sample_size"])
            & (summary["coefficient"] == "interaction")
        )
        summary.loc[mask, "endogeneity_scaled_bias_difference"] = row[
            "scaled_bias_difference"
        ]
        summary.loc[mask, "endogeneity_ci_low"] = row["ci_low"]
        summary.loc[mask, "endogeneity_ci_high"] = row["ci_high"]
        summary.loc[mask, "endogeneity_classification"] = row[
            "classification"
        ]

    summary_path = output / ARTIFACT_NAMES["summary"]
    slopes_path = output / ARTIFACT_NAMES["slopes"]
    scaling_path = output / ARTIFACT_NAMES["scaling"]
    convergence_path = output / ARTIFACT_NAMES["convergence_figure"]
    endogeneity_path = output / ARTIFACT_NAMES["endogeneity_figure"]
    manifest_path = output / ARTIFACT_NAMES["manifest"]
    report_path = output / ARTIFACT_NAMES["report"]
    summary.to_csv(summary_path, index=False)
    slopes.to_csv(slopes_path, index=False)
    scaling.to_csv(scaling_path, index=False)
    _plot_convergence(summary, convergence_path, sample_sizes)
    _plot_endogeneity(summary, endogeneity, endogeneity_path)

    invocation = " ".join(
        [Path(sys.executable).name, "-m", "code.theory.t03_rate_bias_diagnostic"]
        + sys.argv[1:]
    )
    executed_commands = [
        {
            "command": entry.rsplit("::", 1)[0],
            "exit_status": entry.rsplit("::", 1)[1]
            if "::" in entry
            else "recorded-without-status",
        }
        for entry in config.command_log
    ]
    executed_commands.append(
        {"command": invocation, "exit_status": "0 (artifact generation reached)"}
    )
    repo_root = Path(__file__).resolve().parents[2]
    manifest = {
        "schema_version": 1,
        "diagnostic": "t03-rate-bias-diagnostic",
        "seed": config.seed,
        "replications": config.replications,
        "sample_sizes": list(sample_sizes),
        "finite_sample_stress_point": 50,
        "primary_asymptotic_sample_sizes": list(PRIMARY_SAMPLE_SIZES),
        "batch_size": config.batch_size,
        "bootstrap_replications": config.bootstrap_replications,
        "beta": BETA.tolist(),
        "error_serial_coefficient": ERROR_SERIAL_COEFFICIENT,
        "covariance_matrices": {
            name: matrix.tolist()
            for name, matrix in SCENARIO_COVARIANCES.items()
        },
        "cholesky_factors": {
            name: factor.tolist() for name, factor in factors.items()
        },
        "covariance_checks": {
            name: {
                "symmetric": bool(np.allclose(matrix, matrix.T)),
                "positive_definite": bool(
                    np.all(np.linalg.eigvalsh(matrix) > 0.0)
                ),
            }
            for name, matrix in SCENARIO_COVARIANCES.items()
        },
        "estimators": list(ESTIMATORS),
        "unaugmented_estimator_is_canonical_imols": False,
        "rank_gate": {
            "minimum_normalized_eigenvalue": RANK_TOLERANCE,
            "maximum_condition_number": CONDITION_LIMIT,
            "generalized_inverse_used_for_promoted_estimates": False,
        },
        "rate_tolerance": RATE_TOLERANCE,
        "endogeneity_classifications": classifications,
        "raw_draws_written": False,
        "canonical_run_manifest_overwritten": False,
        "t03_status_changed": False,
        "git": {
            "branch": _git_value(["branch", "--show-current"], repo_root),
            "base_commit": _git_value(["rev-parse", "HEAD"], repo_root),
        },
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "executed_commands": executed_commands,
        "artifacts": list(ARTIFACT_NAMES.values()),
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2), encoding="utf-8", newline="\n"
    )
    report_path.write_text(
        _build_report(
            config,
            scaling,
            summary,
            slopes,
            endogeneity,
            classifications,
            executed_commands,
        ),
        encoding="utf-8",
        newline="\n",
    )
    return [
        summary_path,
        slopes_path,
        scaling_path,
        manifest_path,
        convergence_path,
        endogeneity_path,
        report_path,
    ]


def build_argument_parser() -> argparse.ArgumentParser:
    repo_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--replications", type=int, default=DEFAULT_REPLICATIONS)
    parser.add_argument(
        "--sample-sizes",
        nargs="+",
        type=int,
        default=DEFAULT_SAMPLE_SIZES,
    )
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument(
        "--bootstrap-replications",
        type=int,
        default=DEFAULT_BOOTSTRAP_REPLICATIONS,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root
        / "03B_econometrics_validation"
        / "theory"
        / "results",
    )
    parser.add_argument(
        "--record-command",
        action="append",
        default=[],
        help="Record an already executed command as 'command::exit_status'.",
    )
    return parser


def main() -> None:
    arguments = build_argument_parser().parse_args()
    config = DiagnosticConfig(
        seed=arguments.seed,
        replications=arguments.replications,
        sample_sizes=tuple(arguments.sample_sizes),
        batch_size=arguments.batch_size,
        bootstrap_replications=arguments.bootstrap_replications,
        output=arguments.output,
        command_log=tuple(arguments.record_command),
    )
    for path in run_diagnostic(config):
        print(path)


if __name__ == "__main__":
    main()
