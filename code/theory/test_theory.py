from __future__ import annotations

import json

from code.theory.run import Config, run_t01, run_t04, run_t05


def test_fwl_identity_and_noncommutation(tmp_path):
    config = Config(20260723, 100, (50, 100), 50, tmp_path)
    [path] = run_t04(config)
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["fwl_identity_passes"]
    assert result["noncommutation_detected"]


def test_scaling_and_residual_smoke_outputs(tmp_path):
    config = Config(20260723, 100, (50, 100), 50, tmp_path)
    t01_paths = run_t01(config)
    t05_paths = run_t05(config)
    assert len(t01_paths) == 3
    assert len(t05_paths) == 2
    assert all(path.is_file() and path.stat().st_size for path in t01_paths + t05_paths)
