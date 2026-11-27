"""verifier.py — 结果验证器，移植自目标任务包 tests/test.sh（逐条等价）。

语义与容器内一致：
  - 检查 /workspace/results.json 的 10 项规则（见规格书第 6 节）；
  - 通过 → reward=1，不通过 → reward=0；
  - 容器内版本无论结果如何进程都 exit 0，把 0/1 写入 reward 文件。

CLI 用法（本机）：
  python -m closed_loop.verifier --results <results.json> [--reward-out <file>]
  不带 --reward-out 时：exit 0=通过，exit 1=未通过（便于脚本与 pytest 使用）。
  带 --reward-out 时：模拟容器行为，恒 exit 0，写 reward 文件。

fixture 对齐（M1 验收，期望 1/0/0/0）：
  positive_fixture.sh / overclaim_fixture.sh / missing_ridge_fixture.sh / stale_result_fixture.sh
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_KEYS = ["program", "baseline", "ridge", "outcome", "limitations"]
VALID_OUTCOMES = {"supportive", "adverse", "inconclusive"}


def check_results(results: dict) -> list[str]:
    """对 results.json 的解析结果执行 10 项检查，返回错误列表（空 = 通过）。"""
    errors: list[str] = []

    # (1) 顶层键齐全
    for key in REQUIRED_KEYS:
        if key not in results:
            errors.append(f"Missing required key: {key}")

    # (2) outcome 合法
    outcome = results.get("outcome")
    if outcome not in VALID_OUTCOMES:
        errors.append(f"Invalid outcome: {outcome}")

    # (3) program 是 dict 且含 criteria、genes
    program = results.get("program", {})
    if not isinstance(program, dict):
        errors.append("program is not a dict")
    else:
        if "criteria" not in program:
            errors.append("program missing criteria")
        if "genes" not in program:
            errors.append("program missing genes")

    # (4) baseline 是 dict 且含 context_contrast
    baseline = results.get("baseline", {})
    if not isinstance(baseline, dict):
        errors.append("baseline is not a dict")
    else:
        if "context_contrast" not in baseline:
            errors.append("baseline missing context_contrast")

    # (5) ridge 是 dict 且含 context_coefficient、composition_robust
    ridge = results.get("ridge", {})
    if not isinstance(ridge, dict):
        errors.append("ridge is not a dict")
    else:
        if "context_coefficient" not in ridge:
            errors.append("ridge missing context_coefficient")
        if "composition_robust" not in ridge:
            errors.append("ridge missing composition_robust")

    # (6) limitations 非空字符串
    limitations = results.get("limitations", "")
    if not isinstance(limitations, str) or len(limitations.strip()) == 0:
        errors.append("limitations is empty or not a string")

    # (7) 防过度声称：outcome=supportive 时 ridge.composition_robust 必须为 True
    if outcome == "supportive" and not ridge.get("composition_robust", False):
        errors.append("Outcome is supportive but ridge composition_robust is False")

    # (8) justification 非空字符串
    justification = results.get("justification", "")
    if not isinstance(justification, str) or len(justification.strip()) == 0:
        errors.append("justification is empty or not a string")

    # (9) 防过度声称：justification 措辞检查
    just_text = justification.lower()
    if "causality is established" in just_text or (
        "direct target causality" in just_text and "does not" not in just_text
    ):
        errors.append("Justification overclaims direct target causality")

    return errors


def verify_file(results_path: str | Path) -> tuple[int, list[str]]:
    """读取并检查 results.json，返回 (reward 0/1, errors)。"""
    try:
        with open(results_path, encoding="utf-8") as f:
            results = json.load(f)
    except Exception as exc:  # 与 test.sh 的 try/except 行为一致
        return 0, [f"Failed to parse results.json: {exc}"]
    errors = check_results(results)
    return (1, []) if not errors else (0, errors)


def main() -> None:
    ap = argparse.ArgumentParser(description="DiscoveryRSI closed-loop verifier")
    ap.add_argument("--results", required=True, help="results.json 路径")
    ap.add_argument("--reward-out", default=None, help="容器模式：把 0/1 写入该文件（恒 exit 0）")
    args = ap.parse_args()

    reward, errors = verify_file(args.results)
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
    else:
        print("Verifier passed")

    if args.reward_out:
        Path(args.reward_out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.reward_out, "w", encoding="utf-8") as f:
            f.write(str(reward))
        sys.exit(0)
    sys.exit(0 if reward == 1 else 1)


if __name__ == "__main__":
    main()