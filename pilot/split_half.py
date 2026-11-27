"""split_half.py — 半样本（out-of-sample）审计协议，内置命令化。

流程：
  1) 按配对键把样本分成训练集 / 留出集；
  2) 只用训练集数据推导签名（每个基因的配对 delta 均值，取 top-N 上/下调）；
  3) 在留出集上检验签名（配对 Wilcoxon）+ 留一稳健性；
  4) 输出审计报告（含方法学元数据）。

用法：
  python -m pilot.split_half \
    --matrix pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz \
    --metadata pilot/data/gse50760/design.json \
    --group-col condition --a primary --b normal --pair-col patient \
    --top 100 --min-delta 1.5 --train-frac 0.5 \
    --out pilot/results/gse50760_split_half.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .audit import load_matrix, load_metadata, render_markdown, run_claims, to_log2x


def split_pairs(meta: pd.DataFrame, pair_col: str, group_col: str,
                a: str, b: str, train_frac: float) -> tuple[list[str], list[str]]:
    """按配对键顺序切分；返回 (训练配对键, 留出配对键)。只保留 A/B 各恰一个样本的配对。"""
    valid = []
    for key, grp in meta.groupby(pair_col):
        if (grp[group_col] == a).sum() == 1 and (grp[group_col] == b).sum() == 1:
            valid.append(str(key))
    valid = sorted(valid, key=lambda x: (len(x), x))
    n_train = max(1, min(len(valid) - 1, int(round(len(valid) * train_frac))))
    return valid[:n_train], valid[n_train:]


def derive_signature(expr: pd.DataFrame, meta: pd.DataFrame, pairs: list[str],
                     group_col: str, a: str, b: str, pair_col: str,
                     top: int, min_delta: float) -> tuple[list[str], list[str], pd.Series]:
    deltas = []
    for key in pairs:
        grp = meta[meta[pair_col].astype(str) == key]
        a_id = grp[grp[group_col] == a]["sample_id"].iloc[0]
        b_id = grp[grp[group_col] == b]["sample_id"].iloc[0]
        deltas.append(expr[a_id] - expr[b_id])
    D = pd.DataFrame(deltas)
    mean_d = D.mean(axis=0)
    up = mean_d[mean_d >= min_delta].nlargest(top).index.tolist()
    down = mean_d[mean_d <= -min_delta].nsmallest(top).index.tolist()
    return up, down, mean_d


def main() -> None:
    ap = argparse.ArgumentParser(description="半样本审计协议")
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--metadata", required=True)
    ap.add_argument("--value-type", default="log", choices=["log", "counts"])
    ap.add_argument("--group-col", required=True)
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--pair-col", required=True)
    ap.add_argument("--top", type=int, default=100)
    ap.add_argument("--min-delta", type=float, default=1.5)
    ap.add_argument("--train-frac", type=float, default=0.5)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--min-stable", type=float, default=0.8)
    ap.add_argument("--out", default="pilot/results/split_half.md")
    args = ap.parse_args()

    expr = to_log2x(load_matrix(Path(args.matrix)), args.value_type)
    meta = load_metadata(Path(args.metadata))
    meta["sample_id"] = meta["sample_id"].astype(str)

    train, test = split_pairs(meta, args.pair_col, args.group_col, args.a, args.b, args.train_frac)
    if not test:
        raise SystemExit("留出集为空：配对不足")

    up, down, _ = derive_signature(expr, meta, train, args.group_col, args.a, args.b,
                                   args.pair_col, args.top, args.min_delta)

    out_dir = Path(args.out).parent / "split_half_assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = Path(args.matrix).parent.name
    (out_dir / f"{tag}_up.txt").write_text("\n".join(up) + "\n", encoding="utf-8")
    (out_dir / f"{tag}_down.txt").write_text("\n".join(down) + "\n", encoding="utf-8")
    meta_test = meta[meta[args.pair_col].astype(str).isin(test)].to_dict("records")
    (out_dir / f"{tag}_design_test.json").write_text(json.dumps(meta_test, ensure_ascii=False, indent=1), encoding="utf-8")

    base = {
        "type": "signature",
        "dataset": {"matrix": args.matrix, "metadata": str(out_dir / f"{tag}_design_test.json"),
                     "value_type": args.value_type},
        "group": {"column": args.group_col, "a": args.a, "b": args.b, "paired_by": [args.pair_col]},
        "alpha": args.alpha,
        "min_effect": 0.5,
        "robustness": {"covariates": [], "min_stable_fraction": args.min_stable},
    }
    claims = [
        {**base, "id": "split-scan", "name": "留出集扫描", "type": "scan", "min_effect": 1.0},
        {**base, "id": "split-up", "name": "训练集上调签名 → 留出集",
         "claimed_direction": "a_gt_b", "signature": {"features_file": str(out_dir / f"{tag}_up.txt")}},
        {**base, "id": "split-down", "name": "训练集下调签名 → 留出集",
         "claimed_direction": "a_lt_b", "signature": {"features_file": str(out_dir / f"{tag}_down.txt")}},
    ]
    results = run_claims(claims)
    md = render_markdown(results)
    header = (f"# 半样本审计（out-of-sample）\n\n"
              f"- 训练配对：{len(train)}（{', '.join(train)}）\n"
              f"- 留出配对：{len(test)}（{', '.join(test)}）\n"
              f"- 签名规模：top-{args.top}，|delta|≥{args.min_delta}\n"
              f"- 阈值：alpha={args.alpha}，min_stable={args.min_stable}\n\n")
    md = header + md
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()