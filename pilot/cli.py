"""cli.py — pilot 统一命令行入口。

用法：
  python -m pilot.cli <command> [args...]
  python -m pilot.cli datasets          # 列出已注册数据集
  python -m pilot.cli audit --claims ... --out ...
  python -m pilot.cli split-half --matrix ... --metadata ... --group-col ... --a ... --b ... --pair-col ...
  python -m pilot.cli matrix --de-file ... --cohorts ... --sizes 50,100,200 --out ...
  python -m pilot.cli cross --cohorts ... --size 100 --out ...
  python -m pilot.cli prepare-microarray --series-matrix ... --platform-annot ...
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from . import audit, cross_signature, prepare_microarray, replication_matrix, split_half

ROOT = Path(__file__).resolve().parent
DATASETS = ROOT / "datasets.json"

COMMANDS = {
    "audit": audit,
    "split-half": split_half,
    "matrix": replication_matrix,
    "cross": cross_signature,
    "prepare-microarray": prepare_microarray,
}

HELP = """pilot — 复现审计工具箱

命令:
  datasets            列出已注册的数据集
  audit               审计一组主张（signature / scan 模式）
  split-half          半样本协议（训练集选签名 → 留出集检验）
  matrix              多队列 × 多签名规模 复现矩阵
  cross               交叉签名矩阵（每队列自选签名互验）
  prepare-microarray  芯片数据预处理（series matrix + GPL 注释）

示例:
  python -m pilot.cli datasets
  python -m pilot.cli audit --claims pilot/claims.gse50760.json --out pilot/results/x.md
  python -m pilot.cli audit --claims ... --alpha-sweep 0.01,0.05,0.1
  python -m pilot.cli split-half --matrix pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz \\
      --metadata pilot/data/gse50760/design.json --group-col condition --a primary --b normal \\
      --pair-col patient --out pilot/results/split.md
"""


def list_datasets() -> None:
    if not DATASETS.exists():
        print("没有 datasets.json")
        return
    reg = json.loads(DATASETS.read_text(encoding="utf-8"))["datasets"]
    for name, d in reg.items():
        print(f"{name:12s} {d.get('omics','?'):10s} {d.get('n_samples','?'):>4} 样本  {d.get('note','')}")
        print(f"             matrix={d.get('matrix')}")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(HELP)
        return
    cmd = sys.argv[1]
    if cmd == "datasets":
        list_datasets()
        return
    mod = COMMANDS.get(cmd)
    if mod is None:
        print(f"未知命令: {cmd}\n")
        print(HELP)
        sys.exit(1)
    # 把剩余参数交给对应模块的 main()
    sys.argv = [f"pilot {cmd}"] + sys.argv[2:]
    mod.main()


if __name__ == "__main__":
    main()