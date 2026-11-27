"""exp_realcal.py — 真实签名在置换校准下是否仍显著？"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
from pilot.audit import load_matrix, load_metadata, to_log2x

ROOT=Path(__file__).resolve().parents[1]
C = {
 "GSE50760": dict(matrix="pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz", meta="pilot/data/gse50760/design.json", value_type="log", col="condition", a="primary", b="normal", pair="patient"),
 "GSE95132": dict(matrix="pilot/data/gse95132/GSE95132_counts.tsv.gz", meta="pilot/data/gse95132/design.json", value_type="counts", col="tissue", a="tumor", b="adjacent", pair="patient"),
 "GSE110224": dict(matrix="pilot/data/gse110224/matrix.tsv.gz", meta="pilot/data/gse110224/design.json", value_type="log", col="condition", a="cancer", b="normal", pair="patient"),
}
SIZE=100; N_NULL=2000; rng=np.random.default_rng(11)

def load(cfg):
    expr=to_log2x(load_matrix(Path(cfg["matrix"])),cfg["value_type"])
    meta=load_metadata(Path(cfg["meta"])); meta["sample_id"]=meta["sample_id"].astype(str)
    ds=[]
    for key,grp in meta.groupby(cfg["pair"]):
        a=grp[grp[cfg["col"]]==cfg["a"]]["sample_id"]; b=grp[grp[cfg["col"]]==cfg["b"]]["sample_id"]
        if len(a)==1 and len(b)==1: ds.append(expr[a.iloc[0]]-expr[b.iloc[0]])
    return expr, pd.DataFrame(ds)

def stats_of(deltas):
    m=deltas.mean(axis=0); sd=deltas.std(axis=0,ddof=1).replace(0,np.nan)
    return pd.DataFrame({"mean":m,"t":m/sd,
        "cons":(np.sign(deltas)==np.sign(m)).sum(axis=0)/len(deltas)})

def main():
    data={k:load(cfg) for k,cfg in C.items()}
    common=sorted(set.intersection(*[set(d[0].index) for d in data.values()]))
    print("common:",len(common))
    rows=[]
    for src in C:
        st=stats_of(data[src][1])
        for crit in ("effect","tstat"):
            for direction in ("up","down"):
                sign=1 if direction=="up" else -1
                key=(st["mean"]*sign) if crit=="effect" else (st["t"]*sign)
                key=key[key>0].sort_values(ascending=False).head(SIZE)
                genes=[g for g in key.index if g in common]
                if len(genes)<10: continue
                for tgt in C:
                    deltas=data[tgt][1][genes]
                    obs=deltas.mean(axis=1).values.mean()
                    G=len(common)
                    null=np.array([data[tgt][1].iloc[:, rng.choice(G,SIZE,replace=False)].mean(axis=1).values.mean() for _ in range(N_NULL)])
                    p=(np.sum(null>=obs)+1)/(N_NULL+1) if obs>0 else (np.sum(null<=obs)+1)/(N_NULL+1)
                    rows.append(dict(source=src,criterion=crit,direction=direction,target=tgt,
                                     effect=round(float(obs),3),p_perm=p))
    df=pd.DataFrame(rows)
    df.to_csv(ROOT/"paper"/"realcal.csv",index=False)
    lines=["# 真实签名的置换校准结果","",
           "| 来源 | 标准 | 方向 | 目标 | 效应 | p_perm |","|---|---|---|---|---|---|"]
    for _,r in df.iterrows():
        lines.append(f"| {r.source} | {r.criterion} | {r.direction} | {r.target} | {r.effect:+.3f} | {r.p_perm:.2g} |")
    out=ROOT/"paper"/"exp_realcal_results.md"; out.write_text("\n".join(lines),encoding="utf-8")
    print(df.to_string(index=False)); print("wrote",out)

if __name__=="__main__": main()
