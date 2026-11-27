"""closed_loop 测试：verifier 与任务包 fixtures 对齐（M1 地基）。

对齐目标（与 provenance.json 记录一致）：positive→1，overclaim/missing_ridge/stale→0。
fixture 脚本原始内容写死 /workspace；测试在临时目录执行（sed 替换路径），
不修改原任务包文件。
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from closed_loop.verifier import verify_file

TASKS = Path(__file__).resolve().parents[1] / "datasets" / "DiscoveryRSI-Hypothesis-Task-Examples" / "task-packages" / "DiscoveryRSI-Hypothesis-Task-Examples" / "tasks"
TASK_DIR = TASKS / "unc106238-context-response"

FIXTURE_EXPECTATIONS = {
    "positive_fixture.sh": 1,
    "overclaim_fixture.sh": 0,
    "missing_ridge_fixture.sh": 0,
    "stale_result_fixture.sh": 0,
}


def _run_fixture(fixture_name: str, tmp_path: Path) -> Path:
    """在临时目录执行 fixture 脚本，返回其写入的 results.json 路径。"""
    src = (TASK_DIR / "validation" / fixture_name).read_text(encoding="utf-8")
    script = src.replace("/workspace", str(tmp_path))
    script_path = tmp_path / fixture_name
    script_path.write_text(script, encoding="utf-8")
    subprocess.run(["bash", str(script_path)], check=True, capture_output=True)
    return tmp_path / "results.json"


@pytest.mark.parametrize("fixture,expected_reward", list(FIXTURE_EXPECTATIONS.items()))
def test_fixture_alignment(fixture: str, expected_reward: int, tmp_path: Path):
    results_path = _run_fixture(fixture, tmp_path)
    reward, errors = verify_file(results_path)
    assert reward == expected_reward, f"{fixture}: expected reward={expected_reward}, got {reward}, errors={errors}"


def test_missing_results_file_yields_zero(tmp_path: Path):
    reward, errors = verify_file(tmp_path / "nonexistent.json")
    assert reward == 0
    assert errors[0].startswith("Failed to parse")


def test_invalid_outcome_rejected(tmp_path: Path):
    import json

    results = {
        "program": {"criteria": {}, "genes": ["G1"]},
        "baseline": {"context_contrast": 0.1},
        "ridge": {"context_coefficient": 0.1, "composition_robust": True},
        "outcome": "proven",
        "justification": "ok",
        "limitations": "Exploratory; does not establish direct target causality.",
    }
    p = tmp_path / "r.json"
    p.write_text(json.dumps(results))
    reward, errors = verify_file(p)
    assert reward == 0
    assert any("Invalid outcome" in e for e in errors)


def test_overclaim_wording_rejected(tmp_path: Path):
    """justification 声明 'direct target causality is established' 必须被拒（规则 9）。"""
    import json

    results = {
        "program": {"criteria": {}, "genes": ["G1"]},
        "baseline": {"context_contrast": 0.1},
        "ridge": {"context_coefficient": 0.1, "composition_robust": True},
        "outcome": "supportive",
        "justification": "The analysis establishes direct target causality.",
        "limitations": "Exploratory.",
    }
    p = tmp_path / "r.json"
    p.write_text(json.dumps(results))
    reward, errors = verify_file(p)
    assert reward == 0
    assert any("overclaims" in e for e in errors)