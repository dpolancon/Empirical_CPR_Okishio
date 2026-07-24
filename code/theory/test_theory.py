from __future__ import annotations

import json
import numpy as np

from code.theory.advanced import run_t03_local, run_t05_local, run_t06_local
from code.theory.imols import (
    BETA,
    fit_cross_product_imols,
    fixed_state_targets,
    level_design,
    simulate_dgp,
)
from code.theory.run import Config, run_t01, run_t04


def test_fwl_identity_and_noncommutation(tmp_path):
    config = Config(20260723, 100, (50, 100), 50, tmp_path)
    [path] = run_t04(config)
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["fwl_identity_passes"]
    assert result["noncommutation_detected"]


def test_scaling_and_residual_smoke_outputs(tmp_path):
    config = Config(20260723, 100, (50, 100), 50, tmp_path)
    t01_paths = run_t01(config)
    t05_paths = run_t05_local(config)
    assert len(t01_paths) == 3
    assert len(t05_paths) == 4
    assert all(path.is_file() and path.stat().st_size for path in t01_paths + t05_paths)


def test_exact_lagged_interaction_and_correct_state_target():
    capital = np.array([1.0, 2.0, 3.0])
    wage_share = np.array([0.4, 0.5, 0.6])
    design = level_design(capital, wage_share)
    np.testing.assert_allclose(design[:, 3], [0.0, 0.8, 1.5])
    theta, gap = fixed_state_targets(np.array([0.0, 0.8, 0.0, -0.2]), 0.5)
    assert np.isclose(theta, 0.7)
    assert np.isclose(gap, -0.2)


def test_imols_rank_gate_refuses_singular_common_trend():
    rng = np.random.default_rng(123)
    draw = simulate_dgp(rng, 100, scenario="singular-common-trend")
    fit = fit_cross_product_imols(draw.y, draw.capital, draw.wage_share)
    assert not fit.rank_supported


def test_local_task_smoke_artifacts(tmp_path):
    config = Config(
        20260723,
        12,
        (50, 100),
        12,
        tmp_path,
        limit_draws=50,
        bootstrap_replications=19,
    )
    paths = [
        *run_t03_local(config),
        *run_t06_local(config),
    ]
    assert all(path.is_file() and path.stat().st_size for path in paths)
    rows = (tmp_path / "t06-fixed-state-inference.csv").read_text(
        encoding="utf-8"
    )
    assert "theta" in rows and "gap" in rows
