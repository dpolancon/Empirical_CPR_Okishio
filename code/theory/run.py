"""Run deterministic Monte Carlo checks for the six theory tasks."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib import pyplot as plt

from .advanced import run_t03_local, run_t05_local, run_t06_local


DEFAULT_SEED = 20260723
VAULT_DIRECTORY = "03B_econometrics_validation"
DEFAULT_REPLICATIONS = 10_000
DEFAULT_SAMPLE_SIZES = (40, 50, 60, 80, 100, 120, 200, 500, 1_000)
DEFAULT_BATCH_SIZE = 500
SAMPLE_GRIDS = {
    "small-50": (40, 50, 60),
    "small-100": (80, 100, 120),
    "asymptotic": (200, 500, 1_000),
    "all": DEFAULT_SAMPLE_SIZES,
}
SCENARIOS = (
    "correlation-0",
    "correlation-0.5",
    "correlation-0.9",
    "stationary-omega",
    "cointegrated-levels",
    "singular-common-trend",
)
TASKS = ("t01", "t02", "t03", "t04", "t05", "t06")
TASK_ARTIFACTS = {
    "t01": ("t01-scaling-summary.csv", "t01-rate-checks.csv", "t01-scaling-rates.png"),
    "t02": ("t02-design-summary.csv", "t02-coefficient-summary.csv", "t02-rate-checks.csv"),
    "t03": (
        "t03-fixed-b-critical-values.json",
        "t03-imols-summary.csv",
        "t03-rate-checks.csv",
        "t03-rank-diagnostics.csv",
        "t03-naive-estimator-diagnostic.csv",
    ),
    "t04": ("t04-fwl-check.json",),
    "t05": (
        "t05-critical-values.csv",
        "t05-size-power.csv",
        "t05-residual-scaling-summary.csv",
        "t05-residual-rate-checks.csv",
    ),
    "t06": (
        "t06-fixed-state-inference.csv",
        "t06-path-band-coverage.csv",
        "t06-efficiency-wald.csv",
        "t06-i0-diagnostic.csv",
    ),
}


@dataclass(frozen=True)
class Config:
    seed: int
    replications: int
    sample_sizes: tuple[int, ...]
    batch_size: int
    output: Path
    inference: str = "both"
    profile: str = "smoke"
    limit_draws: int = 5_000
    bootstrap_replications: int = 99
    block_length: int | str = "auto"
    resume: bool = False
    workers: int = 1
    sample_grid: str = "all"


def _rng(seed: int, task: int, scenario: int, sample_size: int, batch: int) -> np.random.Generator:
    return np.random.default_rng(
        np.random.SeedSequence([seed, task, scenario, sample_size, batch])
    )


def _batches(replications: int, batch_size: int) -> Iterable[tuple[int, int]]:
    for start in range(0, replications, batch_size):
        yield start, min(batch_size, replications - start)


def _paths(
    rng: np.random.Generator,
    count: int,
    sample_size: int,
    scenario: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    innovations_x = rng.standard_normal((count, sample_size))
    innovations_aux = rng.standard_normal((count, sample_size))
    x = np.cumsum(innovations_x, axis=1)
    if scenario.startswith("correlation-"):
        rho = float(scenario.split("-", 1)[1])
        innovations_omega = (
            rho * innovations_x
            + math.sqrt(max(0.0, 1.0 - rho**2)) * innovations_aux
        )
        omega = np.cumsum(innovations_omega, axis=1)
    elif scenario == "stationary-omega":
        omega = innovations_aux
    elif scenario == "cointegrated-levels":
        omega = x + 0.5 * innovations_aux
    elif scenario == "singular-common-trend":
        omega = x.copy()
    else:
        raise ValueError(f"Unknown scenario: {scenario}")
    omega_lag = np.zeros_like(omega)
    omega_lag[:, 1:] = omega[:, :-1]
    interaction = x * omega_lag
    return x, omega, interaction


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _slope(sample_sizes: Iterable[int], values: Iterable[float]) -> float:
    x = np.log(np.asarray(tuple(sample_sizes), dtype=float))
    y = np.log(np.maximum(np.asarray(tuple(values), dtype=float), 1e-300))
    return float(np.polyfit(x, y, 1)[0])


def run_t01(config: Config) -> list[Path]:
    summary_rows: list[dict] = []
    for scenario_index, scenario in enumerate(SCENARIOS, start=1):
        for sample_size in config.sample_sizes:
            collected = {"x-level": [], "interaction": [], "interaction-partial-sum": []}
            for batch_index, (_, count) in enumerate(
                _batches(config.replications, config.batch_size)
            ):
                rng = _rng(config.seed, 1, scenario_index, sample_size, batch_index)
                x, _, interaction = _paths(rng, count, sample_size, scenario)
                collected["x-level"].append(np.abs(x[:, -1]))
                collected["interaction"].append(np.abs(interaction[:, -1]))
                collected["interaction-partial-sum"].append(
                    np.abs(np.sum(interaction, axis=1))
                )
            for metric, pieces in collected.items():
                summary_rows.append(
                    {
                        "scenario": scenario,
                        "sample_size": sample_size,
                        "metric": metric,
                        "median_absolute": float(np.median(np.concatenate(pieces))),
                    }
                )

    expected = {
        scenario: {
            "x-level": 0.5,
            "interaction": 0.5 if scenario == "stationary-omega" else 1.0,
            "interaction-partial-sum": 1.0 if scenario == "stationary-omega" else 2.0,
        }
        for scenario in SCENARIOS
    }
    rate_rows: list[dict] = []
    for scenario in SCENARIOS:
        for metric in ("x-level", "interaction", "interaction-partial-sum"):
            values = [
                row["median_absolute"]
                for row in summary_rows
                if row["scenario"] == scenario and row["metric"] == metric
            ]
            estimate = _slope(config.sample_sizes, values)
            theory = expected[scenario][metric]
            rate_rows.append(
                {
                    "scenario": scenario,
                    "metric": metric,
                    "estimated_exponent": estimate,
                    "theoretical_exponent": theory,
                    "absolute_error": abs(estimate - theory),
                    "passes_tolerance": abs(estimate - theory) <= 0.15,
                }
            )

    summary_path = config.output / "t01-scaling-summary.csv"
    rates_path = config.output / "t01-rate-checks.csv"
    figure_path = config.output / "t01-scaling-rates.png"
    _write_csv(summary_path, summary_rows)
    _write_csv(rates_path, rate_rows)

    figure, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for scenario in SCENARIOS:
        subset = [
            row
            for row in summary_rows
            if row["scenario"] == scenario and row["metric"] == "interaction"
        ]
        axes[0].loglog(
            [row["sample_size"] for row in subset],
            [row["median_absolute"] for row in subset],
            marker="o",
            label=scenario,
        )
        subset = [
            row
            for row in summary_rows
            if row["scenario"] == scenario
            and row["metric"] == "interaction-partial-sum"
        ]
        axes[1].loglog(
            [row["sample_size"] for row in subset],
            [row["median_absolute"] for row in subset],
            marker="o",
            label=scenario,
        )
    axes[0].set_title("Lagged interaction level")
    axes[1].set_title("Interaction partial sum")
    for axis in axes:
        axis.set_xlabel("T")
        axis.set_ylabel("median absolute magnitude")
        axis.grid(True, which="both", alpha=0.25)
    axes[1].legend(fontsize=7, loc="upper left")
    figure.tight_layout()
    figure.savefig(figure_path, dpi=160)
    plt.close(figure)
    return [summary_path, rates_path, figure_path]


def _design_scales(sample_size: int, scenario: str) -> np.ndarray:
    if scenario == "stationary-omega":
        return np.array([1.0, sample_size**0.5, 1.0, sample_size**0.5])
    return np.array([1.0, sample_size**0.5, sample_size**0.5, float(sample_size)])


def run_t02(config: Config) -> list[Path]:
    design_rows: list[dict] = []
    coefficient_rows: list[dict] = []
    coefficient_scenarios = {
        "correlation-0",
        "correlation-0.5",
        "correlation-0.9",
        "stationary-omega",
    }
    beta = np.array([0.5, 1.0, -0.75, 0.25])
    for scenario_index, scenario in enumerate(SCENARIOS, start=1):
        for sample_size in config.sample_sizes:
            eigenvalues: list[np.ndarray] = []
            conditions: list[np.ndarray] = []
            errors: list[np.ndarray] = []
            scales = _design_scales(sample_size, scenario)
            for batch_index, (_, count) in enumerate(
                _batches(config.replications, config.batch_size)
            ):
                rng = _rng(config.seed, 2, scenario_index, sample_size, batch_index)
                x, omega, interaction = _paths(rng, count, sample_size, scenario)
                design = np.stack(
                    (np.ones_like(x), x, omega, interaction),
                    axis=2,
                )
                normalized = design / scales[None, None, :]
                normalized_gram = np.einsum(
                    "bti,btj->bij", normalized, normalized
                ) / sample_size
                eigen = np.linalg.eigvalsh(normalized_gram)
                eigenvalues.append(eigen[:, 0])
                conditions.append(
                    np.divide(
                        eigen[:, -1],
                        np.maximum(eigen[:, 0], 1e-15),
                    )
                )
                if scenario in coefficient_scenarios:
                    disturbance = rng.standard_normal((count, sample_size))
                    gram = np.einsum("bti,btj->bij", design, design)
                    score = np.einsum("bti,bt->bi", design, disturbance)
                    estimate_error = np.linalg.solve(gram, score[..., None])[..., 0]
                    errors.append(estimate_error)

            design_rows.append(
                {
                    "scenario": scenario,
                    "sample_size": sample_size,
                    "median_min_eigenvalue": float(
                        np.median(np.concatenate(eigenvalues))
                    ),
                    "median_condition_number": float(
                        np.median(np.concatenate(conditions))
                    ),
                    "asymptotic_rank_expected": (
                        "full"
                        if scenario in coefficient_scenarios
                        else "deficient"
                    ),
                }
            )
            if errors:
                all_errors = np.concatenate(errors)
                rmse = np.sqrt(np.mean(all_errors**2, axis=0))
                for column, value in zip(
                    ("intercept", "x", "omega", "interaction"), rmse
                ):
                    coefficient_rows.append(
                        {
                            "scenario": scenario,
                            "sample_size": sample_size,
                            "coefficient": column,
                            "rmse": float(value),
                        }
                    )

    rate_rows: list[dict] = []
    for scenario in sorted(coefficient_scenarios):
        expected = (
            {"intercept": -0.5, "x": -1.0, "omega": -0.5, "interaction": -1.0}
            if scenario == "stationary-omega"
            else {"intercept": -0.5, "x": -1.0, "omega": -1.0, "interaction": -1.5}
        )
        for coefficient, theory in expected.items():
            values = [
                row["rmse"]
                for row in coefficient_rows
                if row["scenario"] == scenario and row["coefficient"] == coefficient
            ]
            estimate = _slope(config.sample_sizes, values)
            rate_rows.append(
                {
                    "scenario": scenario,
                    "coefficient": coefficient,
                    "estimated_exponent": estimate,
                    "theoretical_exponent": theory,
                    "absolute_error": abs(estimate - theory),
                    "passes_tolerance": abs(estimate - theory) <= 0.15,
                }
            )

    design_path = config.output / "t02-design-summary.csv"
    coefficient_path = config.output / "t02-coefficient-summary.csv"
    rate_path = config.output / "t02-rate-checks.csv"
    _write_csv(design_path, design_rows)
    _write_csv(coefficient_path, coefficient_rows)
    _write_csv(rate_path, rate_rows)
    return [design_path, coefficient_path, rate_path]


def run_t03(config: Config) -> list[Path]:
    rows: list[dict] = []
    beta = np.array([0.5, 1.0, -0.75, 0.25])
    for sample_size in config.sample_sizes:
        coverage_parts = {name: [] for name in ("x", "omega", "interaction")}
        bias_parts: list[np.ndarray] = []
        for batch_index, (_, count) in enumerate(
            _batches(config.replications, config.batch_size)
        ):
            rng = _rng(config.seed, 3, 1, sample_size, batch_index)
            innovation_x = rng.standard_normal((count, sample_size))
            innovation_aux = rng.standard_normal((count, sample_size))
            innovation_omega = (
                0.5 * innovation_x + math.sqrt(0.75) * innovation_aux
            )
            x = np.cumsum(innovation_x, axis=1)
            omega = np.cumsum(innovation_omega, axis=1)
            omega_lag = np.zeros_like(omega)
            omega_lag[:, 1:] = omega[:, :-1]
            interaction = x * omega_lag
            design = np.stack((np.ones_like(x), x, omega, interaction), axis=2)
            noise = rng.standard_normal((count, sample_size))
            disturbance = 0.6 * innovation_x + 0.8 * noise
            gram = np.einsum("bti,btj->bij", design, design)
            score = np.einsum("bti,bt->bi", design, disturbance)
            error = np.linalg.solve(gram, score[..., None])[..., 0]
            residual = disturbance - np.einsum("bti,bi->bt", design, error)
            sigma2 = np.sum(residual**2, axis=1) / (sample_size - 4)
            inverse = np.linalg.inv(gram)
            standard_errors = np.sqrt(
                sigma2[:, None] * np.diagonal(inverse, axis1=1, axis2=2)
            )
            bias_parts.append(error)
            for index, name in enumerate(("x", "omega", "interaction"), start=1):
                coverage_parts[name].append(
                    np.abs(error[:, index]) <= 1.96 * standard_errors[:, index]
                )
        errors = np.concatenate(bias_parts)
        for index, name in enumerate(("x", "omega", "interaction"), start=1):
            coverage = float(np.mean(np.concatenate(coverage_parts[name])))
            rows.append(
                {
                    "sample_size": sample_size,
                    "coefficient": name,
                    "mean_bias": float(np.mean(errors[:, index])),
                    "naive_95_coverage": coverage,
                    "passes_coverage_gate": 0.93 <= coverage <= 0.97,
                    "interpretation": "diagnostic-only; no valid cross-product correction implemented",
                }
            )
    path = config.output / "t03-naive-estimator-diagnostic.csv"
    _write_csv(path, rows)
    return [path]


def run_t04(config: Config) -> list[Path]:
    rng = _rng(config.seed, 4, 1, 100, 0)
    observations = 100
    controls = np.column_stack(
        (
            np.ones(observations),
            np.linspace(-1.0, 1.0, observations),
            rng.standard_normal(observations),
        )
    )
    target = rng.standard_normal((observations, 2))
    y = controls @ np.array([1.0, -0.5, 0.25]) + target @ np.array([0.8, -0.3])
    y += rng.standard_normal(observations)
    transform = np.tril(np.ones((observations, observations)))

    transformed_controls = transform @ controls
    transformed_target = transform @ target
    transformed_y = transform @ y
    full_design = np.column_stack((transformed_controls, transformed_target))
    full_beta = np.linalg.lstsq(full_design, transformed_y, rcond=None)[0][-2:]

    annihilator_transformed = np.eye(observations) - transformed_controls @ np.linalg.pinv(
        transformed_controls
    )
    fwl_target = annihilator_transformed @ transformed_target
    fwl_y = annihilator_transformed @ transformed_y
    fwl_beta = np.linalg.lstsq(fwl_target, fwl_y, rcond=None)[0]

    annihilator_original = np.eye(observations) - controls @ np.linalg.pinv(controls)
    operator_difference = transform @ annihilator_original - annihilator_transformed @ transform
    full_inverse = np.linalg.inv(full_design.T @ full_design)[-2:, -2:]
    fwl_inverse = np.linalg.inv(fwl_target.T @ fwl_target)
    result = {
        "seed": config.seed,
        "fwl_coefficient_max_abs_difference": float(np.max(np.abs(full_beta - fwl_beta))),
        "fwl_covariance_max_abs_difference": float(
            np.max(np.abs(full_inverse - fwl_inverse))
        ),
        "transform_residualizer_frobenius_difference": float(
            np.linalg.norm(operator_difference)
        ),
        "identity_tolerance": 1e-10,
        "fwl_identity_passes": bool(
            np.max(np.abs(full_beta - fwl_beta)) <= 1e-10
            and np.max(np.abs(full_inverse - fwl_inverse)) <= 1e-10
        ),
        "noncommutation_detected": bool(np.linalg.norm(operator_difference) > 1e-6),
    }
    path = config.output / "t04-fwl-check.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8", newline="\n")
    return [path]


def run_t05(config: Config) -> list[Path]:
    rows: list[dict] = []
    for process_index, process in enumerate(("stationary-residual", "unit-root-residual"), start=1):
        for sample_size in config.sample_sizes:
            values: list[np.ndarray] = []
            for batch_index, (_, count) in enumerate(
                _batches(config.replications, config.batch_size)
            ):
                rng = _rng(config.seed, 5, process_index, sample_size, batch_index)
                innovations = rng.standard_normal((count, sample_size))
                residual = (
                    innovations
                    if process == "stationary-residual"
                    else np.cumsum(innovations, axis=1)
                )
                partial = np.cumsum(residual, axis=1)
                values.append(np.sum(partial**2, axis=1))
            median = float(np.median(np.concatenate(values)))
            rows.append(
                {
                    "process": process,
                    "sample_size": sample_size,
                    "median_sum_squared_partial_residual": median,
                }
            )
    rate_rows: list[dict] = []
    for process, theory in (("stationary-residual", 2.0), ("unit-root-residual", 4.0)):
        values = [
            row["median_sum_squared_partial_residual"]
            for row in rows
            if row["process"] == process
        ]
        estimate = _slope(config.sample_sizes, values)
        rate_rows.append(
            {
                "process": process,
                "estimated_exponent": estimate,
                "theoretical_exponent": theory,
                "absolute_error": abs(estimate - theory),
                "passes_tolerance": abs(estimate - theory) <= 0.15,
                "scope": "oracle residual diagnostic, not an estimated cross-product CPR test",
            }
        )
    summary_path = config.output / "t05-residual-scaling-summary.csv"
    rates_path = config.output / "t05-residual-rate-checks.csv"
    _write_csv(summary_path, rows)
    _write_csv(rates_path, rate_rows)
    return [summary_path, rates_path]


def _contrast_variance(
    contrasts: np.ndarray,
    inverse_gram: np.ndarray,
    sigma2: np.ndarray,
) -> np.ndarray:
    return sigma2 * np.einsum("bi,bij,bj->b", contrasts, inverse_gram, contrasts)


def run_t06(config: Config) -> list[Path]:
    rows: list[dict] = []
    beta = np.array([0.5, 1.0, -0.75, 0.25])
    for sample_size in config.sample_sizes:
        coverage = {
            "fixed-state": [],
            "integrated-path-state": [],
            "estimated-stationary-state": [],
            "estimated-stationary-state-naive": [],
        }
        for batch_index, (_, count) in enumerate(
            _batches(config.replications, config.batch_size)
        ):
            rng = _rng(config.seed, 6, 1, sample_size, batch_index)
            x, omega, interaction = _paths(
                rng, count, sample_size, "correlation-0.5"
            )
            design = np.stack((np.ones_like(x), x, omega, interaction), axis=2)
            disturbance = rng.standard_normal((count, sample_size))
            gram = np.einsum("bti,btj->bij", design, design)
            score = np.einsum("bti,bt->bi", design, disturbance)
            error = np.linalg.solve(gram, score[..., None])[..., 0]
            beta_hat = beta[None, :] + error
            residual = disturbance - np.einsum("bti,bi->bt", design, error)
            sigma2 = np.sum(residual**2, axis=1) / (sample_size - 4)
            inverse = np.linalg.inv(gram)

            fixed = np.tile(np.array([0.0, 0.0, 1.0, 1.0]), (count, 1))
            fixed_error = np.einsum("bi,bi->b", fixed, error)
            fixed_se = np.sqrt(_contrast_variance(fixed, inverse, sigma2))
            coverage["fixed-state"].append(np.abs(fixed_error) <= 1.96 * fixed_se)

            path = np.zeros((count, 4))
            path[:, 2] = 1.0
            path[:, 3] = x[:, -1]
            path_error = np.einsum("bi,bi->b", path, error)
            path_se = np.sqrt(_contrast_variance(path, inverse, sigma2))
            coverage["integrated-path-state"].append(
                np.abs(path_error) <= 1.96 * path_se
            )

            state = 1.0 + rng.standard_normal((count, sample_size))
            state_hat = np.mean(state, axis=1)
            state_variance = np.var(state, axis=1, ddof=1) / sample_size
            estimated = np.zeros((count, 4))
            estimated[:, 2] = 1.0
            estimated[:, 3] = state_hat
            target_error = (
                beta_hat[:, 2] + beta_hat[:, 3] * state_hat
                - (beta[2] + beta[3])
            )
            regression_variance = _contrast_variance(estimated, inverse, sigma2)
            corrected_se = np.sqrt(
                regression_variance + beta_hat[:, 3] ** 2 * state_variance
            )
            naive_se = np.sqrt(regression_variance)
            coverage["estimated-stationary-state"].append(
                np.abs(target_error) <= 1.96 * corrected_se
            )
            coverage["estimated-stationary-state-naive"].append(
                np.abs(target_error) <= 1.96 * naive_se
            )

        for regime, pieces in coverage.items():
            value = float(np.mean(np.concatenate(pieces)))
            rows.append(
                {
                    "sample_size": sample_size,
                    "regime": regime,
                    "coverage_95": value,
                    "passes_coverage_gate": (
                        0.93 <= value <= 0.97
                        if sample_size >= 500 and not regime.endswith("-naive")
                        else ""
                    ),
                    "scope": "exogenous oracle OLS; estimator uncertainty from T03 remains unresolved",
                }
            )
    path = config.output / "t06-state-inference-summary.csv"
    _write_csv(path, rows)
    return [path]


def build_argument_parser() -> argparse.ArgumentParser:
    repo_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--task",
        nargs="+",
        choices=("all", *TASKS),
        default=("all",),
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--replications", type=int)
    parser.add_argument(
        "--sample-sizes",
        nargs="+",
        type=int,
    )
    parser.add_argument(
        "--sample-grid",
        choices=tuple(SAMPLE_GRIDS),
        default="all",
    )
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument(
        "--inference",
        choices=("fixed-b", "bootstrap", "both"),
        default="both",
    )
    parser.add_argument(
        "--profile",
        choices=("smoke", "full"),
        default="full",
    )
    parser.add_argument("--limit-draws", type=int)
    parser.add_argument(
        "--bootstrap-replications",
        type=int,
        default=0,
        help="Override profile-controlled inner bootstrap draws (0 keeps profile defaults).",
    )
    parser.add_argument(
        "--block-length",
        default="auto",
        help="Circular block length or 'auto'.",
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / VAULT_DIRECTORY / "theory" / "results",
    )
    return parser


def main() -> None:
    args = build_argument_parser().parse_args()
    replications = args.replications
    if replications is None:
        replications = 250 if args.profile == "smoke" else DEFAULT_REPLICATIONS
    limit_draws = args.limit_draws
    if limit_draws is None:
        limit_draws = 5_000 if args.profile == "smoke" else 200_000
    if replications <= 0 or args.batch_size <= 0:
        raise ValueError("replications and batch-size must be positive")
    if limit_draws <= 0 or args.workers <= 0:
        raise ValueError("limit-draws and workers must be positive")
    sample_sizes = (
        tuple(args.sample_sizes)
        if args.sample_sizes
        else SAMPLE_GRIDS[args.sample_grid]
    )
    if any(value < 10 for value in sample_sizes):
        raise ValueError("sample sizes must be at least 10")
    block_length: int | str
    if args.block_length == "auto":
        block_length = "auto"
    else:
        block_length = int(args.block_length)
        if block_length < 2:
            raise ValueError("block-length must be at least 2")
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    config = Config(
        seed=args.seed,
        replications=replications,
        sample_sizes=tuple(sorted(set(sample_sizes))),
        batch_size=args.batch_size,
        output=output,
        inference=args.inference,
        profile=args.profile,
        limit_draws=limit_draws,
        bootstrap_replications=args.bootstrap_replications,
        block_length=block_length,
        resume=args.resume,
        workers=args.workers,
        sample_grid=args.sample_grid,
    )
    selected = (
        TASKS
        if "all" in args.task
        else tuple(dict.fromkeys(args.task))
    )
    runners = {
        "t01": run_t01,
        "t02": run_t02,
        "t03": run_t03_local,
        "t04": run_t04,
        "t05": run_t05_local,
        "t06": run_t06_local,
    }
    existing_manifest: dict = {}
    existing_manifest_path = output / "run-manifest.json"
    if config.resume and existing_manifest_path.is_file():
        try:
            existing_manifest = json.loads(
                existing_manifest_path.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError:
            existing_manifest = {}
    compatible_resume = (
        existing_manifest.get("schema_version") == 2
        and existing_manifest.get("seed") == config.seed
        and existing_manifest.get("profile") == config.profile
        and existing_manifest.get("sample_sizes") == list(config.sample_sizes)
        and existing_manifest.get("inference") == config.inference
    )
    resumed: list[str] = []
    runnable: list[str] = []
    written: list[Path] = []
    for task in selected:
        paths = [output / name for name in TASK_ARTIFACTS[task]]
        if (
            compatible_resume
            and task in existing_manifest.get("tasks", [])
            and all(path.is_file() and path.stat().st_size for path in paths)
        ):
            resumed.append(task)
            written.extend(paths)
        else:
            runnable.append(task)

    if config.workers > 1 and len(runnable) > 1:
        with ThreadPoolExecutor(
            max_workers=min(config.workers, len(runnable))
        ) as executor:
            task_outputs = executor.map(
                lambda task: runners[task](config), runnable
            )
            for paths in task_outputs:
                written.extend(paths)
    else:
        for task in runnable:
            written.extend(runners[task](config))
    manifest = {
        "schema_version": 2,
        "seed": config.seed,
        "replications": config.replications,
        "sample_sizes": list(config.sample_sizes),
        "batch_size": config.batch_size,
        "tasks": list(selected),
        "resumed_tasks": resumed,
        "profile": config.profile,
        "sample_grid": config.sample_grid,
        "inference": config.inference,
        "limit_draws": config.limit_draws,
        "bootstrap_replications": (
            config.bootstrap_replications
            if config.bootstrap_replications > 0
            else {
                "small_samples": 99 if config.profile == "smoke" else 999,
                "asymptotic": 99 if config.profile == "smoke" else 499,
            }
        ),
        "block_length": config.block_length,
        "workers": config.workers,
        "calibration_status": (
            "smoke-only; cannot update theory verdicts"
            if config.profile == "smoke"
            else "full-profile"
        ),
        "acceptance_thresholds": {
            "rate_exponent_absolute_error": 0.15,
            "nominal_5_percent_size_percentage_points": 2,
            "nominal_95_percent_coverage": [0.93, 0.97],
            "small_sample_95_percent_coverage": [0.90, 0.98],
            "small_sample_5_percent_size": [0.02, 0.08],
            "small_sample_method_difference": 0.05,
            "asymptotic_method_difference": 0.02,
            "fwl_identity_absolute_tolerance": 1e-10,
        },
        "artifacts": [path.name for path in written],
        "raw_draws_committed": False,
    }
    manifest_path = output / "run-manifest.json"
    if manifest_path.is_file():
        try:
            previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}
        compatible = (
            previous.get("schema_version") == 2
            and previous.get("seed") == manifest["seed"]
            and previous.get("profile") == manifest["profile"]
            and previous.get("sample_sizes") == manifest["sample_sizes"]
            and previous.get("inference") == manifest["inference"]
        )
        if compatible:
            manifest["tasks"] = sorted(
                set(previous.get("tasks", [])) | set(manifest["tasks"])
            )
            manifest["artifacts"] = sorted(
                set(previous.get("artifacts", []))
                | set(manifest["artifacts"])
            )
    manifest_path.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    for path in [*written, manifest_path]:
        print(path)


if __name__ == "__main__":
    main()
