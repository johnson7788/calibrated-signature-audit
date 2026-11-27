"""exp_selection.py — 创新假设实验：签名选择标准 → 跨队列可迁移性。

假设 H1：在固定签名规模下，按"效应量 × 跨配对稳定性"选基因（stability-weighted），
         比按"效应量绝对值"选基因（effect-ranked）在独立队列中保留更高效应。

做法：
  1) 三个队列各自计算配对 delta（a-b），取基因交集；
  2) 以 GSE50760 为来源，用 4 种标准各选 top-100 上/下调基因；
  3) 在三个队列分别检验签名（配对 Wilcoxon + LOO），计算：
     - 判定（robust/fragile/not_reproduced）
     - 效应保留率 = 目标队列效应 / 来源队列效应
  4) 输出对比表。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from pilot.audit import load_matrix, load_metadata, to_log2x

ROOT = Path(__file__).resolve().parents[1]

COHORTS = {
    "GSE50760": dict(matrix="pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz",
                     meta="pilot/data/gse50760/design.json", value_type="log",
                     col="condition", a="primary", b="normal", pair="patient"),
    "GSE95132": dict(matrix="pilot/data/gse95132/GSE95132_counts.tsv.gz",
                     meta="pilot/data/gse95132/design.json", value_type="counts",
                     col="tissue", a="tumor", b="adjacent", pair="patient"),
    "GSE110224": dict(matrix="pilot/data/gse110224/matrix.tsv.gz",
                      meta="pilot/data/gse110224/design.json", value_type="log",
                      col="condition", a="cancer", b="normal", pair="patient"),
}
SIZE = 100
MIN_STABLE = 0.8
ALPHA = 0.05


def load_cohort(cfg: dict):
    expr = to_log2x(load_matrix(Path(cfg["matrix"])), cfg["value_type"])
    meta = load_metadata(Path(cfg["meta"]))
    meta["sample_id"] = meta["sample_id"].astype(str)
    deltas, pairs = [], []
    for key, grp in meta.groupby(cfg["pair"]):
        a = grp[grp[cfg["col"]] == cfg["a"]]["sample_id"]
        b = grp[grp[cfg["col"]] == cfg["b"]]["sample_id"]
        if len(a) == 1 and len(b) == 1:
            deltas.append(expr[a.iloc[0]] - expr[b.iloc[0]])
            pairs.append(str(key))
    return expr, pd.DataFrame(deltas), pairs, meta, cfg


def signature_stats(expr, deltas, pairs):
    mean_d = deltas.mean(axis=0)
    sd_d = deltas.std(axis=0, ddof=1).replace(0, np.nan)
    consistency = (np.sign(deltas) == np.sign(mean_d)).sum(axis=0) / len(deltas)
    tstat = mean_d / sd_d
    return pd.DataFrame({"mean": mean_d, "sd": sd_d, "consistency": consistency, "t": tstat})


def pick(stats_df: pd.DataFrame, criterion: str, direction: str, n: int) -> list[str]:
    df = stats_df.copy()
    sign = 1 if direction == "up" else -1
    df = df[df["mean"] * sign > 0]  # 只选方向一致的
    if criterion == "effect":
        key = df["mean"] * sign
    elif criterion == "tstat":
        key = df["t"] * sign
    elif criterion == "stability":
        key = (df["mean"] * sign) * df["consistency"]
    elif criterion == "consistency":
        key = df["consistency"] * 1000 + (df["mean"] * sign)
    else:
        raise ValueError(criterion)
    return key.sort_values(ascending=False).head(n).index.tolist()


def audit(expr, deltas, pairs, genes, direction: str) -> dict:
    present = [g for g in genes if g in expr.index]
    if len(present) < 5:
        return {"verdict": "inconclusive", "effect": float("nan"), "p": float("nan"), "loo": 0.0}
    score = expr.loc[present].mean(axis=0)
    deltas_s = []
    for p in pairs:
        # 用该队列已有的配对结构：deltas 行就是配对，但需要 sample ids；改为直接从 deltas 重建
        pass
    # 直接用基因级 deltas 的行顺序与得分差等价：score delta = mean over genes of (a-b)
    vals = deltas[present].mean(axis=1).values
    effect = float(vals.mean())
    if len(vals) < 3:
        return {"verdict": "inconclusive", "effect": effect, "p": float("nan"), "loo": 0.0}
    try:
        p = float(stats.wilcoxon(vals).pvalue)
    except ValueError:
        p = float("nan")
    direction_ok = (effect > 0) if direction == "up" else (effect < 0)
    loo_pass = 0
    for i in range(len(vals)):
        sub = np.delete(vals, i)
        try:
            pi = float(stats.wilcoxon(sub).pvalue)
        except ValueError:
            pi = float("nan")
        if np.isfinite(pi) and pi < ALPHA and ((sub.mean() > 0) == (direction == "up")):
            loo_pass += 1
    loo = loo_pass / len(vals)
    primary = bool(np.isfinite(p) and p < ALPHA and direction_ok)
    if not primary:
        verdict = "not_reproduced"
    elif loo >= MIN_STABLE:
        verdict = "robust"
    else:
        verdict = "fragile"
    return {"verdict": verdict, "effect": effect, "p": p, "loo": loo,
            "n_genes": len(present)}


def main():
    data = {}
    for name, cfg in COHORTS.items():
        expr, deltas, pairs, meta, _ = load_cohort(cfg)
        data[name] = dict(expr=expr, deltas=deltas, pairs=pairs, stats=signature_stats(expr, deltas, pairs))
        print(f"{name}: {len(pairs)} pairs, {expr.shape[0]} features")

    common = set(data["GSE50760"]["expr"].index)
    for name in data:
        common &= set(data[name]["expr"].index)
    common = sorted(common)
    print("common genes:", len(common))

    criteria = ["effect", "tstat", "stability", "consistency"]
    rows = []
    for crit in criteria:
        for direction in ("up", "down"):
            genes = pick(data["GSE50760"]["stats"].loc[common], crit, direction, SIZE)
            for target in COHORTS:
                res = audit(data[target]["expr"], data[target]["deltas"], data[target]["pairs"],
                            genes, direction)
                src_effect = None
                rows.append({
                    "criterion": crit, "direction": direction, "target": target,
                    "verdict": res["verdict"], "effect": round(res["effect"], 3),
                    "p": res["p"], "loo": round(res["loo"], 2),
                })
    df = pd.DataFrame(rows)
    # 效应保留率（相对 GSE50760）
    base = df[df.target == "GSE50760"].set_index(["criterion", "direction"])["effect"]
    df["retention"] = df.apply(
        lambda r: round(r["effect"] / base.loc[(r["criterion"], r["direction"])], 2)
        if base.loc[(r["criterion"], r["direction"])] else np.nan, axis=1)

    out = ROOT / "paper" / "exp_selection_results.md"
    lines = ["# 实验：签名选择标准 × 跨队列可迁移性", "",
             f"来源队列 GSE50760；签名规模 top-{SIZE}；四标准对比；三个队列验证。", "",
             "| 标准 | 方向 | 目标队列 | 判定 | 效应 | p | LOO | 效应保留率 |",
             "|---|---|---|---|---|---|---|---|"]
    for _, r in df.iterrows():
        lines.append(f"| {r.criterion} | {r.direction} | {r.target} | {r.verdict} | "
                     f"{r.effect:+.3f} | {r.p:.3g} | {r.loo:.2f} | {r.retention:.2f} |")
    # 汇总：每个标准在非来源队列的平均保留率
    lines += ["", "## 汇总（非来源队列平均效应保留率）", "",
              "| 标准 | 上调 | 下调 |", "|---|---|---|"]
    for crit in criteria:
        vals = {}
        for direction in ("up", "down"):
            sub = df[(df.criterion == crit) & (df.direction == direction) & (df.target != "GSE50760")]
            vals[direction] = f"{sub['retention'].mean():.2f}"
        lines.append(f"| {crit} | {vals['up']} | {vals['down']} |")
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[-10:]))
    print("wrote", out)


if __name__ == "__main__":
    main()