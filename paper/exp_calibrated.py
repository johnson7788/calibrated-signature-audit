"""exp_calibrated.py — 基因集置换校准能否恢复错误控制？

对每个队列：
  1) 预计算配对 delta（pairs × genes）；
  2) 抽 2000 个随机签名（size 100）构成零分布池；
  3) 另抽 500 个随机"主张"，计算置换 p（相对零分布池），统计 FPR；
  4) 对真实签名（effect/tstat top-100）计算置换 p，看是否仍显著。
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
from pilot.audit import load_matrix, load_metadata, to_log2x

ROOT = Path(__file__).resolve().parents[1]
C = {
 "GSE50760": dict(matrix="pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz", meta="pilot/data/gse50760/design.json", value_type="log", col="condition", a="primary", b="normal", pair="patient"),
 "GSE95132": dict(matrix="pilot/data/gse95132/GSE95132_counts.tsv.gz", meta="pilot/data/gse95132/design.json", value_type="counts", col="tissue", a="tumor", b="adjacent", pair="patient"),
 "GSE110224": dict(matrix="pilot/data/gse110224/matrix.tsv.gz", meta="pilot/data/gse110224/design.json", value_type="log", col="condition", a="cancer", b="normal", pair="patient"),
}
SIZE=100; N_NULL=2000; N_TEST=500

def load(cfg):
    expr = to_log2x(load_matrix(Path(cfg["matrix"])), cfg["value_type"])
    meta = load_metadata(Path(cfg["meta"])); meta["sample_id"]=meta["sample_id"].astype(str)
    ds=[]
    for key,grp in meta.groupby(cfg["pair"]):
        a=grp[grp[cfg["col"]]==cfg["a"]]["sample_id"]; b=grp[grp[cfg["col"]]==cfg["b"]]["sample_id"]
        if len(a)==1 and len(b)==1: ds.append(expr[a.iloc[0]]-expr[b.iloc[0]])
    return expr, pd.DataFrame(ds)

def score(deltas, idx):
    return deltas.iloc[:, idx].mean(axis=1).values.mean()

def main():
    rng=np.random.default_rng(7)
    rows=[]
    for name,cfg in C.items():
        expr, deltas = load(cfg)
        genes=np.array(deltas.columns); G=len(genes)
        # 零分布池
        null_scores=np.array([score(deltas, rng.choice(G,SIZE,replace=False)) for _ in range(N_NULL)])
        # 随机主张的置换 p（单侧，效应>=观测）
        fprs={}
        for a in (0.01,0.05,0.1):
            hits=0
            for _ in range(N_TEST):
                idx=rng.choice(G,SIZE,replace=False)
                s=score(deltas,idx)
                p=(np.sum(null_scores>=s)+1)/(N_NULL+1)
                hits+= (p<a)
            fprs[a]=hits/N_TEST
        rows.append(dict(cohort=name, **{f"fpr_perm_{int(k*100):03d}":v for k,v in fprs.items()},
                         null_mean=float(null_scores.mean()), null_sd=float(null_scores.std())))
        print(name, fprs)
    df=pd.DataFrame(rows); df.to_csv(ROOT/"paper"/"calibration_perm.csv", index=False)
    lines=["# 基因集置换校准后的假阳性率","",
           f"零分布池 N={N_NULL}，检验主张 N={N_TEST}，规模 top-{SIZE}。","",
           "| 队列 | perm-alpha=0.01 | 0.05 | 0.10 |","|---|---|---|---|"]
    for _,r in df.iterrows():
        lines.append(f"| {r.cohort} | {r['fpr_perm_001']:.2%} | {r['fpr_perm_005']:.2%} | {r['fpr_perm_010']:.2%} |")
    out=ROOT/"paper"/"exp_calibrated_results.md"; out.write_text("\n".join(lines),encoding="utf-8")
    print("\n".join(lines)); print("wrote",out)

if __name__=="__main__": main()
