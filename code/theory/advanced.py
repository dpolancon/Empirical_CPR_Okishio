"""Local T03/T05/T06 experiments for the cross-product IM-OLS extension."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from .imols import (
    BETA,
    COEFFICIENTS,
    automatic_block_length,
    bootstrap_cross_product_imols,
    coefficient_rates,
    cointegration_statistic,
    contrast_standard_error,
    fit_cross_product_imols,
    fit_naive_ols,
    fixed_state_targets,
    level_design,
    simulate_dgp,
    simulate_fixed_b_limit_critical_values,
    simulate_residual_limit_critical_values,
    state_contrast,
)


SMALL_50 = (40, 50, 60)
SMALL_100 = (80, 100, 120)
ASYMPTOTIC = (200, 500, 1000)
ANCHORS = {50, 100, 500, 1000}
FIXED_STATES = (0.40, 0.50, 0.60, 0.70)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _rng(config: Any, task: int, cell: int, sample_size: int, replication: int = 0):
    return np.random.default_rng(
        np.random.SeedSequence(
            [config.seed, task, cell, sample_size, replication]
        )
    )


def _bootstrap_outer(config: Any, sample_size: int) -> int:
    if config.profile == "smoke":
        return min(250, config.replications)
    return 2500 if sample_size <= 120 else 2000


def _bootstrap_draws(config: Any, sample_size: int) -> int:
    if config.bootstrap_replications > 0:
        return config.bootstrap_replications
    if config.profile == "smoke":
        return 99
    return 999 if sample_size <= 120 else 499


def _monte_carlo_se(probability: float, count: int) -> float:
    if count <= 0 or not math.isfinite(probability):
        return float("nan")
    return math.sqrt(probability * (1.0 - probability) / count)


def _safe_skew(values: np.ndarray) -> float:
    if values.size < 3:
        return float("nan")
    centered = values - np.mean(values)
    scale = float(np.std(values))
    if scale <= 0:
        return 0.0
    return float(np.mean((centered / scale) ** 3))


def _slope(sample_sizes: list[int], values: list[float]) -> float:
    if len(sample_sizes) < 2 or any(value <= 0 for value in values):
        return float("nan")
    return float(np.polyfit(np.log(sample_sizes), np.log(values), 1)[0])


def _write_checkpoint(
    config: Any, task: str, key: str, payload: dict[str, Any]
) -> None:
    if not config.resume and config.profile == "smoke":
        return
    directory = config.output / "raw" / "checkpoints" / task
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{key}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8", newline="\n")


def _regular_specs(profile: str) -> list[dict[str, Any]]:
    specs = [
        {
            "name": f"rho-{rho:g}-ar-{serial:g}",
            "rho": rho,
            "serial": serial,
            "endogeneity": 0.6,
            "distribution": "gaussian",
        }
        for rho in (0.0, 0.5, 0.9)
        for serial in (0.0, 0.5)
    ]
    specs.extend(
        [
            {
                "name": "strong-endogeneity",
                "rho": 0.5,
                "serial": 0.5,
                "endogeneity": 0.9,
                "distribution": "gaussian",
            },
            {
                "name": "student-t5",
                "rho": 0.5,
                "serial": 0.5,
                "endogeneity": 0.6,
                "distribution": "student-t5",
            },
        ]
    )
    if profile == "smoke":
        return [specs[0], specs[3]]
    return specs


def _diagnostic_specs() -> list[str]:
    return [
        "stationary-omega",
        "local-to-unity-1",
        "local-to-unity-5",
        "local-to-unity-10",
        "cointegrated-levels",
        "singular-common-trend",
        "weak-interaction",
    ]


def run_t03_local(config: Any) -> list[Path]:
    critical = simulate_fixed_b_limit_critical_values(
        config.seed, config.limit_draws
    )
    critical_path = config.output / "t03-fixed-b-critical-values.json"
    critical_path.write_text(
        json.dumps(
            {
                "draws": config.limit_draws,
                "grid_points": 200,
                "critical_values": critical,
                "scope": "local cross-product IM-OLS Brownian experiment",
            },
            indent=2,
        ),
        encoding="utf-8",
        newline="\n",
    )

    summary_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []
    naive_rows: list[dict[str, Any]] = []
    baseline_rmse: dict[tuple[int, int], float] = {}
    specs = _regular_specs(config.profile)

    for spec_index, spec in enumerate(specs, start=1):
        for sample_size in config.sample_sizes:
            errors: list[np.ndarray] = []
            normalized_errors: list[np.ndarray] = []
            covered: list[np.ndarray] = []
            widths: list[np.ndarray] = []
            naive_covered: list[np.ndarray] = []
            conditions: list[float] = []
            minimum_eigenvalues: list[float] = []
            rank_failures = 0
            numerical_failures = 0
            for replication in range(config.replications):
                rng = _rng(config, 3, spec_index, sample_size, replication)
                draw = simulate_dgp(
                    rng,
                    sample_size,
                    rho=spec["rho"],
                    serial=spec["serial"],
                    endogeneity=spec["endogeneity"],
                    distribution=spec["distribution"],
                )
                fit = fit_cross_product_imols(
                    draw.y, draw.capital, draw.wage_share
                )
                conditions.append(fit.condition_number)
                minimum_eigenvalues.append(fit.minimum_eigenvalue)
                rank_failures += int(not fit.rank_supported)
                numerical_failures += int(fit.numerical_failure)
                if fit.numerical_failure or not fit.rank_supported:
                    continue
                error = fit.beta - BETA
                rates = coefficient_rates(sample_size)
                errors.append(error)
                normalized_errors.append(rates * error)
                standard_errors = np.sqrt(
                    np.maximum(np.diag(fit.covariance), 1e-18)
                )
                coefficient_critical = np.array(
                    [critical[name]["q95"] for name in COEFFICIENTS]
                )
                covered.append(np.abs(error) <= coefficient_critical * standard_errors)
                widths.append(2.0 * coefficient_critical * standard_errors)

                naive_beta, naive_covariance = fit_naive_ols(
                    draw.y, draw.capital, draw.wage_share
                )
                naive_se = np.sqrt(
                    np.maximum(np.diag(naive_covariance), 1e-18)
                )
                naive_covered.append(
                    np.abs(naive_beta - BETA) <= 1.96 * naive_se
                )

            if errors:
                error_array = np.vstack(errors)
                normalized_array = np.vstack(normalized_errors)
                coverage_array = np.vstack(covered)
                width_array = np.vstack(widths)
                naive_array = np.vstack(naive_covered)
                for coefficient, name in enumerate(COEFFICIENTS):
                    values = error_array[:, coefficient]
                    coverage = float(np.mean(coverage_array[:, coefficient]))
                    row = {
                        "scenario": spec["name"],
                        "sample_size": sample_size,
                        "coefficient": name,
                        "method": "fixed-b",
                        "successful_replications": error_array.shape[0],
                        "mean_bias": float(np.mean(values)),
                        "median_bias": float(np.median(values)),
                        "rmse": float(np.sqrt(np.mean(values**2))),
                        "normalized_skewness": _safe_skew(
                            normalized_array[:, coefficient]
                        ),
                        "coverage_95": coverage,
                        "coverage_mc_se": _monte_carlo_se(
                            coverage, error_array.shape[0]
                        ),
                        "mean_interval_length": float(
                            np.mean(width_array[:, coefficient])
                        ),
                        "median_condition_number": float(np.median(conditions)),
                        "median_minimum_eigenvalue": float(
                            np.median(minimum_eigenvalues)
                        ),
                        "rank_failure_rate": rank_failures / config.replications,
                        "numerical_failure_rate": numerical_failures
                        / config.replications,
                    }
                    summary_rows.append(row)
                    if spec["name"] == "rho-0.5-ar-0.5":
                        baseline_rmse[(sample_size, coefficient)] = row["rmse"]
                    if spec_index == 1 and coefficient > 0:
                        naive_coverage = float(
                            np.mean(naive_array[:, coefficient])
                        )
                        naive_rows.append(
                            {
                                "sample_size": sample_size,
                                "coefficient": name,
                                "mean_bias": float(np.mean(values)),
                                "naive_95_coverage": naive_coverage,
                                "passes_coverage_gate": 0.93
                                <= naive_coverage
                                <= 0.97,
                                "interpretation": (
                                    "negative control: conventional OLS covariance "
                                    "ignores endogeneity"
                                ),
                            }
                        )
            _write_checkpoint(
                config,
                "t03",
                f"{spec['name']}-t{sample_size}",
                {
                    "scenario": spec["name"],
                    "sample_size": sample_size,
                    "replications": config.replications,
                    "completed": True,
                },
            )

    baseline_spec_index = next(
        (
            index
            for index, spec in enumerate(specs, start=1)
            if spec["name"] == "rho-0.5-ar-0.5"
        ),
        1,
    )
    for sample_size in config.sample_sizes:
        if config.inference == "fixed-b":
            continue
        outer = _bootstrap_outer(config, sample_size)
        coefficient_coverage: list[np.ndarray] = []
        lengths: list[np.ndarray] = []
        successful_draw_rates: list[float] = []
        for replication in range(outer):
            rng = _rng(config, 33, baseline_spec_index, sample_size, replication)
            draw = simulate_dgp(rng, sample_size)
            fit = fit_cross_product_imols(
                draw.y, draw.capital, draw.wage_share
            )
            if fit.numerical_failure or not fit.rank_supported:
                continue
            bootstrap_rng = _rng(
                config, 303, baseline_spec_index, sample_size, replication
            )
            bootstrap_draws = _bootstrap_draws(config, sample_size)
            estimates, _, _ = bootstrap_cross_product_imols(
                bootstrap_rng,
                draw,
                fit,
                bootstrap_draws,
                block_length=(
                    config.block_length
                    if isinstance(config.block_length, int)
                    else automatic_block_length(sample_size)
                ),
            )
            successful_draw_rates.append(
                estimates.shape[0] / bootstrap_draws
            )
            if estimates.shape[0] < max(10, bootstrap_draws // 2):
                continue
            differences = estimates - fit.beta
            lower = fit.beta - np.quantile(differences, 0.975, axis=0)
            upper = fit.beta - np.quantile(differences, 0.025, axis=0)
            coefficient_coverage.append((lower <= BETA) & (BETA <= upper))
            lengths.append(upper - lower)

        if coefficient_coverage:
            coverage_array = np.vstack(coefficient_coverage)
            length_array = np.vstack(lengths)
            for coefficient, name in enumerate(COEFFICIENTS):
                coverage = float(np.mean(coverage_array[:, coefficient]))
                summary_rows.append(
                    {
                        "scenario": "rho-0.5-ar-0.5",
                        "sample_size": sample_size,
                        "coefficient": name,
                        "method": "moving-block-bootstrap",
                        "successful_replications": coverage_array.shape[0],
                        "coverage_95": coverage,
                        "coverage_mc_se": _monte_carlo_se(
                            coverage, coverage_array.shape[0]
                        ),
                        "mean_interval_length": float(
                            np.mean(length_array[:, coefficient])
                        ),
                        "mean_successful_bootstrap_fraction": float(
                            np.mean(successful_draw_rates)
                        ),
                        "block_length": (
                            config.block_length
                            if isinstance(config.block_length, int)
                            else automatic_block_length(sample_size)
                        ),
                    }
                )

    diagnostic_replications = min(
        config.replications, 100 if config.profile == "smoke" else 1000
    )
    for scenario_index, scenario in enumerate(_diagnostic_specs(), start=50):
        for sample_size in config.sample_sizes:
            supported = 0
            conditions: list[float] = []
            minimums: list[float] = []
            failures = 0
            for replication in range(diagnostic_replications):
                rng = _rng(config, 3, scenario_index, sample_size, replication)
                draw = simulate_dgp(
                    rng, sample_size, scenario=scenario
                )
                fit = fit_cross_product_imols(
                    draw.y, draw.capital, draw.wage_share
                )
                supported += int(fit.rank_supported)
                failures += int(fit.numerical_failure)
                conditions.append(fit.condition_number)
                minimums.append(fit.minimum_eigenvalue)
            diagnostic_rows.append(
                {
                    "scenario": scenario,
                    "sample_size": sample_size,
                    "replications": diagnostic_replications,
                    "rank_supported_rate": supported / diagnostic_replications,
                    "numerical_failure_rate": failures / diagnostic_replications,
                    "median_condition_number": float(np.median(conditions)),
                    "median_minimum_eigenvalue": float(np.median(minimums)),
                    "operational_status": (
                        "diagnostic-only"
                        if scenario.startswith(("stationary", "local-to-unity"))
                        else "must-refuse-if-rank-deficient"
                    ),
                }
            )

    rate_rows: list[dict[str, Any]] = []
    baseline_available = sorted(
        {sample for sample, _ in baseline_rmse}
    )
    groups = {
        "finite-sample-effective": [
            value
            for value in baseline_available
            if value in {*SMALL_50, *SMALL_100}
        ],
        "asymptotic-gate": [
            value for value in baseline_available if value in ASYMPTOTIC
        ],
    }
    expected = (-0.5, -1.0, -1.0, -1.5)
    for group, sizes in groups.items():
        for coefficient, name in enumerate(COEFFICIENTS):
            values = [
                baseline_rmse[(sample_size, coefficient)]
                for sample_size in sizes
                if (sample_size, coefficient) in baseline_rmse
            ]
            used_sizes = [
                sample_size
                for sample_size in sizes
                if (sample_size, coefficient) in baseline_rmse
            ]
            estimate = _slope(used_sizes, values)
            theory = expected[coefficient]
            rate_rows.append(
                {
                    "group": group,
                    "coefficient": name,
                    "sample_sizes": " ".join(map(str, used_sizes)),
                    "estimated_exponent": estimate,
                    "theoretical_exponent": theory,
                    "absolute_error": abs(estimate - theory)
                    if math.isfinite(estimate)
                    else "",
                    "passes_tolerance": (
                        abs(estimate - theory) <= 0.15
                        if group == "asymptotic-gate"
                        and math.isfinite(estimate)
                        else ""
                    ),
                }
            )

    summary_path = config.output / "t03-imols-summary.csv"
    rates_path = config.output / "t03-rate-checks.csv"
    diagnostic_path = config.output / "t03-rank-diagnostics.csv"
    naive_path = config.output / "t03-naive-estimator-diagnostic.csv"
    _write_csv(summary_path, summary_rows)
    _write_csv(rates_path, rate_rows)
    _write_csv(diagnostic_path, diagnostic_rows)
    _write_csv(naive_path, naive_rows)
    return [
        critical_path,
        summary_path,
        rates_path,
        diagnostic_path,
        naive_path,
    ]


def run_t05_local(config: Any) -> list[Path]:
    limit_critical = simulate_residual_limit_critical_values(
        config.seed, config.limit_draws
    )
    scaling_rows: list[dict[str, Any]] = []
    for process_index, process in enumerate(
        ("stationary-residual", "unit-root-residual"), start=1
    ):
        for sample_size in config.sample_sizes:
            values = []
            for replication in range(config.replications):
                rng = _rng(config, 5, process_index, sample_size, replication)
                innovations = rng.standard_normal(sample_size)
                residuals = (
                    innovations
                    if process == "stationary-residual"
                    else np.cumsum(innovations)
                )
                values.append(float(np.sum(np.cumsum(residuals) ** 2)))
            scaling_rows.append(
                {
                    "process": process,
                    "sample_size": sample_size,
                    "median_sum_squared_partial_residual": float(
                        np.median(values)
                    ),
                }
            )
    scaling_rate_rows: list[dict[str, Any]] = []
    for process, theory in (
        ("stationary-residual", 2.0),
        ("unit-root-residual", 4.0),
    ):
        asymptotic_rows = [
            row
            for row in scaling_rows
            if row["process"] == process
            and row["sample_size"] in ASYMPTOTIC
        ]
        estimate = _slope(
            [row["sample_size"] for row in asymptotic_rows],
            [
                row["median_sum_squared_partial_residual"]
                for row in asymptotic_rows
            ],
        )
        scaling_rate_rows.append(
            {
                "process": process,
                "estimated_exponent": estimate,
                "theoretical_exponent": theory,
                "absolute_error": abs(estimate - theory)
                if math.isfinite(estimate)
                else "",
                "passes_tolerance": (
                    abs(estimate - theory) <= 0.15
                    if math.isfinite(estimate)
                    else ""
                ),
                "scope": "oracle scaling check using T=200,500,1000",
            }
        )

    result_rows: list[dict[str, Any]] = []
    critical_rows: list[dict[str, Any]] = [
        {
            "method": "fixed-b-limit",
            "sample_size": "limit",
            "replications": config.limit_draws,
            **limit_critical,
        }
    ]
    fixed_q95 = limit_critical["q95"]
    bootstrap_critical_by_size: dict[int, float] = {}

    for sample_size in config.sample_sizes:
        statistics: list[float] = []
        for replication in range(config.replications):
            rng = _rng(config, 5, 20, sample_size, replication)
            draw = simulate_dgp(rng, sample_size)
            fit = fit_cross_product_imols(
                draw.y, draw.capital, draw.wage_share
            )
            if not fit.numerical_failure and fit.rank_supported:
                statistics.append(cointegration_statistic(fit))
        if statistics:
            rejection = float(np.mean(np.asarray(statistics) > fixed_q95))
            result_rows.append(
                {
                    "sample_size": sample_size,
                    "method": "fixed-b",
                    "experiment": "null-size",
                    "alternative_scale": 0.0,
                    "local_alternative": False,
                    "replications": len(statistics),
                    "rejection_rate": rejection,
                    "monte_carlo_se": _monte_carlo_se(
                        rejection, len(statistics)
                    ),
                    "critical_value": fixed_q95,
                }
            )

        if config.inference != "fixed-b":
            outer = _bootstrap_outer(config, sample_size)
            rejected: list[bool] = []
            critical_values: list[float] = []
            for replication in range(outer):
                rng = _rng(config, 55, 20, sample_size, replication)
                draw = simulate_dgp(rng, sample_size)
                fit = fit_cross_product_imols(
                    draw.y, draw.capital, draw.wage_share
                )
                if fit.numerical_failure or not fit.rank_supported:
                    continue
                observed = cointegration_statistic(fit)
                bootstrap_rng = _rng(
                    config, 505, 20, sample_size, replication
                )
                bootstrap_draws = _bootstrap_draws(config, sample_size)
                _, boot_statistics, _ = bootstrap_cross_product_imols(
                    bootstrap_rng,
                    draw,
                    fit,
                    bootstrap_draws,
                    block_length=(
                        config.block_length
                        if isinstance(config.block_length, int)
                        else automatic_block_length(sample_size)
                    ),
                )
                if boot_statistics.size < max(
                    10, bootstrap_draws // 2
                ):
                    continue
                critical_value = float(np.quantile(boot_statistics, 0.95))
                critical_values.append(critical_value)
                rejected.append(observed > critical_value)
            if rejected:
                rejection = float(np.mean(rejected))
                median_critical = float(np.median(critical_values))
                bootstrap_critical_by_size[sample_size] = median_critical
                result_rows.append(
                    {
                        "sample_size": sample_size,
                        "method": "moving-block-bootstrap",
                        "experiment": "null-size",
                        "alternative_scale": 0.0,
                        "local_alternative": False,
                        "replications": len(rejected),
                        "rejection_rate": rejection,
                        "monte_carlo_se": _monte_carlo_se(
                            rejection, len(rejected)
                        ),
                        "critical_value": median_critical,
                    }
                )
                critical_rows.append(
                    {
                        "method": "moving-block-bootstrap",
                        "sample_size": sample_size,
                        "replications": len(critical_values),
                        "q90": float(np.quantile(critical_values, 0.10)),
                        "q95": median_critical,
                        "q99": float(np.quantile(critical_values, 0.90)),
                        "scope": "distribution of sample-specific 5% critical values",
                    }
                )

        for local_alternative in (False, True):
            for scale_index, scale in enumerate((0.25, 0.50, 1.00), start=1):
                rejected_fixed: list[bool] = []
                rejected_bootstrap_calibrated: list[bool] = []
                for replication in range(config.replications):
                    rng = _rng(
                        config,
                        5,
                        30 + scale_index + 10 * int(local_alternative),
                        sample_size,
                        replication,
                    )
                    draw = simulate_dgp(
                        rng,
                        sample_size,
                        alternative_scale=scale,
                        local_alternative=local_alternative,
                    )
                    fit = fit_cross_product_imols(
                        draw.y, draw.capital, draw.wage_share
                    )
                    if fit.numerical_failure or not fit.rank_supported:
                        continue
                    statistic = cointegration_statistic(fit)
                    rejected_fixed.append(statistic > fixed_q95)
                    if sample_size in bootstrap_critical_by_size:
                        rejected_bootstrap_calibrated.append(
                            statistic
                            > bootstrap_critical_by_size[sample_size]
                        )
                for method, values, critical_value in (
                    ("fixed-b", rejected_fixed, fixed_q95),
                    (
                        "moving-block-bootstrap",
                        rejected_bootstrap_calibrated,
                        bootstrap_critical_by_size.get(sample_size),
                    ),
                ):
                    if not values:
                        continue
                    rejection = float(np.mean(values))
                    result_rows.append(
                        {
                            "sample_size": sample_size,
                            "method": method,
                            "experiment": "power",
                            "alternative_scale": scale,
                            "local_alternative": local_alternative,
                            "replications": len(values),
                            "rejection_rate": rejection,
                            "monte_carlo_se": _monte_carlo_se(
                                rejection, len(values)
                            ),
                            "critical_value": critical_value,
                        }
                    )

        _write_checkpoint(
            config,
            "t05",
            f"t{sample_size}",
            {
                "sample_size": sample_size,
                "replications": config.replications,
                "completed": True,
            },
        )

    critical_path = config.output / "t05-critical-values.csv"
    results_path = config.output / "t05-size-power.csv"
    scaling_path = config.output / "t05-residual-scaling-summary.csv"
    rate_path = config.output / "t05-residual-rate-checks.csv"
    _write_csv(critical_path, critical_rows)
    _write_csv(results_path, result_rows)
    _write_csv(scaling_path, scaling_rows)
    _write_csv(rate_path, scaling_rate_rows)
    return [critical_path, results_path, scaling_path, rate_path]


def _path_states(wage_share: np.ndarray) -> np.ndarray:
    states = np.empty_like(wage_share)
    states[0] = 0.0
    states[1:] = wage_share[:-1]
    return states


def run_t06_local(config: Any) -> list[Path]:
    fixed_critical = simulate_fixed_b_limit_critical_values(
        config.seed, config.limit_draws
    )
    contrast_critical = max(
        fixed_critical["capital"]["q95"],
        fixed_critical["interaction"]["q95"],
    )
    summary_rows: list[dict[str, Any]] = []
    path_rows: list[dict[str, Any]] = []
    efficiency_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []

    for sample_size in config.sample_sizes:
        fixed_coverage = {
            state: {"theta": [], "gap": [], "length": []}
            for state in FIXED_STATES
        }
        uniform_rejections: list[bool] = []
        beta_null = BETA.copy()
        beta_null[1] = 1.0
        beta_null[3] = -1.0
        for replication in range(config.replications):
            rng = _rng(config, 6, 1, sample_size, replication)
            draw = simulate_dgp(rng, sample_size)
            fit = fit_cross_product_imols(
                draw.y, draw.capital, draw.wage_share
            )
            if fit.numerical_failure or not fit.rank_supported:
                continue
            for state in FIXED_STATES:
                contrast = state_contrast(state)
                se = contrast_standard_error(fit.covariance, contrast)
                theta_hat, gap_hat = fixed_state_targets(fit.beta, state)
                theta_true, gap_true = fixed_state_targets(BETA, state)
                half_width = contrast_critical * se
                fixed_coverage[state]["theta"].append(
                    abs(theta_hat - theta_true) <= half_width
                )
                fixed_coverage[state]["gap"].append(
                    abs(gap_hat - gap_true) <= half_width
                )
                fixed_coverage[state]["length"].append(2.0 * half_width)

            null_rng = _rng(config, 6, 2, sample_size, replication)
            null_draw = simulate_dgp(
                null_rng, sample_size, beta=beta_null
            )
            null_fit = fit_cross_product_imols(
                null_draw.y, null_draw.capital, null_draw.wage_share
            )
            if not null_fit.numerical_failure and null_fit.rank_supported:
                restriction = null_fit.beta[[1, 3]] - np.array([1.0, -1.0])
                covariance = null_fit.covariance[np.ix_([1, 3], [1, 3])]
                statistic = float(
                    restriction
                    @ np.linalg.pinv(covariance, rcond=1e-12)
                    @ restriction
                )
                uniform_rejections.append(statistic > 5.991464547)

        for state, values in fixed_coverage.items():
            for target in ("theta", "gap"):
                coverage = float(np.mean(values[target]))
                summary_rows.append(
                    {
                        "sample_size": sample_size,
                        "method": "fixed-b",
                        "regime": "fixed-policy-state",
                        "state": state,
                        "target": target,
                        "replications": len(values[target]),
                        "coverage_95": coverage,
                        "coverage_mc_se": _monte_carlo_se(
                            coverage, len(values[target])
                        ),
                        "mean_interval_length": float(
                            np.mean(values["length"])
                        ),
                    }
                )
        if uniform_rejections:
            rejection = float(np.mean(uniform_rejections))
            efficiency_rows.append(
                {
                    "sample_size": sample_size,
                    "method": "fixed-b-wald",
                    "null": "uniform-gap-zero: b=1,d=-1",
                    "replications": len(uniform_rejections),
                    "rejection_rate": rejection,
                    "monte_carlo_se": _monte_carlo_se(
                        rejection, len(uniform_rejections)
                    ),
                }
            )

        if config.inference != "fixed-b":
            outer = _bootstrap_outer(config, sample_size)
            fixed_bootstrap_coverage = {
                state: {"theta": [], "gap": [], "length": []}
                for state in FIXED_STATES
            }
            conditional_band_coverage: list[bool] = []
            unconditional_band_coverage: list[bool] = []
            pointwise_coverage = {fraction: [] for fraction in (0.25, 0.50, 0.75, 1.0)}
            for replication in range(outer):
                rng = _rng(config, 66, 1, sample_size, replication)
                draw = simulate_dgp(rng, sample_size)
                fit = fit_cross_product_imols(
                    draw.y, draw.capital, draw.wage_share
                )
                if fit.numerical_failure or not fit.rank_supported:
                    continue
                bootstrap_rng = _rng(
                    config, 606, 1, sample_size, replication
                )
                bootstrap_draws = _bootstrap_draws(config, sample_size)
                estimates, _, wage_paths = bootstrap_cross_product_imols(
                    bootstrap_rng,
                    draw,
                    fit,
                    bootstrap_draws,
                    block_length=(
                        config.block_length
                        if isinstance(config.block_length, int)
                        else automatic_block_length(sample_size)
                    ),
                )
                if estimates.shape[0] < max(
                    10, bootstrap_draws // 2
                ):
                    continue
                for state in FIXED_STATES:
                    theta_hat, gap_hat = fixed_state_targets(fit.beta, state)
                    theta_star = estimates[:, 1] + state * estimates[:, 3]
                    gap_star = 1.0 - state - theta_star
                    theta_difference = theta_star - theta_hat
                    gap_difference = gap_star - gap_hat
                    theta_lower = theta_hat - np.quantile(
                        theta_difference, 0.975
                    )
                    theta_upper = theta_hat - np.quantile(
                        theta_difference, 0.025
                    )
                    gap_lower = gap_hat - np.quantile(gap_difference, 0.975)
                    gap_upper = gap_hat - np.quantile(gap_difference, 0.025)
                    theta_true, gap_true = fixed_state_targets(BETA, state)
                    fixed_bootstrap_coverage[state]["theta"].append(
                        theta_lower <= theta_true <= theta_upper
                    )
                    fixed_bootstrap_coverage[state]["gap"].append(
                        gap_lower <= gap_true <= gap_upper
                    )
                    fixed_bootstrap_coverage[state]["length"].append(
                        theta_upper - theta_lower
                    )

                observed_states = _path_states(draw.wage_share)
                trim_start = max(
                    int(math.ceil(0.15 * sample_size)), 10
                )
                observed_states = observed_states[trim_start:]
                theta_hat_path = (
                    fit.beta[1] + fit.beta[3] * observed_states
                )
                theta_true_path = BETA[1] + BETA[3] * observed_states
                conditional_star = (
                    estimates[:, 1, None]
                    + estimates[:, 3, None] * observed_states[None, :]
                )
                conditional_difference = (
                    conditional_star - theta_hat_path[None, :]
                )
                pointwise_scale = np.std(
                    conditional_difference, axis=0, ddof=1
                )
                pointwise_scale = np.maximum(pointwise_scale, 1e-12)
                conditional_sup = np.max(
                    np.abs(conditional_difference) / pointwise_scale,
                    axis=1,
                )
                conditional_critical = float(
                    np.quantile(conditional_sup, 0.95)
                )
                conditional_band_coverage.append(
                    bool(
                        np.all(
                            np.abs(theta_hat_path - theta_true_path)
                            <= conditional_critical * pointwise_scale
                        )
                    )
                )

                unconditional_paths = []
                for estimate, wage_path in zip(estimates, wage_paths):
                    star_states = _path_states(wage_path)[trim_start:]
                    unconditional_paths.append(
                        estimate[1] + estimate[3] * star_states
                    )
                unconditional_array = np.vstack(unconditional_paths)
                unconditional_difference = (
                    unconditional_array - theta_hat_path[None, :]
                )
                unconditional_scale = np.std(
                    unconditional_difference, axis=0, ddof=1
                )
                unconditional_scale = np.maximum(
                    unconditional_scale, 1e-12
                )
                unconditional_sup = np.max(
                    np.abs(unconditional_difference)
                    / unconditional_scale,
                    axis=1,
                )
                unconditional_critical = float(
                    np.quantile(unconditional_sup, 0.95)
                )
                unconditional_band_coverage.append(
                    bool(
                        np.all(
                            np.abs(theta_hat_path - theta_true_path)
                            <= unconditional_critical
                            * unconditional_scale
                        )
                    )
                )

                for fraction in pointwise_coverage:
                    index = min(
                        observed_states.size - 1,
                        max(0, int(round(fraction * observed_states.size)) - 1),
                    )
                    differences = conditional_difference[:, index]
                    lower = theta_hat_path[index] - np.quantile(
                        differences, 0.975
                    )
                    upper = theta_hat_path[index] - np.quantile(
                        differences, 0.025
                    )
                    pointwise_coverage[fraction].append(
                        lower <= theta_true_path[index] <= upper
                    )

            for state, values in fixed_bootstrap_coverage.items():
                for target in ("theta", "gap"):
                    if not values[target]:
                        continue
                    coverage = float(np.mean(values[target]))
                    summary_rows.append(
                        {
                            "sample_size": sample_size,
                            "method": "moving-block-bootstrap",
                            "regime": "fixed-policy-state",
                            "state": state,
                            "target": target,
                            "replications": len(values[target]),
                            "coverage_95": coverage,
                            "coverage_mc_se": _monte_carlo_se(
                                coverage, len(values[target])
                            ),
                            "mean_interval_length": float(
                                np.mean(values["length"])
                            ),
                        }
                    )
            for method, values in (
                ("conditional-path-band", conditional_band_coverage),
                ("unconditional-path-band", unconditional_band_coverage),
            ):
                if values:
                    coverage = float(np.mean(values))
                    path_rows.append(
                        {
                            "sample_size": sample_size,
                            "method": method,
                            "trim_fraction": max(0.15, 10 / sample_size),
                            "replications": len(values),
                            "simultaneous_coverage_95": coverage,
                            "coverage_mc_se": _monte_carlo_se(
                                coverage, len(values)
                            ),
                        }
                    )
            for fraction, values in pointwise_coverage.items():
                if values:
                    coverage = float(np.mean(values))
                    path_rows.append(
                        {
                            "sample_size": sample_size,
                            "method": "conditional-pointwise",
                            "path_fraction": fraction,
                            "trim_fraction": max(0.15, 10 / sample_size),
                            "replications": len(values),
                            "simultaneous_coverage_95": coverage,
                            "coverage_mc_se": _monte_carlo_se(
                                coverage, len(values)
                            ),
                        }
                    )

        diagnostic_replications = min(
            config.replications, 100 if config.profile == "smoke" else 1000
        )
        stationary_supported = 0
        stationary_theta_errors = []
        for replication in range(diagnostic_replications):
            rng = _rng(config, 6, 90, sample_size, replication)
            draw = simulate_dgp(
                rng, sample_size, scenario="stationary-omega"
            )
            fit = fit_cross_product_imols(
                draw.y, draw.capital, draw.wage_share
            )
            stationary_supported += int(fit.rank_supported)
            if not fit.numerical_failure:
                state = float(np.mean(draw.wage_share))
                theta_hat, _ = fixed_state_targets(fit.beta, state)
                theta_true, _ = fixed_state_targets(BETA, state)
                stationary_theta_errors.append(theta_hat - theta_true)
        diagnostic_rows.append(
            {
                "sample_size": sample_size,
                "regime": "estimated-stationary-state",
                "replications": diagnostic_replications,
                "i1_rank_gate_pass_rate": stationary_supported
                / diagnostic_replications,
                "theta_rmse_under_unsupported_transform": (
                    float(
                        np.sqrt(
                            np.mean(np.asarray(stationary_theta_errors) ** 2)
                        )
                    )
                    if stationary_theta_errors
                    else ""
                ),
                "status": "diagnostic-only; no operational inference",
                "gap_state_derivative": "-(1+d)",
            }
        )
        _write_checkpoint(
            config,
            "t06",
            f"t{sample_size}",
            {
                "sample_size": sample_size,
                "replications": config.replications,
                "completed": True,
            },
        )

    summary_path = config.output / "t06-fixed-state-inference.csv"
    path_path = config.output / "t06-path-band-coverage.csv"
    efficiency_path = config.output / "t06-efficiency-wald.csv"
    diagnostic_path = config.output / "t06-i0-diagnostic.csv"
    _write_csv(summary_path, summary_rows)
    _write_csv(path_path, path_rows)
    _write_csv(efficiency_path, efficiency_rows)
    _write_csv(diagnostic_path, diagnostic_rows)
    return [summary_path, path_path, efficiency_path, diagnostic_path]
