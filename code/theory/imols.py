"""Cross-product IM-OLS primitives used by the local theory experiments.

The routines in this module implement the *local* extension documented in
T03.  They are deliberately labelled as local mathematical work: the exact
distinct-variable cross-product theorem has not been peer reviewed.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


BETA = np.array([0.5, 1.0, -0.75, 0.25], dtype=float)
COEFFICIENTS = ("intercept", "capital", "wage-share", "interaction")


@dataclass(frozen=True)
class ImolsFit:
    beta: np.ndarray
    nuisance: np.ndarray
    covariance: np.ndarray
    level_residuals: np.ndarray
    cumulative_residuals: np.ndarray
    condition_number: float
    minimum_eigenvalue: float
    rank_supported: bool
    numerical_failure: bool
    long_run_variance: float


@dataclass(frozen=True)
class DgpDraw:
    y: np.ndarray
    capital: np.ndarray
    wage_share: np.ndarray
    disturbance: np.ndarray
    innovation_capital: np.ndarray
    innovation_wage_share: np.ndarray
    scenario: str


def level_design(capital: np.ndarray, wage_share: np.ndarray) -> np.ndarray:
    """Return [1, k_t, omega_t, k_t omega_{t-1}] with an exact one-period lag."""

    capital = np.asarray(capital, dtype=float)
    wage_share = np.asarray(wage_share, dtype=float)
    if capital.ndim != 1 or wage_share.ndim != 1 or capital.size != wage_share.size:
        raise ValueError("capital and wage_share must be equal-length vectors")
    lagged = np.empty_like(wage_share)
    lagged[0] = 0.0
    lagged[1:] = wage_share[:-1]
    return np.column_stack(
        (np.ones(capital.size), capital, wage_share, capital * lagged)
    )


def cumulative_design(capital: np.ndarray, wage_share: np.ndarray) -> np.ndarray:
    """Return the complete augmented cumulative IM-OLS design."""

    design = level_design(capital, wage_share)
    cumulative = np.cumsum(design, axis=0)
    return np.column_stack((cumulative, capital, wage_share))


def coefficient_rates(sample_size: int) -> np.ndarray:
    return np.array(
        [sample_size**0.5, sample_size, sample_size, sample_size**1.5],
        dtype=float,
    )


def cumulative_column_scales(sample_size: int) -> np.ndarray:
    return np.array(
        [
            float(sample_size),
            sample_size**1.5,
            sample_size**1.5,
            sample_size**2.0,
            sample_size**0.5,
            sample_size**0.5,
        ],
        dtype=float,
    )


def automatic_block_length(sample_size: int) -> int:
    value = max(5, int(math.floor(1.75 * sample_size ** (1.0 / 3.0))))
    if sample_size <= 50:
        value = min(value, max(2, sample_size // 4))
    return min(value, max(2, sample_size - 1))


def bartlett_long_run_variance(values: np.ndarray, bandwidth: int) -> float:
    """Scalar Bartlett long-run variance with a nonnegative numerical floor."""

    centered = np.asarray(values, dtype=float) - float(np.mean(values))
    sample_size = centered.size
    if sample_size < 2:
        return float("nan")
    bandwidth = max(1, min(int(bandwidth), sample_size - 1))
    lrv = float(centered @ centered / sample_size)
    for lag in range(1, bandwidth + 1):
        weight = 1.0 - lag / (bandwidth + 1.0)
        covariance = float(centered[lag:] @ centered[:-lag] / sample_size)
        lrv += 2.0 * weight * covariance
    variance_floor = max(float(np.var(centered)), 1e-12) * 1e-8
    return max(lrv, variance_floor)


def _integrated_error_covariance(
    design: np.ndarray,
    inverse_gram: np.ndarray,
    long_run_variance: float,
) -> np.ndarray:
    """Sandwich covariance for a cumulative regression with Brownian errors.

    If M[i,j] = min(i+1,j+1), then H' M H can be evaluated in linear time
    from reverse cumulative sums because M = L L'.
    """

    reverse_cumulative = np.cumsum(design[::-1], axis=0)[::-1]
    middle = reverse_cumulative.T @ reverse_cumulative
    covariance = long_run_variance * inverse_gram @ middle @ inverse_gram
    return (covariance + covariance.T) / 2.0


def fit_cross_product_imols(
    y: np.ndarray,
    capital: np.ndarray,
    wage_share: np.ndarray,
    *,
    bandwidth_ratio: float = 0.20,
    rank_tolerance: float = 1e-10,
    condition_limit: float = 1e12,
) -> ImolsFit:
    """Fit the locally derived augmented cumulative cross-product IM-OLS."""

    y = np.asarray(y, dtype=float)
    capital = np.asarray(capital, dtype=float)
    wage_share = np.asarray(wage_share, dtype=float)
    sample_size = y.size
    if sample_size < 10 or capital.size != sample_size or wage_share.size != sample_size:
        raise ValueError("IM-OLS requires equal-length vectors with at least 10 rows")

    design = cumulative_design(capital, wage_share)
    cumulative_y = np.cumsum(y)
    scales = cumulative_column_scales(sample_size)
    normalized = design / scales
    normalized_gram = normalized.T @ normalized / sample_size
    eigenvalues = np.linalg.eigvalsh(normalized_gram)
    minimum = float(eigenvalues[0])
    maximum = float(eigenvalues[-1])
    condition = maximum / max(minimum, np.finfo(float).eps)
    rank = int(np.linalg.matrix_rank(normalized, tol=rank_tolerance))
    supported = (
        rank == design.shape[1]
        and minimum > rank_tolerance
        and condition < condition_limit
    )

    failure = False
    try:
        normalized_coefficients = np.linalg.lstsq(
            normalized, cumulative_y, rcond=rank_tolerance
        )[0]
        coefficients = normalized_coefficients / scales
        cumulative_residuals = cumulative_y - design @ coefficients
        beta = coefficients[:4]
        nuisance = coefficients[4:]
        level_residuals = y - level_design(capital, wage_share) @ beta
        bandwidth = max(1, int(math.floor(bandwidth_ratio * sample_size)))
        lrv = bartlett_long_run_variance(level_residuals, bandwidth)
        inverse_gram = np.linalg.pinv(design.T @ design, rcond=rank_tolerance)
        covariance = _integrated_error_covariance(design, inverse_gram, lrv)[:4, :4]
        if not np.all(np.isfinite(beta)) or not np.all(np.isfinite(covariance)):
            failure = True
    except np.linalg.LinAlgError:
        failure = True
        beta = np.full(4, np.nan)
        nuisance = np.full(2, np.nan)
        covariance = np.full((4, 4), np.nan)
        level_residuals = np.full(sample_size, np.nan)
        cumulative_residuals = np.full(sample_size, np.nan)
        lrv = float("nan")

    return ImolsFit(
        beta=beta,
        nuisance=nuisance,
        covariance=covariance,
        level_residuals=level_residuals,
        cumulative_residuals=cumulative_residuals,
        condition_number=condition,
        minimum_eigenvalue=minimum,
        rank_supported=supported,
        numerical_failure=failure,
        long_run_variance=lrv,
    )


def fit_naive_ols(
    y: np.ndarray, capital: np.ndarray, wage_share: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    design = level_design(capital, wage_share)
    beta = np.linalg.lstsq(design, y, rcond=1e-12)[0]
    residual = y - design @ beta
    dof = max(1, design.shape[0] - design.shape[1])
    sigma2 = float(residual @ residual / dof)
    covariance = sigma2 * np.linalg.pinv(design.T @ design, rcond=1e-12)
    return beta, covariance


def cointegration_statistic(fit: ImolsFit, *, bandwidth_ratio: float = 0.20) -> float:
    residuals = fit.level_residuals
    sample_size = residuals.size
    bandwidth = max(1, int(math.floor(bandwidth_ratio * sample_size)))
    lrv = bartlett_long_run_variance(residuals, bandwidth)
    partial = np.cumsum(residuals)
    return float(np.sum(partial**2) / (sample_size**2 * lrv))


def fixed_state_targets(beta: np.ndarray, state: float) -> tuple[float, float]:
    theta = float(beta[1] + beta[3] * state)
    gap = float(1.0 - state - theta)
    return theta, gap


def state_contrast(state: float) -> np.ndarray:
    return np.array([0.0, 1.0, 0.0, state], dtype=float)


def contrast_standard_error(covariance: np.ndarray, contrast: np.ndarray) -> float:
    variance = float(contrast @ covariance @ contrast)
    return math.sqrt(max(variance, 0.0))


def simulate_dgp(
    rng: np.random.Generator,
    sample_size: int,
    *,
    rho: float = 0.5,
    serial: float = 0.5,
    endogeneity: float = 0.6,
    distribution: str = "gaussian",
    scenario: str = "regular",
    beta: np.ndarray = BETA,
    alternative_scale: float = 0.0,
    local_alternative: bool = False,
) -> DgpDraw:
    """Simulate the exact lagged-interaction DGP and diagnostic variants."""

    if distribution == "gaussian":
        shocks = rng.standard_normal((3, sample_size))
    elif distribution == "student-t5":
        shocks = rng.standard_t(5, size=(3, sample_size)) / math.sqrt(5.0 / 3.0)
    else:
        raise ValueError(f"Unknown innovation distribution: {distribution}")

    innovation_capital = shocks[0]
    orthogonal = shocks[1]
    innovation_wage = rho * innovation_capital + math.sqrt(
        max(0.0, 1.0 - rho**2)
    ) * orthogonal

    capital = np.cumsum(innovation_capital)
    if scenario == "regular":
        wage_share = np.cumsum(innovation_wage)
    elif scenario == "stationary-omega":
        wage_share = innovation_wage.copy()
    elif scenario.startswith("local-to-unity-"):
        c_value = float(scenario.rsplit("-", 1)[1])
        root = 1.0 - c_value / sample_size
        wage_share = np.empty(sample_size)
        previous = 0.0
        for index, innovation in enumerate(innovation_wage):
            previous = root * previous + innovation
            wage_share[index] = previous
    elif scenario == "cointegrated-levels":
        wage_share = capital + 0.5 * innovation_wage
    elif scenario == "singular-common-trend":
        innovation_wage = innovation_capital.copy()
        wage_share = capital.copy()
    elif scenario == "weak-interaction":
        wage_share = 0.02 * np.cumsum(innovation_wage)
    else:
        raise ValueError(f"Unknown DGP scenario: {scenario}")

    innovation_error = (
        endogeneity * (0.6 * innovation_capital - 0.4 * innovation_wage)
        + math.sqrt(max(1e-8, 1.0 - 0.52 * endogeneity**2)) * shocks[2]
    )
    disturbance = np.empty(sample_size)
    previous_error = 0.0
    for index, innovation in enumerate(innovation_error):
        previous_error = serial * previous_error + innovation
        disturbance[index] = previous_error

    if alternative_scale:
        alternative_innovation = rng.standard_normal(sample_size)
        random_walk = np.cumsum(alternative_innovation)
        scale = alternative_scale / math.sqrt(sample_size) if local_alternative else alternative_scale
        disturbance = disturbance + scale * random_walk

    y = level_design(capital, wage_share) @ beta + disturbance
    return DgpDraw(
        y=y,
        capital=capital,
        wage_share=wage_share,
        disturbance=disturbance,
        innovation_capital=innovation_capital,
        innovation_wage_share=innovation_wage,
        scenario=scenario,
    )


def circular_block_indices(
    rng: np.random.Generator,
    sample_size: int,
    block_length: int,
) -> np.ndarray:
    blocks = int(math.ceil(sample_size / block_length))
    starts = rng.integers(0, sample_size, size=blocks)
    offsets = np.arange(block_length)
    return ((starts[:, None] + offsets[None, :]) % sample_size).ravel()[:sample_size]


def bootstrap_cross_product_imols(
    rng: np.random.Generator,
    draw: DgpDraw,
    fit: ImolsFit,
    replications: int,
    *,
    block_length: int | None = None,
    bandwidth_ratio: float = 0.20,
) -> tuple[np.ndarray, np.ndarray, list[np.ndarray]]:
    """Null-imposed joint moving-block bootstrap with full re-estimation."""

    sample_size = draw.y.size
    block_length = block_length or automatic_block_length(sample_size)
    differences_capital = np.diff(draw.capital, prepend=0.0)
    differences_wage = np.diff(draw.wage_share, prepend=0.0)
    stationary = np.column_stack(
        (
            fit.level_residuals - np.mean(fit.level_residuals),
            differences_capital - np.mean(differences_capital),
            differences_wage - np.mean(differences_wage),
        )
    )
    estimates: list[np.ndarray] = []
    statistics: list[float] = []
    wage_paths: list[np.ndarray] = []
    for _ in range(replications):
        indices = circular_block_indices(rng, sample_size, block_length)
        resampled = stationary[indices]
        capital_star = np.cumsum(resampled[:, 1])
        wage_star = np.cumsum(resampled[:, 2])
        y_star = level_design(capital_star, wage_star) @ fit.beta + resampled[:, 0]
        fit_star = fit_cross_product_imols(
            y_star,
            capital_star,
            wage_star,
            bandwidth_ratio=bandwidth_ratio,
        )
        if fit_star.numerical_failure or not fit_star.rank_supported:
            continue
        estimates.append(fit_star.beta)
        statistics.append(cointegration_statistic(fit_star, bandwidth_ratio=bandwidth_ratio))
        wage_paths.append(wage_star)
    if not estimates:
        return np.empty((0, 4)), np.empty(0), []
    return np.vstack(estimates), np.asarray(statistics), wage_paths


def simulate_fixed_b_limit_critical_values(
    seed: int,
    draws: int,
    *,
    grid_points: int = 200,
    batch_size: int = 250,
    bandwidth_ratio: float = 0.20,
) -> dict[str, dict[str, float]]:
    """Simulate coefficient-wise absolute-t critical values for the local limit."""

    collected = [[] for _ in range(4)]
    rng = np.random.default_rng(np.random.SeedSequence([seed, 303, draws, grid_points]))
    r = np.arange(1, grid_points + 1, dtype=float) / grid_points
    for start in range(0, draws, batch_size):
        count = min(batch_size, draws - start)
        innovations = rng.standard_normal((count, 3, grid_points)) / math.sqrt(grid_points)
        paths = np.cumsum(innovations, axis=2)
        capital = paths[:, 0]
        wage = paths[:, 1]
        error = paths[:, 2]
        error_innovations = innovations[:, 2] * math.sqrt(grid_points)
        int_capital = np.cumsum(capital, axis=1) / grid_points
        int_wage = np.cumsum(wage, axis=1) / grid_points
        int_product = np.cumsum(capital * wage, axis=1) / grid_points
        for index in range(count):
            design = np.column_stack(
                (
                    r,
                    int_capital[index],
                    int_wage[index],
                    int_product[index],
                    capital[index],
                    wage[index],
                )
            )
            gram_inverse = np.linalg.pinv(design.T @ design, rcond=1e-12)
            estimate = gram_inverse @ design.T @ error[index]
            normalized_level_design = np.column_stack(
                (
                    np.ones(grid_points),
                    capital[index],
                    wage[index],
                    capital[index] * wage[index],
                )
            )
            fitted_level_residual = (
                error_innovations[index]
                - normalized_level_design @ estimate[:4] / math.sqrt(grid_points)
            )
            bandwidth = max(1, int(math.floor(bandwidth_ratio * grid_points)))
            fixed_b_lrv = bartlett_long_run_variance(
                fitted_level_residual, bandwidth
            )
            covariance = _integrated_error_covariance(
                design, gram_inverse, fixed_b_lrv / grid_points
            )
            standard_errors = np.sqrt(np.maximum(np.diag(covariance)[:4], 1e-18))
            t_statistics = np.abs(estimate[:4] / standard_errors)
            for coefficient in range(4):
                collected[coefficient].append(float(t_statistics[coefficient]))

    result: dict[str, dict[str, float]] = {}
    for name, values in zip(COEFFICIENTS, collected):
        array = np.asarray(values)
        result[name] = {
            "q90": float(np.quantile(array, 0.90)),
            "q95": float(np.quantile(array, 0.95)),
            "q99": float(np.quantile(array, 0.99)),
        }
    return result


def simulate_residual_limit_critical_values(
    seed: int,
    draws: int,
    *,
    grid_points: int = 200,
    batch_size: int = 250,
    bandwidth_ratio: float = 0.20,
) -> dict[str, float]:
    """Simulate the fitted-residual partial-sum functional under cointegration."""

    values: list[float] = []
    rng = np.random.default_rng(np.random.SeedSequence([seed, 505, draws, grid_points]))
    r = np.arange(1, grid_points + 1, dtype=float) / grid_points
    for start in range(0, draws, batch_size):
        count = min(batch_size, draws - start)
        innovations = rng.standard_normal((count, 3, grid_points)) / math.sqrt(grid_points)
        paths = np.cumsum(innovations, axis=2)
        capital = paths[:, 0]
        wage = paths[:, 1]
        error = paths[:, 2]
        error_innovations = innovations[:, 2] * math.sqrt(grid_points)
        int_capital = np.cumsum(capital, axis=1) / grid_points
        int_wage = np.cumsum(wage, axis=1) / grid_points
        int_product = np.cumsum(capital * wage, axis=1) / grid_points
        for index in range(count):
            target_design = np.column_stack(
                (r, int_capital[index], int_wage[index], int_product[index])
            )
            augmented = np.column_stack(
                (target_design, capital[index], wage[index])
            )
            estimate = np.linalg.lstsq(augmented, error[index], rcond=1e-12)[0]
            fitted_level_partial_sum = error[index] - target_design @ estimate[:4]
            normalized_level_design = np.column_stack(
                (
                    np.ones(grid_points),
                    capital[index],
                    wage[index],
                    capital[index] * wage[index],
                )
            )
            fitted_level_residual = (
                error_innovations[index]
                - normalized_level_design @ estimate[:4] / math.sqrt(grid_points)
            )
            bandwidth = max(1, int(math.floor(bandwidth_ratio * grid_points)))
            fixed_b_lrv = bartlett_long_run_variance(
                fitted_level_residual, bandwidth
            )
            values.append(
                float(np.mean(fitted_level_partial_sum**2) / fixed_b_lrv)
            )
    array = np.asarray(values)
    return {
        "q90": float(np.quantile(array, 0.90)),
        "q95": float(np.quantile(array, 0.95)),
        "q99": float(np.quantile(array, 0.99)),
    }
