"""permutation.py — 基因集置换校准（论文核心方法）。

问题：签名审计通常用样本级检验（配对 Wilcoxon）+ 名义 α，忽略"签名是一组相关特征"
这一事实。随机基因集在名义 5% 下的假阳性率可达 12–25%。

方法：用同规模随机基因集构造零分布，计算置换 p 值：
    p = (1 + #{null >= observed}) / (B + 1)   （上调方向；下调取反向）

用法：
    from pilot.permutation import calibrate_claim
    result = calibrate_claim(deltas, genes, n_null=2000, direction="up")
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def build_null(deltas: pd.DataFrame, size: int, n_null: int = 2000,
               seed: int = 0) -> np.ndarray:
    """用随机基因集构造签名效应的零分布。

    deltas: 配对差值矩阵（pairs × features）
    size:   签名规模（与待检验签名一致）
    返回:   n_null 个随机签名的平均配对效应
    """
    rng = np.random.default_rng(seed)
    n_features = deltas.shape[1]
    if size > n_features:
        raise ValueError(f"signature size {size} exceeds available features {n_features}")
    null = np.empty(n_null)
    values = deltas.values
    for i in range(n_null):
        idx = rng.choice(n_features, size, replace=False)
        null[i] = values[:, idx].mean(axis=1).mean()
    return null


def permutation_p(observed: float, null: np.ndarray, direction: str = "up") -> float:
    """单侧置换 p 值（含 +1 校正）。"""
    null = np.asarray(null)
    if direction == "up":
        hits = int(np.sum(null >= observed))
    elif direction == "down":
        hits = int(np.sum(null <= observed))
    else:
        raise ValueError("direction must be 'up' or 'down'")
    return (1 + hits) / (null.size + 1)


def calibrate_claim(deltas: pd.DataFrame, genes: list[str], n_null: int = 2000,
                    direction: str = "up", seed: int = 0) -> dict:
    """对单个签名做置换校准，返回观测效应、p 值与零分布统计。"""
    present = [g for g in genes if g in deltas.columns]
    if len(present) < 5:
        return {"n_genes": len(present), "observed": float("nan"),
                "p_perm": float("nan"), "null_mean": float("nan"),
                "null_sd": float("nan")}
    observed = float(deltas[present].mean(axis=1).values.mean())
    null = build_null(deltas, len(present), n_null=n_null, seed=seed)
    return {
        "n_genes": len(present),
        "observed": observed,
        "p_perm": permutation_p(observed, null, direction),
        "null_mean": float(null.mean()),
        "null_sd": float(null.std()),
    }


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="单签名置换校准（示例）")
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--metadata", required=True)
    ap.add_argument("--group-col", required=True)
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--pair-col", required=True)
    ap.add_argument("--signature", required=True, help="基因列表文件")
    ap.add_argument("--value-type", default="log", choices=["log", "counts"])
    ap.add_argument("--direction", default="up", choices=["up", "down"])
    ap.add_argument("--n-null", type=int, default=2000)
    args = ap.parse_args()

    from pathlib import Path

    from .audit import load_matrix, load_metadata, to_log2x

    expr = to_log2x(load_matrix(Path(args.matrix)), args.value_type)
    meta = load_metadata(Path(args.metadata))
    meta["sample_id"] = meta["sample_id"].astype(str)
    deltas = []
    for _, grp in meta.groupby(args.pair_col):
        a = grp[grp[args.group_col] == args.a]["sample_id"]
        b = grp[grp[args.group_col] == args.b]["sample_id"]
        if len(a) == 1 and len(b) == 1:
            deltas.append(expr[a.iloc[0]] - expr[b.iloc[0]])
    genes = [ln.strip() for ln in Path(args.signature).read_text().splitlines() if ln.strip()]
    print(calibrate_claim(pd.DataFrame(deltas), genes, n_null=args.n_null,
                          direction=args.direction))