"""exp_transfer.py — 留一队列验证 "transfer-optimized signature"。

协议：
  对每个留出队列 T：用另外两个队列（训练）计算基因级转移分数
    transfer_score = 平均效应 × 方向一致比例（训练队列间）
  选 top-N（上/下调），在 T 上检验，测效应保留率。
  对照：用单个训练队列、按效应量选 top-N。
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from pilot.audit import load_matrix, load_metadata, to_log2x

ROOT = Path(__file__).resolve().parents[1]
COHORTS = {
    "GSE50760": dict(matrix="pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz", meta="pilot/data/gse50760/design.json", value_type="log", col="condition", a="primary", b="normal", pair="patient"),
    "GSE95132": dict(matrix="pilot/data/gse95132/GSE95132_counts.tsv.gz", meta="pilot/data/gse95132/design.json", value_type="counts", col="tissue", a="tumor", b="adjacent", pair="patient"),
    "GSE110224": dict(matrix="pilot/data/gse110224/matrix.tsv.gz", meta="pilot/data/gse110224/design.json", value_type="log", col="condition", a="cancer", b="normal", pair="patient"),
}
SIZES = [50, 100, 200]
ALPHA, MIN_STABLE = 0.05, 0.8

def load(cfg):
    expr = to_log2x(load_matrix(Path(cfg["matrix"])), cfg["value_type"])
    meta = load_metadata(Path(cfg["meta"])); meta["sample_id"] = meta["sample_id"].astype(str)
    ds, pairs = [], []
    for key, grp in meta.groupby(cfg["pair"]):
        a = grp[grp[cfg["col"]] == cfg["a"]]["sample_id"]; b = grp[grp[cfg["col"]] == cfg["b"]]["sample_id"]
        if len(a) == 1 and len(b) == 1:
            ds.append(expr[a.iloc[0]] - expr[b.iloc[0]]); pairs.append(str(key))
    return expr, pd.DataFrame(ds), pairs

def stats_of(deltas):
    mean = deltas.mean(axis=0)
    sd = deltas.std(axis=0, ddof=1).replace(0, np.nan)
    t = mean / sd
    cons = (np.sign(deltas) == np.sign(mean)).sum(axis=0) / len(deltas)
    return pd.DataFrame({"mean": mean, "t": t, "cons": cons})

def select(stats_map, common, criterion, direction, n):
    sign = 1 if direction == "up" else -1
    frames = []
    for name, st in stats_map.items():
        s = st.loc[common].copy()
        frames.append(s[["mean", "t", "cons"]].add_prefix(f"{name}_"))
    allf = pd.concat(frames, axis=1)
    if criterion == "transfer":
        means = sum(allf[f"{k}_mean"] for k in stats_map) / len(stats_map)
        signs = sum(np.sign(allf[f"{k}_mean"]) for k in stats_map) / len(stats_map)
        score = means * signs  # 方向一致才加分
        sel = score[score * sign > 0]
        return sel.sort_values(ascending=False).head(n).index.tolist()
    else:  # effect：单队列
        k = next(iter(stats_map))
        s = stats_map[k].loc[common]
        key = s["mean"] * sign
        return key[key > 0].sort_values(ascending=False).head(n).index.tolist()

def test_on(expr, deltas, pairs, genes, direction):
    present = [g for g in genes if g in expr.index]
    if len(present) < 5:
        return dict(verdict="inconclusive", effect=np.nan, p=np.nan, loo=0.0, n=0)
    vals = deltas[present].mean(axis=1).values
    effect = float(vals.mean())
    p = float(stats.wilcoxon(vals).pvalue) if len(vals) >= 3 else np.nan
    loo = 0
    for i in range(len(vals)):
        sub = np.delete(vals, i)
        try: pi = float(stats.wilcoxon(sub).pvalue)
        except ValueError: pi = np.nan
        if np.isfinite(pi) and pi < ALPHA and ((sub.mean() > 0) == (direction == "up")): loo += 1
    loo /= max(len(vals), 1)
    ok = np.isfinite(p) and p < ALPHA and ((effect > 0) == (direction == "up"))
    verdict = "not_reproduced" if not ok else ("robust" if loo >= MIN_STABLE else "fragile")
    return dict(verdict=verdict, effect=effect, p=p, loo=loo, n=len(present))

def main():
    data = {k: load(cfg) for k, cfg in COHORTS.items()}
    common = set(data["GSE50760"][0].index)
    for k in data: common &= set(data[k][0].index)
    common = sorted(common)
    rows = []
    for T in COHORTS:
        train = [k for k in COHORTS if k != T]
        for size in SIZES:
            for direction in ("up", "down"):
                # transfer：两训练队列
                sm = {k: stats_of(data[k][1]) for k in train}
                g_transfer = select(sm, common, "transfer", direction, size)
                r = test_on(*data[T][:3], g_transfer, direction)
                rows.append(dict(target=T, criterion="transfer", size=size, direction=direction, **r))
                # baseline effect：第一个训练队列
                g_effect = select({train[0]: sm[train[0]]}, common, "effect", direction, size)
                r2 = test_on(*data[T][:3], g_effect, direction)
                rows.append(dict(target=T, criterion="effect", size=size, direction=direction, **r2))
    df = pd.DataFrame(rows)
    out = ROOT / "paper" / "exp_transfer_results.md"
    lines = ["# 留一队列：transfer-optimized vs effect-ranked", "",
             "| 留出队列 | 规模 | 方向 | 标准 | 判定 | 效应 | p | LOO |", "|---|---|---|---|---|---|---|---|"]
    for _, r in df.iterrows():
        lines.append(f"| {r.target} | {r['size']} | {r.direction} | {r.criterion} | {r.verdict} | {r.effect:+.3f} | {r.p:.3g} | {r.loo:.2f} |")
    lines += ["", "## 汇总（判定 robust 比例 / 平均 |效应|）", "",
              "| 标准 | robust 比例 | 平均 |效应| |", "|---|---|---|"]
    for crit in ("transfer", "effect"):
        sub = df[df.criterion == crit]
        rate = (sub.verdict == "robust").mean()
        lines.append(f"| {crit} | {rate:.2f} | {sub.effect.abs().mean():.3f} |")
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[-8:]))
    print("wrote", out)

if __name__ == "__main__":
    main()
