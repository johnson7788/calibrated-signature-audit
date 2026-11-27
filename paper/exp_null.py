"""exp_null.py — 审计协议的零分布校准：随机签名会被判 robust 的比例（假阳性率）。

H0：签名与随机基因集等价。对每个队列，抽 N 个随机签名（固定规模），
按当前协议（alpha=0.05, LOO>=0.8, 方向固定）判定，统计 robust 比例。
再扫描不同 alpha/LOO 阈值，给出校准后的阈值。
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from pilot.audit import load_matrix, load_metadata, to_log2x

ROOT = Path(__file__).resolve().parents[1]
C = {
 "GSE50760": dict(matrix="pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz", meta="pilot/data/gse50760/design.json", value_type="log", col="condition", a="primary", b="normal", pair="patient"),
 "GSE95132": dict(matrix="pilot/data/gse95132/GSE95132_counts.tsv.gz", meta="pilot/data/gse95132/design.json", value_type="counts", col="tissue", a="tumor", b="adjacent", pair="patient"),
 "GSE110224": dict(matrix="pilot/data/gse110224/matrix.tsv.gz", meta="pilot/data/gse110224/design.json", value_type="log", col="condition", a="cancer", b="normal", pair="patient"),
}
N = 500
SIZE = 100
ALPHAS = [0.01, 0.05, 0.10]
MIN_STABLES = [0.6, 0.8, 1.0]

def load(cfg):
    expr = to_log2x(load_matrix(Path(cfg["matrix"])), cfg["value_type"])
    meta = load_metadata(Path(cfg["meta"])); meta["sample_id"]=meta["sample_id"].astype(str)
    ds=[]
    for key,grp in meta.groupby(cfg["pair"]):
        a=grp[grp[cfg["col"]]==cfg["a"]]["sample_id"]; b=grp[grp[cfg["col"]]==cfg["b"]]["sample_id"]
        if len(a)==1 and len(b)==1: ds.append(expr[a.iloc[0]]-expr[b.iloc[0]])
    return expr, pd.DataFrame(ds)

def test_sig(deltas, genes, alpha, min_stable):
    v = deltas[[g for g in genes if g in deltas.columns]].mean(axis=1).values
    if len(v) < 5: return False
    try: p = stats.wilcoxon(v).pvalue
    except ValueError: return False
    if not (p < alpha and v.mean() > 0): return False
    loo = 0
    for i in range(len(v)):
        sub = np.delete(v, i)
        try: pi = stats.wilcoxon(sub).pvalue
        except ValueError: pi = np.nan
        if np.isfinite(pi) and pi < alpha and sub.mean() > 0: loo += 1
    return loo / len(v) >= min_stable

def main():
    rng = np.random.default_rng(42)
    rows=[]
    for name,cfg in C.items():
        expr, deltas = load(cfg)
        genes = list(expr.index)
        sigs = [list(rng.choice(genes, SIZE, replace=False)) for _ in range(N)]
        for alpha in ALPHAS:
            for ms in MIN_STABLES:
                fpr = np.mean([test_sig(deltas, s, alpha, ms) for s in sigs])
                rows.append(dict(cohort=name, alpha=alpha, min_stable=ms, fpr=fpr))
    df = pd.DataFrame(rows)
    df.to_csv(ROOT/"paper"/"null_calibration.csv", index=False)
    lines=["# 零分布校准：随机签名的假阳性率（FPR）","",
           f"N={N} 随机签名/队列，规模 top-{SIZE}，方向固定为上调（等价于单侧）。","",
           "| 队列 | alpha | min_stable | FPR |","|---|---|---|---|"]
    for _,r in df.iterrows():
        lines.append(f"| {r.cohort} | {r.alpha} | {r.min_stable} | {r.fpr:.3%} |")
    # 校准建议：找每个队列 FPR<=5% 的最宽松组合
    lines += ["","## 校准建议（FPR ≤ 5% 的最宽松阈值）","","| 队列 | alpha | min_stable | FPR |","|---|---|---|---|"]
    for name in C:
        sub = df[(df.cohort==name) & (df.fpr<=0.05)].sort_values(["alpha","min_stable"], ascending=[False,True])
        if len(sub):
            r=sub.iloc[0]; lines.append(f"| {name} | {r.alpha} | {r.min_stable} | {r.fpr:.3%} |")
        else:
            lines.append(f"| {name} | 无满足组合 | - | - |")
    out=ROOT/"paper"/"exp_null_results.md"; out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[-10:])); print("wrote", out)

if __name__=="__main__": main()
